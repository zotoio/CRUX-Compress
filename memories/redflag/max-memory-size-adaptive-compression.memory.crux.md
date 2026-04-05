---
id: "da3d798"
title: "maxMemorySize hard cap may force compression beyond target ratio — plan for adaptive escalation"
description: "Memory files have a hard size cap (default 1000 lines) and a minimum compression threshold (default 500 lines). Files below compressionMinLines are not compressed. If the target compression ratio (default 33%) still exceeds maxMemorySize, the compression logic must escalate aggressiveness. If maximum compression still exceeds the cap, flag for manual review rather than silently truncating."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [compression, limits, adaptive, memory-size]
compressed: true
compressionTarget: 33
beforeTokens: 160
afterTokens: 55
reducedBy: 66%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/max-memory-size-adaptive-compression.memory.md
---

⟦CRUX:memory
P.⊛{¬assume 33% always fits; check compressionMinLines(500) first; 1500L×33%=495L<1000}
Γ.adaptive{
 1.compress→33%
 2.check vs maxMemorySize
 3.exceeded→↑aggressiveness(¬examples,shorter desc,+CRUX)
 4.repeat until ok|max compression
 5.still>cap→flag manual review;¬truncate
}
R{silent truncation=data loss; user decides split|↑limit|accept loss}
⟧
