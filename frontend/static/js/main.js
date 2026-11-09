/* =========================================================
   EURY NATURE CABANA — main.js v4
   GSAP 3.12 + Lenis 1.1 + React Bits–inspired effects
   ========================================================= */

// ===== GSAP SETUP =====
gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothTouch: false,
});

gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
lenis.on('scroll', ScrollTrigger.update);

// ===== PAGE LOADER =====
window.addEventListener('load', () => {
    const loader = document.getElementById('pageLoader');
    if (loader) setTimeout(() => loader.classList.add('hidden'), 450);
});

// ===== SCROLL PROGRESS BAR =====
const progressBar = document.createElement('div');
progressBar.className = 'scroll-progress';
document.body.prepend(progressBar);
lenis.on('scroll', ({ progress }) => {
    progressBar.style.width = (progress * 100) + '%';
});

// ===== NAVBAR =====
const navbar = document.getElementById('navbar');
const backToTop = document.getElementById('backToTop');
const isHomepage = !!document.querySelector('.hero');

if (isHomepage) {
    navbar.classList.add('transparent');
    document.body.classList.add('has-transparent-nav');
}

function updateNavbar() {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
    if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 300);
}
window.addEventListener('scroll', updateNavbar, { passive: true });
updateNavbar();

// ===== HAMBURGER =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('active');
        const spans = hamburger.querySelectorAll('span');
        if (hamburger.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
        } else {
            spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
        }
    });
}

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        if (hamburger) {
            hamburger.classList.remove('active');
            hamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
        }
    });
});

if (backToTop) {
    backToTop.addEventListener('click', () => lenis.scrollTo(0, { duration: 1.4 }));
}

// ===== HERO VIDEO =====
const heroVideo = document.querySelector('.hero-video');
if (heroVideo && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.pause();
    heroVideo.removeAttribute('autoplay');
}

