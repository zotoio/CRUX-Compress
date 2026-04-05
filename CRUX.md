---
name: crux-compression-specification
version: 2.8.5
description: Semantic compressor for markdown, code, and images. Converts source files to CRUX notation achieving 5-10x token reduction while preserving all actionable information in a form LLMs understand.
readonly: true
---
# CRUX Compression Specification v2.5.0

A semantic compression notation for reducing markdown rules, code files, and images to a configurable target percentage (default ≤25%) of original token count while preserving all actionable information.

## Etymology

**CRUX** = **C**ontext **R**eduction **U**sing **X**-encoding

The "X" is intentionally flexible:
- e**X**pressive symbols (→ ⊳ ⊲ ∋ ∀ » ⊕)
- e**X**tensible notation (custom blocks)
- e**X**change format (compress ↔ expand)

The name also serves as a backronym for "crux" — the decisive or most important point — which is exactly what the compression preserves while stripping everything else.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Foundation
> CRITICAL FOUNDATIONAL CRUX RULES
> 0. ALWAYS INTERPRET AND UNDERSTAND ALL CRUX RULES FIRST - At session start, interpret all CRUX notation in rules. When new rules are added to context, interpret them immediately. Build a mental model of all rules that can be visualized on request.
> 1. AGENTS MUST NEVER EDIT THIS FILE UNLESS SPECIFICALLY ASKED TO BY NAME BY THE USER, AT WHICH POINT ASK THE USER TO CONFIRM
> 2. AGENTS MUST NOT LOAD THE SOURCE FILE in ⟦CRUX:source ... ⟧
> 3. UPDATES TO THE SOURCE FILE MUST TRIGGER SURGICAL DIFF UPDATES TO RELATED CRUX FILE
> 4. IF CRUX GENERATION DOES NOT RESULT IN SIGNIFICANT REDUCTION IN TOKENS, DON'T DO IT.

## Encoding Symbols

### Structure

| Symbol | Meaning |
|--------|---------|
| `⟦CRUX:source ... ⟧` | Block delimiters (source file reference after colon) |
| `{k=v,k2=v2}` | Object/map |
| `[a,b,c]` | List/array |
| `(grouping)` | Logical grouping |
| `.sub` | Namespace (e.g., `Π.core`, `Λ.build`) |
| `;` | Statement separator (multiple clauses on one line) |

### Comparison (Numeric)

| Symbol | Meaning |
|--------|---------|
| `>` | greater than |
| `<` | less than |
| `≥` | greater or equal |
| `≤` | less or equal |
| `≠` | not equal |
| `..` | range / to (e.g., `20..30` = 20 to 30) |

### Priority / Preference

| Symbol | Meaning |
|--------|---------|
| `≻` | preferred over / ranks above / takes precedence |
| `≺` | ranks below / lower priority |

Example: `CONFIRMED ≻ DRAFT` means CONFIRMED takes precedence over DRAFT

### Data Flow

| Symbol | Meaning |
|--------|---------|
| `→` | flows to / maps to / outputs / conditional then |
| `←` | flows from / derives from / inputs |

Example: `trigger→action`, `source←upstream`, `∀changes→run_tests`

### Sequence

| Symbol | Meaning |
|--------|---------|
| `»` | then / next step / sequential (ordered operations) |

Example: `analyze»transform»output` (do analyze, then transform, then output)

### Relations

| Symbol | Meaning |
|--------|---------|
| `⊳` | has domain/expertise (left=entity, right=capability) |
| `⊲` | triggered by / activated on (left=entity, right=trigger) |
| `@` | located at path |
| `:` | has type / is-a / key-value separator (context-dependent) |
| `=` | equals / defined as |
| `∋` | contains / includes |

Note: `:` meaning depends on context — `agent:coordinator` (type), `{line:≥80%}` (key-value), `fix:typo` (prefix)

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
| `+` | add / include / with (context-dependent) |
| `-` | remove / exclude |

Note: `+` meaning depends on context — `+file` (add), `log+ctx` (with/and), `gap→assume+mark` (combination)

### Qualifiers

