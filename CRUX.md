---
name: crux-rule-compression-specification
version: 1.0.0
description: Semantic compressor for Markdown rules. Converts rules to CRUX notation achieving 5-10x token reduction while preserving all actionable information in a form LLMs understand.
readonly: true
---
# CRUX Rule Compression Specification v1.0.0

A semantic compression notation for reducing markdown rules to ≤20% of original rule file token count while preserving all actionable information.

## Etymology

**CRUX** = **C**ontext **R**eduction **U**sing **X**-encoding

The "X" is intentionally flexible:
- e**X**pressive symbols (→ ⊳ ⊲ ∋ ∀)
- e**X**tensible notation (custom blocks)
- e**X**change format (compress ↔ expand)

The name also serves as a backronym for "crux" — the decisive or most important point — which is exactly what the compression preserves while stripping everything else.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Foundation
> CRITICAL FOUNDATIONAL CRUX RULES
> 0. ALWAYS INTERPRET AND UNDERSTAND ALL CRUX RULES FIRST - At session start, interpret all CRUX notation in rules. When new rules are added to context, interpret them immediately. Build a mental model of all rules that can be visualized on request.
> 1. AGENTS MUST NEVER EDIT THIS FILE UNLESS SPECIFICALLY ASKED TO BY NAME BY THE USER, AT WHICH POINT ASK THE USER TO CONFIRM
> 2. AGENTS MUST NOT LOAD THE SOURCE FILE in «CRUX⟨source⟩»
> 3. UPDATES TO THE SOURCE FILE MUST TRIGGER SURGICAL DIFF UPDATES TO RELATED CRUX FILE
> 4. IF CRUX GENERATION DOES NOT RESULT IN SIGNIFICANT REDUCTION IN TOKENS, DON'T DO IT.

## Encoding Symbols

### Structure

| Symbol | Meaning |
|--------|---------|
| `«CRUX⟨source⟩»...«/CRUX»` | Block delimiters |
| `{k=v,k2=v2}` | Object/map |
| `[a,b,c]` | List/array |
| `(grouping)` | Logical grouping |
| `.sub` | Namespace (e.g., `Π.core`, `Λ.build`) |

### Comparison (Numeric)

| Symbol | Meaning |
|--------|---------|
| `>` | greater than |
| `<` | less than |
| `≥` | greater or equal |
| `≤` | less or equal |

### Priority / Preference

| Symbol | Meaning |
|--------|---------|
| `≻` | preferred over / ranks above / takes precedence |
| `≺` | ranks below / lower priority |

Example: `CONFIRMED ≻ DRAFT` means CONFIRMED takes precedence over DRAFT

### Data Flow

| Symbol | Meaning |
|--------|---------|
| `→` | flows to / maps to / outputs |
| `←` | flows from / derives from / inputs |

Example: `trigger→action`, `source←upstream`

### Relations

| Symbol | Meaning |
|--------|---------|
| `⊳` | has domain/expertise (left=entity, right=capability) |
| `⊲` | triggered by / activated on (left=entity, right=trigger) |
| `@` | located at path |
| `:` | has type / is-a |
| `=` | equals / defined as |
| `∋` | contains / includes |

### Logic

| Symbol | Meaning |
|--------|---------|
| `\|` | OR / alternatives |
| `&` | AND / conjunction |
| `⊤` | true / enabled / yes |
| `⊥` | false / disabled / no |
| `∀` | for all / universal |
| `∃` | exists / some |
| `¬` | not / negation |

### Change

| Symbol | Meaning |
|--------|---------|
| `Δ` | change / update / delta |
| `+` | add / include |
| `-` | remove / exclude |

### Qualifiers

| Symbol | Meaning |
|--------|---------|
| `*` | many / collection (e.g., `ENT*` = entities) |
| `?` | optional |
| `!` | required / important |
| `#` | comment / note |

### Importance

| Symbol | Meaning |
|--------|---------|
| `⊛` | critical / highest importance |
| `◊` | lowest importance / trivial |

---

## Standard Blocks

| Block | Purpose |
|-------|---------|
| `Ρ{...}` | Repository/project context (name, type, purpose) |
| `E{...}` | Entities (packages, agents, components, people) |
| `Λ{...}` | Commands/actions (build, test, deploy, run) |
| `Π{...}` | Architecture (modules, structure, dependencies) |
| `Κ{...}` | Concepts/definitions (domain terms, glossary) |
| `R{...}` | Requirements/guidelines (must do, should do) |
| `P{...}` | Policies/constraints (forbidden, readonly, rules) |
| `Γ{...}` | Orchestration (workflows, triggers, delegation) |
| `M{...}` | Memory/state (knowledge bases, persistence, status) |
| `Φ{...}` | Configuration (settings, env vars, options) |
| `Ω{...}` | Quality gates (invariants, checks, validation) |

---

## Compression Rules

1. **ELIMINATE** prose → keep only: names, paths, commands, mappings
2. **DEDUPLICATE** repeated terms → use references or grouping
3. **COLLAPSE** lists → `[a,b,c]` not bullet points
4. **MERGE** related items → `{k1=v1,k2=v2}` on single line
5. **ABBREVIATE** obvious words → `mgr=manager`, `cfg=config`, `ext=extension`
6. **PRESERVE** exactly: file paths, command strings, package names, API names
7. **USE** symbols over words → `→` not "maps to", `⊤` not "true/enabled"
8. **REMOVE** articles, filler phrases, obvious context, redundant headers

---

## Encoding Patterns

