---
id: "cd0c954"
title: "Archive original source files before overwriting with compressed outputs"
description: "When compressing memory files (or any CRUX compression), move the original uncompressed file to a dated archive directory (e.g., .ai-ignored/memories/sources/[yyyymmdd]/) before writing the compressed version. This preserves rollback capability and audit trail."
type: "core"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [compression, archival, rollback, data-integrity]
compressed: true
compressionTarget: 33
beforeTokens: 150
afterTokens: 50
reducedBy: 67%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/archive-source-before-compression.memory.md
---

⟦CRUX:memory
Γ.compress{
 1.mkdir .ai-ignored/memories/sources/{yyyymmdd}/
 2.mv original→archive
 3.write compressed@original.crux.md
}
R{rollback preserved; audit trail; .ai-ignored/=¬agent ctx; group by date→easy cleanup}
Ω{∀destructive transform→archive original first}
⟧
