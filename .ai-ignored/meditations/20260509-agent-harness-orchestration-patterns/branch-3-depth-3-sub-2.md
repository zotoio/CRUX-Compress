---
branch: 3
depth: 3
subfocus_index: 2
subfocus: "Skip-by-default env-var gating patterns and failure modes"
parent_subfocus: "How should agent harnesses classify operations into cost tiers and gate execution accordingly?"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The parent subfocus asks how agent harnesses should classify and gate by cost tier. This branch drills into the specific mechanism — skip-by-default env-var gating — examining its inversion logic, discoverability strategies, naming conventions, the interplay between per-category gates and global deadlines, and how package.json scripts encode opt-in paths. The pattern is already implemented in this repo and deserves deep analysis of its design choices and failure modes.

## Discoveries

### The canonical pattern and its inversion logic

[memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE with skip-by-default] The repo uses this exact construct:

```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";
describe.skipIf(skipExpensive)("Q: Meditate", () => { /* ... */ });
```

The `!== "false"` comparison is a deliberate design choice with specific properties:

| Env var value | `!== "false"` result | Behavior |
|---------------|---------------------|----------|
| `undefined` (unset) | `true` | **Skip** (safe default) |
| `""` (empty) | `true` | **Skip** |
| `"true"` | `true` | **Skip** |
| `"1"` | `true` | **Skip** |
| `"false"` | `false` | **Run** (only opt-in path) |
| `"False"` (typo) | `true` | **Skip** (safe failure) |
| Any other string | `true` | **Skip** |

Only the exact string `"false"` enables execution. Every misconfiguration, typo, or unset state defaults to the safe (cheap) path. This is maximally conservative — the universe of possible env var states collapses to a single opt-in value.

The alternative `=== "true"` inversion for a `RUN_EXPENSIVE` variable would achieve the same runtime behavior but the naming would differ. The SKIP naming is superior because it matches what the user observes: test output says "SKIPPED" and references the SKIP variable. The name describes the default behavior, not the opt-in behavior.

### Five-channel discoverability

[memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE with skip-by-default] The discoverability problem — engineers not knowing gated tests exist — is attacked through five independent channels:

1. **Console output at setup time**: `vitest.setup.ts` prints `"✓ Expensive tests (Meditate, Integration) will be SKIPPED (set SDK_EVAL_SKIP_EXPENSIVE=false to run them)"` on every run. This is the most important channel because it's impossible to miss during normal development.

2. **`.env.example`**: Documents the variable with its default and how to override. Template for copying into `.env`.

3. **README env var table**: Documents all variables in a structured table. Entry point for new contributors.

4. **`package.json` scripts**: `pnpm run` lists all available scripts including `test:meditate` and `test:integration`. The script names themselves are discoverable.

5. **Test file header comments**: Each gated test file documents the gate in its JSDoc header: `"GATED behind SDK_EVAL_SKIP_EXPENSIVE (default: skip). Run explicitly: SDK_EVAL_SKIP_EXPENSIVE=false pnpm test:integration"`.

Each channel compensates for the others being missed. An engineer who reads only the README, or only runs `pnpm test`, or only reads the test source will still discover the gate.

### Naming convention: `{SYSTEM}_{SUBSYSTEM}_{ACTION}_{QUALIFIER}`

The env var `SDK_EVAL_SKIP_EXPENSIVE` follows a scoped naming pattern: `SDK_EVAL` (system/subsystem) + `SKIP` (action/default behavior) + `EXPENSIVE` (qualifier/category). The companion `SDK_EVAL_MAX_DURATION_MS` shares the system prefix but describes a threshold rather than a binary gate.

This convention encodes two properties in the name: (a) what system it belongs to (preventing collisions), and (b) what the default behavior is (SKIP). An engineer encountering the variable can infer the default without reading documentation.

### Package.json as opt-in encoding

The `package.json` scripts create named aliases that inline the env var override:

```json
"test": "vitest run",
"test:meditate": "SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep 'Meditate'",
"test:integration": "SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep 'Integration'"
```

Key properties of this design:

- **`pnpm test` is always safe**: It runs only non-gated tests. No env var manipulation can change this because the base `test` script doesn't touch the gate.
- **Named opt-in scripts**: Each expensive category has its own script. The script name is the documentation — `pnpm test:meditate` tells you exactly what you're opting into.
- **No `test:all` or `test:expensive` alias**: The user must name what they want to run. This prevents accidental "run everything" invocations.
- **Inline env var**: The script sets the env var as a command prefix, not via `.env` file manipulation. This makes the mechanism explicit and self-contained.

### Orthogonal composition: per-category gates + global deadline

