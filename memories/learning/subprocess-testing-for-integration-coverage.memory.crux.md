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
compressed: true
compressionTarget: 33
beforeTokens: 170
afterTokens: 55
reducedBy: 68%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/subprocess-testing-for-integration-coverage.memory.md
---

⟦CRUX:memory
R{unit test import→miss CLI parsing,cwd,file IO,exit codes,stdout/stderr}
Λ.pattern{subprocess.run([python,script,--args],cwd=tmp_path,capture_output=⊤,text=⊤)}
R.assert{returncode==0; stdout|output files}
E.used{evals/test_e_memory_index.py}
Ω{∀CLI script→subprocess test}
⟧
