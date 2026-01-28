// CRUX Symbol Rendering Shader
// Renders CRUX notation symbols (⟦, ⟧, Ρ, Κ, R, Λ, Ω, →, etc.) using SDF

struct VertexOutput {
  @builtin(position) position: vec4<f32>,
  @location(0) uv: vec2<f32>,
  @location(1) symbolIndex: f32,
  @location(2) alpha: f32,
  @location(3) glow: f32,
}

struct SymbolParams {
  viewProjection: mat4x4<f32>,
  time: f32,
  scrollProgress: f32,
  padding: vec2<f32>,
}

@group(0) @binding(0) var<uniform> params: SymbolParams;
@group(0) @binding(1) var symbolTexture: texture_2d<f32>;
@group(0) @binding(2) var symbolSampler: sampler;

// Symbol positions (pre-computed merge targets)
struct SymbolInstance {
  position: vec3<f32>,
  scale: f32,
  symbolIndex: f32,
  alpha: f32,
  padding: vec2<f32>,
}

@group(0) @binding(3) var<storage, read> symbols: array<SymbolInstance>;

// Vertex shader for symbol billboards
@vertex
fn vertexMain(
  @builtin(vertex_index) vertexIndex: u32,
  @builtin(instance_index) instanceIndex: u32
) -> VertexOutput {
  var output: VertexOutput;
  
  let symbol = symbols[instanceIndex];
  
  // Quad vertices
  let quadPositions = array<vec2<f32>, 6>(
    vec2<f32>(-1.0, -1.0),
    vec2<f32>(1.0, -1.0),
    vec2<f32>(-1.0, 1.0),
    vec2<f32>(-1.0, 1.0),
    vec2<f32>(1.0, -1.0),
    vec2<f32>(1.0, 1.0)
  );
  
  let quadPos = quadPositions[vertexIndex];
  
  // Billboard in world space
  let worldPos = symbol.position + vec3<f32>(quadPos * symbol.scale, 0.0);
  
  output.position = params.viewProjection * vec4<f32>(worldPos, 1.0);
  output.uv = quadPos * 0.5 + 0.5;
  output.symbolIndex = symbol.symbolIndex;
  output.alpha = symbol.alpha;
  
  // Pulsing glow effect
  let pulse = sin(params.time * 2.0 + symbol.symbolIndex) * 0.5 + 0.5;
  output.glow = 0.3 + pulse * 0.2;
  
  return output;
}

// SDF for basic shapes used in CRUX symbols
fn sdBox(p: vec2<f32>, b: vec2<f32>) -> f32 {
  let d = abs(p) - b;
  return length(max(d, vec2<f32>(0.0))) + min(max(d.x, d.y), 0.0);
}

fn sdCircle(p: vec2<f32>, r: f32) -> f32 {
  return length(p) - r;
}

fn sdTriangle(p: vec2<f32>, r: f32) -> f32 {
  let k = sqrt(3.0);
  var q = p;
  q.x = abs(q.x) - r;
  q.y = q.y + r / k;
  if (q.x + k * q.y > 0.0) {
    q = vec2<f32>(q.x - k * q.y, -k * q.x - q.y) / 2.0;
  }
  q.x -= clamp(q.x, -2.0 * r, 0.0);
  return -length(q) * sign(q.y);
}

