#!/usr/bin/env bash
# Renders walkthrough.mp4 from titled color slides (ffmpeg + DejaVu).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT="walkthrough.mp4"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# slide <file_base> <seconds> <title> <line1> [line2] [line3] ...
slide() {
  local base="$1"
  local dur="$2"
  shift 2
  local title="$1"
  shift
  local vf="drawtext=fontfile=${FONT_B}:text='${title}':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=200"
  local y=280
  local line
  for line in "$@"; do
    vf+=",drawtext=fontfile=${FONT}:text='${line}':fontsize=26:fontcolor=0xaeb8c9:x=(w-text_w)/2:y=${y}"
    y=$((y + 44))
  done
  ffmpeg -y -hide_banner -loglevel error -f lavfi -i "color=c=0x0c0f14:s=1280x720:d=${dur}:r=30" \
    -vf "$vf" -c:v libx264 -pix_fmt yuv420p "$TMP/${base}.mp4"
}

slide s1 5 "Context word-frequency" \
  "Reproducible report for project-local agent context" \
  "Rules + AGENTS.md + session snapshot (see WALKTHROUGH.md)"

slide s2 5 "Corpus" \
  "Five always-applied .cursor/rules/*.crux.mdc files" \
  "Root AGENTS.md" \
  "Verbatim session blocks (user rules, git, cloud task excerpt)"

slide s3 5 "Tokenization" \
  "ASCII alphanumerics + underscores, lowercased" \
  "Greek letters kept as separate CRUX tokens" \
  "Excludes full generic tool schema text"

slide s4 6 "Results" \
  "2570 total tokens, 864 unique words" \
  "Top token crux with 101 occurrences" \
  "Interactive HTML — SVG bars plus WebGPU harmonics"

slide s5 5 "Deliverables" \
  "WALKTHROUGH.md  report.html  walkthrough.mp4" \
  "Regenerate via generate_data.py then build_report.py"

{
  printf "file '%s'\n" "$TMP/s1.mp4"
  printf "file '%s'\n" "$TMP/s2.mp4"
  printf "file '%s'\n" "$TMP/s3.mp4"
  printf "file '%s'\n" "$TMP/s4.mp4"
  printf "file '%s'\n" "$TMP/s5.mp4"
} > "$TMP/list.txt"

ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT"
echo "Wrote $DIR/$OUT"
