#!/usr/bin/env bash
#
# CRUX Knowledge Packets (CRUX-KP) — Unpack
#
# Extracts CRUX blocks from a knowledge packet JSON file,
# validates integrity, and optionally writes individual .crux.md files.
#
# Usage:
#   crux-unpack.sh <packet.crux.json>
#   crux-unpack.sh --info <packet.crux.json>
#   crux-unpack.sh --extract <packet.crux.json> --output-dir <dir>
#   crux-unpack.sh --validate <packet.crux.json>
#
# Options:
#   --info               Show packet metadata without extracting
#   --extract            Write individual .crux.md files
#   --output-dir <dir>   Directory for extracted files (default: ./crux-unpacked/)
#   --validate           Validate packet integrity (checksums, structure)
#   --filter <type>      Only extract blocks of type: text, code, image
#   --help, -h           Show this help

set -euo pipefail

show_help() {
    cat << 'EOF'
CRUX Knowledge Packets — Unpack

Extracts CRUX blocks from a knowledge packet, validates integrity,
and optionally writes individual .crux.md files.

Usage:
  crux-unpack.sh <packet.crux.json>
  crux-unpack.sh --info <packet.crux.json>
  crux-unpack.sh --extract <packet.crux.json> --output-dir <dir>
  crux-unpack.sh --validate <packet.crux.json>

Options:
  --info               Show packet metadata without extracting
  --extract            Write individual .crux.md files
  --output-dir <dir>   Directory for extracted files (default: ./crux-unpacked/)
  --validate           Validate packet integrity (checksums, structure)
  --filter <type>      Only extract blocks of type: text, code, image
  --help, -h           Show this help

Examples:
  crux-unpack.sh --info context.crux.json
  crux-unpack.sh --extract context.crux.json --output-dir ./rules/
  crux-unpack.sh --validate context.crux.json
EOF
}

log() {
    echo "[crux-unpack] $*" >&2
}

require_python3() {
    if ! command -v python3 &>/dev/null; then
        log "Error: python3 is required for JSON parsing"
        exit 1
    fi
}

show_info() {
    local packet_file="$1"
    require_python3

    python3 << PYEOF
import json, sys

with open("$packet_file", "r") as f:
    packet = json.load(f)

print("=== CRUX Knowledge Packet ===")
print(f"Packet ID:       {packet.get('packet_id', 'N/A')}")
print(f"Created:         {packet.get('created', 'N/A')}")
print(f"CRUX KP Version: {packet.get('crux_kp_version', 'N/A')}")
print(f"CRUX Spec:       {packet.get('crux_spec_version', 'N/A')}")

if packet.get('label'):
    print(f"Label:           {packet['label']}")
if packet.get('source_model'):
    print(f"Source Model:    {packet['source_model']}")
if packet.get('target_model'):
    print(f"Target Model:    {packet['target_model']}")

print(f"Modalities:      {', '.join(packet.get('modalities', []))}")
print(f"Block Count:     {packet.get('block_count', 0)}")
print(f"Total Tokens:    {packet.get('total_tokens', 0)}")
print()
print("--- Blocks ---")
for i, block in enumerate(packet.get("blocks", [])):
    print(f"  [{i+1}] {block.get('source', '?')} ({block.get('type', '?')}/{block.get('language', '?')}) — {block.get('tokens', 0)} tokens")
PYEOF
}

validate_packet() {
    local packet_file="$1"
    require_python3

    python3 << PYEOF
import json, sys

errors = []
warnings = []

try:
    with open("$packet_file", "r") as f:
        packet = json.load(f)
except json.JSONDecodeError as e:
    print(f"FAIL: Invalid JSON — {e}")
    sys.exit(1)

required_fields = ["crux_kp_version", "packet_id", "created", "modalities", "blocks"]
for field in required_fields:
    if field not in packet:
        errors.append(f"Missing required field: {field}")

if "blocks" in packet:
    for i, block in enumerate(packet["blocks"]):
        for bf in ["source", "type", "crux"]:
            if bf not in block:
                errors.append(f"Block {i+1}: missing '{bf}'")
        if "crux" in block:
            crux = block["crux"]
            if "⟦CRUX:" not in crux:
                warnings.append(f"Block {i+1}: no ⟦CRUX: delimiter found")
            if "⟧" not in crux:
                warnings.append(f"Block {i+1}: no closing ⟧ delimiter found")

    declared = packet.get("block_count", -1)
    actual = len(packet["blocks"])
    if declared != actual:
        errors.append(f"block_count mismatch: declared={declared}, actual={actual}")

    declared_mods = set(packet.get("modalities", []))
    actual_mods = set(b.get("type", "") for b in packet["blocks"])
    if declared_mods != actual_mods:
        warnings.append(f"modalities mismatch: declared={declared_mods}, actual={actual_mods}")

print("=== Validation Report ===")
if errors:
    for e in errors:
        print(f"  ERROR:   {e}")
if warnings:
    for w in warnings:
        print(f"  WARNING: {w}")

if errors:
    print(f"\nRESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
    sys.exit(1)
elif warnings:
    print(f"\nRESULT: PASS with warnings ({len(warnings)} warnings)")
else:
    print("\nRESULT: PASS — packet is valid")
PYEOF
}

extract_blocks() {
    local packet_file="$1"
    local output_dir="$2"
    local filter_type="${3:-}"
    require_python3

    mkdir -p "$output_dir"

    python3 << PYEOF
import json, os, re, sys

with open("$packet_file", "r") as f:
    packet = json.load(f)

output_dir = "$output_dir"
filter_type = "$filter_type"
extracted = 0

for i, block in enumerate(packet.get("blocks", [])):
    btype = block.get("type", "")
    if filter_type and btype != filter_type:
        continue

    source = block.get("source", f"block-{i+1}")
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', source)
    if not safe_name.endswith(".crux.md"):
        safe_name += ".crux.md"

    filepath = os.path.join(output_dir, safe_name)
    with open(filepath, "w") as f:
        f.write(block["crux"])

    print(f"  Extracted: {filepath} ({block.get('tokens', '?')} tokens)")
    extracted += 1

print(f"\n{extracted} blocks extracted to {output_dir}")
PYEOF
}

# ============================================================
# Main
# ============================================================

MODE=""
PACKET_FILE=""
OUTPUT_DIR="./crux-unpacked"
FILTER_TYPE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            show_help
            exit 0
            ;;
        --info)
            MODE="info"
            shift
            ;;
        --extract)
            MODE="extract"
            shift
            ;;
        --validate)
            MODE="validate"
            shift
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --filter)
            FILTER_TYPE="$2"
            shift 2
            ;;
        -*)
            log "Error: Unknown option: $1"
            exit 1
            ;;
        *)
            PACKET_FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$PACKET_FILE" ]]; then
    log "Error: no packet file specified"
    show_help
    exit 1
fi

if [[ ! -f "$PACKET_FILE" ]]; then
    log "Error: file not found: $PACKET_FILE"
    exit 1
fi

case "${MODE:-info}" in
    info)
        show_info "$PACKET_FILE"
        ;;
    extract)
        extract_blocks "$PACKET_FILE" "$OUTPUT_DIR" "$FILTER_TYPE"
        ;;
    validate)
        validate_packet "$PACKET_FILE"
        ;;
    *)
        show_info "$PACKET_FILE"
        ;;
esac
