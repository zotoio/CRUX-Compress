#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
    create_sample_md "$TEST_TEMP_DIR/sample.md"
    create_sample_crux "$TEST_TEMP_DIR/sample.crux.mdc"
}

teardown() {
    cleanup_temp_dir
}

@test "crux-utils.sh exists and is executable" {
    assert_file_exists "$CRUX_UTILS"
    [[ -x "$CRUX_UTILS" ]] || chmod +x "$CRUX_UTILS"
}

@test "crux-utils.sh --help shows usage" {
    run "$CRUX_UTILS" --help
    assert_exit_code 0
    assert_output_contains "CRUX Utils"
    assert_output_contains "--token-count"
    assert_output_contains "--cksum"
}

@test "crux-utils.sh with no args shows help" {
    run "$CRUX_UTILS"
    assert_exit_code 0
    assert_output_contains "Usage:"
}

@test "crux-utils.sh --token-count estimates tokens for a file" {
    run "$CRUX_UTILS" --token-count "$TEST_TEMP_DIR/sample.md"
    assert_exit_code 0
    assert_output_contains "Token Estimate"
    assert_output_contains "TOTAL TOKENS"
    assert_output_contains "Prose tokens"
    assert_output_contains "Code tokens"
}

@test "crux-utils.sh --token-count fails for non-existent file" {
    run "$CRUX_UTILS" --token-count "$TEST_TEMP_DIR/nonexistent.md"
    assert_exit_code 1
    assert_output_contains "File not found"
}

@test "crux-utils.sh --token-count --ratio compares two files" {
    run "$CRUX_UTILS" --token-count --ratio "$TEST_TEMP_DIR/sample.md" "$TEST_TEMP_DIR/sample.crux.mdc"
    assert_exit_code 0
    assert_output_contains "Compression Ratio Analysis"
    assert_output_contains "Compression Summary"
    assert_output_contains "Source tokens"
    assert_output_contains "CRUX tokens"
    assert_output_contains "Ratio"
}

@test "crux-utils.sh --token-count --ratio fails with wrong number of args" {
    run "$CRUX_UTILS" --token-count --ratio "$TEST_TEMP_DIR/sample.md"
    assert_exit_code 1
    assert_output_contains "requires two file arguments"
}

@test "crux-utils.sh --cksum calculates checksum" {
    run "$CRUX_UTILS" --cksum "$TEST_TEMP_DIR/sample.md"
    assert_exit_code 0
    assert_output_contains "Checksum"
    assert_output_contains "FRONTMATTER"
}

@test "crux-utils.sh --cksum produces consistent output" {
    run "$CRUX_UTILS" --cksum "$TEST_TEMP_DIR/sample.md"
    local first_output="$output"
    
    run "$CRUX_UTILS" --cksum "$TEST_TEMP_DIR/sample.md"
    local second_output="$output"
    
    [[ "$first_output" == "$second_output" ]]
}

@test "crux-utils.sh --cksum fails for non-existent file" {
    run "$CRUX_UTILS" --cksum "$TEST_TEMP_DIR/nonexistent.md"
    assert_exit_code 1
    assert_output_contains "File not found"
}

@test "crux-utils.sh unknown mode fails" {
    run "$CRUX_UTILS" --unknown-mode
    assert_exit_code 1
    assert_output_contains "Unknown mode"
}

@test "crux-utils.sh token count for CRUX file counts special chars" {
    # Create a file with CRUX special characters
    cat > "$TEST_TEMP_DIR/special.crux.mdc" << 'EOF'
# Test
«CRUX⟨test.md⟩»
Κ{code→clean}
R.style{indent→consistent}
∀fn→small
«/CRUX»
EOF
    
    run "$CRUX_UTILS" --token-count "$TEST_TEMP_DIR/special.crux.mdc"
    assert_exit_code 0
    assert_output_contains "Special tokens"
}
