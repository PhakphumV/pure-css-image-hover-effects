/**
 * Gallery Script - Pure CSS Image Hover Effects
 * Handles image switching for the header button group
 * Uses picsum.photos for placeholder images
 */

(function() {
  'use strict';

  // Configuration
  const IMAGES_PER_EFFECT = 10;
  const IMAGE_WIDTH = 600;
  const IMAGE_HEIGHT = 400;
  const DEFAULT_IMAGE_INDEX = 0;

  let effects = [];
  let currentImageIndex = DEFAULT_IMAGE_INDEX;
  const imageElements = [];

  /**
   * Generate a picsum.photos URL with a deterministic seed
   */
  function getImageUrl(imageId) {
    return `https://picsum.photos/${IMAGE_WIDTH}/${IMAGE_HEIGHT}?random=${imageId}`;
  }

  /**
   * Preload an image
   */
  function preloadImage(url) {
    const img = new Image();
    img.src = url;
    return img;
  }

  /**
   * Load the effect manifest generated from the effects directory.
   */
  function loadEffects() {
    const data = window.__EFFECTS_MANIFEST__;
    if (Array.isArray(data)) {
      return data;
    }

    if (data && Array.isArray(data.effects)) {
      return data.effects;
    }

    console.warn('The effect manifest is not available.');
    return [];
  }

  /**
   * Create a card element for an effect
   */
  function createCard(effect, index) {
    const card = document.createElement('a');
    card.className = 'card';
    card.href = `effects/${effect.folder}/index.html`;
    card.dataset.effectId = effect.id;
    card.setAttribute('role', 'link');
    card.setAttribute('aria-label', `View ${effect.title} effect`);

    // Initial image uses currentImageIndex (all cards start with same image)
    const img = document.createElement('img');
    img.src = getImageUrl(currentImageIndex + 1);
    img.alt = effect.title + ' demo';
    img.loading = 'lazy';

    // Store reference for later updates
    imageElements.push(img);

    card.innerHTML = `
      <div class="card__media ${effect.id}" aria-hidden="true">
      </div>
      <div class="card__content">
        <h2 class="card__title">${effect.title}</h2>
        <p class="card__desc">${effect.desc}</p>
      </div>
    `;

    // Insert the img element
    card.querySelector('.card__media').appendChild(img);

    return card;
  }

  // To add css style from each effect folder, we can dynamically create a link element and append it to the head
  function loadEffectStyles() {
    effects.forEach(effect => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = `effects/${effect.folder}/style.css`;
      document.head.appendChild(link);
    });
  }

  /**
   * Create header button group
   */
  function createSwitcher() {
    const container = document.querySelector('.switcher-buttons');
    if (!container) return;

    for (let i = 1; i <= IMAGES_PER_EFFECT; i++) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'switcher-btn';
      btn.textContent = i;
      btn.setAttribute('aria-label', `Switch to image ${i}`);
      if (i === 1) btn.setAttribute('aria-selected', 'true');

      btn.addEventListener('click', () => {
        // Update selected state
        container.querySelectorAll('.switcher-btn').forEach(b => {
          b.setAttribute('aria-selected', 'false');
        });
        btn.setAttribute('aria-selected', 'true');

        // Change all images to the SAME selected image
        currentImageIndex = i - 1;
        updateAllImages(i);
      });

      container.appendChild(btn);
    }

    // Preload all images
    for (let i = 0; i < IMAGES_PER_EFFECT; i++) {
      preloadImage(getImageUrl(i + 1));
    }
  }

  /**
   * Update all images to the same selected image
   */
  function updateAllImages(selectedImageNum) {
    const newSrc = getImageUrl(selectedImageNum);
    imageElements.forEach(img => {
      img.style.opacity = '0';
      setTimeout(() => {
        img.src = newSrc;
        img.style.opacity = '1';
      }, 150);
    });
  }

  /**
   * Initialize the gallery
   */
  function initGallery() {
    const gallery = document.getElementById('gallery');
    if (!gallery) return;

    // Create header switcher first
    createSwitcher();

    effects = loadEffects();

    // Load effect styles
    loadEffectStyles();

    if (!effects.length) {
      gallery.innerHTML = '<p class="card__desc">No effects are available yet. Run <code>node scripts/generate-effects-data.js</code> to generate the manifest.</p>';
      return;
    }

    // Create and append all cards
    effects.forEach((effect, index) => {
      const card = createCard(effect, index);
      gallery.appendChild(card);
    });

    // Add intersection observer for lazy loading images
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target.querySelector('img');
            if (img && img.loading === 'lazy') {
              img.loading = 'eager';
            }
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '100px' });

      document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
      });
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGallery);
  } else {
    initGallery();
  }

})();