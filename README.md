# Articulate English — The Ascent

Storefront for Articulate English's slide-deck library.
Live: https://articulate-english.github.io/portal/

## What the page is

Intro scroll, then a cover-flow gallery of the products for sale, then three buy
buttons. Nothing after that.

| Room | Height | Content |
|---|---|---|
| r1 | 700vh | DNA-helix loader — 13 bars rotating in 3D, "keep scrolling down" |
| r2 | 900vh | Three.js particle ring — 200 cyan + 250 violet points, cursor-repel |
| r3 | 800vh | Name reveal — "ARTICULATE ENGLISH", character by character |
| r4 | 400vh | Role + slogan — "English Lessons" / "Learn English the way it's actually spoken." |
| r5 | 120vh | Fade the wordmark out, hand off to the gallery |
| r6 | 1400vh | Cover-flow gallery — 7 product cards with mirrored reflections |

After r6: `.card-actions` — three buy buttons (deck / level / library).

One hand-rolled `requestAnimationFrame` loop capped at 30fps drives all of it.
Variable-proximity text (Roboto Flex `wght`/`opsz` follows the cursor), landscape
prompt, autoplay-after-4s-idle.

## Products shown

Seven sale items — decks and lesson content only. Apps, tools and free products are
deliberately **not** listed here.

| Card | Price | Product |
|---|---|---|
| IELTS Speaking Mastery | $29 | portal of 12 topic decks (deck-1…deck-12) |
| IELTS Writing & Essays | $14.99 | structured slide deck |
| IELTS Slide Decks | $12.99 | topic-by-topic speaking decks |
| B1 Grammar Lessons | $12.99 | 12 lesson pages |
| B2 Grammar Lessons | $12.99 | 10 lesson pages |
| Linking Words B1–C2 | $6.99 | four decks of cohesive devices |
| Speaking: Sliding In | $9.99 | question-card deck |

Each card carries its title, price and buy link. The caption is only drawn on the
focused card, so the cover-flow never stacks text on text.

## Commerce

Two URL maps at the top of the inline script:

- `GUMROAD_URLS` — per product, keyed by slug
- `GUMROAD_BUNDLES` — per buy button, keyed by `data-bundle`

Paste real Gumroad URLs (`https://<you>.gumroad.com/l/<id>`). **An empty entry is
honest, not a placeholder**: the card relabels itself "On Gumroad soon" and the buy
button is `aria-disabled` instead of pointing at a dead link. No URL is ever
invented.

## Assets

- `assets/cards/*.webp` — product screenshots, lazy-loaded
- `assets/favicon.svg` — the mark

Three.js loads from `cdn.jsdelivr.net`.

## Local preview

```bash
python -m http.server 8123 --bind 127.0.0.1
# open http://127.0.0.1:8123/
```

## Verification notes

- `node --check` on the inline script passes; zero console errors on load.
- The cover-flow and all motion require a real browser. Headless Chrome reports
  `document.visibilityState === 'hidden'`, which throttles `requestAnimationFrame`
  to ~1fps, so the springs never converge there. To verify the gallery headlessly,
  drive rAF with a timer in a throwaway copy.
- `updateAllVP()` re-measures only when the pointer actually moved (the portfolio
  original called `getBoundingClientRect()` on every character every frame).
- Unreferenced files kept deliberately: `assets/cards/{whiteboard,video-call,
  video-lesson-maker,language-tool,vocab-forge}.webp` — the free tools and the
  VocabForge app that are intentionally not sold here.
