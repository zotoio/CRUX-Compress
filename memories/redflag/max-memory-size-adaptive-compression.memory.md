---
title: "maxMemorySize hard cap may force compression beyond target ratio — plan for adaptive escalation"
description: "Memory files have a hard size cap (default 2048 bytes). If the target compression ratio (default 33%) still exceeds maxMemorySize, the compression logic must escalate aggressiveness. If maximum compression still exceeds the cap, flag for manual review rather than silently truncating."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [compression, limits, adaptive, memory-size]
---

**Pitfall**: Assuming the target compression ratio (e.g., 33%) is always sufficient.

**Problem**: Some memories start large enough that even 33% of original still exceeds `maxMemorySize` (default 2048 bytes). A 10KB memory compressed to 33% is still 3.3KB — over the limit.

**Required behavior**:

1. Compress to target ratio (33%)
2. Check size against `maxMemorySize`
3. If exceeded, increase compression aggressiveness (remove examples, shorten descriptions, use more CRUX notation)
4. Repeat until size is acceptable OR maximum compression reached
5. If still too large at maximum compression, flag for **manual review** — do NOT silently truncate

Silent truncation causes data loss. The user must decide whether to split the memory, increase the size limit, or accept information loss.
