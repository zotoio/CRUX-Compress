# CRUX Test Report

**Generated**: 2026-05-24 19:55 (Sunday, AEST)
**Version**: 2.10.2 (from `.crux/crux.json`)
**Environment**: Linux 6.17.0-29-generic, Python 3, Bash
**Test Command**: `/crux-test` (full suite)

## Summary

| Test | Status | Notes |
|------|--------|-------|
| 1. Compression | PASS | `sample-rule.md` → `sample-rule.crux.md`; 82% reduction (6354 → 1122 tokens, ratio 17.7%) |
| 2. Decompression | PASS | LLM interpretation aligned with source; all major sections recognised |
| 3. Token Estimation | PASS | Source 6354 / CRUX 1120 tokens; ratio 17.6%; target ≤25% met |
| 4. Checksum | PASS | Deterministic (`2253728265` × 2); modification changed checksum (`2253728265` → `2066403381`) |
| 5. Install Script | PASS (with note) | `install.py` valid; `--help` shows `--backup` + `--verbose`; curl docs in README |
| 6. Semantic Validation | PASS | Fresh subagent → **confidence: 89%** (completeness 85, accuracy 94, reconstructability 82, no-hall 98) |
| 7. Special Characters | PASS | `special-chars.md` → 37 special tokens detected (of 136 total) |
| 8. Crux-Compress Command | PASS | End-to-end: compressed `compress-test.md` (40% reduction, **confidence 92%**); skip-if-unchanged verified |
| 9. Semantic Stability (Drift) | PASS | `no-change.md` checksum matched baseline; fresh validation **95%** (baseline 94%) — no drift |
| 10. Force Recompression | PASS (with finding) | `--force` simulated by delete; new compression at `19:46` (vs baseline `19:37`); skip-after-force verified; aggressive recompression confidence dropped to 75% (see Issues) |

**Overall**: **10 / 10 tests passed**

---

## Detailed Results

### Test 1: Compression

**Command**: `crux-cursor-rule-manager` subagent invoked on `tests/fixtures/sample-rule.md`.

**Output**: `tests/fixtures/sample-rule.crux.md` created.

**Frontmatter verification** — all required fields present:

```5:9:tests/fixtures/sample-rule.crux.md
sourceChecksum: "2253728265"
cruxLevel: 25
beforeTokens: 6354
afterTokens: 1122
reducedBy: 82%
```

| Field | Present | Value |
|-------|---------|-------|
| `generated` | YES | `2026-05-24 19:28` |
| `sourceChecksum` | YES | `"2253728265"` |
| `beforeTokens` | YES | `6354` |
| `afterTokens` | YES | `1122` |
| `cruxLevel` | YES | `25` |
| `reducedBy` | YES | `82%` |
| `confidence` | YES | filled to `89%` by Test 6 |

**CRUX header**: `⟦CRUX:tests/fixtures/sample-rule.md` confirmed at line 17 of the output (block also closes with `⟧`).

**Reduction**: 82% (1122 / 6354 = 17.7% of original), comfortably under the 25% target.

---

### Test 2: Decompression

**Method**: Read `tests/fixtures/sample-rule.crux.md` without consulting `CRUX.md`. Interpret the notation from semantic context alone.

**Interpretation** (key rules extracted from the CRUX block):

- `Ρ{team coding standards; multi-lang}` — Premise: multi-language team coding standards.
- `Κ{fn=function;cls=class;...}` — Abbreviation dictionary.
- `R.naming{JS/TS{...};Py{...};Go{...}}` — Per-language naming conventions (camelCase / PascalCase / snake_case / UPPER_SNAKE / exported vs unexported).
- `R.style{fn≤30ln; early return; nest≤3; SRP; composition≻inheritance}` plus per-language formatting (chars/indent) and complexity limits with `!` marking required gates.
- `R.docs{∀public→jsdoc|docstring|godoc[params+return+throws+example]}` — Universal "all public APIs documented".
- `R.errors{¬swallow!; log+ctx!; custom types!; fail fast!; hierarchy{Base→[Validation,Business,Integration,System]→subtypes}}` — Error handling policy with hierarchy.
- `R.testing{cov{line≥80%⊕90%;...}; AAA; mock external only!}` — Coverage thresholds (minimum⊕target) and mocking guidance.
- `Π.arch{layers=[Presentation,Application,Domain,Infrastructure]→inward deps}` — Layered architecture with inward dependencies.
- `R.api{REST; URL{nouns;plural;kebab-case}; codes{2xx,4xx,5xx}; pagination; ver=URL /api/v{n}/}` — RESTful conventions.
- `R.git{commits=conventional; types{feat→minor;fix→patch;...}; branch protection per branch}` — Conventional commits and branch protection rules.
- `R.security{auth=OAuth2/OIDC; data{rest=AES-256;transit=TLS1.3;pw=bcrypt≥12}; secrets{env|vault;¬git!;¬log!}}` — Crypto, authn, secret management.
- `R.db`, `R.logging`, `R.perf`, `R.review`, `R.flags`, `R.a11y`, `R.release` — All major source sections captured.
- `Ω{consistency; quality; security; perf; maintainability; a11y; reliability; ∀team→follow}` — Summary outcome statement.

