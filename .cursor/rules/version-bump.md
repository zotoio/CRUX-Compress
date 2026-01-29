---
alwaysApply: true
crux: true
---
# Automatic Version Bumping Rule

When committing changes, analyze commit messages and update `.crux/crux.json` version accordingly.

## Conventional Commit Version Rules

Apply semantic versioning based on conventional commit prefixes:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:` | Patch (0.0.X) | 1.0.0 → 1.0.1 |
| `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `chore:` | Patch (0.0.X) | 1.0.0 → 1.0.1 |
| `feat:` | Minor (0.X.0) | 1.0.0 → 1.1.0 |
| `BREAKING CHANGE:` in body or `!` after type | Major (X.0.0) | 1.0.0 → 2.0.0 |

## When to Apply

1. **Before creating a commit** - If the user asks you to commit changes, analyze the commit message type and bump `.crux/crux.json` version before staging
2. **Include .crux/crux.json in the commit** - Stage the updated `.crux/crux.json` along with the other changes

## Version Bump Logic

```
MAJOR.MINOR.PATCH

- MAJOR: Breaking changes (API incompatibility)
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes and minor changes (backwards compatible)
```

## Examples

- `fix: correct typo in output message` → Bump patch: 1.2.3 → 1.2.4
- `feat: add support for custom output directory` → Bump minor: 1.2.3 → 1.3.0
- `feat!: change default compression format` → Bump major: 1.2.3 → 2.0.0
- `refactor: simplify staging logic` → Bump patch: 1.2.3 → 1.2.4

## Important

- Only bump version once per commit, using the highest-impact change type
- Reset lower version numbers when bumping higher ones (1.2.3 → 2.0.0, not 2.2.3)
- Do not bump version for commits that don't follow conventional commit format (ask user to clarify) 
