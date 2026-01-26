#!/bin/bash
# Detect source file changes that need CRUX compression
# Triggered by: afterFileEdit hook
#
# This hook queues modified source files (with crux: true) for compression.
# The sessionStart hook will inject context to trigger /crux-compress.

# Read input JSON from stdin (Cursor sends edit details)
read -r input

# Extract file path from the input
file_path=$(echo "$input" | jq -r '.file_path')

# Debug logging (optional - comment out in production)
# echo "$(date '+%Y-%m-%d %H:%M:%S') - afterFileEdit: $file_path" >> /tmp/xfi-crux-hook-debug.log

# Only process .cursor/rules/*.md files (not .crux.mdc outputs)
if [[ "$file_path" == .cursor/rules/*.md ]] && [[ "$file_path" != *.crux.mdc ]]; then
    # Check if file has crux: true in frontmatter
    if head -20 "$file_path" 2>/dev/null | grep -q "crux:[[:space:]]*true"; then
        # Queue for compression (avoid duplicates)
        pending_file=".cursor/hooks/pending-crux-compress.json"
        mkdir -p .cursor/hooks
        
        # Initialize or update pending list
        if [[ -f "$pending_file" ]]; then
            existing=$(cat "$pending_file")
            # Add if not already present
            if ! echo "$existing" | jq -e ".files | index(\"$file_path\")" > /dev/null 2>&1; then
                echo "$existing" | jq ".files += [\"$file_path\"] | .updated = \"$(date -Iseconds)\"" > "$pending_file"
            fi
        else
            echo "{\"files\": [\"$file_path\"], \"updated\": \"$(date -Iseconds)\"}" > "$pending_file"
        fi
        
        # Debug logging (optional)
        # echo "$(date '+%Y-%m-%d %H:%M:%S') - Queued for CRUX compression: $file_path" >> /tmp/xfi-crux-hook-debug.log
    fi
fi
