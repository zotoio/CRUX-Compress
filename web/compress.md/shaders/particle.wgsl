// Particle Compute and Render Shaders for CRUX Compression Visualization

// Simulation parameters passed from JavaScript
struct SimParams {
  deltaTime: f32,
  scrollProgress: f32,
  mouseX: f32,
  mouseY: f32,
  mouseActive: f32,
  canvasWidth: f32,
  canvasHeight: f32,
  time: f32,
}

// Individual particle structure
struct Particle {
  position: vec3<f32>,
  velocity: vec3<f32>,
  baseColor: vec3<f32>,
  targetColor: vec3<f32>,
  size: f32,
  compressionState: f32,
  life: f32,
  seed: f32,
}

// Storage buffers for particle data
@group(0) @binding(0) var<uniform> params: SimParams;
@group(0) @binding(1) var<storage, read_write> particles: array<Particle>;

// Constants
const ATTRACTION_STRENGTH: f32 = 2.5;
const DAMPING: f32 = 0.95;
const MOUSE_REPULSION_RADIUS: f32 = 8.0;
const MOUSE_REPULSION_STRENGTH: f32 = 15.0;
const MERGE_THRESHOLD: f32 = 0.7;
const CENTER: vec3<f32> = vec3<f32>(0.0, 0.0, 0.0);

// Pseudo-random function
fn rand(seed: f32, offset: f32) -> f32 {
  return fract(sin(seed * 12.9898 + offset * 78.233) * 43758.5453);
}

// Compute shader for particle simulation
@compute @workgroup_size(256)
fn computeMain(@builtin(global_invocation_id) id: vec3<u32>) {
  let idx = id.x;
  let particleCount = arrayLength(&particles);
  
  if (idx >= particleCount) {
    return;
  }
  
  var p = particles[idx];
  
  // Compression state interpolation based on scroll
  let targetCompression = smoothstep(0.0, 1.0, params.scrollProgress);
  p.compressionState = mix(p.compressionState, targetCompression, params.deltaTime * 3.0);
  
  // Calculate attraction to center (stronger as compression increases)
  let toCenter = CENTER - p.position;
  let distToCenter = length(toCenter);
  let attractionDir = normalize(toCenter);
  
  // Dynamic attraction based on compression state
  let compressionForce = ATTRACTION_STRENGTH * p.compressionState * p.compressionState;
  let scatterForce = 1.0 - p.compressionState;
  
  // Apply attraction force
  let attraction = attractionDir * compressionForce * min(distToCenter, 10.0);
  
  // Add some orbital motion when scattered
  let orbitSpeed = 0.5 * scatterForce;
  let orbit = vec3<f32>(
    -toCenter.y * orbitSpeed,
    toCenter.x * orbitSpeed,
    sin(params.time + p.seed * 6.28) * 0.2 * scatterForce
  );
  
  // Mouse repulsion
  var mouseRepulsion = vec3<f32>(0.0);
  if (params.mouseActive > 0.5) {
    // Convert mouse to world space (simplified)
    let mouseWorld = vec3<f32>(
      params.mouseX * 30.0,
      params.mouseY * 20.0,
      0.0
    );
    
    let toMouse = p.position - mouseWorld;
    let distToMouse = length(toMouse);
    
    if (distToMouse < MOUSE_REPULSION_RADIUS) {
      let repulsionStrength = MOUSE_REPULSION_STRENGTH * (1.0 - distToMouse / MOUSE_REPULSION_RADIUS);
      // Stronger repulsion when compressed (creates wake effect)
      let strengthMod = 0.3 + p.compressionState * 0.7;
      mouseRepulsion = normalize(toMouse) * repulsionStrength * strengthMod;
    }
  }
  
  // Breathing motion when not being actively scrolled
  let breathe = sin(params.time * 0.5 + p.seed * 6.28) * 0.1 * (1.0 - abs(params.scrollProgress - 0.5) * 2.0);
  let breatheForce = attractionDir * breathe;
  
  // Combine forces
  let totalForce = attraction + orbit + mouseRepulsion + breatheForce;
  
  // Update velocity with damping
  p.velocity = p.velocity * DAMPING + totalForce * params.deltaTime;
  
  // Clamp velocity
  let maxSpeed = 20.0;
  let speed = length(p.velocity);
  if (speed > maxSpeed) {
    p.velocity = p.velocity * (maxSpeed / speed);
  }
  
  // Update position
  p.position = p.position + p.velocity * params.deltaTime;
  
  // Color interpolation: verbose (cool blue) -> compressed (warm amber) -> symbol (gold)
  let verboseColor = vec3<f32>(0.4, 0.6, 0.8);   // Cool blue
  let compressedColor = vec3<f32>(0.9, 0.6, 0.2); // Warm amber
  let symbolColor = vec3<f32>(1.0, 0.85, 0.4);    // Bright gold
  
  if (p.compressionState < MERGE_THRESHOLD) {
    // Transition from verbose to compressed
    let t = p.compressionState / MERGE_THRESHOLD;
    p.targetColor = mix(verboseColor, compressedColor, t);
  } else {
    // Transition from compressed to symbol
    let t = (p.compressionState - MERGE_THRESHOLD) / (1.0 - MERGE_THRESHOLD);
    p.targetColor = mix(compressedColor, symbolColor, t);
  }
  
  p.baseColor = mix(p.baseColor, p.targetColor, params.deltaTime * 2.0);
  
  // Size based on compression state
  let baseSize = 0.1 + rand(p.seed, 1.0) * 0.1;
  let compressedSize = 0.05;
  let symbolSize = 0.15 + rand(p.seed, 2.0) * 0.1;
  
  if (p.compressionState < MERGE_THRESHOLD) {
    p.size = mix(baseSize, compressedSize, p.compressionState / MERGE_THRESHOLD);
  } else {
    let t = (p.compressionState - MERGE_THRESHOLD) / (1.0 - MERGE_THRESHOLD);
    p.size = mix(compressedSize, symbolSize, t * t);
  }
  
  // Write back
  particles[idx] = p;
}

