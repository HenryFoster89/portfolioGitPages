// ================================
// DATA ANALYTICS PORTFOLIO - MAIN.JS
// Enrico Stancanelli
// ================================

// ================================
// 1. MOBILE MENU TOGGLE
// ================================
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

function toggleMenu() {
  navMenu.classList.toggle('active');
  hamburger.classList.toggle('active');
}

if (hamburger) {
  hamburger.addEventListener('click', toggleMenu);

  // Close menu when clicking nav link
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (navMenu.classList.contains('active')) {
        toggleMenu();
      }
    });
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
      if (navMenu.classList.contains('active')) {
        toggleMenu();
      }
    }
  });
}

// ================================
// 2. SMOOTH SCROLL WITH OFFSET
// ================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');

    // Ignore empty anchors
    if (href === '#') {
      e.preventDefault();
      return;
    }

    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      const navbar = document.querySelector('.navbar');
      const navHeight = navbar ? navbar.offsetHeight : 0;
      const targetPosition = target.offsetTop - navHeight;

      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  });
});

// ================================
// 3. INTERSECTION OBSERVER (Fade-in animations)
// ================================
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Keep observing for repeatable animations if needed
      // observer.unobserve(entry.target); // Uncomment to trigger only once
    }
  });
}, observerOptions);

// Observe all fade-in elements
document.querySelectorAll('.fade-in').forEach(el => {
  observer.observe(el);
});

// ================================
// 4. ACTIVE NAV LINK HIGHLIGHTING
// ================================
const sections = document.querySelectorAll('section[id]');

function highlightNavigation() {
  const scrollY = window.pageYOffset;

  sections.forEach(section => {
    const sectionHeight = section.offsetHeight;
    const sectionTop = section.offsetTop - 100;
    const sectionId = section.getAttribute('id');
    const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
      navLinks.forEach(link => link.classList.remove('active'));
      if (navLink) navLink.classList.add('active');
    }
  });
}

// Only run if there are sections with IDs
if (sections.length > 0) {
  window.addEventListener('scroll', highlightNavigation);
  // Run once on load
  highlightNavigation();
}

// ================================
// 5. NAVBAR SCROLL EFFECT
// ================================
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll > 100) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }

  lastScroll = currentScroll;
});

// ================================
// 6. SKILL BARS ANIMATION
// ================================
const skillBars = document.querySelectorAll('.skill-progress');

if (skillBars.length > 0) {
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const progress = entry.target.getAttribute('data-progress');
        entry.target.style.width = progress + '%';
        skillObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  skillBars.forEach(bar => skillObserver.observe(bar));
}

// ================================
// 7. SCROLL TO TOP BUTTON
// ================================
// Check if button already exists (to avoid duplicates)
let scrollTopBtn = document.querySelector('.scroll-top-btn');

if (!scrollTopBtn) {
  scrollTopBtn = document.createElement('button');
  scrollTopBtn.innerHTML = '↑';
  scrollTopBtn.className = 'scroll-top-btn';
  scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
  document.body.appendChild(scrollTopBtn);
}

window.addEventListener('scroll', () => {
  if (window.pageYOffset > 500) {
    scrollTopBtn.classList.add('visible');
  } else {
    scrollTopBtn.classList.remove('visible');
  }
});

scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ================================
// 8. PROJECT CARD CLICK HANDLING
// ================================
const projectCards = document.querySelectorAll('.project-card');

projectCards.forEach(card => {
  card.addEventListener('click', function(e) {
    // Only navigate if not clicking on a link directly
    if (!e.target.closest('a')) {
      const link = this.querySelector('.project-link');
      if (link) {
        window.location.href = link.getAttribute('href');
      }
    }
  });
});

// ================================
// 9. DYNAMIC YEAR IN FOOTER
// ================================
const yearElement = document.querySelector('.current-year');
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// ================================
// 10. PERFORMANCE: LAZY LOADING IMAGES
// ================================
const images = document.querySelectorAll('img[data-src]');

if (images.length > 0 && 'IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
}

// ================================
// 11. ACCESSIBILITY: KEYBOARD NAVIGATION
// ================================
// Ensure hamburger menu can be toggled with Enter/Space
if (hamburger) {
  hamburger.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleMenu();
    }
  });
}

// ================================
// 12. CONSOLE LOG (Dev info)
// ================================
console.log('%c Portfolio Loaded Successfully! ', 'background: #3498DB; color: white; padding: 10px; font-size: 14px; font-weight: bold;');
console.log('%c Built by Enrico Stancanelli ', 'color: #2C3E50; font-size: 12px;');
console.log('%c Logistics Data Analyst ', 'color: #27AE60; font-size: 12px;');

// ================================
// 13. PREVENT LOADING FLICKER
// ================================
// Remove any loading class if present
document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.remove('loading');
});
