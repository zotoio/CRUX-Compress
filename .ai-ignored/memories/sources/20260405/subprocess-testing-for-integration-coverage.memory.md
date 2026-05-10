---
id: "c784aeb"
title: "Testing Python scripts via subprocess provides strong integration coverage beyond unit tests"
description: "The memory index script (memory-index.py) is tested by invoking it as a subprocess against fixture directories rather than importing and testing functions directly. This validates CLI argument parsing, file I/O, and output formatting as an integrated whole."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [testing, subprocess, integration, python]
---

For Python CLI scripts, unit tests that import and call functions directly miss important integration concerns:

- CLI argument parsing (`argparse`, etc.)
- Working directory assumptions
- File I/O error handling
- Exit codes
- stdout/stderr formatting

Testing via `subprocess.run()` validates all of these as an integrated whole. Example pattern:

```python
result = subprocess.run(
    ["python", "scripts/memory-index.py", "--config", str(config_path)],
    cwd=tmp_path,
    capture_output=True,
    text=True
)
assert result.returncode == 0
# Assert on result.stdout or output files
```

This technique is used in `evals/test_e_memory_index.py` and should be applied to any script that will be invoked from the command line.
