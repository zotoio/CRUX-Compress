# Contributing to CRUX Compress

Thank you for your interest in contributing to CRUX Compress! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive experience for everyone.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/CRUX-Compress.git`
3. Add the upstream remote: `git remote add upstream https://github.com/zotoio/CRUX-Compress.git`
4. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Bash 4.0+
- [BATS](https://github.com/bats-core/bats-core) (Bash Automated Testing System) for running tests
- `jq` for JSON processing
- `bc` for calculations

### Installing BATS

```bash
# macOS (Homebrew)
brew install bats-core

# Ubuntu/Debian
sudo apt-get install bats

# Or install from source
git clone https://github.com/bats-core/bats-core.git
cd bats-core
./install.sh /usr/local
```

## Testing

CRUX Compress uses [BATS](https://github.com/bats-core/bats-core) (Bash Automated Testing System) for testing. All shell scripts have corresponding test suites.

### Test Structure

```
tests/
├── fixtures/               # Test fixtures and sample files
│   ├── compress-test.crux.mdc
│   ├── compress-test.md
│   ├── no-change.crux.mdc
│   ├── no-change.md
│   ├── no-crux-frontmatter.mdc
│   ├── sample-rule.crux.mdc
│   ├── sample-rule.md
│   └── special-chars.md
├── helpers.bash            # Shared test utilities and assertions
├── test_create_zip.bats    # Tests for scripts/create-crux-zip.sh
├── test_crux_utils.bats    # Tests for CRUX-Utils skill
├── test_detect_hook.bats   # Tests for the detect-crux-changes.sh hook
└── test_install.bats       # Tests for install.sh
```

### Test Suites

| Test File | Script Under Test | Coverage |
|-----------|------------------|----------|
| `test_install.bats` | `install.sh` | Installation script validation, CLI options, dependencies |
| `test_crux_utils.bats` | `.cursor/skills/CRUX-Utils/scripts/crux-utils.sh` | Token counting, checksums, compression ratio |
| `test_detect_hook.bats` | `.cursor/hooks/detect-crux-changes.sh` | Hook triggering, file filtering, queue management |
| `test_create_zip.bats` | `scripts/create-crux-zip.sh` | Zip creation, version matching, required files |

### Running Tests

```bash
# Run all tests
bats tests/*.bats

# Run a specific test file
bats tests/test_install.bats

# Run with verbose output
bats tests/*.bats --verbose-run

# Run with TAP output (used in CI)
bats tests/*.bats --formatter tap

# Run tests matching a pattern
bats tests/*.bats --filter "install"
```

### Test Helpers

The `tests/helpers.bash` file provides common utilities:

```bash
# Setup/teardown for temp directories
setup_temp_dir      # Creates TEST_TEMP_DIR
cleanup_temp_dir    # Removes TEST_TEMP_DIR

# File assertions
assert_file_exists "$path"
assert_file_not_exists "$path"
assert_dir_exists "$path"

# Output assertions
assert_output_contains "expected string"
assert_output_not_contains "unexpected string"

# Exit code assertion
assert_exit_code 0
```

### Writing New Tests

1. Create a new `.bats` file in the `tests/` directory
2. Load helpers at the top: `load 'helpers'`
3. Use `setup()` and `teardown()` for test isolation
4. Name tests descriptively: `@test "script handles edge case correctly"`

Example:

```bash
#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
}

teardown() {
    cleanup_temp_dir
}

@test "my-script.sh handles empty input" {
    run ./my-script.sh ""
    assert_exit_code 1
    assert_output_contains "Error: empty input"
}
```

### CI Integration

Tests run automatically on:
- Push to `main` branch
- Push to `feature/**` branches
- Pull requests to `main`

The CI pipeline (`.github/workflows/test.yml`) runs:
1. BATS test suite
2. Zip creation validation
3. Install script syntax check
4. ShellCheck linting

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

| Prefix | Version Bump | Example |
|--------|-------------|---------|
| `fix:` | Patch (0.0.x) | `fix: correct token counting for unicode` |
| `feat:` | Minor (0.x.0) | `feat: add compression ratio display` |
| `feat!:` or `BREAKING CHANGE` | Major (x.0.0) | `feat!: change output format` |

Other prefixes (`docs:`, `chore:`, `test:`, `refactor:`, `style:`) trigger a patch bump.

### Examples

```bash
# Bug fix (1.0.0 → 1.0.1)
git commit -m "fix: handle empty files gracefully"

# New feature (1.0.1 → 1.1.0)
git commit -m "feat: add --verbose flag to install script"

# Breaking change (1.1.0 → 2.0.0)
git commit -m "feat!: change CRUX notation syntax

BREAKING CHANGE: The arrow operator → is now required"
```

## Pull Request Process

1. **Update tests**: Add or update tests for any new functionality
2. **Run tests locally**: Ensure all tests pass with `bats tests/*.bats`
3. **Check linting**: Run ShellCheck on your scripts
4. **Update documentation**: Update README.md if you've changed functionality
5. **Descriptive PR title**: Use conventional commit format
6. **Link issues**: Reference any related issues with "Fixes #123" or "Relates to #456"

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] ShellCheck passes
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventional commits
- [ ] No merge conflicts with main

## Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the problem
2. **Steps to reproduce**: Minimal steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Bash version, BATS version (if relevant)
6. **Logs/Output**: Any error messages or relevant output

## Release Process

Releases are fully automated via GitHub Actions. The CI/CD pipeline ensures that version bumps only occur when tests pass and release-relevant files change.

### CI/CD Flow

```
Push to main
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Test Workflow (.github/workflows/test.yml)                     │
│  ├─ Run BATS test suite                                         │
│  ├─ Validate zip creation                                       │
│  ├─ Check install script syntax                                 │
│  └─ Run ShellCheck linting                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ success
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Version Bump Workflow (.github/workflows/version-bump.yml)     │
│  ├─ Check if release-relevant files changed                     │
│  │   (skips if only docs, tests, or non-release files changed) │
│  ├─ Analyze commit message for bump type (feat→minor, fix→patch)│
│  └─ Update .crux/crux.json and CRUX.md, commit with [skip ci]   │
└────────────────────────────┬────────────────────────────────────┘
                             │ Version changed
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Release Workflow (.github/workflows/release.yml)               │
│  ├─ Generate checksums for release files                        │
│  ├─ Update scripts/crux-release-files.json manifest             │
│  ├─ Build distribution zip (CRUX-Compress-vX.Y.Z.zip)           │
│  ├─ Create GitHub Release with tag vX.Y.Z                       │
│  ├─ Generate release notes from commits                         │
│  └─ Update CHANGELOG.md and commit                              │
└─────────────────────────────────────────────────────────────────┘
```

### Release-Relevant Files

Version bumps only occur when these files change (matches distribution zip contents):

| File/Path | Description |
|-----------|-------------|
| `CRUX.md` | Core specification |
| `AGENTS.md` | Agent awareness block |
| `.crux/crux.json` | Version metadata |
| `.crux/crux-release-files.json` | Release manifest with checksums |
| `.cursor/hooks.json` | Hook configuration |
| `.cursor/agents/crux-cursor-rule-manager.md` | Subagent definition |
| `.cursor/commands/crux-compress.md` | Command definition |
| `.cursor/hooks/detect-crux-changes.sh` | Hook script |
| `.cursor/rules/_CRUX-RULE.mdc` | Always-applied rule |
| `.cursor/skills/CRUX-Utils/**` | Utility skill |

Changes to other files (README, tests, examples, scripts) do **not** trigger releases.

### Manual Version Bump

If you need to force a version bump:

1. Go to **Actions** → **Version Bump** workflow
2. Click **Run workflow**
3. Select bump type: `patch`, `minor`, or `major`
4. Click **Run workflow**

### Version Bump Rules

| Commit Prefix | Version Bump | Example |
|---------------|-------------|---------|
| `fix:` | Patch (0.0.x) | `fix: correct token counting` |
| `feat:` | Minor (0.x.0) | `feat: add new operator` |
| `feat!:` or `BREAKING CHANGE` | Major (x.0.0) | `feat!: change syntax` |
| Other (`docs:`, `chore:`, etc.) | Patch (0.0.x) | `docs: update README` |

## Questions?

Feel free to open an issue for questions or discussions about contributions.