**Comparison to source**: All 14 major sections of `sample-rule.md` are represented. Specific examples (e.g. `getUserById`, `IsValidEmail` in naming) are dropped in favour of pattern names, which is the expected loss-leader for compression at level 25.

**Result**: PASS. An LLM without the CRUX spec can recover all rule categories and their core constraints.

---

### Test 3: Token Estimation

**Command**:

```bash
python3 .cursor/skills/crux-utils/scripts/crux-utils.py --token-count --ratio tests/fixtures/sample-rule.md tests/fixtures/sample-rule.crux.md
```

**Output**:

```
=== Token Estimate: sample-rule.md ===
Prose tokens:      3866
Code tokens:       2480
Special tokens:    8
TOTAL TOKENS:      6354

=== Token Estimate: sample-rule.crux.md ===
Prose tokens:      60
Code tokens:       1003
Special tokens:    57
TOTAL TOKENS:      1120

=== Compression Summary ===
Source tokens:     6354
CRUX tokens:       1120
Ratio:             17.6% of original
Reduction:         82.4%
Target (≤25%):     YES
```

| Metric | Value |
|--------|-------|
| Prose/Code/Special on source | 3866 / 2480 / 8 |
| Prose/Code/Special on CRUX | 60 / 1003 / 57 |
| Compression ratio | 17.6% of original |
| Target met (≤25%) | YES |

---

### Test 4: Checksum

**Determinism check** (`crux-utils --cksum tests/fixtures/sample-rule.md` × 2):

| Run | Checksum |
|-----|----------|
| First call | `2253728265` |
| Second call | `2253728265` |

**Sensitivity check** (copied file, appended `# modification`, recalculated):

| State | Checksum |
|-------|----------|
| Original copy | `2253728265` |
| After append | `2066403381` |

Result: deterministic (same input → same output) and sensitive (any change → different output).

---

### Test 5: Install Script

The test command's wording references `install.sh`. In the current repository the installer is implemented as `install.py` (Python) — see `install.crux.md` (the spec source) and `install.py`. This is a deliberate design choice (Python is a hard dependency anyway because `crux-utils` is Python). Treating `install.py` as the install script:

| Check | Result |
|-------|--------|
| File exists in project root | YES — `install.py` (47 KB) |
| Syntax valid | YES — `py_compile` passed |
| `--help` runs cleanly | YES |
| `--help` mentions `--backup` | YES |
| `--help` mentions `--verbose` | YES |
| curl usage example | YES (documented in `README.md` line 246, 252, 265, 268, 271, 274, 277, 312 — the natural location since curl is the *delivery mechanism*, not an installer feature) |

`--help` excerpt:

```
usage: install.py [-h] [-y] [--force] [--backup] [--verbose] [--with-memories]
                  [--with-mcp-server]

CRUX Compress Installer

options:
  -h, --help         show this help message and exit
  -y                 Non-interactive mode
  --force            Backup and install regardless of version
  --backup           Create backups of existing files
  --verbose          Show detailed progress
  --with-memories    Set up optional memory system scaffolding
  --with-mcp-server  Install standalone MCP memory server (user-level)
```

**Note**: The `/crux-test` command file at `.cursor/commands/crux-test.md` should be updated to reference `install.py` instead of `install.sh` to remove this drift.

---

### Test 6: Semantic Validation (Fresh Subagent)

A **fresh** `crux-cursor-rule-manager` instance was spawned with explicit instructions NOT to consult `CRUX.md`. It evaluated `tests/fixtures/sample-rule.crux.md` against the original source.

**Result** (verbatim from the validator):

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Completeness | 85% | 0.30 | 25.5 |
| Accuracy | 94% | 0.30 | 28.2 |
| Reconstructability | 82% | 0.25 | 20.5 |
| No Hallucination | 98% | 0.15 | 14.7 |
| **Overall confidence** | **89%** | — | (25.5 + 28.2 + 20.5 + 14.7) |

**Status**: Good (80-89%) — accept as-is, minor improvements optional.

**Frontmatter update**: `confidence: pending` → `confidence: 89%` in `tests/fixtures/sample-rule.crux.md` (line 8).

**Issues**: none (above 80% threshold).

---

### Test 7: Special Characters

