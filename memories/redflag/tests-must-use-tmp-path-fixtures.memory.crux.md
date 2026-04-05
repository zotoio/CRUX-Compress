---
id: "9b9a4ac"
title: "Tests must use tmp_path fixtures — never modify the actual repository"
description: "Eval tests that write to repo directories risk polluting the working tree with fixture artifacts that persist after test runs. All file-writing tests must use pytest's tmp_path fixture or equivalent isolated temporary directories."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [testing, isolation, fixtures, pytest]
compressed: true
compressionTarget: 33
beforeTokens: 140
afterTokens: 45
reducedBy: 68%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/tests-must-use-tmp-path-fixtures.memory.md
---

⟦CRUX:memory
P.⊛{¬write→repo dirs(memories/,.crux/)}
R.problem{artifacts persist; pollute git status; accidental commit; break subsequent runs}
R.solution{tmp_path(pytest)|tempfile.TemporaryDirectory; create fixture@temp; assert@temp; auto cleanup}
Ω{enforced in evals/; standard ∀Python tests}
⟧
