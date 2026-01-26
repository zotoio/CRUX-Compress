---
name: token-count-estimator
description: Estimate token counts for markdown and code files using deterministic heuristics. Use when the user needs to estimate tokens, compare file sizes for compression, or analyze token usage.
---

# Token Count Estimator

Estimates token counts for files using deterministic character-based heuristics. Provides consistent results suitable for CRUX compression ratio calculations.

## Quick Start

Run the token estimator script:

```bash
bash .cursor/skills/token-count-estimator/scripts/count-tokens.sh <file_path>
```

## Output Format

```
=== Token Estimate: <filename> ===
Prose tokens:      <count>
Code tokens:       <count>
Special tokens:    <count>
---
TOTAL TOKENS:      <count>
```

## Estimation Method

The script uses these deterministic ratios:

| Content Type | Chars/Token | Notes |
|--------------|-------------|-------|
| Prose (markdown) | 4.0 | English text, headers, lists |
| Code blocks | 3.5 | More symbols, shorter identifiers |
| Special chars | 1.0 | Unicode symbols (→, ⊳, «, etc.) |

### Special Character Detection

These Unicode symbols count as 1 token each:
- CRUX delimiters: `« » ⟨ ⟩`
- Arrows/flow: `→ ← ≻ ≺`
- Logic: `⊤ ⊥ ∀ ∃ ¬ ∋`
- Relations: `⊳ ⊲`
- Comparison: `≥ ≤ ≠`
- Other: `Δ ⊛ ◊ Ρ Λ Π Κ Γ Φ Ω`

## Usage Examples

**Single file:**
```bash
bash .cursor/skills/token-count-estimator/scripts/count-tokens.sh CRUX.md
```

**Compare before/after compression:**
```bash
# Get source token count
bash .cursor/skills/token-count-estimator/scripts/count-tokens.sh rules/my-rule.mdc

# Get CRUX token count
bash .cursor/skills/token-count-estimator/scripts/count-tokens.sh rules/my-rule.crux.mdc

# Calculate ratio manually or use the --ratio flag
bash .cursor/skills/token-count-estimator/scripts/count-tokens.sh --ratio rules/my-rule.mdc rules/my-rule.crux.mdc
```

## Determinism Guarantee

The script produces identical output for identical input:
- No random elements
- No timestamp dependencies
- Pure character/pattern counting
- Consistent across runs
