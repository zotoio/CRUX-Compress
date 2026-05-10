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
        this.reductionFill.style.width = '83%';
      }, 800);
    }

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

    // CRUX output copy overlay buttons
    document.querySelectorAll('.crux-copy-btn').forEach(button => {
      button.addEventListener('click', async () => {
        const container = button.parentElement;
        const code = container.querySelector('code');
        if (!code) return;

        try {
          await navigator.clipboard.writeText(code.textContent);

          const originalHTML = button.innerHTML;
          button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
          `;
          button.classList.add('copied');

          setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('copied');
          }, 2000);
        } catch (err) {
          console.error('Failed to copy CRUX:', err);
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
  let ticking = false;
  
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
    
    if (Math.abs(progress - lastProgress) > 0.01) {
      lastProgress = progress;
      
      if (compressionFill) {
        compressionFill.style.width = `${progress * 100}%`;
      }
      
      const recovered = Math.round(progress * 80);
      if (percentage) {
        percentage.textContent = recovered;
      }
    }
    
    ticking = false;
  }
  
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(updateStats);
      ticking = true;
    }
  }, { passive: true });
  
  updateStats();
}

// Sticky nav: show after scrolling past hero (main page only)
function initSiteNav() {
  const nav = document.getElementById('site-nav');
  const hero = document.getElementById('hero');
  if (!nav || !hero) return;

  function update() {
    const heroBottom = hero.getBoundingClientRect().bottom;
    nav.classList.toggle('is-visible', heroBottom < 0);
  }

  let ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () { update(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });
  update();
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  new CompressionDemo();
  animateHeroStats();
  initSiteNav();
});