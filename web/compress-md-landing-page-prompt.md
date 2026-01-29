---
crux: true
---

# COMPRESS.MD — Landing Page Build Specification

> **Executable Prompt for AI Agent**  
> Target: Single static landing page for [CRUX-Compress](https://github.com/zotoio/CRUX-Compress)  
> Domain: `compress.md`  
> Status: **EXPERIMENTAL** — Communicate this clearly throughout

---

## Ρ{PURPOSE}

Build a technically sophisticated, visually distinctive landing page that demonstrates CRUX compression in real-time. The page must convince AI/ML engineers that CRUX is worth exploring by *showing* compression happening, not just claiming it works.

**Core Message**: Reclaim up to 80% of your context window. CRUX extracts the semantic core from verbose AI rules and compresses it into notation LLMs understand natively.

**Visitor Journey**:
1. Land → See compression visualization in hero section
2. Scroll → Explore compression stages
3. Understand → Expandable spec sections explain the notation
4. Act → Install via quickstart

---

## Λ{CONSTRAINTS}

### Technical Requirements
```
stack:        static HTML/CSS/JS (no build step required)
hosting:      GitHub Pages compatible
dependencies: minimal, CDN-loaded where needed
performance:  ≤3s first meaningful paint on 4G
accessibility: WCAG 2.1 AA for text content
```

### Design Constraints
```
palette:      NOT purple, NOT standard AI-site gradients
              USE: deep teals, warm ambers, charcoal blacks
              ACCENT: compression-state colors (verbose=cool, compressed=warm)
typography:   monospace for code/CRUX notation
              sans-serif for prose (Inter, system-ui fallback)
layout:       NO generic card grids, NO cookie-cutter hero sections
              YES: asymmetric layouts, intentional whitespace, editorial feel
animations:   purposeful only — every animation must communicate compression
```

### Content Constraints
```
tone:         technical, precise, forward-looking
              speak to engineers who've hit context limits
              acknowledge experimental status honestly
claims:       "up to 80% token reduction" (cite: AI rules benchmark)
              "experimental tool" (emphasize throughout)
              "LLMs interpret natively" (no decompression step)
```

---

## Π{PAGE_STRUCTURE}

### Section 0: Hero — "The Compression Chamber"

**Concept**: A visually striking hero section with CSS-animated background showing the essence of compression. Features animated gradients and floating particles that evoke the transformation from verbose to compressed.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │         [CSS Animated Background — Full Height]         │   │
│  │                                                         │   │
│  │    Gradient particles floating and pulsing...           │   │
│  │    ...creating an atmosphere of transformation          │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗ │
│  ║  CRUX                                                     ║ │
│  ║  Context Reduction Using X-encoding                       ║ │
│  ║                                                           ║ │
│  ║  ░░░░░░░░████████████████████░░░░░░░░  80% RECOVERED     ║ │
│  ║  2,500 tokens  →  500 tokens                              ║ │
│  ║                                                           ║ │
│  ║  [ Scroll to explore ]                                    ║ │
│  ╚═══════════════════════════════════════════════════════════╝ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CSS Animation Notes**:
```css
/* Hero background with animated gradients */
.hero-background {
  background: var(--bg-primary);
}

.hero-particles {
  background: 
    radial-gradient(circle at 20% 30%, rgba(91, 138, 154, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(212, 145, 90, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(240, 198, 116, 0.08) 0%, transparent 40%);
}

/* Optional floating particles via CSS animations */
@keyframes float {
  0%, 100% { transform: translate3d(0, 0, 0); opacity: 0.3; }
  50% { transform: translate3d(20px, -30px, 0); opacity: 0.5; }
}
```

---

### Section 1: The Problem

**Layout**: Split screen — left side verbose markdown, right side context window visualization

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  THE PROBLEM                                                  │
│                                                               │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │ # Team Standards    │    │ ████████████████████ │          │
│  │                     │    │ ████████████████████ │ ← rules  │
│  │ ## Style Rules      │    │ ████████████████████ │          │
│  │ - Use 2 spaces...   │    │ ████████████████████ │          │
│  │ - Never use tabs... │    │ ░░░░░░░░░░░░░░░░░░░░ │ ← code   │
│  │ - Lines must not... │    │ ░░░░░░░░░░░░░░░░░░░░ │          │
│  │                     │    │                      │          │
│  │ [continues...]      │    │ 70% consumed by rules│          │
│  └─────────────────────┘    └─────────────────────┘          │
│                                                               │
│  Your AI assistant reads natural language well.               │
│  It just doesn't need 2,500 tokens to understand              │
│  "use camelCase for functions."                               │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Copy**:
> AI coding assistants like Cursor, Copilot, and Claude rely on context windows to understand your project. When you add natural language rules to guide agent behavior, those rules consume valuable tokens—often thousands per file.
>
> As your rule library grows, context window usage balloons. Less room for code. Less room for conversation. Less room for the work that matters.
>
> You want readable, maintainable rules. LLMs just need the actionable information.

---

### Section 2: The Approach — Live Compression Demo

**Concept**: Side-by-side panels showing actual CRUX compression. Left panel has verbose markdown, right panel shows CRUX output. As user scrolls, the compression animates line-by-line.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  THE APPROACH                                                   │
│                                                                 │
│  CRUX extracts the decisive points — the crux — and encodes    │
│  them in notation all LLMs understand without additional        │
│  instructions.                                                  │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │ BEFORE: 625 tokens       │  │ AFTER: 112 tokens        │    │
│  │─────────────────────────-│  │─────────────────────────-│    │
│  │ # Team Development       │  │ ⟦CRUX:coding-standards   │    │
│  │ Standards                │  │                          │    │
│  │                          │  │ Ρ{team dev standards}    │    │
│  │ ## Key Definitions       │→→│                          │    │
│  │ | Abbreviation | Mean... │  │ Κ{fn=function;           │    │
│  │ | fn | function |        │  │   cls=class;             │    │
│  │ | cls | class |          │  │   cmp=component}         │    │
│  │                          │  │                          │    │
│  │ ## Style Rules           │→→│ R.style{indent=2sp;      │    │
│  │ - Use 2 spaces for...    │  │   ¬tabs!;                │    │
│  │ - Never use tabs!        │  │   line≤100ch}            │    │
│  │ - Lines must not...      │  │                          │    │
│  │                          │  │ Ω{quality≻speed;         │    │
│  │ [... more ...]           │  │   readable≻clever}       │    │
│  │                          │  │                          │    │
│  └──────────────────────────┘  └──────────────────────────┘    │
│                                                                 │
│  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  82% SAVED         │
│                                                                 │
│  LLMs interpret CRUX natively. No decompression. No training.  │
│  The semantic meaning is preserved in a form they already      │
│  understand.                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Section 3: The Notation — Interactive Spec Explorer

