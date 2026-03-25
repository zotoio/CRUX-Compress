---
generated: 2026-03-10 14:00
sourceChecksum: 506935896
cruxLevel: 25
beforeTokens: 525
afterTokens: 318
reducedBy: 39%
confidence: 95%
crux: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Zip Contents Protection Rule

```crux
⟦CRUX:zip-contents-protection.md
P.⊛{¬auto-add to scripts/create-crux-zip.sh w/o explicit user request!}

Κ{script=scripts/create-crux-zip.sh→dist pkg;
 affects=[installs,ver bumps,dist size]}

P.never{auto-add when creating:
 .cursor/rules/*.mdc|.cursor/skills/*/|scripts/*.sh|any files}

P.only{Δ zip when user says:
 "add X to dist zip"|"include X in release"|"modify zip contents"}

Λ.add{w/ permission→
 1.Δ scripts/create-crux-zip.sh +path;
 2.Δ .github/workflows/version-bump.yml RELEASE_PATHS;
 3.Δ CONTRIBUTORS.md table;
 4.warn: +file→ver bump}

M.zip{
 CRUX.md;.crux/crux.json;AGENTS.crux.md←AGENTS.md;
 .cursor/[hooks.json,agents/crux-cursor-rule-manager.md,
 commands/crux-compress.md,hooks/[crux-detect-changes.sh,crux-session-start.sh],
 rules/_CRUX-RULE.mdc,skills/crux-utils/[SKILL.md,scripts/crux-utils.sh]]}

Ω{dist=minimal;+files→[↑size,?conflicts,↑updates,↑maint]}
⟧
```
