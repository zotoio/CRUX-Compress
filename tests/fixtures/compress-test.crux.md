---
generated: 2026-02-08 14:32
sourceChecksum: 2179275645
beforeTokens: 480
afterTokens: 291
confidence: 93%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Test Coding Standards Rule

```crux
⟦CRUX:compress-test.md
Ρ{test coding standards; BATS test suite}
Κ{test=unit test; fixture=test data file}

R.naming{
  tests=test_*.bats; fixtures=*.md|*.mdc; helpers=helpers.bash
}

R.structure{
  setup()→init env; teardown()→cleanup tmp!
  ¬artifacts in workdir; tmp→$BATS_TMPDIR
}

R.assertions{
  success→assert_success; fail→assert_failure
  substr→assert_output --partial; line→assert_line
}

E.patterns{
  ⊤:@test "desc"{run fn ""»assert_failure»assert_output --partial "err"}
  ⊥:@test "test"{fn "" #¬run,¬assert}
}

Γ.apply{
  +BATS tests; review test PRs; debug test fails
}

P.critical{
  ⊛¬skip run⊲assertions!
  ⊛cleanup tmp@teardown!
  ⊛descriptive test names!
  ⊛¬hardcoded paths→use vars
}

P.err{
  fail→check $output+$status+$lines
  debug→set -x temp
}
⟧
```
