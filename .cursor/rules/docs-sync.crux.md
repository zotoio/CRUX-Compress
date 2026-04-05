---
generated: 2026-04-04 12:00
sourceChecksum: 1356781034
cruxLevel: 25
beforeTokens: 468
afterTokens: 320
reducedBy: 32%
confidence: 88%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Documentation Synchronization Rule

```crux
⟦CRUX:docs-sync.md
Ρ{doc sync rule}
Κ{doc=documentation}
E.docs{
 README.md←install|usage|feature Δ
 CONTRIBUTORS.md←CI/CD|testing|contrib Δ
 web/compress.md/←landing|examples|feature highlights
}
Γ.README{
 install.py→upd install
 CRUX.md→upd spec+examples
 .cursor/commands/*→upd cmd usage
 .cursor/skills/*/SKILL.md→upd skill desc
}
Γ.CONTRIBUTORS{
 .github/workflows/*.yml→upd CI/CD flow+desc
 evals/*.py→upd test struct|run
 scripts/*.sh→upd dev setup
 tests/helpers.bash→upd test helper doc
}
Γ.web{
 CRUX.md→upd spec examples on landing
 +feature→upd feature highlights
 .cursor/agents/*→upd agent/tooling desc
}
R.upd{
 surgical; ¬rewrite
 format=consistent
 upd ver+paths+examples
 +workflow|test→+tables/lists
 CI/CD flow diagram=accurate
}
P.skip{
 .cursor/rules/example/*
 temp|gen files
 ¬spec features→doc existing only
}
Ω{concise|actionable}
⟧
```
