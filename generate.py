#!/usr/bin/env python3
"""Generate the 20 November 2026 news front page (v1).

Draws a one-page newspaper front page with PIL: masthead, region strip,
numbers strip, 3 hero cards, a 10-card grid, a dotted world map with a
numbered brief list, a DATE CHECK box and a sources footer.
All illustrations are original flat drawings coded below.
Output: entry.png (900 x 1024, under 1 MiB).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
OUT = "entry.png"

PAPER = (248, 244, 232)
INK = (20, 33, 61)
INK_SOFT = (58, 66, 84)
RED = (180, 35, 24)
RED_DK = (140, 25, 16)
RULE = (20, 33, 61)
CARD_BG = (255, 255, 255)
CARD_LINE = (198, 190, 168)
MUTED = (110, 106, 92)

REGION_COLORS = {
    "Asia-Pacific": (192, 57, 43),
    "Europe": (31, 97, 141),
    "North America": (30, 132, 73),
    "Middle East": (125, 60, 152),
    "Latin America": (185, 119, 14),
    "Africa": (160, 64, 0),
    "World": (93, 109, 126),
}

FDIR = "/usr/share/fonts/truetype/dejavu/"

def serif_b(sz):
    return ImageFont.truetype(FDIR + "DejaVuSerif-Bold.ttf", sz)

def serif(sz):
    return ImageFont.truetype(FDIR + "DejaVuSerif.ttf", sz)

def sans_b(sz):
    return ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", sz)

def sans(sz):
    return ImageFont.truetype(FDIR + "DejaVuSans.ttf", sz)

def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

TRUNCATED = []

def fit(draw, text, font, max_w, max_lines):
    """Wrap and truncate with an ellipsis so it never exceeds max_lines."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) > max_lines:
        TRUNCATED.append(text[:60])
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines

def text_c(draw, xy, s, font, fill, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

# ---------------------------------------------------------------- icons
def icon_market(d, x, y, w, h, c):
    # falling candlesticks + red down arrow
    bw = w / 6
    tops = [0.25, 0.35, 0.5, 0.6, 0.75]
    for i, t in enumerate(tops):
        bx = x + i * bw + bw * 0.2
        d.rectangle([bx, y + h * t, bx + bw * 0.6, y + h * (t + 0.18)],
                    fill=(192, 57, 43) if i % 2 == 0 else (30, 132, 73))
    d.line([(x + 4, y + h * 0.22), (x + w - 8, y + h * 0.8)], fill=RED, width=5)
    d.polygon([(x + w - 8, y + h * 0.8), (x + w - 22, y + h * 0.72),
               (x + w - 14, y + h * 0.92)], fill=RED)

def icon_baseball(d, x, y, w, h, c):
    cx, cy, r = x + w * 0.5, y + h * 0.5, min(w, h) * 0.4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=RED, width=3)
    # two curved seams, left and right
    for s in (-1, 1):
        pts = []
        for k in range(9):
            t = -1.0 + k * 0.25
            px = cx + s * r * 0.62 - s * math.sin(t * 1.1) * r * 0.18
            py = cy + t * r * 0.62
            pts.append((px, py))
        d.line(pts, fill=RED, width=2)
        for k in range(4):
            t = -0.75 + k * 0.5
            px = cx + s * r * 0.62 - s * math.sin(t * 1.1) * r * 0.18
            py = cy + t * r * 0.62
            d.line([(px - 3, py), (px + 3, py)], fill=RED, width=2)