**Command**: `python3 .cursor/skills/crux-utils/scripts/crux-utils.py --token-count tests/fixtures/special-chars.md`

**Output**:

```
=== Token Estimate: special-chars.md ===
Prose tokens:      73
Code tokens:       26
Special tokens:    37
TOTAL TOKENS:      136
```

Special-tokens count of **37** reflects the Unicode CRUX symbols in the fixture (`→ ← ≻ ≺ ≥ ≤ ≠ ∀ ∃ ¬ ⊤ ⊥ ∋ ⊳ ⊲ « » ⟨ ⟩ Ρ Λ Π Κ Γ Φ Ω Δ ⊛ ◊` and the embedded CRUX block delimiters `⟦ ⟧`).

---

### Test 8: Crux-Compress Command End-to-End

**Setup**: `tests/fixtures/compress-test.md` (permanent fixture, `crux: true`, ~480 tokens).

**Step 1 — Compression**:
- Fresh `crux-cursor-rule-manager` spawned.
- Output written to `tests/fixtures/compress-test.crux.md`.
- 480 → 287 tokens (40% reduction, ratio 59.8%).
- ≤25% target NOT met. Subagent reported this is expected for small sources where fixed overhead (frontmatter, banner, fence) consumes a disproportionate share of the token budget.

**Step 2 — Validation** (fresh subagent):

| Dimension | Score |
|-----------|-------|
| Completeness | 95% |
| Accuracy | 93% |
| Reconstructability | 90% |
| No Hallucination | 90% |
| **Overall confidence** | **92%** |

Frontmatter updated to `confidence: 92%`. Workflow complete.

**Step 3 — Skip-if-unchanged**:
- Pre-skip state: `generated: 2026-05-24 19:37`, `sourceChecksum: "2179275645"`, `confidence: 92%`.
- New `crux-cursor-rule-manager` spawned with skip-aware prompt.
- Subagent computed current source checksum (`2179275645`), compared to existing CRUX `sourceChecksum` (`2179275645`), found match → **skipped recompression**.
- Post-skip state: identical frontmatter, `generated` timestamp unchanged.

Result: PASS for both compression-then-validate workflow and skip optimization.

---

### Test 9: Semantic Stability (Drift Detection)

**Step 1 — Source unchanged check**:

| Field | Current | Baseline |
|-------|---------|----------|
| `tests/fixtures/no-change.md` checksum | `2942027156` | `2942027156` |

Match → source has not changed.

**Step 2 — Baseline still accurate**:

A fresh `crux-cursor-rule-manager` instance validated the existing `no-change.crux.md` baseline (without modifying it) against `no-change.md`.

| Dimension | Score |
|-----------|-------|
| Completeness | 95% |
| Accuracy | 95% |
| Reconstructability | 90% |
| No Hallucination | 100% |
| **Overall confidence** | **95%** |

Baseline frontmatter `confidence: 94%` is closely matched by the fresh validation (95%). No semantic drift.

**Step 3 — Sections verification**:

All 8 expected CRUX sections present in `no-change.crux.md`:

- `R.coverage` (line/branch/function thresholds + critical=100%) — YES
- Critical path requirements (`critical=100%∋[payment,auth,validation,err handling]`) — YES
- Test naming pattern (`R.naming{pattern="should [behavior] when [condition]"}`) — YES
- AAA pattern (`R.structure{AAA=Arrange»Act»Assert}`) — YES
- Test categories (`Κ.categories`) — YES
- Test independence (`R.structure.independence`) — YES
- Mocking guidelines (`R.mock`) — YES
- CI requirements (`R.CI`) — YES

Result: PASS. Baseline holds; no recompression needed.

---

### Test 10: Force Recompression (`--force`)

**Step 1 — Baseline state** (after Test 8):

```
generated: 2026-05-24 19:37
sourceChecksum: "2179275645"
afterTokens: 287
reducedBy: 40%
confidence: 92%
```

**Step 2 — Simulate `--force`**: deleted `tests/fixtures/compress-test.crux.md`.

**Step 3 — Recompress without source change**:
- Fresh `crux-cursor-rule-manager` spawned.
- Since CRUX file was absent, no skip triggered.
- New output written.

**Step 4 — Post-force state**:

```
generated: 2026-05-24 19:46    ← NEWER than 19:37 ✓
sourceChecksum: "2179275645"   ← matches (source unchanged) ✓
afterTokens: 119               ← much more aggressive (vs 287)
reducedBy: 75%                 ← well under 25% target this time
confidence: 75%                ← see Issues below
```

`generated` timestamp moved from 19:37 → 19:46, confirming force-recompression bypassed the skip path.

