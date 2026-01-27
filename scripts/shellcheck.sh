#!/bin/bash
# Run shellcheck on all shell scripts in the project
# Usage: ./scripts/shellcheck.sh [--fix]
#
# Options:
#   --fix    Show diff suggestions (requires shellcheck ≥0.8.0)
#
# Exit codes:
#   0 - All scripts pass
#   1 - Shellcheck found issues
#   2 - Shellcheck not installed

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if shellcheck is installed
if ! command -v shellcheck &> /dev/null; then
    echo -e "${RED}Error: shellcheck is not installed${NC}"
    echo ""
    echo "Install with:"
    echo "  macOS:        brew install shellcheck"
    echo "  Ubuntu/Debian: sudo apt install shellcheck"
    echo "  Fedora:       sudo dnf install ShellCheck"
    echo "  Arch:         sudo pacman -S shellcheck"
    echo "  Snap:         sudo snap install shellcheck"
    exit 2
fi

# Parse arguments
SHELLCHECK_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            SHELLCHECK_ARGS+=("--format=diff")
            shift
            ;;
        --help)
            echo "Usage: ./scripts/shellcheck.sh [--fix]"
            echo ""
            echo "Options:"
            echo "  --fix    Show diff suggestions"
            echo "  --help   Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Find all shell scripts
SCRIPTS=(
    "$PROJECT_ROOT/install.sh"
    "$PROJECT_ROOT/scripts/create-crux-zip.sh"
    "$PROJECT_ROOT/.cursor/skills/CRUX-Utils/scripts/crux-utils.sh"
    "$PROJECT_ROOT/.cursor/skills/token-count-estimator/scripts/count-tokens.sh"
    "$PROJECT_ROOT/.cursor/hooks/detect-crux-changes.sh"
    "$PROJECT_ROOT/tests/helpers.bash"
)

# Filter to only existing files
EXISTING_SCRIPTS=()
for script in "${SCRIPTS[@]}"; do
    if [[ -f "$script" ]]; then
        EXISTING_SCRIPTS+=("$script")
    fi
done

if [[ ${#EXISTING_SCRIPTS[@]} -eq 0 ]]; then
    echo -e "${YELLOW}No shell scripts found to check${NC}"
    exit 0
fi

echo "Running shellcheck on ${#EXISTING_SCRIPTS[@]} scripts..."
echo ""

# Run shellcheck
if shellcheck "${SHELLCHECK_ARGS[@]}" "${EXISTING_SCRIPTS[@]}"; then
    echo ""
    echo -e "${GREEN}✓ All scripts pass shellcheck${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Shellcheck found issues${NC}"
    exit 1
fi