def icon_shield(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.5
    d.polygon([(cx, y + h * 0.08), (cx + w * 0.3, y + h * 0.2),
               (cx + w * 0.28, y + h * 0.6), (cx, y + h * 0.88),
               (cx - w * 0.28, y + h * 0.6), (cx - w * 0.3, y + h * 0.2)],
              fill=(255, 255, 255), outline=INK, width=3)
    d.line([(cx - w * 0.16, cy + h * 0.02), (cx - w * 0.03, cy + h * 0.16),
            (cx + w * 0.2, cy - h * 0.14)], fill=(30, 132, 73), width=4)

def icon_dove(d, x, y, w, h, c):
    icon_shield(d, x, y, w, h, c)

def icon_ai(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.52
    bw, bh = w * 0.5, h * 0.5
    d.line([(cx, y + h * 0.08), (cx, cy - bh / 2)], fill=INK, width=3)
    d.ellipse([cx - 4, y + h * 0.02, cx + 4, y + h * 0.1], fill=RED)
    d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                        radius=8, fill=(255, 255, 255), outline=INK, width=3)
    d.ellipse([cx - bw * 0.28, cy - bh * 0.12, cx - bw * 0.08, cy + bh * 0.08],
              fill=INK)
    d.ellipse([cx + bw * 0.08, cy - bh * 0.12, cx + bw * 0.28, cy + bh * 0.08],
              fill=INK)
    d.line([(cx - bw * 0.2, cy + bh * 0.28), (cx + bw * 0.2, cy + bh * 0.28)],
           fill=INK, width=3)

def icon_island(d, x, y, w, h, c):
    d.polygon([(x + w * 0.2, y + h * 0.75), (x + w * 0.35, y + h * 0.3),
               (x + w * 0.55, y + h * 0.18), (x + w * 0.72, y + h * 0.45),
               (x + w * 0.8, y + h * 0.75)], fill=(39, 174, 96),
              outline=INK)
    d.line([(x + w * 0.12, y + h * 0.3), (x + w * 0.38, y + h * 0.55),
            (x + w * 0.6, y + h * 0.4), (x + w * 0.88, y + h * 0.62)],
           fill=RED, width=4)
    d.polygon([(x + w * 0.88, y + h * 0.62), (x + w * 0.76, y + h * 0.56),
               (x + w * 0.82, y + h * 0.72)], fill=RED)

def icon_flags(d, x, y, w, h, c):
    cols = [(192, 57, 43), (31, 97, 141), (30, 132, 73)]
    for i, col in enumerate(cols):
        px = x + w * (0.22 + i * 0.28)
        d.line([(px, y + h * 0.15), (px, y + h * 0.85)], fill=INK, width=3)
        d.polygon([(px, y + h * 0.15), (px + w * 0.22, y + h * 0.28),
                   (px, y + h * 0.42)], fill=col, outline=INK)

def icon_embassy(d, x, y, w, h, c):
    bx, by, bw, bh = x + w * 0.18, y + h * 0.3, w * 0.5, h * 0.55
    d.polygon([(bx - 6, by), (bx + bw / 2, by - h * 0.18),
               (bx + bw + 6, by)], fill=(180, 35, 24))
    d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255), outline=INK,
                width=2)
    for i in range(3):
        cx = bx + bw * (0.2 + i * 0.3)
        d.rectangle([cx - 3, by + 6, cx + 3, by + bh - 4], fill=INK)
    cx, cy = x + w * 0.8, y + h * 0.28
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(cx, cy), (cx + math.cos(a) * w * 0.14,
                            cy + math.sin(a) * h * 0.16)],
               fill=(230, 126, 34), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(230, 126, 34))