// ===== HERO ENTRANCE ANIMATION =====
if (isHomepage) {
    gsap.set(['.hero-badge', '.hero-title', '.hero-sub', '.hero-actions', '.hero-booking-bar'], {
        autoAlpha: 0, y: 32
    });
    gsap.set('.hero-scroll-indicator', { autoAlpha: 0 });

    const heroTl = gsap.timeline({ delay: 0.5 });
    heroTl
        .to('.hero-badge',            { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out' })
        .to('.hero-title',            { autoAlpha: 1, y: 0, duration: 1.0, ease: 'power2.out' }, '-=0.2')
        .to('.hero-sub',              { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out' }, '-=0.4')
        .to('.hero-actions',          { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out' }, '-=0.3')
        .to('.hero-scroll-indicator', { autoAlpha: 1, duration: 0.5 }, '-=0.1')
        .to('.hero-booking-bar',      { autoAlpha: 1, y: 0, duration: 0.7, ease: 'power2.out' }, '-=0.4');

    // Hero parallax
    gsap.to('.hero-video-wrap', {
        yPercent: 25, ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1.5 }
    });

    // Fade scroll indicator out on scroll
    gsap.to('.hero-scroll-indicator', {
        autoAlpha: 0,
        scrollTrigger: { trigger: '.hero', start: '5% top', end: '12% top', scrub: true }
    });
}

// ===== ROTATING WORDS (React Bits RotatingText-inspired) =====
const rotWords = [...document.querySelectorAll('.rotating-word')];
if (rotWords.length > 1) {
    let cur = 0;
    gsap.set(rotWords, { autoAlpha: 0, y: 28, filter: 'blur(8px)' });
    gsap.to(rotWords[0], { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: 0.6, ease: 'power2.out', delay: 1.4 });

    setInterval(() => {
        const prev = rotWords[cur];
        cur = (cur + 1) % rotWords.length;
        gsap.to(prev, { autoAlpha: 0, y: -28, filter: 'blur(6px)', duration: 0.4, ease: 'power2.in' });
        gsap.fromTo(rotWords[cur],
            { autoAlpha: 0, y: 28, filter: 'blur(6px)' },
            { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: 0.5, ease: 'power2.out', delay: 0.25 }
        );
    }, 2800);
}

// ===== SECTION TITLE BLUR REVEAL (React Bits BlurText-inspired) =====
document.querySelectorAll('.section-title').forEach(el => {
    gsap.fromTo(el,
        { autoAlpha: 0, filter: 'blur(16px)', y: 16 },
        {
            autoAlpha: 1, filter: 'blur(0px)', y: 0,
            duration: 1, ease: 'power2.out',
            scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' }
        }
    );
});

// ===== SCROLL REVEALS (GSAP replaces IntersectionObserver) =====
function initReveal(selector, fromVars, dur) {
    gsap.utils.toArray(selector).forEach(el => {
        const siblings = [...(el.parentElement?.children || [])].filter(c => c.matches && c.matches(selector));
        const delay = Math.min(siblings.indexOf(el) * 0.11, 0.55);
        gsap.fromTo(el,
            { autoAlpha: 0, ...fromVars },
            {
                autoAlpha: 1, y: 0, x: 0, scale: 1,
                duration: dur || 0.85, delay,
                ease: 'power3.out',
                scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' }
            }
        );
    });
}
initReveal('.reveal',       { y: 50 });
initReveal('.reveal-left',  { x: -60, y: 0 });
initReveal('.reveal-right', { x: 60, y: 0 });
initReveal('.reveal-zoom',  { scale: 0.88, y: 0 });

// ===== PAGE HERO PARALLAX (inner pages) =====
const pageHeroBg = document.querySelector('.page-hero-bg');
if (pageHeroBg) {
    gsap.to(pageHeroBg, {
        yPercent: 25, ease: 'none',
        scrollTrigger: { trigger: '.page-hero', start: 'top top', end: 'bottom top', scrub: 1.5 }
    });
}

// ===== SECTION TAG FADE IN =====
document.querySelectorAll('.section-tag').forEach(el => {
    gsap.fromTo(el,
        { autoAlpha: 0, y: 12 },
        {
            autoAlpha: 1, y: 0, duration: 0.5, ease: 'power2.out',
            scrollTrigger: { trigger: el, start: 'top 90%', toggleActions: 'play none none none' }
        }
    );
});

// ===== STAT COUNTER (data-count attribute) =====
function animateCounter(el) {
    const target = parseInt(el.dataset.count);
    if (isNaN(target)) return;
    const suffix = el.dataset.suffix || '';
    const obj = { val: 0 };
    gsap.to(obj, {
        val: target, duration: 2, ease: 'power1.out',
        onUpdate() { el.textContent = Math.floor(obj.val) + suffix; }
    });
}
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });
document.querySelectorAll('.counter').forEach(el => counterObserver.observe(el));

// ===== CURSOR GLOW (React Bits-inspired, desktop only) =====
if (window.matchMedia('(pointer: fine)').matches && !('ontouchstart' in window)) {
    const glow = document.createElement('div');
    glow.className = 'cursor-glow';
    document.body.appendChild(glow);
    document.addEventListener('mousemove', e => {
        gsap.to(glow, { x: e.clientX, y: e.clientY, duration: 1.4, ease: 'power3.out', overwrite: 'auto' });
    });
}

// ===== TESTIMONIALS SLIDER =====
const testTrack = document.querySelector('.testimonials-track');
const testDots = document.querySelectorAll('.test-dot');
let currentTest = 0, testInterval;

function goToTestimonial(n) {
    currentTest = (n + testDots.length) % testDots.length;
    if (testTrack) testTrack.style.transform = `translateX(-${currentTest * 100}%)`;
    testDots.forEach(d => d.classList.remove('active'));
    testDots[currentTest]?.classList.add('active');
}
function startTestSlider() {
    testInterval = setInterval(() => goToTestimonial(currentTest + 1), 5500);
}
if (testTrack) {
    goToTestimonial(0);
    startTestSlider();
    testDots.forEach((dot, i) => dot.addEventListener('click', () => {
        clearInterval(testInterval);
        goToTestimonial(i);
        startTestSlider();
    }));
}

// ===== BOOKING BAR =====
const heroBookingForm = document.getElementById('heroBookingBar');
if (heroBookingForm) {
    heroBookingForm.addEventListener('submit', e => {
        e.preventDefault();
        const ci = document.getElementById('heroCheckin')?.value || '';
        const co = document.getElementById('heroCheckout')?.value || '';
        const g  = document.getElementById('heroGuests')?.value || '2';
        window.location.href = `book.html?checkin=${ci}&checkout=${co}&guests=${g}`;
    });
}

// ===== IMAGE LIGHTBOX =====
const lightbox = document.createElement('div');
lightbox.id = 'lightbox';
lightbox.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:3000;display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;cursor:pointer;';
lightbox.innerHTML = '<button style="position:absolute;top:20px;right:28px;background:none;border:none;color:white;font-size:2.5rem;cursor:pointer;" onclick="closeLightbox(event)">&times;</button><div id="lightboxContent" style="max-width:90vw;max-height:85vh;text-align:center;"></div>';
document.body.appendChild(lightbox);

function openLightbox(content) {
    document.getElementById('lightboxContent').innerHTML = content;
    gsap.to(lightbox, { autoAlpha: 1, duration: 0.3, ease: 'power2.out' });
    document.body.style.overflow = 'hidden';
}
function closeLightbox(e) {
    if (e) e.stopPropagation();
    gsap.to(lightbox, { autoAlpha: 0, duration: 0.25, ease: 'power2.in' });
    document.body.style.overflow = '';
}
lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });

document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
        const bg = item.querySelector('.gallery-img');
        if (bg) openLightbox(`<div style="width:600px;max-width:85vw;height:400px;background:${getComputedStyle(bg).background};border-radius:8px;"></div>`);
    });
});

// ===== COOKIE NOTICE =====
if (!localStorage.getItem('cabana_cookie_accepted')) {
    const cookie = document.createElement('div');
    cookie.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#1a1a1a;color:#ccc;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;z-index:1500;font-size:0.85rem;gap:20px;flex-wrap:wrap;';
    cookie.innerHTML = '<span>🍃 We use cookies to enhance your experience. <a href="#" style="color:#b89650;">Learn more</a></span><button onclick="this.parentElement.remove();localStorage.setItem(\'cabana_cookie_accepted\',\'1\')" style="background:var(--forest-500);color:white;border:none;padding:8px 20px;border-radius:40px;cursor:pointer;font-size:0.8rem;letter-spacing:0.08em;flex-shrink:0;">Accept</button>';
    document.body.appendChild(cookie);
}

// ===== FAQ ACCORDION =====
document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
        const item = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item.open').forEach(open => {
            open.classList.remove('open');
            open.querySelector('.faq-icon').textContent = '+';
        });
        if (!isOpen) {
            item.classList.add('open');
            btn.querySelector('.faq-icon').textContent = '\xD7';
        }
    });
});

// ===== ACTIVE NAV LINK =====
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href') || '';
    if (currentPath.endsWith(href) || (href === 'index.html' && (currentPath === '/' || currentPath.endsWith('/')))) {
        link.style.color = 'var(--amber-500)';
        link.style.fontWeight = '600';
    }
});

// ===== GLOBALS =====
window.openBooking   = () => window.location.href = 'book.html';
window.closeBooking  = () => {};
window.closeLightbox = closeLightbox;
