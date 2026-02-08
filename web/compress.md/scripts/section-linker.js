/**
 * Section Linker — Links corresponding sections across the Original,
 * CRUX Compressed, and Decompressed panels.
 *
 * - Hover: temporarily highlights the matching section in both panels.
 * - Click: locks the highlight so it persists across tab switches,
 *          letting users compare the same section in Original vs Decompressed.
 * - Click again (or click outside): unlocks.
 *
 * Also manages the Original/Decompressed tab switching.
 */
(function () {
  'use strict';

  var SECTIONS = [
    { id: 'header',   original: /^# Comprehensive/,       crux: /⟦CRUX:|^Ρ\{|^Κ\{/,          decompressed: /^# Team Coding/ },
    { id: 'naming',   original: /### Naming Conventions/,  crux: /R\.naming\{/,                 decompressed: /## 1\) Naming/ },
    { id: 'style',    original: /### Code Style/,          crux: /R\.style\{|R\.format\{|R\.complexity\{/, decompressed: /## [234]\) (Code style|Formatting|Complexity)/ },
    { id: 'docs',     original: /### Documentation/,       crux: /R\.docs\{/,                   decompressed: /## 5\) Documentation/ },
    { id: 'errors',   original: /### Error Handling/,      crux: /P\.err\{|E\.err\{/,           decompressed: /## 6\) Error/ },
    { id: 'test',     original: /## Testing/,              crux: /R\.test\{/,                   decompressed: /## 7\) Testing/ },
    { id: 'arch',     original: /## Architecture/,         crux: /Π\.arch\{|Π\.src\{/,          decompressed: /## 8\) Architecture/ },
    { id: 'api',      original: /## API Design/,           crux: /R\.api\{/,                    decompressed: /## 9\) API/ },
    { id: 'git',      original: /## Git Workflow/,         crux: /R\.git\{/,                    decompressed: /## 10\) Git/ },
    { id: 'security', original: /## Security/,             crux: /P\.security\{/,               decompressed: /## 11\) Security/ },
    { id: 'db',       original: /## Database/,             crux: /R\.db\{/,                     decompressed: /## 12\) Database/ },
    { id: 'log',      original: /## Logging/,              crux: /R\.log\{/,                    decompressed: /## 13\) Logging/ },
    { id: 'perf',     original: /## Performance/,          crux: /R\.perf\{/,                   decompressed: /## 14\) Performance/ },
    { id: 'review',   original: /## Code Review/,          crux: /R\.review\{/,                 decompressed: /## 15\) Code review/ },
    { id: 'flags',    original: /## Feature Flags/,        crux: /E\.feature_flag\{/,           decompressed: /## 16\) Feature/ },
    { id: 'a11y',     original: /## Accessibility/,        crux: /R\.a11y\{/,                   decompressed: /## 17\) Accessibility/ },
    { id: 'release',  original: /## Release/,              crux: /R\.release\{/,                decompressed: /## 18\) Release/ },
    { id: 'summary',  original: /## Summary/,              crux: /^Ω\{/,                       decompressed: /## 19\) Quality/ }
  ];

  // Section display names for the lock indicator
  var SECTION_NAMES = {
    header: 'Header', naming: 'Naming', style: 'Code Style', docs: 'Docs',
    errors: 'Errors', test: 'Testing', arch: 'Architecture', api: 'API',
    git: 'Git', security: 'Security', db: 'Database', log: 'Logging',
    perf: 'Performance', review: 'Review', flags: 'Feature Flags',
    a11y: 'Accessibility', release: 'Release', summary: 'Summary'
  };

  function getLineText(tr) {
    var td = tr.querySelector('.code-line-content');
    return td ? td.textContent : '';
  }

  function findMatch(text, field) {
    for (var i = 0; i < SECTIONS.length; i++) {
      if (SECTIONS[i][field].test(text)) return SECTIONS[i].id;
    }
    return null;
  }

  function tagMarkdownRows(rows, field) {
    var current = null;
    for (var i = 0; i < rows.length; i++) {
      var text = getLineText(rows[i]);
      var match = findMatch(text, field);
      if (match) {
        current = match;
      } else if (/^#{1,2}\s/.test(text)) {
        current = null;
      }
      if (current) rows[i].setAttribute('data-section', current);
    }
  }

  function tagCruxRows(rows) {
    var current = null;
    for (var i = 0; i < rows.length; i++) {
      var text = getLineText(rows[i]);
      var match = findMatch(text, 'crux');
      if (match) {
        current = match;
      } else if (text.trim() === '') {
        current = null;
      }
      if (current) rows[i].setAttribute('data-section', current);
    }
  }

  // State
  var originalRows = [];
  var cruxRows = [];
  var decompressedRows = [];
  var activeTab = 'original';
  var currentHighlight = null;
  var lockedSection = null;      // null = unlocked, section id = locked
  var lockIndicator = null;      // DOM element for the lock badge

  function activeLeftRows() {
    return activeTab === 'original' ? originalRows : decompressedRows;
  }

  function visibleRows() {
    return activeLeftRows().concat(cruxRows);
  }

  /** Apply highlight/dim classes to visible rows for a given section. */
  function applyHighlight(sectionId, sourcePanel) {
    currentHighlight = sectionId;
    var visible = visibleRows();
    var firstOther = null;

    for (var i = 0; i < visible.length; i++) {
      var row = visible[i];
      if (row.dataset.section === sectionId) {
        row.classList.add('section-active');
        row.classList.remove('section-dimmed');
        if (!firstOther && row.dataset.panel !== sourcePanel) {
          firstOther = row;
        }
      } else {
        row.classList.remove('section-active');
        row.classList.add('section-dimmed');
      }
    }

    // Scroll the other panel to reveal the highlighted section
    if (firstOther) {
      var container = firstOther.closest('.demo-panel-content');
      if (container) {
        var rowRect = firstOther.getBoundingClientRect();
        var containerRect = container.getBoundingClientRect();
        var isVisible = rowRect.top >= containerRect.top &&
                        rowRect.bottom <= containerRect.bottom;
        if (!isVisible) {
          container.scrollBy({
            top: rowRect.top - containerRect.top - containerRect.height / 3,
            behavior: 'smooth'
          });
        }
      }
    }
  }

  function clearHighlights() {
    currentHighlight = null;
    var all = originalRows.concat(cruxRows, decompressedRows);
    for (var i = 0; i < all.length; i++) {
      all[i].classList.remove('section-active', 'section-dimmed');
    }
  }

  // ---- Lock indicator ----

  function createLockIndicator() {
    var el = document.createElement('div');
    el.className = 'section-lock-indicator';
    el.innerHTML =
      '<svg class="section-lock-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
        '<rect x="3" y="11" width="18" height="11" rx="2"/>' +
        '<path d="M7 11V7a5 5 0 0110 0v4"/>' +
      '</svg>' +
      '<span class="section-lock-name"></span>' +
      '<button class="section-lock-close" aria-label="Unlock section" title="Click to unlock">&times;</button>';
    el.style.display = 'none';

    // Insert after the panel tabs header
    var header = document.querySelector('.demo-panel-header--tabbed');
    if (header) header.parentNode.insertBefore(el, header.nextSibling);

    // Close button unlocks
    el.querySelector('.section-lock-close').addEventListener('click', function (e) {
      e.stopPropagation();
      unlock();
    });

    return el;
  }

  function showLockIndicator(sectionId) {
    if (!lockIndicator) return;
    lockIndicator.querySelector('.section-lock-name').textContent =
      SECTION_NAMES[sectionId] || sectionId;
    lockIndicator.style.display = '';
  }

  function hideLockIndicator() {
    if (lockIndicator) lockIndicator.style.display = 'none';
  }

  // ---- Lock / unlock ----

  function lock(sectionId) {
    lockedSection = sectionId;
    applyHighlight(sectionId, null);
    showLockIndicator(sectionId);
    // Add locked class to demo for visual feedback
    var demo = document.getElementById('compression-demo');
    if (demo) demo.classList.add('section-locked');
  }

  function unlock() {
    lockedSection = null;
    clearHighlights();
    hideLockIndicator();
    var demo = document.getElementById('compression-demo');
    if (demo) demo.classList.remove('section-locked');
  }

  // ---- Hover + Click handlers ----

  var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  function setupInteraction(panelContent, panelId) {
    // Hover: preview highlight (only on non-touch and when not locked)
    if (!isTouch) {
      panelContent.addEventListener('mouseover', function (e) {
        if (lockedSection) return;
        var tr = e.target.closest('tr[data-section]');
        if (tr) {
          applyHighlight(tr.dataset.section, panelId);
        } else {
          clearHighlights();
        }
      });

      panelContent.addEventListener('mouseleave', function () {
        if (lockedSection) return;
        clearHighlights();
      });
    }

    // Click / tap: toggle lock
    panelContent.addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-section]');
      if (!tr) {
        if (lockedSection) unlock();
        return;
      }

      var sectionId = tr.dataset.section;
      if (lockedSection === sectionId) {
        unlock();
      } else {
        lock(sectionId);
      }
    });
  }

  // ---- Tooltip hint ----

  function addHoverHint() {
    var demo = document.getElementById('compression-demo');
    if (!demo) return;
    var hint = document.createElement('p');
    hint.className = 'section-hover-hint';
    var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    hint.textContent = isTouch
      ? 'Tap a section to lock \u00B7 Tap again to unlock \u00B7 Switch tabs to compare'
      : 'Hover to preview sections \u00B7 Click to lock \u00B7 Switch tabs to compare';
    demo.parentNode.insertBefore(hint, demo.nextSibling);
  }

  // ---- Tab management ----

  function switchTab(target) {
    if (target === activeTab) return;
    activeTab = target;

    // Toggle panel visibility
    var originalPanel = document.getElementById('demo-original-panel');
    var decompressedPanel = document.getElementById('demo-decompressed-panel');

    if (target === 'original') {
      originalPanel.classList.remove('demo-panel-content--hidden');
      decompressedPanel.classList.add('demo-panel-content--hidden');
    } else {
      originalPanel.classList.add('demo-panel-content--hidden');
      decompressedPanel.classList.remove('demo-panel-content--hidden');
    }

    // Toggle tab active state
    var tabs = document.querySelectorAll('.demo-tab');
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].dataset.target === target) {
        tabs[i].classList.add('demo-tab--active');
      } else {
        tabs[i].classList.remove('demo-tab--active');
      }
    }

    // Update source tokens display
    var tokensEl = document.getElementById('demo-source-tokens');
    if (tokensEl) {
      tokensEl.textContent = target === 'original'
        ? '873 lines \u00B7 ~6,278 tokens'
        : '504 lines \u00B7 ChatGPT 5.2';
    }

    // Update reduction text
    var reductionText = document.getElementById('demo-reduction-text');
    var reductionFill = document.getElementById('reduction-bar-fill');
    if (target === 'original') {
      if (reductionText) reductionText.innerHTML = '<strong>83% reduction</strong> \u2014 same semantic information';
      if (reductionFill) reductionFill.style.width = '83%';
    } else {
      if (reductionText) reductionText.innerHTML = '<strong>504 lines</strong> reconstructed from 83 lines of CRUX';
      if (reductionFill) reductionFill.style.width = '83%';
    }

    // Re-apply locked section to new visible rows
    if (lockedSection) {
      clearHighlights();
      applyHighlight(lockedSection, null);
    }
  }

  function setupTabs() {
    var tabs = document.querySelectorAll('.demo-tab');
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].addEventListener('click', function () {
        switchTab(this.dataset.target);
      });
    }
  }

  // ---- Init ----

  function init() {
    var origCode = document.getElementById('demo-original-code');
    var cruxCode = document.getElementById('demo-crux-code');
    var decompCode = document.getElementById('demo-decompressed-code');

    if (!origCode || !cruxCode || !decompCode ||
        !origCode.classList.contains('has-line-numbers') ||
        !cruxCode.classList.contains('has-line-numbers') ||
        !decompCode.classList.contains('has-line-numbers')) {
      setTimeout(init, 200);
      return;
    }

    var origRows = origCode.querySelectorAll('tr');
    var crRows = cruxCode.querySelectorAll('tr');
    var decRows = decompCode.querySelectorAll('tr');

    tagMarkdownRows(origRows, 'original');
    tagCruxRows(crRows);
    tagMarkdownRows(decRows, 'decompressed');

    for (var i = 0; i < origRows.length; i++) {
      origRows[i].dataset.panel = 'original';
      originalRows.push(origRows[i]);
    }
    for (var j = 0; j < crRows.length; j++) {
      crRows[j].dataset.panel = 'crux';
      cruxRows.push(crRows[j]);
    }
    for (var k = 0; k < decRows.length; k++) {
      decRows[k].dataset.panel = 'decompressed';
      decompressedRows.push(decRows[k]);
    }

    // Create lock indicator
    lockIndicator = createLockIndicator();

    // Attach interaction handlers
    var originalPanel = document.getElementById('demo-original-panel');
    var cruxPanel = cruxCode.closest('.demo-panel-content');
    var decompPanel = document.getElementById('demo-decompressed-panel');

    if (originalPanel) setupInteraction(originalPanel, 'original');
    if (cruxPanel) setupInteraction(cruxPanel, 'crux');
    if (decompPanel) setupInteraction(decompPanel, 'decompressed');

    // Tabs and hint
    setupTabs();
    addHoverHint();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(init, 300);
    });
  } else {
    setTimeout(init, 300);
  }
})();
