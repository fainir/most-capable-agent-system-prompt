import unittest
from html.parser import HTMLParser


ORIGIN = "https://staged.example.test"
EN = "/blog/api-document"
KO = "/blog/api-document-ko"


class Metadata(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.lang = None
        self.canonicals = []
        self.alternates = []
        self.feed(document)

    def handle_starttag(self, tag, fields):
        attrs = dict(fields)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "link":
            rel = attrs.get("rel", "").split()
            if "canonical" in rel:
                self.canonicals.append(attrs.get("href"))
            if "alternate" in rel and "hreflang" in attrs:
                self.alternates.append((attrs["hreflang"], attrs.get("href")))


def document(lang, path, alternates):
    links = "".join(
        f'<link rel="alternate" hreflang="{locale}" href="{ORIGIN + route}">'
        for locale, route in alternates.items()
    )
    return (
        f'<html lang="{lang}"><head><link rel="canonical" href="{ORIGIN + path}">'
        f"{links}</head><body></body></html>"
    )


def validate(document_html, lang, path, published_group):
    metadata = Metadata(document_html)
    expected = (
        [(locale, ORIGIN + route) for locale, route in published_group.items()]
        if len(published_group) > 1 else []
    )
    if metadata.lang != lang:
        raise ValueError("Document language")
    if metadata.canonicals != [ORIGIN + path]:
        raise ValueError("Final self-canonical")
    if sorted(metadata.alternates) != sorted(expected):
        raise ValueError("Full published alternate group")


def validate_cutover(path, hops, final):
    destination = ORIGIN + path
    if hops != [(301, destination)] or final != (200, destination):
        raise ValueError("Legacy host redirect")


class CutoverTests(unittest.TestCase):
    def test_both_pages_link_to_the_full_published_group(self):
        group = {"en": EN, "ko": KO}
        for lang, path in group.items():
            with self.subTest(lang=lang):
                validate(document(lang, path, group), lang, path, group)

    def test_missing_self_alternate_fails(self):
        with self.assertRaisesRegex(ValueError, "alternate group"):
            validate(document("ko", KO, {"en": EN}), "ko", KO, {"en": EN, "ko": KO})

    def test_korean_post_canonical_cannot_point_at_english(self):
        group = {"en": EN, "ko": KO}
        with self.assertRaisesRegex(ValueError, "self-canonical"):
            validate(document("ko", EN, group), "ko", KO, group)

    def test_single_published_locale_has_no_translation_alternate(self):
        validate(document("ko", KO, {}), "ko", KO, {"ko": KO})
        with self.assertRaisesRegex(ValueError, "alternate group"):
            validate(document("ko", KO, {"en": EN}), "ko", KO, {"ko": KO})

    def test_legacy_redirect_preserves_the_existing_korean_slug(self):
        target = ORIGIN + KO
        validate_cutover(KO, [(301, target)], (200, target))
        for destination in (ORIGIN + EN, target + "-ko"):
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(ValueError, "Legacy host redirect"):
                    validate_cutover(KO, [(301, destination)], (200, destination))

    def test_redirect_chain_fails_even_if_the_final_page_is_correct(self):
        target = ORIGIN + KO
        with self.assertRaisesRegex(ValueError, "Legacy host redirect"):
            validate_cutover(KO, [(301, ORIGIN + EN), (301, target)], (200, target))


if __name__ == "__main__":
    unittest.main()
