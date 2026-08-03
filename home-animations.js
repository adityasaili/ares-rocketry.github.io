/* ==========================================================
   Home page space theme: starfield + smooth scroll + reveals
   Only loaded on index.html — safe to keep separate from
   the site-wide script.js so no other page is affected.
   ========================================================== */

document.addEventListener('DOMContentLoaded', () => {

    let particlesContainer = null;
    let lenis = null;
    let lenisRafId = null;

    /* ---------- 1. Starfield background (tsParticles) ---------- */
    if (window.tsParticles) {
        tsParticles.load({
            id: 'starfield',
            options: {
                fullScreen: { enable: false },
                background: { color: { value: 'transparent' } },
                fpsLimit: 30,
                particles: {
                    number: { value: 80, density: { enable: true, area: 1000 } },
                    color: { value: ['#ffffff', '#9fd8f5', '#46c8f0'] },
                    opacity: {
                        value: { min: 0.15, max: 0.9 },
                        animation: { enable: true, speed: 0.5, sync: false, startValue: 'random' }
                    },
                    size: { value: { min: 0.4, max: 1.8 } },
                    move: {
                        enable: true,
                        speed: 0.12,
                        direction: 'none',
                        random: true,
                        straight: false,
                        outModes: { default: 'out' }
                    },
                    links: { enable: false }
                },
                detectRetina: true
            }
        }).then((container) => { particlesContainer = container; })
          .catch(() => { /* fail silently — dark background still looks fine without it */ });
    }

    /* ---------- 2. Lenis smooth scroll ---------- */
    function startLenisLoop() {
        if (!lenis || lenisRafId !== null) return;
        const raf = (time) => {
            lenis.raf(time);
            lenisRafId = requestAnimationFrame(raf);
        };
        lenisRafId = requestAnimationFrame(raf);
    }

    function stopLenisLoop() {
        if (lenisRafId !== null) {
            cancelAnimationFrame(lenisRafId);
            lenisRafId = null;
        }
    }

    if (window.Lenis) {
        lenis = new Lenis({ duration: 1.1, smoothWheel: true });
        lenis.on('scroll', () => {
            if (window.ScrollTrigger) ScrollTrigger.update();
        });
        startLenisLoop();
    }

    /* ---------- Pause everything when the tab isn't visible ---------- */
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (particlesContainer) particlesContainer.pause();
            stopLenisLoop();
        } else {
            if (particlesContainer) particlesContainer.play();
            startLenisLoop();
        }
    });

    /* ---------- 3. GSAP scroll-triggered reveals ---------- */
    if (window.gsap && window.ScrollTrigger) {
        gsap.registerPlugin(ScrollTrigger);

        gsap.utils.toArray('.stat-card').forEach((el, i) => {
            gsap.fromTo(el,
                { opacity: 0, y: 30 },
                {
                    opacity: 1, y: 0, duration: 0.7, delay: i * 0.08, ease: 'power2.out',
                    scrollTrigger: { trigger: el, start: 'top 88%' }
                }
            );
        });

        gsap.fromTo('.mission-spotlight__visual',
            { opacity: 0, x: -40 },
            {
                opacity: 1, x: 0, duration: 0.9, ease: 'power2.out',
                scrollTrigger: { trigger: '.mission-spotlight', start: 'top 75%' }
            }
        );

        gsap.fromTo('.mission-spotlight__content',
            { opacity: 0, x: 40 },
            {
                opacity: 1, x: 0, duration: 0.9, ease: 'power2.out',
                scrollTrigger: { trigger: '.mission-spotlight', start: 'top 75%' }
            }
        );

        gsap.fromTo('.leadership h2, .leadership__intro',
            { opacity: 0, y: 20 },
            {
                opacity: 1, y: 0, duration: 0.7, ease: 'power2.out',
                scrollTrigger: { trigger: '.leadership', start: 'top 80%' }
            }
        );

        gsap.utils.toArray('.leadership-card').forEach((el, i) => {
            gsap.fromTo(el,
                { opacity: 0, y: 30 },
                {
                    opacity: 1, y: 0, duration: 0.6, delay: i * 0.1, ease: 'power2.out',
                    scrollTrigger: { trigger: el, start: 'top 90%' }
                }
            );
        });

        gsap.fromTo('.subteams-teaser h2, .subteams-teaser__intro',
            { opacity: 0, y: 20 },
            {
                opacity: 1, y: 0, duration: 0.7, ease: 'power2.out',
                scrollTrigger: { trigger: '.subteams-teaser', start: 'top 80%' }
            }
        );

        gsap.utils.toArray('.subteam-chip').forEach((el, i) => {
            gsap.fromTo(el,
                { opacity: 0, scale: 0.85 },
                {
                    opacity: 1, scale: 1, duration: 0.5, delay: i * 0.05, ease: 'back.out(1.6)',
                    scrollTrigger: { trigger: el, start: 'top 92%' }
                }
            );
        });

        gsap.fromTo('.cta-band__inner',
            { opacity: 0, y: 24 },
            {
                opacity: 1, y: 0, duration: 0.8, ease: 'power2.out',
                scrollTrigger: { trigger: '.cta-band', start: 'top 85%' }
            }
        );
    }
});
