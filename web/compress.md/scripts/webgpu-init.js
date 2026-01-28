/**
 * WebGPU Initialization and Fallback Detection
 * Handles WebGPU context setup and shows fallback for unsupported browsers
 */

class WebGPUContext {
  constructor() {
    this.canvas = document.getElementById('webgpu-canvas');
    this.fallback = document.getElementById('webgpu-fallback');
    this.device = null;
    this.context = null;
    this.format = null;
    this.isSupported = false;
    this.initAttempted = false;
  }

  async init() {
    // Prevent multiple init attempts
    if (this.initAttempted) {
      return this.isSupported;
    }
    this.initAttempted = true;

    // WebGPU disabled for now - use CSS fallback
    // TODO: Re-enable when WebGPU visualization is production-ready
    this.showFallback();
    return false;

    /* WebGPU initialization code (disabled)
    // Check WebGPU support
    if (!navigator.gpu) {
      this.showFallback();
      return false;
    }

    try {
      const adapter = await navigator.gpu.requestAdapter({
        powerPreference: 'high-performance'
      });

      if (!adapter) {
        this.showFallback();
        return false;
      }

      // Try to get device with minimal requirements
      this.device = await adapter.requestDevice();

      // Try to get webgpu context
      this.context = this.canvas.getContext('webgpu');
      if (!this.context) {
        this.showFallback();
        return false;
      }

      this.format = navigator.gpu.getPreferredCanvasFormat();

      this.context.configure({
        device: this.device,
        format: this.format,
        alphaMode: 'premultiplied'
      });

      // Handle device loss
      this.device.lost.then((info) => {
        console.warn('WebGPU device lost:', info.message);
        this.isSupported = false;
        this.showFallback();
      });

      this.isSupported = true;
      this.resizeCanvas();
      
      // Handle resize (debounced)
      let resizeTimeout;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => this.resizeCanvas(), 100);
      });

      return true;
    } catch (error) {
      console.warn('WebGPU not available:', error.message);
      this.showFallback();
      return false;
    }
    */
  }

  resizeCanvas() {
    if (!this.isSupported) return;
    
    const dpr = Math.min(window.devicePixelRatio, 2);
    const width = this.canvas.clientWidth;
    const height = this.canvas.clientHeight;

    this.canvas.width = width * dpr;
    this.canvas.height = height * dpr;

    window.dispatchEvent(new CustomEvent('webgpu-resize', {
      detail: { width: this.canvas.width, height: this.canvas.height, dpr }
    }));
  }

  showFallback() {
    // Hide canvas, show CSS fallback background
    if (this.canvas) this.canvas.style.display = 'none';
    if (this.fallback) this.fallback.hidden = false;
    this.isSupported = false;
    
    // Create lightweight CSS-only particle animation
    this.createFallbackAnimation();
  }

  createFallbackAnimation() {
    const container = this.fallback?.querySelector('.fallback-particles');
    if (!container || container.children.length > 0) return;

    // Use fewer particles for better performance
    const particleCount = 20;
    
    // Add keyframe animation first
    if (!document.getElementById('fallback-keyframes')) {
      const style = document.createElement('style');
      style.id = 'fallback-keyframes';
      style.textContent = `
        @keyframes float {
          0%, 100% { transform: translate3d(0, 0, 0); opacity: 0.3; }
          50% { transform: translate3d(20px, -30px, 0); opacity: 0.5; }
        }
        .fallback-particle {
          position: absolute;
          border-radius: 50%;
          will-change: transform, opacity;
          pointer-events: none;
        }
      `;
      document.head.appendChild(style);
    }

    // Create particles
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'fallback-particle';
      const size = 4 + Math.random() * 4;
      const isWarm = Math.random() > 0.5;
      particle.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        background: ${isWarm ? 'rgba(212, 145, 90, 0.4)' : 'rgba(91, 138, 154, 0.35)'};
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: float ${10 + Math.random() * 10}s ease-in-out infinite;
        animation-delay: ${-Math.random() * 10}s;
      `;
      container.appendChild(particle);
    }
  }

  getDevice() { return this.device; }
  getContext() { return this.context; }
  getFormat() { return this.format; }
  getCanvas() { return this.canvas; }
}

// Global WebGPU context
window.webgpuContext = new WebGPUContext();
