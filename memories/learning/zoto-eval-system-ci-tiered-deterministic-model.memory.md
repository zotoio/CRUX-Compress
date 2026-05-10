---
id: "06531e8"
title: "Zoto eval system CI integration follows tiered deterministic-first model"
description: "The Zoto eval system supports a tiered CI model: static evals gate PRs, LLM evals run on schedule, and eval:update --check detects drift deterministically (exit code 2) to safely gate PRs."
type: "learning"
strength: 1
created: 2026-05-10
modified: 2026-05-10
source: "adhoc"
tags: [ci, evals, zoto, pipeline, drift-detection, automation]
---

# Zoto Eval System CI Integration — Tiered Deterministic-First Model

A 3-tier strategy for embedding evals in CI pipelines, with specific guidance for the Zoto eval system.

## Tier 1: Static Evals on Every Push/PR (Gate PRs)

Keep pytest-based static evals running on every push and PR. These are cheap, deterministic, and safe to gate merges on. They validate structure, schemas, and invariants without calling LLMs.

## Tier 2: SDK/LLM Evals on Schedule (Never Gate PRs)

Run LLM-backed SDK evals as scheduled workflows (e.g. nightly) plus manual `workflow_dispatch` for on-demand runs. These are non-deterministic and costly — they should never block PR merges. Always upload artifacts so results are inspectable after runs complete.

## Tier 3: Lightweight SDK Smoke Test on PR (Optional, Label-Gated)

Optionally add a minimal SDK smoke test that runs on PRs only when a specific label (e.g. `run-sdk-evals`) is applied. Keep it to 1-2 fast tests with aggressive timeouts. This provides on-demand LLM eval feedback without blocking the default merge path.

## Zoto Eval System Integration

If the Zoto eval system is configured (`.zoto/eval-system/config.yml`), the same tiered model applies:

- **Static evals** in the PR gate — safe, deterministic
- **LLM evals** on schedule — non-deterministic, informational only
- **`eval:update --check`** can gate PRs since it's deterministic (exit code 2 on critical drift) — it detects when covered targets have drifted from their generated eval cases without invoking any LLM

## Key Principles

- Never gate merges on LLM eval results — non-determinism causes flaky CI
- Run LLM evals on schedule to catch regressions over time
- Always upload eval artifacts for post-run inspection
- Use `workflow_dispatch` for on-demand eval runs with suite filtering
- Set aggressive timeouts on all eval jobs to prevent runaway costs
- `eval:update --check` is the one Zoto-specific command safe for PR gating because it's purely deterministic (file diff + exit code)
