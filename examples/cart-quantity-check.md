# Check a cart quantity change with a coding agent

Give Claude Code, Codex or Cursor the same acceptance checks for a fictional cart. The cart accepts whole numbers from 1 through 9. Values such as `2.5`, `True` and `"3"` should be rejected.

## Reproduce the failing checks

In a new folder, save the following as `cart_test.py`. Run `python3 -m unittest cart_test` with Python 3.

```python
import unittest


def accepts_quantity(value):
    return isinstance(value, (int, float)) and 1 <= value <= 9


class CartQuantityTests(unittest.TestCase):
    def test_accepts_whole_quantities_in_range(self):
        for value in (1, 3, 9):
            with self.subTest(value=value):
                self.assertTrue(accepts_quantity(value))

    def test_rejects_other_values(self):
        for value in (0, 10, 2.5, True, "3"):
            with self.subTest(value=value):
                self.assertFalse(accepts_quantity(value))
```

The starting code fails two of the eight checks. It accepts `2.5` within the range and treats `True` as the integer `1`.

## Review the change

Ask your agent to update only `accepts_quantity` so that all eight checks pass. Ask it to show the diff and the actual test output. Rerun the same command yourself and confirm the test cases are intact. If you compare tools, start each with the original file and compare the evidence each one shows.

[Watch the worked Python example](https://www.youtube.com/watch?v=9LGFSPoYGZs).

For feedback on one of your own workflows, [request an implementation review from AI Your Work](https://aiyourwork.chat/services?utm_source=github&utm_medium=readme&utm_campaign=cart-workflow-review#implementation-request). Describe one change your agent handles, the check it should pass and the decision you want a person to approve. The assessment offers free advice. Any paid implementation starts with an agreed scope and price.
