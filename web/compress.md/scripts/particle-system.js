/**
 * WebGPU Particle System
 * 3D particle visualization showing compression from chaos to CRUX symbols
 */

class ParticleSystem {
  constructor(webgpuContext) {
    this.ctx = webgpuContext;
    this.device = null;
    this.particleCount = 3000;
    this.particles = null;
    this.particleBuffer = null;
    this.uniformBuffer = null;
    this.viewBuffer = null;
    this.computePipeline = null;
    this.renderPipeline = null;
    this.bindGroup = null;
    this.lastTime = performance.now();
    this.scrollProgress = 0;
    this.mouseX = 0;
    this.mouseY = 0;
    this.mouseActive = false;
    this.time = 0;
    this.isRunning = false;
    this.cameraController = null;
  }

  async init() {
    if (!this.ctx.isSupported) {
      return false;
    }

    this.device = this.ctx.getDevice();
    
    // Load shaders
    const shaderCode = await this.loadShader('shaders/particle.wgsl');
    if (!shaderCode) {
      console.error('Failed to load particle shader');
      return false;
    }

    const shaderModule = this.device.createShaderModule({
      code: shaderCode
    });

    // Initialize particle data
    this.initParticles();
    
    // Create buffers
    this.createBuffers();
    
    // Create pipelines
    await this.createPipelines(shaderModule);
    
    // Create bind groups
    this.createBindGroups();
    
    // Setup event listeners
    this.setupEvents();
    
    return true;
  }

  async loadShader(path) {
    try {
      const response = await fetch(path);
      return await response.text();
    } catch (error) {
      console.error('Shader load error:', error);
      return null;
    }
  }

  initParticles() {
    // Particle structure: position(3) + velocity(3) + baseColor(3) + targetColor(3) + size(1) + compressionState(1) + life(1) + seed(1) = 16 floats
    const floatsPerParticle = 16;
    this.particles = new Float32Array(this.particleCount * floatsPerParticle);
    
    for (let i = 0; i < this.particleCount; i++) {
      const offset = i * floatsPerParticle;
      
      // Random spherical distribution for initial position
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const radius = 15 + Math.random() * 25; // Scattered far from center
      
      // Position
      this.particles[offset + 0] = radius * Math.sin(phi) * Math.cos(theta);
      this.particles[offset + 1] = radius * Math.sin(phi) * Math.sin(theta);
      this.particles[offset + 2] = radius * Math.cos(phi);
      
      // Velocity (small random)
      this.particles[offset + 3] = (Math.random() - 0.5) * 2;
      this.particles[offset + 4] = (Math.random() - 0.5) * 2;
      this.particles[offset + 5] = (Math.random() - 0.5) * 2;
      
      // Base color (verbose blue)
      this.particles[offset + 6] = 0.4;
      this.particles[offset + 7] = 0.6;
      this.particles[offset + 8] = 0.8;
      
      // Target color (same initially)
      this.particles[offset + 9] = 0.4;
      this.particles[offset + 10] = 0.6;
      this.particles[offset + 11] = 0.8;
      
      // Size
      this.particles[offset + 12] = 0.1 + Math.random() * 0.1;
      
      // Compression state (0 = scattered)
      this.particles[offset + 13] = 0;
      
      // Life
      this.particles[offset + 14] = 1.0;
      
      // Seed for randomness
      this.particles[offset + 15] = Math.random();
    }
  }

  createBuffers() {
    // Particle storage buffer
    this.particleBuffer = this.device.createBuffer({
      size: this.particles.byteLength,
      usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST,
      mappedAtCreation: true
    });
    new Float32Array(this.particleBuffer.getMappedRange()).set(this.particles);
    this.particleBuffer.unmap();

    // Simulation parameters uniform buffer
    // deltaTime, scrollProgress, mouseX, mouseY, mouseActive, canvasWidth, canvasHeight, time
    this.uniformBuffer = this.device.createBuffer({
      size: 32, // 8 floats * 4 bytes
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST
    });

    // View parameters uniform buffer
    // viewProjection (16 floats) + cameraPosition (3 floats) + time (1 float) = 20 floats
    this.viewBuffer = this.device.createBuffer({
      size: 80, // 20 floats * 4 bytes
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST
    });
  }

