<CRUX agents="always>
## CRITICAL: CRUX Notation

This repository uses CRUX notation for semantic compression. **Load `CRUX.md` from the project root** to understand the encoding symbols and decompress any CRUX-formatted content you encounter.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

### Foundational CRUX Rules (MUST FOLLOW)

0. **ALWAYS INTERPRET AND UNDERSTAND ALL CRUX RULES FIRST** - At the beginning of each agent session, interpret and understand all crux notation detected in rules, and when a new rule(s) is added to context do the same for the new rule(s) immediately. Build a mental model of all rules in context that the user can ask for at any point in time that will include a visualisation.
1. **NEVER EDIT `CRUX.md`** - The specification is read-only unless the user specifically asks you by name to edit it, at which point ask the user to confirm before proceeding
2. **DO NOT LOAD SOURCE FILES when CRUX exists** - When you see `«CRUX⟨source_file⟩»`, use the compressed CRUX content instead of loading the original source file. The CRUX version is semantically equivalent and more token-efficient.
3. **SURGICAL DIFF UPDATES** - When updating a source file that has a corresponding `.crux.mdc` file, you MUST also update the CRUX file with surgical diff changes to maintain synchronization.
4. **ABORT IF NO SIGNIFICANT REDUCTION** - If CRUX compression does not achieve significant token reduction (target ≤20% of original), DO NOT generate the CRUX file. The source is already compact enough.
</CRUX>