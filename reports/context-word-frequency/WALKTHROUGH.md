# Context word-frequency analysis — walkthrough and report

This document records how the **word counts for the agent context** were produced, what corpus they reflect, and where the interactive and video outputs live.

## Goal

Answer: *“For the text that models this chat session’s injected context, what is each word’s frequency, sorted descending?”*

The full runtime context also includes large generic system and tool schemas. Those are **not** represented as a single file in the repository, so they were **excluded** from the corpus to keep the analysis grounded in **project-local, reproducible sources**.

## Corpus (what was counted)

1. **Always-applied Cursor rules (compressed `.mdc`)**  
   - `.cursor/rules/_CRUX-RULE.mdc`  
   - `.cursor/rules/crux-memories-integration.crux.mdc`  
   - `.cursor/rules/docs-sync.crux.mdc`  
   - `.cursor/rules/zip-contents-protection.crux.mdc`  
   - `.cursor/rules/version-bump.crux.mdc`

2. **`AGENTS.md`** at the repository root (duplicated in part in the injected `cloud_instructions` block).

3. **Session-injected text** reproduced verbatim from the prior turn’s context (summarized as labels here):  
   `user_info`, `git_status`, requestable-rule pointer, `cloud_task_instructions` excerpt, skill file paths, subagent type names, full `user_rules`, and the `background_agent` note.

## Tokenization

- **ASCII tokens:** contiguous runs of `[A-Za-z0-9_]` plus optional English apostrophe suffixes (e.g. `I'll`), then **lowercased**.  
- **Greek letters** (Unicode blocks U+0370–03FF and U+1F00–1FFF): kept as separate tokens (CRUX notation in the rules).  
- **Not split:** hyphenated compounds stay as one token if there is no separator matching the pattern above.

## Process (reproducible)

1. Concatenate the corpus sections in a fixed order (rules → `AGENTS.md` → inline session text).  
2. Run the tokenizer regular expression over the full string.  
3. Count with `collections.Counter`, sort by descending count.  
4. Emit `data.json` via:

   ```bash
   python3 reports/context-word-frequency/generate_data.py
   ```

## Results (summary)

| Metric | Value |
|--------|------:|
| Total tokens | 2,570 |
| Unique words | 864 |
| Top token | `crux` (101) |

The machine-readable full ranking is in `data.json`. The interactive page charts the **top 24** terms and lists the full table with search.

## Deliverables in this folder

| File | Purpose |
|------|---------|
| `WALKTHROUGH.md` | This narrative (analysis + interpretation). |
| `generate_data.py` | Regenerates `data.json` from the repo + inline corpus. |
| `data.json` | Full word list, stats, corpus metadata. |
| `report.html` | Self-contained page: **SVG** bar chart, **WebGPU** animated panel (with graceful fallback), sortable/searchable table. |
| `walkthrough.mp4` | Short **video** walkthrough (ffmpeg titled slides). |
| `render_walkthrough_video.sh` | Regenerates `walkthrough.mp4` (requires ffmpeg + DejaVu fonts). |
| `build_report.py` | Embeds `data.json` into `report.html` for offline `file://` use. |

## Interpretation notes

- High counts for **`crux`**, **`md`**, **`cursor`**, **`file`**, **`rule`**, **`skill`** reflect the repository’s CRUX/Cursor rule content, not general English prose.  
- Tokens like **`Δ`**, **`Κ`**, **`Γ`** appear because CRUX-encoded rules use Greek symbols as structured markers.  
- **`sourcechecksum`**, **`alwaysapply`**, etc. come from YAML front matter in generated rule files.  
- **`user`**, **`must`**, **`not`** are elevated by both AGENTS.md and the long `user_rules` block.

## Limitations

- **Not** a full dump of the model’s entire context window (tool specs, hidden system prompts, etc.).  
- Tokenization is **heuristic**; different tokenizers (model BPE, etc.) would yield different splits.  
- The **inline session** block is a snapshot; if injection text changes, re-run `generate_data.py` and rebuild the HTML/video.