| Symbol | Meaning |
|--------|---------|
| `*` | many / collection (e.g., `ENT*` = entities) |
| `?` | optional |
| `!` | required / important |
| `#` | comment / note |
| `⊕` | optimal / target (e.g., `≥80%⊕90%` = min 80%, target 90%) |

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

# Function signature (code compression)
Λ.fnName{params→ReturnType; body_intent}

# Error handling (code compression)
P.err{condition→action; fallback→alternative}

# Type definitions (code compression)
E.types{TypeName{field:type; field2:type2}}

# Import grouping (code compression)
Κ{mod1,mod2,mod3; Types=@pkg/types}

# IO channels (code compression)
io{stdout→data; stderr→log; return→result}

# Iteration pattern (code compression)
∀item{condition→action; else→skip}

# Visual element (image compression)
E.name{shape:form;style:color+effect;label="text"}

# Spatial layout (image compression)
Π.layout{flow:L→R; element@position→element@position}

# Visual metaphor (image compression)
Ω.metaphor{concept(visual)→meaning; msg="takeaway"}
```

---

## Image Compression

CRUX can compress images by extracting their **semantic visual description** into notation. This is inherently **lossy** — it preserves meaning, not pixels.

### How It Works

1. An LLM with vision reads the source image
2. The semantic content is encoded using standard CRUX blocks
3. Output is a `.crux.md` file (not `.crux.mdc` — images are not Cursor rules)
4. "Decompression" = feeding the `.crux.md` to an LLM with image generation

### Visual Description Blocks

Use standard blocks with visual-specific semantics:

| Block | Visual Purpose | Example |
|-------|---------------|---------|
| `Ρ{}` | Image purpose/context | `Ρ{architecture diagram; hero visual}` |
| `Κ{}` | Visual vocabulary/key | `Κ{prism=engine; beam=data flow}` |
| `Π.layout{}` | Spatial composition | `Π.layout{L→R flow; A@left→B@center→C@right}` |
| `E.name{}` | Visual element | `E.input{shape:cube; style:blue+glass; label="Title"}` |
| `Ω.metaphor{}` | Conceptual meaning | `Ω.metaphor{big→small; msg="compression"}` |

### Visual Element Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `shape:` | Geometric form | `shape:cube\|diamond\|circle\|arrow` |
| `style:` | Color, transparency, effects | `style:blue+glass;lg` or `style:golden+glow;sm` |
| `label=` | Visible text (verbatim) | `label="Compressed CRUX Notation (20% Size)"` |
| `∋` | Sub-elements contained | `face∋[Ρ,Λ,Π,Ω] symbols` |
| `@` | Position in layout | `element@left\|center\|right\|top\|bottom` |

### Image Quality Gates

```crux
Ω.image{
  preserve_text    = ⊤   # All visible text/labels verbatim
  layout_accurate  = ⊤   # Spatial relationships described
  elements_complete = ⊤   # All visual elements enumerated
  style_captured   = ⊤   # Colors, effects, scale noted
  metaphor_clear   = ⊤   # Conceptual meaning articulated
  reconstructable  = ⊤   # LLM+image gen could recreate
}
```

**Note**: Image compression has no token ratio target. The goal is semantic fidelity — an LLM with image generation should produce a recognizably similar result from the `.crux.md` description alone.

---

## Code Compression

CRUX can compress source code files by extracting their **semantic structure** into notation. This preserves function signatures, control flow intent, and architectural patterns while eliminating syntactic verbosity.

### How It Works

1. An LLM reads the source code file
2. The semantic structure is encoded using standard CRUX blocks with code-specific mappings
3. Output is a `.crux.md` file (not `.crux.mdc` — code files are not Cursor rules)
4. "Decompression" = an LLM reconstructing functionally equivalent code from the `.crux.md`

### Code Block Mappings

Use standard blocks with code-specific semantics:

| Block | Code Purpose | Example |
|-------|-------------|---------|
| `Λ{}` | Functions/methods | `Λ.fetchData{url,opts→Promise<Response>; retry(3)»fetch»validate}` |
| `Γ{}` | Orchestration/main flow | `Γ.main{init»configure»run»cleanup}` |
| `Κ{}` | Imports/dependencies | `Κ{fs,path,axios; Types=@pkg/types}` |
| `Φ{}` | Configuration/constants | `Φ{MAX_RETRIES=3; TIMEOUT=5000; ENV=prod}` |
| `E{}` | Types/interfaces/entities | `E{Config{host:str; port:num; tls:bool}}` |
| `P.err{}` | Error handling patterns | `P.err{fetch→retry»throw; parse→log+default}` |
| `M{}` | State/memory/storage | `M{cache:Map<k,v>; db:singleton}` |
| `Ρ{}` | Module purpose/context | `Ρ{HTTP client wrapper;TS;Node}` |
| `P.security{}` | Security patterns | `P.security{input→sanitize; path∈allowed}` |
| `Ω.decomp{}` | Decompression guidance | `Ω.decomp{emulate=tsc --strict;src=ts;focus=[...]}` |

### Code-Specific Compression Rules

In addition to the general compression rules:

1. **PRESERVE** function/method names verbatim — these are the API contract
2. **PRESERVE** type signatures for public interfaces (`params→ReturnType`)
3. **COLLAPSE** function bodies to intent chains (`parse»validate»transform→result`)
4. **ENCODE** IO semantics explicitly — distinguish stdout vs stderr, return channels
5. **ENCODE** error handling patterns concisely (`try→catch→retry|throw`)
6. **GROUP** imports by source (`Κ{stdlib; external; internal}`)
7. **ABBREVIATE** common patterns: `async/await` implied, `Promise<T>` can shorten to just `T` when obvious
8. **GENERATE** `Ω.decomp` block with language-specific tool emulation

### Code Quality Gates

```crux
Ω.code{
  fn_names_verbatim = ⊤   # Function names preserved exactly
  type_sigs_present = ⊤   # Public interface types included
  io_semantics      = ⊤   # stdout/stderr/return distinguished
  error_patterns    = ⊤   # Error handling encoded
  control_flow      = ⊤   # Branching/loops/conditionals captured
  decomp_block      = ⊤   # Ω.decomp present with emulate=
  no_hallucination  = ⊤   # Only encode what's in source
  target_ratio      ≤ level/100 # Default 0.25; configurable via crux: <n>
}
```

### Template (Code)

```
⟦CRUX:{filename of source code}
Ρ{module purpose; language; framework}
Κ{imports and dependencies}
Φ{constants and configuration}
E{types, interfaces, entities}
Λ.functionName{params→ReturnType; intent}
Γ.orchestration{flow description}
P.err{error handling patterns}
P.security{security patterns if applicable}
M{state management if applicable}
Ω.decomp{emulate=tool;src=ext;focus=[...]}
⟧
```

---

## Output Format

All CRUX compression produces `*.crux.md` files — a universal, IDE-agnostic format. For Cursor IDE users, an automatic adapter step copies the `.crux.md` to `.crux.mdc` with Cursor-specific frontmatter injected (see Cursor Adapter below).

### Template (Markdown)

```
⟦CRUX:{filename of source markdown rules}
{blocks in logical order, one concept per line, max ~80 chars/line}
⟧
```

### Template (Code)

```
⟦CRUX:{filename of source code file}
Ρ{module purpose; language; framework}
Κ{imports and dependencies}
Φ{constants and configuration}
E{types, interfaces, entities}
Λ.functionName{params→ReturnType; intent}
Γ.orchestration{flow description}
P.err{error handling patterns}
M{state management}
Ω.decomp{emulate=tool;src=ext;focus=[...]}
⟧
```

### Template (Image)

```
⟦CRUX:{filename of source image}
Ρ{image purpose/context}
Κ{visual vocabulary mappings}
Π.layout{spatial composition and flow}
E.element1{shape; style; label; contents}
E.element2{...}
Ω.metaphor{conceptual meaning}
⟧
```

### Do

- Start immediately with `⟦CRUX:{source_file}`
- Use single line per logical unit
- Group related items with namespaces
- Preserve all actionable information (text, layout, meaning for images)
- End with `⟧`

### Don't

- Add explanatory prose outside the block
- Invent information not in source
- Use multiple lines for simple lists
- Include redundant metadata

---

## Cursor Adapter

CRUX compression is IDE-agnostic — all output uses the universal `.crux.md` format. For **Cursor IDE** users, a post-compression adapter step produces a `.crux.mdc` copy that Cursor recognizes as a rule file.

### How It Works

1. Compression always produces `[filename].crux.md` (universal)
2. If the source file is in `.cursor/rules/` (auto-detected) or `--cursor` flag is passed:
   - Copy `.crux.md` content to `[filename].crux.mdc`
   - Inject `alwaysApply` and other Cursor-specific frontmatter from the source file
3. The `.crux.mdc` is a **derived artifact** — the `.crux.md` is the source of truth

### File Relationship

```
Source: .cursor/rules/my-rule.md
    │
    ├─→ .cursor/rules/my-rule.crux.md     (universal CRUX, no alwaysApply)
    │
    └─→ .cursor/rules/my-rule.crux.mdc    (Cursor adapter: + alwaysApply)
