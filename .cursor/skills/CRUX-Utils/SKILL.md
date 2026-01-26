---
name: CRUX-Utils
description: Multi-purpose utility for CRUX compression workflows. Provides token estimation and checksum calculation. Use when estimating tokens for compression, comparing file sizes, or getting checksums for sourceChecksum tracking.
---

# CRUX Utils

Multi-purpose utility for CRUX compression workflows. Provides deterministic tools for token estimation and checksum calculation.

## Quick Start

```bash
# Token count estimation
bash .cursor/skills/CRUX-Utils/scripts/crux-utils.sh --token-count <file>

# Compare source vs CRUX (ratio mode)
bash .cursor/skills/CRUX-Utils/scripts/crux-utils.sh --token-count --ratio <source> <crux>

# Get checksum for sourceChecksum frontmatter
bash .cursor/skills/CRUX-Utils/scripts/crux-utils.sh --cksum <file>
```

## Modes

### `--token-count <file>`

Estimate token count for a single file.

**Output:**
```
=== Token Estimate: example.md ===
Prose tokens:      397
Code tokens:       0
Special tokens:    0
---
TOTAL TOKENS:      397
```

### `--token-count --ratio <source> <crux>`

Compare source file vs CRUX file and calculate compression ratio.

**Output:**
```
=== Compression Ratio Analysis ===

=== Token Estimate: source.md ===
...
=== Token Estimate: source.crux.mdc ===
...

=== Compression Summary ===
Source tokens:     397
CRUX tokens:       140
Ratio:             35.2% of original
Reduction:         64.8%
Target (≤20%):     NO
```

### `--cksum <file>`

Get checksum of a file, formatted for CRUX frontmatter `sourceChecksum` field.

**Output:**
```
=== Checksum: example.md ===
Checksum:          1234567890
---
FRONTMATTER:       "1234567890"
```

## Token Estimation Method

| Content Type | Chars/Token | Notes |
|--------------|-------------|-------|
| Prose (markdown) | 4.0 | English text, headers, lists |
| Code blocks | 3.5 | More symbols, shorter identifiers |
| Special chars | 1.0 | CRUX Unicode symbols |

### Special Characters (1 token each)

CRUX delimiters and symbols that count as 1 token each:
- Delimiters: `« » ⟨ ⟩`
- Arrows/flow: `→ ← ≻ ≺`
- Logic: `⊤ ⊥ ∀ ∃ ¬ ∋`
- Relations: `⊳ ⊲`
- Comparison: `≥ ≤ ≠`
- Blocks: `Δ Ρ Λ Π Κ Γ Φ Ω`
- Other: `⊛ ◊ θ`

## Determinism Guarantee

Both modes produce identical output for identical input:
- No random elements
- No timestamp dependencies
- Pure character/pattern counting
- Consistent across runs

## Usage in CRUX Workflow

**For compression tasks:**
1. Get source checksum: `--cksum <source>` → use FRONTMATTER value for `sourceChecksum`
2. Estimate source tokens: `--token-count <source>` → use for `beforeTokens`
3. After compression: `--token-count <crux>` → use for `afterTokens`
4. Verify ratio: `--token-count --ratio <source> <crux>` → check Target (≤20%)
