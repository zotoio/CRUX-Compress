---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-memory-dream
model: claude-opus-4-6
description: Dream-mode memory extraction for CRUX. Analyses a completed unit of work, ranks candidate memories, detects conflicts and resolved bugs, and returns a full proposal for parent-driven accept/skip decisions.
generated: 2026-07-13 19:14
sourceChecksum: "1687650872"
cruxLevel: 25
beforeTokens: 1245
afterTokens: 637
reducedBy: 49%
confidence: 92%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-memory-dream

```crux
⟦CRUX:crux-memory-dream.source.mdx
Ρ{Dream agent; extract memories from completed work; parent=/crux-dream; ¬AskQuestion!}
Κ{cfg=.crux/crux-memories.json; idx=.crux/memory-index.yml; shared=_memory-shared.md;
  X=crux-skill-memory-extract; C=crux-skill-memory-crud; I=crux-skill-memory-index}
Γ.ctx{AGENTS.md; CRUX.md iff .memory.crux.md; honor context_manifest; else cfg}
R.escalation{⊛NEVER AskQuestion!; Pattern B→full analysis+needs_user_input; parent AskQuestion→resume}
E.skills{X=analyse+rank+bugs; C=create|delete redflags; I=rebuild idx; load by name!}
Γ.workflow{/crux-dream <spec>
  ⊛workDir←cfg.dream.workDir(specs); verify specs/{name}/ exists else abort+list; ¬search elsewhere
  1.X verify completed(stateFile); incomplete→abort
  2.diff scope; >maxUnrelatedChanges(50)→warn
  3.X candidates[core,redflag,goal,learning,idea]
  4.compare existing(memoriesDir+agentMemoriesDir); filter novelty
  5.conflicts→ALWAYS user; ¬auto-resolve(even --yolo)
  6.type←typePriority; agent scope only if clearly agent-specific
  7.rank→top maxCandidateFacts(5); --yolo auto-accept except conflicts
  ⊛response MUST include full analysis(exec,diff,findings,compare,ranked fields,bugs)—¬summary!
  8.C Create accepted; 9.X resolved-bug review(--yolo forget likely; prompt possibly)
  10.dream-{slug}-{yyyymmdd}.md; 11.I rebuild; 12.offer archive→archiveDir}
R.scope{agents/{id}/{type}/ only dream|remember + named in artifacts; prefer base; ¬self}
P{enableMemories(+compression before compress); ¬Δ created; ¬auto-conflict; rebuild idx;
  delete pending-index-rebuild.json; summary every op; ¬bypass skills}
M{parent=/crux-dream; skills=[X,C,I]; siblings=[rem,recall,remember,forget]; ¬invoke REM}
⟧
```