The per-category gate and global deadline are independent protection layers:

| Layer | Type | Protects against |
|-------|------|------------------|
| `SDK_EVAL_SKIP_EXPENSIVE` | Binary (run/skip) | Known-expensive categories running by default |
| `SDK_EVAL_MAX_DURATION_MS` | Continuous (time limit) | Unexpected cost in any test, including non-gated ones |

They compose multiplicatively: a cheap test that unexpectedly becomes expensive (agent enters infinite loop, API returns slow) is bounded by the deadline even though the gate didn't prevent it from running. A gated test that's opted in is still bounded by the deadline. Neither alone is sufficient.

### Config-based feature flags: a parallel pattern

[memory:Plugin design patterns: advisory gates and progressive enhancement defaults] The memory system uses a structurally similar but syntactically different pattern: `enableMemories: "true"` in `.crux/crux-memories.json`, checked as `flags.enableMemories === "true"`. This is an enable-by-explicit-config pattern rather than skip-by-env-var.

The plugin system uses a third variant: `enabledByDefault: boolean` in a JSON registry, overridable by `--plugin X` (explicit inclusion) or `--no-plugin X` (explicit exclusion) CLI flags. Three tiers of override: registry default → CLI flag → per-invocation.

[memory:Session-scope command design: in-band handling and subagent inheritance] The amnesia system adds a fourth layer: a session-scope runtime toggle (`/crux-amnesia on`) that overrides the config-based flag, with subagent inheritance via `alwaysApply` rules. The CRUX rule encodes the precedence explicitly: `Φ.amnesia=session override ≻ enableMemories`.

The full generalized override stack across the repo is: **config default → env-var override → CLI flag override → session-scope override → per-invocation override**. Each layer has different persistence characteristics (permanent, process-scoped, shell-scoped, session-scoped, call-scoped).

## Connections

### The double-negative readability problem is a feature

The `!== "false"` idiom reads as a triple negative: the variable says SKIP, the comparison says NOT, the value says FALSE. But this apparent awkwardness is a feature: the cognitive friction forces readers to slow down and think about what they're opting into. A clean `if (RUN_EXPENSIVE)` is easy to flip without realizing the cost implications. The ugly `!== "false"` makes the decision point conspicuous.

### Package.json scripts as the missing link between gates and CI

The gating pattern has a CI discoverability gap: if a CI pipeline only runs `pnpm test`, expensive tests silently never execute in CI — a safe but potentially dangerous omission (regressions in expensive paths go undetected). The package.json scripts bridge this by providing named targets that CI workflows can explicitly invoke on appropriate schedules (nightly, pre-release). The scripts are the contract between the gating mechanism and the CI configuration.

### Subagent inheritance generalizes the env-var pattern

In production agent harnesses, the equivalent of a process env var is the parent context passed to child agents. The amnesia pattern demonstrates that session-scope flags silently fail to propagate to subagents unless explicit inheritance is implemented. This is structurally identical to the problem of env vars not propagating across process boundaries in CI: a parent CI job sets `SDK_EVAL_SKIP_EXPENSIVE=false`, but a spawned subprocess in a different shell doesn't inherit it unless explicitly forwarded.

### Advisory vs hard gates: a spectrum

[memory:Plugin design patterns: advisory gates and progressive enhancement defaults] The plugin system's `failClosed: false` (advisory) gates occupy a different point on the spectrum from the binary skip/run gates. Advisory gates warn but preserve output; hard gates prevent execution entirely. The skip-by-default pattern is a hard gate (tests don't run at all), but a production agent harness might prefer advisory gating for some operations — warn that an operation is expensive and log the cost, but still execute it. The cost-tier classification should determine which type of gate is appropriate: catastrophically expensive operations get hard gates, moderately expensive ones get advisory gates.

## Summary

Skip-by-default env-var gating (`!== "false"`) is a maximally conservative pattern where only the exact string `"false"` enables execution; every other state (unset, typo, empty) defaults to skip. Its effectiveness depends on multi-channel discoverability (console output, `.env.example`, README, package.json scripts, source comments) because the primary failure mode is not misconfiguration but invisibility — engineers not knowing gated paths exist. The pattern composes orthogonally with global deadlines (per-category binary gates prevent known-expensive operations; continuous time limits catch unexpected expense). Package.json scripts serve as the contract layer between gate mechanisms and CI workflows, encoding opt-in as named aliases that inline the env var. When generalized to production agent harnesses, the pattern extends to a multi-layer override stack (config → env → CLI → session → per-call) with subagent inheritance as the critical propagation mechanism — flags that don't cross agent boundaries silently violate intent, just as env vars that don't cross process boundaries silently skip tests.