// Render CRUX symbols procedurally
fn renderSymbol(uv: vec2<f32>, symbolIndex: f32) -> f32 {
  let p = uv * 2.0 - 1.0; // Center coordinates
  
  let idx = i32(symbolIndex) % 14;
  
  var d: f32 = 1.0;
  
  // Different symbols based on index
  switch idx {
    case 0: { // ⟦ - Left double bracket
      d = min(
        sdBox(p - vec2<f32>(-0.2, 0.0), vec2<f32>(0.1, 0.6)),
        sdBox(p - vec2<f32>(0.1, 0.0), vec2<f32>(0.1, 0.6))
      );
    }
    case 1: { // ⟧ - Right double bracket
      d = min(
        sdBox(p - vec2<f32>(0.2, 0.0), vec2<f32>(0.1, 0.6)),
        sdBox(p - vec2<f32>(-0.1, 0.0), vec2<f32>(0.1, 0.6))
      );
    }
    case 2: { // Ρ - Rho (Repository)
      d = min(
        sdBox(p - vec2<f32>(-0.2, 0.0), vec2<f32>(0.1, 0.5)),
        sdCircle(p - vec2<f32>(0.1, 0.2), 0.25)
      );
    }
    case 3: { // Κ - Kappa (Concepts)
      d = min(
        sdBox(p - vec2<f32>(-0.2, 0.0), vec2<f32>(0.1, 0.5)),
        min(
          sdBox(p - vec2<f32>(0.1, 0.2), vec2<f32>(0.3, 0.08)),
          sdBox(p - vec2<f32>(0.1, -0.2), vec2<f32>(0.3, 0.08))
        )
      );
    }
    case 4: { // R - Requirements
      d = min(
        sdBox(p - vec2<f32>(-0.2, 0.0), vec2<f32>(0.1, 0.5)),
        min(
          sdCircle(p - vec2<f32>(0.1, 0.2), 0.2),
          sdBox(p - vec2<f32>(0.15, -0.3), vec2<f32>(0.25, 0.08))
        )
      );
    }
    case 5: { // Λ - Lambda (Commands)
      d = min(
        sdBox(vec2<f32>(p.x - 0.15, p.y + 0.1), vec2<f32>(0.08, 0.4)),
        sdBox(vec2<f32>(p.x + 0.15, p.y + 0.1), vec2<f32>(0.08, 0.4))
      );
    }
    case 6: { // Ω - Omega (Quality)
      d = min(
        sdCircle(p - vec2<f32>(0.0, 0.1), 0.35),
        min(
          sdBox(p - vec2<f32>(-0.25, -0.35), vec2<f32>(0.1, 0.15)),
          sdBox(p - vec2<f32>(0.25, -0.35), vec2<f32>(0.1, 0.15))
        )
      );
    }
    case 7: { // → - Arrow right
      d = min(
        sdBox(p, vec2<f32>(0.4, 0.08)),
        sdTriangle(vec2<f32>(-p.x + 0.3, p.y), 0.2)
      );
    }
    case 8: { // ← - Arrow left
      d = min(
        sdBox(p, vec2<f32>(0.4, 0.08)),
        sdTriangle(vec2<f32>(p.x + 0.3, p.y), 0.2)
      );
    }
    case 9: { // ∀ - For all
      d = min(
        sdBox(vec2<f32>(p.x - 0.15, -p.y + 0.1), vec2<f32>(0.08, 0.4)),
        min(
          sdBox(vec2<f32>(p.x + 0.15, -p.y + 0.1), vec2<f32>(0.08, 0.4)),
          sdBox(p - vec2<f32>(0.0, 0.0), vec2<f32>(0.2, 0.08))
        )
      );
    }
    case 10: { // ¬ - Negation
      d = min(
        sdBox(p - vec2<f32>(0.0, 0.1), vec2<f32>(0.4, 0.08)),
        sdBox(p - vec2<f32>(0.3, -0.1), vec2<f32>(0.08, 0.2))
      );
    }
    case 11: { // ≻ - Preferred over
      d = min(
        sdBox(p - vec2<f32>(-0.1, 0.15), vec2<f32>(0.3, 0.08)),
        sdBox(p - vec2<f32>(-0.1, -0.15), vec2<f32>(0.3, 0.08))
      );
    }
    case 12: { // ⊤ - True
      d = min(
        sdBox(p - vec2<f32>(0.0, 0.3), vec2<f32>(0.4, 0.08)),
        sdBox(p - vec2<f32>(0.0, 0.0), vec2<f32>(0.08, 0.35))
      );
    }
    case 13: { // ⊥ - False
      d = min(
        sdBox(p - vec2<f32>(0.0, -0.3), vec2<f32>(0.4, 0.08)),
        sdBox(p - vec2<f32>(0.0, 0.0), vec2<f32>(0.08, 0.35))
      );
    }
    default: {
      d = sdCircle(p, 0.3);
    }
  }
  
  // Convert SDF to alpha with antialiasing
  let edge = 0.05;
  return 1.0 - smoothstep(-edge, edge, d);
}

// Fragment shader
@fragment
fn fragmentMain(input: VertexOutput) -> @location(0) vec4<f32> {
  // Render symbol shape
  let shape = renderSymbol(input.uv, input.symbolIndex);
  
  if (shape < 0.01) {
    discard;
  }
  
  // Symbol color (bright gold with glow)
  let baseColor = vec3<f32>(1.0, 0.85, 0.4);
  let glowColor = vec3<f32>(1.0, 0.9, 0.6);
  
  // Add glow effect
  let finalColor = mix(baseColor, glowColor, input.glow);
  
  return vec4<f32>(finalColor, shape * input.alpha);
}