```

### When the Adapter Runs

- **Automatic**: Source file is in `.cursor/rules/` directory
- **Explicit**: `--cursor` flag passed to `/crux-compress`
- **Skipped**: Source file is outside `.cursor/rules/` and no `--cursor` flag

### Cursor-Specific Frontmatter

The adapter copies these fields from the source file's frontmatter into the `.crux.mdc`:
- `alwaysApply` (defaults to `false` if not present)
- Any other Cursor-recognized frontmatter fields

These fields are **not** included in the universal `.crux.md` output.

---

## Compression Level

The compression level controls how aggressively CRUX compresses the source material. It is expressed as a **target percentage** of the original token count — lower values mean more aggressive compression.

### Setting the Level

The level can be set via **frontmatter** or **CLI flag**:

| Method | Example | Effect |
|--------|---------|--------|
| `crux: true` | Default | Target ≤25% of original |
| `crux: 40` | Frontmatter number | Target ≤40% of original |
| `--25` | CLI flag | Target ≤25% of original |
| `--40` | CLI flag | Target ≤40% of original |

**CLI flag overrides frontmatter** when both are present.

### Valid Range

- **1–100** (integer percentage)
- `crux: true` is equivalent to `crux: 25` (or `crux: 80` for images)
- Values outside 1–100 are rejected with an error

### Behavior by Source Type

| Source Type | Level Meaning | Default (`true`) |
|-------------|--------------|-------------------|
| **Markdown rules** | Target token ratio (e.g., 40 = keep ≤40% of tokens) | 25% |
| **Code files** | Target token ratio | 25% |
| **URLs** | Target token ratio | 25% |
| **Images** | Detail retention (100 = maximum detail, 1 = minimal) | 80 |

### How Level Affects Compression

**For text-based sources** (markdown, code, URLs):
- Lower values → more aggressive symbol use, deeper abbreviation, tighter merging
- Higher values → more prose preserved, lighter abbreviation, closer to original structure
- The `reducedBy` frontmatter field reflects the actual achieved reduction

**For images**:
- The level controls **detail retention** in the semantic visual description
- `crux: 100` → describe every visual element, texture, color gradient, spatial relationship
- `crux: 80` (default) → detailed description including textures, gradients, secondary elements
- `crux: 10` → only the essential concept and primary elements

### Examples

```yaml
# Default compression (25% target)
crux: true

