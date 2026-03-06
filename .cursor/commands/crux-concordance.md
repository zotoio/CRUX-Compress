# crux-concordance

Analyze semantic concordance across CRUX-compressed artifacts to detect drift between code, documentation, and images.

## Usage

```
/crux-concordance @file1.crux.md @file2.crux.md       - Compare two CRUX artifacts
/crux-concordance @docs.crux.md @code.crux.md @img.crux.md - Compare multiple artifacts
/crux-concordance ALL                                   - Compare all .crux.md files in .cursor/rules/
/crux-concordance --threshold 80                        - Set custom concordance threshold
```

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--threshold <N>` | Concordance warning threshold (0-100) | 70 |
| `--json` | Output results as JSON | off |

## Behavior

When this command is invoked:

1. **Collect CRUX files**: Parse the arguments to determine which `.crux.md` files to analyze
   - If specific files are referenced with `@`, use those files
   - If `ALL` is specified, scan `.cursor/rules/` for all `.crux.md` files

2. **Run concordance analysis**: Execute the concordance script
   ```bash
   bash scripts/crux-concordance.sh <file1> <file2> [file3 ...]
   ```

3. **Interpret results**: The script outputs:
   - **Pairwise concordance scores** (Jaccard similarity of entity sets)
   - **Shared entities** between each pair
   - **Drift entities** unique to each file in a pair
   - **Overall summary** with average and minimum concordance

4. **Report to user**: Present the concordance report, highlighting:
   - Pairs with concordance below threshold (drift detected)
   - Specific entities that exist in one artifact but not another
   - Recommendations for resolving drift

## What It Detects

The concordance analyzer extracts semantic entities from CRUX standard blocks:

| Block | What's Extracted | Example Drift |
|-------|-----------------|---------------|
| `Ρ{}` | Project context | README describes "API server" but code CRUX says "web app" |
| `E{}` | Named entities | Architecture diagram has "AuthService" but code has "IdentityProvider" |
| `Λ{}` | Commands/actions | Docs describe `deploy` command but code only has `build` and `test` |
| `Π{}` | Architecture | Image shows `src/services/` but code CRUX has `lib/handlers/` |
| `Κ{}` | Concept definitions | Different key definitions between doc and code |
| `Φ{}` | Configuration | Config values differ between documentation and implementation |

## Cross-Modal Concordance

Because CRUX compresses all modalities into the same symbolic notation, concordance works across:

- **Code ↔ Documentation**: Does the README match the implementation?
- **Architecture Diagrams ↔ Code**: Does the diagram reflect actual structure?
- **API Specs ↔ Implementation**: Do endpoint definitions match handlers?
- **Multiple Code Modules**: Do shared entities stay consistent across services?

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║           CRUX Concordance Analysis Report                  ║
╚══════════════════════════════════════════════════════════════╝

Files Analyzed:
  [1] architecture.crux.md (24 entities)
  [2] api-handlers.crux.md (31 entities)

Pairwise Concordance:
  ────────────────────────────────────────────
  architecture.crux.md ↔ api-handlers.crux.md
    Score: 62%  │  Shared: 18  │  Only-A: 6  │  Only-B: 13

    ⚠ DRIFT DETECTED — below threshold of 70%
    Only in architecture.crux.md:
      - e.authservice
      - π.src/legacy/
    Only in api-handlers.crux.md:
      - e.identityprovider
      - λ.webhook_handler
      - π.lib/handlers/
  ────────────────────────────────────────────

Summary:
  Average Concordance: 62%
  Minimum Concordance: 62%
  Threshold:           70%

✗ Semantic drift detected — concordance below threshold
```

## Integration with CI/CD

Add to your CI pipeline to catch drift automatically:

```yaml
- name: Check CRUX concordance
  run: |
    bash scripts/crux-concordance.sh --dir .cursor/rules/ --threshold 70
```

Exit code 2 indicates drift was detected (concordance below threshold).