  async createPipelines(shaderModule) {
    // Compute pipeline for particle simulation
    this.computePipeline = this.device.createComputePipeline({
      layout: 'auto',
      compute: {
        module: shaderModule,
        entryPoint: 'computeMain'
      }
    });

    // Render pipeline for particle drawing
    this.renderPipeline = this.device.createRenderPipeline({
      layout: 'auto',
      vertex: {
        module: shaderModule,
        entryPoint: 'vertexMain'
      },
      fragment: {
        module: shaderModule,
        entryPoint: 'fragmentMain',
        targets: [{
          format: this.ctx.getFormat(),
          blend: {
            color: {
              srcFactor: 'src-alpha',
              dstFactor: 'one-minus-src-alpha',
              operation: 'add'
            },
            alpha: {
              srcFactor: 'one',
              dstFactor: 'one-minus-src-alpha',
              operation: 'add'
            }
          }
        }]
      },
      primitive: {
        topology: 'triangle-list'
      }
    });
  }

  createBindGroups() {
    // Compute bind group
    this.computeBindGroup = this.device.createBindGroup({
      layout: this.computePipeline.getBindGroupLayout(0),
      entries: [
        { binding: 0, resource: { buffer: this.uniformBuffer } },
        { binding: 1, resource: { buffer: this.particleBuffer } }
      ]
    });

    // Render bind group
    this.renderBindGroup = this.device.createBindGroup({
      layout: this.renderPipeline.getBindGroupLayout(0),
      entries: [
        { binding: 0, resource: { buffer: this.uniformBuffer } },
        { binding: 1, resource: { buffer: this.particleBuffer } },
        { binding: 2, resource: { buffer: this.viewBuffer } }
      ]
    });
  }

