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

Build a technically sophisticated, visually distinctive landing page that demonstrates CRUX compression in real-time using WebGPU. The page must convince AI/ML engineers that CRUX is worth exploring by *showing* compression happening, not just claiming it works.

**Core Message**: Reclaim up to 80% of your context window. CRUX extracts the semantic core from verbose AI rules and compresses it into notation LLMs understand natively.

**Visitor Journey**:
1. Land → See compression happening in 3D (WebGPU hero)
2. Scroll → Camera pans through compression stages
3. Understand → Expandable spec sections explain the notation
4. Act → Install via quickstart

---

## Λ{CONSTRAINTS}

### Technical Requirements
```
stack:        static HTML/CSS/JS (no build step required)
gpu:          WebGPU required (provide fallback message for unsupported browsers)
hosting:      GitHub Pages compatible
dependencies: minimal, CDN-loaded where needed
performance:  ≤3s first meaningful paint on 4G
accessibility: WCAG 2.1 AA for text content (WebGPU canvas exempt)
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

### Section 0: WebGPU Hero — "The Compression Chamber"

**Concept**: A 3D visualization showing text tokens as particles that get pulled toward a central point, merge, and emerge as compressed CRUX symbols. Camera starts wide, showing the chaos of verbose text, then slowly dollies in as compression occurs.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │         [WebGPU Canvas — Full Viewport Height]          │   │
│  │                                                         │   │
│  │    Particles representing tokens swirl inward...        │   │
│  │    ...compress into dense CRUX symbols...               │   │
│  │    ...camera follows the transformation                 │   │
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

**WebGPU Implementation Notes**:
```javascript
// Particle system requirements:
// - 2000-5000 particles representing "tokens"
// - Each particle has: position, velocity, color, size, "compression state"
// - Compression state: 0.0 (verbose/scattered) → 1.0 (compressed/clustered)
// - Color shift: cool blues (verbose) → warm amber (compressed)
// - Particle merging: multiple particles collapse into single CRUX symbol
// - Camera: orbit controls disabled, scripted dolly/pan on scroll
// - MOUSE REACTIVITY: particles and camera respond to cursor position

// Mouse interaction requirements:
// - Track normalized mouse position (-1 to 1 on both axes)
// - Particles near cursor get subtle repulsion force (creates "wake" effect)
// - Camera has slight parallax offset based on mouse position
// - Effect intensity scales with compression state (more reactive when compressed)

// Shader requirements:
// - Vertex shader: particle instancing, size attenuation
// - Fragment shader: soft circles with glow, color interpolation
// - Compute shader (optional): physics simulation for attraction + mouse repulsion

// Fallback for non-WebGPU:
// - Detect via navigator.gpu
// - Show static SVG animation or CSS-only version
// - Clear message: "WebGPU visualization requires Chrome 113+ / Edge 113+"
```

**Mouse Reactivity Specification**:
```javascript
// Mouse state tracking
const mouseState = {
  normalized: { x: 0, y: 0 },      // -1 to 1, center is 0,0
  velocity: { x: 0, y: 0 },         // for momentum effects
  isOverCanvas: false,
  lastUpdate: performance.now()
};

// Update on mousemove
canvas.addEventListener('mousemove', (e) => {
  const rect = canvas.getBoundingClientRect();
  mouseState.normalized.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  mouseState.normalized.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  // Calculate velocity for momentum
  const now = performance.now();
  const dt = (now - mouseState.lastUpdate) / 1000;
  mouseState.velocity.x = (mouseState.normalized.x - prevX) / dt;
  mouseState.velocity.y = (mouseState.normalized.y - prevY) / dt;
  mouseState.lastUpdate = now;
});

// Particle mouse repulsion (in compute shader or JS)
const MOUSE_REPULSION_RADIUS = 0.3;    // normalized units
const MOUSE_REPULSION_STRENGTH = 0.5;  // scales with proximity

function applyMouseRepulsion(particle, mousePos3D) {
  const toMouse = subtract(particle.position, mousePos3D);
  const dist = length(toMouse);
  if (dist < MOUSE_REPULSION_RADIUS && dist > 0.001) {
    const force = normalize(toMouse);
    const strength = (1 - dist / MOUSE_REPULSION_RADIUS) * MOUSE_REPULSION_STRENGTH;
    particle.velocity = add(particle.velocity, scale(force, strength));
  }
}

// Camera parallax offset
const PARALLAX_STRENGTH = 2.0;  // units of camera offset at edges

function getCameraOffset(mouseNorm, compressionState) {
  // More parallax when compressed (tighter view = more noticeable movement)
  const intensity = 0.3 + compressionState * 0.7;
  return {
    x: mouseNorm.x * PARALLAX_STRENGTH * intensity,
    y: mouseNorm.y * PARALLAX_STRENGTH * intensity * 0.5  // less vertical
  };
}

