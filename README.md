# Articulate English — The Ascent

Marketing and storefront site for Articulate English. Built on the same
architecture as the portfolio site (`WGT-Edutech/Portfolio`), with ESL content
and the real learning-material screenshots.

Live: https://articulate-english.github.io/portal/

## Architecture (mirrors the portfolio)

Six scroll rooms, driven by one hand-rolled `requestAnimationFrame` loop capped at 30fps:

| Room | Height | Content |
|---|---|---|
| r1 | 700vh | DNA-helix loader — 13 bars rotating in 3D, "keep scrolling down" |
| r2 | 900vh | Three.js particle ring — 200 cyan + 250 violet points, cursor-repel, swells near the pointer |
| r3 | 800vh | Name reveal — "ARTICULATE ENGLISH", character by character |
| r4 | 400vh | Role + slogan — "English Lessons" / "Learn English the way it's actually spoken." |
| r5 | 120vh | Shrink-to-nav transition |
| r6 | 1400vh | Cover-flow gallery — 12 material cards with mirrored reflections |

Plus: phase dots, variable-proximity text (Roboto Flex `wght`/`opsz` follows the cursor),
mobile menu, landscape prompt, autoplay-after-4s-idle.

Below the scroll experience: **Playground** (3 interactive toys), **Materials**
(12 product detail sections), **Pricing** (3 tiers), footer.

## Differences from the portfolio

- ESL text throughout, and 12 real learning-material screenshots
- **Logo** — the inline SVG "A" monogram from `articulate-english/b2-fce-speaking`
  (cyan `#22d3ee` circle, white A, adaptive outline). Same mark as the favicon.
- **Colour theme toggle** — sun/moon switch, persists to `localStorage`, respects
  `prefers-color-scheme`. Full light theme.
- **Playground** — pop-the-words bubbles, flip cards, sort-the-phrase
- **Commerce** — Gumroad CTAs on every material and pricing tier

## Assets

- `assets/cards/*.webp` — 12 screenshots, compressed from the portfolio originals
  (6.1 MB → 166 KB), lazy-loaded
- `assets/favicon.svg` — the mark

Three.js is loaded from `cdn.jsdelivr.net` (as the portfolio does).

## Gumroad setup

1. Create products on Gumroad.
2. Replace every `href="#"` on a `.btn-gumroad` with the real product URL.
3. Until then, buttons show a "being set up" notice.

## Local preview

```bash
python -m http.server 8123 --bind 127.0.0.1
# open http://127.0.0.1:8123/
```

## Verification notes

- `node --check` on the inline script passes; zero console errors on load.
- Motion, frame rate and Lighthouse scores require a real browser — headless Chrome
  reports `document.visibilityState === 'hidden'`, which stops `requestAnimationFrame`.
- One improvement over the portfolio: `updateAllVP()` now re-measures only when the
  pointer actually moved (the original called `getBoundingClientRect()` on every
  character every frame).
- `assets/nebula-*.webp` are currently **unreferenced** — kept because the nebula
  background was requested earlier. Say the word and it goes back in behind the particles.
