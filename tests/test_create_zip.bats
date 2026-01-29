#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
}

teardown() {
    cleanup_temp_dir
}

@test "create-crux-zip.sh exists and is executable" {
    assert_file_exists "$CREATE_ZIP"
    [[ -x "$CREATE_ZIP" ]] || chmod +x "$CREATE_ZIP"
}

@test "create-crux-zip.sh creates a versioned zip file" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    # Check that a zip file was created
    local zip_count
    zip_count=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip 2>/dev/null | wc -l)
    [[ "$zip_count" -eq 1 ]]
}

@test "create-crux-zip.sh zip contains CRUX.md" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains "CRUX.md"
}

@test "create-crux-zip.sh zip contains AGENTS.crux.md" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains "AGENTS.crux.md"
}

@test "create-crux-zip.sh AGENTS.crux.md contains CRUX block" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    mkdir -p "$TEST_TEMP_DIR/extracted"
    unzip -q "$zip_file" -d "$TEST_TEMP_DIR/extracted"
    
    # Verify it contains the CRUX block
    run cat "$TEST_TEMP_DIR/extracted/AGENTS.crux.md"
    assert_output_contains "<CRUX"
    assert_output_contains "</CRUX>"
}

@test "create-crux-zip.sh zip contains .crux/crux.json" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".crux/crux.json"
}

@test "create-crux-zip.sh zip contains .cursor/hooks.json" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/hooks.json"
}

@test "create-crux-zip.sh zip contains crux-cursor-rule-manager.md" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/agents/crux-cursor-rule-manager.md"
}

@test "create-crux-zip.sh zip contains crux-compress.md" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/commands/crux-compress.md"
}

@test "create-crux-zip.sh zip contains crux-detect-changes.sh" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/hooks/crux-detect-changes.sh"
}

@test "create-crux-zip.sh zip contains _CRUX-RULE.mdc" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/rules/_CRUX-RULE.mdc"
}

@test "create-crux-zip.sh zip contains CRUX-Utils skill" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/skills/CRUX-Utils/SKILL.md"
    assert_output_contains ".cursor/skills/CRUX-Utils/scripts/crux-utils.sh"
}

@test "create-crux-zip.sh version in filename matches .crux/crux.json" {
    local expected_version
    if command -v jq &> /dev/null; then
        expected_version=$(jq -r '.version' "$PROJECT_ROOT/.crux/crux.json")
    else
        expected_version=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PROJECT_ROOT/.crux/crux.json" | sed 's/.*"\([^"]*\)"$/\1/')
    fi
    
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    assert_file_exists "$TEST_TEMP_DIR/CRUX-Compress-v${expected_version}.zip"
}

@test "create-crux-zip.sh extracted .crux/crux.json version matches source" {
    local expected_version
    if command -v jq &> /dev/null; then
        expected_version=$(jq -r '.version' "$PROJECT_ROOT/.crux/crux.json")
    else
        expected_version=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PROJECT_ROOT/.crux/crux.json" | sed 's/.*"\([^"]*\)"$/\1/')
    fi
    
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    mkdir -p "$TEST_TEMP_DIR/extracted"
    unzip -q "$zip_file" -d "$TEST_TEMP_DIR/extracted"
    
    local extracted_version
    if command -v jq &> /dev/null; then
        extracted_version=$(jq -r '.version' "$TEST_TEMP_DIR/extracted/.crux/crux.json")
    else
        extracted_version=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$TEST_TEMP_DIR/extracted/.crux/crux.json" | sed 's/.*"\([^"]*\)"$/\1/')
    fi
    
    [[ "$extracted_version" == "$expected_version" ]]
}

@test "create-crux-zip.sh zip contains release manifest if it exists" {
    # Check if manifest file exists at new location
    if [[ -f "$PROJECT_ROOT/.crux/crux-release-files.json" ]]; then
        run "$CREATE_ZIP" "$TEST_TEMP_DIR"
        assert_exit_code 0
        
        local zip_file
        zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
        
        run unzip -l "$zip_file"
        assert_output_contains ".crux/crux-release-files.json"
    else
        skip "Release manifest file does not exist"
    fi
}
