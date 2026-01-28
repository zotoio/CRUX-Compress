/**
 * Scroll-Linked Camera Controller
 * Manages camera movement through the compression visualization based on scroll position
 */

class CameraController {
  constructor(canvas) {
    this.canvas = canvas;
    this.scrollProgress = 0;
    this.mouseX = 0;
    this.mouseY = 0;
    this.targetMouseX = 0;
    this.targetMouseY = 0;
    
    // Camera state
    this.position = [0, 0, 50];
    this.fov = 60;
    
    // Camera keyframes (scroll position -> camera state)
    this.keyframes = [
      { scroll: 0.0, pos: [0, 0, 50], fov: 60 },
      { scroll: 0.25, pos: [10, 5, 35], fov: 55 },
      { scroll: 0.5, pos: [5, 2, 20], fov: 50 },
      { scroll: 0.75, pos: [2, 1, 12], fov: 45 },
      { scroll: 1.0, pos: [0, 0, 8], fov: 40 }
    ];
    
    // View/projection matrices
    this.viewMatrix = new Float32Array(16);
    this.projectionMatrix = new Float32Array(16);
    this.viewProjectionMatrix = new Float32Array(16);
    
    this.setupEvents();
    this.update(0);
  }

  setupEvents() {
    // Scroll tracking
    window.addEventListener('scroll', () => {
      const hero = document.getElementById('hero');
      if (!hero) return;
      
      const rect = hero.getBoundingClientRect();
      const heroHeight = hero.offsetHeight;
      
      if (rect.top >= 0) {
        this.scrollProgress = 0;
      } else if (rect.bottom <= 0) {
        this.scrollProgress = 1;
      } else {
        this.scrollProgress = Math.min(1, Math.max(0, -rect.top / heroHeight));
      }
      
      // Update camera on scroll (no continuous animation loop)
      this.updateFromScroll();
    });

    // Mouse parallax
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.targetMouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.targetMouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      this.updateFromScroll();
    });

    this.canvas.addEventListener('mouseleave', () => {
      this.targetMouseX = 0;
      this.targetMouseY = 0;
      this.updateFromScroll();
    });
  }

  updateFromScroll() {
    // Smooth mouse interpolation
    this.mouseX += (this.targetMouseX - this.mouseX) * 0.3;
    this.mouseY += (this.targetMouseY - this.mouseY) * 0.3;
    
    this.update(this.scrollProgress);
  }

  update(scrollProgress) {
    // Find keyframe pair to interpolate between
    let prev = this.keyframes[0];
    let next = this.keyframes[this.keyframes.length - 1];
    
    for (let i = 0; i < this.keyframes.length - 1; i++) {
      if (scrollProgress >= this.keyframes[i].scroll && scrollProgress <= this.keyframes[i + 1].scroll) {
        prev = this.keyframes[i];
        next = this.keyframes[i + 1];
        break;
      }
    }
    
    // Calculate interpolation factor
    const range = next.scroll - prev.scroll;
    const t = range > 0 ? (scrollProgress - prev.scroll) / range : 0;
    
    // Smooth interpolation (cubic bezier approximation)
    const smoothT = this.smoothstep(t);
    
    // Interpolate camera position
    this.position[0] = this.lerp(prev.pos[0], next.pos[0], smoothT);
    this.position[1] = this.lerp(prev.pos[1], next.pos[1], smoothT);
    this.position[2] = this.lerp(prev.pos[2], next.pos[2], smoothT);
    
    // Add mouse parallax (stronger when compressed)
    const parallaxStrength = 2.0 * (0.3 + scrollProgress * 0.7);
    this.position[0] += this.mouseX * parallaxStrength;
    this.position[1] += this.mouseY * parallaxStrength;
    
    // Interpolate FOV
    this.fov = this.lerp(prev.fov, next.fov, smoothT);
    
    // Update matrices
    this.updateMatrices();
  }

  updateMatrices() {
    const aspect = this.canvas.width / this.canvas.height;
    const near = 0.1;
    const far = 200;
    
    // Perspective projection matrix
    const f = 1.0 / Math.tan((this.fov * Math.PI / 180) / 2);
    this.projectionMatrix = new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) / (near - far), -1,
      0, 0, (2 * far * near) / (near - far), 0
    ]);
    
    // Simple view matrix (camera looking at origin)
    const target = [0, 0, 0];
    const up = [0, 1, 0];
    
    // Calculate view matrix
    this.viewMatrix = this.lookAt(this.position, target, up);
    
    // Combine view and projection
    this.viewProjectionMatrix = this.multiply4x4(this.projectionMatrix, this.viewMatrix);
  }

  lookAt(eye, target, up) {
    const zAxis = this.normalize([
      eye[0] - target[0],
      eye[1] - target[1],
      eye[2] - target[2]
    ]);
    const xAxis = this.normalize(this.cross(up, zAxis));
    const yAxis = this.cross(zAxis, xAxis);
    
    return new Float32Array([
      xAxis[0], yAxis[0], zAxis[0], 0,
      xAxis[1], yAxis[1], zAxis[1], 0,
      xAxis[2], yAxis[2], zAxis[2], 0,
      -this.dot(xAxis, eye), -this.dot(yAxis, eye), -this.dot(zAxis, eye), 1
    ]);
  }

  multiply4x4(a, b) {
    const result = new Float32Array(16);
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 4; j++) {
        result[i * 4 + j] = 
          a[i * 4 + 0] * b[0 * 4 + j] +
          a[i * 4 + 1] * b[1 * 4 + j] +
          a[i * 4 + 2] * b[2 * 4 + j] +
          a[i * 4 + 3] * b[3 * 4 + j];
      }
    }
    return result;
  }

  normalize(v) {
    const len = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    return [v[0] / len, v[1] / len, v[2] / len];
  }

  cross(a, b) {
    return [
      a[1] * b[2] - a[2] * b[1],
      a[2] * b[0] - a[0] * b[2],
      a[0] * b[1] - a[1] * b[0]
    ];
  }

  dot(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  }

  lerp(a, b, t) {
    return a + (b - a) * t;
  }

  smoothstep(t) {
    // Cubic smoothstep for natural camera movement
    return t * t * (3 - 2 * t);
  }

  getViewProjectionMatrix() {
    return this.viewProjectionMatrix;
  }

  getPosition() {
    return new Float32Array(this.position);
  }

  getFov() {
    return this.fov;
  }

  getScrollProgress() {
    return this.scrollProgress;
  }
}

// Export for use in particle system
window.CameraController = CameraController;
