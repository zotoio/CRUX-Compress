#!/usr/bin/env bash
#
# CRUX Utils - Multi-purpose utility for CRUX compression workflows
#
# Usage:
#   crux-utils.sh --token-count <file>
#   crux-utils.sh --token-count --ratio <source_file> <crux_file>
#   crux-utils.sh --cksum <file>
#
# Modes:
#   --token-count   Estimate token count for a file
#   --cksum         Get checksum of a file (for sourceChecksum tracking)

set -euo pipefail

# CRUX and common special Unicode characters (1 token each)
SPECIAL_CHARS='«»⟨⟩→←≻≺⊤⊥∀∃¬∋⊳⊲≥≤≠ΔΡΛΠΚΓΦΩθ⊛◊'

# Token estimation ratios (chars per token)
PROSE_RATIO=4.0
CODE_RATIO=3.5

show_help() {
    cat << 'EOF'
CRUX Utils - Multi-purpose utility for CRUX compression workflows

Usage:
  crux-utils.sh --token-count <file>
  crux-utils.sh --token-count --ratio <source_file> <crux_file>
  crux-utils.sh --cksum <file>

Modes:
  --token-count   Estimate token count for a file
                  Use --ratio to compare source vs CRUX files
  --cksum         Get checksum of a file (for sourceChecksum tracking)
                  Output format: "checksum" (for CRUX frontmatter)

Examples:
  crux-utils.sh --token-count myfile.md
  crux-utils.sh --token-count --ratio source.md source.crux.mdc
  crux-utils.sh --cksum myfile.md
EOF
}

# ============================================================
# Token Count Functions
# ============================================================

count_special_chars() {
    local file="$1"
    local count=0
    
    while IFS= read -r -n1 char; do
        if [[ "$SPECIAL_CHARS" == *"$char"* ]] && [[ -n "$char" ]]; then
            ((count++)) || true
        fi
    done < "$file"
    
    echo "$count"
}

extract_code_blocks() {
    local file="$1"
    awk '/^```/{if(in_block){in_block=0}else{in_block=1;next}} in_block{print}' "$file"
}

extract_prose() {
    local file="$1"
    awk '/^```/{in_block=!in_block;next} !in_block{print}' "$file"
}

count_chars_without_special() {
    local content="$1"
    local cleaned
    cleaned=$(echo "$content" | tr -d "$SPECIAL_CHARS")
    echo -n "$cleaned" | wc -c | tr -d ' '
}

estimate_tokens() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        exit 1
    fi
    
    local special_count
    special_count=$(count_special_chars "$file")
    
    local code_content
    code_content=$(extract_code_blocks "$file")
    local code_chars
    code_chars=$(count_chars_without_special "$code_content")
    
    local prose_content
    prose_content=$(extract_prose "$file")
    local prose_chars
    prose_chars=$(count_chars_without_special "$prose_content")
    
    local prose_tokens code_tokens total_tokens
    prose_tokens=$(echo "scale=0; $prose_chars / $PROSE_RATIO" | bc)
    code_tokens=$(echo "scale=0; $code_chars / $CODE_RATIO" | bc)
    total_tokens=$(echo "$prose_tokens + $code_tokens + $special_count" | bc)
    
    local filename
    filename=$(basename "$file")
    
    echo "=== Token Estimate: $filename ==="
    echo "Prose tokens:      $prose_tokens"
    echo "Code tokens:       $code_tokens"
    echo "Special tokens:    $special_count"
    echo "---"
    echo "TOTAL TOKENS:      $total_tokens"
    
    echo "$total_tokens" > /tmp/crux_utils_token_result_$$
}

calculate_ratio() {
    local source_file="$1"
    local crux_file="$2"
    
    echo "=== Compression Ratio Analysis ==="
    echo ""
    
    estimate_tokens "$source_file"
    local source_tokens
    source_tokens=$(cat /tmp/crux_utils_token_result_$$)
    rm -f /tmp/crux_utils_token_result_$$
    
    echo ""
    
    estimate_tokens "$crux_file"
    local crux_tokens
    crux_tokens=$(cat /tmp/crux_utils_token_result_$$)
    rm -f /tmp/crux_utils_token_result_$$
    
    echo ""
    echo "=== Compression Summary ==="
    echo "Source tokens:     $source_tokens"
    echo "CRUX tokens:       $crux_tokens"
    
    if [[ "$source_tokens" -gt 0 ]]; then
        local ratio
        ratio=$(echo "scale=1; ($crux_tokens * 100) / $source_tokens" | bc)
        echo "Ratio:             ${ratio}% of original"
        
        local reduction
        reduction=$(echo "scale=1; 100 - $ratio" | bc)
        echo "Reduction:         ${reduction}%"
        
        local target_met
        if (( $(echo "$ratio <= 20" | bc -l) )); then
            target_met="YES"
        else
            target_met="NO"
        fi
        echo "Target (≤20%):     $target_met"
    fi
}

run_token_count() {
    shift  # Remove --token-count
    
    if [[ $# -eq 0 ]]; then
        echo "Error: --token-count requires a file argument" >&2
        echo "Usage: crux-utils.sh --token-count <file>" >&2
        echo "       crux-utils.sh --token-count --ratio <source> <crux>" >&2
        exit 1
    fi
    
    if [[ "$1" == "--ratio" ]]; then
        if [[ $# -ne 3 ]]; then
            echo "Error: --ratio requires two file arguments" >&2
            echo "Usage: crux-utils.sh --token-count --ratio <source> <crux>" >&2
            exit 1
        fi
        calculate_ratio "$2" "$3"
    else
        estimate_tokens "$1"
        rm -f /tmp/crux_utils_token_result_$$ 2>/dev/null || true
    fi
}

# ============================================================
# Checksum Functions
# ============================================================

run_cksum() {
    shift  # Remove --cksum
    
    if [[ $# -eq 0 ]]; then
        echo "Error: --cksum requires a file argument" >&2
        echo "Usage: crux-utils.sh --cksum <file>" >&2
        exit 1
    fi
    
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        exit 1
    fi
    
    # Run cksum and extract only the checksum value
    # cksum outputs: checksum bytes filename
    # We only need the checksum for sourceChecksum frontmatter
    local result
    result=$(cksum "$file")
    local checksum
    checksum=$(echo "$result" | awk '{print $1}')
    
    echo "=== Checksum: $(basename "$file") ==="
    echo "Checksum:          $checksum"
    echo "---"
    echo "FRONTMATTER:       \"$checksum\""
}

# ============================================================
# Main
# ============================================================

if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

case "$1" in
    --token-count)
        run_token_count "$@"
        ;;
    --cksum)
        run_cksum "$@"
        ;;
    --help|-h)
        show_help
        ;;
    *)
        echo "Error: Unknown mode: $1" >&2
        echo "Use --help for usage information" >&2
        exit 1
        ;;
esac