**Concept**: Expandable/collapsible sections for each part of the CRUX specification. Default state: collapsed with preview. Click to expand full documentation.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  THE NOTATION                                                   │
│                                                                 │
│  CRUX uses mathematical and logical symbols that LLMs          │
│  interpret without explicit instruction.                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▶ STRUCTURE         «» ⟨⟩ {} [] ()                      │   │
│  │   Delimiters, grouping, hierarchy                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▼ RELATIONS         → ← ⊳ ⊲ @ : = ∋                     │   │
│  │───────────────────────────────────────────────────────────│   │
│  │                                                           │   │
│  │   →  implies / leads to / produces                        │   │
│  │   ←  derives from / sourced from                          │   │
│  │   ⊳  triggers / invokes                                   │   │
│  │   ⊲  triggered by / invoked by                            │   │
│  │   @  at / located in / context                            │   │
│  │   :  has property / defined as                            │   │
│  │   =  equals / assigned                                    │   │
│  │   ∋  contains / includes                                  │   │
│  │                                                           │   │
│  │   Example:                                                │   │
│  │   "When error occurs, log and handle it"                  │   │
│  │   → err→log+handle                                        │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▶ LOGIC             | & ⊤ ⊥ ∀ ∃ ¬                       │   │
│  │   Boolean operations, quantifiers, negation              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▶ STANDARD BLOCKS   Ρ E Λ Π Κ R P Γ M Φ Ω               │   │
│  │   Purpose, Examples, Triggers, Priorities, Keys...       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [View Full Specification on GitHub →]                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Expandable Sections Content** (from CRUX v2.1.0 spec):