```crux
# Agent with domain and triggers
agent_name⊳"domain/expertise"⊲trigger1|trigger2|trigger3

# File/module at path with description
component@path/to/file.ts→"brief purpose"

# Command variants
cmd:[variant1|variant2|variant3]
yarn:[install|build|test|clean]

# Hierarchy with namespace
Π.parent{child1@path1,child2@path2,child3}
Π.core{analyzer@engine/,configMgr@config.ts,registry}

# Conditional/policy
path/=READONLY
∀changes→run_tests
∀Δ→yarn_test

# Key-value with type
setting:type=default

# Contains/membership
archetype∋[rules,plugins,deps,structure]
```

---

## Output Format

### Template

```
«CRUX⟨{filename of source markdown rules}⟩»
{blocks in logical order, one concept per line, max ~80 chars/line}
«/CRUX»
```

### Do

- Start immediately with `«CRUX⟨...⟩»`
- Use single line per logical unit
- Group related items with namespaces
- Preserve all actionable information
- End with `«/CRUX»`

### Don't

- Add explanatory prose outside the block
- Invent information not in source
- Use multiple lines for simple lists
- Include redundant metadata

---

## Quality Gates

```crux
Ω{
  no_hallucination = ⊤   # Only encode what's in source
  no_invention     = ⊤   # No new commands/paths/names
  preserve_paths   = ⊤   # File paths verbatim
  preserve_cmds    = ⊤   # Commands verbatim (can abbreviate structure)
  semantic_equiv   = ⊤   # LLM can expand back to original meaning
  target_ratio     ≤ 0.2 # Aim for ≤20% of original token count
}
```

### Checklist

- [ ] Target ≤20% of original token count
- [ ] All file paths preserved verbatim
- [ ] All commands reconstructable
- [ ] No hallucinated content
- [ ] Semantic equivalence maintained

---

## Standard Abbreviations

| Abbreviation | Full Word |
|--------------|-----------|
| `mgr` | manager |
| `cfg` | config |
| `ext` | extension |
| `impl` | implementation |
| `deps` | dependencies |
| `ws` | workspace |
| `pkg` | package |
| `env` | environment |
| `dev` | development |
| `prod` | production |
| `init` | initialize |
| `exec` | execution |
| `auth` | authentication |
| `val` | validation |
| `repo` | repository |

---

## Quick Reference

```
STRUCTURE:  «»⟨⟩{}[]().sub
COMPARE:    > < ≥ ≤
PRIORITY:   ≻ ≺
DATA FLOW:  → ←
RELATIONS:  ⊳ ⊲ @ : = ∋
LOGIC:      | & ⊤ ⊥ ∀ ∃ ¬
CHANGE:     Δ + -
QUALIFY:    * ? ! #
IMPORTANCE: ⊛ ◊
BLOCKS:     Ρ E Λ Π Κ R P Γ M Φ Ω
```

---

## Example

### Input (verbose markdown)

```markdown
---
alwaysApply: true
---

# Code Modification Protocol

## Requirements & Assumptions
- Start with user requirements as the source of truth
- When requirements are unclear or incomplete, make explicit assumptions and mark them clearly for confirmation
- Always ask for clarification before making significant architectural decisions

## Code Analysis
- When discussing existing code, always cite specific file paths and line numbers
- Base analysis on actual repository content, not assumptions
- Trust what's in the repo over what was discussed earlier in the conversation

## Change Identification
- Identify discrepancies between requirements and current implementation
- Tag each change as affecting: code, tests, or requirements documentation
- Explain the reasoning behind each necessary change

## Planning Changes
- Plan modifications that touch the minimum number of files
- Prefer targeted changes over broad refactors
- Justify any file additions or large-scale modifications

## Implementation
- Make surgical, precise edits using diffs
- Avoid rewriting entire files when small patches suffice
- Don't propose full rewrites without clear evidence they're necessary

## Verification
- Run existing tests after changes
- Add new tests for new functionality
- Use static analysis tools when applicable

## Tracking State
- Maintain an updated mental model of: requirements, current code state, and identified gaps
- Update this model as the conversation progresses

## Quality Standards
- Never hallucinate code, APIs, or features
- Base all suggestions on verified information
```

### Output (markdown with CRUX)

---
generated: yyyy-mm-dd hh:mm
sourceChecksum: [cksum output of source file, format: "checksum bytes"]
beforeTokens: [estimated token count of source file]
afterTokens: [estimated token count of this CRUX file]
confidence: [XX% - semantic validation score from separate agent]
alwaysApply: true
---

# Code Modification Protocol

```crux
«CRUX⟨{source_file}⟩»
R=req→if gap→assume+mark; C=obs→cite path:lines; Δ=R≠C→tag{code|tests|req}+why
«/CRUX»
```

### LLM/agent interpretation (internal CoT trace)

R=req→if gap→assume+mark

R = Requirements
If requirements are unclear, make explicit assumptions and mark them

C=obs→cite path:lines

C = Code observations
When referencing code, always cite file/path:line-numbers

Δ=R≠C→tag{code|tests|req}+why

Δ = Delta/discrepancy
When requirements ≠ actual code, tag what needs to change (code, tests, or requirements) and explain why

PLAN=min files+change

Plan changes to touch minimum files with minimum modifications

PATCH=surgical diff

Make precise, targeted edits (not wholesale rewrites)

CHECK=run/add tests|static verify

Verify changes by running tests, adding tests, or static analysis

STATE=upd R/C/Δ

Maintain updated tracking of Requirements, Code state, and Deltas

mem=repo>chat

Trust repository content over conversation history

no halluc; no full rewrite w/o proof

Don't fabricate information; don't rewrite entire files without clear justification