/**
 * Effect Page Script - Pure CSS Image Hover Effects
 * Dynamically generates HTML and CSS code panels
 * from the actual preview markup and style.css file.
 * 
 * Loaded by every effect page. Reads the live .preview-container DOM
 * and fetches ./style.css to populate the code panels.
 */

(function() {
  'use strict';

  /**
   * HTML escape utility
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Extract effect ID from the preview container's child div class
   */
  function getEffectId() {
    const previewContainer = document.querySelector('.preview-container');
    if (!previewContainer) return null;
    
    const effectDiv = previewContainer.querySelector('div[class]');
    if (!effectDiv) return null;
    
    // Get the first class that looks like an effect ID (contains hyphen)
    const classes = effectDiv.className.split(' ').filter(c => c && c.includes('-'));
    return classes[0] || null;
  }

  /**
   * Generate HTML snippet from live preview markup
   */
  function generateHtmlSnippet(effectId) {
    const previewContainer = document.querySelector('.preview-container');
    if (!previewContainer) return '<!-- Preview container not found -->';
    
    const effectDiv = previewContainer.querySelector('div.' + effectId);
    if (!effectDiv) return '<!-- Effect div not found -->';
    
    // Clone to avoid mutating live DOM
    const clone = effectDiv.cloneNode(true);
    
    // Replace image src with placeholder
    const img = clone.querySelector('img');
    if (img) {
      img.setAttribute('src', 'your-image.jpg');
      // Keep meaningful alt, replace generic ones
      if (!img.alt || img.alt === 'Demo image') {
        img.setAttribute('alt', 'Description');
      }
    }
    
    // Get outerHTML and pretty-print
    let html = clone.outerHTML;
    
    // Format: put child elements on new lines with indentation
    html = html
      .replace(/><\//g, '>\n  </')
      .replace(/><img/g, '>\n  <img')
      .trim();
    
    return escapeHtml(html);
  }

  /**
   * Fetch CSS from style.css
   */
  async function fetchCssCode() {
    try {
      const response = await fetch('./style.css');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const css = await response.text();
      return escapeHtml(css.trim());
    } catch (err) {
      console.error('Failed to load style.css:', err);
      return '/* Failed to load style.css */\n' + escapeHtml(err.message);
    }
  }

  /**
   * Populate both code panels
   */
  async function populateCodePanels() {
    const effectId = getEffectId();
    
    if (!effectId) {
      console.warn('Could not determine effect ID');
      return;
    }
    
    // Find the code elements
    const htmlCodeEl = document.querySelector('.panel--code:first-of-type .code-block code');
    const cssCodeEl = document.querySelector('.panel--code:last-of-type .code-block code');
    
    if (!htmlCodeEl || !cssCodeEl) {
      console.warn('Code panel elements not found');
      return;
    }
    
    // Generate and inject HTML
    const htmlSnippet = generateHtmlSnippet(effectId);
    htmlCodeEl.textContent = htmlSnippet;
    
    // Fetch and inject CSS
    const cssSnippet = await fetchCssCode();
    cssCodeEl.textContent = cssSnippet;
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', populateCodePanels);
  } else {
    populateCodePanels();
  }

})();