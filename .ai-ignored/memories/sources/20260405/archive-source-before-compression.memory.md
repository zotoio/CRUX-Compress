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
---

Before replacing an uncompressed file with its CRUX-compressed version:

1. Create the archive directory if needed: `.ai-ignored/memories/sources/{yyyymmdd}/`
2. Move (not copy) the original file to the archive directory
3. Write the new compressed file to the original location with `.crux.md` extension

This pattern:
- Preserves the original for rollback if compression introduces errors
- Provides an audit trail of what was compressed and when
- Uses `.ai-ignored/` to keep archives out of agent context by default
- Groups by date for easy cleanup of old archives

The same pattern applies to any destructive transformation where the original might be needed.
