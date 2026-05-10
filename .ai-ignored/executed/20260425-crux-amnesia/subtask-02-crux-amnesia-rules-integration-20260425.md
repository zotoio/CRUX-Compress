# Subtask: Rules Integration

## Metadata
- **Subtask ID**: 02
- **Feature**: crux-amnesia
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Define the amnesia override section within the CRUX memories integration rule (`.cursor/rules/crux-memories-integration.md`) and ensure the CRUX-compressed version (`.crux.mdc`) includes the corresponding `Φ.amnesia` block. This rule is always-applied and governs all agent behavior regarding memory usage, making it the authoritative source for amnesia semantics.

## Deliverables Checklist
- [x] "Session Override: `/crux-amnesia`" section exists in `.cursor/rules/crux-memories-integration.md`
- [x] Section specifies amnesia as a chat-session-only override
- [x] Section states amnesia takes precedence over `enableMemories: "true"`
- [x] Section lists all suppressed behaviors: discovery, loading, annotation, reference tracking, dream nudges
- [x] Section states subagents inherit amnesia state for ordinary work
- [x] Section explicitly prohibits modification of config, memory files, trackers, and index
- [x] Section lists all five explicit memory commands as exceptions to amnesia
- [x] CRUX-compressed file `.cursor/rules/crux-memories-integration.crux.mdc` includes `Φ.amnesia` block
- [x] Compressed `Φ.amnesia` block correctly encodes: session override, suppression list, subagent inheritance, explicit command exceptions, and state protection

## Definition of Done
- [x] Source file `.cursor/rules/crux-memories-integration.md` contains the amnesia section
- [x] Amnesia section appears before the "When Memories Are Enabled" section (override takes precedence)
- [x] All five exception commands listed: `/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget`
- [x] CRUX-compressed rule regenerated with `Φ.amnesia` block
- [x] No linter errors in either file

## Implementation Notes
- The amnesia section is positioned immediately after the rule title and introductory paragraph, before `Φ.enabled` and `Φ.disabled`. This ordering reflects the override precedence: amnesia > enabled > disabled
- The source file uses natural language; the compressed version uses CRUX phase notation (`Φ.amnesia`)
- The `Φ.amnesia` block in the compressed rule encodes the full behavioral contract in approximately 4 lines of CRUX notation, covering: session scope, suppression list, subagent inheritance, explicit command exceptions, and state protection
- The rule is `alwaysApply: true`, meaning every agent session loads it — ensuring amnesia behavior is consistently enforced across all agents

### CRUX Compression Details
The compressed `Φ.amnesia` block maps to the following semantic structure:
```
Φ.amnesia{/crux-amnesia=session override ≻ enableMemories;
 suppress[discover,load,annotate,refs,dream-nudge]; ¬Δ cfg|files|trackers|idx;
 subagents→inherit; explicit /crux-dream|recall|remember|meditate|forget→user intent OK}
```

Key symbols:
- `≻` = takes precedence over
- `¬Δ` = never modify
- `→inherit` = subagents inherit the state
- `→user intent OK` = explicit invocation overrides amnesia

## Testing Strategy
- Verify amnesia section exists in the source rule file
- Verify `Φ.amnesia` block exists in the compressed rule file
- Grep for all five exception commands in both files
- Verify the source file's frontmatter includes `alwaysApply: true`
- Verify the compressed file carries the `> [!IMPORTANT] > Generated file - do not edit!` banner

## Execution Notes

### Reverse-Engineered From
- `.cursor/rules/crux-memories-integration.md` (source, current state as of 20260425)
- `.cursor/rules/crux-memories-integration.crux.mdc` (compressed, current state as of 20260425)

### Key Implementation Details
1. The amnesia section in the source file is 7 bullet points covering the complete behavioral contract
2. The compressed rule uses `Φ.amnesia` as one of three phase blocks (`Φ.amnesia`, `Φ.enabled`, `Φ.disabled`)
3. The exception list was updated in this session to include `/crux-remember` and `/crux-meditate` (previously only `/crux-dream`, `/crux-recall`, `/crux-forget`)
4. The rule file uses `crux: true` in its frontmatter, enabling automatic CRUX compression via the detect-changes hook

### Files Covered
- `.cursor/rules/crux-memories-integration.md` (source)
- `.cursor/rules/crux-memories-integration.crux.mdc` (generated)
