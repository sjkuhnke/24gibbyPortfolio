(function () {

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('page-loaded');

    const photos = document.querySelectorAll('.collage-photo');
    if (photos.length && !prefersReduced) {
      photos.forEach((photo, i) => {
        photo.style.animationDelay = `${i * 90}ms`;
        photo.classList.add('collage-reveal');
      });
    }

    const heroEls = document.querySelectorAll('.hero-text > *');
    if (heroEls.length && !prefersReduced) {
      heroEls.forEach((el, i) => {
        el.style.animationDelay = `${380 + i * 100}ms`;
        el.classList.add('hero-entrance');
      });
    }

    setTimeout(initScrollObserver, 100);

    initPageTransitions();
  });


  function initScrollObserver () {
    if (!('IntersectionObserver' in window) || prefersReduced) {
      document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('revealed'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = el.dataset.revealDelay || 0;

          setTimeout(() => el.classList.add('revealed'), parseInt(delay));
          observer.unobserve(el);
        }
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -40px 0px'
    });

    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));

    document.querySelectorAll('[data-reveal-group]').forEach(group => {
      const children = group.querySelectorAll('[data-reveal]');
      children.forEach((child, i) => {
        child.dataset.revealDelay = i * (parseInt(group.dataset.revealStagger) || 80);
      });

      if (group.hasAttribute('data-reveal')) observer.observe(group);
    });
  }

  function initPageTransitions () {
    if (prefersReduced) return;

    const bar = document.createElement('div');
    bar.id = 'page-transition-bar';
    document.body.appendChild(bar);

    document.addEventListener('click', e => {
      const link = e.target.closest('a[href]');
      if (!link) return;

      const href = link.getAttribute('href');
      const isInternal = (
        href &&
        !href.startsWith('http') &&
        !href.startsWith('//') &&
        !href.startsWith('#') &&
        !href.startsWith('mailto:') &&
        !link.hasAttribute('target')
      );

      if (!isInternal) return;

      e.preventDefault();

      bar.classList.add('running');
      document.body.classList.add('page-leaving');

      setTimeout(() => {
        window.location.href = href;
      }, 280);
    });

    window.addEventListener('pageshow', () => {
      bar.classList.remove('running');
      document.body.classList.remove('page-leaving');
    });
  }

})();