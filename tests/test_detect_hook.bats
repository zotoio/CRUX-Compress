#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
    
    # Create a mock project structure
    mkdir -p "$TEST_TEMP_DIR/.cursor/rules"
    mkdir -p "$TEST_TEMP_DIR/.cursor/hooks"
    mkdir -p "$TEST_TEMP_DIR/.crux"
    
    # Copy the hook script
    cp "$DETECT_HOOK" "$TEST_TEMP_DIR/.cursor/hooks/"
    chmod +x "$TEST_TEMP_DIR/.cursor/hooks/crux-detect-changes.sh"
}

teardown() {
    cleanup_temp_dir
}

@test "crux-detect-changes.sh exists and is executable" {
    assert_file_exists "$DETECT_HOOK"
    [[ -x "$DETECT_HOOK" ]] || chmod +x "$DETECT_HOOK"
}

@test "hook queues file with crux: true frontmatter" {
    # Create a rule file with crux: true
    cat > "$TEST_TEMP_DIR/.cursor/rules/test-rule.md" << 'EOF'
---
crux: true
---

# Test Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called with JSON input
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Check that the file was queued
    assert_file_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
    
    # Verify the file is in the queue
    run cat "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/test-rule.md"
}

@test "hook ignores file without crux: true frontmatter" {
    # Create a rule file without crux: true
    cat > "$TEST_TEMP_DIR/.cursor/rules/no-crux.md" << 'EOF'
---
alwaysApply: true
---

# No CRUX Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called
    echo '{"file_path": ".cursor/rules/no-crux.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook ignores .crux.md files" {
    # Create a .crux.md file (universal CRUX output)
    cat > "$TEST_TEMP_DIR/.cursor/rules/test.crux.md" << 'EOF'
---
crux: true
generated: 2024-01-01
---

# Compressed Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called
    echo '{"file_path": ".cursor/rules/test.crux.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook ignores .crux.mdc files" {
    # Create a .crux.mdc file (Cursor adapter)
    cat > "$TEST_TEMP_DIR/.cursor/rules/test.crux.mdc" << 'EOF'
---
crux: true
generated: 2024-01-01
alwaysApply: true
---

# Compressed Rule (Cursor adapter)
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called
    echo '{"file_path": ".cursor/rules/test.crux.mdc"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook ignores files outside .cursor/rules" {
    # Create a file outside .cursor/rules
    mkdir -p "$TEST_TEMP_DIR/docs"
    cat > "$TEST_TEMP_DIR/docs/test.md" << 'EOF'
---
crux: true
---

# Outside Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called
    echo '{"file_path": "docs/test.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook avoids duplicate entries in queue" {
    # Create a rule file
    cat > "$TEST_TEMP_DIR/.cursor/rules/test-rule.md" << 'EOF'
---
crux: true
---

# Test Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Call the hook twice for the same file
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Count occurrences of the file path
    local count
    count=$(grep -o 'test-rule.md' "$TEST_TEMP_DIR/.crux/pending-compression.json" | wc -l)
    
    [[ "$count" -eq 1 ]]
}

@test "hook creates valid JSON in pending file" {
    # Create a rule file
    cat > "$TEST_TEMP_DIR/.cursor/rules/test-rule.md" << 'EOF'
---
crux: true
---

# Test Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    # Validate JSON with jq
    run jq '.' "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_exit_code 0
}

@test "hook handles crux: true with spaces" {
    # Create a rule file with spaces around crux: true
    cat > "$TEST_TEMP_DIR/.cursor/rules/spaced.md" << 'EOF'
---
crux:   true
---

# Spaced Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/spaced.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook queues file with numeric crux value" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/numeric-level.md" << 'EOF'
---
crux: 40
---

# Numeric Level Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/numeric-level.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
    run cat "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/numeric-level.md"
}

@test "hook queues file with crux: 100" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/max-level.md" << 'EOF'
---
crux: 100
---

# Max Level Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/max-level.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
    run cat "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/max-level.md"
}

@test "hook queues file with crux: 1" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/min-level.md" << 'EOF'
---
crux: 1
---

# Min Level Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/min-level.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
    run cat "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/min-level.md"
}

@test "hook ignores file with crux: 0" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/zero-level.md" << 'EOF'
---
crux: 0
---

# Zero Level Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/zero-level.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook ignores file with crux: false" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/false-crux.md" << 'EOF'
---
crux: false
---

# False CRUX Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/false-crux.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook ignores file with crux: arbitrary string" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/string-crux.md" << 'EOF'
---
crux: something
---

# String CRUX Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    echo '{"file_path": ".cursor/rules/string-crux.md"}' | bash .cursor/hooks/crux-detect-changes.sh
    
    assert_file_not_exists "$TEST_TEMP_DIR/.crux/pending-compression.json"
}

@test "hook cleanup removes stale pending entry when output is current" {
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
    echo '{"file_path":"docs/ignored.md"}' | bash .cursor/hooks/crux-detect-changes.sh

    run jq -r '.files | length' "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains "0"
}

@test "hook cleanup keeps pending entry when source is newer than output" {
    cat > "$TEST_TEMP_DIR/.cursor/rules/fresh.md" << 'EOF'
---
crux: true
---

# Fresh Rule
EOF
    cat > "$TEST_TEMP_DIR/.cursor/rules/fresh.crux.mdc" << 'EOF'
---
generated: 2026-01-01 00:00
---

compressed
EOF
    touch -t 202601010000 "$TEST_TEMP_DIR/.cursor/rules/fresh.crux.mdc"
    touch -t 202601010100 "$TEST_TEMP_DIR/.cursor/rules/fresh.md"
    echo '{"files":[".cursor/rules/fresh.md"]}' > "$TEST_TEMP_DIR/.crux/pending-compression.json"

    cd "$TEST_TEMP_DIR"
    echo '{"file_path":"docs/ignored.md"}' | bash .cursor/hooks/crux-detect-changes.sh

    run jq -r '.files[]?' "$TEST_TEMP_DIR/.crux/pending-compression.json"
    assert_output_contains ".cursor/rules/fresh.md"
}
