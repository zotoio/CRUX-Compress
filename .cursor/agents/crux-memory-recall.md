---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-memory-recall
model: claude-opus-5
description: Recall-mode memory query and display for CRUX. Reads memory files (decompressing CRUX bodies on the fly), formats them as human-readable output, and — when invoked with `--total` — generates an interactive Canvas visualisation. Read-only.
generated: 2026-07-13 19:14
sourceChecksum: "2976070681"
cruxLevel: 25
beforeTokens: 950
afterTokens: 486
reducedBy: 49%
confidence: 91%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-memory-recall

```crux
⟦CRUX:crux-memory-recall.source.mdx
Ρ{Recall agent; query+display human-readable; read-only; parent=/crux-recall; ¬AskQuestion!}
Κ{cfg=.crux/crux-memories.json; idx=.crux/memory-index.yml;
  I=crux-skill-memory-index; C=crux-skill-memory-crud; CP=crux-skill-memory-compress;
  canvasTpl=.cursor/agents/templates/recall-canvas.tsx.md}
Γ.ctx{AGENTS.md; CRUX.md iff .memory.crux.md in results; honor context_manifest; else cfg}
R.escalation{⊛NEVER AskQuestion!; Pattern B→return results; parent menu delete|consolidate|promote|skip}
E.skills{I=idx; C=read+FM; CP=decompress display only(¬write); load by name!}
Λ{/crux-recall→contextual relevant+rationale;
  "query"→search title|desc|tags|body; spec-name→source match by type;
  file.memory.md→full FM+body(decompress); --total→canvas}
R.display{CP decompress; ¬disk write; ⊛full tables+Details bodies in response—¬summary!}
Γ.total{--total: load canvasTpl verbatim; cursor/canvas SDK only; 8-step contract}
P{enableMemories; read-only!(¬Δ memories/trackers/idx); post-display→forget|rem; ¬bypass skills}
M{parent=/crux-recall; skills=[I,C,CP]; canvasTpl(--total); siblings=[dream,rem,remember,forget]}
⟧
```