def icon_cyclone(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.52
    for k in range(3):
        r0 = min(w, h) * (0.08 + k * 0.12)
        d.arc([cx - r0, cy - r0 * 0.8, cx + r0, cy + r0 * 0.8],
              200 + k * 40, 200 + k * 40 + 220, fill=(31, 97, 141), width=4)
    d.line([(cx, cy), (cx + w * 0.34, cy)], fill=(31, 97, 141), width=3)

def icon_chip(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.5
    s = min(w, h) * 0.52
    for i in range(3):
        off = -s / 2 + i * s / 2
        d.line([(cx + off, y + h * 0.06), (cx + off, cy - s / 2)], fill=INK,
               width=2)
        d.line([(cx + off, cy + s / 2), (cx + off, y + h * 0.94)], fill=INK,
               width=2)
        d.line([(x + w * 0.06, cy + off), (cx - s / 2, cy + off)], fill=INK,
               width=2)
        d.line([(cx + s / 2, cy + off), (x + w * 0.94, cy + off)], fill=INK,
               width=2)
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([cx - s * 0.22, cy - s * 0.22, cx + s * 0.22, cy + s * 0.22],
                fill=(31, 97, 141))

def icon_badge(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.5
    d.polygon([(cx, y + h * 0.12), (cx + w * 0.3, y + h * 0.22),
               (cx + w * 0.28, y + h * 0.62), (cx, y + h * 0.86),
               (cx - w * 0.28, y + h * 0.62), (cx - w * 0.3, y + h * 0.22)],
              fill=(31, 97, 141), outline=INK)
    d.ellipse([cx - 4, cy - 2, cx + 4, cy + 6], fill=(255, 255, 255))

def icon_bank(d, x, y, w, h, c):
    bx, by, bw, bh = x + w * 0.15, y + h * 0.32, w * 0.7, h * 0.5
    d.polygon([(bx - 4, by), (bx + bw / 2, by - h * 0.16),
               (bx + bw + 4, by)], fill=(125, 60, 152))
    d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255), outline=INK,
                width=2)
    for i in range(4):
        cx = bx + bw * (0.14 + i * 0.24)
        d.rectangle([cx - 3, by + 5, cx + 3, by + bh - 4], fill=INK)
    d.polygon([(x + w * 0.82, y + h * 0.12), (x + w * 0.94, y + h * 0.34),
               (x + w * 0.7, y + h * 0.34)], fill=(230, 126, 34),
              outline=INK)
    d.text((x + w * 0.82, y + h * 0.2), "!", font=sans_b(14), fill=INK,
           anchor="mm")

def icon_pad(d, x, y, w, h, c):
    cx, cy = x + w * 0.5, y + h * 0.5
    d.rounded_rectangle([cx - w * 0.36, cy - h * 0.26, cx + w * 0.36,
                         cy + h * 0.26], radius=12, fill=(255, 255, 255),
                        outline=INK, width=3)
    d.line([(cx - w * 0.22, cy), (cx - w * 0.1, cy)], fill=INK, width=3)
    d.line([(cx - w * 0.16, cy - h * 0.08), (cx - w * 0.16, cy + h * 0.08)],
           fill=INK, width=3)
    for ox, oy in ((0.16, -0.08), (0.24, 0.05), (0.16, 0.12), (0.08, 0.05)):
        d.ellipse([cx + w * ox - 3, cy + h * oy - 3, cx + w * ox + 3,
                   cy + h * oy + 3], fill=RED)

def icon_cricket(d, x, y, w, h, c):
    d.line([(x + w * 0.3, y + h * 0.15), (x + w * 0.55, y + h * 0.75)],
           fill=(139, 90, 43), width=8)
    d.rectangle([x + w * 0.45, y + h * 0.6, x + w * 0.65, y + h * 0.85],
                fill=(139, 90, 43))
    d.ellipse([x + w * 0.68, y + h * 0.2, x + w * 0.88, y + h * 0.4],
              fill=RED, outline=INK, width=2)
    for i in range(3):
        sx = x + w * (0.18 + i * 0.09)
        d.line([(sx, y + h * 0.55), (sx, y + h * 0.88)], fill=(230, 190, 90),
               width=4)

ICONS = {
    "market": icon_market, "baseball": icon_baseball, "dove": icon_dove,
    "ai": icon_ai, "island": icon_island, "flags": icon_flags,
    "embassy": icon_embassy, "cyclone": icon_cyclone, "chip": icon_chip,
    "badge": icon_badge, "bank": icon_bank, "pad": icon_pad,
    "cricket": icon_cricket,
}

# ---------------------------------------------------------------- content
HEROES = [
    ("market", "Asia-Pacific",
     "Asia sinks as AI debut fails to calm fear",
     "Stocks tumble across Asia on Friday. Tokyo's Nikkei falls 4.6% and "
     "Seoul's Kospi 4.7%, heading for their worst week since 2020."),
    ("baseball", "North America",
     "Trump pardons Pete Rose, baseball's hit king",
     "President Donald Trump grants a posthumous pardon to Pete Rose, "
     "the late baseball star and all-time hits leader."),
    ("dove", "Europe",
     "Kushner: Russia open to NATO-like guarantees",
     "US envoy Jared Kushner says Russia is \u201ccomfortable\u201d with "
     "security guarantees for Ukraine \u201cbased on\u201d NATO's Article 5."),
]

GRID = [
    ("ai", "North America", "Anthropic up 17% on debut",
     "The AI firm closes at $97.17, up 17% from its $83 IPO price, "
     "in the largest IPO on record."),
    ("island", "Asia-Pacific", "Taiwan moves to steady stocks",
     "The regulator unveils five measures as short-selling limits "
     "take effect today."),
    ("flags", "Asia-Pacific", "Takaichi dodges Taiwan question",
     "Japan's PM won't say if Tokyo would act over Taiwan, at APEC."),
    ("embassy", "Europe", "Blast near Dutch embassy in Kyiv",
     "A projectile lands near the Dutch embassy in Kyiv, causing "
     "minor damage."),
    ("cyclone", "Asia-Pacific", "Cyclone Akvan hits India's east coast",
     "The severe storm makes landfall on Odisha and Andhra Pradesh; "
     "thousands evacuate."),
    ("chip", "North America", "California probes Nvidia over China chips",
     "The attorney general subpoenas Nvidia over its China chip risk "
     "disclosures as AI stocks slide."),
    ("badge", "Asia-Pacific", "6,310 held in Korea gambling sweep",
     "Police arrest 6,310 people and freeze $116m in the biggest "
     "online gambling crackdown."),
    ("bank", "North America", "Citi hid $35bn of risk, Reuters says",
     "Citigroup misbooked trades in Europe and understated risk by "
     "$35bn, Reuters reports."),
    ("pad", "North America", "GTA VI sales surge on launch day",
     "Rockstar's game takes over the zeitgeist as launch-day sales "
     "surge around the world."),
    ("cricket", "Asia-Pacific", "Nicholls 113* as NZ reach 273/5",
     "Henry Nicholls' unbeaten century anchors New Zealand on day two "
     "of the Wellington Test."),
]

NUMBERS = [
    ("-4.6%", "Nikkei 225, Tokyo"),
    ("-4.7%", "Kospi, Seoul"),
    ("-7%", "Asia stocks this week"),
    ("6,310", "held in Korea sweep"),
    ("$35bn", "Citi risk hidden"),
]

REGIONS = [
    ("Asia-Pacific", 14), ("Europe", 10), ("North America", 10),
    ("Latin America", 2), ("Middle East", 2), ("Africa", 1), ("World", 2),
]

BRIEFS = [
    "ECB warns of AI market risk to Irish pensions.",
    "F5 patches critical NGINX flaws; servers at risk.",
    "Sweden tops the 2026 EF English Proficiency Index.",
    "Senate hearing clashes over Social Security's future.",
    "Amsterdam court backs McDonald's worker dismissal.",
    "Tokyo drops its 2027 casino resort bid.",
    "Modi opens FICCI's centenary convention in Delhi.",
    "Collider taken apart to fit magnets never run before.",
    "Canada reimposes sanctions on 11 Iranian entities.",
    "Bomb threats force emergency landings in Europe.",
    "Trump made 751 personal trades in September.",
    "AOC: up to her if she is Don Lemon's 2028 mate.",
    "Fiji declares a state of disaster over drought.",
    "Korea's top court clears ex-PM Han Duck-soo.",
    "UN: N. Korea expanding Yongbyon enrichment.",
    "US and Venezuela to restore military cooperation.",
    "Korea and China ease cultural content barriers.",
    "Gold falls below $3,700 an ounce.",
    "Red Wednesday conference opens in Budapest.",
    "Ancient proteins found in Estonian child burials.",
    "Delhi launches student mental health policy.",
    "Hungarian EUFOR troops practise helicopter drills.",
    "Vasco 2-1 Inter; Vitoria 2-1 Bragantino.",
    "Zverev reaches ATP Finals semi-finals in Turin.",
    "Sri Lanka 309/9, lead Pakistan by 82 at stumps.",
    "Trump back from China; White House briefing today.",
    "Storm alerts for Suwarrow and Pukapuka islands.",
    "World Children's Day marked around the world.",
]

# ---------------------------------------------------------------- drawing
def draw_map(d, x, y, w, h):
    """Dotted world map from continent ellipses, with red story dots."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 244),
                outline=CARD_LINE)
    blobs = [
        (0.06, 0.12, 0.30, 0.30),   # North America
        (0.16, 0.48, 0.16, 0.34),   # South America
        (0.46, 0.10, 0.16, 0.22),   # Europe
        (0.47, 0.34, 0.18, 0.36),   # Africa
        (0.64, 0.08, 0.32, 0.38),   # Asia
        (0.82, 0.62, 0.14, 0.16),   # Australia
    ]
    step = 7
    for r in range(0, h, step):
        for c in range(0, w, step):
            px, py = x + c, y + r
            fx, fy = c / w, r / h
            inside = False
            for bx, by, bw, bh in blobs:
                ex, ey = bx + bw / 2, by + bh / 2
                if ((fx - ex) / (bw / 2)) ** 2 + ((fy - ey) / (bh / 2)) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([px, py, px + 2, py + 2], fill=(90, 110, 135))
    spots = [(0.18, 0.2), (0.24, 0.55), (0.52, 0.18), (0.55, 0.42),
             (0.7, 0.2), (0.8, 0.28), (0.88, 0.7), (0.35, 0.28),
             (0.62, 0.5), (0.12, 0.32)]
    for fx, fy in spots:
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer double border
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=1)

    y = 24
    # ---- masthead
    text_c(d, (W / 2, y), "THE WORLD TODAY", serif_b(50), INK, anchor="ma")
    y += 58
    d.line([(28, y), (W - 28, y)], fill=INK, width=2)
    y += 8
    text_c(d, (W / 2, y), "FRIDAY, 20 NOVEMBER 2026", sans_b(20), RED,
           anchor="ma")
    y += 24
    text_c(d, (W / 2, y), "ONE DAY  \u2022  ONE PAGE  \u2022  41 STORIES",
           sans(12), INK_SOFT, anchor="ma")
    y += 18
    d.line([(28, y), (W - 28, y)], fill=INK, width=2)
    y += 10

    # ---- region strip
    x = 28
    for name, n in REGIONS:
        col = REGION_COLORS[name]
        label = f"{name} {n}"
        f = sans_b(11)
        tw = d.textlength(label, font=f)
        d.rounded_rectangle([x, y, x + tw + 16, y + 22], radius=11, fill=col)
        d.text((x + 8, y + 4), label, font=f, fill=(255, 255, 255))
        x += tw + 24
    y += 32

    # ---- numbers strip
    d.text((28, y), "THE DAY IN NUMBERS", font=sans_b(13), fill=INK)
    y += 18
    bw = (W - 56 - 4 * 8) / 5
    for i, (num, lab) in enumerate(NUMBERS):
        bx = 28 + i * (bw + 8)
        d.rectangle([bx, y, bx + bw, y + 52], fill=CARD_BG,
                    outline=CARD_LINE, width=1)
        d.text((bx + bw / 2, y + 4), num, font=serif_b(24), fill=RED,
               anchor="ma")
        lines = fit(d, lab, sans(10), bw - 10, 2)
        ly = y + 31
        for ln in lines:
            d.text((bx + bw / 2, ly), ln, font=sans(10), fill=INK_SOFT,
                   anchor="ma")
            ly += 12
    y += 58

    # ---- hero cards (3 across)
    d.text((28, y), "THE DAY'S BIG STORIES", font=sans_b(13), fill=INK)
    y += 18
    hw = (W - 56 - 2 * 10) / 3
    hh = 172
    for i, (icon, region, head, body) in enumerate(HEROES):
        hx = 28 + i * (hw + 10)
        col = REGION_COLORS[region]
        d.rectangle([hx, y, hx + hw, y + hh], fill=CARD_BG,
                    outline=CARD_LINE, width=1)
        d.rectangle([hx, y, hx + hw, y + 72], fill=(238, 234, 220))
        d.rectangle([hx, y + 72, hx + hw, y + 75], fill=col)
        ICONS[icon](d, hx + hw / 2 - 40, y + 2, 80, 68, col)
        ty = y + 82
        d.text((hx + 10, ty), region.upper(), font=sans_b(9), fill=col)
        ty += 13
        for ln in fit(d, head, serif_b(16), hw - 20, 2):
            d.text((hx + 10, ty), ln, font=serif_b(16), fill=INK)
            ty += 19
        ty += 2
        for ln in fit(d, body, sans(11), hw - 20, 3):
            d.text((hx + 10, ty), ln, font=sans(11), fill=INK_SOFT)
            ty += 14
    y += hh + 10

    # ---- 10-card grid (5 x 2)
    d.text((28, y), "AROUND THE WORLD", font=sans_b(13), fill=INK)
    y += 18
    gw = (W - 56 - 4 * 8) / 5
    gh = 118
    for row in range(2):
        for col_i in range(5):
            idx = row * 5 + col_i
            icon, region, head, body = GRID[idx]
            gx = 28 + col_i * (gw + 8)
            gy = y + row * (gh + 6)
            col = REGION_COLORS[region]
            d.rectangle([gx, gy, gx + gw, gy + gh], fill=CARD_BG,
                        outline=CARD_LINE, width=1)
            d.rectangle([gx, gy, gx + gw, gy + 36], fill=(238, 234, 220))
            d.rectangle([gx, gy + 36, gx + gw, gy + 38], fill=col)
            ICONS[icon](d, gx + gw / 2 - 19, gy + 2, 38, 32, col)
            ty = gy + 43
            for ln in fit(d, head, sans_b(11), gw - 12, 2):
                d.text((gx + 6, ty), ln, font=sans_b(11), fill=INK)
                ty += 13
            ty += 1
            for ln in fit(d, body, sans(9), gw - 12, 3):
                d.text((gx + 6, ty), ln, font=sans(9), fill=INK_SOFT)
                ty += 11
    y += 2 * gh + 6 + 10

    # ---- bottom: map + brief list
    map_w = 300
    d.text((28, y), "WHERE IT HAPPENED", font=sans_b(13), fill=INK)
    d.text((28 + map_w + 16, y), "THE REST OF THE DAY", font=sans_b(13),
           fill=INK)
    y += 18
    map_h = 168
    draw_map(d, 28, y, map_w, map_h)
    d.text((28, y + map_h + 4), "Red dots mark where the day's stories happened.",
           font=sans(9), fill=MUTED)
    bx0 = 28 + map_w + 16
    bw2 = W - 28 - bx0
    half = (len(BRIEFS) + 1) // 2
    fnt = sans(9)
    lh = 12
    for j, b in enumerate(BRIEFS):
        col_i = 0 if j < half else 1
        r = j if j < half else j - half
        px = bx0 + col_i * (bw2 / 2 + 6)
        py = y + r * lh
        num = f"{j + 1}."
        d.text((px, py), num, font=sans_b(9), fill=RED)
        nw = d.textlength(num + " ", font=sans_b(9))
        lines = fit(d, b, fnt, bw2 / 2 - 6 - nw - 2, 1)
        d.text((px + nw, py), lines[0] if lines else "", font=fnt,
               fill=INK_SOFT)
    y += map_h + 18

    # ---- date check box
    d.rectangle([28, y, W - 28, y + 38], outline=RED, width=2)
    d.text((W / 2, y + 3), "DATE CHECK  \u2014  FRIDAY 20 NOVEMBER 2026",
           font=sans_b(12), fill=RED, anchor="ma")
    d.text((W / 2, y + 20),
           "Every story here happened or was first reported on 20 November 2026. "
           "Nothing from 19 November is shown as today's news.",
           font=sans(10), fill=INK, anchor="ma")
    y += 44

    # ---- footer
    d.text((28, y), "Original drawings  \u2022  No photographs  \u2022  "
           "Sources: Reuters, CNBC, NEXA, Washington Examiner, LiveScore, "
           "GGRAsia, JBizNews", font=sans(9), fill=MUTED)
    d.text((W - 28, y), "THE WORLD TODAY", font=serif_b(10), fill=MUTED,
           anchor="ra")
    assert y + 12 <= H - 13, f"layout overflow: footer at y={y}"
    print("layout ok, footer y =", y)

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)
    if TRUNCATED:
        print("WARNING truncated texts:", len(TRUNCATED))
        for t in TRUNCATED:
            print("  -", t)
    else:
        print("no text truncated")

if __name__ == "__main__":
    main()
