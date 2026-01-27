---
crux: true
alwaysApply: true
description: A test rule for compress command testing
---

# Test Coding Standards Rule

This rule defines coding standards and best practices for the test suite. Follow these guidelines when writing or modifying test code.

## File Naming Conventions

| File Type | Pattern | Example |
|-----------|---------|---------|
| Unit tests | `test_*.bats` | `test_utils.bats` |
| Fixtures | `*.md` or `*.mdc` | `sample-rule.md` |
| Helpers | `helpers.bash` | `helpers.bash` |

## Test Structure Guidelines

### Setup and Teardown

1. Always use `setup()` to initialize test environment
2. Always use `teardown()` to clean up temporary files
3. Never leave test artifacts in the working directory
4. Use `$BATS_TMPDIR` for temporary test files

### Assertions

- Use `assert_success` for commands that should succeed
- Use `assert_failure` for commands that should fail
- Use `assert_output --partial` for substring matching
- Use `assert_line` for checking specific output lines

## Code Examples

### Good Test Pattern

```bash
@test "function handles empty input gracefully" {
  run my_function ""
  assert_failure
  assert_output --partial "Error: empty input"
}
```

### Bad Test Pattern (Avoid)

```bash
@test "test something" {
  my_function ""  # No run, no assertions
}
```

## When to Apply

- Apply when writing new BATS tests
- Apply when reviewing test pull requests
- Apply when debugging test failures

## Critical Rules

1. **NEVER** skip the `run` command before assertions
2. **ALWAYS** clean up temporary files in teardown
3. **MUST** use descriptive test names that explain the scenario
4. **AVOID** hardcoded paths - use variables instead

## Error Handling

When a test fails:

1. Check the `$output` variable for error messages
2. Check `$status` for the exit code
3. Review the `$lines` array for line-by-line output
4. Enable `set -x` temporarily for debugging
