---
generated: 2026-04-25 19:26
sourceChecksum: "2179275645"
cruxLevel: 25
beforeTokens: 480
afterTokens: 305
reducedBy: 36%
confidence: pending
crux: true
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards rule}
Κ{ut=unit test; fx=fixture; hlp=helper}

R.naming{
  ut→test_*.bats(test_utils.bats)
  fx→*.md|*.mdc(sample-rule.md)
  hlp→helpers.bash
}

R.structure{
  setup()→init env; teardown()→cleanup tmp
  ¬leave artifacts; use $BATS_TMPDIR
}

R.assert{
  success→assert_success; fail→assert_failure
  substr→assert_output --partial; ln→assert_line
}

E.good{
  @test "desc" {run fn ""; assert_failure; assert_output --partial "err"}
}

E.bad{
  @test "vague" {fn ""} #¬run,¬assert
}

Γ.apply{
  +BATS tests; +review PR; +debug fail
}

P.critical{
  ⊛¬skip run⊲assert!
  ⊛cleanup tmp@teardown!
  ⊛desc test names!
  ⊛¬hardcoded paths→use vars
}

P.err.debug{
  $output→err msg; $status→exit code
  $lines→ln-by-ln; set -x→temp debug
}
⟧
```
