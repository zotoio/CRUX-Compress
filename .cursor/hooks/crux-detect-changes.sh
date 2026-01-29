#!/bin/bash
# Detect source file changes that need CRUX compression
# Triggered by: afterFileEdit hook
#
# This hook queues modified source files (with crux: true) for compression.
# Tracks pending files in .crux/pending-compression.json
# Only operates on .md files under .cursor/rules/
# See: https://github.com/zotoio/CRUX-Compress

pending_file=".crux/pending-compression.json"

# Function to check if a file is valid for CRUX compression
is_valid_crux_file() {
    local file="$1"
    # Must be under .cursor/rules/, end with .md, not be .crux.mdc or .crux.md
    [[ "$file" == .cursor/rules/*.md ]] && \
    [[ "$file" != *.crux.mdc ]] && \
    [[ "$file" != *.crux.md ]] && \
    [[ -f "$file" ]] && \
    head -20 "$file" 2>/dev/null | grep -q "crux:[[:space:]]*true"
}

# Function to normalize path to repo-relative
normalize_path() {
    local path="$1"
    # Remove leading ./
    path="${path#./}"
    # Convert absolute path to repo-relative by removing repo root prefix
    local repo_root
    repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"
    if [[ -n "$repo_root" && "$path" == "$repo_root"/* ]]; then
        path="${path#"$repo_root"/}"
    fi
    echo "$path"
}

# Function to clean up invalid entries from pending file
cleanup_invalid_entries() {
    if [[ ! -f "$pending_file" ]]; then
        return
    fi
    
    local valid_files=()
    while IFS= read -r file; do
        if [[ -n "$file" ]] && is_valid_crux_file "$file"; then
            valid_files+=("$file")
        fi
    done < <(jq -r '.files[]?' "$pending_file" 2>/dev/null)
    
    # Rebuild the pending file with only valid entries
    local files_json
    files_json=$(printf '%s\n' "${valid_files[@]}" | jq -R . | jq -s .)
    echo "{\"files\": $files_json, \"updated\": \"$(date -Iseconds)\"}" > "$pending_file"
}

# Read input JSON from stdin (Cursor sends edit details)
read -r input

# Extract and normalize file path from the input
raw_path=$(echo "$input" | jq -r '.file_path')
file_path=$(normalize_path "$raw_path")

# Debug logging (optional - comment out in production)
# echo "$(date '+%Y-%m-%d %H:%M:%S') - afterFileEdit: $file_path" >> /tmp/xfi-crux-hook-debug.log

# Clean up any invalid entries first
cleanup_invalid_entries

# Only process valid .cursor/rules/*.md files with crux: true
if is_valid_crux_file "$file_path"; then
    mkdir -p .crux
    
    # Ensure file always exists with valid structure
    if [[ ! -f "$pending_file" ]] || ! jq -e '.files' "$pending_file" > /dev/null 2>&1; then
        echo '{"files": [], "updated": ""}' > "$pending_file"
    fi
    
    # Add entry to array if not already present
    existing=$(cat "$pending_file")
    if ! echo "$existing" | jq -e ".files | index(\"$file_path\")" > /dev/null 2>&1; then
        echo "$existing" | jq ".files += [\"$file_path\"] | .updated = \"$(date -Iseconds)\"" > "$pending_file"
    fi
    
    # Debug logging (optional)
    # echo "$(date '+%Y-%m-%d %H:%M:%S') - Queued for CRUX compression: $file_path" >> /tmp/xfi-crux-hook-debug.log
fi
