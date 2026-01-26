#!/usr/bin/env bash
# Shared test helpers for BATS tests

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BATS_TEST_FILENAME}")/.." && pwd)"

# Path to scripts under test
CRUX_UTILS="${PROJECT_ROOT}/.cursor/skills/CRUX-Utils/scripts/crux-utils.sh"
CREATE_ZIP="${PROJECT_ROOT}/create-crux-zip.sh"
DETECT_HOOK="${PROJECT_ROOT}/.cursor/hooks/detect-crux-changes.sh"
INSTALL_SCRIPT="${PROJECT_ROOT}/install.sh"

# Path to test fixtures
FIXTURES="${PROJECT_ROOT}/tests/fixtures"

# Create a temporary directory for test artifacts
setup_temp_dir() {
    TEST_TEMP_DIR=$(mktemp -d)
    export TEST_TEMP_DIR
}

# Clean up temporary directory
cleanup_temp_dir() {
    if [[ -n "$TEST_TEMP_DIR" && -d "$TEST_TEMP_DIR" ]]; then
        rm -rf "$TEST_TEMP_DIR"
    fi
}

# Create a sample markdown file for testing
create_sample_md() {
    local path="$1"
    cat > "$path" << 'EOF'
---
crux: true
alwaysApply: true
---

# Sample Rule

This is a sample rule for testing CRUX compression.

## Guidelines

1. Always write clean code
2. Follow naming conventions
3. Add proper documentation

### Code Style

- Use consistent indentation
- Keep functions small
- Write meaningful comments

```javascript
function example() {
    const result = processData(input);
    return result;
}
```

## Summary

This rule ensures code quality across the project.
EOF
}

# Create a sample CRUX file for testing
create_sample_crux() {
    local path="$1"
    cat > "$path" << 'EOF'
---
generated: 2024-01-01 12:00
sourceChecksum: "1234567890"
beforeTokens: 500
afterTokens: 100
confidence: 95%
alwaysApply: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Sample Rule

```crux
«CRUX⟨sample-rule.md⟩»

Κ{code:clean;naming:conventions;docs:proper}
R.style{indent:consistent;fn:small;comments:meaningful}

«/CRUX»
```
EOF
}

# Assert that a file exists
assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "Expected file to exist: $file"
        return 1
    fi
}

# Assert that a file does not exist
assert_file_not_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo "Expected file to not exist: $file"
        return 1
    fi
}

# Assert that a directory exists
assert_dir_exists() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "Expected directory to exist: $dir"
        return 1
    fi
}

# Assert that output contains a string
assert_output_contains() {
    local expected="$1"
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected output to contain: $expected"
        echo "Actual output: $output"
        return 1
    fi
}

# Assert that output does not contain a string
assert_output_not_contains() {
    local unexpected="$1"
    if [[ "$output" == *"$unexpected"* ]]; then
        echo "Expected output to not contain: $unexpected"
        echo "Actual output: $output"
        return 1
    fi
}

# Assert exit code
assert_exit_code() {
    local expected="$1"
    if [[ "$status" -ne "$expected" ]]; then
        echo "Expected exit code: $expected"
        echo "Actual exit code: $status"
        return 1
    fi
}