// Apply to camera each frame
function updateCamera(basePosition, scrollProgress, mouseNorm) {
  const keyframePos = interpolateKeyframes(scrollProgress);
  const offset = getCameraOffset(mouseNorm, scrollProgress);
  return {
    x: keyframePos.x + offset.x,
    y: keyframePos.y + offset.y,
    z: keyframePos.z
  };
}
```

**Mouse Effects Summary**:
| Effect | Trigger | Behavior |
|--------|---------|----------|
| Particle repulsion | Cursor near particles | Particles gently pushed away, creating "wake" |
| Camera parallax | Cursor position | Subtle camera offset, depth illusion |
| Intensity scaling | Scroll progress | Effects stronger when view is compressed |
| Momentum | Fast mouse movement | Particles continue moving briefly after cursor stops |
| Glow intensify | Hover near CRUX symbols | Symbols brighten when cursor approaches |

**Touch/Mobile Handling**:
```javascript
// Touch creates same effect as mouse, mapped to touch position
canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  mouseState.normalized.x = ((touch.clientX - rect.left) / rect.width) * 2 - 1;
  mouseState.normalized.y = -((touch.clientY - rect.top) / rect.height) * 2 + 1;
  mouseState.isOverCanvas = true;
}, { passive: false });

canvas.addEventListener('touchend', () => {
  // Gradually fade out mouse influence rather than instant stop
  fadeOutMouseInfluence();
});

// On mobile without hover, add subtle autonomous "breathing" motion
// to particles when no touch is active, suggesting interactivity
function autonomousMotion(time) {
  if (!mouseState.isOverCanvas && isMobile) {
    const breathe = Math.sin(time * 0.001) * 0.1;
    // Apply subtle oscillation to particle cluster
  }
}
```

**Scroll-Triggered Camera Animation**:
```
scroll 0%   → camera position: far, wide angle, particles scattered
scroll 25%  → camera dollies in, particles begin gravitating to center
scroll 50%  → camera at medium distance, particles merging, CRUX symbols forming
scroll 75%  → camera close, dense cluster of CRUX notation visible
scroll 100% → camera rests, compression complete, stats overlay visible
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
│  └── VERSION                                                   │
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

## Γ{WEBGPU_IMPLEMENTATION}

### Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     WebGPU Rendering Pipeline                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Particle   │───▶│   Compute    │───▶│   Render     │      │
│  │   Buffer     │    │   Shader     │    │   Pipeline   │      │
│  │              │    │              │    │              │      │
│  │  positions   │    │  attraction  │    │  instanced   │      │
│  │  velocities  │    │  damping     │    │  quads       │      │
│  │  colors      │    │  merging     │    │  alpha blend │      │
│  │  states      │    │              │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Scroll Controller                      │  │
│  │                                                           │  │
│  │  scrollY → normalizedProgress (0.0 - 1.0)                │  │
│  │         → camera.position.z interpolation                │  │
│  │         → particle.compressionState interpolation        │  │
│  │         → color.temperature interpolation                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Particle System Specification

```javascript
// Particle structure (per-particle data)
struct Particle {
  position: vec3<f32>,      // world position
  velocity: vec3<f32>,      // current velocity
  baseColor: vec3<f32>,     // verbose state color (cool)
  targetColor: vec3<f32>,   // compressed state color (warm)
  size: f32,                // radius
  compressionState: f32,    // 0.0 = scattered, 1.0 = compressed
  mergeTarget: u32,         // index of particle to merge with (-1 if none)
  isSymbol: u32,            // 0 = token particle, 1 = CRUX symbol
  symbolIndex: u32,         // which CRUX symbol (if isSymbol)
}

// Constants
const PARTICLE_COUNT = 3000;
const ATTRACTION_STRENGTH = 2.5;
const DAMPING = 0.95;
const MERGE_DISTANCE = 0.1;
const SYMBOL_EMERGENCE_THRESHOLD = 0.7;

// Color palette
const VERBOSE_COLOR = vec3(0.4, 0.6, 0.8);   // cool blue
const COMPRESSED_COLOR = vec3(0.9, 0.6, 0.2); // warm amber
const SYMBOL_COLOR = vec3(1.0, 0.85, 0.4);    // bright gold
```

### Compute Shader (WGSL) — with mouse reactivity

