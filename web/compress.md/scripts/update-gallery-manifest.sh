#!/usr/bin/env bash
set -euo pipefail

ASSETS_DIR="$(cd "$(dirname "$0")/../assets" && pwd)"
MANIFEST="$ASSETS_DIR/manifest.json"
TYPES=("rules" "code" "images" "urls")

extract_frontmatter_value() {
  local file="$1" key="$2"
  sed -n '/^---$/,/^---$/p' "$file" 2>/dev/null \
    | grep -E "^${key}:" \
    | head -1 \
    | sed "s/^${key}:[[:space:]]*//" \
    | sed 's/^["'"'"']//;s/["'"'"']$//' \
    | sed 's/~//g'
}

extract_title() {
  local file="$1" fallback="$2"
  local title
  title=$(grep -m1 '^# ' "$file" 2>/dev/null | sed 's/^# //' || true)
  if [[ -n "$title" ]]; then
    echo "$title"
    return
  fi
  title=$(grep -m1 'Ρ{' "$file" 2>/dev/null \
    | sed 's/.*Ρ{//' | sed 's/[;}].*//' | sed 's/,.*//' | xargs || true)
  if [[ -n "$title" ]]; then
    local first_char rest
    first_char=$(echo "$title" | cut -c1 | tr '[:lower:]' '[:upper:]')
    rest=$(echo "$title" | cut -c2-)
    echo "${first_char}${rest}"
    return
  fi
  echo "$fallback"
}

get_source_ext() {
  local dir="$1" shortname="$2"
  local first_ext="" has_md=""
  for f in "$dir/${shortname}.source."*; do
    [[ -f "$f" ]] || continue
    local ext="${f##*.source.}"
    [[ -z "$first_ext" ]] && first_ext="$ext"
    [[ "$ext" == "md" ]] && has_md="true"
  done
  if [[ -n "$has_md" ]]; then
    echo "md"
  elif [[ -n "$first_ext" ]]; then
    echo "$first_ext"
  else
    echo ""
  fi
}

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\n/\\n/g; s/\r/\\r/g'
}

find_decompressed() {
  local dir="$1" shortname="$2"
  local results=()
  for f in "$dir/${shortname}.decompressed-"*; do
    [[ -f "$f" ]] || continue
    local basename model_and_ext ext model
    basename=$(basename "$f")
    model_and_ext="${basename#"${shortname}.decompressed-"}"
    ext="${model_and_ext##*.}"
    model="${model_and_ext%.*}"
    model=$(json_escape "$model")
    ext=$(json_escape "$ext")
    results+=("{\"model\":\"${model}\",\"ext\":\"${ext}\"}")
  done
  if [[ ${#results[@]} -eq 0 ]]; then
    echo "[]"
  else
    local joined
    joined=$(printf ",%s" "${results[@]}")
    echo "[${joined:1}]"
  fi
}

build_meta() {
  local file="$1" type="$2"
  local parts=()
  if [[ "$type" == "images" ]]; then
    local before_size after_size reduced
    before_size=$(extract_frontmatter_value "$file" "beforeSize")
    [[ -z "$before_size" ]] && before_size=$(extract_frontmatter_value "$file" "originalSize")
    after_size=$(extract_frontmatter_value "$file" "afterSize")
    reduced=$(extract_frontmatter_value "$file" "reducedBy")
    [[ -n "$before_size" ]] && parts+=("\"beforeSize\":\"$before_size\"")
    [[ -n "$after_size" ]] && parts+=("\"afterSize\":\"$after_size\"")
    [[ -n "$reduced" ]] && parts+=("\"reduction\":\"${reduced}\"")
  else
    local before_tokens after_tokens reduced decompressed_tokens
    before_tokens=$(extract_frontmatter_value "$file" "beforeTokens")
    after_tokens=$(extract_frontmatter_value "$file" "afterTokens")
    reduced=$(extract_frontmatter_value "$file" "reducedBy")
    decompressed_tokens=$(extract_frontmatter_value "$file" "decompressedTokens")
    [[ -n "$before_tokens" ]] && parts+=("\"sourceTokens\":\"~${before_tokens}\"")
    [[ -n "$after_tokens" ]] && parts+=("\"cruxTokens\":\"~${after_tokens}\"")
    [[ -n "$decompressed_tokens" ]] && parts+=("\"decompressedTokens\":\"~${decompressed_tokens}\"")
    [[ -n "$reduced" ]] && parts+=("\"reduction\":\"${reduced}\"")
  fi
  if [[ ${#parts[@]} -eq 0 ]]; then
    echo "{}"
  else
    local joined
    joined=$(printf ",%s" "${parts[@]}")
    echo "{${joined:1}}"
  fi
}

echo "Scanning asset directories..."

tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

echo "{" > "$tmpfile"

type_idx=0
for type in "${TYPES[@]}"; do
  type_dir="$ASSETS_DIR/$type"
  [[ -d "$type_dir" ]] || continue

  [[ $type_idx -gt 0 ]] && echo "," >> "$tmpfile"
  echo "  \"$type\": [" >> "$tmpfile"

  item_idx=0
  for crux_file in "$type_dir"/*.crux.md; do
    [[ -f "$crux_file" ]] || continue

    shortname=$(basename "$crux_file" .crux.md)
    shortname=$(json_escape "$shortname")
    source_ext=$(get_source_ext "$type_dir" "$shortname")
    source_ext=$(json_escape "$source_ext")
    has_source=$([[ -n "$source_ext" ]] && echo "true" || echo "false")
    title=$(extract_title "$crux_file" "$shortname")
    title=$(json_escape "$title")
    decompressed=$(find_decompressed "$type_dir" "$shortname")
    meta=$(build_meta "$crux_file" "$type")

    [[ $item_idx -gt 0 ]] && echo "," >> "$tmpfile"

    if [[ "$type" == "urls" ]]; then
      src_url=$(extract_frontmatter_value "$crux_file" "sourceUrl")
      src_url=$(json_escape "$src_url")
      has_screenshot=$([[ -f "$type_dir/${shortname}.screenshot.png" ]] && echo "true" || echo "false")
      has_html=$([[ -f "$type_dir/${shortname}.source.html" ]] && echo "true" || echo "false")
      cat >> "$tmpfile" <<ITEM
    {
      "name": "$shortname",
      "title": "$title",
      "sourceExt": "$source_ext",
      "hasSource": $has_source,
      "hasCrux": true,
      "decompressed": $decompressed,
      "meta": $meta,
      "sourceUrl": "$src_url",
      "hasScreenshot": $has_screenshot,
      "hasSourceHtml": $has_html
    }
ITEM
    else
      cat >> "$tmpfile" <<ITEM
    {
      "name": "$shortname",
      "title": "$title",
      "sourceExt": "$source_ext",
      "hasSource": $has_source,
      "hasCrux": true,
      "decompressed": $decompressed,
      "meta": $meta
    }
ITEM
    fi
    item_idx=$((item_idx + 1))
    echo "  [$type] $shortname -> $title"
  done

  echo "  ]" >> "$tmpfile"
  type_idx=$((type_idx + 1))
done

echo "}" >> "$tmpfile"
mv "$tmpfile" "$MANIFEST"
trap - EXIT

echo ""
echo "Manifest written to: $MANIFEST"
echo "Total items: $(grep -c '"name"' "$MANIFEST")"