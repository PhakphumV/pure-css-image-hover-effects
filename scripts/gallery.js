/**
 * Gallery Script - Pure CSS Image Hover Effects
 * Handles image switching for each effect card on the index page
 * Uses picsum.photos for placeholder images
 */

(function() {
  'use strict';

  // Configuration
  const IMAGES_PER_EFFECT = 10;
  const IMAGE_WIDTH = 400;
  const IMAGE_HEIGHT = 300;

  // Effect definitions - each effect gets a unique ID for image seeding
  const effects = [
    {
      id: 'scale-reveal',
      title: 'Scale Reveal',
      desc: 'Image scales up within a clipped container',
      folder: 'scale-reveal'
    },
    {
      id: 'slide-reveal',
      title: 'Slide Reveal',
      desc: 'Image slides and scales on hover',
      folder: 'slide-reveal'
    },
    {
      id: 'fade-colorize',
      title: 'Fade to Color',
      desc: 'Grayscale to full color transition',
      folder: 'fade-colorize'
    },
    {
      id: 'glow-border',
      title: 'Glow Border',
      desc: 'Radial glow expands on hover',
      folder: 'glow-border'
    },
    {
      id: 'rotate-3d',
      title: '3D Rotate',
      desc: 'Perspective rotation with scale',
      folder: 'rotate-3d'
    },
    {
      id: 'clip-reveal',
      title: 'Clip Reveal',
      desc: 'Center-expanding clip path reveal',
      folder: 'clip-reveal'
    },
    {
      id: 'blur-sharpen',
      title: 'Blur to Sharp',
      desc: 'Blurred grayscale sharpens on hover',
      folder: 'blur-sharpen'
    },
    {
      id: 'zoom-rotate',
      title: 'Zoom & Rotate',
      desc: 'Subtle rotation with zoom',
      folder: 'zoom-rotate'
    },
    {
      id: 'vignette',
      title: 'Vignette',
      desc: 'Dark vignette fades in on hover',
      folder: 'vignette'
    },
    {
      id: 'duotone',
      title: 'Duotone Shift',
      desc: 'Duotone filter transitions to normal',
      folder: 'duotone'
    }
  ];

  // State tracking for each card
  const cardStates = new Map();

  /**
   * Generate a picsum.photos URL with a deterministic seed
   */
  function getImageUrl(effectIndex, imageIndex) {
    // Using a combined seed for reproducible but varied images
    const seed = effectIndex * 100 + imageIndex;
    return `https://picsum.photos/${IMAGE_WIDTH}/${IMAGE_HEIGHT}?random=${seed}`;
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

    // Initialize state for this card
    cardStates.set(effect.id, { currentIndex: 0, preloaded: [] });

    // Preload all images for this effect
    for (let i = 0; i < IMAGES_PER_EFFECT; i++) {
      preloadImage(getImageUrl(index, i));
    }

    card.innerHTML = `
      <div class="card__media ${effect.id}" aria-hidden="true">
        <img src="${getImageUrl(index, 0)}" alt="${effect.title} demo" loading="lazy">
      </div>
      <div class="card__content">
        <h2 class="card__title">${effect.title}</h2>
        <p class="card__desc">${effect.desc}</p>
        <div class="card__switcher">
          <span class="card__counter" aria-live="polite">1 / ${IMAGES_PER_EFFECT}</span>
          <button type="button" class="btn" aria-label="Next image">Next image</button>
        </div>
      </div>
    `;

    // Add click handler for the "Next image" button
    const nextBtn = card.querySelector('.btn');
    const counter = card.querySelector('.card__counter');
    const img = card.querySelector('img');

    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation(); // Prevent navigation to dedicated page

      const state = cardStates.get(effect.id);
      state.currentIndex = (state.currentIndex + 1) % IMAGES_PER_EFFECT;
      const newSrc = getImageUrl(index, state.currentIndex);

      // Smooth transition: fade out, swap, fade in
      img.style.opacity = '0';
      setTimeout(() => {
        img.src = newSrc;
        img.style.opacity = '1';
        counter.textContent = `${state.currentIndex + 1} / ${IMAGES_PER_EFFECT}`;
      }, 150);
    });

    // Keyboard support for the button
    nextBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        nextBtn.click();
      }
    });

    return card;
  }

  /**
   * Initialize the gallery
   */
  function initGallery() {
    const gallery = document.getElementById('gallery');
    if (!gallery) return;

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