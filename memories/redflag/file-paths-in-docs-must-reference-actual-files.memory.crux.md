---
id: "dbfd3ed"
title: "File paths in documentation and websites must reference files that actually exist"
description: "Adversarial verification caught that web/compress.md/index.html listed hook files as .sh when the actual files are .py. Documentation file trees should be verified against disk contents, not assumed accurate from previous edits."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [documentation, verification, website, file-paths, adversarial]
compressed: true
compressionTarget: 33
beforeTokens: 130
afterTokens: 45
reducedBy: 65%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/file-paths-in-docs-must-reference-actual-files.memory.md
---

⟦CRUX:memory
P.⊛{doc file trees→stale names|extensions}
E.example{web/ listed .sh; actual=.py; audit missed stale ext}
R.prevention{
 1.rename|re-ext→grep all docs for old name
 2.checklist∋"paths point to files that exist"
 3.adversarial verifiers spot-check paths vs ls
}
⟧
