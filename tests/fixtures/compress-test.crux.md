---
generated: 2026-04-26 00:55
sourceChecksum: "2179275645"
cruxLevel: 25
beforeTokens: 480
afterTokens: 247
reducedBy: 49%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards rule}
Κ{ut=unit test; fx=fixture; h=helper}

R.naming{
  ut:test_*.bats; fx:*.md|*.mdc; h:helpers.bash
}

R.struct{
  setup()→init env; teardown()→cleanup
  ¬artifacts!; tmp→$BATS_TMPDIR
}

R.assert{
  assert_success|assert_failure
  assert_output --partial→substring
  assert_line→specific ln
}

E.good{
  @test "desc" { run fn ""; assert_failure; assert_output --partial "err" }
}

E.bad{
  @test "test" { fn "" } # ¬run,¬assert
}

Λ.apply{+BATS tests|PR review|debug}

P.critical{
  ¬skip run!; cleanup in teardown!
  test names=descriptive!; ¬hardcoded paths→use vars
}

P.err{
  fail→check[$output,$status,$lines]; debug→set -x
}
⟧
```
