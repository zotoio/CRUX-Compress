#!/bin/bash
# Run all tests (shellcheck + bats + optional crux-test)
# Usage: ./scripts/test.sh [--crux-test]
#
# Options:
#   --crux-test    Also run /crux-test via cursor-agent (requires cursor-agent CLI)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
RUN_CRUX_TEST=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --crux-test)
            RUN_CRUX_TEST=true
            shift
            ;;
        --help|-h)
            echo "Usage: ./scripts/test.sh [--crux-test]"
            echo ""
            echo "Options:"
            echo "  --crux-test    Also run /crux-test via cursor-agent (requires cursor-agent CLI)"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

cd "$PROJECT_ROOT"

echo "=== Running shellcheck ==="
echo ""
./scripts/shellcheck.sh

echo ""
echo "=== Running bats tests ==="
echo ""
bats tests/*.bats

# Optionally run crux-test via cursor-agent
if [[ "$RUN_CRUX_TEST" == "true" ]]; then
    echo ""
    echo "=== Running /crux-test via cursor-agent ==="
    echo ""
    
    if ! command -v cursor-agent &> /dev/null; then
        echo -e "${YELLOW}Warning: cursor-agent not found, skipping crux-test${NC}"
    else
        cursor-agent --model opus-4.5-thinking --print --output-format stream-json --workspace "$PROJECT_ROOT" "/crux-test"
    fi
fi

echo ""
echo -e "${GREEN}✓ All tests passed${NC}"