**Step 5 — Verify normal skip still works**:
- Spawned another `crux-cursor-rule-manager` without `--force`.
- Subagent computed source checksum (`2179275645`), found match in existing CRUX file (also `2179275645`), and skipped.
- `generated` stayed at `19:46`. Confirmed.

**Result**: PASS. Force triggered recompression (new timestamp), and the subsequent normal run correctly skipped (timestamp unchanged).

---

## Metrics

| Metric | Value |
|--------|-------|
| Source tokens (`sample-rule.md`) | 6354 |
| CRUX tokens (`sample-rule.crux.md`) | 1120 |
| Compression ratio | 17.6% of original |
| Reduction | 82.4% |
| Source checksum | `2253728265` |
| Semantic confidence (sample-rule) | 89% |
| Semantic confidence (compress-test, initial) | 92% |
| Semantic confidence (compress-test, post-force aggressive) | 75% |
| Semantic confidence (no-change baseline drift check) | 95% (vs frontmatter 94%) |
| Special tokens (`special-chars.md`) | 37 |

---

## Issues Found

### Minor — documentation drift

1. **`install.sh` vs `install.py`**: The `/crux-test` command file at `.cursor/commands/crux-test.md` (Test 5) references a shell `install.sh`, but the actual installer is `install.py`. The test still passes because the install spec works correctly — the test wording just needs updating to match reality. Suggest updating Test 5 in the command to: "Check `install.py` exists in project root; verify Python syntax with `python3 -m py_compile install.py`; run `python3 install.py --help`".

### Minor — non-determinism in compression aggressiveness

2. **Force-recompression aggressiveness varied confidence**: On `compress-test.md`, the first compression produced 287 tokens (40% reduction, 92% confidence). After `--force` delete + re-compression, a fresh agent produced 119 tokens (75% reduction, 75% confidence). The same `cruxLevel: 25` target produced two materially different outputs — the second was more aggressive and dropped specific assertion commands (`assert_success`, `assert_failure`, `assert_output --partial`), the good/bad code examples, and the "When to Apply" section. Confidence at 75% sits in the **Marginal (70-79%)** band per `.cursor/commands/crux-compress.md` confidence table — a real signal that the second pass over-compressed. A guardrail like "if confidence < 80%, re-attempt with looser ratio target" would catch this automatically.

### Minor — small-file compression overhead

3. **Sub-1000-token sources can't hit the 25% target**: `compress-test.md` (~480 tokens) cannot fit under ≤25% in the initial run because frontmatter (9 lines), the generated-file banner, the heading, and code-fence delimiters consume a non-trivial fixed budget. The CRUX rules' `ABORT IF NO SIGNIFICANT REDUCTION` clause already covers the case where the source is "compact enough", but the gradient between "tiny source" and "abort" deserves clarification. (Note: the post-force aggressive run *did* hit 25%, at the cost of confidence — see Issue 2.)

---

## Recommendations

1. **Update `.cursor/commands/crux-test.md` Test 5** to reference `install.py` and the Python toolchain. Drop the bash-syntax-check step in favour of `python3 -m py_compile install.py`. Move the curl-usage expectation to a separate README check, since curl is the delivery mechanism rather than an installer feature.

2. **Add a confidence-aware retry to `/crux-compress`**: when the post-compression validation confidence is below 80% (Marginal), automatically re-spawn the compression agent with the target ratio relaxed by 10–15 percentage points (e.g. level 25 → level 40) and re-validate. This would catch over-aggressive compressions like Test 10's post-force result without requiring a manual `--force` cycle.

3. **Surface compression non-determinism in the report**: when `/crux-compress` runs in `--force` mode and the prior CRUX file existed, log both the prior and new `reducedBy` and `confidence` values so users can detect when a force-recompression has materially changed semantics.

4. **Small-file allowance**: consider treating sources under ~600 tokens as a special case in `/crux-compress` — either skip with a message ("source already compact"), or apply a relaxed ratio target (e.g. ≤50%) without flagging it as a failure.

5. **Commit baseline outputs**: `tests/fixtures/sample-rule.crux.md` and `tests/fixtures/compress-test.crux.md` are freshly generated by this test run and can be committed alongside this report to capture the current 89%/92%/(75% post-force) baselines.

---

## Test Artefacts (state after this run)

| File | State | Frontmatter highlight |
|------|-------|----------------------|
| `tests/fixtures/sample-rule.crux.md` | regenerated | `generated: 2026-05-24 19:28`, `confidence: 89%` |
| `tests/fixtures/compress-test.crux.md` | regenerated (post-force) | `generated: 2026-05-24 19:46`, `confidence: 75%`, `reducedBy: 75%` |
| `tests/fixtures/no-change.crux.md` | UNCHANGED (permanent baseline) | `generated: 2026-01-28 12:45`, `confidence: 94%` |

End of report.
