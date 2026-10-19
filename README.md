# Articulate English — PWA Portal

Static portal page showcasing Articulate English's Progressive Web Apps with Gumroad purchase links.

## Products

| App | Description | Price | Status |
|---|---|---|---|
| Alien Guitar Tuner | Cosmic guitar tuner with pitch detection | Free | Ready |
| Alien Metronome | Cosmic metronome with FX and synth | Free | Ready |
| IELTS Speaking Practice | 12 IELTS speaking decks | $4.99 | Ready |
| Tesselaarsdal Syntropic Farm | Investment proposal PWA | $0.99 | Ready |

## Gumroad Setup

1. Create products on [Gumroad](https://gumroad.com) for each app
2. Update the `href="#"` links in `index.html` with actual Gumroad product URLs
3. Format: `https://<your-username>.gumroad.com/l/<product-id>`

## Development

Single-file static site — no build step. Edit `index.html` directly.

## Deployment

Push to `main` branch. GitHub Pages serves from root.

```bash
git add index.html
git commit -m "Update portal"
git push origin main
```

Live URL: https://articulate-english.github.io/portal/
