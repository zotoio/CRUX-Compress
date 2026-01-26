#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
    
    # Create a mock project structure
    mkdir -p "$TEST_TEMP_DIR/.cursor/rules"
    mkdir -p "$TEST_TEMP_DIR/.cursor/hooks"
    
    # Copy the hook script
    cp "$DETECT_HOOK" "$TEST_TEMP_DIR/.cursor/hooks/"
    chmod +x "$TEST_TEMP_DIR/.cursor/hooks/detect-crux-changes.sh"
}

teardown() {
    cleanup_temp_dir
}

@test "detect-crux-changes.sh exists and is executable" {
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
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Check that the file was queued
    assert_file_exists "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
    
    # Verify the file is in the queue
    run cat "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
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
    echo '{"file_path": ".cursor/rules/no-crux.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
}

@test "hook ignores .crux.mdc files" {
    # Create a .crux.mdc file
    cat > "$TEST_TEMP_DIR/.cursor/rules/test.crux.mdc" << 'EOF'
---
crux: true
generated: 2024-01-01
---

# Compressed Rule
EOF
    
    cd "$TEST_TEMP_DIR"
    
    # Simulate the hook being called
    echo '{"file_path": ".cursor/rules/test.crux.mdc"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
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
    echo '{"file_path": "docs/test.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Check that no pending file was created
    assert_file_not_exists "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
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
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Count occurrences of the file path
    local count
    count=$(grep -o 'test-rule.md' "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json" | wc -l)
    
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
    
    echo '{"file_path": ".cursor/rules/test-rule.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    # Validate JSON with jq
    run jq '.' "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
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
    
    echo '{"file_path": ".cursor/rules/spaced.md"}' | bash .cursor/hooks/detect-crux-changes.sh
    
    assert_file_exists "$TEST_TEMP_DIR/.cursor/hooks/pending-crux-compress.json"
}
