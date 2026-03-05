/**
 * Adapter Export Demo
 * - Switches assistant target output tabs
 * - Calculates duplicated edits and hours saved
 */
(function () {
  'use strict';

  function formatNumber(value, decimals) {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals || 0,
      maximumFractionDigits: decimals || 0
    }).format(value);
  }

  function setActiveTab(root, target) {
    var buttons = root.querySelectorAll('.adapter-target-button');
    var panels = root.querySelectorAll('.adapter-output-panel');

    for (var i = 0; i < buttons.length; i++) {
      var isActive = buttons[i].dataset.target === target;
      buttons[i].classList.toggle('adapter-target-button--active', isActive);
      buttons[i].setAttribute('aria-selected', String(isActive));
    }

    for (var j = 0; j < panels.length; j++) {
      var panelActive = panels[j].dataset.targetPanel === target;
      panels[j].classList.toggle('adapter-output-panel--active', panelActive);
    }
  }

  function updateCalculator(root) {
    var targetsInput = root.querySelector('#adapter-target-count');
    var updatesInput = root.querySelector('#adapter-update-count');
    var minutesInput = root.querySelector('#adapter-minutes-per-target');

    if (!targetsInput || !updatesInput || !minutesInput) {
      return;
    }

    var targets = Math.max(2, Number(targetsInput.value) || 2);
    var updates = Math.max(1, Number(updatesInput.value) || 1);
    var minutesPerTarget = Math.max(1, Number(minutesInput.value) || 1);

    var manualEdits = targets * updates;
    var exportedEdits = updates;
    var duplicatedEdits = manualEdits - exportedEdits;
    var reductionPercent = ((duplicatedEdits / manualEdits) * 100);
    var hoursSaved = (duplicatedEdits * minutesPerTarget) / 60;

    var reductionEl = root.querySelector('#adapter-reduction-percent');
    var editsEl = root.querySelector('#adapter-duplicated-edits');
    var hoursEl = root.querySelector('#adapter-hours-saved');

    if (reductionEl) {
      reductionEl.textContent = formatNumber(Math.round(reductionPercent));
    }

    if (editsEl) {
      editsEl.textContent = formatNumber(duplicatedEdits);
    }

    if (hoursEl) {
      hoursEl.textContent = formatNumber(hoursSaved, hoursSaved < 10 ? 1 : 0);
    }
  }

  function init() {
    var root = document.getElementById('adapter-export-demo');
    if (!root) {
      return;
    }

    var buttons = root.querySelectorAll('.adapter-target-button');
    var inputs = root.querySelectorAll('.adapter-calculator-input');

    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function () {
        setActiveTab(root, this.dataset.target);
      });
    }

    for (var j = 0; j < inputs.length; j++) {
      inputs[j].addEventListener('input', function () {
        updateCalculator(root);
      });
    }

    setActiveTab(root, 'cursor');
    updateCalculator(root);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
