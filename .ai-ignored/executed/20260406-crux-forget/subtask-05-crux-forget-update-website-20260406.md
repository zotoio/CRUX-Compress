# Subtask: Update Website Memories Page

## Metadata
- **Subtask ID**: 05
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01, 02
- **Created**: 20260406

## Objective
Update `web/compress.md/memories.html` to include the `/crux-forget` command in the commands grid and architecture diagram.

## Deliverables Checklist
- [x] `/crux-forget` added to the commands grid in the MindReader section
- [x] Architecture diagram COMMANDS box updated to include `/crux-forget`
- [x] Memory Lifecycle diagram updated if appropriate (Forget is an exit point — memories can be removed at any stage)

## Definition of Done
- [x] `web/compress.md/memories.html` updated with forget command references
- [x] HTML is valid and renders correctly
- [x] No linter errors

## Implementation Notes

### File to Edit
`web/compress.md/memories.html`

### Changes Required

**1. Architecture Diagram — COMMANDS box (lines 46-49):**
The COMMANDS rectangle currently shows two commands. Add `/crux-forget`:

Currently:
```xml
<text x="120" y="70" ... >/crux-dream</text>
<text x="120" y="88" ... >/crux-mindreader</text>
```

Add a third line and adjust the box height to accommodate:
```xml
<text x="120" y="70" ... >/crux-dream</text>
<text x="120" y="88" ... >/crux-mindreader</text>
<text x="120" y="106" ... >/crux-forget</text>
```

The COMMANDS `<rect>` at line 46 has `height="90"` — increase to `height="108"` or similar to fit the third command. Adjust the arrow from COMMANDS to AGENT accordingly if it no longer aligns (the arrow originates at `y1="65"` — may need to shift to ~`y1="73"`).

**2. Commands Grid — MindReader section (lines 749-772):**
Add a new `.memories-command` block for `/crux-forget` after the existing mindreader block:

```html
<div class="memories-command">
  <div class="memories-command-header">
    <code class="memories-command-name">/crux-forget</code>
    <span class="memories-command-desc">Remove memories</span>
  </div>
  <div class="memories-command-usage">
    <div class="memories-command-line"><code>/crux-forget &lt;memory-id&gt;</code><span>Forget a specific memory by ID</span></div>
    <div class="memories-command-line"><code>/crux-forget "query"</code><span>Search and select memories to forget</span></div>
    <div class="memories-command-line"><code>/crux-forget</code><span>List all memories for selection</span></div>
  </div>
</div>
```

**3. Memory Lifecycle Diagram (lines 154-200):**
Consider whether to add a "FORGET" element. The current lifecycle is WORK → DREAM → REM → MINDREADER (circular). Forget is an exit point from the cycle — a user can remove a memory at any point. One approach: add a small "FORGET" element below or to the side with an arrow from MINDREADER (since viewing memories naturally leads to forgetting unwanted ones). This is optional — if it complicates the diagram too much, skip it and just document the command in the grid.

**4. Cross-Platform Support section (lines 816-837):**
The Cursor platform card lists `.cursor/commands/crux-dream.md`. This is a representative example and does not need to list every command. No change needed here unless it explicitly lists all commands.

### SVG Guidelines
- Use the same font families, sizes, and colours as existing elements
- Test that viewBox dimensions still accommodate the new content
- Maintain consistent spacing between elements

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Open the HTML file in a browser to verify rendering
- Verify the new command appears in the grid
- Verify the architecture diagram still renders correctly with the adjusted box
- Check that no existing content was accidentally removed

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask 05)
- Started: 2026-04-07
- Completed: 2026-04-07

### Work Log
1. **Architecture Diagram COMMANDS box**: Increased `<rect>` height from 90 to 108 to fit third command. Added `/crux-forget` as a third `<text>` element at y=106. Arrow from COMMANDS→AGENT at y=65 remains within the enlarged box (y=20 to y=128), no adjustment needed.
2. **Commands Grid**: Added a new `.memories-command` block for `/crux-forget` after the `/crux-mindreader` block. Includes three usage variants: by memory-id, by search query, and interactive listing.
3. **Memory Lifecycle Diagram**: Added a "FORGET" element as a dashed-border rectangle at the right side of the diagram (x=660, y=220). Used red stroke (#e06c75) and dashed pattern to visually distinguish it as an exit ramp. Added a red arrow marker (`lc-arrow-red`) in defs and a dashed arrow from near the REM circle down to the FORGET box with a "forget" label. The element is positioned to avoid overlapping the existing REM→MINDREADER curved arrow.

### Blockers Encountered
None.

### Files Modified
- `web/compress.md/memories.html`

### Adversarial Verification (Judge)
- **Verifier**: zoto-spec-judge
- **Date**: 2026-04-07
- **Verdict**: **Verified**

**Deliverables Checklist — independently confirmed:**
- [x] Architecture diagram COMMANDS box includes `/crux-forget` as third `<text>` element at y=106 (line 50)
- [x] COMMANDS `<rect>` height increased from 90 to 108 to fit third command (line 46)
- [x] Commands grid has `.memories-command` block for `/crux-forget` with 3 usage variants (lines 784-794)
- [x] Memory Lifecycle diagram has FORGET element: dashed-border red rectangle at x=660, y=220 with `/crux-forget` label and red arrow from REM phase (lines 205-210)
- [x] Red arrow marker (`lc-arrow-red`) defined in SVG defs (lines 161-163)

**Definition of Done — independently confirmed:**
- [x] `web/compress.md/memories.html` updated with forget command references
- [x] HTML is valid — proper structure with DOCTYPE, head, body, all tags closed
- [x] No linter errors (verified via ReadLints)

**Additional observations:**
- SVG styling is consistent with existing elements (same font families, colors, sizes)
- FORGET element uses distinctive visual treatment (dashed border, red stroke `#e06c75`) to indicate it's an exit ramp from the lifecycle — good design choice
- No existing content was removed; all original sections intact (914 lines)
