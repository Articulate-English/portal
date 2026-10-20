# Articulate English — The Ascent

A gamified, scroll-driven journey through Articulate English's ESL learning materials. Single-file static site (Lenis + GSAP ScrollTrigger), no build step.

Live: https://articulate-english.github.io/portal/

## What's inside

**Intro (r1–r5)**
- Cosmic nebula backdrop (WebP, layered with a dark scrim for text contrast)
- 3D double-helix light spiral — canvas 2D perspective projection, additive glow, drifting toward the viewer
- Particle-text hero title ("ARTICULATE") — React Bits ParticleText, ported to vanilla
- Slow even slide-up into "The Ascent" map
- Rare shooting stars (one every 4–8s, reduced-motion safe)
- Self-scrolling intro (14s), releases control on any user input

**The Ascent (r6)**
- Continuous cover-flow ring of 10 product families (no discrete stepping)
- Discovery meter (fixed, left) + checkpoint dots (fixed, right)
- "Collected N / 10" counter

**Below the fold**
- Scroll-velocity topic marquee
- 10 alternating product detail sections
- Pricing tiers + Gumroad CTAs
- Footer

## The 10 collections

| Collection | CEFR | Units | Price |
|---|---|---|---|
| IELTS Speaking Mastery | B1–C1 | 80+ decks | $29 |
| B1 Speaking Library | B1 | 17 decks | $12.99 |
| B2 Advanced Speaking | B2 | 8 decks | $12.99 |
| Grammar Vault | A2–C1 | 10+ decks | $12.99 |
| Linking Words Collection | B1–C2 | 4 decks | $6.99 |
| Business English Suite | B1–C1 | 13+ decks | $14.99 |
| Accent Reduction Lab | All | 5 guides | $9.99 |
| Exam Simulators | B2+ | 6 units | $14.99 |
| Young Learners | A1–A2 | 2 sets | $7.99 |
| Travel & Languages | A2–B1 | 8+ decks | $9.99 |

## Gumroad setup

1. Create products on [Gumroad](https://gumroad.com) for each collection (and/or the three tiers).
2. In `index.html`, replace every `href="#"` on a `.btn-gumroad` with the real product URL.
3. Format: `https://<username>.gumroad.com/l/<product-id>`
4. Until then, buttons show a "being set up" notice.

## Structure

```
index.html                      single-file site
assets/nebula-planet-bg.webp    cosmic backdrop (1920w)
assets/nebula-planet-bg-1280.webp  mobile variant
js/gsap.min.js                  vendored
js/ScrollTrigger.min.js         vendored
js/lenis.min.js                 vendored
```

## Local preview

```bash
python -m http.server 8123 --bind 127.0.0.1
# open http://127.0.0.1:8123/
```

## Deploy

Push to `main`. GitHub Pages serves from root.

```bash
git add index.html assets/ js/
git commit -m "Update site"
git push origin main
```

## Verification notes

- `node --check` on the inline script passes; zero console errors on load.
- Motion (spiral animation, scroll choreography, Lenis smoothing) requires a real
  browser — headless Chrome reports `document.visibilityState = "hidden"`, which
  stops `requestAnimationFrame`, so animation cannot be verified headlessly.
