# Subtask: Website — Add CRUX Memories Section

## Metadata
- **Subtask ID**: 04
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Add a CRUX Memories feature section to the website landing page (`web/compress.md/index.html`) so the feature is discoverable. The section should be concise, note the opt-in nature, and link to the README for details.

## Deliverables Checklist
- [x] New "Memories" feature card or section added to `web/compress.md/index.html`
- [x] Content covers: what memories are (learning from completed work), lifecycle (Dream/REM/MindReader), opt-in nature
- [x] Visual style consistent with existing feature cards (rules, images, code, URLs)
- [ ] Link to README memories section for detailed documentation
- [x] Note that memories are disabled by default and require explicit enablement
- [x] Update quickstart install command from `install.sh | bash` to `install.py | python3 -` (lines ~406 and ~414 reference stale `install.sh`)

## Definition of Done
- [x] Website HTML is well-formed (no unclosed tags)
- [x] New section uses existing CSS classes and design patterns
- [x] No JavaScript errors introduced
- [x] Content accurately represents the memories feature as documented in README
- [x] No linter errors in modified files

## Implementation Notes

### Current Website Structure
- `web/compress.md/index.html` (~512 lines)
- Feature cards for: rules, images, code, URLs (with example reduction stats)
- Interactive notation explorer (symbols + blocks table)
- Quickstart section with `install.sh` one-liner and file tree
- Gallery sections for each compression type

### Where to Add Memories Section
- Place after the URL compression section and before the Notation section. Memories is a capability (not a compression type), so it should be visually distinct from the compression cards while still appearing in the feature showcase area.
- Style should match existing cards but clearly indicate this is a different capability (not a compression type)

### Content Guidance
The memories section should convey:
1. **What**: CRUX agents learn from completed work (plans, executions) and store reusable insights
2. **How**: Three modes — Dream (extract learnings), REM Sleep (rebalance/consolidate), MindReader (query)
3. **Opt-in**: Disabled by default; enable via `.crux/crux-memories.json`
4. **Integration**: Works with existing CRUX workflows; memories inform future agent sessions

### What NOT to Change
- Do not add implementation details or configuration specifics
- Keep it concise — the README has full documentation

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Open the HTML file and verify well-formedness visually
- Defer full website verification to subtask 08

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask 04 executor)
- Started: 20260404
- Completed: 20260404

### Work Log
1. Read full HTML structure of `web/compress.md/index.html` and `styles/main.css` to understand design patterns
2. Added new `section--memories` HTML section between URL Compression and Notation sections (lines 208-247)
3. Added CSS styles for `.section--memories`, `.memories-modes` grid, `.memories-mode` cards, `.memories-optin` notice, and `.memories-optin-badge` — uses teal accent (`--accent-verbose`) to visually distinguish from compression type sections which use amber
4. Updated quickstart install command from `install.sh | bash` to `install.py | python3 -` in both `data-copy` attribute and visible `<pre><code>` block
5. Updated prerequisites from `unzip` to `python3`
6. Verified no linter errors in modified files

### Blockers Encountered
None

### Files Modified
- `web/compress.md/index.html` — added memories section, updated install command and prerequisites
- `web/compress.md/styles/main.css` — added memories section CSS styles

### Adversarial Verification (integrity-expert, 20260404)

**Verdict: PARTIAL — 1 item unchecked**

#### Deliverables Verification

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | Memories section added | PASS | `index.html` lines 208-247: `<section id="memories" class="section section--memories">` with Dream/REM/MindReader cards |
| 2 | Content coverage | PASS | Intro text covers what memories are; three mode cards cover Dream, REM Sleep, MindReader; opt-in badge present |
| 3 | Visual consistency | PASS | Uses existing `.section`, `.section-content`, `.section-title`, `.section-intro`, `.spec-link` classes; CSS uses same design tokens (`--bg-tertiary`, `--border-subtle`, `--radius-lg`); teal accent (`--accent-verbose`) intentionally differentiates from compression-type sections |
| 4 | README link | **FAIL** | Link at line 243 targets `README.md#crux-memories` but README heading is `## Memories` (line 574), generating anchor `#memories`. The link will land on the README page but will NOT scroll to the correct section. Fix: change `#crux-memories` to `#memories` |
| 5 | Opt-in noted | PASS | Lines 238-241: "Memories are disabled by default. Enable via `.crux/crux-memories.json`" — matches README wording |
| 6 | Install command updated | PASS | `data-copy` attribute (line 447) and `<pre><code>` block (line 455) both use `install.py \| python3 -`; prerequisites updated to `python3` (line 442) |

#### Definition of Done Verification

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | Well-formed HTML | PASS | All tags in memories section (lines 208-247) properly opened and closed; document structure intact |
| 2 | Existing CSS classes | PASS | New CSS (main.css lines 1766-1864) follows established patterns; responsive breakpoint at 768px consistent with other sections |
| 3 | No JS errors | PASS | No JavaScript added; memories section is pure HTML/CSS; existing script references unchanged |
| 4 | Content accuracy | PASS | Dream/REM Sleep/MindReader descriptions match README § Memories; opt-in mechanism matches README § Enabling Memories |
| 5 | No linter errors | PASS | `ReadLints` on both files returned zero errors |

#### Required Fix
- `web/compress.md/index.html` line 243: Change `README.md#crux-memories` → `README.md#memories` to match the actual GitHub-generated anchor for `## Memories`
