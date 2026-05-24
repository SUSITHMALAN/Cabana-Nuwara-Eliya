/* =========================================================
   CABANA NUWARA ELIYA - Main JavaScript
   ========================================================= */

// ===================== PAGE LOADER =====================
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('pageLoader');
        if (loader) loader.classList.add('hidden');
    }, 1400);
});

// ===================== SCROLL PROGRESS BAR =====================
const progressBar = document.createElement('div');
progressBar.className = 'scroll-progress';
document.body.prepend(progressBar);

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = (scrollTop / docHeight) * 100;
    progressBar.style.width = pct + '%';
});

// ===================== NAVBAR =====================
const navbar = document.getElementById('navbar');
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.scrollY > 80) {
        navbar.classList.add('scrolled');
        backToTop.classList.add('visible');
    } else {
        navbar.classList.remove('scrolled');
        backToTop.classList.remove('visible');
    }
});

// Hamburger Menu
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

// Close mobile nav on link click
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        if (hamburger) {
            hamburger.classList.remove('active');
            hamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
        }
    });
});

// Back to top
if (backToTop) {
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===================== HERO SLIDER =====================
const heroSlides = document.querySelectorAll('.hero-slide');
const heroDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;
let slideInterval;

function goToSlide(n) {
    heroSlides.forEach(s => s.classList.remove('active'));
    heroDots.forEach(d => d.classList.remove('active'));
    currentSlide = (n + heroSlides.length) % heroSlides.length;
    heroSlides[currentSlide].classList.add('active');
    heroDots[currentSlide]?.classList.add('active');
}

function nextSlide() { goToSlide(currentSlide + 1); }
function prevSlide() { goToSlide(currentSlide - 1); }

function startSlider() {
    slideInterval = setInterval(nextSlide, 5000);
}

if (heroSlides.length > 0) {
    goToSlide(0);
    startSlider();

    heroDots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(slideInterval);
            goToSlide(i);
            startSlider();
        });
    });

    const prevBtn = document.getElementById('heroPrev');
    const nextBtn = document.getElementById('heroNext');
    if (prevBtn) prevBtn.addEventListener('click', () => { clearInterval(slideInterval); prevSlide(); startSlider(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { clearInterval(slideInterval); nextSlide(); startSlider(); });

    // Touch/swipe support
    let touchStartX = 0;
    const heroEl = document.querySelector('.hero');
    if (heroEl) {
        heroEl.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
        heroEl.addEventListener('touchend', e => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) {
                clearInterval(slideInterval);
                diff > 0 ? nextSlide() : prevSlide();
                startSlider();
            }
        });
    }
}

// ===================== TESTIMONIALS SLIDER =====================
const testTrack = document.querySelector('.testimonials-track');
const testDots = document.querySelectorAll('.test-dot');
let currentTest = 0;
let testInterval;

function goToTestimonial(n) {
    const total = testDots.length;
    currentTest = (n + total) % total;
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
    testDots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(testInterval);
            goToTestimonial(i);
            startTestSlider();
        });
    });
}

// ===================== BOOKING MODAL =====================
function openBooking() {
    window.location.href = '/book';
}
function closeBooking() {
    // Legacy support
}

// ===================== SCROLL REVEAL =====================
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, entry.target.dataset.delay || 0);
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el, i) => {
    // Stagger siblings
    const parent = el.parentElement;
    const siblings = [...parent.children].filter(c => c.classList.contains('reveal') || c.classList.contains('reveal-left') || c.classList.contains('reveal-right'));
    const idx = siblings.indexOf(el);
    el.dataset.delay = idx * 100;
    revealObserver.observe(el);
});

// ===================== HERO BOOKING BAR =====================
const heroBookingForm = document.getElementById('heroBookingBar');
if (heroBookingForm) {
    heroBookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const checkin = heroBookingForm.checkin.value;
        const checkout = heroBookingForm.checkout.value;
        const adults = heroBookingForm.adults.value;
        window.location.href = `/book?checkin=${checkin}&checkout=${checkout}&guests=${adults}`;
    });
}

// ===================== COUNTER ANIMATION =====================
function animateCounter(el) {
    const target = parseInt(el.dataset.count);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = Math.floor(current) + (el.dataset.suffix || '');
    }, 16);
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

// ===================== IMAGE LIGHTBOX =====================
const lightbox = document.createElement('div');
lightbox.id = 'lightbox';
lightbox.style.cssText = `
    position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:3000;
    display:flex;align-items:center;justify-content:center;
    opacity:0;visibility:hidden;transition:all 0.3s ease;cursor:pointer;
`;
lightbox.innerHTML = `
    <button style="position:absolute;top:20px;right:28px;background:none;border:none;color:white;font-size:2.5rem;cursor:pointer;line-height:1;" onclick="closeLightbox(event)">&times;</button>
    <div id="lightboxContent" style="max-width:90vw;max-height:85vh;text-align:center;"></div>
`;
document.body.appendChild(lightbox);

function openLightbox(content) {
    document.getElementById('lightboxContent').innerHTML = content;
    lightbox.style.opacity = '1';
    lightbox.style.visibility = 'visible';
    document.body.style.overflow = 'hidden';
}
function closeLightbox(e) {
    if (e) e.stopPropagation();
    lightbox.style.opacity = '0';
    lightbox.style.visibility = 'hidden';
    document.body.style.overflow = '';
}
lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });

document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
        const bg = item.querySelector('.gallery-img');
        if (bg) {
            openLightbox(`<div style="width:600px;max-width:85vw;height:400px;background:${getComputedStyle(bg).background};border-radius:8px;"></div>`);
        }
    });
});

// ===================== COOKIE NOTICE =====================
if (!localStorage.getItem('cabana_cookie_accepted')) {
    const cookie = document.createElement('div');
    cookie.style.cssText = `
        position:fixed;bottom:0;left:0;right:0;background:#1a1a1a;color:#ccc;
        padding:16px 32px;display:flex;align-items:center;justify-content:space-between;
        z-index:1500;font-size:0.85rem;gap:20px;flex-wrap:wrap;
    `;
    cookie.innerHTML = `
        <span>🍃 We use cookies to enhance your experience at Cabana Nuwara Eliya. <a href="#" style="color:#b89650;">Learn more</a></span>
        <button onclick="this.parentElement.remove();localStorage.setItem('cabana_cookie_accepted','1')"
            style="background:#2c5f2e;color:white;border:none;padding:8px 20px;border-radius:4px;cursor:pointer;font-size:0.8rem;letter-spacing:0.08em;flex-shrink:0;">
            Accept
        </button>
    `;
    document.body.appendChild(cookie);
}

// ===================== PARALLAX EFFECT =====================
window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    document.querySelectorAll('.parallax-bg').forEach(el => {
        el.style.transform = `translateY(${scrollY * 0.3}px)`;
    });
});

// ===================== ACTIVE NAV LINK =====================
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.style.color = 'var(--primary)';
        link.style.fontWeight = '600';
    }
});

// Make openBooking and closeBooking global
window.openBooking = openBooking;
window.closeBooking = closeBooking;
window.closeLightbox = closeLightbox;
