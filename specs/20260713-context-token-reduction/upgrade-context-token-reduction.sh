#!/usr/bin/env bash
# upgrade-context-token-reduction.sh
#
# Idempotent upgrade script for the context-token-reduction spec.
# Run this against any pre-spec consumer install to bring it up to date.
#
# Usage:
#   bash upgrade-context-token-reduction.sh          # dry-run: prints planned actions, exits 0
#   bash upgrade-context-token-reduction.sh --yes    # apply: executes the actions
#
# Safe to re-run: every step guards itself before acting.
# Requires: bash >=4, python3, grep (for plain -R flag usage use grep directly)

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DRY_RUN=1
for arg in "$@"; do
  if [ "${arg}" = "--yes" ]; then DRY_RUN=0; fi
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log()    { echo "[upgrade] $*"; }
action() { echo "  [ACTION] $*"; }
warn()   { echo "  [WARN]   $*"; }
skip()   { echo "  [SKIP]   $*"; }

apply() {
  # apply <description> <command ...>
  local desc="$1"; shift
  if [ "${DRY_RUN}" -eq 1 ]; then
    action "DRY-RUN: ${desc}"
  else
    action "${desc}"
    "$@"
  fi
}

section() { echo; echo "=== $* ==="; }

# ---------------------------------------------------------------------------
# Dry-run banner
# ---------------------------------------------------------------------------
if [ "${DRY_RUN}" -eq 1 ]; then
  echo "========================================================"
  echo "  CRUX context-token-reduction upgrade — DRY RUN"
  echo "  Run with --yes to apply changes."
  echo "========================================================"
fi

cd "${REPO_ROOT}"

# ---------------------------------------------------------------------------
# Step 0: Precondition detection — memory-manager split (S05)
# ---------------------------------------------------------------------------
section "Step 0: Precondition detection"

NEEDS_SPLIT=0
if test -f ".cursor/agents/crux/crux-cursor-memory-manager.md" \
   && ! test -f ".cursor/agents/crux/crux-memory-dream.md"; then
  NEEDS_SPLIT=1
  log "Pre-upgrade install detected: monolithic umbrella present, thin agents absent."
  log "Steps 1–4 will run to complete the memory-manager split."
else
  log "Memory-manager split already applied (thin agents present). Skipping Steps 1–4."
fi

# ---------------------------------------------------------------------------
# Step 1: Copy the five thin agents + Canvas template (S05)
# Requires thin agents to be present in the repo tree (dist zip extracts them
# via install.py once scripts/create-crux-zip.py is updated — see D05 below).
# ---------------------------------------------------------------------------
if [ "${NEEDS_SPLIT}" -eq 1 ]; then
  section "Step 1: Copy thin agents + Canvas template"

  DIST_AGENTS_SRC=".cursor/agents"

  log "Note: this step copies thin agents from the local source tree."
  log "      On a consumer install, these files arrive via 'python3 install.py'"
  log "      once the dist zip includes them (awaiting user approval — see Step 2)."

  mkdir -p ".cursor/agents/crux/templates"

  for agent in crux-memory-dream crux-memory-rem crux-memory-recall crux-memory-remember crux-memory-forget; do
    dest=".cursor/agents/crux/${agent}.md"
    src="${DIST_AGENTS_SRC}/${agent}.md"
    if test -f "${dest}"; then
      skip "${dest} already exists"
    elif test -f "${src}"; then
      apply "copy ${src} → ${dest}" cp "${src}" "${dest}"
    else
      warn "${src} not found — dist zip may not yet include thin agents."
      warn "Re-run after updating scripts/create-crux-zip.py (see Step 2 note)."
    fi
  done

  CANVAS_SRC="${DIST_AGENTS_SRC}/templates/recall-canvas.tsx.md"
  CANVAS_DEST=".cursor/agents/crux/templates/recall-canvas.tsx.md"
  if test -f "${CANVAS_DEST}"; then
    skip "${CANVAS_DEST} already exists"
  elif test -f "${CANVAS_SRC}"; then
    apply "copy ${CANVAS_SRC} → ${CANVAS_DEST}" cp "${CANVAS_SRC}" "${CANVAS_DEST}"
  else
    warn "${CANVAS_SRC} not found — dist zip may not yet include the Canvas template."
  fi
fi

# ---------------------------------------------------------------------------
# Step 2: Dist-zip update pending — manual action required
# scripts/create-crux-zip.py was NOT modified by this spec.
# ---------------------------------------------------------------------------
section "Step 2: Dist-zip additions check"

DIST_SCRIPT="scripts/create-crux-zip.py"
EXPECTED_THIN_AGENT="crux-memory-dream.md"

if grep -q "${EXPECTED_THIN_AGENT}" "${DIST_SCRIPT}" 2>/dev/null; then
  log "scripts/create-crux-zip.py already includes thin agent entries."
