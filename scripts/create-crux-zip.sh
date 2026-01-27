#!/bin/bash
# Create CRUX distribution zip file
# Usage: ./scripts/create-crux-zip.sh [output-dir]
#
# This script packages all CRUX-related files for distribution.
# Output: CRUX-Compress-v{version}.zip (version read from VERSION)

set -e

# Get the directory where this script is located (works regardless of where it's called from)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# Convert output dir to absolute path (important: script cd's later, relative paths would break)
OUTPUT_DIR="$(cd "${1:-.}" && pwd)"

# Read version from VERSION file
VERSION=$(tr -d '[:space:]' < "$PROJECT_ROOT/VERSION")
ZIP_NAME="CRUX-Compress-v${VERSION}.zip"

cd "$PROJECT_ROOT"

echo "Creating CRUX distribution package v${VERSION}..."
echo "Output: $OUTPUT_DIR/$ZIP_NAME"

# Create temp directory for staging
STAGING_DIR=$(mktemp -d)
trap 'rm -rf "$STAGING_DIR"' EXIT

# Create directory structure
mkdir -p "$STAGING_DIR/.cursor/agents"
mkdir -p "$STAGING_DIR/.cursor/commands"
mkdir -p "$STAGING_DIR/.cursor/hooks"
mkdir -p "$STAGING_DIR/.cursor/rules"
mkdir -p "$STAGING_DIR/.cursor/skills/CRUX-Utils/scripts"

# Copy core files
echo "Copying core files..."
cp CRUX.md "$STAGING_DIR/"
cp VERSION "$STAGING_DIR/"

# Extract CRUX block from AGENTS.md into AGENTS.crux.md
# This contains only the <CRUX...> to </CRUX> block for merging during install
echo "Extracting CRUX block from AGENTS.md..."
sed -n '/<CRUX/,/<\/CRUX>/p' AGENTS.md > "$STAGING_DIR/AGENTS.crux.md"

if [[ ! -s "$STAGING_DIR/AGENTS.crux.md" ]]; then
    echo "ERROR: Could not extract CRUX block from AGENTS.md"
    exit 1
fi

# Copy Cursor integration files
echo "Copying Cursor integration files..."
cp .cursor/hooks.json "$STAGING_DIR/.cursor/"

# Copy agent
cp .cursor/agents/crux-cursor-rule-manager.md "$STAGING_DIR/.cursor/agents/"

# Copy command
cp .cursor/commands/crux-compress.md "$STAGING_DIR/.cursor/commands/"

# Copy hook
cp .cursor/hooks/detect-crux-changes.sh "$STAGING_DIR/.cursor/hooks/"

# Copy always-applied rule
cp .cursor/rules/_CRUX-RULE.mdc "$STAGING_DIR/.cursor/rules/"

# Copy CRUX-Utils skill
echo "Copying CRUX-Utils skill..."
cp .cursor/skills/CRUX-Utils/SKILL.md "$STAGING_DIR/.cursor/skills/CRUX-Utils/"
cp .cursor/skills/CRUX-Utils/scripts/crux-utils.sh "$STAGING_DIR/.cursor/skills/CRUX-Utils/scripts/"

# Create the zip
echo "Creating zip archive..."
cd "$STAGING_DIR"
zip -r "$OUTPUT_DIR/$ZIP_NAME" . -x "*.DS_Store" -x "*__MACOSX*"

echo ""
echo "Done! Created: $OUTPUT_DIR/$ZIP_NAME"
echo ""
echo "Contents:"
unzip -l "$OUTPUT_DIR/$ZIP_NAME"
