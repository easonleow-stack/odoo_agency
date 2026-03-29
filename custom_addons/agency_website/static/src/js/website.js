/**
 * Ads On Marketing — Frontend Website JS
 * Smooth animations, scroll effects, and interactive elements.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Smooth scroll for anchor links ──────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ── Navbar background on scroll ─────────────────────────────
    var header = document.querySelector('.agency-header');
    if (header) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
                header.style.boxShadow = '0 2px 20px rgba(15, 23, 42, 0.08)';
            } else {
                header.classList.remove('scrolled');
                header.style.boxShadow = 'none';
            }
        });
    }

    // ── Fade-in on scroll (Intersection Observer) ───────────────
    var fadeElements = document.querySelectorAll(
        '.service-card, .campaign-card, .portfolio-card, .value-card, ' +
        '.team-card, .kpi-card, .dashboard-card, .service-detail-row, ' +
        '.stat-item, .contact-form-wrapper, .contact-info-card'
    );

    if (fadeElements.length && 'IntersectionObserver' in window) {
        fadeElements.forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(24px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        });

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        fadeElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    // ── Active nav link highlighting ────────────────────────────
    var currentPath = window.location.pathname;
    document.querySelectorAll('.agency-nav-links .nav-link').forEach(function (link) {
        var href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
            link.style.color = '#6c63ff';
            link.style.fontWeight = '600';
        }
    });

});
