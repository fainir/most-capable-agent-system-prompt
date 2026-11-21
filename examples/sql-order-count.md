# Catch inflated order counts in a SQL report

A shop needs one row per customer, with the number of orders each person placed. Count orders even when they have no line items. Keep customers who have never ordered in the report.

## Run the checks

The exercise uses Python 3 with its built-in SQLite module and runs entirely in memory. Download [sql-order-count.py](sql-order-count.py) from GitHub’s Raw view and run this command in the folder where you saved it.

```sh
python3 sql-order-count.py
```

From a repository checkout, run `python3 examples/sql-order-count.py` from the root.

Ada has two orders. Order 42 has two line items and order 43 has none. Bo has one order. Cy has no orders. The starting query reports Ada’s count as three, so one of the four tests fails.

## Fix the report and check it again

Ask your coding agent to change only the SQL in `REPORT` and show you the diff and test output. Rerun the four tests yourself. The result should be Ada 2, Bo 1 and Cy 0. Ask the agent to explain why a plain count of order IDs reports three for Ada and what would happen if either join became an inner join.

[SQLite’s aggregate functions](https://www.sqlite.org/lang_aggfunc.html#count) explain when a count skips NULL values. [SQLite’s join rules](https://www.sqlite.org/lang_select.html#fromclause) explain how rows with no match survive a left join.

## Keep practicing

The author’s [free Hired in 60 SQL exercise](https://hiredin60.com/lessons/165/?utm_source=github&utm_medium=example&utm_campaign=sql-order-count#sql-left-join-practice) lets you predict the output before revealing the answer. The [optional $12 interview review pack](https://hiredin60.com/shop) has a free sample on the Shop page.
