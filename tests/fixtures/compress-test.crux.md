---
generated: 2026-05-10 19:08
sourceChecksum: "2179275645"
cruxLevel: 25
beforeTokens: 480
afterTokens: 285
reducedBy: 41%
confidence: pending
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards+best practices}
Κ{ut=unit test; fx=fixture; hlp=helper}
R.naming{
  ut=test_*.bats; fx=*.md|*.mdc; hlp=helpers.bash
}
R.structure{
  ∀test→setup()+teardown()!
  teardown→cleanup temp; use $BATS_TMPDIR
  ¬artifacts in workdir!
}
R.assert{
  success→assert_success; fail→assert_failure
  substr→assert_output --partial; ln→assert_line
}
E{
  ⊤:run fn ""»assert_failure»assert_output --partial "Error: empty input"
  ⊥:fn "" w/o run|assertions
}
Λ.apply{+BATS tests; +review test PRs; +debug test failures}
P.⊛{
  ¬skip run⊲assertions!
  ∀teardown→cleanup temp!
  test names=descriptive!
  ¬hardcoded paths→use vars!
}
P.err{
  fail→check $output+$status+$lines
  debug→set -x(temp)
}
⟧
```
