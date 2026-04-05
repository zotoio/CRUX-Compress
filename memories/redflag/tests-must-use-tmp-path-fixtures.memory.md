---
title: "Tests must use tmp_path fixtures — never modify the actual repository"
description: "Eval tests that write to repo directories risk polluting the working tree with fixture artifacts that persist after test runs. All file-writing tests must use pytest's tmp_path fixture or equivalent isolated temporary directories."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [testing, isolation, fixtures, pytest]
---

**Anti-pattern**: Tests that write files directly to repository directories (e.g., `memories/`, `.crux/`).

**Problem**: Test artifacts persist after test runs, polluting the working tree. These show up in `git status`, can accidentally be committed, and may break subsequent test runs.

**Solution**: Always use `tmp_path` (pytest built-in fixture) or `tempfile.TemporaryDirectory` for any test that creates files. Structure tests to:

1. Create fixture data in the temp directory
2. Run the operation under test
3. Assert on files in the temp directory
4. Let pytest clean up automatically

This is enforced in the CRUX Memories eval suite (`evals/`) and should be standard for all Python tests.
