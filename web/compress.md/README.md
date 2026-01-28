# compress.md Landing Page

A single-page static website showcasing CRUX-Compress — a semantic compression notation for reducing AI context window consumption.

## Overview

This landing page features:

- **WebGPU 3D Visualization**: Interactive particle system showing tokens compressing into CRUX symbols
- **Scroll-linked Camera**: Camera movement tied to scroll position for cinematic experience
- **Live Compression Demo**: Side-by-side before/after comparison of verbose markdown vs CRUX notation
- **Interactive Spec Explorer**: Expandable sections documenting all CRUX symbols and blocks
- **Quickstart Guide**: Installation and usage instructions

## Tech Stack

- Pure HTML/CSS/JavaScript (no build step required)
- WebGPU for 3D particle rendering
- WGSL shaders for compute and render pipelines
- CSS custom properties for theming
- Intersection Observer for scroll animations

## Browser Support

### WebGPU Required (for 3D visualization)
- Chrome 113+
- Edge 113+
- Firefox Nightly (with WebGPU flag enabled)
- Safari 18+ (limited support)

### Fallback
Browsers without WebGPU support will see a static CSS-animated fallback with floating particles.

## Local Development

1. Serve the files with any static file server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js (npx)
npx serve .

# Using PHP
php -S localhost:8000
```

2. Open http://localhost:8000 in a WebGPU-supported browser

## Deployment

This site is designed for GitHub Pages deployment:

1. Push to your repository
2. Enable GitHub Pages in repository settings
3. Set source to the appropriate branch/folder

Alternatively, deploy to any static hosting service:
- Netlify
- Vercel
- Cloudflare Pages
- AWS S3 + CloudFront

## File Structure

```
compress.md/
├── index.html              # Main page with all content
├── styles/
│   └── main.css           # All styles with CSS custom properties
├── scripts/
│   ├── webgpu-init.js     # WebGPU setup and fallback detection
│   ├── particle-system.js # Particle simulation and rendering
│   ├── camera-controller.js # Scroll-linked camera movement
│   ├── compression-demo.js  # Before/after animation
│   └── spec-expander.js   # Interactive specification explorer
├── shaders/
│   ├── particle.wgsl      # Compute and render shaders for particles
│   └── symbol.wgsl        # CRUX symbol SDF rendering
├── assets/
│   ├── favicon.svg        # CRUX-themed favicon
│   └── og-image.png       # Social sharing image (to be added)
└── README.md              # This file
```

## Design Principles

- **No purple, no standard AI gradients** — Uses deep teals, warm ambers, and charcoal blacks
- **Asymmetric, editorial layout** — Intentional whitespace, not generic card grids
- **Purposeful animation** — Every motion communicates compression
- **Performance first** — Target ≤3s first meaningful paint on 4G
- **Honest messaging** — Clear experimental status throughout

## Color Palette

| Purpose | Hex | Description |
|---------|-----|-------------|
| Background Primary | `#0a0f0f` | Near-black with teal undertone |
| Background Secondary | `#141c1c` | Dark teal-gray |
| Background Tertiary | `#1e2a2a` | Code block background |
| Text Primary | `#e8eeee` | Warm white |
| Accent Verbose | `#5b8a9a` | Cool teal (uncompressed) |
| Accent Compressed | `#d4915a` | Warm amber (compressed) |
| Accent Symbol | `#f0c674` | Bright gold (CRUX symbols) |

## License

MIT License — see [LICENSE.md](../../LICENSE.md) in the repository root.

## Links

- [CRUX-Compress Repository](https://github.com/zotoio/CRUX-Compress)
- [Full CRUX Specification](https://github.com/zotoio/CRUX-Compress/blob/main/CRUX.md)
- [Report Issues](https://github.com/zotoio/CRUX-Compress/issues)
