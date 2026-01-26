#!/usr/bin/env bash
#
# Token Count Estimator
# Deterministic token estimation for markdown and code files
#
# Usage:
#   count-tokens.sh <file>
#   count-tokens.sh --ratio <source_file> <crux_file>
#
# Estimation ratios:
#   - Prose: 4.0 chars/token
#   - Code:  3.5 chars/token
#   - Special Unicode: 1 token each

set -euo pipefail

# CRUX and common special Unicode characters (1 token each)
SPECIAL_CHARS='«»⟨⟩→←≻≺⊤⊥∀∃¬∋⊳⊲≥≤≠ΔΡΛΠΚΓΦΩθ⊛◊'

# Ratios (chars per token)
PROSE_RATIO=4.0
CODE_RATIO=3.5

count_special_chars() {
    local file="$1"
    local count=0
    
    # Count each special character occurrence
    while IFS= read -r -n1 char; do
        if [[ "$SPECIAL_CHARS" == *"$char"* ]] && [[ -n "$char" ]]; then
            ((count++)) || true
        fi
    done < "$file"
    
    echo "$count"
}

extract_code_blocks() {
    local file="$1"
    # Extract content between ``` markers
    awk '/^```/{if(in_block){in_block=0}else{in_block=1;next}} in_block{print}' "$file"
}

extract_prose() {
    local file="$1"
    # Extract content outside ``` markers (prose/markdown)
    awk '/^```/{in_block=!in_block;next} !in_block{print}' "$file"
}

count_chars_without_special() {
    local content="$1"
    # Remove special chars and count remaining
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
    
    # Count special characters (1 token each)
    local special_count
    special_count=$(count_special_chars "$file")
    
    # Extract and count code block characters
    local code_content
    code_content=$(extract_code_blocks "$file")
    local code_chars
    code_chars=$(count_chars_without_special "$code_content")
    
    # Extract and count prose characters
    local prose_content
    prose_content=$(extract_prose "$file")
    local prose_chars
    prose_chars=$(count_chars_without_special "$prose_content")
    
    # Calculate tokens using bc for floating point
    local prose_tokens code_tokens total_tokens
    prose_tokens=$(echo "scale=0; $prose_chars / $PROSE_RATIO" | bc)
    code_tokens=$(echo "scale=0; $code_chars / $CODE_RATIO" | bc)
    total_tokens=$(echo "$prose_tokens + $code_tokens + $special_count" | bc)
    
    # Output results
    local filename
    filename=$(basename "$file")
    
    echo "=== Token Estimate: $filename ==="
    echo "Prose tokens:      $prose_tokens"
    echo "Code tokens:       $code_tokens"
    echo "Special tokens:    $special_count"
    echo "---"
    echo "TOTAL TOKENS:      $total_tokens"
    
    # Return total for ratio calculation
    echo "$total_tokens" > /tmp/token_count_result_$$
}

calculate_ratio() {
    local source_file="$1"
    local crux_file="$2"
    
    echo "=== Compression Ratio Analysis ==="
    echo ""
    
    # Get source tokens
    estimate_tokens "$source_file"
    local source_tokens
    source_tokens=$(cat /tmp/token_count_result_$$)
    rm -f /tmp/token_count_result_$$
    
    echo ""
    
    # Get CRUX tokens
    estimate_tokens "$crux_file"
    local crux_tokens
    crux_tokens=$(cat /tmp/token_count_result_$$)
    rm -f /tmp/token_count_result_$$
    
    echo ""
    echo "=== Compression Summary ==="
    echo "Source tokens:     $source_tokens"
    echo "CRUX tokens:       $crux_tokens"
    
    # Calculate ratio percentage
    if [[ "$source_tokens" -gt 0 ]]; then
        local ratio
        ratio=$(echo "scale=1; ($crux_tokens * 100) / $source_tokens" | bc)
        echo "Ratio:             ${ratio}% of original"
        
        local reduction
        reduction=$(echo "scale=1; 100 - $ratio" | bc)
        echo "Reduction:         ${reduction}%"
        
        # Check against target
        local target_met
        if (( $(echo "$ratio <= 20" | bc -l) )); then
            target_met="YES"
        else
            target_met="NO"
        fi
        echo "Target (≤20%):     $target_met"
    fi
}

# Main
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <file>"
    echo "       $0 --ratio <source_file> <crux_file>"
    exit 1
fi

if [[ "$1" == "--ratio" ]]; then
    if [[ $# -ne 3 ]]; then
        echo "Usage: $0 --ratio <source_file> <crux_file>"
        exit 1
    fi
    calculate_ratio "$2" "$3"
else
    estimate_tokens "$1"
    rm -f /tmp/token_count_result_$$ 2>/dev/null || true
fi