# Moderate compression (40% target — more verbose output)
crux: 40

# Aggressive compression (10% target — very terse)
crux: 10

# Maximum detail for images (retain all visual information)
crux: 100
```

### Frontmatter in Output

The compression level is recorded in the `.crux.md` output frontmatter:

```yaml
---
generated: 2026-03-10 14:00
sourceChecksum: "1234567890"
cruxLevel: 25
beforeTokens: 1000
afterTokens: 250
reducedBy: 75%
confidence: 92%
---
```

---

## Quality Gates

```crux
Ω{
  no_hallucination = ⊤   # Only encode what's in source
  no_invention     = ⊤   # No new commands/paths/names
  preserve_paths   = ⊤   # File paths verbatim
  preserve_cmds    = ⊤   # Commands verbatim (can abbreviate structure)
  semantic_equiv   = ⊤   # LLM can expand back to original meaning
  target_ratio     ≤ level/100 # Default 0.25; configurable via crux: <n>
}
```

### Checklist

- [ ] Target ≤ level% of original token count (default 25%)
- [ ] All file paths preserved verbatim
- [ ] All commands reconstructable
- [ ] No hallucinated content
- [ ] Semantic equivalence maintained
- [ ] `Ω.decomp` block present (code files only)

### `Ω.decomp` — Decompression Guidance

The `Ω.decomp` block embeds a hint for LLMs reconstructing code from CRUX notation. It instructs the decompressing LLM to mentally emulate the validation tool appropriate for the source language, catching issues that compression operates above (e.g., shell quoting semantics, type narrowing).

**Syntax:**
```crux
Ω.decomp{emulate=<tool>;src=<ext>;focus=[<areas>]}
```

**Fields:**
- `emulate=` — The validation tool to mentally emulate during decompression (self-documenting)
- `src=` — Source file extension (determines language context)
- `focus=` — Array of specific areas where compression loses fidelity

**Standard Tool Mapping:**

| Source Extension | `emulate=` Value | Focus Areas |
|-----------------|-----------------|-------------|
| `.sh`, `.bash` | `shellcheck` | quoting, word splitting, io redirection, subshell capture |
| `.ts`, `.tsx` | `tsc --strict` | type narrowing, null checks, async/await, generics |
| `.js`, `.jsx` | `eslint --recommended` | type coercion, scope, hoisting, prototype chain |
| `.py` | `mypy --strict` | type hints, None checks, import resolution |
| `.rs` | `cargo clippy` | ownership, borrowing, lifetimes, unsafe blocks |
| `.go` | `go vet` | error handling, goroutine leaks, interface satisfaction |
| `.java` | `spotbugs` | null safety, resource management, concurrency |
| `.sql` | `sqlfluff` | injection, join semantics, index usage |
| `.css`, `.scss` | `stylelint` | specificity, cascade, browser compat |

**Why `emulate=` instead of `ext→tool`:**

The `→` operator is ambiguous in CRUX — it could mean "run tool" or "pipe to tool." The `emulate=` keyword is self-documenting: any LLM reading `emulate=shellcheck` understands "act as this tool would" without needing the CRUX specification loaded.

**Example (bash):**
```crux
Ω.decomp{emulate=shellcheck;src=sh;
  focus=[io_redir(log fn→stderr via >&2),
  quoting(word_split+glob in array assign),
  subshell_capture(echo→stdout only;log→stderr)]}
