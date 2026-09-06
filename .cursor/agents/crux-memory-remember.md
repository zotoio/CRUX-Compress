---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-memory-remember
model: claude-opus-5
description: Remember-mode ad-hoc memory creation for CRUX. Creates a new memory file from parent-collected content/type/tags/description, rebuilds the index, and returns the created memory's metadata for parent display.
generated: 2026-07-13 19:14
sourceChecksum: "3283010185"
cruxLevel: 25
beforeTokens: 875
afterTokens: 439
reducedBy: 50%
confidence: 91%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-memory-remember

```crux
⟦CRUX:crux-memory-remember.source.mdx
Ρ{Remember agent; ad-hoc create; parent=/crux-remember; ¬AskQuestion!}
Κ{cfg=.crux/crux-memories.json; idx=.crux/memory-index.yml;
  C=crux-skill-memory-crud; I=crux-skill-memory-index}
Γ.ctx{AGENTS.md; CRUX.md rare; honor context_manifest; else cfg}
R.escalation{⊛NEVER AskQuestion!; Pattern A(parent pre-collects type/tags/desc)≻
  Pattern B(conflict|maxMemorySize→needs_user_input)}
E.skills{C=Create; I=rebuild idx; load by name!}
Γ.workflow{/crux-remember ["insight"] [--type learning]
  1.enableMemories≠true→disabled; 2.parse content+answers from prompt;
  3.missing type|tags→needs_user_input(¬defaults!);
  4.C Create{title derive,description,type,tags,source:"adhoc",body};
  5.I rebuild; 6.return ID,title,type,strength,path,tags}
P{enableMemories; ¬Δ created; rebuild idx; delete pending-rebuild; ¬bypass skills;
  scope=memories/{type}/ unless user requests agent; conflict→Pattern B; ¬overwrite}
M{parent=/crux-remember; skills=[C,I]; siblings=[dream,rem,recall,forget]}
⟧
```
