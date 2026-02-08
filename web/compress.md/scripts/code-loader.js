/**
 * Code Loader — Fetches external code files, injects them into <code> elements,
 * applies syntax highlighting via highlight.js, and adds line numbers.
 * 
 * Any <code> element with a `data-src` attribute will have its content replaced
 * with the fetched file contents. After loading, highlight.js is invoked to
 * apply syntax highlighting based on the element's language class.
 * 
 * Supports `data-extract="crux"` to extract only the content between ```crux
 * fences from a .crux.md file (strips frontmatter and markdown wrapping).
 * 
 * Line numbers are added to all code blocks inside elements with class
 * `code-demo-card-content`, `image-demo-card-content`, or `demo-panel-content`.
 */
(function () {
  'use strict';

  // Register a custom CRUX language for highlight.js
  if (typeof hljs !== 'undefined') {
    hljs.registerLanguage('crux', function () {
      return {
        name: 'CRUX',
        case_insensitive: false,
        contains: [
          // Block delimiters
          {
            className: 'meta',
            begin: /⟦CRUX:[^\n]*/
          },
          {
            className: 'meta',
            begin: /⟧/
          },
          // Standard blocks (Greek letters)
          {
            className: 'keyword',
            begin: /[ΡEΛΠΚRPΓMΦΩ](?:\.\w+)?(?=\{)/
          },
          // CRUX symbols — flow, logic, relations
          {
            className: 'built_in',
            begin: /[→←»⊳⊲∋≻≺∀∃¬⊤⊥Δ⊛◊⊕≥≤≠]/
          },
          // Strings
          {
            className: 'string',
            begin: /"/, end: /"/
          },
          // Numbers and percentages
          {
            className: 'number',
            begin: /\b\d+(\.\d+)?%?/
          },
          // Comments
          {
            className: 'comment',
            begin: /#/, end: /$/
          },
          // Named identifiers before = or :
          {
            className: 'attr',
            begin: /\b[A-Z_][A-Z_0-9]*(?==)/
          },
          // Function/variable names after Λ.
          {
            className: 'title.function',
            begin: /(?<=\.)\w+(?=\{)/
          }
        ]
      };
    });

    // Don't auto-highlight on load — we do it manually after fetch
    hljs.configure({ ignoreUnescapedHTML: true });
  }

  /**
   * Extract content between ```crux and ``` fences from a .crux.md file.
   */
  function extractCruxBlock(text) {
    var startMarker = '```crux\n';
    var endMarker = '\n```';
    var startIdx = text.indexOf(startMarker);
    if (startIdx === -1) return text;

    var contentStart = startIdx + startMarker.length;
    var contentEnd = text.indexOf(endMarker, contentStart);
    if (contentEnd === -1) return text.substring(contentStart);

    return text.substring(contentStart, contentEnd);
  }

  /**
   * Apply syntax highlighting to a <code> element using highlight.js.
   */
  function highlightElement(codeEl) {
    if (typeof hljs === 'undefined') return;

    var langClass = codeEl.className.match(/language-(\w+)/);
    if (langClass) {
      var lang = langClass[1];
      try {
        var result = hljs.highlight(codeEl.textContent, { language: lang });
        codeEl.innerHTML = result.value;
        codeEl.classList.add('hljs');
      } catch (e) {
        hljs.highlightElement(codeEl);
      }
    } else {
      hljs.highlightElement(codeEl);
    }
  }

  /**
   * Add line numbers to a <code> element by wrapping each line in a span.
   * Works after highlight.js has already processed the innerHTML.
   * Uses a table-based layout so line numbers don't get selected on copy.
   */
  function addLineNumbers(codeEl) {
    var html = codeEl.innerHTML;
    // Split on newlines — hljs output is a flat string with \n separators
    var lines = html.split('\n');

    // Remove trailing empty line (common artifact)
    if (lines.length > 1 && lines[lines.length - 1] === '') {
      lines.pop();
    }

    var tableHtml = '<table class="code-lines" role="presentation"><tbody>';
    for (var i = 0; i < lines.length; i++) {
      tableHtml += '<tr>' +
        '<td class="code-line-number" data-line="' + (i + 1) + '"></td>' +
        '<td class="code-line-content">' + (lines[i] || ' ') + '</td>' +
        '</tr>';
    }
    tableHtml += '</tbody></table>';

    codeEl.innerHTML = tableHtml;
    codeEl.classList.add('has-line-numbers');
  }

  /**
   * Process a code element: highlight then add line numbers.
   */
  function processCodeElement(codeEl) {
    highlightElement(codeEl);
    addLineNumbers(codeEl);
  }

  /**
   * Fetch a file and inject its contents into the target <code> element,
   * then apply syntax highlighting and line numbers.
   */
  function loadCode(codeEl) {
    var src = codeEl.getAttribute('data-src');
    if (!src) return;

    var extract = codeEl.getAttribute('data-extract');

    fetch(src)
      .then(function (response) {
        if (!response.ok) {
          throw new Error('HTTP ' + response.status + ' loading ' + src);
        }
        return response.text();
      })
      .then(function (text) {
        if (extract === 'crux') {
          text = extractCruxBlock(text);
        }
        codeEl.textContent = text;
        processCodeElement(codeEl);
      })
      .catch(function (err) {
        console.error('code-loader:', err);
        codeEl.textContent = '// Failed to load ' + src;
      });
  }

  /**
   * Highlight and add line numbers to inline code blocks
   * (those not loaded via data-src but already in the HTML).
   */
  function highlightInlineBlocks() {
    if (typeof hljs === 'undefined') return;

    // Target code blocks in demo panels and card contents
    var selectors = [
      '.code-demo-card-content pre code',
      '.image-demo-card-content pre code',
      '.demo-panel-content pre code'
    ];
    var blocks = document.querySelectorAll(selectors.join(','));

    for (var i = 0; i < blocks.length; i++) {
      var block = blocks[i];
      // Skip data-src blocks (handled by loadCode) and already-processed blocks
      if (block.hasAttribute('data-src') || block.classList.contains('has-line-numbers')) {
        continue;
      }
      if (block.textContent.trim().length > 0) {
        processCodeElement(block);
      }
    }
  }

  // Load all data-src code blocks
  var elements = document.querySelectorAll('code[data-src]');
  for (var i = 0; i < elements.length; i++) {
    loadCode(elements[i]);
  }

  // Highlight and number existing inline code blocks
  highlightInlineBlocks();

})();
