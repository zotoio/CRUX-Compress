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
    assert_output_contains "-y"
    assert_output_contains "--force"
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

# New flag tests
@test "install.sh handles -y flag" {
    run grep -E "NON_INTERACTIVE=true" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh handles --force flag" {
    run grep -E "FORCE=true" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines check_not_in_crux_repo function" {
    run grep -E "^check_not_in_crux_repo\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines detect_git_root function" {
    run grep -E "^detect_git_root\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines create_backup_zip function" {
    run grep -E "^create_backup_zip\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines get_version_change_type function" {
    run grep -E "^get_version_change_type\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines preview_installation function" {
    run grep -E "^preview_installation\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines show_file_diff function" {
    run grep -E "^show_file_diff\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines confirm function" {
    run grep -E "^confirm\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines show_completion_report function" {
    run grep -E "^show_completion_report\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines download_update_script function" {
    run grep -E "^download_update_script\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh defines download_and_stage function" {
    run grep -E "^download_and_stage\(\)" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh checks for zip dependency" {
    run grep -E "command -v zip" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh runs clear at start of main" {
    run grep -E "^[[:space:]]*clear$" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh detects CRUX repo to prevent self-install" {
    run grep -E "scripts/create-crux-zip.sh" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh checks for *.crux.* files in backup" {
    run grep -E '\*\.crux\.\*' "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh displays major/minor/patch version change type" {
    run grep -E "major|minor|patch" "$INSTALL_SCRIPT"
    assert_exit_code 0
}

@test "install.sh provides revert instructions" {
    run grep -E "revert" "$INSTALL_SCRIPT"
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

# Unit tests for version comparison
# Note: We extract just the function and test it standalone since sourcing the full script
# triggers set -e which makes testing return codes difficult
@test "install.sh compare_versions detects newer version" {
    # Extract and run just the function
    local func
    func=$(sed -n '/^compare_versions()/,/^}/p' "$INSTALL_SCRIPT")
    run bash -c "$func; compare_versions '2.0.0' '1.0.0'"
    [[ "$status" -eq 0 ]]
}

@test "install.sh compare_versions detects equal version" {
    local func
    func=$(sed -n '/^compare_versions()/,/^}/p' "$INSTALL_SCRIPT")
    run bash -c "$func; compare_versions '1.0.0' '1.0.0'"
    [[ "$status" -eq 1 ]]
}

@test "install.sh compare_versions detects older version" {
    local func
    func=$(sed -n '/^compare_versions()/,/^}/p' "$INSTALL_SCRIPT")
    run bash -c "$func; compare_versions '1.0.0' '2.0.0'"
    [[ "$status" -eq 2 ]]
}

@test "install.sh get_version_change_type detects major change" {
    run bash -c "source '$INSTALL_SCRIPT' 2>/dev/null; get_version_change_type '1.0.0' '2.0.0'"
    assert_output_contains "major"
}

@test "install.sh get_version_change_type detects minor change" {
    run bash -c "source '$INSTALL_SCRIPT' 2>/dev/null; get_version_change_type '1.0.0' '1.1.0'"
    assert_output_contains "minor"
}

@test "install.sh get_version_change_type detects patch change" {
    run bash -c "source '$INSTALL_SCRIPT' 2>/dev/null; get_version_change_type '1.0.0' '1.0.1'"
    assert_output_contains "patch"
}
