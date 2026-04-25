/**
 * Shared Navigation Component
 * Generates the site nav with dropdown demos menu and GitHub link.
 * On the main page (with hero), nav appears on scroll.
 * On subpages, nav is always visible.
 */
(function () {
  'use strict';

  var GITHUB_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">' +
    '<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>' +
    '</svg>';

  var CHEVRON_SVG = '<svg class="site-nav-chevron" width="10" height="10" viewBox="0 0 10 10" fill="none">' +
    '<path d="M2.5 4L5 6.5L7.5 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  var HAMBURGER_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' +
    '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>' +
    '</svg>';

  var CLOSE_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' +
    '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>' +
    '</svg>';

  function buildNav() {
    var nav = document.getElementById('site-nav');
    if (!nav) return;

    var isMainPage = !!document.getElementById('hero');
    var prefix = isMainPage ? '' : 'index.html';

    nav.innerHTML =
      '<div class="site-nav-inner">' +
        '<a href="' + (isMainPage ? '#hero' : 'index.html') + '" class="site-nav-brand">CRUX</a>' +
        '<button class="site-nav-hamburger" aria-label="Toggle menu">' + HAMBURGER_SVG + '</button>' +
        '<div class="site-nav-links">' +
          '<div class="site-nav-dropdown">' +
            '<button class="site-nav-link site-nav-dropdown-toggle">Demos ' + CHEVRON_SVG + '</button>' +
            '<div class="site-nav-dropdown-menu">' +
              '<a href="demo-rules.html" class="site-nav-dropdown-item">AI Rules & Context</a>' +
              '<a href="demo-images.html" class="site-nav-dropdown-item">Images</a>' +
              '<a href="demo-code.html" class="site-nav-dropdown-item">Code</a>' +
              '<a href="demo-urls.html" class="site-nav-dropdown-item">URLs</a>' +
            '</div>' +
          '</div>' +
          '<a href="memories.html" class="site-nav-link">Memories</a>' +
          '<a href="notation.html" class="site-nav-link">Notation</a>' +
          '<a href="' + prefix + '#quickstart" class="site-nav-link">Quickstart</a>' +
          '<a href="https://github.com/zotoio/CRUX-Compress" class="site-nav-github" target="_blank" rel="noopener" title="View on GitHub">' + GITHUB_SVG + '</a>' +
        '</div>' +
      '</div>';

    if (!isMainPage) {
      nav.classList.add('is-visible', 'is-subpage');
    }

    initDropdown(nav);
    initHamburger(nav);
    highlightActive(nav);
  }

  function initDropdown(nav) {
    var toggle = nav.querySelector('.site-nav-dropdown-toggle');
    var menu = nav.querySelector('.site-nav-dropdown-menu');
    if (!toggle || !menu) return;

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.contains('is-open');
      menu.classList.toggle('is-open', !open);
      toggle.classList.toggle('is-open', !open);
    });

    document.addEventListener('click', function () {
      menu.classList.remove('is-open');
      toggle.classList.remove('is-open');
    });

    menu.addEventListener('click', function (e) { e.stopPropagation(); });
  }

  function initHamburger(nav) {
    var btn = nav.querySelector('.site-nav-hamburger');
    var links = nav.querySelector('.site-nav-links');
    if (!btn || !links) return;

    btn.addEventListener('click', function () {
      var open = links.classList.contains('is-mobile-open');
      links.classList.toggle('is-mobile-open', !open);
      btn.innerHTML = open ? HAMBURGER_SVG : CLOSE_SVG;
    });
  }

  function highlightActive(nav) {
    var path = window.location.pathname;
    var page = path.substring(path.lastIndexOf('/') + 1) || 'index.html';

    var demoPages = ['demo-rules.html', 'demo-images.html', 'demo-code.html', 'demo-urls.html'];
    var isDemoPage = demoPages.indexOf(page) !== -1;

    nav.querySelectorAll('.site-nav-link, .site-nav-dropdown-item').forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      if (href === page || (href === '#quickstart' && page === 'index.html')) {
        link.classList.add('is-active');
      }
    });

    if (isDemoPage) {
      var toggle = nav.querySelector('.site-nav-dropdown-toggle');
      if (toggle) toggle.classList.add('is-active');
    }
  }

  function loadFooterVersion() {
    fetch('version.json')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.version) return;
        var els = document.querySelectorAll('.footer-version');
        for (var i = 0; i < els.length; i++) {
          els[i].textContent = 'v' + data.version;
        }
      })
      .catch(function () {});
  }

  document.addEventListener('DOMContentLoaded', function () {
    buildNav();
    loadFooterVersion();
  });
})();
