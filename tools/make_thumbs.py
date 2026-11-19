# -*- coding: utf-8 -*-
"""Generate the portal lesson-card thumbnails.

Designed product cards (840x560 = 2x the 420x280 card) instead of app screenshots:
consistent layout, per-product accent, product name + one benefit line + brand mark.

Run:  uv run --with pillow python tools/make_thumbs.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cards")
W, H = 840, 560

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_LIGHT = "C:/Windows/Fonts/segoeuil.ttf"

# slug: (title lines, benefit, accent rgb)
CARDS = {
    "ielts-speaking-mastery": (["IELTS Speaking", "Mastery"], "Exam-ready speaking, end to end", (34, 211, 238)),
    "ielts-slide-decks": (["IELTS Slide Decks"], "Visual decks for exam speaking class", (56, 189, 248)),
    "ielts-speaking-packs": (["IELTS Speaking", "Packs"], "Packs for every part of the test", (45, 212, 191)),
    "exam-speaking-practice": (["Exam Speaking", "Practice"], "Real exam-style speaking practice", (96, 165, 250)),
    "speaking-slide-decks": (["Speaking Slide", "Decks"], "Open-ended decks that get students talking", (167, 139, 250)),
    "sliding-in": (["Speaking:", "Sliding In"], "107 topics · 1,452 questions · offline app", (129, 140, 248)),
    "travel-english": (["Travel English"], "Speak confidently on any trip", (251, 191, 36)),
    "banking-investment-english": (["Banking &", "Investment English"], "Money language that actually lands", (52, 211, 153)),
    "business-english": (["Business English"], "Meetings, emails and small talk that work", (251, 113, 133)),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_bg(top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bottom, y / (H - 1)))
    return img


def glow(accent):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([W * 0.45, -H * 0.35, W * 1.35, H * 0.65], fill=accent + (70,))
    d.ellipse([-W * 0.25, H * 0.45, W * 0.55, H * 1.45], fill=accent + (28,))
    return layer.filter(ImageFilter.GaussianBlur(90))


def motif(d, accent):
    """Concentric rings + a diagonal beam: one consistent system, per-card accent."""
    cx, cy = int(W * 0.78), int(H * 0.42)
    for i, r in enumerate((150, 205, 262, 322)):
        alpha = 120 - i * 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent + (max(0, alpha),), width=3)
    d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=accent + (38,))
    d.polygon([(W * 0.62, H), (W * 0.86, 0), (W * 0.98, 0), (W * 0.74, H)], fill=accent + (16,))


def text_block(d, title_lines, benefit, accent):
    f_title = ImageFont.truetype(FONT_BOLD, 74)
    f_sub = ImageFont.truetype(FONT_REG, 27)
    f_brand = ImageFont.truetype(FONT_BOLD, 19)
    f_meta = ImageFont.truetype(FONT_REG, 21)

    x = 74
    y = 118
    for line in title_lines:
        d.text((x, y), line, font=f_title, fill=(247, 246, 255))
        y += 84

    # accent rule
    d.rounded_rectangle([x, y + 6, x + 62, y + 12], radius=3, fill=accent + (255,))
    y += 40
    d.text((x, y), benefit, font=f_sub, fill=(196, 190, 220))

    # brand mark
    d.text((74, 52), "ARTICULATE ENGLISH", font=f_brand, fill=(150, 145, 180))
    d.text((74, H - 58), "B1+ / B2  ·  ENGLISH SPEAKING", font=f_meta, fill=(110, 106, 140))


def build(slug, title_lines, benefit, accent):
    img = gradient_bg((13, 12, 24), (24, 22, 42)).convert("RGBA")
    img.alpha_composite(glow(accent))
    d = ImageDraw.Draw(img, "RGBA")
    motif(d, accent)

    # vignette for depth
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).rectangle([0, 0, W, H], fill=0)
    img = Image.alpha_composite(
        img, Image.new("RGBA", (W, H), (0, 0, 0, 0))
    )
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], outline=(255, 255, 255, 10), width=2)

    text_block(d, title_lines, benefit, accent)

    out = os.path.join(OUT, slug + ".png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (title, benefit, accent) in CARDS.items():
        path = build(slug, title, benefit, accent)
        print("%-28s %6d bytes" % (os.path.basename(path), os.path.getsize(path)))


if __name__ == "__main__":
    main()