```yaml
STRUCTURE:
  symbols: "⟦ ⟧ { } [ ] ( ) .sub ;"
  meaning: "Delimiters and hierarchy"
  details:
    - "⟦CRUX:source⟧ — block delimiters with source file reference"
    - "{k=v,k2=v2} — object/map"
    - "[a,b,c] — list/array"
    - "(grouping) — logical grouping"
    - ".sub — namespace (e.g., Π.core, Λ.build)"
    - "; — statement separator"

COMPARISON:
  symbols: "> < ≥ ≤ ≠ .."
  meaning: "Numeric comparison and ranges"
  details:
    - "> < ≥ ≤ ≠ — standard comparisons"
    - ".. — range/to (e.g., 20..30 = 20 to 30)"

PRIORITY:
  symbols: "≻ ≺"
  meaning: "Precedence and ranking"
  details:
    - "≻ preferred over / ranks above: CONFIRMED≻DRAFT"
    - "≺ ranks below / lower priority"

DATA_FLOW:
  symbols: "→ ←"
  meaning: "Flow and mapping"
  details:
    - "→ flows to / maps to / conditional then: trigger→action"
    - "← flows from / derives from: source←upstream"

SEQUENCE:
  symbols: "»"
  meaning: "Ordered operations"
  details:
    - "» then / next step: analyze»transform»output"

RELATIONS:
  symbols: "⊳ ⊲ @ : = ∋"
  meaning: "Domain, triggers, location, types"
  details:
    - "⊳ has domain/expertise: agent⊳'code review'"
    - "⊲ triggered by: agent⊲commit|PR|review"
    - "@ located at path: component@path/to/file.ts"
    - ": has type / key-value: agent:coordinator, {line:≥80%}"
    - "= equals / defined as"
    - "∋ contains: archetype∋[rules,plugins,deps]"

LOGIC:
  symbols: "| & ⊤ ⊥ ∀ ∃ ¬"
  meaning: "Boolean and quantifiers"
  details:
    - "| OR / alternatives"
    - "& AND / conjunction"
    - "⊤ true / enabled / yes"
    - "⊥ false / disabled / no"
    - "∀ for all / universal: ∀changes→run_tests"
    - "∃ exists / some"
    - "¬ not / negation: ¬halluc"

CHANGE:
  symbols: "Δ + -"
  meaning: "Modification and delta"
  details:
    - "Δ change / update / delta: ∀Δ→yarn_test"
    - "+ add / include / with (context-dependent)"
    - "- remove / exclude"

QUALIFIERS:
  symbols: "* ? ! # ⊕"
  meaning: "Modifiers and targets"
  details:
    - "* many / collection: ENT* = entities"
    - "? optional"
    - "! required / important"
    - "# comment / note"
    - "⊕ optimal / target: ≥80%⊕90% = min 80%, target 90%"

IMPORTANCE:
  symbols: "⊛ ◊"
  meaning: "Criticality markers"
  details:
    - "⊛ critical / highest importance"
    - "◊ lowest importance / trivial"

STANDARD_BLOCKS:
  symbols: "Ρ E Λ Π Κ R P Γ M Φ Ω"
  meaning: "Semantic containers"
  details:
    - "Ρ (Rho) — Repository/project context"
    - "E — Entities (packages, agents, components)"
    - "Λ (Lambda) — Commands/actions (build, test, deploy)"
    - "Π (Pi) — Architecture (modules, structure, deps)"
    - "Κ (Kappa) — Concepts/definitions (domain terms)"
    - "R — Requirements/guidelines (must do, should do)"
    - "P — Policies/constraints (forbidden, readonly)"
    - "Γ (Gamma) — Orchestration (workflows, triggers)"
    - "M — Memory/state (knowledge bases, persistence)"
    - "Φ (Phi) — Configuration (settings, env vars)"
    - "Ω (Omega) — Quality gates (invariants, validation)"
```

---

### Section 4: Quickstart

