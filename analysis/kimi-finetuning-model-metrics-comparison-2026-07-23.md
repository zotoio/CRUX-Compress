# Kimi Finetuning Process — 3-Model Metrics Comparison

Comparison of three parallel Cursor Cloud Agent runs on the same task: document the Kimi open-weights fine-tuning process and report prompt-execution metrics. All runs started at **2026-07-23 09:07:09 UTC** on `github.com/zotoio/CRUX-Compress`.

---

## Run Overview

| | **Grok 4.5 High** | **Composer 2.5** | **Opus 4.8 Thinking High** |
|---|---|---|---|
| **Run ID** | [bc-36c6d5ca](https://cursor.com/agents/bc-36c6d5ca-7cad-4e57-be58-8e19bc1d5fa3) | [bc-172c856e](https://cursor.com/agents/bc-172c856e-fd5e-408a-9561-1bc8c707304f) | [bc-8e825890](https://cursor.com/agents/bc-8e825890-b26f-42ce-bb7b-bc7876763c1a) |
| **Model slug** | `cursor-grok-4.5-high` | `composer-2.5` | `claude-opus-4-8-thinking-high` |
| **Started (UTC)** | 2026-07-23 09:07:09 | 2026-07-23 09:07:09 | 2026-07-23 09:07:09 |
| **Status** | IDLE (success) | IDLE (success) | IDLE (success) |
| **Code changes / PR** | None | None | None |

---

## Execution Metrics (Primary Comparison)

| Metric | **Grok 4.5 High** | **Composer 2.5** | **Opus 4.8 Thinking High** |
|---|---|---|---|
| **Wall-clock duration** | **104.4 s** (~1.7 min) | **67.9 s** (~1.1 min) | **71.0 s** (~1.2 min) |
| **Tool calls** | **8** | **7** | **1** recorded (agent claimed 2) |
| **Tool wall time** | 9.1 s | 9.4 s | 4.6 s |
| **Transcript messages** | 24 (16 asst, 8 tool) | 19 (12 asst, 7 tool) | 4 (3 asst, 1 tool) |
| **Final response size** | 7,885 chars | **11,109 chars** | 9,278 chars |
| **Est. total tokens** | 28k–40k | **70k–85k** | ~30k |
| **Est. input tokens** | 25k–35k | 65k–78k | ~28k |
| **Est. output tokens** | 3.5k–5k | 5k–7k | ~2.4k |
| **Est. cost (USD)** | $0.05–0.11 | **$0.04–0.06** | $0.11–0.21 |
| **Mid-point cost est.** | ~$0.06–0.08 | ~$0.05 | ~$0.11–0.20 |

> **Note:** Wall-clock duration is from run metadata (`createdAtMs` → `lastMessageActivityAtMs`). Token counts and costs are agent estimates — Cursor does not expose per-run billed tokens in the Cloud Agent API.

---

## Tool Usage Breakdown

| Tool type | **Grok 4.5** | **Composer 2.5** | **Opus 4.8** |
|---|---|---|---|
| `web_search` | 2 | 2 | 1 |
| `mcp` (cursor-cloud) | 2 | 2 | 0 |
| `run_terminal_cmd` | 3 | 1 | 0 |
| `read_file` | 1 | 1 | 0 |
| `grep` | 0 | 1 | 0 |
| `get_mcp_tools` | 1 | 0 | 0 |

### Tool duration detail (Grok 4.5)

| Tool | Count | Total (ms) | Avg (ms) |
|---|---|---|---|
| `web_search` | 2 | 8,278 | 4,139 |
| `run_terminal_cmd` | 3 | 540 | 180 |
| `get_mcp_tools` | 1 | 187 | 187 |
| `read_file` | 1 | 68 | 68 |
| `mcp` | 1 | 31 | 31 |

---

## Pricing Basis (Cursor Models Pool)

| Model | Input / M | Cache read / M | Output / M |
|---|---|---|---|
| Grok 4.5 | $2.00 | $0.50 | $6.00 |
| Composer 2.5 | $0.50 | $0.20 | $2.50 |
| Opus 4.8 | $5.00 | $0.50 | $25.00 |

---

## Task & Outcome (All Three)

| Aspect | All three runs |
|---|---|
| **Task** | Document Kimi open-weights fine-tuning (LoRA SFT via LLaMA-Factory + KTransformers) and report prompt-execution metrics |
| **Actual Kimi training** | None — research/documentation only |
| **Outcome** | All succeeded; no repo changes |
| **Guide depth** | 7–11 documented phases/steps each |

---

## Kimi Fine-Tuning Content Summary

All three agents produced similar guidance. Key points converged across runs:

- **Checkpoint:** Use `moonshotai/Kimi-K2-Base` (not Instruct) for fine-tuning
- **Strategy:** LoRA / QLoRA via PEFT; full-parameter SFT impractical for most teams
- **Stack:** LLaMA-Factory + KTransformers (hybrid CPU/GPU MoE offload)
- **Precision:** Convert shipped INT4/FP8 weights to BF16 before SFT
- **Hardware (minimum):** 2× RTX 4090, x86 with AMX, 1 TB RAM, 600 GB+ NVMe
- **Hardware (recommended):** 4× RTX 4090 or 2–4× H100, 2 TB RAM
- **LoRA defaults:** r=8–16, alpha=32, dropout=0.05–0.1
- **Training:** LR 1e-4–2e-4, 1–3 epochs, effective batch 32–128, BF16
- **Throughput cited:** ~44.55 tokens/s on 2× RTX 4090 + Intel 8488C (KTransformers benchmark)

### Model architecture numbers (cited by agents)

| Property | Value |
|---|---|
| Total parameters | ~1T (MoE) |
| Active parameters per token | ~32B |
| Experts | 384 (8 routed + 1 shared per token) |
| Pretraining tokens | 15.5T |
| Context window | 128K (K2) / 256K (K2.5) |
| Optimizer (pretrain) | MuonClip |
| Base weights size | ~600 GB (INT4) / ~2 TB (BF16) |
| LoRA adapter size | 100–500 MB |

---

## Takeaways

1. **Fastest:** Composer 2.5 at **67.9 s**; Opus close behind at **71.0 s**; Grok slowest at **104.4 s**.
2. **Cheapest:** Composer 2.5 at **~$0.04–0.06**; Grok mid-range; Opus highest at **~$0.11–0.21** (higher per-token rates).
3. **Most verbose output:** Composer 2.5 (**11,109 chars**).
4. **Most tool-heavy:** Grok 4.5 (**8 calls**, including 3 timing shell commands).
5. **Highest token estimate:** Composer 2.5 (**70k–85k**), likely from large system/rule context.
6. **Caveat:** Opus transcript appears truncated (4 messages vs 19–24); its self-reported **3–4 min** conflicts with the **71 s** index duration. Wall-clock from run metadata is the most reliable timing source.

---

## Data Sources

- Run metadata: Cursor Cloud MCP `batch-fetch-details` (2026-07-23)
- Transcripts: `/tmp/cursor/cloud-agent-transcripts/2026-07-23T09-19-57Z-387c/`
- Pricing: Cursor Models pool rates as cited by each agent at time of run
