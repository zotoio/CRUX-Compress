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
5. Verify the CRUX block contains `«CRUX⟨sample-rule.md⟩»` header
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

**Purpose**: Verify semantic validation scoring works.

1. Read both `tests/fixtures/sample-rule.md` and `tests/fixtures/sample-rule.crux.mdc`
2. Evaluate semantic equivalence on these dimensions:
   - **Completeness** (0-100%): Are all actionable items present?
   - **Accuracy** (0-100%): Does CRUX correctly represent meaning?
   - **Reconstructability** (0-100%): Could you reconstruct the original intent?
   - **No Hallucination** (0-100%): Is everything in CRUX actually in source?
3. Calculate weighted confidence score:
   - Completeness 30%
   - Accuracy 30%
   - Reconstructability 25%
   - No Hallucination 15%
4. Record: PASS/FAIL (pass if ≥80%), individual scores, overall confidence

---

### Test 7: Special Characters Test

**Purpose**: Verify CRUX special characters are counted correctly.

1. Use `CRUX-Utils` skill on `tests/fixtures/special-chars.md`
2. Verify "Special tokens" count is > 0
3. Count should reflect the Unicode symbols in the file
4. Record: PASS/FAIL, special token count

---

## Output Format

After running all tests, create `CRUX-TEST-REPORT.md` with this structure:

```markdown
# CRUX Test Report

**Generated**: [timestamp]
**Version**: [from version.txt]
**Environment**: [OS, bash version if relevant]

## Summary

| Test | Status | Notes |
|------|--------|-------|
| Compression | PASS/FAIL | Token reduction: X% |
| Decompression | PASS/FAIL | Interpretation accuracy notes |
| Token Estimation | PASS/FAIL | Tokens: X, Ratio: Y% |
| Checksum | PASS/FAIL | Deterministic: Yes/No |
| Install Script | PASS/FAIL | Syntax OK, help available |
| Semantic Validation | PASS/FAIL | Confidence: X% |
| Special Characters | PASS/FAIL | Special tokens: X |

**Overall**: X/7 tests passed

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
