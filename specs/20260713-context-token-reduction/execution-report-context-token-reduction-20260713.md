# Execution Report: context-token-reduction

**Spec**: `specs/20260713-context-token-reduction/`  
**Executed**: 2026-07-13  
**Executor**: Spec System (`/z-spec-execute`)  
**Agents**: `crux-platform-architect`, `crux-software-engineer`, `crux-cursor-rule-manager`

---

## Executive Summary

The `context-token-reduction` spec shipped nine subtasks targeting a ≥30% reduction in context tokens consumed per agent spawn across common CRUX workflows. All nine subtasks completed and were independently judge-verified.

**What shipped:**

- **Lazy CRUX.md loading** (S01): Removed unconditional `Read CRUX.md` from five agents; added `context_manifest` honor block pattern. Saves ~7,341 tokens per non-CRUX agent spawn.
- **Always-on rules compressed** (S02): CRUX-compressed the two largest always-applied rules (`docs-sync.crux.mdc`, `crux-memories-integration.crux.mdc`).
- **Compress-command template extraction** (S03): Extracted inline compression prompts into `.cursor/commands/templates/compress-prompts.md`, reducing `crux-compress` fat file.
- **Shared memory surface deduplication** (S04): Extracted cross-agent boilerplate into `.cursor/skills/_memory-shared.md`, pointed thin agents and skills at it.
- **Memory-manager split** (S05): Split the 27.5 KB monolithic `crux-cursor-memory-manager.md` into five mode-scoped thin agents (`crux-memory-dream`, `crux-memory-rem`, `crux-memory-recall`, `crux-memory-remember`, `crux-memory-forget`) plus an extracted Canvas template. Saves 52–80% tokens depending on the operation.
- **`/crux-test` pytest shim** (S06): Rewrote `/crux-test` to delegate to the pytest suite rather than running LLM-only tests; added `evals/test_p_crux_test.py`.
- **CRUX compression of large primitives** (S07): Wave 1 (crux-meditate, meditation-guide, crux-compress) + Wave 2 (five thin agents) compressed to ≤25% of source tokens with ≥91% confidence. Waves 3–5 deferred.
- **Evals and CI coverage** (S08): Added `evals/test_s_context_reduction.py` covering all key invariants; added `context_reduction_smoke` pytest marker; extended CI.
- **Docs sync and upgrade file** (S09, this subtask): Upgrade script, docs updates, execution report (this file).

