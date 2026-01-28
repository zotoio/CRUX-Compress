# crux-test

Run comprehensive tests on all CRUX features via LLM interaction and produce a markdown test report.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-test                    - Run all tests
/crux-test compression        - Test compression only
/crux-test decompression      - Test decompression only
/crux-test utilities          - Test CRUX-Utils skill only
/crux-test validation         - Test semantic validation only
```

## Instructions

When this command is invoked, you will exercise each CRUX feature systematically and produce a test report saved as `CRUX-TEST-REPORT.md` in the project root.

### Test Suite

Execute the following tests in order:

---

### Pre-Test Cleanup

**Purpose**: Delete existing `.crux.mdc` files so freshly generated versions can be committed.

Before running any tests, delete the following files if they exist:
- `tests/fixtures/sample-rule.crux.mdc`
- `tests/fixtures/compress-test.crux.mdc`

This ensures the compression tests generate fresh output that reflects the current state of the source files and can be included in commits.

**Note**: Do NOT delete `tests/fixtures/no-change.crux.mdc` - it is a permanent baseline for drift detection.

**Alternative**: The `--force` flag in `/crux-compress` can be used to achieve the same effect by deleting CRUX files before recompression. However, for test isolation, we delete files explicitly in this pre-test phase.



---

### Test 1: Compression Test

**Purpose**: Verify CRUX compression works correctly.

1. Read the sample rule file at `tests/fixtures/sample-rule.md`
2. Spawn a `crux-cursor-rule-manager` subagent to compress it
3. Verify the output was created at `tests/fixtures/sample-rule.crux.mdc`
4. Check the output has required frontmatter fields:
   - `generated` (timestamp)
   - `sourceChecksum` (checksum value)
   - `beforeTokens` (number)
   - `afterTokens` (number)
5. Verify the CRUX block contains `⟦CRUX:sample-rule.md` header
6. Record: PASS/FAIL, token reduction percentage

---

### Test 2: Decompression Test

**Purpose**: Verify LLMs can understand CRUX notation without the specification.

1. Read the compressed file `tests/fixtures/sample-rule.crux.mdc`
2. **Without reading CRUX.md**, explain what the compressed notation means
3. List the key rules/guidelines encoded in the CRUX
4. Compare your interpretation to the original source
5. Record: PASS/FAIL, interpretation accuracy notes

---

### Test 3: Token Estimation Test

**Purpose**: Verify the CRUX-Utils skill works correctly.

1. Use the `CRUX-Utils` skill to estimate tokens for `tests/fixtures/sample-rule.md`
2. Verify output contains:
   - Prose tokens count
   - Code tokens count
   - Special tokens count
   - Total tokens count
3. Use `--ratio` mode to compare source vs CRUX file
4. Verify compression ratio is calculated
5. Record: PASS/FAIL, token counts, ratio

---

### Test 4: Checksum Test

**Purpose**: Verify checksum calculation is consistent.

1. Use `CRUX-Utils` skill with `--cksum` mode on `tests/fixtures/sample-rule.md`
2. Record the checksum value
3. Run checksum again on the same file
4. Verify the checksums match (deterministic)
5. Modify the file slightly, recalculate checksum
6. Verify the checksum changed
7. Record: PASS/FAIL, checksum values

---

### Test 5: Install Script Test

**Purpose**: Verify the install script is valid and functional.

1. Check `install.sh` exists in project root
2. Verify bash syntax with `bash -n install.sh`
3. Run `./install.sh --help` and capture output
4. Verify help mentions:
   - `--backup` option
   - `--verbose` option
   - curl usage example
5. Record: PASS/FAIL, help output snippet

---

### Test 6: Semantic Validation Test

**Purpose**: Verify semantic validation scoring works using a fresh subagent instance.

1. Spawn a **fresh `crux-cursor-rule-manager` subagent instance** for validation:
   - Task the validation agent:
     ```
     Perform semantic validation on this CRUX file:
     - Source: tests/fixtures/sample-rule.md
     - CRUX: tests/fixtures/sample-rule.crux.mdc
     - DO NOT use the CRUX specification - evaluate purely on semantic understanding
     - Compare meaning and completeness between source and CRUX
     - Evaluate on these dimensions:
       - Completeness (0-100%): Are all actionable items present?
       - Accuracy (0-100%): Does CRUX correctly represent meaning?
       - Reconstructability (0-100%): Could you reconstruct the original intent?
       - No Hallucination (0-100%): Is everything in CRUX actually in source?
     - Calculate weighted confidence score:
       - Completeness 30%, Accuracy 30%, Reconstructability 25%, No Hallucination 15%
     - Return: individual dimension scores and overall confidence percentage
     - Flag any issues if confidence < 80%
     ```
2. The validation agent returns the confidence score and dimension breakdown
3. Update the `.crux.mdc` frontmatter with `confidence: XX%` (replacing "pending")
4. Record: PASS/FAIL (pass if ≥80%), individual scores, overall confidence

**Why Fresh Agent?** Using a separate agent instance ensures:
- No bias from the compression process or test orchestration
- Independent semantic evaluation
- The validator doesn't rely on CRUX specification knowledge loaded earlier
- True test of whether an LLM can understand the compressed notation

---

### Test 7: Special Characters Test

**Purpose**: Verify CRUX special characters are counted correctly.

1. Use `CRUX-Utils` skill on `tests/fixtures/special-chars.md`
2. Verify "Special tokens" count is > 0
3. Count should reflect the Unicode symbols in the file
4. Record: PASS/FAIL, special token count

---

### Test 8: Crux-Compress Command Test

**Purpose**: Verify the `/crux-compress` command works correctly end-to-end.

1. **Setup**: Verify `tests/fixtures/compress-test.md` exists (permanent test fixture with `crux: true`)
2. **Simulate the command**: Follow the `/crux-compress` workflow:
   - Spawn a `crux-cursor-rule-manager` subagent to compress `tests/fixtures/compress-test.md`
   - Verify output created at `tests/fixtures/compress-test.crux.mdc`
   - Spawn a fresh validation subagent to get confidence score
   - Update the `.crux.mdc` frontmatter with confidence
3. **Verify the complete workflow**:
   - Compression subagent created the CRUX file
   - Validation subagent returned confidence ≥80%
   - Frontmatter has all required fields: `generated`, `sourceChecksum`, `beforeTokens`, `afterTokens`, `confidence`
4. **Verify skip-if-unchanged**: Run compression again on the same file
   - Should report "source unchanged" and skip recompression
   - Verify by checking that `generated` timestamp didn't change
5. Record: PASS/FAIL, workflow completion status, skip-if-unchanged working

**Note**: `compress-test.md` is a permanent source fixture. The `compress-test.crux.mdc` file are regenerated each test run and can be committed.

---

### Test 9: Semantic Stability Test (Drift Detection)

**Purpose**: Verify that the existing CRUX baseline still accurately represents the source, detecting semantic drift over time.

1. **Setup**: Verify both files exist:
   - Source: `tests/fixtures/no-change.md` (testing standards)
   - Baseline: `tests/fixtures/no-change.crux.mdc` (permanent CRUX baseline)
2. **Verify source unchanged**:
   - Calculate checksum of `no-change.md` using CRUX-Utils
   - Compare to `sourceChecksum` in the baseline frontmatter
   - If checksums match, source is unchanged
3. **Validate baseline still accurate**:
   - Spawn a fresh validation subagent to compare source vs baseline CRUX
   - Get confidence score (must be ≥80%)
   - If confidence drops below threshold, flag as drift detected
4. **Verify logical structure intact**:
   - Read the baseline CRUX block
   - Confirm it contains expected sections:
     - Coverage thresholds (COV)
     - Critical path requirements (CRIT)
     - Test naming pattern (NAME)
     - AAA pattern
     - Test categories (CAT)
     - Mocking guidelines (MOCK)
     - Test independence (INDEP)
     - CI requirements
5. Record: PASS/FAIL, checksum match status, confidence score

**Pass Criteria**:
- Checksums match (source unchanged) AND confidence ≥80%
- OR checksums differ (source changed) - flag for baseline regeneration

**Rationale**: This test detects if the CRUX baseline drifts out of sync with the source over time, or if model interpretation changes affect semantic validation scores.

---

### Test 10: Force Recompression Test (`--force`)

**Purpose**: Verify the `--force` flag correctly bypasses checksum-based skip and forces fresh recompression.

1. **Setup**: Ensure `tests/fixtures/compress-test.crux.mdc` exists from Test 8
2. **Record baseline state**:
   - Note the current `generated` timestamp in the CRUX frontmatter
   - Note the current `sourceChecksum` value
3. **Simulate `--force` behavior**:
   - Delete `tests/fixtures/compress-test.crux.mdc` (as `--force` would)
   - Log: "Deleted: tests/fixtures/compress-test.crux.mdc (--force)"
4. **Recompress without source changes**:
   - Spawn a `crux-cursor-rule-manager` subagent to compress `tests/fixtures/compress-test.md`
   - Since the CRUX file was deleted, compression should proceed (not skip)
5. **Verify force behavior worked**:
   - Confirm new `tests/fixtures/compress-test.crux.mdc` was created
   - Verify `generated` timestamp is newer than baseline
   - Verify `sourceChecksum` matches (source unchanged, but compression happened)
6. **Compare to normal skip behavior**:
   - Run compression again WITHOUT deleting the CRUX file
   - Should report "source unchanged" and skip (normal behavior)
   - Verify `generated` timestamp didn't change this time
7. Record: PASS/FAIL, force triggered recompression, normal skip still works

**Pass Criteria**:
- `--force` (delete + recompress) creates new CRUX file with updated timestamp
- Subsequent compression without `--force` correctly skips (unchanged source)

**Rationale**: This test ensures the `--force` flag implementation correctly:
- Bypasses the checksum optimization when needed
- Allows users to force fresh recompression for debugging or validation
- Doesn't break normal skip-if-unchanged behavior

---

## Output Format

After running all tests, create `CRUX-TEST-REPORT.md` with this structure:

```markdown
# CRUX Test Report

