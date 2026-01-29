/**
 * Compression Demo
 * Animates the before/after code comparison on scroll
 */

class CompressionDemo {
  constructor() {
    this.demo = document.getElementById('compression-demo');
    this.beforePanel = document.querySelector('.demo-panel--before');
    this.afterPanel = document.querySelector('.demo-panel--after');
    this.reductionFill = document.getElementById('reduction-bar-fill');
    this.isVisible = false;
    this.hasAnimated = false;
    
    this.setupObserver();
    this.setupCopyButtons();
  }

  setupObserver() {
    const options = {
      root: null,
      rootMargin: '0px',
      threshold: 0.3
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !this.hasAnimated) {
          this.animate();
          this.hasAnimated = true;
        }
      });
    }, options);

    if (this.demo) {
      observer.observe(this.demo);
    }
  }

  animate() {
    // Animate the panels appearing
    if (this.beforePanel) {
      this.beforePanel.style.opacity = '0';
      this.beforePanel.style.transform = 'translateX(-20px)';
      
      setTimeout(() => {
        this.beforePanel.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        this.beforePanel.style.opacity = '1';
        this.beforePanel.style.transform = 'translateX(0)';
      }, 100);
    }

    if (this.afterPanel) {
      this.afterPanel.style.opacity = '0';
      this.afterPanel.style.transform = 'translateX(20px)';
      
      setTimeout(() => {
        this.afterPanel.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        this.afterPanel.style.opacity = '1';
        this.afterPanel.style.transform = 'translateX(0)';
      }, 400);
    }

    // Animate the reduction bar
    if (this.reductionFill) {
      this.reductionFill.style.width = '0%';
      
      setTimeout(() => {
        this.reductionFill.style.transition = 'width 1s ease-out';
        this.reductionFill.style.width = '82%';
      }, 800);
    }

    // Animate line-by-line highlighting (optional enhancement)
    this.animateCodeLines();
  }

  animateCodeLines() {
    const beforeCode = document.getElementById('demo-before-code');
    const afterCode = document.getElementById('demo-after-code');
    
    if (!beforeCode || !afterCode) return;

    // Add highlighting effect to show transformation
    const beforeLines = beforeCode.textContent.split('\n');
    const afterLines = afterCode.textContent.split('\n');

    // Wrap lines in spans for animation (join without \n since spans are display:block)
    beforeCode.innerHTML = beforeLines.map((line, i) => 
      `<span class="code-line" style="animation-delay: ${i * 50}ms">${this.escapeHtml(line)}</span>`
    ).join('');

    afterCode.innerHTML = afterLines.map((line, i) => 
      `<span class="code-line code-line--crux" style="animation-delay: ${i * 100 + 500}ms">${this.highlightCrux(line)}</span>`
    ).join('');

    // Add animation styles
    this.addAnimationStyles();
  }

  highlightCrux(line) {
    // Highlight CRUX symbols - avoid = and ; as they break HTML attributes
    const symbols = ['⟦', '⟧', 'Ρ', 'Κ', 'Λ', 'Ω', '→', '←', '∀', '¬', '≻', '⊤', '⊥', '≤', '≥'];
    const blocks = ['⟦CRUX:', '.style', '.docs'];
    
    let result = this.escapeHtml(line);
    
    // Highlight symbols first (before adding HTML that contains these chars)
    symbols.forEach(symbol => {
      result = result.replace(new RegExp(this.escapeRegex(symbol), 'g'), 
        `<span class="crux-symbol">${symbol}</span>`);
    });
    
    // Highlight block identifiers (these don't conflict with HTML)
    blocks.forEach(block => {
      const escapedBlock = this.escapeHtml(block);
      result = result.replace(new RegExp(this.escapeRegex(escapedBlock), 'g'), 
        `<span class="crux-block">${escapedBlock}</span>`);
    });
    
    return result;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  addAnimationStyles() {
    if (document.getElementById('compression-demo-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'compression-demo-styles';
    style.textContent = `
      .code-line {
        display: block;
        opacity: 0;
        animation: fadeInLine 0.3s ease forwards;
      }
      
      @keyframes fadeInLine {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
      }
      
      .code-line--crux {
        animation-name: fadeInCruxLine;
      }
      
      @keyframes fadeInCruxLine {
        from { opacity: 0; transform: translateX(10px); }
        to { opacity: 1; transform: translateX(0); }
      }
      
      .crux-symbol {
        color: #f0c674;
        font-weight: 600;
      }
      
      .crux-block {
        color: #d4915a;
      }
    `;
    document.head.appendChild(style);
  }

  setupCopyButtons() {
    document.querySelectorAll('.copy-button').forEach(button => {
      button.addEventListener('click', async () => {
        const text = button.dataset.copy;
        
        try {
          await navigator.clipboard.writeText(text);
          
          const originalText = button.innerHTML;
          button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            Copied!
          `;
          button.classList.add('copied');
          
          setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('copied');
          }, 2000);
        } catch (err) {
          console.error('Failed to copy:', err);
        }
      });
    });
  }
}

// Try-it examples for interactive demo
const tryItExamples = {
  apiRules: `⟦CRUX:api-rules
Ρ{REST API design standards}
R{∀endpoint→versioned(/v{n}/);auth=JWT|API_KEY;rate.limit=100/min}
P.response{success→{data,meta};error→{code,message,details?}}
Λ{5xx→retry»backoff[max=3];429→wait(retry-after)}
Γ{req»validate»auth»process»respond}
Ω{consistency≻flexibility;explicit≻implicit;¬halluc}
⟧`,
  
  codeModProtocol: `⟦CRUX:code-mod-protocol
R=req→truth;gap→assume+mark;?arch→ask first
C=obs→cite path:lines;repo≻chat
Δ=R≠C→tag{code|tests|req}+why
PLAN=min files+targeted Δ;justify+file|broad
PATCH=surgical diff;¬rewrite w/o proof
CHECK=run»+tests|static val
STATE={R,C,Δ}→upd on progress
Ω{¬halluc;verified only}
⟧`
};

// Hero Stats Animation - animates compression bar and percentage based on scroll
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

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  new CompressionDemo();
  animateHeroStats();
});
