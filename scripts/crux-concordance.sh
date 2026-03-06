#!/bin/bash
# CRUX Concordance Analyzer — Cross-Modal Semantic Drift Detection
#
# Compares entity graphs extracted from multiple CRUX-compressed artifacts
# (code, documentation, images) to detect semantic inconsistencies.
#
# Usage:
#   ./scripts/crux-concordance.sh <file1.crux.md> <file2.crux.md> [file3.crux.md ...]
#   ./scripts/crux-concordance.sh --dir <directory>
#   ./scripts/crux-concordance.sh --help
#
# Options:
#   --dir <path>    Scan a directory for all .crux.md files
#   --json          Output results as JSON
#   --threshold <N> Set concordance warning threshold (default: 70)
#   --help          Show this help message
#
# Exit codes:
#   0 - All concordance scores above threshold
#   1 - Error (missing files, bad arguments)
#   2 - Concordance below threshold (drift detected)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_ROOT
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

OUTPUT_JSON=false
THRESHOLD=70
FILES=()
SCAN_DIR=""

usage() {
    cat << 'EOF'
CRUX Concordance Analyzer — Cross-Modal Semantic Drift Detection

Usage:
  crux-concordance <file1.crux.md> <file2.crux.md> [file3.crux.md ...]
  crux-concordance --dir <directory>
  crux-concordance --help

Options:
  --dir <path>    Scan a directory recursively for all .crux.md files
  --json          Output results as JSON
  --threshold <N> Set concordance warning threshold 0-100 (default: 70)
  --help          Show this help message

Description:
  Compares entity graphs extracted from multiple CRUX-compressed artifacts
  to detect semantic drift — inconsistencies between how different artifacts
  (code, docs, images) describe the same system.

  Entity extraction parses CRUX standard blocks:
    Ρ (Repository)  E (Entities)    Λ (Commands)   Π (Architecture)
    Κ (Concepts)    R (Requirements) P (Policies)   Γ (Orchestration)
    M (Memory)      Φ (Configuration) Ω (Quality)

  The concordance score uses Jaccard similarity:
    score = |shared entities| / |all unique entities| × 100

Exit codes:
  0 - All concordance scores at or above threshold
  1 - Error (missing files, bad arguments)
  2 - Concordance below threshold (drift detected)

Examples:
  crux-concordance docs.crux.md code.crux.md
  crux-concordance --dir .cursor/rules/ --threshold 80
  crux-concordance arch-diagram.crux.md src/main.crux.md api-spec.crux.md --json
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                usage
                exit 0
                ;;
            --json)
                OUTPUT_JSON=true
                shift
                ;;
            --threshold)
                if [[ -z "${2:-}" ]]; then
                    echo -e "${RED}Error: --threshold requires a numeric argument${NC}" >&2
                    exit 1
                fi
                THRESHOLD="$2"
                if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]] || [[ "$THRESHOLD" -gt 100 ]]; then
                    echo -e "${RED}Error: --threshold must be 0-100${NC}" >&2
                    exit 1
                fi
                shift 2
                ;;
            --dir)
                if [[ -z "${2:-}" ]]; then
                    echo -e "${RED}Error: --dir requires a path argument${NC}" >&2
                    exit 1
                fi
                SCAN_DIR="$2"
                shift 2
                ;;
            -*)
                echo -e "${RED}Unknown option: $1${NC}" >&2
                echo "Run with --help for usage information." >&2
                exit 1
                ;;
            *)
                FILES+=("$1")
                shift
                ;;
        esac
    done

    if [[ -n "$SCAN_DIR" ]]; then
        if [[ ! -d "$SCAN_DIR" ]]; then
            echo -e "${RED}Error: Directory not found: $SCAN_DIR${NC}" >&2
            exit 1
        fi
        while IFS= read -r -d '' f; do
            FILES+=("$f")
        done < <(find "$SCAN_DIR" -name "*.crux.md" -type f -print0 2>/dev/null | sort -z)
    fi

    if [[ ${#FILES[@]} -lt 2 ]]; then
        echo -e "${RED}Error: At least 2 CRUX files required for concordance analysis${NC}" >&2
        echo "Run with --help for usage information." >&2
        exit 1
    fi

    for f in "${FILES[@]}"; do
        if [[ ! -f "$f" ]]; then
            echo -e "${RED}Error: File not found: $f${NC}" >&2
            exit 1
        fi
    done
}

# Extract semantic entities from a CRUX file
# Parses standard block identifiers and their named sub-entities
extract_entities() {
    local file="$1"
    local entities=()

    local content
    content=$(cat "$file")

    local in_crux=false
    while IFS= read -r line; do
        if [[ "$line" == *"⟦CRUX:"* ]]; then
            in_crux=true
            local source_ref
            source_ref=$(echo "$line" | sed -n 's/.*⟦CRUX:\([^;⟧ ]*\).*/\1/p')
            if [[ -n "$source_ref" ]]; then
                entities+=("SOURCE:$source_ref")
            fi
            continue
        fi
        if [[ "$line" == *"⟧"* ]]; then
            in_crux=false
            continue
        fi

        if $in_crux; then
            # Extract block-level entities: Ρ{...}, E{...}, E.name{...}, etc.
            local block_markers="Ρ|E|Λ|Π|Κ|R|P|Γ|M|Φ|Ω"
            while IFS= read -r match; do
                if [[ -n "$match" ]]; then
                    local block_type block_name
                    block_type="${match%%.*}"
                    block_name=$(echo "$match" | sed -n 's/[^.]*\.\([^{]*\).*/\1/p')
                    if [[ -n "$block_name" ]]; then
                        entities+=("${block_type}.${block_name}")
                    fi
                fi
            done < <(echo "$line" | grep -oE "(${block_markers})\.[a-zA-Z_][a-zA-Z0-9_]*" 2>/dev/null || true)

            # Extract key=value identifiers inside blocks
            while IFS= read -r kv; do
                if [[ -n "$kv" ]]; then
                    local key
                    key=$(echo "$kv" | cut -d= -f1 | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
                    if [[ -n "$key" && ${#key} -gt 1 && "$key" != *"{"* && "$key" != *"}"* ]]; then
                        entities+=("$key")
                    fi
                fi
            done < <(echo "$line" | grep -oE '[a-zA-Z_][a-zA-Z0-9_]*=[^;}\]]+' 2>/dev/null || true)

            # Extract entity names from E.name patterns in content
            while IFS= read -r ent; do
                if [[ -n "$ent" ]]; then
                    entities+=("$ent")
                fi
            done < <(echo "$line" | grep -oE '[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*' 2>/dev/null || true)

            # Extract standalone identifiers in list contexts [a,b,c]
            if [[ "$line" == *"["*"]"* ]]; then
                local list_content
                list_content=$(echo "$line" | grep -oE '\[[^]]+\]' 2>/dev/null | head -1 || true)
                if [[ -n "$list_content" ]]; then
                    list_content="${list_content#[}"
                    list_content="${list_content%]}"
                    IFS=',' read -ra items <<< "$list_content"
                    for item in "${items[@]}"; do
                        item=$(echo "$item" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
                        if [[ -n "$item" && ${#item} -gt 1 && "$item" != *"="* ]]; then
                            entities+=("$item")
                        fi
                    done
                fi
            fi
        fi
    done <<< "$content"

    # Normalize: lowercase, deduplicate, sort
    local normalized=()
    for e in "${entities[@]}"; do
        local lower
        lower=$(echo "$e" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]]*//g')
        if [[ -n "$lower" ]]; then
            normalized+=("$lower")
        fi
    done

    printf '%s\n' "${normalized[@]}" | sort -u
}

# Calculate Jaccard similarity between two entity sets
jaccard_similarity() {
    local file1="$1"
    local file2="$2"

    local shared=0
    local total_unique=0

    local all_entities
    all_entities=$(sort -u <(cat "$file1") <(cat "$file2"))
    total_unique=$(echo "$all_entities" | grep -c . || true)

    if [[ "$total_unique" -eq 0 ]]; then
        echo "0"
        return
    fi

    shared=$(comm -12 <(sort "$file1") <(sort "$file2") | grep -c . || true)

    if command -v bc &> /dev/null; then
        echo "$shared $total_unique" | awk '{printf "%.0f", ($1/$2)*100}'
    else
        echo $(( (shared * 100) / total_unique ))
    fi
}

# Generate pairwise concordance report
generate_report() {
    local -a entity_files=()
    local -a file_entity_counts=()

    for f in "${FILES[@]}"; do
        local tmp_entities
        tmp_entities=$(mktemp)
        extract_entities "$f" > "$tmp_entities"
        entity_files+=("$tmp_entities")
        local count
        count=$(wc -l < "$tmp_entities" | tr -d ' ')
        file_entity_counts+=("$count")
    done

    local num_files=${#FILES[@]}
    local total_pairs=$(( num_files * (num_files - 1) / 2 ))
    local score_sum=0
    local min_score=100
    local below_threshold=false
    local pair_results=()

    for (( i=0; i<num_files; i++ )); do
        for (( j=i+1; j<num_files; j++ )); do
            local score
            score=$(jaccard_similarity "${entity_files[$i]}" "${entity_files[$j]}")
            score_sum=$((score_sum + score))

            if [[ "$score" -lt "$min_score" ]]; then
                min_score=$score
            fi
            if [[ "$score" -lt "$THRESHOLD" ]]; then
                below_threshold=true
            fi

            local shared_entities only_a only_b
            shared_entities=$(comm -12 <(sort "${entity_files[$i]}") <(sort "${entity_files[$j]}") | wc -l | tr -d ' ')
            only_a=$(comm -23 <(sort "${entity_files[$i]}") <(sort "${entity_files[$j]}") | wc -l | tr -d ' ')
            only_b=$(comm -13 <(sort "${entity_files[$i]}") <(sort "${entity_files[$j]}") | wc -l | tr -d ' ')

            pair_results+=("${i}:${j}:${score}:${shared_entities}:${only_a}:${only_b}")
        done
    done

    local avg_score
    if [[ "$total_pairs" -gt 0 ]]; then
        avg_score=$((score_sum / total_pairs))
    else
        avg_score=0
    fi

    if $OUTPUT_JSON; then
        output_json "${entity_files[@]}" -- "${file_entity_counts[@]}" -- "${pair_results[@]}" -- "$avg_score" "$min_score"
    else
        output_text "${entity_files[@]}" -- "${file_entity_counts[@]}" -- "${pair_results[@]}" -- "$avg_score" "$min_score"
    fi

    for tmp in "${entity_files[@]}"; do
        rm -f "$tmp"
    done

    if $below_threshold; then
        return 2
    fi
    return 0
}

output_text() {
    local -a entity_files=()
    local -a counts=()
    local -a pairs=()
    local phase="entity_files"

    for arg in "$@"; do
        if [[ "$arg" == "--" ]]; then
            if [[ "$phase" == "entity_files" ]]; then
                phase="counts"
            elif [[ "$phase" == "counts" ]]; then
                phase="pairs"
            elif [[ "$phase" == "pairs" ]]; then
                phase="summary"
            fi
            continue
        fi
        case $phase in
            entity_files) entity_files+=("$arg") ;;
            counts) counts+=("$arg") ;;
            pairs) pairs+=("$arg") ;;
            summary)
                if [[ -z "${avg_score:-}" ]]; then
                    avg_score="$arg"
                else
                    min_score="$arg"
                fi
                ;;
        esac
    done

    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║           CRUX Concordance Analysis Report                  ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    echo -e "${BOLD}Files Analyzed:${NC}"
    for (( i=0; i<${#FILES[@]}; i++ )); do
        local basename
        basename=$(basename "${FILES[$i]}")
        echo -e "  ${CYAN}[$((i+1))]${NC} ${basename} ${DIM}(${counts[$i]} entities)${NC}"
    done
    echo ""

    echo -e "${BOLD}Pairwise Concordance:${NC}"
    echo -e "  ${DIM}────────────────────────────────────────────${NC}"
    for pair in "${pairs[@]}"; do
        IFS=':' read -r idx_a idx_b score shared only_a only_b <<< "$pair"
        local name_a name_b color
        name_a=$(basename "${FILES[$idx_a]}")
        name_b=$(basename "${FILES[$idx_b]}")

        if [[ "$score" -ge 80 ]]; then
            color="$GREEN"
        elif [[ "$score" -ge "$THRESHOLD" ]]; then
            color="$YELLOW"
        else
            color="$RED"
        fi

        echo -e "  ${name_a} ↔ ${name_b}"
        echo -e "    Score: ${color}${score}%${NC}  │  Shared: ${shared}  │  Only-A: ${only_a}  │  Only-B: ${only_b}"

        if [[ "$score" -lt "$THRESHOLD" ]]; then
            echo ""
            echo -e "    ${RED}⚠ DRIFT DETECTED${NC} — below threshold of ${THRESHOLD}%"

            local drift_a drift_b
            drift_a=$(comm -23 <(sort "${entity_files[$idx_a]}") <(sort "${entity_files[$idx_b]}") | head -5)
            drift_b=$(comm -13 <(sort "${entity_files[$idx_a]}") <(sort "${entity_files[$idx_b]}") | head -5)
            if [[ -n "$drift_a" ]]; then
                echo -e "    ${DIM}Only in ${name_a}:${NC}"
                while IFS= read -r e; do
                    echo -e "      - $e"
                done <<< "$drift_a"
            fi
            if [[ -n "$drift_b" ]]; then
                echo -e "    ${DIM}Only in ${name_b}:${NC}"
                while IFS= read -r e; do
                    echo -e "      - $e"
                done <<< "$drift_b"
            fi
        fi
        echo -e "  ${DIM}────────────────────────────────────────────${NC}"
    done
    echo ""

    local summary_color
    if [[ "$avg_score" -ge 80 ]]; then
        summary_color="$GREEN"
    elif [[ "$avg_score" -ge "$THRESHOLD" ]]; then
        summary_color="$YELLOW"
    else
        summary_color="$RED"
    fi

    echo -e "${BOLD}Summary:${NC}"
    echo -e "  Average Concordance: ${summary_color}${avg_score}%${NC}"
    echo -e "  Minimum Concordance: ${summary_color}${min_score}%${NC}"
    echo -e "  Threshold:           ${THRESHOLD}%"
    echo -e "  Files Compared:      ${#FILES[@]}"
    echo -e "  Pairs Evaluated:     ${#pairs[@]}"
    echo ""

    if [[ "$min_score" -lt "$THRESHOLD" ]]; then
        echo -e "${RED}✗ Semantic drift detected — concordance below threshold${NC}"
    else
        echo -e "${GREEN}✓ All concordance scores at or above threshold${NC}"
    fi
    echo ""
}

output_json() {
    local -a entity_files=()
    local -a counts=()
    local -a pairs=()
    local phase="entity_files"

    for arg in "$@"; do
        if [[ "$arg" == "--" ]]; then
            if [[ "$phase" == "entity_files" ]]; then
                phase="counts"
            elif [[ "$phase" == "counts" ]]; then
                phase="pairs"
            elif [[ "$phase" == "pairs" ]]; then
                phase="summary"
            fi
            continue
        fi
        case $phase in
            entity_files) entity_files+=("$arg") ;;
            counts) counts+=("$arg") ;;
            pairs) pairs+=("$arg") ;;
            summary)
                if [[ -z "${avg_score:-}" ]]; then
                    avg_score="$arg"
                else
                    min_score="$arg"
                fi
                ;;
        esac
    done

    echo "{"
    echo "  \"threshold\": $THRESHOLD,"
    echo "  \"averageConcordance\": ${avg_score},"
    echo "  \"minimumConcordance\": ${min_score},"
    echo "  \"filesAnalyzed\": ${#FILES[@]},"
    echo "  \"files\": ["

    for (( i=0; i<${#FILES[@]}; i++ )); do
        local comma=""
        [[ $i -lt $(( ${#FILES[@]} - 1 )) ]] && comma=","
        echo "    {\"path\": \"${FILES[$i]}\", \"entities\": ${counts[$i]}}${comma}"
    done

    echo "  ],"
    echo "  \"pairs\": ["

    for (( p=0; p<${#pairs[@]}; p++ )); do
        IFS=':' read -r idx_a idx_b score shared only_a only_b <<< "${pairs[$p]}"
        local comma=""
        [[ $p -lt $(( ${#pairs[@]} - 1 )) ]] && comma=","

        local drift_items_a drift_items_b
        drift_items_a=$(comm -23 <(sort "${entity_files[$idx_a]}") <(sort "${entity_files[$idx_b]}") | head -10 | while IFS= read -r e; do printf '"%s",' "$e"; done | sed 's/,$//')
        drift_items_b=$(comm -13 <(sort "${entity_files[$idx_a]}") <(sort "${entity_files[$idx_b]}") | head -10 | while IFS= read -r e; do printf '"%s",' "$e"; done | sed 's/,$//')

        echo "    {"
        echo "      \"fileA\": \"${FILES[$idx_a]}\","
        echo "      \"fileB\": \"${FILES[$idx_b]}\","
        echo "      \"concordance\": $score,"
        echo "      \"shared\": $shared,"
        echo "      \"onlyInA\": $only_a,"
        echo "      \"onlyInB\": $only_b,"
        echo "      \"driftEntitiesA\": [${drift_items_a}],"
        echo "      \"driftEntitiesB\": [${drift_items_b}]"
        echo "    }${comma}"
    done

    echo "  ],"

    if [[ "$min_score" -lt "$THRESHOLD" ]]; then
        echo "  \"status\": \"drift_detected\""
    else
        echo "  \"status\": \"concordant\""
    fi

    echo "}"
}

main() {
    parse_args "$@"
    generate_report
}

main "$@"
