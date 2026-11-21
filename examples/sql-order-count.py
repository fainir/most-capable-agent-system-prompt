"""A report exercise. Run with python3 sql-order-count.py."""
import sqlite3
import unittest


REPORT = """
SELECT customers.name, COUNT(orders.id) AS order_count
FROM customers
LEFT JOIN orders ON orders.customer_id = customers.id
LEFT JOIN line_items ON line_items.order_id = orders.id
GROUP BY customers.id, customers.name
ORDER BY customers.id
"""


class OrderCountTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript("""
            CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL REFERENCES customers(id)
            );
            CREATE TABLE line_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id)
            );
            INSERT INTO customers VALUES (1, 'Ada'), (2, 'Bo'), (3, 'Cy');
            INSERT INTO orders VALUES (42, 1), (43, 1), (44, 2);
            INSERT INTO line_items VALUES (101, 42), (102, 42), (103, 44);
        """)

    def report(self):
        return self.db.execute(REPORT).fetchall()

    def test_includes_each_customer_once(self):
        self.assertEqual([name for name, _ in self.report()], ["Ada", "Bo", "Cy"])

    def test_counts_orders_once_even_with_multiple_lines(self):
        self.assertEqual(dict(self.report())["Ada"], 2)

    def test_counts_an_order_without_lines(self):
        self.db.execute("DELETE FROM line_items WHERE order_id = 44")
        self.assertEqual(dict(self.report())["Bo"], 1)

    def test_zero_orders_is_zero(self):
        self.assertEqual(dict(self.report())["Cy"], 0)


if __name__ == "__main__":
    unittest.main()
