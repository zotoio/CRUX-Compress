#!/bin/bash
# Display pending CRUX compressions at session start
# Triggered by: sessionStart hook
#
# Checks .crux/pending-compression.json for any files left pending
# from previous sessions and injects context for the agent.
# See: https://github.com/zotoio/CRUX-Compress

# Read input JSON from stdin (Cursor sends session details)
# shellcheck disable=SC2034 # input is consumed from stdin for Cursor hook interface
read -r input

pending_file=".crux/pending-compression.json"

# Function to check if CRUX output is already current for source
is_crux_output_current() {
    local source="$1"
    local crux_md=""
    local crux_mdc=""

    case "$source" in
        .cursor/rules/*.md)
            crux_md="${source%.md}.crux.md"
            crux_mdc="${source%.md}.crux.mdc"
            ;;
        *)
            return 1
            ;;
    esac

    [[ -f "$crux_md" && ! "$source" -nt "$crux_md" ]] && return 0
    [[ -f "$crux_mdc" && ! "$source" -nt "$crux_mdc" ]] && return 0
    return 1
}

# Check if there are pending files from previous sessions
if [[ -f "$pending_file" ]]; then
    raw_files=$(jq -r '.files[]?' "$pending_file" 2>/dev/null)

    # Filter out stale entries where CRUX output is already current.
    files=""
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        if [[ "$file" == .cursor/rules/*.md ]] && \
           [[ "$file" != *.crux.md ]] && \
           [[ "$file" != *.crux.mdc ]] && \
           [[ -f "$file" ]] && \
           ! is_crux_output_current "$file"; then
            if [[ -z "$files" ]]; then
                files="$file"
            else
                files="${files}"$'\n'"$file"
            fi
        fi
    done <<< "$raw_files"

    # Persist cleanup of stale/invalid pending entries.
    raw_count=$(printf '%s\n' "$raw_files" | sed '/^$/d' | wc -l | tr -d ' ')
    files_count=$(printf '%s\n' "$files" | sed '/^$/d' | wc -l | tr -d ' ')
    if [[ "$raw_count" -ne "$files_count" ]]; then
        if [[ -n "$files" ]]; then
            files_json=$(printf '%s\n' "$files" | jq -R . | jq -sc .)
            echo "{\"files\": $files_json, \"updated\": \"$(date -Iseconds)\"}" > "$pending_file"
        else
            echo '{"files": []}' > "$pending_file"
        fi
    fi
    
    if [[ -n "$files" ]]; then
        # Count pending files
        count=$(echo "$files" | wc -l | tr -d ' ')
        
        # Build the file list for context
        file_list=""
        while IFS= read -r file; do
            if [[ -n "$file" ]]; then
                file_list="${file_list}  - ${file}\n"
            fi
        done <<< "$files"
        
        # Output additional_context for the agent
        # This gets injected into the conversation's initial system context
        cat << EOF
{
  "additional_context": "[URGENT: CRUX Pending Compression]\n\n**IMPORTANT: Before responding to the user's message, you MUST first inform them:**\n\n${count} source file(s) need CRUX compression:\n${file_list}\nStart your response with: \"Note: There are pending CRUX compressions from a previous session. Would you like me to run /crux-compress for these files?\"\n\nThen proceed to answer their actual question."
}
EOF
    else
        # No pending files, output empty response
        echo "{}"
    fi
else
    # No pending file exists, output empty response
    echo "{}"
fi

exit 0