**Generated**: [timestamp]
**Version**: [from VERSION]
**Environment**: [OS, bash version if relevant]

## Summary

| Test | Status | Notes |
|------|--------|-------|
| Compression | PASS/FAIL | Token reduction: X% |
| Decompression | PASS/FAIL | Interpretation accuracy notes |
| Token Estimation | PASS/FAIL | Tokens: X, Ratio: Y% |
| Checksum | PASS/FAIL | Deterministic: Yes/No |
| Install Script | PASS/FAIL | Syntax OK, help available |
| Semantic Validation | PASS/FAIL | Confidence: X% (fresh subagent) |
| Special Characters | PASS/FAIL | Special tokens: X |
| Crux-Compress Command | PASS/FAIL | Full workflow, skip-if-unchanged |
| Semantic Stability | PASS/FAIL | Drift detection, baseline confidence |
| Force Recompression | PASS/FAIL | --force bypasses skip, normal skip works |

**Overall**: X/10 tests passed

## Detailed Results

### Test 1: Compression
[Detailed output]

### Test 2: Decompression
[Detailed output]

... [continue for all tests]

## Metrics

- **Source tokens** (sample-rule.md): X
- **CRUX tokens** (sample-rule.crux.mdc): X
- **Compression ratio**: X% of original
- **Semantic confidence**: X%

## Issues Found

[List any issues discovered during testing]

## Recommendations

[Any suggested improvements]
```

## Important Notes

- Run tests in the order specified
- Do not skip tests unless specifically requested
- If a test fails, continue with remaining tests
- Always produce the test report, even if some tests fail
- The report should be actionable and include specific metrics
