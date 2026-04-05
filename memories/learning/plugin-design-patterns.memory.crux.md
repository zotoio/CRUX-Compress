---
id: "b0c02ea"
title: "Plugin design patterns: advisory gates and progressive enhancement defaults"
description: "Plugins should use advisory quality gates (failClosed: false) that warn but preserve output, combined with enabledByDefault for progressive enhancement. Users retain full control via --no-plugin for opt-out or explicit --plugin flags which override all defaults."
type: "learning"
strength: 2
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [plugins, quality-gates, advisory, user-experience, policy, defaults, opt-out, architecture, extensibility]
consolidated_from: ["a97d331", "daab846"]
compressed: true
compressionTarget: 33
beforeTokens: 280
afterTokens: 95
reducedBy: 66%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/plugin-design-patterns.memory.md
---

⟦CRUX:memory
Φ.advisory{failClosed=⊥→warn+write; output=always; strict=opt-in via --no-plugin|failClosed:⊤}
R.advisory{guideline≻hard; ¬lose output; iterate ok}

Φ.defaults{enabledByDefault→progressive enhancement; ¬break existing}
Γ.flags{
 ∅→load defaults auto
 --plugin X→X only; override all
 --no-plugin X→defaults-X
}
R.design{explicit≻implicit; scripts unchanged; opt-out=granular}
Ω{extensible CLI; +capability default; user ctrl retained}
⟧
