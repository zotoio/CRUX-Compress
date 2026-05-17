---
generated: 2026-05-17 16:43
sourceChecksum: "2179275645"
cruxLevel: 25
beforeTokens: 480
afterTokens: 184
reducedBy: 62%
confidence: 90%
crux: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards}
R.naming{test_*.bats;*.md|*.mdc;helpers.bash}
R.struct{setup()→init;teardown()→cleanup;$BATS_TMPDIR}
R.assert{assert_[success|failure|output --partial|line]}
E{⊤:run fn ""→assert_failure+"Error: empty input";⊥:¬run|assert}
Γ{BATS|pr review|debug}
P.⊛{run⊲assert!;cleanup@teardown!;desc names!;¬hardcode→vars}
P.err{$output+$status+$lines;set -x}
⟧
```