// Vertex shader output
struct VertexOutput {
  @builtin(position) position: vec4<f32>,
  @location(0) color: vec3<f32>,
  @location(1) alpha: f32,
  @location(2) uv: vec2<f32>,
}

// Camera/view uniforms
struct ViewParams {
  viewProjection: mat4x4<f32>,
  cameraPosition: vec3<f32>,
  time: f32,
}

@group(0) @binding(2) var<uniform> view: ViewParams;

// Vertex shader for instanced particle rendering
@vertex
fn vertexMain(
  @builtin(vertex_index) vertexIndex: u32,
  @builtin(instance_index) instanceIndex: u32
) -> VertexOutput {
  var output: VertexOutput;
  
  let p = particles[instanceIndex];
  
  // Billboard quad vertices
  let quadPositions = array<vec2<f32>, 6>(
    vec2<f32>(-1.0, -1.0),
    vec2<f32>(1.0, -1.0),
    vec2<f32>(-1.0, 1.0),
    vec2<f32>(-1.0, 1.0),
    vec2<f32>(1.0, -1.0),
    vec2<f32>(1.0, 1.0)
  );
  
  let quadPos = quadPositions[vertexIndex];
  
  // Billboard orientation (face camera)
  let worldPos = p.position + vec3<f32>(quadPos * p.size, 0.0);
  
  output.position = view.viewProjection * vec4<f32>(worldPos, 1.0);
  output.color = p.baseColor;
  output.alpha = 0.6 + p.compressionState * 0.3;
  output.uv = quadPos * 0.5 + 0.5;
  
  return output;
}

// Fragment shader for particle rendering
@fragment
fn fragmentMain(input: VertexOutput) -> @location(0) vec4<f32> {
  // Circular particle with soft edge
  let dist = length(input.uv - vec2<f32>(0.5));
  let edge = 0.5;
  let softness = 0.1;
  
  let alpha = 1.0 - smoothstep(edge - softness, edge, dist);
  
  if (alpha < 0.01) {
    discard;
  }
  
  // Add subtle glow
  let glow = exp(-dist * 4.0) * 0.3;
  let finalColor = input.color + vec3<f32>(glow);
  
  return vec4<f32>(finalColor, alpha * input.alpha);
}
