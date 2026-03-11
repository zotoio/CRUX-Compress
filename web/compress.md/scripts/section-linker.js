/**
 * Section Linker — Links corresponding sections across the Original,
 * CRUX Compressed, and Decompressed panels in the rules gallery.
 *
 * - Hover: temporarily highlights the matching section in both panels.
 * - Click: locks the highlight so it persists across tab switches.
 * - Click again (or click outside): unlocks.
 *
 * Waits for gallery-loader + code-loader to finish before initializing.
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
    { id: 'api',      original: /## API Design/,           crux: /R\.api\{/,                   decompressed: /## 9\) API/ },
    { id: 'git',      original: /## Git Workflow/,         crux: /R\.git\{/,                   decompressed: /## 10\) Git/ },
    { id: 'security', original: /## Security/,             crux: /P\.security\{/,               decompressed: /## 11\) Security/ },
    { id: 'db',       original: /## Database/,             crux: /R\.db\{/,                    decompressed: /## 12\) Database/ },
    { id: 'log',      original: /## Logging/,              crux: /R\.log\{/,                   decompressed: /## 13\) Logging/ },
    { id: 'perf',     original: /## Performance/,          crux: /R\.perf\{/,                  decompressed: /## 14\) Performance/ },
    { id: 'review',   original: /## Code Review/,          crux: /R\.review\{/,                decompressed: /## 15\) Code review/ },
    { id: 'flags',    original: /## Feature Flags/,        crux: /E\.feature_flag\{/,          decompressed: /## 16\) Feature/ },
    { id: 'a11y',     original: /## Accessibility/,        crux: /R\.a11y\{/,                  decompressed: /## 17\) Accessibility/ },
    { id: 'release',  original: /## Release/,              crux: /R\.release\{/,               decompressed: /## 18\) Release/ },
    { id: 'summary',  original: /## Summary/,              crux: /^Ω\{/,                      decompressed: /## 19\) Quality/ }
  ];

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
      if (match) current = match;
      else if (/^#{1,2}\s/.test(text)) current = null;
      if (current) rows[i].setAttribute('data-section', current);
    }
  }

  function tagCruxRows(rows) {
    var current = null;
    for (var i = 0; i < rows.length; i++) {
      var text = getLineText(rows[i]);
      var match = findMatch(text, 'crux');
      if (match) current = match;
      else if (text.trim() === '') current = null;
      if (current) rows[i].setAttribute('data-section', current);
    }
  }

  var originalRows = [];
  var cruxRows = [];
  var decompressedRows = [];
  var currentHighlight = null;
  var lockedSection = null;
  var lockIndicator = null;
  var galleryContainer = null;
  var observerSetup = false;
  var reinitTimer = null;

  function visibleRows() {
    return originalRows.concat(cruxRows);
  }

  function applyHighlight(sectionId, sourcePanel) {
    currentHighlight = sectionId;
    var visible = originalRows.concat(cruxRows, decompressedRows);
    var firstOther = null;

    for (var i = 0; i < visible.length; i++) {
      var row = visible[i];
      if (row.dataset.section === sectionId) {
        row.classList.add('section-active');
        row.classList.remove('section-dimmed');
        if (!firstOther && row.dataset.panel !== sourcePanel) {
          var panel = row.closest('.demo-panel-content');
          if (panel && !panel.classList.contains('demo-panel-content--hidden')) {
            firstOther = row;
          }
        }
      } else {
        row.classList.remove('section-active');
        row.classList.add('section-dimmed');
      }
    }

    if (firstOther) {
      var container = firstOther.closest('.demo-panel-content');
      if (container) {
        var rowRect = firstOther.getBoundingClientRect();
        var containerRect = container.getBoundingClientRect();
        var isVisible = rowRect.top >= containerRect.top && rowRect.bottom <= containerRect.bottom;
        if (!isVisible) {
          container.scrollBy({ top: rowRect.top - containerRect.top - containerRect.height / 3, behavior: 'smooth' });
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

  function createLockIndicator(afterEl) {
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
    if (afterEl) afterEl.parentNode.insertBefore(el, afterEl.nextSibling);
    el.querySelector('.section-lock-close').addEventListener('click', function (e) {
      e.stopPropagation();
      unlock();
    });
    return el;
  }

  function showLockIndicator(sectionId) {
    if (!lockIndicator) return;
    lockIndicator.querySelector('.section-lock-name').textContent = SECTION_NAMES[sectionId] || sectionId;
    lockIndicator.style.display = '';
  }

  function hideLockIndicator() {
    if (lockIndicator) lockIndicator.style.display = 'none';
  }

  function lock(sectionId) {
    lockedSection = sectionId;
    applyHighlight(sectionId, null);
    showLockIndicator(sectionId);
    var demo = galleryContainer ? galleryContainer.querySelector('.compression-demo') : null;
    if (demo) demo.classList.add('section-locked');
  }

  function unlock() {
    lockedSection = null;
    clearHighlights();
    hideLockIndicator();
    var demo = galleryContainer ? galleryContainer.querySelector('.compression-demo') : null;
    if (demo) demo.classList.remove('section-locked');
  }

  var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  function setupInteraction(panelContent, panelId) {
    if (!isTouch) {
      panelContent.addEventListener('mouseover', function (e) {
        if (lockedSection) return;
        var tr = e.target.closest('tr[data-section]');
        if (tr) applyHighlight(tr.dataset.section, panelId);
        else clearHighlights();
      });
      panelContent.addEventListener('mouseleave', function () {
        if (lockedSection) return;
        clearHighlights();
      });
    }
    panelContent.addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-section]');
      if (!tr) { if (lockedSection) unlock(); return; }
      var sectionId = tr.dataset.section;
      if (lockedSection === sectionId) unlock();
      else lock(sectionId);
    });
  }

  function addHoverHint(demoEl) {
    if (!demoEl) return;
    var hint = document.createElement('p');
    hint.className = 'section-hover-hint';
    hint.textContent = isTouch
      ? 'Tap a section to lock \u00B7 Tap again to unlock \u00B7 Switch tabs to compare'
      : 'Hover to preview sections \u00B7 Click to lock \u00B7 Switch tabs to compare';
    demoEl.parentNode.insertBefore(hint, demoEl.nextSibling);
  }

  function scheduleReinit() {
    // Debounce re-initialization: multiple class mutations can fire in rapid
    // succession during a carousel transition; clearing the previous timer
    // ensures init() runs only once after the dust settles.
    clearTimeout(reinitTimer);
    reinitTimer = setTimeout(init, 300);
  }

  function init() {
    galleryContainer = document.querySelector('[data-gallery="rules"]');
    if (!galleryContainer) return;

    var activeItem = galleryContainer.querySelector('.gallery-item--active');
    if (!activeItem) { setTimeout(init, 300); return; }

    var codeBlocks = activeItem.querySelectorAll('code.has-line-numbers');
    if (codeBlocks.length < 2) { setTimeout(init, 300); return; }

    var beforePanel = activeItem.querySelector('.demo-panel--before');
    var afterPanel = activeItem.querySelector('.demo-panel--after');
    if (!beforePanel || !afterPanel) return;

    var origPanelContent = beforePanel.querySelector('.demo-panel-content:not(.demo-panel-content--hidden)');
    var cruxPanelContent = afterPanel.querySelector('.demo-panel-content');
    var decompPanelContents = beforePanel.querySelectorAll('.demo-panel-content.demo-panel-content--hidden');

    if (!origPanelContent || !cruxPanelContent) return;

    var origCode = origPanelContent.querySelector('code.has-line-numbers');
    var cruxCode = cruxPanelContent.querySelector('code.has-line-numbers');
    if (!origCode || !cruxCode) { setTimeout(init, 300); return; }

    // Remove any existing hover hints before rebuilding
    var oldHints = galleryContainer.querySelectorAll('.section-hover-hint');
    for (var h = 0; h < oldHints.length; h++) {
      oldHints[h].parentNode.removeChild(oldHints[h]);
    }

    // Clear state before rebuilding
    originalRows = [];
    cruxRows = [];
    decompressedRows = [];
    clearHighlights();
    if (lockedSection) {
      lockedSection = null;
      if (lockIndicator && lockIndicator.parentNode) {
        lockIndicator.parentNode.removeChild(lockIndicator);
        lockIndicator = null;
      }
    }

    var origTableRows = origCode.querySelectorAll('tr');
    var cruxTableRows = cruxCode.querySelectorAll('tr');

    tagMarkdownRows(origTableRows, 'original');
    tagCruxRows(cruxTableRows);

    for (var i = 0; i < origTableRows.length; i++) {
      origTableRows[i].dataset.panel = 'original';
      originalRows.push(origTableRows[i]);
    }
    for (var j = 0; j < cruxTableRows.length; j++) {
      cruxTableRows[j].dataset.panel = 'crux';
      cruxRows.push(cruxTableRows[j]);
    }

    for (var d = 0; d < decompPanelContents.length; d++) {
      var decompCode = decompPanelContents[d].querySelector('code.has-line-numbers');
      if (decompCode) {
        var decRows = decompCode.querySelectorAll('tr');
        tagMarkdownRows(decRows, 'decompressed');
        for (var k = 0; k < decRows.length; k++) {
          decRows[k].dataset.panel = 'decompressed';
          decompressedRows.push(decRows[k]);
        }
      }
    }

    var tabbedHeader = beforePanel.querySelector('.demo-panel-header--tabbed');
    if (tabbedHeader) lockIndicator = createLockIndicator(tabbedHeader);

    setupInteraction(origPanelContent, 'original');
    setupInteraction(cruxPanelContent, 'crux');
    for (var dp = 0; dp < decompPanelContents.length; dp++) {
      setupInteraction(decompPanelContents[dp], 'decompressed');
    }

    var demo = activeItem.querySelector('.compression-demo');
    addHoverHint(demo);

    // Set up gallery-navigation observers once to avoid duplicate registrations.
    // Uses a MutationObserver to detect when a gallery item gains the
    // gallery-item--active class (carousel navigation), then clears and rebuilds
    // the row arrays so they always point to the current active item's DOM.
    if (!observerSetup) {
      observerSetup = true;
      var navObserver = new MutationObserver(function (mutations) {
        for (var mutationIndex = 0; mutationIndex < mutations.length; mutationIndex++) {
          var target = mutations[mutationIndex].target;
          if (target.classList &&
              target.classList.contains('gallery-item') &&
              target.classList.contains('gallery-item--active')) {
            scheduleReinit();
            return;
          }
        }
      });
      navObserver.observe(galleryContainer, {
        attributes: true,
        attributeFilter: ['class'],
        subtree: true
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(init, 500); });
  } else {
    setTimeout(init, 500);
  }
})();