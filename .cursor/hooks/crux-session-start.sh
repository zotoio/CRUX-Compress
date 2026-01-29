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

# Check if there are pending files from previous sessions
if [[ -f "$pending_file" ]]; then
    files=$(jq -r '.files[]?' "$pending_file" 2>/dev/null)
    
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
