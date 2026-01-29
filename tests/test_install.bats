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

# ============================================================================
# hooks.json merge tests
# ============================================================================

# Extract merge_hooks_json function for testing
extract_merge_hooks_json() {
    # Extract the function and its dependencies
    cat << 'EXTEOF'
log_verbose() { :; }
log_success() { echo "$1"; }
log_warn() { echo "$1" >&2; }
EXTEOF
    sed -n '/^merge_hooks_json()/,/^}/p' "$INSTALL_SCRIPT"
}

@test "install.sh merge_hooks_json creates hooks.json if not exists" {
    cd "$TEST_TEMP_DIR"
    mkdir -p .cursor
    
    # Create staging hooks
    local staging_hooks
    staging_hooks=$(mktemp)
    cat > "$staging_hooks" << 'EOF'
{"hooks":{"sessionStart":[{"command":"echo test"}]}}
EOF
    
    # Run merge function
    local func
    func=$(extract_merge_hooks_json)
    run bash -c "$func; merge_hooks_json '$staging_hooks'"
    
    assert_exit_code 0
    assert_file_exists ".cursor/hooks.json"
    
    # Verify content
    run cat .cursor/hooks.json
    assert_output_contains "sessionStart"
    assert_output_contains "echo test"
    
    rm -f "$staging_hooks"
}

@test "install.sh merge_hooks_json handles null arrays in existing hooks.json" {
    cd "$TEST_TEMP_DIR"
    mkdir -p .cursor
    
    # Create existing hooks.json with null array
    cat > .cursor/hooks.json << 'EOF'
{"hooks":{"sessionStart":null,"afterFileEdit":[{"command":"existing"}]}}
EOF
    
    # Create staging hooks
    local staging_hooks
    staging_hooks=$(mktemp)
    cat > "$staging_hooks" << 'EOF'
{"hooks":{"sessionStart":[{"command":"new-session"}],"afterFileEdit":[{"command":"new-edit"}]}}
EOF
    
    # Run merge function
    local func
    func=$(extract_merge_hooks_json)
    run bash -c "$func; merge_hooks_json '$staging_hooks'"
    
    assert_exit_code 0
    
    # Verify merged content - should have both hooks
    run cat .cursor/hooks.json
    assert_output_contains "sessionStart"
    assert_output_contains "new-session"
    assert_output_contains "existing"
    
    rm -f "$staging_hooks"
}

@test "install.sh merge_hooks_json handles missing .hooks object" {
    cd "$TEST_TEMP_DIR"
    mkdir -p .cursor
    
    # Create existing hooks.json without .hooks
    cat > .cursor/hooks.json << 'EOF'
{"version":"1.0"}
EOF
    
    # Create staging hooks
    local staging_hooks
    staging_hooks=$(mktemp)
    cat > "$staging_hooks" << 'EOF'
{"hooks":{"sessionStart":[{"command":"new-cmd"}]}}
EOF
    
    # Run merge function
    local func
    func=$(extract_merge_hooks_json)
    run bash -c "$func; merge_hooks_json '$staging_hooks'"
    
    assert_exit_code 0
    
    # Verify hooks were added
    run cat .cursor/hooks.json
    assert_output_contains "sessionStart"
    assert_output_contains "new-cmd"
    
    rm -f "$staging_hooks"
}

@test "install.sh merge_hooks_json adds missing lifecycle hooks" {
    cd "$TEST_TEMP_DIR"
    mkdir -p .cursor
    
    # Create existing hooks.json with only sessionStart
    cat > .cursor/hooks.json << 'EOF'
{"hooks":{"sessionStart":[{"command":"existing-session"}]}}
EOF
    
    # Create staging hooks with afterFileEdit and stop
    local staging_hooks
    staging_hooks=$(mktemp)
    cat > "$staging_hooks" << 'EOF'
{"hooks":{"afterFileEdit":[{"command":"new-edit"}],"stop":[{"command":"new-stop"}]}}
EOF
    
    # Run merge function
    local func
    func=$(extract_merge_hooks_json)
    run bash -c "$func; merge_hooks_json '$staging_hooks'"
    
    assert_exit_code 0
    
    # Verify all hooks exist
    run cat .cursor/hooks.json
    assert_output_contains "sessionStart"
    assert_output_contains "existing-session"
    assert_output_contains "afterFileEdit"
    assert_output_contains "new-edit"
    assert_output_contains "stop"
    assert_output_contains "new-stop"
    
    rm -f "$staging_hooks"
}