```

---

## Token Estimation

Token counts are required in CRUX output frontmatter (`beforeTokens`, `afterTokens`).

### Primary Method: CRUX-Utils Skill

If the `CRUX-Utils` skill is available, use `--token-count` mode for deterministic token counting. The skill also provides `--cksum` mode for sourceChecksum generation.

### Fallback Method: LLM-Based Estimation

If the skill is not available, use these heuristics:

| Content Type | Chars/Token | Notes |
|--------------|-------------|-------|
| Prose (markdown) | 4.0 | English text, headers, lists |
| Code blocks | 3.5 | More symbols, shorter identifiers |
| Special chars | 1.0 | CRUX Unicode symbols (→, ⊳, ⟦, », etc.) |

**Estimation formula**:
```
total_tokens = (prose_chars / 4.0) + (code_chars / 3.5) + special_char_count
```

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
| `w/` | with |
| `w/o` | without |
| `ln` | lines |
| `cls` | class |
| `iface` | interface |
| `svc` | service |
| `txn` | transaction |
| `idx` | index |
| `fn` | function |
| `var` | variable |
| `param` | parameter |
| `ctx` | context |
| `msg` | message |
| `req` | request |
| `res` | response |

---

## Quick Reference

```
STRUCTURE:  ⟦⟧{}[]().sub;
COMPARE:    > < ≥ ≤ ≠ ..
PRIORITY:   ≻ ≺
DATA FLOW:  → ←
SEQUENCE:   »
RELATIONS:  ⊳ ⊲ @ : = ∋
LOGIC:      | & ⊤ ⊥ ∀ ∃ ¬
CHANGE:     Δ + -
QUALIFY:    * ? ! # ⊕
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
sourceChecksum: [checksum from CRUX-Utils skill]
beforeTokens: ~400
afterTokens: ~140
confidence: [XX% - semantic validation score from separate agent]
alwaysApply: true
---