```wgsl
struct SimParams {
  scrollProgress: f32,
  deltaTime: f32,
  mouseX: f32,           // normalized -1 to 1
  mouseY: f32,           // normalized -1 to 1
  mouseActive: f32,      // 1.0 if cursor over canvas, 0.0 otherwise
}

@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> params: SimParams;

const ATTRACTION_STRENGTH: f32 = 2.5;
const DAMPING: f32 = 0.95;
const MOUSE_REPULSION_RADIUS: f32 = 8.0;      // world units
const MOUSE_REPULSION_STRENGTH: f32 = 15.0;

@compute @workgroup_size(256)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let idx = id.x;
    if (idx >= arrayLength(&particles)) { return; }
    
    var p = particles[idx];
    
    // 1. Attraction toward center, strength based on scroll progress
    let toCenter = -p.position;
    let attractionForce = normalize(toCenter) * params.scrollProgress * ATTRACTION_STRENGTH;
    
    // 2. Mouse repulsion (project mouse to 3D plane at z=0)
    let mousePos3D = vec3<f32>(params.mouseX * 20.0, params.mouseY * 12.0, 0.0);
    let toMouse = p.position - mousePos3D;
    let mouseDist = length(toMouse);
    var mouseForce = vec3<f32>(0.0);
    
    if (params.mouseActive > 0.5 && mouseDist < MOUSE_REPULSION_RADIUS && mouseDist > 0.01) {
        let repulsionDir = normalize(toMouse);
        let falloff = 1.0 - (mouseDist / MOUSE_REPULSION_RADIUS);
        // Stronger repulsion when more compressed (particles denser)
        let intensityScale = 0.3 + params.scrollProgress * 0.7;
        mouseForce = repulsionDir * falloff * falloff * MOUSE_REPULSION_STRENGTH * intensityScale;
    }
    
    // 3. Apply forces with damping
    p.velocity = (p.velocity + attractionForce + mouseForce) * DAMPING;
    p.position = p.position + p.velocity * params.deltaTime;
    
    // 4. Update compression state for color interpolation
    p.compressionState = smoothstep(0.0, 1.0, params.scrollProgress);
    
    particles[idx] = p;
}
```

### Camera Animation Keyframes

```javascript
const cameraKeyframes = [
  { scroll: 0.0,  position: [0, 0, 50],  fov: 60, lookAt: [0, 0, 0] },
  { scroll: 0.25, position: [10, 5, 35], fov: 55, lookAt: [0, 0, 0] },
  { scroll: 0.5,  position: [5, 2, 20],  fov: 50, lookAt: [0, 0, 0] },
  { scroll: 0.75, position: [2, 1, 12],  fov: 45, lookAt: [0, 0, 0] },
  { scroll: 1.0,  position: [0, 0, 8],   fov: 40, lookAt: [0, 0, 0] },
];

// Interpolation: use cubic bezier for smooth camera motion
function interpolateCamera(scrollProgress) {
  // Find surrounding keyframes
  // Apply cubic interpolation
  // Return { position, fov, lookAt }
}
```

### CRUX Symbol Rendering

When particles merge (at ~70% scroll), they transform into CRUX symbols:

```javascript
const CRUX_SYMBOLS = [
  '⟦', '⟧', 'Ρ', 'Κ', 'R', 'Λ', 'Ω', 
  '→', '←', '∀', '¬', '≻', '⊤', '⊥'
];

// Render symbols as SDF (Signed Distance Field) or pre-rendered textures
// Symbols should glow and pulse slightly when formed
```

### Fallback for Non-WebGPU Browsers

```html
<div id="webgpu-fallback" style="display: none;">
  <div class="fallback-animation">
    <!-- CSS-only particle animation using @keyframes -->
    <!-- Simpler, but still communicates compression -->
  </div>
  <p class="fallback-message">
    Full 3D visualization requires WebGPU 
    (Chrome 113+, Edge 113+, or Firefox Nightly with flag).
    <br>
    <a href="#quickstart">Skip to installation →</a>
  </p>
</div>

<script>
  if (!navigator.gpu) {
    document.getElementById('webgpu-canvas').style.display = 'none';
    document.getElementById('webgpu-fallback').style.display = 'flex';
  }
</script>
```

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

1. **WebGPU is the hero** — The 3D compression visualization IS the differentiator. Don't ship without it working impressively.

2. **Experimental status is honest** — Every major section should acknowledge this is new, evolving, potentially breaking. Build trust through transparency.

3. **Show, don't claim** — The live compression demo does more than any marketing copy. Make it unmissable.

4. **Technical audience respect** — No dumbing down. These are engineers who've hit context limits. Speak to their pain precisely.

5. **Performance is non-negotiable** — If WebGPU tanks the page, fix it or simplify. A smooth 60fps simple animation beats a janky complex one.

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
  - Chrome 113+ (WebGPU)
  - Edge 113+ (WebGPU)
  - Firefox Nightly (WebGPU flag)
  - Safari 18+ (WebGPU, limited)
  - Fallback: Any modern browser (CSS animation)
estimated_build_time: 8-12 hours
dependencies:
  - None required (vanilla JS)
  - Optional: Three.js for simplified WebGPU abstraction
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
│   ├── webgpu-init.js      # WebGPU setup, fallback detection
│   ├── particle-system.js  # Particle simulation
│   ├── camera-controller.js # Scroll-linked camera
│   ├── compression-demo.js  # Before/after animation
│   └── spec-expander.js    # Expandable notation sections
├── shaders/
│   ├── particle.wgsl       # Compute + render shaders
│   └── symbol.wgsl         # CRUX symbol rendering
├── assets/
│   ├── og-image.png        # Social sharing image
│   └── favicon.svg         # CRUX-themed favicon
└── README.md               # Deployment instructions
```

---

**END OF SPECIFICATION**

*This prompt is designed to be executed by an AI coding agent (Claude, Cursor, etc.) to produce a complete, deployable static site. The agent should read this entire document, then implement section by section, testing WebGPU functionality in a real browser environment.*