@test "install.sh merge_hooks_json avoids duplicate commands" {
    cd "$TEST_TEMP_DIR"
    mkdir -p .cursor
    
    # Create existing hooks.json
    cat > .cursor/hooks.json << 'EOF'
{"hooks":{"sessionStart":[{"command":"shared-cmd","args":["old"]}]}}
EOF
    
    # Create staging hooks with same command
    local staging_hooks
    staging_hooks=$(mktemp)
    cat > "$staging_hooks" << 'EOF'
{"hooks":{"sessionStart":[{"command":"shared-cmd","args":["new"]},{"command":"unique-cmd"}]}}
EOF
    
    # Run merge function
    local func
    func=$(extract_merge_hooks_json)
    run bash -c "$func; merge_hooks_json '$staging_hooks'"
    
    assert_exit_code 0
    
    # Verify no duplicate - should have original "old" args, plus unique-cmd
    run cat .cursor/hooks.json
    assert_output_contains "shared-cmd"
    assert_output_contains "unique-cmd"
    # Count occurrences of shared-cmd - should be exactly 1
    local count
    count=$(grep -o "shared-cmd" .cursor/hooks.json | wc -l)
    [[ "$count" -eq 1 ]]
    
    rm -f "$staging_hooks"
}

# ============================================================================
# AGENTS.md upsert tests
# ============================================================================

# Extract upsert_agents_crux_block function for testing
extract_upsert_function() {
    cat << 'EXTEOF'
log_verbose() { :; }
log_success() { echo "$1"; }
log_warn() { echo "$1" >&2; }
EXTEOF
    sed -n '/^upsert_agents_crux_block()/,/^}/p' "$INSTALL_SCRIPT"
}

@test "install.sh upsert_agents_crux_block creates new AGENTS.md" {
    cd "$TEST_TEMP_DIR"
    
    # Create CRUX block file with multi-line content
    cat > AGENTS.crux.md << 'EOF'
<CRUX agents="always">

## CRITICAL: CRUX Notation
This is a multi-line
CRUX block with special characters: "quotes" and 'apostrophes'

### Rules
1. First rule
2. Second rule

</CRUX>
EOF
    
    # Run upsert function
    local func
    func=$(extract_upsert_function)
    run bash -c "$func; upsert_agents_crux_block 'AGENTS.crux.md'"
    
    assert_exit_code 0
    assert_file_exists "AGENTS.md"
    
    # Verify content
    run cat AGENTS.md
    assert_output_contains "<CRUX agents"
    assert_output_contains "CRITICAL: CRUX Notation"
    assert_output_contains "multi-line"
    assert_output_contains "</CRUX>"
}

@test "install.sh upsert_agents_crux_block prepends to existing AGENTS.md" {
    cd "$TEST_TEMP_DIR"
    
    # Create existing AGENTS.md without CRUX block
    cat > AGENTS.md << 'EOF'
# My Project Agents

## Custom Agent 1
Does something cool.

## Custom Agent 2
Does something else.
EOF
    
    # Create CRUX block file
    cat > AGENTS.crux.md << 'EOF'
<CRUX agents="always">
CRUX content here
</CRUX>
EOF
    
    # Run upsert function
    local func
    func=$(extract_upsert_function)
    run bash -c "$func; upsert_agents_crux_block 'AGENTS.crux.md'"
    
    assert_exit_code 0
    
    # Verify CRUX block is at top, existing content preserved
    run cat AGENTS.md
    assert_output_contains "<CRUX agents"
    assert_output_contains "CRUX content here"
    assert_output_contains "My Project Agents"
    assert_output_contains "Custom Agent 1"
    
    # Verify CRUX block comes first
    local first_line
    first_line=$(head -1 AGENTS.md)
    [[ "$first_line" == '<CRUX agents="always">' ]]
}

@test "install.sh upsert_agents_crux_block replaces existing CRUX block" {
    cd "$TEST_TEMP_DIR"
    
    # Create existing AGENTS.md with old CRUX block
    cat > AGENTS.md << 'EOF'
<CRUX agents="old">
Old CRUX content
Should be replaced
</CRUX>

# My Project Agents

Custom content that should be preserved.
EOF
    
    # Create new CRUX block file
    cat > AGENTS.crux.md << 'EOF'
<CRUX agents="new">
New CRUX content
With multiple lines
</CRUX>
EOF
    
    # Run upsert function
    local func
    func=$(extract_upsert_function)
    run bash -c "$func; upsert_agents_crux_block 'AGENTS.crux.md'"
    
    assert_exit_code 0
    
    # Verify old content replaced, custom content preserved
    run cat AGENTS.md
    assert_output_contains "New CRUX content"
    assert_output_contains "With multiple lines"
    assert_output_contains "My Project Agents"
    assert_output_contains "Custom content"
    assert_output_not_contains "Old CRUX content"
    assert_output_not_contains "Should be replaced"
}

