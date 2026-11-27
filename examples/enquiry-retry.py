import sqlite3
import unittest


def store():
    db = sqlite3.connect(":memory:")
    db.executescript("""
        CREATE TABLE enquiry (reference TEXT PRIMARY KEY, text TEXT NOT NULL);
        CREATE TABLE delivery (
            reference TEXT PRIMARY KEY REFERENCES enquiry(reference),
            draft_text TEXT NOT NULL,
            state TEXT NOT NULL,
            receipt TEXT
        );
    """)
    return db


def capture(db, reference, text, draft):
    with db:
        added = db.execute(
            "INSERT INTO enquiry VALUES (?, ?) ON CONFLICT(reference) DO NOTHING",
            (reference, text),
        ).rowcount
        saved = db.execute("SELECT text FROM enquiry WHERE reference=?", (reference,)).fetchone()
        if saved != (text,):
            raise ValueError("This reference belongs to a different enquiry")
        if added:
            db.execute(
                "INSERT INTO delivery (reference, draft_text, state) VALUES (?, ?, 'draft')",
                (reference, draft),
            )
    return reference


def approve(db, reference):
    with db:
        db.execute(
            "UPDATE delivery SET state='approved' WHERE reference=? AND state='draft'",
            (reference,),
        )


def attempt(db, reference, provider):
    with db:
        taken = db.execute(
            "UPDATE delivery SET state='unknown' WHERE reference=? AND state='approved'",
            (reference,),
        ).rowcount
    if taken:
        provider.accept_then_timeout(reference)
    return taken == 1


def reconcile(db, reference, provider):
    receipt = provider.receipts.get(reference)
    if receipt:
        with db:
            db.execute(
                "UPDATE delivery SET state='accepted', receipt=? WHERE reference=? AND state='unknown'",
                (receipt, reference),
            )


class FixtureProvider:
    def __init__(self):
        self.receipts = {}
        self.attempts = 0

    def accept_then_timeout(self, reference):
        self.attempts += 1
        self.receipts[reference] = f"receipt-{self.attempts}"
        raise TimeoutError("Connection closed after acceptance")


class RetryTest(unittest.TestCase):
    def setUp(self):
        self.db = store()
        self.addCleanup(self.db.close)
        self.provider = FixtureProvider()
        self.draft = "Thanks for your enquiry. I will review the website fix."
        self.reference = capture(self.db, "enquiry-1", "Quote a website fix", self.draft)

    def state(self):
        return self.db.execute(
            "SELECT state, receipt FROM delivery WHERE reference=?", (self.reference,)
        ).fetchone()

    def test_retry_keeps_one_enquiry_and_one_draft(self):
        retry = capture(self.db, self.reference, "Quote a website fix", "A new generated draft")
        self.assertEqual(retry, self.reference)
        self.assertEqual(self.db.execute("SELECT count(*) FROM enquiry").fetchone(), (1,))
        self.assertEqual(self.db.execute("SELECT count(*) FROM delivery").fetchone(), (1,))
        self.assertEqual(self.db.execute("SELECT draft_text FROM delivery").fetchone(), (self.draft,))
        self.assertEqual(self.state(), ("draft", None))

    def test_edited_text_needs_a_new_reference(self):
        with self.assertRaisesRegex(ValueError, "different enquiry"):
            capture(self.db, self.reference, "Quote a different job", self.draft)
        saved = self.db.execute("SELECT text FROM enquiry").fetchone()
        self.assertEqual(saved, ("Quote a website fix",))

    def test_unapproved_draft_never_reaches_the_provider(self):
        self.assertFalse(attempt(self.db, self.reference, self.provider))
        self.assertEqual(self.provider.attempts, 0)
        self.assertEqual(self.state(), ("draft", None))

    def test_accepted_but_timed_out_resolves_without_a_second_send(self):
        approve(self.db, self.reference)
        with self.assertRaises(TimeoutError):
            attempt(self.db, self.reference, self.provider)
        self.assertEqual(self.state(), ("unknown", None))
        self.assertFalse(attempt(self.db, self.reference, self.provider))
        reconcile(self.db, self.reference, self.provider)
        self.assertEqual(self.state(), ("accepted", "receipt-1"))
        self.assertEqual(self.provider.attempts, 1)

    def test_absent_receipt_leaves_the_delivery_unknown(self):
        approve(self.db, self.reference)
        with self.assertRaises(TimeoutError):
            attempt(self.db, self.reference, self.provider)
        reconcile(self.db, self.reference, FixtureProvider())
        self.assertEqual(self.state(), ("unknown", None))
        self.assertFalse(attempt(self.db, self.reference, self.provider))


if __name__ == "__main__":
    unittest.main()
