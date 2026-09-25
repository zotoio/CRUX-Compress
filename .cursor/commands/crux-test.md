# crux-test

Run the CRUX command suite via pytest. Test cases live in
`evals/test_r_crux_command_suite.py`; LLM-driven scenarios are marked
`llm_driven` and skipped by default in CI.

## Usage

| Command | Description |
|---------|-------------|
| `python3 scripts/run_crux_command_suite.py` | All deterministic tests |
| `python3 scripts/run_crux_command_suite.py --smoke` | Fast CI smoke subset |
| `python3 -m pytest evals/test_r_crux_command_suite.py -m crux_command_smoke -v` | Smoke, verbose |

## Historical Scenario → Pytest Mapping

| Historical /crux-test scenario | Pytest class |
|-------------------------------|--------------|
| 1 — Compression Test | `TestCompressionRoundtrip` |
| 2 — Decompression Test | `TestDecompressionUnderstanding` *(llm_driven)* |
| 3 — Token Estimation Test | `TestTokenEstimation` |
| 4 — Checksum Test | `TestChecksumDeterminism` |
| 5 — Install Script Test | `TestInstallScript` |
| 6 — Semantic Validation Test | `TestSemanticValidation` *(llm_driven)* |
| 7 — Special Characters Test | `TestSpecialCharacters` |
| 8 — Crux-Compress Command Test | `TestCruxCompressWorkflow` |
| 9 — Semantic Stability / Drift Detection | `TestSemanticStabilityDriftDetection` |
| 10 — Force Recompression Test | `TestForceRecompression` |
