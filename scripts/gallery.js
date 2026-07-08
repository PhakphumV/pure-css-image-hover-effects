/**
 * Gallery Script - Pure CSS Image Hover Effects
 * Handles image switching for the header button group
 * Uses picsum.photos for placeholder images
 */

(function() {
  'use strict';

  // Configuration
  const IMAGES_PER_EFFECT = 10;
  const IMAGE_WIDTH = 400;
  const IMAGE_HEIGHT = 300;
  const DEFAULT_IMAGE_INDEX = 0;

  // Effect definitions
  const effects = [
    { id: 'scale-reveal', title: 'Scale Reveal', desc: 'Image scales up within a clipped container', folder: 'scale-reveal' },
    { id: 'slide-reveal', title: 'Slide Reveal', desc: 'Image slides and scales on hover', folder: 'slide-reveal' },
    { id: 'fade-colorize', title: 'Fade to Color', desc: 'Grayscale to full color transition', folder: 'fade-colorize' },
    { id: 'glow-border', title: 'Glow Border', desc: 'Radial glow expands on hover', folder: 'glow-border' },
    { id: 'rotate-3d', title: '3D Rotate', desc: 'Perspective rotation with scale', folder: 'rotate-3d' },
    { id: 'clip-reveal', title: 'Clip Reveal', desc: 'Center-expanding clip path reveal', folder: 'clip-reveal' },
    { id: 'blur-sharpen', title: 'Blur to Sharp', desc: 'Blurred grayscale sharpens on hover', folder: 'blur-sharpen' },
    { id: 'zoom-rotate', title: 'Zoom & Rotate', desc: 'Subtle rotation with zoom', folder: 'zoom-rotate' },
    { id: 'vignette', title: 'Vignette', desc: 'Dark vignette fades in on hover', folder: 'vignette' },
    { id: 'duotone', title: 'Duotone Shift', desc: 'Duotone filter transitions to normal', folder: 'duotone' }
  ];

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
   * Create a card element for an effect
   */
  function createCard(effect, index) {
    const card = document.createElement('a');
    card.className = 'card';
    card.href = `effects/${effect.folder}/index.html`;
    card.dataset.effectId = effect.id;
    card.setAttribute('role', 'link');
    card.setAttribute('aria-label', `View ${effect.title} effect`);

    const imgIndex = index + 1;
    const img = document.createElement('img');
    img.src = getImageUrl(imgIndex);
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

        // Change all images
        currentImageIndex = i - 1;
        updateAllImages();
      });

      container.appendChild(btn);
    }

    // Preload all images
    for (let i = 0; i < IMAGES_PER_EFFECT; i++) {
      preloadImage(getImageUrl(i + 1));
    }
  }

  /**
   * Update all images to the current index
   */
  function updateAllImages() {
    imageElements.forEach((img, idx) => {
      const imageId = ((idx % IMAGES_PER_EFFECT) + 1) + currentImageIndex;
      img.style.opacity = '0';
      setTimeout(() => {
        img.src = getImageUrl(((idx % IMAGES_PER_EFFECT) + 1) + currentImageIndex);
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