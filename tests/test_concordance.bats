#!/usr/bin/env bats

load 'helpers'

setup() {
    setup_temp_dir
}

teardown() {
    cleanup_temp_dir
}

create_crux_file_a() {
    local path="$1"
    cat > "$path" << 'EOF'
---
generated: 2025-01-01 12:00
sourceChecksum: "1111111111"
beforeTokens: 500
afterTokens: 100
---

# Architecture

```crux
⟦CRUX:architecture.md
Ρ{api server}
Κ{token=JWT;db=postgres}
E.UserService{
  auth=oauth2;roles=[admin,user,guest]
}
E.OrderService{
  payment=stripe;queue=redis
}
Λ.deploy{env=[staging,prod]}
Λ.build{target=docker}
Π.core{src/services/;src/handlers/}
Φ{port=3000;timeout=30}
Ω{cov≥80%;lint=strict}
⟧
```
EOF
}

create_crux_file_b() {
    local path="$1"
    cat > "$path" << 'EOF'
---
generated: 2025-01-01 12:00
sourceChecksum: "2222222222"
beforeTokens: 600
afterTokens: 120
---

# Implementation

```crux
⟦CRUX:implementation.md
Ρ{api server}
Κ{token=JWT;db=postgres;cache=redis}
E.UserService{
  auth=oauth2;roles=[admin,user]
}
E.PaymentService{
  provider=stripe;webhook=enabled
}
Λ.build{target=docker}
Λ.test{runner=jest}
Π.core{src/services/;src/middleware/}
Φ{port=3000;timeout=60}
Ω{cov≥90%;lint=strict}
⟧
```
EOF
}

create_crux_file_identical() {
    local path="$1"
    cat > "$path" << 'EOF'
---
generated: 2025-01-01 12:00
sourceChecksum: "3333333333"
beforeTokens: 500
afterTokens: 100
---

# Same Content

```crux
⟦CRUX:same.md
Ρ{api server}
Κ{token=JWT;db=postgres}
E.UserService{auth=oauth2}
Λ.deploy{env=[staging,prod]}
Φ{port=3000}
⟧
```
EOF
}

create_crux_file_disjoint() {
    local path="$1"
    cat > "$path" << 'EOF'
---
generated: 2025-01-01 12:00
sourceChecksum: "4444444444"
beforeTokens: 400
afterTokens: 80
---

# Completely Different

```crux
⟦CRUX:different.md
Ρ{mobile app}
Κ{framework=react_native;state=redux}
E.ScreenManager{navigation=stack}
E.ThemeProvider{mode=[dark,light]}
Λ.lint{tool=eslint}
Φ{platform=ios;version=16}
⟧
```
EOF
}

@test "crux-concordance.sh exists and is executable" {
    assert_file_exists "$CONCORDANCE_SCRIPT"
    [[ -x "$CONCORDANCE_SCRIPT" ]] || chmod +x "$CONCORDANCE_SCRIPT"
}

@test "crux-concordance.sh --help shows usage" {
    run "$CONCORDANCE_SCRIPT" --help
    assert_exit_code 0
    assert_output_contains "CRUX Concordance Analyzer"
    assert_output_contains "--threshold"
    assert_output_contains "--json"
    assert_output_contains "--dir"
}

@test "crux-concordance.sh with no args shows error" {
    run "$CONCORDANCE_SCRIPT"
    assert_exit_code 1
    assert_output_contains "At least 2 CRUX files required"
}

@test "crux-concordance.sh with one file shows error" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md"
    assert_exit_code 1
    assert_output_contains "At least 2 CRUX files required"
}

@test "crux-concordance.sh with missing file shows error" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/nonexistent.crux.md"
    assert_exit_code 1
    assert_output_contains "File not found"
}

@test "crux-concordance.sh compares two similar files" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_b "$TEST_TEMP_DIR/b.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md"
    assert_output_contains "Concordance Analysis Report"
    assert_output_contains "Score:"
    assert_output_contains "Shared:"
}

@test "crux-concordance.sh reports high concordance for identical files" {
    create_crux_file_identical "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_identical "$TEST_TEMP_DIR/b.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md"
    assert_exit_code 0
    assert_output_contains "100%"
    assert_output_contains "at or above threshold"
}

@test "crux-concordance.sh detects drift between disjoint files" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_disjoint "$TEST_TEMP_DIR/b.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md"
    assert_exit_code 2
    assert_output_contains "DRIFT DETECTED"
}

@test "crux-concordance.sh --json outputs valid JSON" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_b "$TEST_TEMP_DIR/b.crux.md"
    run "$CONCORDANCE_SCRIPT" --json "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md"
    assert_output_contains "\"threshold\":"
    assert_output_contains "\"averageConcordance\":"
    assert_output_contains "\"pairs\":"
    assert_output_contains "\"status\":"
}

@test "crux-concordance.sh --threshold adjusts sensitivity" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_b "$TEST_TEMP_DIR/b.crux.md"

    # Very low threshold should pass
    run "$CONCORDANCE_SCRIPT" --threshold 10 "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md"
    assert_exit_code 0
    assert_output_contains "at or above threshold"
}

@test "crux-concordance.sh --threshold rejects invalid values" {
    run "$CONCORDANCE_SCRIPT" --threshold 200
    assert_exit_code 1
    assert_output_contains "must be 0-100"
}

@test "crux-concordance.sh --dir scans directory" {
    mkdir -p "$TEST_TEMP_DIR/rules"
    create_crux_file_a "$TEST_TEMP_DIR/rules/a.crux.md"
    create_crux_file_b "$TEST_TEMP_DIR/rules/b.crux.md"
    run "$CONCORDANCE_SCRIPT" --dir "$TEST_TEMP_DIR/rules"
    assert_output_contains "Concordance Analysis Report"
    assert_output_contains "a.crux.md"
    assert_output_contains "b.crux.md"
}

@test "crux-concordance.sh --dir with nonexistent dir shows error" {
    run "$CONCORDANCE_SCRIPT" --dir "$TEST_TEMP_DIR/nonexistent"
    assert_exit_code 1
    assert_output_contains "Directory not found"
}

@test "crux-concordance.sh compares three files" {
    create_crux_file_a "$TEST_TEMP_DIR/a.crux.md"
    create_crux_file_b "$TEST_TEMP_DIR/b.crux.md"
    create_crux_file_disjoint "$TEST_TEMP_DIR/c.crux.md"
    run "$CONCORDANCE_SCRIPT" "$TEST_TEMP_DIR/a.crux.md" "$TEST_TEMP_DIR/b.crux.md" "$TEST_TEMP_DIR/c.crux.md"
    assert_output_contains "Files Analyzed:"
    assert_output_contains "Pairs Evaluated:"
    assert_output_contains "[1]"
    assert_output_contains "[2]"
    assert_output_contains "[3]"
}

@test "crux-concordance.sh unknown option shows error" {
    run "$CONCORDANCE_SCRIPT" --foobar
    assert_exit_code 1
    assert_output_contains "Unknown option"
}
