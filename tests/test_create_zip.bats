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

@test "create-crux-zip.sh zip contains VERSION" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains "VERSION"
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

@test "create-crux-zip.sh zip contains detect-crux-changes.sh" {
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    run unzip -l "$zip_file"
    assert_output_contains ".cursor/hooks/detect-crux-changes.sh"
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

@test "create-crux-zip.sh version in filename matches VERSION" {
    local expected_version
    expected_version=$(cat "$PROJECT_ROOT/VERSION" | tr -d '[:space:]')
    
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    assert_file_exists "$TEST_TEMP_DIR/CRUX-Compress-v${expected_version}.zip"
}

@test "create-crux-zip.sh extracted VERSION matches source" {
    local expected_version
    expected_version=$(cat "$PROJECT_ROOT/VERSION" | tr -d '[:space:]')
    
    run "$CREATE_ZIP" "$TEST_TEMP_DIR"
    assert_exit_code 0
    
    local zip_file
    zip_file=$(ls "$TEST_TEMP_DIR"/CRUX-Compress-v*.zip)
    
    mkdir -p "$TEST_TEMP_DIR/extracted"
    unzip -q "$zip_file" -d "$TEST_TEMP_DIR/extracted"
    
    local extracted_version
    extracted_version=$(cat "$TEST_TEMP_DIR/extracted/VERSION" | tr -d '[:space:]')
    
    [[ "$extracted_version" == "$expected_version" ]]
}
