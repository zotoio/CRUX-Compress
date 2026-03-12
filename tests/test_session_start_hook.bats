#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir

    mkdir -p "$TEST_TEMP_DIR/.cursor/rules"
    mkdir -p "$TEST_TEMP_DIR/.cursor/hooks"
    mkdir -p "$TEST_TEMP_DIR/.crux"

    cp "$SESSION_START_HOOK" "$TEST_TEMP_DIR/.cursor/hooks/"
    chmod +x "$TEST_TEMP_DIR/.cursor/hooks/crux-session-start.sh"
}

teardown() {
    cleanup_temp_dir
}

@test "session-start removes stale pending entries when CRUX output is current" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/stale.md" << 'EOF'
---
crux: true
---

# Stale Rule
EOF
    cat > "$TEST_TEMP_DIR/.cursor/rules/stale.crux.md" << 'EOF'
---
generated: 2026-01-01 00:00
---

compressed
EOF
    touch -t 202601010000 "$TEST_TEMP_DIR/.cursor/rules/stale.md"
    touch -t 202601010100 "$TEST_TEMP_DIR/.cursor/rules/stale.crux.md"
    echo '{"files":[".cursor/rules/stale.md"]}' > "$TEST_TEMP_DIR/.crux/pending-compression.json"

    cd "$TEST_TEMP_DIR"
    run bash .cursor/hooks/crux-session-start.sh <<< '{}'
    assert_exit_code 0
    assert_output_contains "{}"

    run jq -r '.files | length' "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains "0"
}

@test "session-start keeps non-stale pending entries and alerts agent" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/pending.md" << 'EOF'
---
crux: true
---

# Pending Rule
EOF
    cat > "$TEST_TEMP_DIR/.cursor/rules/pending.crux.mdc" << 'EOF'
---
generated: 2026-01-01 00:00
---

compressed
EOF
    touch -t 202601010000 "$TEST_TEMP_DIR/.cursor/rules/pending.crux.mdc"
    touch -t 202601010100 "$TEST_TEMP_DIR/.cursor/rules/pending.md"
    echo '{"files":[".cursor/rules/pending.md"]}' > "$TEST_TEMP_DIR/.crux/pending-compression.json"

    cd "$TEST_TEMP_DIR"
    run bash .cursor/hooks/crux-session-start.sh <<< '{}'
    assert_exit_code 0
    assert_output_contains "additional_context"
    assert_output_contains ".cursor/rules/pending.md"

    run jq -r '.files[]?' "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/pending.md"
}
