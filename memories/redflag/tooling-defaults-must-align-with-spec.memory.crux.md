---
id: "96a7410"
title: "Tooling defaults must align with specification defaults — drift causes silent mismatches"
description: "The crux-utils.py default compression target was 20% while the CRUX.md specification said 25%. This drift went unnoticed until a dedicated plugin refactor. Tools that implement spec behavior must track and match spec defaults."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [tooling, specification, defaults, drift, alignment]
compressed: true
compressionTarget: 33
beforeTokens: 155
afterTokens: 50
reducedBy: 68%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/tooling-defaults-must-align-with-spec.memory.md
---

⟦CRUX:memory
P.⊛{tool default≠spec default→silent mismatch}
E.example{crux-utils.py --ratio=20%; CRUX.md=25%; ¬noticed until plugin refactor}
R.prevention{
 1.impl spec→ref spec constant(comment|cfg)
 2.spec default=tool default
 3.test: tool.default==spec.documented
 4.Δspec default→grep hardcoded old val
}
⟧