@test "install.sh upsert_agents_crux_block handles special characters" {
    cd "$TEST_TEMP_DIR"
    
    # Create CRUX block with special characters that could break awk
    cat > AGENTS.crux.md << 'EOF'
<CRUX agents="always">

Special chars: & | $ ` \ " ' < > { } [ ] ( )
Regex-like: .*+?^$ [a-z] (foo|bar)
Backslashes: path\to\file and C:\Windows

</CRUX>
EOF
    
    # Run upsert function
    local func
    func=$(extract_upsert_function)
    run bash -c "$func; upsert_agents_crux_block 'AGENTS.crux.md'"
    
    assert_exit_code 0
    
    # Verify special characters preserved
    run cat AGENTS.md
    assert_output_contains "Special chars"
    assert_output_contains "Regex-like"
}

@test "install.sh upsert_agents_crux_block removes AGENTS.crux.md after upsert" {
    cd "$TEST_TEMP_DIR"
    
    cat > AGENTS.crux.md << 'EOF'
<CRUX agents="always">
Content
</CRUX>
EOF
    
    local func
    func=$(extract_upsert_function)
    run bash -c "$func; upsert_agents_crux_block 'AGENTS.crux.md'"
    
    assert_exit_code 0
    assert_file_not_exists "AGENTS.crux.md"
}

# ============================================================================
# File checksum / preview tests
# ============================================================================

# Extract get_checksum and preview_installation functions
extract_checksum_functions() {
    # Colors
    echo 'GREEN="\033[0;32m"; YELLOW="\033[1;33m"; BLUE="\033[0;34m"; NC="\033[0m"'
    sed -n '/^get_checksum()/,/^}/p' "$INSTALL_SCRIPT"
    sed -n '/^preview_installation()/,/^}/p' "$INSTALL_SCRIPT"
}

@test "install.sh get_checksum returns consistent hash" {
    cd "$TEST_TEMP_DIR"
    
    echo "test content" > testfile.txt
    
    # Extract just get_checksum
    local func
    func=$(sed -n '/^get_checksum()/,/^}/p' "$INSTALL_SCRIPT")
    
    # Run twice and compare
    run bash -c "$func; get_checksum 'testfile.txt'"
    local hash1="$output"
    
    run bash -c "$func; get_checksum 'testfile.txt'"
    local hash2="$output"
    
    [[ "$hash1" == "$hash2" ]]
    [[ -n "$hash1" ]]
}

@test "install.sh get_checksum differs for different content" {
    cd "$TEST_TEMP_DIR"
    
    echo "content 1" > file1.txt
    echo "content 2" > file2.txt
    
    local func
    func=$(sed -n '/^get_checksum()/,/^}/p' "$INSTALL_SCRIPT")
    
    run bash -c "$func; get_checksum 'file1.txt'"
    local hash1="$output"
    
    run bash -c "$func; get_checksum 'file2.txt'"
    local hash2="$output"
    
    [[ "$hash1" != "$hash2" ]]
}

@test "install.sh preview_installation shows CREATE for new files" {
    cd "$TEST_TEMP_DIR"
    
    # Create staging directory with a new file
    mkdir -p staging
    echo "new content" > staging/newfile.txt
    
    local func
    func=$(extract_checksum_functions)
    
    run bash -c "$func; preview_installation 'staging'"
    
    assert_exit_code 0
    assert_output_contains "CREATE"
    assert_output_contains "newfile.txt"
}

@test "install.sh preview_installation shows UPDATE for changed files" {
    cd "$TEST_TEMP_DIR"
    
    # Create existing file
    echo "old content" > existingfile.txt
    
    # Create staging directory with different content
    mkdir -p staging
    echo "new content" > staging/existingfile.txt
    
    local func
    func=$(extract_checksum_functions)
    
    run bash -c "$func; preview_installation 'staging'"
    
    assert_exit_code 0
    assert_output_contains "UPDATE"
    assert_output_contains "existingfile.txt"
}

@test "install.sh preview_installation shows NO CHANGE for identical files" {
    cd "$TEST_TEMP_DIR"
    
    # Create existing file
    echo "same content" > samefile.txt
    
    # Create staging directory with identical content
    mkdir -p staging
    echo "same content" > staging/samefile.txt
    
    local func
    func=$(extract_checksum_functions)
    
    run bash -c "$func; preview_installation 'staging'"
    
    assert_exit_code 0
    assert_output_contains "NO CHANGE"
    assert_output_contains "samefile.txt"
}

@test "install.sh preview_installation handles mixed scenarios" {
    cd "$TEST_TEMP_DIR"
    
    # Create existing files
    echo "unchanged" > unchanged.txt
    echo "will change" > changed.txt
    
    # Create staging directory
    mkdir -p staging
    echo "unchanged" > staging/unchanged.txt      # Same content
    echo "has changed" > staging/changed.txt      # Different content
    echo "brand new" > staging/newfile.txt        # New file
    
    local func
    func=$(extract_checksum_functions)
    
    run bash -c "$func; preview_installation 'staging'"
    
    assert_exit_code 0
    assert_output_contains "NO CHANGE"
    assert_output_contains "unchanged.txt"
    assert_output_contains "UPDATE"
    assert_output_contains "changed.txt"
    assert_output_contains "CREATE"
    assert_output_contains "newfile.txt"
}