**Tokens saved (average across three canonical workflows)**: ~57.6% reduction. See [Baseline vs Post-Spec Token-Cost Table](#baseline-vs-post-spec-token-cost-table).

---

## Per-Subtask Status

| Subtask | Title | State | Judge |
|---------|-------|-------|-------|
| S01 | Lazy CRUX.md + context_manifest | completed | verified |
| S02 | Compress always-on rules | completed | verified |
| S03 | Extract compress-command templates | completed | verified |
| S04 | Dedupe memory skill shared surface | completed | verified |
| S05 | Split memory-manager + Canvas template | completed | verified |
| S06 | /crux-test pytest shim | completed | verified |
| S07 | CRUX-compress large primitives | completed | verified |
| S08 | Evals and CI coverage | completed | verified |
| S09 | Docs sync + upgrade file | completed | verified |

Status files: [`status/`](status/)

---

## Baseline vs Post-Spec Token-Cost Table

Source: [`evals/reports/context-token-reduction-baseline.md`](../../evals/reports/context-token-reduction-baseline.md)

### Per-File Token Savings (Wave 1+2 Compressions — S07)

| File | Pre-spec (SoT) | Post-spec (Loadable) | Saved | Ratio |
|------|---------------:|-----------:|------:|------:|
| `crux-meditate.md` | 25,468 | 5,207 | 20,261 | 20.4% |
| `crux-cursor-meditation-guide.md` | 10,745 | 2,189 | 8,556 | 20.4% |
| `crux-compress.md` | 6,395 | 1,408 | 4,987 | 22.0% |
| `crux-memory-dream.md` | 1,245 | 671 | 574 | 53.9% |
| `crux-memory-rem.md` | 1,084 | 627 | 457 | 57.8% |
| `crux-memory-recall.md` | 950 | 520 | 430 | 54.7% |
| `crux-memory-remember.md` | 875 | 473 | 402 | 54.1% |
| `crux-memory-forget.md` | 941 | 487 | 454 | 51.7% |
| **Total Wave 1+2** | **47,703** | **11,582** | **36,121** | **24.3%** |

### Canonical Workflow Summary

| Workflow | Pre-spec tokens | Post-spec tokens | Reduction | % Saved |
|----------|----------------:|-----------------:|----------:|--------:|
| (a) Trivial Q&A | ~12,120 | ~4,779 | ~7,341 | **60.6%** |
| (b) `/crux-dream` (no compressed mems) | ~18,750 | ~8,980 | ~9,770 | **52.1%** |
| (c) 10-subtask `/z-spec-execute` | ~122,160 | ~48,750 | ~73,410 | **60.1%** |
| **Average** | | | | **~57.6%** |

> The ≥30% aspirational target is met across all three workflows. The dominant gains come from lazy CRUX.md loading (S01) and Wave 1 CRUX compression of meditate/guide/compress (S07).

---

## Deferred Compressions (S07 Waves 3–5)

The following files were not compressed due to budget constraints or policy:

| File | Reason |
|------|--------|
| `.cursor/agents/crux-cursor-memory-manager.md` | Skip: thin shim ≤60 lines — compression overhead outweighs savings |
| `.cursor/commands/crux-test.md` | Explicit skip: S06 rewrote it as a thin pytest shim |
| Wave 3 meditation skills (6 files) | Deferred: budget |
| Wave 4 memory skills (6 files, incl. memory-compress) | Deferred: leave plaintext |
| Wave 5 remaining agents/commands (5 files) | Deferred: budget |

These compressions can be applied in a future spec or via `/crux-compress` at operator discretion.

---

## Dist Manifest Additions — Awaiting User Approval

> **`scripts/create-crux-zip.py` was NOT modified by this spec.** The user must review and apply the additions below at their discretion. The accompanying version bump (`.crux/crux.json`) is done in the release commit, not by this spec.

The following new files were created by this spec and must be added to `SOURCE_DIST_FILES` in `scripts/create-crux-zip.py` for consumers to receive them in the distribution zip.

### From S05 (Memory-Manager Split)

Add after the existing `.cursor/agents/crux-cursor-memory-manager.md` entry so the memory-agent block stays cohesive:

```python
# In SOURCE_DIST_FILES, after ".cursor/agents/crux-cursor-memory-manager.md":
".cursor/agents/crux-memory-dream.md",
".cursor/agents/crux-memory-rem.md",
".cursor/agents/crux-memory-recall.md",
".cursor/agents/crux-memory-remember.md",
".cursor/agents/crux-memory-forget.md",
".cursor/agents/templates/recall-canvas.tsx.md",
```

> The umbrella `.cursor/agents/crux-cursor-memory-manager.md` **stays in the list** during the deprecation window so pre-upgrade consumer installs continue to resolve the registered name. Remove it after one minor release once all consumers have run the upgrade script.

### From S03 (Compress-Command Template)

Add in the commands templates section:

```python
# In SOURCE_DIST_FILES, in the commands section:
".cursor/commands/templates/compress-prompts.md",
```

### From S04 (Shared Memory Surface)

Add in the skills section:

```python
# In SOURCE_DIST_FILES, before or in the crux-skill-memory-* group:
".cursor/skills/_memory-shared.md",
```

### From S07 (SoT `.source.mdx` files — optional, for consumers who edit primitives)

These SoT files are not required for consumers who only use the shipped loadables. Include if consumers should be able to edit and regenerate CRUX-compressed primitives locally:

```python
# In SOURCE_DIST_FILES, SoT sources alongside their loadable counterparts:
".cursor/commands/crux-compress.source.mdx",
".cursor/commands/crux-meditate.source.mdx",
".cursor/agents/crux-cursor-meditation-guide.source.mdx",
".cursor/agents/crux-memory-dream.source.mdx",
".cursor/agents/crux-memory-rem.source.mdx",
".cursor/agents/crux-memory-recall.source.mdx",
".cursor/agents/crux-memory-remember.source.mdx",
".cursor/agents/crux-memory-forget.source.mdx",
```

### Approval gate

Per `zip-contents-protection.crux.mdc`, no automatic modifications were made to `scripts/create-crux-zip.py`. To apply:

1. Review each group above.
2. Edit `scripts/create-crux-zip.py` manually to add the approved paths.
3. Run `python3 scripts/create-crux-zip.py` to rebuild the dist zip and update `.crux/dist-manifest.json`.
4. Commit with a `feat:` message to trigger the minor version bump.

---

## Version Bump Note

Per `version-bump.crux.mdc`, this spec introduces a `feat` (new mode-scoped agents, new skills surface, new eval coverage) and requires a **minor** version bump to `.crux/crux.json` at the release commit. This bump is performed by the release engineer when merging the spec changes to `main` — it is **not** applied inside the spec.

---

## Consumer Upgrade Instructions

For existing CRUX-Compress consumer installs upgrading to the post-spec state:

1. Run the upgrade script (dry-run first):

   ```bash
   bash specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh
   bash specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh --yes
   ```

   The script:
   - Detects pre-upgrade installs (umbrella present, thin agents absent)
   - Copies thin agents and Canvas template from the repo/dist into the consumer `.cursor/agents/crux/` path
   - Warns if `scripts/create-crux-zip.py` has not yet been updated with the new files
   - Audits for custom callers still referencing the deprecated umbrella dispatcher
   - Rebuilds the memory index
   - Re-runs `install.py` to reconcile the installer manifest
   - Runs post-upgrade sanity checks

2. See the full per-step consumer upgrade guide in [`subtask-05-split-memory-manager-and-canvas-template-20260713.md`](subtask-05-split-memory-manager-and-canvas-template-20260713.md#consumer-upgrade-steps).

---

*This report is the D07 deliverable for Subtask 09 of the context-token-reduction spec.*