  setupEvents() {
    const canvas = this.ctx.getCanvas();
    
    // Mouse tracking
    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      this.mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      this.mouseActive = true;
    });

    canvas.addEventListener('mouseleave', () => {
      this.mouseActive = false;
    });

    // Touch support
    canvas.addEventListener('touchmove', (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      const rect = canvas.getBoundingClientRect();
      this.mouseX = ((touch.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouseY = -((touch.clientY - rect.top) / rect.height) * 2 + 1;
      this.mouseActive = true;
    }, { passive: false });

    canvas.addEventListener('touchend', () => {
      this.mouseActive = false;
    });

    // Scroll tracking
    window.addEventListener('scroll', () => {
      const hero = document.getElementById('hero');
      if (!hero) return;
      
      const rect = hero.getBoundingClientRect();
      const heroHeight = hero.offsetHeight;
      
      // Calculate scroll progress through hero section
      if (rect.top >= 0) {
        this.scrollProgress = 0;
      } else if (rect.bottom <= 0) {
        this.scrollProgress = 1;
      } else {
        this.scrollProgress = Math.min(1, Math.max(0, -rect.top / heroHeight));
      }
    });
  }

  setCameraController(controller) {
    this.cameraController = controller;
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.lastTime = performance.now();
    this.animate();
  }

  stop() {
    this.isRunning = false;
  }

  animate() {
    if (!this.isRunning) return;

    const now = performance.now();
    const deltaTime = Math.min((now - this.lastTime) / 1000, 0.1); // Cap delta time
    this.lastTime = now;
    this.time += deltaTime;

    this.update(deltaTime);
    this.render();

    requestAnimationFrame(() => this.animate());
  }

  update(deltaTime) {
    const canvas = this.ctx.getCanvas();
    
    // Update simulation parameters
    const simParams = new Float32Array([
      deltaTime,
      this.scrollProgress,
      this.mouseX,
      this.mouseY,
      this.mouseActive ? 1.0 : 0.0,
      canvas.width,
      canvas.height,
      this.time
    ]);
    this.device.queue.writeBuffer(this.uniformBuffer, 0, simParams);

    // Update view parameters
    if (this.cameraController) {
      const viewProjection = this.cameraController.getViewProjectionMatrix();
      const cameraPosition = this.cameraController.getPosition();
      
      const viewParams = new Float32Array(20);
      viewParams.set(viewProjection, 0);
      viewParams.set(cameraPosition, 16);
      viewParams[19] = this.time;
      
      this.device.queue.writeBuffer(this.viewBuffer, 0, viewParams);
    }

    // Run compute shader
    const commandEncoder = this.device.createCommandEncoder();
    const computePass = commandEncoder.beginComputePass();
    computePass.setPipeline(this.computePipeline);
    computePass.setBindGroup(0, this.computeBindGroup);
    computePass.dispatchWorkgroups(Math.ceil(this.particleCount / 256));
    computePass.end();
    
    this.device.queue.submit([commandEncoder.finish()]);
  }

  render() {
    const context = this.ctx.getContext();
    const textureView = context.getCurrentTexture().createView();

    const commandEncoder = this.device.createCommandEncoder();
    
    const renderPass = commandEncoder.beginRenderPass({
      colorAttachments: [{
        view: textureView,
        clearValue: { r: 0.039, g: 0.059, b: 0.059, a: 1.0 }, // --bg-primary
        loadOp: 'clear',
        storeOp: 'store'
      }]
    });

    renderPass.setPipeline(this.renderPipeline);
    renderPass.setBindGroup(0, this.renderBindGroup);
    renderPass.draw(6, this.particleCount); // 6 vertices per quad, instanced
    renderPass.end();

    this.device.queue.submit([commandEncoder.finish()]);
  }

  getScrollProgress() {
    return this.scrollProgress;
  }
}

// Initialize particle system when WebGPU is ready
document.addEventListener('DOMContentLoaded', async () => {
  const ctx = window.webgpuContext;
  
  // Always start hero stats animation (works without WebGPU)
  animateHeroStats();
  
  // Try to initialize WebGPU particle system
  const success = await ctx.init();
  
  if (success) {
    try {
      const particleSystem = new ParticleSystem(ctx);
      const initialized = await particleSystem.init();
      
      if (initialized) {
        // Create camera controller
        const cameraController = new CameraController(ctx.getCanvas());
        particleSystem.setCameraController(cameraController);
        
        // Store globally for debugging
        window.particleSystem = particleSystem;
        window.cameraController = cameraController;
        
        // Start animation
        particleSystem.start();
      }
    } catch (error) {
      console.warn('Particle system failed to initialize:', error.message);
    }
  }
});

// Animate compression bar and stats based on scroll progress
function animateHeroStats() {
  const compressionFill = document.getElementById('compression-fill');
  const percentage = document.getElementById('percentage');
  const hero = document.getElementById('hero');
  
  if (!hero) return;
  
  let lastProgress = -1;
  
  function updateStats() {
    const rect = hero.getBoundingClientRect();
    const heroHeight = hero.offsetHeight;
    
    let progress = 0;
    if (rect.top >= 0) {
      progress = 0;
    } else if (rect.bottom <= 0) {
      progress = 1;
    } else {
      progress = Math.min(1, Math.max(0, -rect.top / heroHeight));
    }
    
    // Only update DOM if progress changed significantly
    if (Math.abs(progress - lastProgress) > 0.01) {
      lastProgress = progress;
      
      // Animate compression bar
      if (compressionFill) {
        compressionFill.style.width = `${progress * 100}%`;
      }
      
      // Calculate percentage recovered
      const recovered = Math.round(progress * 80);
      if (percentage) {
        percentage.textContent = recovered;
      }
    }
    
    requestAnimationFrame(updateStats);
  }
  
  updateStats();
}
