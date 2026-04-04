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
- [ ] New "Memories" feature card or section added to `web/compress.md/index.html`
- [ ] Content covers: what memories are (learning from completed work), lifecycle (Dream/REM/MindReader), opt-in nature
- [ ] Visual style consistent with existing feature cards (rules, images, code, URLs)
- [ ] Link to README memories section for detailed documentation
- [ ] Note that memories are disabled by default and require explicit enablement

## Definition of Done
- [ ] Website HTML is well-formed (no unclosed tags)
- [ ] New section uses existing CSS classes and design patterns
- [ ] No JavaScript errors introduced
- [ ] Content accurately represents the memories feature as documented in README
- [ ] No linter errors in modified files

## Implementation Notes

### Current Website Structure
- `web/compress.md/index.html` (~512 lines)
- Feature cards for: rules, images, code, URLs (with example reduction stats)
- Interactive notation explorer (symbols + blocks table)
- Quickstart section with `install.sh` one-liner and file tree
- Gallery sections for each compression type

### Where to Add Memories Section
- After the existing compression type cards (rules/images/code/URLs)
- OR as a new section before the quickstart
- Style should match existing cards but clearly indicate this is a different capability (not a compression type)

### Content Guidance
The memories section should convey:
1. **What**: CRUX agents learn from completed work (plans, executions) and store reusable insights
2. **How**: Three modes — Dream (extract learnings), REM Sleep (rebalance/consolidate), MindReader (query)
3. **Opt-in**: Disabled by default; enable via `.crux/crux-memories.json`
4. **Integration**: Works with existing CRUX workflows; memories inform future agent sessions

### What NOT to Change
- Do not modify the install command on the website (that's a separate concern)
- Do not add implementation details or configuration specifics
- Keep it concise — the README has full documentation

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Open the HTML file and verify well-formedness visually
- Defer full website verification to subtask 08

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
