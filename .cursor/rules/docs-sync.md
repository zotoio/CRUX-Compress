---
alwaysApply: true
crux: true
---

# Documentation Synchronization Rule

When you modify files that affect project functionality or workflows, update the corresponding documentation to keep it in sync.

## Documentation Files

| Doc File | Update When... |
|----------|----------------|
| `README.md` | Installation, usage, or feature changes |
| `CONTRIBUTORS.md` | CI/CD workflow, testing, or contribution process changes |
| `web/compress.md/` | Landing page content, examples, or feature highlights |

## Trigger Files → Documentation Updates.

### README.md Updates
- `install.sh` - Update installation instructions
- `CRUX.md` - Update specification references or examples
- `.cursor/commands/*` - Update command usage examples
- `.cursor/skills/*/SKILL.md` - Update skill descriptions

### CONTRIBUTORS.md Updates
- `.github/workflows/*.yml` - Update CI/CD flow diagram and descriptions
- `tests/*.bats` - Update test structure or running instructions
- `scripts/*.sh` - Update development setup if scripts change
- `tests/helpers.bash` - Update test helper documentation

### web/compress.md/ Updates
- `CRUX.md` - Update specification examples on landing page
- Feature additions - Update feature highlights
- `.cursor/agents/*` - Update agent/tooling descriptions

## Update Guidelines

1. Make surgical updates - don't rewrite entire sections
2. Keep formatting consistent with existing style
3. Update version numbers, paths, and examples to match actual code
4. If adding new workflows or test files, add them to relevant tables/lists
5. Keep the CI/CD flow diagram in CONTRIBUTORS.md accurate

## What NOT to Update

- Don't update docs for changes to example files in `.cursor/rules/example/`
- Don't update docs for temporary or generated files
- Don't add speculative features - only document what exists
- Keep documentation concise and actionable