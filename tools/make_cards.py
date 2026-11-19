# -*- coding: utf-8 -*-
"""Generate the portal lesson-card thumbnails in the site's own visual language.

Site tokens (index.html): --purple #8b5cf6, --accent2 #22d3ee, --text-cream #f4f1ea,
--bg #000, Oswald for display type, Inter for body. The motif is the site's own
particle ring, so the cards read as part of the same product.

840x560 (2x the 420x280 card). The bottom band is kept quiet because the card
caption bar overlays it when a card is active.

Run:  uv run --with pillow python tools/make_cards.py
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets", "cards")
FONTS = os.path.join(HERE, "fonts")

W, H = 840, 560
PURPLE = (139, 92, 246)
CYAN = (34, 211, 238)
CREAM = (244, 241, 234)

F_OSWALD = os.path.join(FONTS, "oswald-700.ttf")
F_INTER = os.path.join(FONTS, "inter-400.ttf")
F_INTER_SB = os.path.join(FONTS, "inter-600.ttf")

# slug: (title lines, benefit line)
CARDS = {
    "ielts-speaking-mastery": (["IELTS", "Speaking", "Mastery"], "Exam-ready speaking, end to end"),
    "ielts-slide-decks": (["IELTS", "Slide Decks"], "Visual decks for exam speaking class"),
    "ielts-speaking-packs": (["IELTS", "Speaking", "Packs"], "A pack for every part of the test"),
    "exam-speaking-practice": (["Exam", "Speaking", "Practice"], "Real exam-style speaking practice"),
    "speaking-slide-decks": (["Speaking", "Slide Decks"], "Open-ended decks that fill the room"),
    "sliding-in": (["Speaking:", "Sliding In"], "107 topics · 1,452 questions · offline app"),
    "travel-english": (["Travel", "English"], "Speak confidently on any trip"),
    "banking-investment-english": (["Banking &", "Investment", "English"], "Money language that lands"),
    "business-english": (["Business", "English"], "Meetings, email and small talk"),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def base_gradient():
    top, bottom = (5, 6, 15), (10, 7, 22)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bottom, y / (H - 1)))
    return img


def blobs():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([W * 0.38, -H * 0.30, W * 1.25, H * 0.55], fill=PURPLE + (95,))
    d.ellipse([-W * 0.30, H * 0.50, W * 0.45, H * 1.35], fill=CYAN + (40,))
    return layer.filter(ImageFilter.GaussianBlur(110))


def particle_ring(d, rng, accent, radius=150, n=44, squash=0.52):
    """Dots on an ellipse — the site's particle ring, redrawn for a flat card."""
    cx, cy = W * 0.74, H * 0.40
    for i in range(n):
        a = (i / n) * math.tau
        jitter = rng.uniform(-4, 4)
        x = cx + math.cos(a) * (radius + jitter)
        y = cy + math.sin(a) * (radius + jitter) * squash
        r = rng.uniform(1.6, 4.4)
        alpha = rng.randint(60, 190)
        d.ellipse([x - r, y - r, x + r, y + r], fill=accent + (alpha,))
    for i in range(12):
        a = rng.uniform(0, math.tau)
        x = cx + math.cos(a) * radius
        y = cy + math.sin(a) * radius * squash
        r = rng.uniform(2.5, 5.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=accent + (235,))


def accent_rule(d, x, y, w=74):
    for i in range(w):
        d.line([(x + i, y), (x + i, y + 6)], fill=lerp(PURPLE, CYAN, i / (w - 1)) + (255,))


def text_block(d, title_lines, benefit):
    n = len(title_lines)
    size, lead, y = (76, 84, 78) if n >= 3 else (82, 90, 92)
    f_title = ImageFont.truetype(F_OSWALD, size)
    f_sub = ImageFont.truetype(F_INTER, 27)
    f_brand = ImageFont.truetype(F_INTER_SB, 18)

    x = 70
    for line in title_lines:
        d.text((x, y), line, font=f_title, fill=CREAM + (255,))
        y += lead

    accent_rule(d, x, y + 4)
    y += 34
    d.text((x, y), benefit, font=f_sub, fill=CREAM + (140,))

    d.text((70, 46), "A R T I C U L A T E   E N G L I S H", font=f_brand, fill=CREAM + (120,))


def build(slug, title_lines, benefit, seed):
    rng = random.Random(seed)
    img = base_gradient().convert("RGBA")
    img.alpha_composite(blobs())
    d = ImageDraw.Draw(img, "RGBA")

    # back ring (cyan, larger, fainter) then front ring (purple) — as on the site
    particle_ring(d, rng, CYAN, radius=215, n=40)
    particle_ring(d, rng, PURPLE, radius=150, n=34)

    d.rectangle([1, 1, W - 2, H - 2], outline=PURPLE + (80,), width=2)

    text_block(d, title_lines, benefit)

    out = os.path.join(OUT, slug + ".png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (slug, (title, benefit)) in enumerate(CARDS.items()):
        path = build(slug, title, benefit, seed=1000 + i)
        print("%-30s %7d bytes" % (os.path.basename(path), os.path.getsize(path)))


if __name__ == "__main__":
    main()
