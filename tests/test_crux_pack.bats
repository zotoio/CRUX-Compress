#!/usr/bin/env bats

# Tests for CRUX Knowledge Packets (crux-pack.sh and crux-unpack.sh)

load helpers

CRUX_PACK="${PROJECT_ROOT}/scripts/crux-pack.sh"
CRUX_UNPACK="${PROJECT_ROOT}/scripts/crux-unpack.sh"

setup() {
    setup_temp_dir

    # Create sample CRUX files for packing
    mkdir -p "$TEST_TEMP_DIR/crux-files"

    cat > "$TEST_TEMP_DIR/crux-files/rule1.crux.md" << 'EOF'
⟦CRUX:coding-standards.md
Ρ{team dev standards}
Κ{fn=function;cls=class}
R.style{indent=2sp;¬tabs!;line≤100ch}
Ω{quality≻speed}
⟧
EOF

    cat > "$TEST_TEMP_DIR/crux-files/script1.crux.md" << 'EOF'
⟦CRUX:deploy.sh
Ρ{deployment script;bash}
Κ{curl,jq,aws-cli}
Λ.deploy{env,tag→exit_code; validate»build»push»verify}
P.err{deploy_fail→rollback»notify}
Ω.decomp{emulate=shellcheck;src=sh;focus=[quoting,io_redir]}
⟧
EOF

    cat > "$TEST_TEMP_DIR/crux-files/image1.crux.md" << 'EOF'
⟦CRUX:architecture.png
Ρ{system architecture diagram}
Κ{box=service;arrow=data flow}
Π.layout{L→R;client@left→api@center→db@right}
E.client{shape:browser;style:blue}
E.api{shape:hexagon;label="API Gateway"}
E.db{shape:cylinder;label="PostgreSQL"}
Ω.metaphor{request flow through system layers}
⟧
EOF

    # Create a .crux directory with crux.json for version detection
    mkdir -p "$TEST_TEMP_DIR/.crux"
    echo '{"version": "2.6.0"}' > "$TEST_TEMP_DIR/.crux/crux.json"
}

teardown() {
    cleanup_temp_dir
}

# ============================================================
# crux-pack.sh tests
# ============================================================

@test "crux-pack: shows help with --help" {
    run bash "$CRUX_PACK" --help
    assert_exit_code 0
    assert_output_contains "Knowledge Packets"
    assert_output_contains "Usage"
}

@test "crux-pack: shows help with -h" {
    run bash "$CRUX_PACK" -h
    assert_exit_code 0
    assert_output_contains "Knowledge Packets"
}

@test "crux-pack: fails with no arguments" {
    run bash "$CRUX_PACK"
    assert_exit_code 1
    assert_output_contains "no input files"
}

@test "crux-pack: packs single CRUX file to stdout" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "crux_kp_version"
    assert_output_contains "packet_id"
    assert_output_contains "blocks"
    assert_output_contains "coding-standards.md"
}

@test "crux-pack: packs multiple CRUX files" {
    run bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/script1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/image1.crux.md"
    assert_exit_code 0
    assert_output_contains "block_count"
    assert_output_contains "coding-standards.md"
    assert_output_contains "deploy.sh"
    assert_output_contains "architecture.png"
}

@test "crux-pack: detects text modality" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "\"type\": \"text\""
}

@test "crux-pack: detects code modality" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/script1.crux.md"
    assert_exit_code 0
    assert_output_contains "\"type\": \"code\""
}

@test "crux-pack: detects image modality" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/image1.crux.md"
    assert_exit_code 0
    assert_output_contains "\"type\": \"image\""
}

@test "crux-pack: multi-modal packet lists all modalities" {
    run bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/script1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/image1.crux.md"
    assert_exit_code 0
    assert_output_contains "text"
    assert_output_contains "code"
    assert_output_contains "image"
}

@test "crux-pack: writes to output file with -o" {
    run bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        -o "$TEST_TEMP_DIR/output.crux.json"
    assert_exit_code 0
    assert_file_exists "$TEST_TEMP_DIR/output.crux.json"
    # Verify it's valid JSON
    python3 -c "import json; json.load(open('$TEST_TEMP_DIR/output.crux.json'))"
}

@test "crux-pack: --dir packs all .crux.md files in directory" {
    run bash "$CRUX_PACK" --dir "$TEST_TEMP_DIR/crux-files"
    assert_exit_code 0
    assert_output_contains "block_count"
    # Should find all 3 files
    assert_output_contains "coding-standards.md"
    assert_output_contains "deploy.sh"
    assert_output_contains "architecture.png"
}

@test "crux-pack: --source-model tags the packet" {
    run bash "$CRUX_PACK" \
        --source-model "claude-4" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "source_model"
    assert_output_contains "claude-4"
}

@test "crux-pack: --target-model tags the packet" {
    run bash "$CRUX_PACK" \
        --target-model "gpt-4o" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "target_model"
    assert_output_contains "gpt-4o"
}

@test "crux-pack: --label adds human-readable label" {
    run bash "$CRUX_PACK" \
        --label "Frontend coding standards for Q1 sprint" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "label"
    assert_output_contains "Frontend coding standards"
}

@test "crux-pack: --compact outputs without formatting" {
    run bash "$CRUX_PACK" --compact "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    # Compact output should be a single line (no pretty-printing)
    local line_count
    line_count=$(echo "$output" | grep -v '^\[crux-pack\]' | wc -l)
    [ "$line_count" -le 2 ]
}