# Code Modification Protocol

```crux
⟦CRUX:{source_file}
R=req→truth;gap→assume+mark;?arch→ask first
C=obs→cite path:lines;repo≻chat
Δ=R≠C→tag{code|tests|req}+why
PLAN=min files+targeted Δ;justify+file|broad
PATCH=surgical diff;¬rewrite w/o proof
CHECK=run/+tests|static val
STATE={R,C,Δ}→upd on progress
Ω{¬halluc;verified only}
⟧
```

### LLM/agent interpretation (internal CoT trace)

`R=req→truth;gap→assume+mark;?arch→ask first`
Requirements: user requirements are source of truth (req→truth); when gaps exist, assume and mark them (gap→assume+mark); when architecture is uncertain (?arch), ask first

`C=obs→cite path:lines;repo≻chat`
Code analysis: observations should cite specific file paths and line numbers (obs→cite path:lines); trust repo over conversation history (repo≻chat)

`Δ=R≠C→tag{code|tests|req}+why`
Changes: when requirements ≠ current code (R≠C), tag what's affected (code, tests, or requirements docs) and explain why (+why)

`PLAN=min files+targeted Δ;justify+file|broad`
Planning: touch minimum files with targeted changes (min files+targeted Δ); justify when adding files or making broad modifications (justify+file|broad)

`PATCH=surgical diff;¬rewrite w/o proof`
Implementation: make surgical, precise edits using diffs; don't rewrite entire files without proof it's necessary (¬rewrite w/o proof)

`CHECK=run/+tests|static val`
Verification: run existing tests, add new tests, or use static validation (run/+tests|static val)

`STATE={R,C,Δ}→upd on progress`
Tracking: maintain mental model of requirements (R), code state (C), and changes (Δ); update as conversation progresses (→upd on progress)

`Ω{¬halluc;verified only}`
Quality: never hallucinate (¬halluc); base all suggestions on verified information only

---

## Image Example

### Input (image)

A concept diagram showing: a large translucent blue cube labeled "Bulky Documentation (Verbose English & Markdown)" on the left, with text visible on its faces. Lines converge into a central diamond/prism shape displaying CRUX symbols (Ρ, Λ, Π, Ω) and encoding symbols (→, ⊕, ∀, ¬). Labels "Automation", "Validation", "Semantic Preservation" float nearby. A golden beam exits to a small golden diamond labeled "Compressed CRUX Notation (20% Size)". Dark blue background with circuit-board traces.

### Output (.crux.md file)

```crux
⟦CRUX:concept-diagram.png
Ρ{CRUX-Compress concept diagram; marketing/hero visual}
Κ{prism=compression engine; beam=data flow; cube=input; gem=output}

Π.layout{
 L→R flow; dark blue bg+circuit traces
 input:cube@left→prism@center→output:gem@right
}

E.input{
 cube:translucent blue+glass;lg
 label="Bulky Documentation (Verbose English & Markdown)"
 face∋visible code+markdown text ln
}

E.prism{
 shape:diamond/crystal;white+blue glow
 face∋[Ρ,Λ,Π,Ω] CRUX block symbols
 base∋[→,⊕,∀,¬] encoding symbols
 beams:input→prism=many thin white ln converging
}

E.output{
 shape:sm golden diamond;bright glow+flare
 label="Compressed CRUX Notation (20% Size)"
 beam:prism→output=single golden ray
}

E.labels{
 float@prism.right=[Automation,Validation,Semantic Preservation]
 style=cyan+icon badges
}

Ω.metaphor{
 verbose docs(lg)→CRUX engine(prism+symbols)→compact output(sm,20%)
 visual=light refraction analogy; many rays→1 focused beam
 msg="CRUX distills bulky rules to their essential meaning"
}
⟧
```

### Key differences from text compression

- **Lossy**: Decompression produces a semantically similar but not pixel-identical image
- **No token ratio**: Goal is semantic fidelity, not a percentage target
- **Visual vocabulary**: Uses `shape:`, `style:`, `label=`, `@position` for spatial description
- **Decompression**: Feed `.crux.md` to any LLM with image generation capabilities