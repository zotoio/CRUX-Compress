---
id: "01d6207"
title: "File-based inter-agent coordination outperforms transcript polling for deep recursive trees"
description: "For deep recursive agent trees (9+ agents), file-based coordination via a shared working directory outperforms both JSONL transcript polling and in-context return values. Each agent writes to a predictable file path; parents poll via prefix-globs."
type: "core"
strength: 2
created: 2026-05-24
modified: 2026-05-24
source: "20260516-meditate-research-mode-overhaul"
tags: [architecture, agent-coordination, file-based, polling, recursive-agents, working-directory, design-pattern]
---

For deep recursive agent trees (9+ agents), file-based coordination via a shared working directory outperforms both JSONL transcript polling and in-context return values. Each agent writes its output to a predictable file path; parent agents poll for child output files using prefix-globs to know when aggregation can proceed.

Key properties that make this superior:
- **Predictable paths**: `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}.md` — parents know the prefix, can glob without knowing the trailing slug/timestamp
- **Self-describing files**: YAML frontmatter carries mode, branch, depth, subfocus, parent, timestamp — any agent can understand any file without context
- **Crash recovery**: files persist on disk; a crashed child's partial output is visible to the parent's next poll
- **No transcript parsing**: JSONL transcripts are opaque, model-specific, and expensive to scan at scale
- **Lock-free except where needed**: only the global facet registry requires a mutex (`mkdir`-based); everything else is append-only or single-writer

The `mkdir`-based lock protocol (create directory = acquire, `rmdir` = release, orphan cleanup after 5 minutes of stale lock) provides a lightweight filesystem mutex for the one truly contended resource (facet-registry.yml) without introducing external dependencies.