@test "crux-pack: includes token counts" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "total_tokens"
    assert_output_contains "tokens"
}

@test "crux-pack: includes checksums per block" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/rule1.crux.md"
    assert_exit_code 0
    assert_output_contains "checksum"
}

@test "crux-pack: detects language from source reference" {
    run bash "$CRUX_PACK" "$TEST_TEMP_DIR/crux-files/script1.crux.md"
    assert_exit_code 0
    assert_output_contains "\"language\": \"shell\""
}

@test "crux-pack: skips missing files with warning" {
    run bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/nonexistent.crux.md"
    assert_exit_code 0
    assert_output_contains "skipping missing file"
}

@test "crux-pack: --stdin reads file list from stdin" {
    echo "$TEST_TEMP_DIR/crux-files/rule1.crux.md" | run bash "$CRUX_PACK" --stdin
    assert_exit_code 0
}

# ============================================================
# crux-unpack.sh tests
# ============================================================

@test "crux-unpack: shows help with --help" {
    run bash "$CRUX_UNPACK" --help
    assert_exit_code 0
    assert_output_contains "Knowledge Packets"
    assert_output_contains "Unpack"
}

@test "crux-unpack: fails with no arguments" {
    run bash "$CRUX_UNPACK"
    assert_exit_code 1
    assert_output_contains "no packet file"
}

@test "crux-unpack: fails with missing file" {
    run bash "$CRUX_UNPACK" "$TEST_TEMP_DIR/nonexistent.json"
    assert_exit_code 1
    assert_output_contains "file not found"
}

@test "crux-unpack: --info shows packet metadata" {
    bash "$CRUX_PACK" \
        --label "test packet" \
        --source-model "claude" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/script1.crux.md" \
        -o "$TEST_TEMP_DIR/packet.crux.json"

    run bash "$CRUX_UNPACK" --info "$TEST_TEMP_DIR/packet.crux.json"
    assert_exit_code 0
    assert_output_contains "CRUX Knowledge Packet"
    assert_output_contains "Packet ID"
    assert_output_contains "Block Count"
    assert_output_contains "coding-standards.md"
    assert_output_contains "deploy.sh"
}

@test "crux-unpack: --validate passes for valid packet" {
    bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        -o "$TEST_TEMP_DIR/valid.crux.json"

    run bash "$CRUX_UNPACK" --validate "$TEST_TEMP_DIR/valid.crux.json"
    assert_exit_code 0
    assert_output_contains "PASS"
}

@test "crux-unpack: --validate fails for invalid JSON" {
    echo "not json" > "$TEST_TEMP_DIR/invalid.json"

    run bash "$CRUX_UNPACK" --validate "$TEST_TEMP_DIR/invalid.json"
    assert_exit_code 1
    assert_output_contains "FAIL"
}

@test "crux-unpack: --validate detects missing required fields" {
    echo '{"blocks": []}' > "$TEST_TEMP_DIR/incomplete.json"

    run bash "$CRUX_UNPACK" --validate "$TEST_TEMP_DIR/incomplete.json"
    assert_exit_code 1
    assert_output_contains "Missing required field"
}

@test "crux-unpack: --extract writes .crux.md files" {
    bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/script1.crux.md" \
        -o "$TEST_TEMP_DIR/packet.crux.json"

    run bash "$CRUX_UNPACK" \
        --extract "$TEST_TEMP_DIR/packet.crux.json" \
        --output-dir "$TEST_TEMP_DIR/unpacked"
    assert_exit_code 0
    assert_output_contains "Extracted"
    assert_dir_exists "$TEST_TEMP_DIR/unpacked"

    # Check that files were created
    local file_count
    file_count=$(find "$TEST_TEMP_DIR/unpacked" -name "*.crux.md" | wc -l)
    [ "$file_count" -eq 2 ]
}

@test "crux-unpack: --filter extracts only matching type" {
    bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/script1.crux.md" \
        "$TEST_TEMP_DIR/crux-files/image1.crux.md" \
        -o "$TEST_TEMP_DIR/mixed.crux.json"

    run bash "$CRUX_UNPACK" \
        --extract "$TEST_TEMP_DIR/mixed.crux.json" \
        --output-dir "$TEST_TEMP_DIR/code-only" \
        --filter code
    assert_exit_code 0

    local file_count
    file_count=$(find "$TEST_TEMP_DIR/code-only" -name "*.crux.md" | wc -l)
    [ "$file_count" -eq 1 ]
}

@test "crux-pack: round-trip preserves CRUX content" {
    bash "$CRUX_PACK" \
        "$TEST_TEMP_DIR/crux-files/rule1.crux.md" \
        -o "$TEST_TEMP_DIR/rt-packet.crux.json"

    bash "$CRUX_UNPACK" \
        --extract "$TEST_TEMP_DIR/rt-packet.crux.json" \
        --output-dir "$TEST_TEMP_DIR/rt-unpacked"

    # Find the extracted file and verify CRUX content is preserved
    local extracted_file
    extracted_file=$(find "$TEST_TEMP_DIR/rt-unpacked" -name "*.crux.md" | head -1)
    [ -n "$extracted_file" ]

    run grep "⟦CRUX:coding-standards.md" "$extracted_file"
    assert_exit_code 0

    run grep "Ρ{team dev standards}" "$extracted_file"
    assert_exit_code 0

    run grep "Ω{quality≻speed}" "$extracted_file"
    assert_exit_code 0
}
