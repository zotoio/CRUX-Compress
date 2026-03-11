(function () {
  'use strict';

  var ARROW_SVG = '<svg width="48" height="48" viewBox="0 0 48 48" fill="none">' +
    '<path d="M8 24h32M32 16l8 8-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  var COPY_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<rect x="9" y="9" width="13" height="13" rx="2"/>' +
    '<path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>' +
    '</svg>';

  var NAV_PREV_SVG = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">' +
    '<path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  var NAV_NEXT_SVG = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none">' +
    '<path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  var MODEL_DISPLAY_NAMES = {
    'unknown': 'LLM',
    'html': 'HTML Page',
    'nano-banana-2': 'Nano Banana 2',
    'gpt4o': 'GPT-4o',
    'gpt4': 'GPT-4',
    'chatgpt52': 'ChatGPT 5.2',
    'chatgpt': 'ChatGPT',
    'claude': 'Claude',
    'gemini': 'Gemini',
    'sonnet': 'Sonnet',
    'opus': 'Opus'
  };

  function displayModel(model) {
    return MODEL_DISPLAY_NAMES[model] || model.charAt(0).toUpperCase() + model.slice(1);
  }

  function formatBytes(bytes) {
    var n = parseInt(bytes, 10);
    if (isNaN(n)) return bytes;
    if (n >= 1048576) return (n / 1048576).toFixed(1) + ' MB';
    if (n >= 1024) return (n / 1024).toFixed(1) + ' KB';
    return n + ' B';
  }

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'className') e.className = attrs[k];
        else if (k === 'innerHTML') e.innerHTML = attrs[k];
        else if (k === 'textContent') e.textContent = attrs[k];
        else e.setAttribute(k, attrs[k]);
      });
    }
    if (children) {
      (Array.isArray(children) ? children : [children]).forEach(function (c) {
        if (typeof c === 'string') e.appendChild(document.createTextNode(c));
        else if (c) e.appendChild(c);
      });
    }
    return e;
  }

  function copyBtn() {
    var btn = el('button', { className: 'crux-copy-btn', 'aria-label': 'Copy CRUX output', title: 'Copy to clipboard', innerHTML: COPY_SVG });
    btn.addEventListener('click', function () {
      var code = btn.parentElement.querySelector('code');
      if (!code) return;
      var text = code.textContent;
      navigator.clipboard.writeText(text).then(function () {
        btn.classList.add('copied');
        setTimeout(function () { btn.classList.remove('copied'); }, 1500);
      }).catch(function () {
        btn.title = 'Copy failed – check clipboard permissions';
        setTimeout(function () { btn.title = 'Copy to clipboard'; }, 2000);
      });
    });
    return btn;
  }

  function arrow(cssClass) {
    return el('div', { className: cssClass, innerHTML: ARROW_SVG });
  }

  function modelSelector(decompressed, onSelect) {
    if (!decompressed || decompressed.length <= 1) return null;
    var wrap = el('div', { className: 'model-selector' });
    decompressed.forEach(function (d, i) {
      var btn = el('button', {
        className: 'model-selector-btn' + (i === 0 ? ' model-selector-btn--active' : ''),
        textContent: displayModel(d.model),
        'data-model': d.model
      });
      btn.addEventListener('click', function () {
        wrap.querySelectorAll('.model-selector-btn').forEach(function (b) {
          b.classList.remove('model-selector-btn--active');
        });
        btn.classList.add('model-selector-btn--active');
        onSelect(d, i);
      });
      wrap.appendChild(btn);
    });
    return wrap;
  }

  function placeholderCard(label) {
    var card = el('div', { className: 'image-demo-card image-demo-card--placeholder' });
    card.appendChild(el('div', { className: 'image-demo-card-header' }, [
      el('span', { className: 'image-demo-card-label', textContent: label })
    ]));
    var content = el('div', { className: 'image-demo-card-content image-demo-placeholder' });
    content.appendChild(el('span', { textContent: 'No image available' }));
    card.appendChild(content);
    return card;
  }

  // ── Renderers ──

  function renderRulesItem(item, basePath) {
    var frag = document.createDocumentFragment();
    var demo = el('div', { className: 'compression-demo' });

    // Left panel: original + decompressed tabs
    var leftPanel = el('div', { className: 'demo-panel demo-panel--before' });
    var header = el('div', { className: 'demo-panel-header demo-panel-header--tabbed' });
    var tabs = el('div', { className: 'demo-panel-tabs' });
    var tabOriginal = el('button', { className: 'demo-tab demo-tab--active', 'data-target': 'original', textContent: 'ORIGINAL' });
    var tabDecomp = el('button', { className: 'demo-tab', 'data-target': 'decompressed', textContent: 'DECOMPRESSED' });
    tabs.appendChild(tabOriginal);
    tabs.appendChild(tabDecomp);
    header.appendChild(tabs);
    var tokenSpan = null;
    if (item.meta.sourceTokens) {
      tokenSpan = el('span', { className: 'demo-panel-tokens', textContent: item.meta.sourceTokens + ' tokens' });
      header.appendChild(tokenSpan);
    }
    leftPanel.appendChild(header);

    var originalPanel = el('div', { className: 'demo-panel-content' });
    var origPre = el('pre');
    var langClass = 'language-markdown';
    origPre.appendChild(el('code', { className: langClass, 'data-src': basePath + '/' + item.name + '.source.' + item.sourceExt, textContent: 'Loading...' }));
    originalPanel.appendChild(origPre);
    leftPanel.appendChild(originalPanel);

    var decompPanels = [];
    item.decompressed.forEach(function (d, i) {
      var panel = el('div', { className: 'demo-panel-content demo-panel-content--hidden', 'data-model': d.model });
      var pre = el('pre');
      pre.appendChild(el('code', { className: langClass, 'data-src': basePath + '/' + item.name + '.decompressed-' + d.model + '.' + d.ext, textContent: 'Loading...' }));
      panel.appendChild(pre);
      leftPanel.appendChild(panel);
      decompPanels.push(panel);
    });

    var ms = null;
    if (item.decompressed.length > 1) {
      ms = modelSelector(item.decompressed, function (d) {
        decompPanels.forEach(function (p) {
          p.classList.toggle('demo-panel-content--hidden', p.getAttribute('data-model') !== d.model);
        });
      });
    }

    function switchTab(target) {
      tabOriginal.classList.toggle('demo-tab--active', target === 'original');
      tabDecomp.classList.toggle('demo-tab--active', target === 'decompressed');
      originalPanel.classList.toggle('demo-panel-content--hidden', target !== 'original');
      decompPanels.forEach(function (p, i) {
        if (target === 'decompressed') {
          var activeModel = ms ? ms.querySelector('.model-selector-btn--active') : null;
          var model = activeModel ? activeModel.getAttribute('data-model') : item.decompressed[0].model;
          p.classList.toggle('demo-panel-content--hidden', p.getAttribute('data-model') !== model);
        } else {
          p.classList.add('demo-panel-content--hidden');
        }
      });
      if (ms) ms.style.display = target === 'decompressed' ? '' : 'none';
      if (tokenSpan) {
        tokenSpan.textContent = item.meta.sourceTokens + ' tokens';
      }
    }

    tabOriginal.addEventListener('click', function () { switchTab('original'); });
    tabDecomp.addEventListener('click', function () { switchTab('decompressed'); });

    demo.appendChild(leftPanel);
    demo.appendChild(arrow('demo-arrow'));

    // Right panel: CRUX
    var rightPanel = el('div', { className: 'demo-panel demo-panel--after' });
    var rHeader = el('div', { className: 'demo-panel-header' });
    rHeader.appendChild(el('span', { className: 'demo-panel-title', textContent: 'CRUX COMPRESSED' }));
    if (item.meta.cruxTokens) {
      rHeader.appendChild(el('span', { className: 'demo-panel-tokens', textContent: item.meta.cruxTokens + ' tokens' }));
    }
    rightPanel.appendChild(rHeader);
    var rContent = el('div', { className: 'demo-panel-content' });
    rContent.appendChild(copyBtn());
    var rPre = el('pre');
    rPre.appendChild(el('code', { className: 'language-crux', 'data-src': basePath + '/' + item.name + '.crux.md', 'data-extract': 'crux', textContent: 'Loading...' }));
    rContent.appendChild(rPre);
    rightPanel.appendChild(rContent);
    demo.appendChild(rightPanel);

    frag.appendChild(demo);

    if (ms) {
      ms.style.display = 'none';
      frag.appendChild(ms);
    }

    if (item.meta.reduction) {
      var reduction = el('div', { className: 'demo-reduction' });
      var bar = el('div', { className: 'reduction-bar' });
      var fill = el('div', { className: 'reduction-bar-fill' });
      fill.style.width = item.meta.reduction;
      bar.appendChild(fill);
      reduction.appendChild(bar);
      var reductionText = el('p', { className: 'reduction-text' });
      var strong = el('strong', { textContent: item.meta.reduction + ' reduction' });
      reductionText.appendChild(strong);
      reductionText.appendChild(document.createTextNode(' — same semantic information'));
      reduction.appendChild(reductionText);
      frag.appendChild(reduction);
    }
    return frag;
  }

  function renderCodeItem(item, basePath) {
    var frag = document.createDocumentFragment();
    var demo = el('div', { className: 'code-demo' });
    var row = el('div', { className: 'code-demo-row' });

    // Original
    var origCard = el('div', { className: 'code-demo-card' });
    var origHeader = el('div', { className: 'code-demo-card-header' });
    origHeader.appendChild(el('span', { className: 'code-demo-card-label', textContent: 'Original' }));
    if (item.meta.sourceTokens) {
      origHeader.appendChild(el('span', { className: 'code-demo-card-meta', textContent: item.meta.sourceTokens + ' tokens' }));
    }
    origCard.appendChild(origHeader);
    var origContent = el('div', { className: 'code-demo-card-content' });
    var origPre = el('pre');
    var langMap = { sh: 'bash', bash: 'bash', ts: 'typescript', js: 'javascript', py: 'python' };
    var lang = langMap[item.sourceExt] || item.sourceExt;
    origPre.appendChild(el('code', { className: 'language-' + lang, 'data-src': basePath + '/' + item.name + '.source.' + item.sourceExt, textContent: 'Loading...' }));
    origContent.appendChild(origPre);
    origCard.appendChild(origContent);
    row.appendChild(origCard);

    row.appendChild(arrow('code-demo-arrow'));

    // CRUX
    var cruxCard = el('div', { className: 'code-demo-card code-demo-card--crux' });
    var cruxHeader = el('div', { className: 'code-demo-card-header' });
    cruxHeader.appendChild(el('span', { className: 'code-demo-card-label', textContent: 'CRUX Compressed' }));
    if (item.meta.cruxTokens) {
      cruxHeader.appendChild(el('span', { className: 'code-demo-card-meta', textContent: item.meta.cruxTokens + ' tokens' }));
    }
    cruxCard.appendChild(cruxHeader);
    var cruxContent = el('div', { className: 'code-demo-card-content' });
    cruxContent.appendChild(copyBtn());
    var cruxPre = el('pre');
    cruxPre.appendChild(el('code', { className: 'language-crux', 'data-src': basePath + '/' + item.name + '.crux.md', 'data-extract': 'crux', textContent: 'Loading...' }));
    cruxContent.appendChild(cruxPre);
    cruxCard.appendChild(cruxContent);
    row.appendChild(cruxCard);
    demo.appendChild(row);

    // Reduction stats
    if (item.meta.reduction) {
      var stats = el('div', { className: 'code-demo-reduction' });
      stats.appendChild(el('div', { className: 'code-demo-stat' }, [
        el('span', { className: 'code-demo-stat-value', textContent: item.meta.reduction }),
        el('span', { className: 'code-demo-stat-label', textContent: 'token reduction' })
      ]));
      demo.appendChild(stats);
    }

    // Decompressed
    if (item.decompressed.length > 0) {
      var decompSection = el('div', { className: 'code-demo-decompressed' });
      decompSection.appendChild(el('h3', { textContent: 'Decompressed by ' + displayModel(item.decompressed[0].model) }));

      var decompCards = [];
      item.decompressed.forEach(function (d, i) {
        var dRow = el('div', { className: 'code-demo-decompressed-row', 'data-model': d.model });
        if (i > 0) dRow.style.display = 'none';
        var dCard = el('div', { className: 'code-demo-card code-demo-card--decompressed' });
        var dHeader = el('div', { className: 'code-demo-card-header' });
        dHeader.appendChild(el('span', { className: 'code-demo-card-label', textContent: displayModel(d.model) + ' (from .crux.md only)' }));
        dCard.appendChild(dHeader);
        var dContent = el('div', { className: 'code-demo-card-content' });
        var dPre = el('pre');
        var dLang = langMap[d.ext] || d.ext;
        dPre.appendChild(el('code', { className: 'language-' + dLang, 'data-src': basePath + '/' + item.name + '.decompressed-' + d.model + '.' + d.ext, textContent: 'Loading...' }));
        dContent.appendChild(dPre);
        dCard.appendChild(dContent);
        dRow.appendChild(dCard);
        decompCards.push(dRow);
        decompSection.appendChild(dRow);
      });

      var ms = modelSelector(item.decompressed, function (d) {
        var heading = decompSection.querySelector('h3');
        if (heading) heading.textContent = 'Decompressed by ' + displayModel(d.model);
        decompCards.forEach(function (c) {
          c.style.display = c.getAttribute('data-model') === d.model ? '' : 'none';
        });
      });
      if (ms) decompSection.insertBefore(ms, decompSection.children[1]);

      demo.appendChild(decompSection);
    }

    frag.appendChild(demo);
    return frag;
  }

  function renderImageItem(item, basePath) {
    var frag = document.createDocumentFragment();
    var demo = el('div', { className: 'image-demo' });
    var row = el('div', { className: 'image-demo-row' });

    // Left column: original image + decompressed stacked vertically
    var leftCol = el('div', { className: 'image-demo-left' });

    if (item.hasSource) {
      var origCard = el('div', { className: 'image-demo-card' });
      var origHeader = el('div', { className: 'image-demo-card-header' });
      origHeader.appendChild(el('span', { className: 'image-demo-card-label', textContent: 'Original Image' }));
      if (item.meta.beforeSize) {
        origHeader.appendChild(el('span', { className: 'image-demo-card-size', textContent: formatBytes(item.meta.beforeSize) }));
      }
      origCard.appendChild(origHeader);
      var origContent = el('div', { className: 'image-demo-card-content' });
      origContent.appendChild(el('img', { src: basePath + '/' + item.name + '.source.' + item.sourceExt, alt: item.title, loading: 'lazy' }));
      origCard.appendChild(origContent);
      leftCol.appendChild(origCard);
    } else {
      leftCol.appendChild(placeholderCard('Original Image'));
    }

    if (item.decompressed.length > 0) {
      var decompCards = [];
      item.decompressed.forEach(function (d, i) {
        var dCard = el('div', { className: 'image-demo-card image-demo-card--decompressed', 'data-model': d.model });
        if (i > 0) dCard.style.display = 'none';
        var dHeader = el('div', { className: 'image-demo-card-header' });
        dHeader.appendChild(el('span', { className: 'image-demo-card-label', textContent: 'Decompressed by ' + displayModel(d.model) + ' (from .crux.md)' }));
        dCard.appendChild(dHeader);
        var dContent = el('div', { className: 'image-demo-card-content' });
        dContent.appendChild(el('img', { src: basePath + '/' + item.name + '.decompressed-' + d.model + '.' + d.ext, alt: item.title + ' decompressed by ' + displayModel(d.model), loading: 'lazy' }));
        dCard.appendChild(dContent);
        decompCards.push(dCard);
        leftCol.appendChild(dCard);
      });

      var ms = modelSelector(item.decompressed, function (d) {
        decompCards.forEach(function (c) {
          c.style.display = c.getAttribute('data-model') === d.model ? '' : 'none';
        });
      });
      if (ms) leftCol.insertBefore(ms, decompCards[0]);
    }

    row.appendChild(leftCol);

    // Arrow column: forward arrow (→) aligned to original, reverse arrow (←) aligned to decompressed
    var arrowCol = el('div', { className: 'image-demo-arrows' });
    arrowCol.appendChild(arrow('image-demo-arrow'));
    if (item.decompressed.length > 0) {
      arrowCol.appendChild(arrow('image-demo-arrow-reverse'));
    }
    row.appendChild(arrowCol);

    // CRUX card
    var cruxCard = el('div', { className: 'image-demo-card image-demo-card--crux' });
    var cruxHeader = el('div', { className: 'image-demo-card-header' });
    cruxHeader.appendChild(el('span', { className: 'image-demo-card-label', textContent: 'CRUX Semantic Description' }));
    if (item.meta.afterSize) {
      cruxHeader.appendChild(el('span', { className: 'image-demo-card-size', textContent: formatBytes(item.meta.afterSize) }));
    }
    cruxCard.appendChild(cruxHeader);
    var cruxContent = el('div', { className: 'image-demo-card-content' });
    cruxContent.appendChild(copyBtn());
    var cruxPre = el('pre');
    cruxPre.appendChild(el('code', { className: 'language-crux', 'data-src': basePath + '/' + item.name + '.crux.md', 'data-extract': 'crux', textContent: 'Loading...' }));
    cruxContent.appendChild(cruxPre);
    cruxCard.appendChild(cruxContent);
    row.appendChild(cruxCard);
    demo.appendChild(row);

    // Reduction stats
    if (item.meta.reduction) {
      var stats = el('div', { className: 'image-demo-reduction' });
      stats.appendChild(el('div', { className: 'image-demo-stat' }, [
        el('span', { className: 'image-demo-stat-value', textContent: item.meta.reduction }),
        el('span', { className: 'image-demo-stat-label', textContent: 'size reduction' })
      ]));
      stats.appendChild(el('div', { className: 'image-demo-stat' }, [
        el('span', { className: 'image-demo-stat-value', textContent: 'Lossy' }),
        el('span', { className: 'image-demo-stat-label', textContent: 'preserves meaning, not pixels' })
      ]));
      demo.appendChild(stats);
    }

    frag.appendChild(demo);
    return frag;
  }

  function renderUrlItem(item, basePath) {
    var frag = document.createDocumentFragment();
    var demo = el('div', { className: 'url-demo' });

    // Command bar
    if (item.sourceUrl) {
      var cmdBar = el('div', { className: 'url-demo-command' });
      var cmdInner = el('div', { className: 'url-demo-command-bar' });
      cmdInner.appendChild(el('span', { className: 'url-demo-command-prompt', innerHTML: '&gt;' }));
      cmdInner.appendChild(el('code', { className: 'url-demo-command-text', textContent: '/crux-compress ' + item.sourceUrl }));
      cmdBar.appendChild(cmdInner);
      demo.appendChild(cmdBar);
    }

    var row = el('div', { className: 'url-demo-row' });

    // Source card
    var srcCard = el('div', { className: 'url-demo-card url-demo-card--screenshot' });
    var srcHeader = el('div', { className: 'url-demo-card-header' });
    var srcLabel = item.sourceUrl ? item.sourceUrl.replace(/^https?:\/\//, '') : item.name;
    srcHeader.appendChild(el('span', { className: 'url-demo-card-label', textContent: 'Source: ' + srcLabel }));
    if (item.meta.sourceTokens) {
      srcHeader.appendChild(el('span', { className: 'url-demo-card-meta', textContent: item.meta.sourceTokens + ' tokens' }));
    }
    srcCard.appendChild(srcHeader);
    var srcContent = el('div', { className: 'url-demo-card-content url-demo-card-content--iframe' });
    if (item.sourceUrl) {
      srcContent.appendChild(el('iframe', { src: item.sourceUrl, title: srcLabel, sandbox: 'allow-scripts' }));
    } else if (item.hasSource) {
      var srcPre = el('pre');
      srcPre.appendChild(el('code', { className: 'language-markdown', 'data-src': basePath + '/' + item.name + '.source.' + item.sourceExt, textContent: 'Loading...' }));
      srcContent.appendChild(srcPre);
    }
    srcCard.appendChild(srcContent);
    row.appendChild(srcCard);

    row.appendChild(arrow('url-demo-arrow'));

    // CRUX card
    var cruxCard = el('div', { className: 'url-demo-card url-demo-card--crux' });
    var cruxHeader = el('div', { className: 'url-demo-card-header' });
    cruxHeader.appendChild(el('span', { className: 'url-demo-card-label', textContent: 'CRUX Compressed' }));
    if (item.meta.cruxTokens) {
      cruxHeader.appendChild(el('span', { className: 'url-demo-card-meta', textContent: item.meta.cruxTokens + ' tokens' }));
    }
    cruxCard.appendChild(cruxHeader);
    var cruxContent = el('div', { className: 'url-demo-card-content' });
    cruxContent.appendChild(copyBtn());
    var cruxPre = el('pre');
    cruxPre.appendChild(el('code', { className: 'language-crux', 'data-src': basePath + '/' + item.name + '.crux.md', 'data-extract': 'crux', textContent: 'Loading...' }));
    cruxContent.appendChild(cruxPre);
    cruxCard.appendChild(cruxContent);
    row.appendChild(cruxCard);
    demo.appendChild(row);

    // Reduction stats
    if (item.meta.reduction) {
      var stats = el('div', { className: 'url-demo-reduction' });
      stats.appendChild(el('div', { className: 'url-demo-stat' }, [
        el('span', { className: 'url-demo-stat-value', textContent: item.meta.reduction }),
        el('span', { className: 'url-demo-stat-label', textContent: 'token reduction' })
      ]));
      demo.appendChild(stats);
    }

    // Decompressed
    if (item.decompressed.length > 0) {
      var decompSection = el('div', { className: 'url-demo-decompressed' });
      decompSection.appendChild(el('h3', { textContent: 'Decompressed by ' + displayModel(item.decompressed[0].model) }));

      var decompPanels = [];
      item.decompressed.forEach(function (d, i) {
        var dWrap = el('div', { className: 'url-demo-decompressed-panel', 'data-model': d.model });
        if (i > 0) dWrap.style.display = 'none';
        var dCard = el('div', { className: 'url-demo-card url-demo-card--decompressed' });
        var dHeader = el('div', { className: 'url-demo-card-header' });
        dHeader.appendChild(el('span', { className: 'url-demo-card-label', textContent: displayModel(d.model) + ' (from .crux.md only)' }));
        dCard.appendChild(dHeader);
        var dSrc = basePath + '/' + item.name + '.decompressed-' + d.model + '.' + d.ext;
        var dContent;
        if (d.ext === 'html') {
          dContent = el('div', { className: 'url-demo-card-content url-demo-card-content--iframe' });
          dContent.appendChild(el('iframe', { src: dSrc, title: item.title + ' decompressed by ' + displayModel(d.model), sandbox: 'allow-scripts' }));
        } else {
          dContent = el('div', { className: 'url-demo-card-content' });
          var dPre = el('pre');
          dPre.appendChild(el('code', { className: 'language-markdown', 'data-src': dSrc, textContent: 'Loading...' }));
          dContent.appendChild(dPre);
        }
        dCard.appendChild(dContent);
        dWrap.appendChild(dCard);
        decompPanels.push(dWrap);
        decompSection.appendChild(dWrap);
      });

      var ms = modelSelector(item.decompressed, function (d) {
        var heading = decompSection.querySelector('h3');
        if (heading) heading.textContent = 'Decompressed by ' + displayModel(d.model);
        decompPanels.forEach(function (p) {
          p.style.display = p.getAttribute('data-model') === d.model ? '' : 'none';
        });
      });
      if (ms) decompSection.insertBefore(ms, decompSection.children[1]);

      demo.appendChild(decompSection);
    }

    frag.appendChild(demo);
    return frag;
  }

  // ── Gallery builder ──

  var RENDERERS = {
    rules: renderRulesItem,
    code: renderCodeItem,
    images: renderImageItem,
    urls: renderUrlItem
  };

  function buildGallery(container, items, type) {
    var basePath = 'assets/' + type;
    var renderer = RENDERERS[type];
    if (!renderer || items.length === 0) return;

    var itemsWrap = el('div', { className: 'gallery-items' });

    items.forEach(function (item, i) {
      var galleryItem = el('div', { className: 'gallery-item' + (i === 0 ? ' gallery-item--active' : '') });
      galleryItem.appendChild(el('h3', { className: 'gallery-item-title', textContent: item.title }));
      galleryItem.appendChild(renderer(item, basePath));
      itemsWrap.appendChild(galleryItem);
    });

    container.appendChild(itemsWrap);

    if (items.length === 1) {
      itemsWrap.querySelector('.gallery-item').style.position = 'relative';
    }

    // Carousel nav (only when multiple items)
    if (items.length > 1) {
      var prevBtn = el('button', { className: 'gallery-nav gallery-nav--prev', 'aria-label': 'Previous example', innerHTML: NAV_PREV_SVG });
      var nextBtn = el('button', { className: 'gallery-nav gallery-nav--next', 'aria-label': 'Next example', innerHTML: NAV_NEXT_SVG });

      var dotsWrap = el('div', { className: 'gallery-dots' });
      items.forEach(function (item, i) {
        var dot = el('button', { className: 'gallery-dot' + (i === 0 ? ' gallery-dot--active' : ''), 'aria-label': item.title, title: item.title });
        dot.addEventListener('click', function () { goTo(i); });
        dotsWrap.appendChild(dot);
      });

      var currentIdx = 0;
      var galleryItems = itemsWrap.querySelectorAll('.gallery-item');
      var dots = dotsWrap.querySelectorAll('.gallery-dot');

      function lockHeight() {
        var max = 0;
        for (var i = 0; i < galleryItems.length; i++) {
          galleryItems[i].style.position = 'relative';
          galleryItems[i].style.opacity = '1';
          galleryItems[i].style.transform = 'none';
          var h = galleryItems[i].offsetHeight;
          if (h > max) max = h;
        }
        for (var j = 0; j < galleryItems.length; j++) {
          galleryItems[j].style.position = '';
          galleryItems[j].style.opacity = '';
          galleryItems[j].style.transform = '';
        }
        itemsWrap.style.height = max + 'px';
      }

      lockHeight();

      // Re-lock height after async content finishes loading (CodeLoader fetches / images).
      // MutationObserver watches for DOM node additions caused by CodeLoader injecting code.
      var heightUpdateTimer;
      // Capture count at build time; all code[data-src] blocks exist in the static template.
      var totalBlocks = itemsWrap.querySelectorAll('code[data-src]').length;

      function disconnectObserver() {
        heightObserver.disconnect();
      }

      function scheduleHeightUpdate() {
        clearTimeout(heightUpdateTimer);
        heightUpdateTimer = setTimeout(function () {
          lockHeight();
          // Disconnect once all data-src code blocks have been processed.
          // Relies on CodeLoader adding the 'has-line-numbers' class after injection;
          // the 10 s fallback below handles the case where this class is never applied.
          var processed = itemsWrap.querySelectorAll('code[data-src].has-line-numbers').length;
          if (processed >= totalBlocks && totalBlocks > 0) {
            disconnectObserver();
          }
        }, 100);
      }

      var heightObserver = new MutationObserver(scheduleHeightUpdate);
      heightObserver.observe(itemsWrap, { subtree: true, childList: true });

      // Fallback: always disconnect after 10 s to avoid leaks if CodeLoader never
      // applies .has-line-numbers (e.g. on network error).
      if (totalBlocks > 0) {
        setTimeout(disconnectObserver, 10000);
      }

      // Also re-lock when any gallery images finish loading.
      var galleryImgs = itemsWrap.querySelectorAll('img');
      for (var k = 0; k < galleryImgs.length; k++) {
        if (!galleryImgs[k].complete) {
          galleryImgs[k].addEventListener('load', scheduleHeightUpdate, { once: true });
        }
      }

      var resizeTimer;
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(lockHeight, 150);
      });

      function goTo(idx) {
        if (idx === currentIdx) return;
        var forward = idx > currentIdx || (currentIdx === items.length - 1 && idx === 0);
        var outgoing = galleryItems[currentIdx];

        outgoing.style.transition = 'none';
        outgoing.style.transform = '';
        outgoing.offsetHeight;
        outgoing.style.transition = '';
        outgoing.style.transform = forward ? 'translateX(-30px)' : 'translateX(30px)';
        outgoing.classList.remove('gallery-item--active');
        dots[currentIdx].classList.remove('gallery-dot--active');

        var incoming = galleryItems[idx];
        incoming.style.transition = 'none';
        incoming.style.transform = forward ? 'translateX(30px)' : 'translateX(-30px)';
        incoming.offsetHeight;
        incoming.style.transition = '';
        incoming.style.transform = '';
        incoming.classList.add('gallery-item--active');

        currentIdx = idx;
        dots[currentIdx].classList.add('gallery-dot--active');

        var codeEls = incoming.querySelectorAll('code[data-src]:not(.has-line-numbers)');
        if (codeEls.length > 0 && window.CodeLoader) {
          window.CodeLoader.processContainer(incoming);
        }
      }

      prevBtn.addEventListener('click', function () { goTo((currentIdx - 1 + items.length) % items.length); });
      nextBtn.addEventListener('click', function () { goTo((currentIdx + 1) % items.length); });

      container.insertBefore(prevBtn, itemsWrap);
      container.appendChild(nextBtn);
      container.appendChild(dotsWrap);

      var autoTimer = null;
      var AUTO_INTERVAL = 6000;
      var hovering = false;

      function startAuto() {
        if (autoTimer) return;
        autoTimer = setInterval(function () {
          if (!hovering) goTo((currentIdx + 1) % items.length);
        }, AUTO_INTERVAL);
      }

      function stopAuto() {
        if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
      }

      container.addEventListener('mouseenter', function () {
        hovering = true;
        stopAuto();
      });
      container.addEventListener('mouseleave', function () {
        hovering = false;
        startAuto();
      });

      startAuto();
    }

    // Process code blocks in the first visible item
    if (window.CodeLoader) {
      window.CodeLoader.processContainer(itemsWrap.querySelector('.gallery-item--active'));
    }
  }

  // ── Init ──

  function init() {
    fetch('assets/manifest.json')
      .then(function (r) { return r.json(); })
      .then(function (manifest) {
        var types = ['rules', 'code', 'images', 'urls'];
        types.forEach(function (type) {
          var container = document.querySelector('[data-gallery="' + type + '"]');
          var items = manifest[type];
          if (container && items && items.length > 0) {
            if (type === 'images') {
              items = items.filter(function (item) { return item.hasSource; });
            }
            if (items.length > 0) {
              buildGallery(container, items, type);
            }
          }
        });
      })
      .catch(function (err) {
        console.error('gallery-loader: failed to load manifest', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();