else
  warn "scripts/create-crux-zip.py has NOT been updated with the new dist files."
  warn "The following paths must be added to SOURCE_DIST_FILES in create-crux-zip.py"
  warn "by the repository owner after reviewing the execution report:"
  warn ""
  warn "  (after .cursor/agents/crux-cursor-memory-manager.md)"
  warn "    \".cursor/agents/crux-memory-dream.md\","
  warn "    \".cursor/agents/crux-memory-rem.md\","
  warn "    \".cursor/agents/crux-memory-recall.md\","
  warn "    \".cursor/agents/crux-memory-remember.md\","
  warn "    \".cursor/agents/crux-memory-forget.md\","
  warn "    \".cursor/agents/templates/recall-canvas.tsx.md\","
  warn ""
  warn "  (in the commands templates section)"
  warn "    \".cursor/commands/templates/compress-prompts.md\","
  warn ""
  warn "  (SoT .source.mdx files — only if consumers need editable source)"
  warn "    \".cursor/commands/crux-compress.source.mdx\","
  warn "    \".cursor/commands/crux-meditate.source.mdx\","
  warn "    \".cursor/agents/crux-cursor-meditation-guide.source.mdx\","
  warn "    \".cursor/agents/crux-memory-dream.source.mdx\","
  warn "    \".cursor/agents/crux-memory-rem.source.mdx\","
  warn "    \".cursor/agents/crux-memory-recall.source.mdx\","
  warn "    \".cursor/agents/crux-memory-remember.source.mdx\","
  warn "    \".cursor/agents/crux-memory-forget.source.mdx\","
  warn ""
  warn "  (shared memory surface)"
  warn "    \".cursor/skills/_memory-shared.md\","
  warn ""
  warn "See specs/20260713-context-token-reduction/execution-report-context-token-reduction-20260713.md"
  warn "for the full diff and rationale."
fi

# ---------------------------------------------------------------------------
# Step 3: Warn about consumer-custom files still referencing the umbrella
# ---------------------------------------------------------------------------
section "Step 3: Custom-caller audit"

log "Scanning for files referencing crux-cursor-memory-manager outside the expected locations..."

custom_hits=$(grep -RIl --include='*.md' --include='*.mdc' --include='*.mdx' 'crux-cursor-memory-manager' .cursor/ 2>/dev/null \
  | grep -v 'crux-cursor-memory-manager\.md$' \
  | grep -v 'crux-cursor-meditation-guide\.md$' \
  | grep -v 'crux-cursor-meditation-guide\.source\.mdx$' \
  | grep -v 'spec-agent-allocation' \
  | grep -v 'zip-contents-protection' \
  | grep -v 'skill-and-agent-references' \
  || true)

if [ -n "${custom_hits}" ]; then
  warn "The following files still reference crux-cursor-memory-manager by name."
  warn "The umbrella dispatcher will continue working for one minor release, but"
  warn "you should re-point these to the appropriate crux-memory-* thin agent:"
  while IFS= read -r f; do
    warn "  ${f}"
  done <<< "${custom_hits}"
else
  log "No custom-caller references found — clean."
fi

# ---------------------------------------------------------------------------
# Step 4: Rebuild memory index after agent addition
# Detects both the repo-local layout and the consumer crux/ subdirectory layout.
# ---------------------------------------------------------------------------
if [ "${NEEDS_SPLIT}" -eq 1 ]; then
  section "Step 4: Rebuild memory index"

  INDEX_SCRIPT_REPO=".cursor/skills/crux-skill-memory-index/scripts/memory-index.py"
  INDEX_SCRIPT_CONSUMER=".cursor/skills/crux/crux-skill-memory-index/scripts/memory-index.py"

  if test -f "${INDEX_SCRIPT_REPO}"; then
    apply "rebuild memory index (repo layout)" python3 "${INDEX_SCRIPT_REPO}"
  elif test -f "${INDEX_SCRIPT_CONSUMER}"; then
    apply "rebuild memory index (consumer crux/ layout)" python3 "${INDEX_SCRIPT_CONSUMER}"
  else
    warn "memory-index.py not found at either expected path. Skipping index rebuild."
    warn "Run the memory index rebuild manually after locating the script."
  fi
fi

# ---------------------------------------------------------------------------
# Step 5: Re-run install.py to reconcile the installer manifest
# ---------------------------------------------------------------------------
section "Step 5: Reconcile installer manifest"

if test -f "install.py"; then
  apply "run python3 install.py" python3 install.py
else
  warn "install.py not found in ${REPO_ROOT}. Skipping installer reconciliation."
fi

# ---------------------------------------------------------------------------
# Step 6: Post-upgrade sanity check
# ---------------------------------------------------------------------------
section "Step 6: Post-upgrade sanity check"

ALL_OK=1

for agent in crux-memory-dream crux-memory-rem crux-memory-recall crux-memory-remember crux-memory-forget; do
  path_consumer=".cursor/agents/crux/${agent}.md"
  path_repo=".cursor/agents/${agent}.md"
  if test -s "${path_consumer}" || test -s "${path_repo}"; then
    log "OK: ${agent} present"
  else
    warn "MISSING: ${agent} — investigate before next release."
    ALL_OK=0
  fi
done

for template in ".cursor/agents/crux/templates/recall-canvas.tsx.md" ".cursor/agents/templates/recall-canvas.tsx.md"; do
  if test -s "${template}"; then
    log "OK: Canvas template present at ${template}"
    break
  fi
done

UMBRELLA_CONSUMER=".cursor/agents/crux/crux-cursor-memory-manager.md"
UMBRELLA_REPO=".cursor/agents/crux-cursor-memory-manager.md"
if test -f "${UMBRELLA_CONSUMER}" || test -f "${UMBRELLA_REPO}"; then
  log "OK: umbrella dispatcher present (deprecation window active)"
else
  warn "Umbrella dispatcher not found — thin agents must be fully in place before removing it."
fi

if [ "${ALL_OK}" -eq 0 ]; then
  echo
  warn "One or more sanity checks failed. Investigate before proceeding."
  exit 1
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo
if [ "${DRY_RUN}" -eq 1 ]; then
  echo "========================================================"
  echo "  DRY RUN complete. Re-run with --yes to apply changes."
  echo "========================================================"
else
  log "Upgrade complete."
fi
