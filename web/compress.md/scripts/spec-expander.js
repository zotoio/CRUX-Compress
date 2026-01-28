/**
 * Spec Explorer - Interactive Notation Reference
 * Expandable/collapsible sections for CRUX notation symbols
 */

class SpecExpander {
  constructor() {
    this.explorer = document.getElementById('spec-explorer');
    this.sections = [];
    
    if (this.explorer) {
      this.init();
    }
  }

  init() {
    this.sections = this.explorer.querySelectorAll('.spec-section');
    
    this.sections.forEach(section => {
      const header = section.querySelector('.spec-section-header');
      
      header.addEventListener('click', () => {
        this.toggle(section);
      });

      // Keyboard accessibility
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.toggle(section);
        }
      });
    });

    // Scroll-triggered reveal animation
    this.setupScrollAnimation();
  }

  toggle(section) {
    const isOpen = section.classList.contains('is-open');
    
    // Close all other sections (accordion behavior)
    // Uncomment for accordion mode:
    // this.sections.forEach(s => s.classList.remove('is-open'));
    
    if (isOpen) {
      section.classList.remove('is-open');
    } else {
      section.classList.add('is-open');
      
      // Animate content height
      const content = section.querySelector('.spec-section-content');
      if (content) {
        content.style.maxHeight = content.scrollHeight + 'px';
        setTimeout(() => {
          content.style.maxHeight = 'none';
        }, 300);
      }
    }
  }

  setupScrollAnimation() {
    const options = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateSections();
          observer.unobserve(entry.target);
        }
      });
    }, options);

    if (this.explorer) {
      observer.observe(this.explorer);
    }
  }

  animateSections() {
    this.sections.forEach((section, index) => {
      section.style.opacity = '0';
      section.style.transform = 'translateY(20px)';
      
      setTimeout(() => {
        section.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        section.style.opacity = '1';
        section.style.transform = 'translateY(0)';
      }, index * 50);
    });
  }

  // Expand specific section by group name
  expand(groupName) {
    const section = this.explorer.querySelector(`[data-group="${groupName}"]`);
    if (section && !section.classList.contains('is-open')) {
      this.toggle(section);
    }
  }

  // Collapse all sections
  collapseAll() {
    this.sections.forEach(section => {
      section.classList.remove('is-open');
    });
  }

  // Expand all sections
  expandAll() {
    this.sections.forEach(section => {
      section.classList.add('is-open');
    });
  }
}

/**
 * Scroll-triggered animations for all sections
 */
class ScrollAnimator {
  constructor() {
    this.elements = document.querySelectorAll('.section-title, .section-intro, .experimental-warning, .install-section, .installed-section, .usage-section');
    this.init();
  }

  init() {
    const options = {
      root: null,
      rootMargin: '0px 0px -50px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, options);

    this.elements.forEach(el => {
      el.classList.add('animate-on-scroll');
      observer.observe(el);
    });
  }
}

/**
 * Smooth scroll for anchor links
 */
class SmoothScroll {
  constructor() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
}

/**
 * Context Window Animation
 * Animates the problem visualization
 */
class ContextWindowAnimation {
  constructor() {
    this.contextWindow = document.querySelector('.context-window');
    this.rulesSegment = document.querySelector('.context-segment--rules');
    
    if (this.contextWindow) {
      this.setupObserver();
    }
  }

  setupObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animate();
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    observer.observe(this.contextWindow);
  }

  animate() {
    if (this.rulesSegment) {
      // Animate the rules segment growing
      this.rulesSegment.style.transition = 'width 1.5s ease-out';
      
      // Start small, grow to show the problem
      this.rulesSegment.style.width = '10%';
      
      setTimeout(() => {
        this.rulesSegment.style.width = '70%';
      }, 500);
    }
  }
}

// Initialize all components on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.specExpander = new SpecExpander();
  new ScrollAnimator();
  new SmoothScroll();
  new ContextWindowAnimation();
});
