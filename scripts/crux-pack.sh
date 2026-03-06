#!/usr/bin/env bash
#
# CRUX Knowledge Packets (CRUX-KP) — Pack
#
# Bundles multiple CRUX-compressed files into a single portable JSON
# "knowledge packet" optimized for cross-agent, cross-model context transfer.
#
# Usage:
#   crux-pack.sh [options] <file1.crux.md> [file2.crux.md ...]
#   crux-pack.sh --dir <directory>
#   crux-pack.sh --stdin
#
# Options:
#   --output, -o <file>    Output file (default: stdout)
#   --source-model <name>  Tag the source model (e.g., "claude", "gpt-4")
#   --target-model <name>  Tag the intended target model
#   --label <text>         Human-readable label for the packet
#   --dir <directory>      Pack all .crux.md files in directory
#   --stdin                Read file list from stdin (one per line)
#   --compact              Omit whitespace in JSON output
#   --help, -h             Show this help

set -euo pipefail

CRUX_VERSION=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

show_help() {
    cat << 'EOF'
CRUX Knowledge Packets — Pack

Bundles CRUX-compressed files into a portable JSON knowledge packet
for cross-agent, cross-model context transfer.

Usage:
  crux-pack.sh [options] <file1.crux.md> [file2.crux.md ...]
  crux-pack.sh --dir <directory>
  crux-pack.sh --stdin

Options:
  --output, -o <file>    Output file (default: stdout)
  --source-model <name>  Tag the source model (e.g., "claude", "gpt-4")
  --target-model <name>  Tag the intended target model
  --label <text>         Human-readable label for the packet
  --dir <directory>      Pack all .crux.md files in directory
  --stdin                Read file list from stdin (one per line)
  --compact              Omit whitespace in JSON output
  --help, -h             Show this help

Examples:
  crux-pack.sh .cursor/rules/*.crux.md -o context.crux.json
  crux-pack.sh --dir .cursor/rules/ --source-model claude
  find . -name "*.crux.md" | crux-pack.sh --stdin --compact
EOF
}

log() {
    echo "[crux-pack] $*" >&2
}

detect_crux_version() {
    local crux_json="$REPO_ROOT/.crux/crux.json"
    if [[ -f "$crux_json" ]]; then
        CRUX_VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$crux_json" | head -1 | grep -o '"[^"]*"$' | tr -d '"')
    fi
    if [[ -z "$CRUX_VERSION" ]]; then
        CRUX_VERSION="unknown"
    fi
}

generate_packet_id() {
    if command -v uuidgen &>/dev/null; then
        uuidgen | tr '[:upper:]' '[:lower:]'
    elif [[ -f /proc/sys/kernel/random/uuid ]]; then
        cat /proc/sys/kernel/random/uuid
    else
        date +%s%N | sha256sum | head -c 36
    fi
}

detect_modality() {
    local file="$1"
    local content
    content=$(cat "$file")

    if echo "$content" | grep -qE '⟦CRUX:.*\.(png|jpg|jpeg|gif|webp|svg|bmp|tiff)'; then
        echo "image"
    elif echo "$content" | grep -qE '⟦CRUX:.*\.(sh|bash|ts|tsx|js|jsx|py|rs|go|java|rb|c|cpp|sql|css|scss)'; then
        echo "code"
    else
        echo "text"
    fi
}

detect_language() {
    local file="$1"
    local source_ref
    source_ref=$(grep -oE '⟦CRUX:[^[:space:]⟧]+' "$file" | head -1 | sed 's/⟦CRUX://')

    if [[ -z "$source_ref" ]]; then
        echo "unknown"
        return
    fi

    local ext="${source_ref##*.}"
    case "$ext" in
        md|mdc|markdown) echo "markdown" ;;
        sh|bash) echo "shell" ;;
        ts|tsx) echo "typescript" ;;
        js|jsx) echo "javascript" ;;
        py) echo "python" ;;
        rs) echo "rust" ;;
        go) echo "go" ;;
        java) echo "java" ;;
        rb) echo "ruby" ;;
        css|scss) echo "css" ;;
        sql) echo "sql" ;;
        png|jpg|jpeg|gif|webp|svg) echo "$ext" ;;
        *) echo "$ext" ;;
    esac
}

estimate_tokens_simple() {
    local file="$1"
    local chars
    chars=$(wc -c < "$file" | tr -d ' ')
    echo $(( (chars + 3) / 4 ))
}

json_escape() {
    local input="$1"
    printf '%s' "$input" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()), end="")' 2>/dev/null \
        || printf '%s' "$input" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | awk '{printf "%s\\n", $0}' | sed '$ s/\\n$//'
}

build_packet() {
    local -a files=("$@")
    local packet_id
    packet_id=$(generate_packet_id)
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    local -a modalities_seen=()
    local total_tokens=0
    local blocks_json=""
    local file_count=0

    for file in "${files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log "Warning: skipping missing file: $file"
            continue
        fi

        local modality
        modality=$(detect_modality "$file")
        local language
        language=$(detect_language "$file")
        local tokens
        tokens=$(estimate_tokens_simple "$file")
        local crux_content
        crux_content=$(cat "$file")
        local source_ref
        source_ref=$(grep -oE '⟦CRUX:[^[:space:]⟧]+' "$file" | head -1 | sed 's/⟦CRUX://' || echo "$file")
        local checksum
        checksum=$(cksum "$file" | awk '{print $1}')

        local escaped_content
        escaped_content=$(json_escape "$crux_content")
        local escaped_source
        escaped_source=$(json_escape "$source_ref")

        local found=0
        for m in "${modalities_seen[@]+"${modalities_seen[@]}"}"; do
            if [[ "$m" == "$modality" ]]; then
                found=1
                break
            fi
        done
        if [[ "$found" -eq 0 ]]; then
            modalities_seen+=("$modality")
        fi

        total_tokens=$((total_tokens + tokens))

        if [[ -n "$blocks_json" ]]; then
            blocks_json+=","
        fi

        blocks_json+="{"
        blocks_json+="\"source\":$escaped_source,"
        blocks_json+="\"type\":\"$modality\","
        blocks_json+="\"language\":\"$language\","
        blocks_json+="\"tokens\":$tokens,"
        blocks_json+="\"checksum\":\"$checksum\","
        blocks_json+="\"crux\":$escaped_content"
        blocks_json+="}"

        file_count=$((file_count + 1))
    done

    if [[ "$file_count" -eq 0 ]]; then
        log "Error: no valid CRUX files found"
        exit 1
    fi

    local modalities_json="["
    local first=1
    for m in "${modalities_seen[@]}"; do
        if [[ "$first" -eq 0 ]]; then
            modalities_json+=","
        fi
        modalities_json+="\"$m\""
        first=0
    done
    modalities_json+="]"

    local source_model_field=""
    if [[ -n "${SOURCE_MODEL:-}" ]]; then
        source_model_field="\"source_model\":\"$SOURCE_MODEL\","
    fi

    local target_model_field=""
    if [[ -n "${TARGET_MODEL:-}" ]]; then
        target_model_field="\"target_model\":\"$TARGET_MODEL\","
    fi

    local label_field=""
    if [[ -n "${PACKET_LABEL:-}" ]]; then
        local escaped_label
        escaped_label=$(json_escape "$PACKET_LABEL")
        label_field="\"label\":$escaped_label,"
    fi

    local json="{"
    json+="\"crux_kp_version\":\"1.0.0\","
    json+="\"crux_spec_version\":\"$CRUX_VERSION\","
    json+="\"packet_id\":\"$packet_id\","
    json+="\"created\":\"$timestamp\","
    json+="$source_model_field"
    json+="$target_model_field"
    json+="$label_field"
    json+="\"modalities\":$modalities_json,"
    json+="\"block_count\":$file_count,"
    json+="\"total_tokens\":$total_tokens,"
    json+="\"blocks\":[$blocks_json]"
    json+="}"

    if [[ "${COMPACT:-0}" -eq 1 ]]; then
        echo "$json"
    else
        if command -v python3 &>/dev/null; then
            echo "$json" | python3 -m json.tool 2>/dev/null || echo "$json"
        elif command -v jq &>/dev/null; then
            echo "$json" | jq . 2>/dev/null || echo "$json"
        else
            echo "$json"
        fi
    fi
}

# ============================================================
# Main
# ============================================================

OUTPUT_FILE=""
SOURCE_MODEL=""
TARGET_MODEL=""
PACKET_LABEL=""
COMPACT=0
FROM_DIR=""
FROM_STDIN=0
FILES=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            show_help
            exit 0
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --source-model)
            SOURCE_MODEL="$2"
            shift 2
            ;;
        --target-model)
            TARGET_MODEL="$2"
            shift 2
            ;;
        --label)
            PACKET_LABEL="$2"
            shift 2
            ;;
        --dir)
            FROM_DIR="$2"
            shift 2
            ;;
        --stdin)
            FROM_STDIN=1
            shift
            ;;
        --compact)
            COMPACT=1
            shift
            ;;
        -*)
            log "Error: Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            FILES+=("$1")
            shift
            ;;
    esac
done

detect_crux_version

if [[ -n "$FROM_DIR" ]]; then
    while IFS= read -r -d '' f; do
        FILES+=("$f")
    done < <(find "$FROM_DIR" -name "*.crux.md" -type f -print0 | sort -z)
fi

if [[ "$FROM_STDIN" -eq 1 ]]; then
    while IFS= read -r line; do
        [[ -n "$line" ]] && FILES+=("$line")
    done
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
    log "Error: no input files specified"
    echo "Usage: crux-pack.sh [options] <file1.crux.md> [file2.crux.md ...]" >&2
    exit 1
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    build_packet "${FILES[@]}" > "$OUTPUT_FILE"
    log "Packed ${#FILES[@]} CRUX files → $OUTPUT_FILE"
else
    build_packet "${FILES[@]}"
fi
