---
generated: 2026-03-11 14:32
sourceChecksum: "2179275645"
cruxLevel: 25
beforeTokens: 480
afterTokens: 313
reducedBy: 35%
confidence: 93%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards; BATS test suite best practices}
Κ{ut=unit test; fix=fixture; tmp=$BATS_TMPDIR}

R.naming{
  ut=test_*.bats; fix=*.md|*.mdc; helpers=helpers.bash
}

R.struct{
  setup()→init env; teardown()→cleanup tmp
  ¬artifacts in workdir!; tmp files→$BATS_TMPDIR
}

R.assert{
  success→assert_success; fail→assert_failure
  substr→assert_output --partial; line→assert_line
}

E.good{
  @test "fn handles empty input"→run fn ""»assert_failure»
    assert_output --partial "Error: empty input"
}

E.bad{
  @test "test something"→fn "" # ¬run,¬assert!
}

Λ.apply{
  +BATS tests; review test PRs; debug test fails
}

P.critical{
  ¬skip run⊲assert!; ∀teardown→cleanup tmp!
  test names=descriptive!; ¬hardcoded paths→use vars
}

R.err{
  fail→check $output+$status+$lines
  debug→set -x temp
}
⟧
```