**Concept**: Single command install, clear prerequisites, immediate next steps.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  QUICKSTART                                                     │
│                                                                 │
│  ⚠ EXPERIMENTAL — CRUX is under active development.            │
│    Expect breaking changes. Provide feedback.                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  curl -fsSL https://raw.githubusercontent.com/zotoio/  │   │
│  │       CRUX-Compress/main/install.sh | bash             │   │
│  │                                                    [📋] │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Prerequisites: curl, unzip, Cursor IDE                         │
│                                                                 │
│  What gets installed:                                           │
│  ├── CRUX.md              Specification (read-only)            │
│  ├── AGENTS.md            Agent awareness notice               │
│  ├── .cursor/                                                  │
│  │   ├── rules/_CRUX-RULE.mdc    Always-applied rule          │
│  │   ├── agents/crux-cursor-rule-manager.md                   │
│  │   ├── commands/crux-compress.md                            │
│  │   └── hooks/detect-crux-changes.sh                         │
│  └── .crux/crux.json                                           │
│                                                                 │
│  Then:                                                          │
│  1. Add `crux: true` to any rule file's frontmatter            │
│  2. Run `/crux-compress ALL` in Cursor                         │
│  3. Watch your context window breathe again                     │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  # In your rule file:                                   │   │
│  │  ---                                                    │   │
│  │  crux: true                                             │   │
│  │  ---                                                    │   │
│  │  # Your verbose markdown rules here...                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [View on GitHub →]  [Read Full Docs →]  [Report Issue →]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Section 5: Footer

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  CRUX — Context Reduction Using X-encoding                      │
│                                                                 │
│  An experimental tool for AI context optimization.              │
│  MIT License. Contributions welcome.                            │
│                                                                 │
│  [GitHub]  [Specification]  [Changelog]  [Issues]               │
│                                                                 │
│  v2.1.0                                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

---

## Φ{VISUAL_DESIGN_SYSTEM}

### Color Tokens

```css
:root {
  /* Primary palette — NOT purple, NOT standard AI gradients */
  --color-bg-primary: #0a0f0f;        /* near-black with teal undertone */
  --color-bg-secondary: #141c1c;      /* dark teal-gray */
  --color-bg-tertiary: #1e2a2a;       /* code block background */
  
  /* Text */
  --color-text-primary: #e8eeee;      /* warm white */
  --color-text-secondary: #8fa3a3;    /* muted teal-gray */
  --color-text-tertiary: #5a7070;     /* subtle */
  
  /* Accent — compression states */
  --color-verbose: #5b8a9a;           /* cool teal (uncompressed) */
  --color-compressed: #d4915a;        /* warm amber (compressed) */
  --color-symbol: #f0c674;            /* bright gold (CRUX symbols) */
  
  /* Interactive */
  --color-link: #7ab3c2;              /* teal link */
  --color-link-hover: #9fd4e3;        /* lighter on hover */
  
  /* Borders & dividers */
  --color-border: #2a3838;
  --color-border-focus: #4a6868;
  
  /* Status */
  --color-experimental: #c27a5a;      /* warm orange for warnings */
}
```

### Typography Scale

```css
:root {
  /* Font stacks */
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  
  /* Scale (1.25 ratio) */
  --text-xs: 0.64rem;     /* 10.24px */
  --text-sm: 0.8rem;      /* 12.8px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.25rem;     /* 20px */
  --text-xl: 1.563rem;    /* 25px */
  --text-2xl: 1.953rem;   /* 31.25px */
  --text-3xl: 2.441rem;   /* 39px */
  --text-4xl: 3.052rem;   /* 48.8px */
  
  /* Line heights */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### Spacing System

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-24: 6rem;     /* 96px */
  --space-32: 8rem;     /* 128px */
}
```

### Component Patterns

**Code Blocks** (NOT standard dark theme):
```css
.code-block {
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--color-compressed);
  border-radius: 0 4px 4px 0;
  padding: var(--space-4);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  overflow-x: auto;
}

.code-block--crux {
  border-left-color: var(--color-symbol);
  background: linear-gradient(
    135deg,
    var(--color-bg-tertiary) 0%,
    rgba(240, 198, 116, 0.05) 100%
  );
}
```

**Expandable Sections**:
```css
.spec-section {
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: var(--space-3);
  overflow: hidden;
}

.spec-section__header {
  display: flex;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-secondary);
  cursor: pointer;
  transition: background 0.2s;
}

.spec-section__header:hover {
  background: var(--color-bg-tertiary);
}

.spec-section__symbols {
  font-family: var(--font-mono);
  color: var(--color-symbol);
  margin-left: auto;
}

.spec-section__content {
  padding: var(--space-4);
  display: none;
}

.spec-section--expanded .spec-section__content {
  display: block;
}
```

**Compression Progress Bar**:
```css
.compression-bar {
  height: 8px;
  background: var(--color-bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.compression-bar__fill {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--color-verbose) 0%,
    var(--color-compressed) 100%
  );
  transition: width 0.5s ease-out;
}

.compression-bar__label {
  position: absolute;
  right: var(--space-2);
  top: 50%;
  transform: translateY(-50%);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-primary);
}
```

