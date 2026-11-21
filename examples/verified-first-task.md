# Try one task with a check

Use a fresh folder and synthetic data for your first task with the [agent system prompt](../README.md#quick-start). A small CSV cleanup gives you a result you can verify before asking the agent to work in a real project.

Save this as `incoming.csv`:

```csv
task,status
send test report,done
check sample,open
draft reply,done
send test report,done
archive example,done
draft reply,open
```

Paste the system prompt into your coding agent. Give it this first task:

> Use only incoming.csv in this folder. Create done.csv with the header and each unique row whose status is exactly done, in its original order. Keep incoming.csv intact. Run a check that compares the actual output with the three expected rows. Show me the result and the command you ran.

The expected file is:

```csv
task,status
send test report,done
draft reply,done
archive example,done
```

If you have Python 3, run this from the same folder to check the result independently:

```sh
python3 - <<'PY'
import csv

with open("done.csv", newline="", encoding="utf-8") as file:
    actual = list(csv.reader(file))

expected = [
    ["task", "status"],
    ["send test report", "done"],
    ["draft reply", "done"],
    ["archive example", "done"],
]
if actual != expected:
    raise SystemExit("FAIL: done.csv does not contain the expected rows in order.")
print("PASS: done.csv contains the three expected rows in order.")
PY
```

An open task, duplicate row or reordered result fails the check. Ask the agent to fix the output and run the same check again.

If you try it, [report the result in an issue](https://github.com/fainir/most-capable-agent-system-prompt/issues/new). Include the agent you used, whether it ran the check before calling the task done, and the PASS or FAIL line. Keep your real project data private.

## Review a recurring CSV workflow

If you prepare the same file each week, you can adapt this brief for a [free workflow review through AI Your Work](https://aiyourwork.chat/services?utm_source=github&utm_medium=example&utm_campaign=csv-workflow-review#implementation-request).

> Every Friday I get a task export. Create one file with the first occurrence of each completed row, in its original order, and keep the input intact. Show the counts of rows read, kept and removed. Ask for approval before writing the result to our shared folder.

Describe the column names or use fictional data. If the review leads to paid implementation, you agree on scope and price before work starts.
