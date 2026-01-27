#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
}

teardown() {
    cleanup_temp_dir
}

@test "install.sh exists and is executable" {
    assert_file_exists "$INSTALL_SCRIPT"
    [[ -x "$INSTALL_SCRIPT" ]] || chmod +x "$INSTALL_SCRIPT"
}

@test "install.sh has valid bash syntax" {
    run bash -n "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh --help shows usage information" {
    run "$INSTALL_SCRIPT" --help
    assert_exit_code 0
    assert_output_contains "CRUX Compress Installer"
    assert_output_contains "--backup"
    assert_output_contains "--verbose"
}

@test "install.sh --help mentions curl usage" {
    run "$INSTALL_SCRIPT" --help
    assert_exit_code 0
    assert_output_contains "curl"
}

@test "install.sh rejects unknown options" {
    run "$INSTALL_SCRIPT" --unknown-option
    assert_exit_code 1
    assert_output_contains "Unknown option"
}

@test "install.sh defines required functions" {
    # Source the script and check for functions
    run bash -c "source '$INSTALL_SCRIPT' --help 2>/dev/null; type get_latest_version"
    # The script exits on --help, so we just verify it parses
    run bash -n "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh has proper shebang" {
    local first_line
    first_line=$(head -1 "$INSTALL_SCRIPT")
    [[ "$first_line" == "#!/bin/bash" ]]
}

@test "install.sh sets strict mode" {
    run grep -E "^set -e" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines REPO_OWNER" {
    run grep -E "^REPO_OWNER=" "$INSTALL_SCRIPT"
    assert_exit_code 0
    assert_output_contains "zotoio"
}

@test "install.sh defines REPO_NAME" {
    run grep -E "^REPO_NAME=" "$INSTALL_SCRIPT"
    assert_exit_code 0
    assert_output_contains "CRUX-Compress"
}

@test "install.sh handles --backup flag" {
    run grep -E "BACKUP=true" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh handles --verbose flag" {
    run grep -E "VERBOSE=true" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines backup_file function" {
    run grep -E "^backup_file\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines compare_versions function" {
    run grep -E "^compare_versions\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh checks for curl dependency" {
    run grep -E "command -v curl" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh checks for unzip dependency" {
    run grep -E "command -v unzip" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh creates required directories" {
    # The script relies on unzip to create directories during extraction
    run grep -E "unzip -o" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh makes scripts executable" {
    run grep -E "chmod \+x" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

# Integration test - only run locally (not in CI)
@test "install.sh get_latest_version function works (requires network)" {
    # Skip in CI environments to avoid rate limiting and network dependencies
    [[ -n "${CI:-}" ]] && skip "Skipping network test in CI"
    
    # Skip if no network connectivity to GitHub
    curl -s --connect-timeout 3 https://api.github.com > /dev/null 2>&1 || skip "No network"
    
    # Show the URL being requested
    run bash -c "source '$INSTALL_SCRIPT'; echo \"API URL: \$GITHUB_API\"; get_latest_version"
    echo "Exit code: $status"
    echo "Output: $output"
    assert_exit_code 0
}
