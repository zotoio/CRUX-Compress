# Subtask 08 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 08 |
| feature | context-token-reduction |
| assigned_agent | crux-software-engineer |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13T19:18:00+10:00 |
| last_heartbeat | 2026-07-13T19:38:40+10:00 |
| completed_at | 2026-07-13T19:37:30+10:00 |
| git_sha | 7f81a121f9906dba980d8d293e6f6225b4c95ad8 |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — Lazy-CRUX enforcement eval: (`evals/test_s_context_reduction.py`)
- [x] **D02** — **D02** — `context_manifest` honor eval: (`evals/test_s_context_reduction.py`)
- [x] **D03** — **D03** — Template lazy-load eval: (`evals/test_s_context_reduction.py`)
- [x] **D04** — **D04** — Memory-manager split eval: (`evals/test_s_context_reduction.py`)
- [x] **D05** — **D05** — Compressed-primitive semantic parity eval: (`evals/fixtures/crux-compressed/`)
- [x] **D06** — **D06** — `/crux-test` shim eval: (`evals/test_s_context_reduction.py`)
- [x] **D07** — **D07** — CI wiring: (`pytest.ini`)
- [x] **D08** — **D08** — Baseline vs post-spec token-cost measurement: (`evals/reports/context-token-reduction-baseline.md`)
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **modified** `evals/test_s_context_reduction.py` — Honest LLM skip + D04 .source.mdx scan + optional CRUX_LLM_RESULT injection
- **modified** `.cursor/commands/crux-meditate.source.mdx` — Related: umbrella → thin agents; loadable recompress deferred (KD-2)
- **created** `evals/fixtures/crux-compressed/` — 8 must-preserve fixtures for Wave 1+2
- **created** `evals/reports/context-token-reduction-baseline.md` — D08 token-cost report
- **modified** `pytest.ini` — context_reduction_smoke marker
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
## Re-verify after fix_list (judge Mode 1) — 2026-07-13T19:38

### Prior fix_list — confirmed fixed
- **D02**: `_try_invoke_llm_parity` / `_skip_if_no_llm_harness` present.
  `CRUX_LLM_EVAL=1` alone → 9 skipped; with `CRUX_LLM_RESULT_JSON` → 1 passed.
- **D04**: Scan covers `*.md` + `*.source.mdx`; SoT Related lists thin agents;
  `rg crux-cursor-memory-manager .cursor/commands/` → 0 matches (SoT + loadable).
- **D05**: Same honest-skip / optional-injection for `TestCompressedPrimitiveParityLLM`.

### KD-2 note (not a DoD/false-green gap)
- `crux-meditate.source.mdx` SoT checksum now `2429874930` vs loadable
  `sourceChecksum: "857180073"` (recompress deferred).
- Loadable Related is `M.related{…_memory-shared…}` and does **not** name the
  umbrella; D04 invariant holds on both surfaces — no false eval green.
- Flag deferred for Subtask 07 hygiene / future recompress; does not fail DoD.

### Independent verification
- `pytest evals/test_s_context_reduction.py -m "not llm_driven"` → 92 passed
- `scripts/test.py` → 863 passed, 11 skipped (exit 0)
- Templates, fixtures, baseline report, thin agents, shims, CI (`pytest evals/`) OK

<!-- status:notes:end -->