---

## Ε{EXAMPLES}

### Example: Before/After Animation

The compression demo should animate through this transformation:

**Before (verbose markdown)**:
```markdown
# Team Development Standards

## Style Rules

### Indentation & Formatting

* Use **2 spaces** for indentation
* **Never use tabs!** This is strictly enforced
* Lines must not exceed **100 characters**

### Naming Conventions

| Element | Convention |
| --- | --- |
| Functions | camelCase |
| Classes | PascalCase |
| Constants | UPPER_SNAKE_CASE |
```

**After (CRUX notation)**:
```
⟦CRUX:coding-standards.md
Ρ{team dev standards}
R.style{
  indent=2sp; ¬tabs!; line≤100ch
  naming{fn=camelCase; cls=PascalCase; const=UPPER_SNAKE}
}
⟧
```

### Example: Interactive Demo Copy-Paste

Include a "Try it yourself" section with copy-paste CRUX for users to test in any LLM:

```
Explain this notation:

⟦CRUX:api-rules
Ρ{REST API design standards}
R{∀endpoint→versioned(/v{n}/);auth=JWT|API_KEY;rate.limit=100/min}
P.response{success→{data,meta};error→{code,message,details?}}
Λ{5xx→retry»backoff[max=3];429→wait(retry-after)}
Γ{req»validate»auth»process»respond}
Ω{consistency≻flexibility;explicit≻implicit;¬halluc}
⟧
```

**Second example** (from CRUX.md spec — Code Modification Protocol):

```
Explain and follow these rules:

⟦CRUX:code-mod-protocol
R=req→truth;gap→assume+mark;?arch→ask first
C=obs→cite path:lines;repo≻chat
Δ=R≠C→tag{code|tests|req}+why
PLAN=min files+targeted Δ;justify+file|broad
PATCH=surgical diff;¬rewrite w/o proof
CHECK=run»+tests|static val
STATE={R,C,Δ}→upd on progress
Ω{¬halluc;verified only}
⟧
```

---

## Ω{PRINCIPLES}

### Non-Negotiables

1. **Visual impact matters** — The hero section should immediately communicate the essence of compression through design.

2. **Experimental status is honest** — Every major section should acknowledge this is new, evolving, potentially breaking. Build trust through transparency.

3. **Show, don't claim** — The live compression demo does more than any marketing copy. Make it unmissable.

4. **Technical audience respect** — No dumbing down. These are engineers who've hit context limits. Speak to their pain precisely.

5. **Performance is non-negotiable** — Keep animations smooth and lightweight. A smooth 60fps simple animation beats a janky complex one.

### Design Philosophy

- **Asymmetry over grids** — Break the template feel
- **Editorial whitespace** — Let content breathe
- **Purposeful animation** — Every motion communicates compression
- **Warm technical** — Precise but not cold; expert but not gatekeeping

### Forward-Looking Tone

Position CRUX as:
- Early but promising
- Part of an emerging context engineering discipline
- A tool that will evolve with community input
- Something to experiment with, not depend on (yet)

---

## M{METADATA}

```yaml
project: compress.md
version: 1.0.0-alpha
repository: https://github.com/zotoio/CRUX-Compress
license: MIT
target_browsers:
  - All modern browsers (Chrome, Edge, Firefox, Safari)
  - Mobile browsers supported
estimated_build_time: 4-6 hours
dependencies:
  - None required (vanilla JS)
hosting: GitHub Pages
analytics: None by default (privacy-first)
```

---

## Κ{DELIVERABLES}

```
/compress.md/
├── index.html              # Single page, all content
├── styles/
│   └── main.css            # All styles, CSS custom properties
├── scripts/
│   ├── camera-controller.js # Scroll-linked animations
│   ├── compression-demo.js  # Before/after animation
│   └── spec-expander.js    # Expandable notation sections
├── assets/
│   ├── og-image.png        # Social sharing image
│   └── favicon.svg         # CRUX-themed favicon
└── README.md               # Deployment instructions
```

---

**END OF SPECIFICATION**

*This prompt is designed to be executed by an AI coding agent (Claude, Cursor, etc.) to produce a complete, deployable static site. The agent should read this entire document, then implement section by section.*
