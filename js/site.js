// Global site scripts for GTME blog
(function () {
  function onReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  // Header scroll behavior (applies where .header exists)
  onReady(function headerScroll() {
    const header = document.querySelector('.header');
    if (!header) return;
    window.addEventListener('scroll', function () {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollTop > 50) {
        header.style.backgroundColor = 'rgba(244, 244, 244, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
        header.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
      } else {
        header.style.backgroundColor = 'rgb(244, 244, 244)';
        header.style.backdropFilter = 'none';
        header.style.boxShadow = 'none';
      }
    });
  });

  // Mobile menu toggle and accessibility
  onReady(function mobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    if (!mobileMenuButton || !mobileMenuOverlay) return;

    function closeMenu() {
      mobileMenuButton.setAttribute('aria-expanded', 'false');
      mobileMenuButton.classList.remove('open');
      mobileMenuOverlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    mobileMenuButton.addEventListener('click', function () {
      const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
      mobileMenuButton.setAttribute('aria-expanded', (!isExpanded).toString());
      mobileMenuButton.classList.toggle('open');
      mobileMenuOverlay.classList.toggle('open');
      document.body.style.overflow = mobileMenuOverlay.classList.contains('open') ? 'hidden' : '';
    });

    mobileMenuOverlay.addEventListener('click', function (event) {
      if (event.target === mobileMenuOverlay) closeMenu();
    });

    const mobileNavLinks = mobileMenuOverlay.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach((link) => {
      link.addEventListener('click', closeMenu);
    });
  });

  // Category filter logic (only runs on index page where elements exist)
  onReady(function categoryFilters() {
    const filterPills = document.querySelectorAll('.filter-pill');
    const postCards = document.querySelectorAll('.post-card');
    const featuredPost = document.querySelector('.featured-post');
    const featuredBadge = document.querySelector('.featured-badge');
    if (!filterPills.length || !postCards.length) return;

    const allPosts = [...postCards];
    if (featuredPost) allPosts.push(featuredPost);

    function getFilterTags(category) {
      const filterMap = {
        all: [],
        'gtm-engineering': ['gtm-engineering'],
        revops: ['revops', 'revenue-operations'],
        strategy: ['strategy', 'go-to-market-strategy'],
        'go-to-market': ['go-to-market', 'go-to-market-strategy'],
      };
      return filterMap[category] || [];
    }

    function postMatchesFilter(post, filterTags) {
      if (filterTags.length === 0) return true;
      const postTags = post.getAttribute('data-tags');
      if (!postTags) return false;
      const postTagsArray = postTags.split(',').map((tag) => tag.trim().toLowerCase());
      return filterTags.some((filterTag) =>
        postTagsArray.some(
          (postTag) =>
            postTag === filterTag.toLowerCase() ||
            postTag.includes(filterTag.toLowerCase()) ||
            filterTag.toLowerCase().includes(postTag)
        )
      );
    }

    function applyFilter(category) {
      const filterTags = getFilterTags(category);
      let featuredPostVisible = false;

      allPosts.forEach((post) => {
        const shouldShow = postMatchesFilter(post, filterTags);
        if (post === featuredPost && shouldShow) featuredPostVisible = true;
        if (shouldShow) {
          post.classList.remove('filtering-out', 'post-hidden');
          post.classList.add('filtering-in');
          setTimeout(() => post.classList.remove('filtering-in'), 400);
        } else {
          post.classList.remove('filtering-in');
          post.classList.add('filtering-out');
          setTimeout(() => {
            if (post.classList.contains('filtering-out')) post.classList.add('post-hidden');
          }, 300);
        }
      });

      if (featuredBadge) {
        if (featuredPostVisible) {
          featuredBadge.classList.remove('filtering-out', 'post-hidden');
          featuredBadge.classList.add('filtering-in');
          setTimeout(() => featuredBadge.classList.remove('filtering-in'), 400);
        } else {
          featuredBadge.classList.remove('filtering-in');
          featuredBadge.classList.add('filtering-out');
          setTimeout(() => {
            if (featuredBadge.classList.contains('filtering-out')) featuredBadge.classList.add('post-hidden');
          }, 300);
        }
      }
    }

    // Wire pill clicks
    filterPills.forEach((pill) => {
      pill.addEventListener('click', function (e) {
        e.preventDefault();
        const category = this.getAttribute('data-category');
        filterPills.forEach((p) => {
          p.classList.remove('active');
          p.setAttribute('aria-pressed', 'false');
        });
        this.classList.add('active');
        this.setAttribute('aria-pressed', 'true');
        applyFilter(category);
        const url = new URL(window.location);
        if (category === 'all') url.searchParams.delete('category');
        else url.searchParams.set('category', category);
        window.history.replaceState({}, '', url);
      });
    });

    // Init from URL
    const urlParams = new URLSearchParams(window.location.search);
    const initialCategory = urlParams.get('category') || 'all';
    const initialPill = document.querySelector(`[data-category="${initialCategory}"]`);
    if (initialPill) {
      filterPills.forEach((p) => {
        p.classList.remove('active');
        p.setAttribute('aria-pressed', 'false');
      });
      initialPill.classList.add('active');
      initialPill.setAttribute('aria-pressed', 'true');
      if (initialCategory !== 'all') setTimeout(() => applyFilter(initialCategory), 100);
    } else {
      const allPill = document.querySelector('[data-category="all"]');
      if (allPill) allPill.setAttribute('aria-pressed', 'true');
    }
  });

  // Copy link helper (attaches if a matching button exists)
  onReady(function copyLinkHelper() {
    const copyButton = document.querySelector('button[onclick*="clipboard"], button[data-copy-link]');
    if (!copyButton) return;
    copyButton.addEventListener('click', function () {
      const text = this.getAttribute('data-copy-link') || window.location.href;
      navigator.clipboard
        .writeText(text)
        .then(() => {
          const originalHTML = copyButton.innerHTML;
          const originalBg = copyButton.style.backgroundColor;
          const originalColor = copyButton.style.color;
          copyButton.innerHTML = '✓ Copied!';
          copyButton.style.backgroundColor = 'var(--color-success)';
          copyButton.style.color = 'white';
          setTimeout(function () {
            copyButton.innerHTML = originalHTML;
            copyButton.style.backgroundColor = originalBg;
            copyButton.style.color = originalColor;
          }, 2000);
        })
        .catch(() => {
          // no-op
        });
    });
  });
})();
