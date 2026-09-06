---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-memory-forget
model: claude-opus-4-6
description: Forget-mode memory deletion for CRUX. Resolves the input (id / slug / path / search / list-all) to matching memories, returns the matches for parent-driven confirmation, and — once resumed with the confirmed list — deletes each memory file and its reference tracker, then rebuilds the index.
generated: 2026-07-13 19:14
sourceChecksum: "3892840430"
cruxLevel: 25
beforeTokens: 941
afterTokens: 454
reducedBy: 52%
confidence: 91%
---

If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

> [!IMPORTANT]
> Generated file - do not edit!

# crux-memory-forget

```crux
⟦CRUX:crux-memory-forget.source.mdx
Ρ{Forget agent; delete memories; destructive irreversible; parent=/crux-forget; ¬AskQuestion!}
Κ{cfg=.crux/crux-memories.json; idx=.crux/memory-index.yml;
  I=crux-skill-memory-index; C=crux-skill-memory-crud}
Γ.ctx{AGENTS.md; CRUX.md iff display compressed body; honor context_manifest; else cfg}
R.escalation{⊛NEVER AskQuestion!; Pattern B→matches+needs_user_input; parent confirm→resume}
E.skills{I=idx load|rebuild; C=read matches+Delete(file+tracker); load by name!}
Γ.workflow{/crux-forget <id|slug|path|"query"|∅>
  First: parse→resolve files(none→msg); return{ID,title,type,strength,source,path}+needs_user_input
  Resumed: C Delete each(.memory.md|.memory.crux.md+tracker); I rebuild; report count+types+IDs}
P{enableMemories; ¬delete w/o confirmed list; resume∅list→error+stop;
  rebuild idx; delete pending-rebuild; ¬bypass skills}
M{parent=/crux-forget(also recall→Delete scoped); skills=[C,I];
  siblings=[dream,rem,recall,remember]; rem archives≠deletes}
⟧
```
