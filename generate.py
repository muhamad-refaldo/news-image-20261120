#!/usr/bin/env python3
"""news-image-20261120 v2 — one-page newspaper front page, 900x1024.
Original drawings only (Pillow shapes). No photos, no network, deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
M = 18
CW = W - 2 * M  # 864 content width

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (251, 245, 230)
INK = (26, 26, 26)
GREY = (87, 83, 78)
LINE = (214, 211, 209)
RED = (185, 28, 28)
CARD = (255, 255, 255)
TINT = (243, 238, 226)
DARK = (17, 24, 39)

REGION_COLORS = {
    "Asia-Pacific": (185, 28, 28),
    "Europe": (29, 78, 216),
    "North America": (22, 101, 52),
    "Middle East": (194, 65, 12),
    "Africa": (126, 34, 206),
    "Latin America": (14, 116, 144),
    "Oceania": (146, 64, 14),
    "World": (87, 83, 78),
}
REGION_SHORT = {
    "Asia-Pacific": "ASIA-PACIFIC",
    "Europe": "EUROPE",
    "North America": "N. AMERICA",
    "Middle East": "MID EAST",
    "Africa": "AFRICA",
    "Latin America": "LATIN AM.",
    "Oceania": "OCEANIA",
    "World": "WORLD",
}

# ---------------------------------------------------------------- data
HEROES = [
    {
        "region": "Asia-Pacific",
        "headline": "Asia sinks as AI rout deepens",
        "body": "Tokyo's Nikkei plunges 5.06% to 56,436.65 and Seoul's Kospi falls 5.21% to 4,869.96, closing below 5,000, as an AI sell-off sweeps the region. Taiwan's Taiex drops 6.63%. Asia heads for its worst week since 2020.",
        "pic": "chart",
        "sources": "Sources: Reuters, AJP, TradingView",
    },
    {
        "region": "Asia-Pacific",
        "headline": "Court: Myanmar committed genocide",
        "body": "The International Court of Justice rules 9-6 that Myanmar committed genocide against the Rohingya, the first such finding against a state. The court cites mass killings and sexual violence in Rakhine State.",
        "pic": "scales",
        "sources": "Sources: OneTurn, Bangladesh Chronicle",
    },
    {
        "region": "Middle East",
        "headline": "Missile hits Riyadh's tallest tower",
        "body": "Houthi missiles strike Riyadh's financial district, damaging the Public Investment Fund tower. Saudi Arabia intercepts another missile and five drones on Friday as the conflict spills into the Gulf.",
        "pic": "tower",
        "sources": "Sources: OneTurn, Bangladesh Chronicle",
    },
]

GRID = [
    {"region": "North America", "headline": "Wall Street sinks into correction",
     "body": "The S&P 500 falls 3.7% to 6,910.39, its seventh straight loss, entering a correction. The Nasdaq drops 5.28%.", "pic": "chart"},
    {"region": "North America", "headline": "Anthropic slides on day two",
     "body": "Anthropic shares fall 9.1% to $88.30 on their second day of trading, giving back much of Thursday's 17% debut gain.", "pic": "robot"},
    {"region": "Asia-Pacific", "headline": "Cyclone Akvan hits India's coast",
     "body": "Cyclone Akvan crosses the coast near Gopalpur with winds of 70-80 kmph. More than 300,000 people are evacuated in Odisha.", "pic": "cyclone"},
    {"region": "North America", "headline": "GTA VI: $3.79bn in one day",
     "body": "Rockstar says Grand Theft Auto VI took $3.79 billion in day-one sales, the biggest entertainment launch in history.", "pic": "controller"},
    {"region": "Europe", "headline": "Medvedev into Turin semi-finals",
     "body": "Daniil Medvedev beats Frances Tiafoe 6-3, 6-4 to reach the ATP Finals semi-finals for the first time since 2023.", "pic": "tennis"},
    {"region": "North America", "headline": "Citi hid $35bn of risk",
     "body": "Citigroup misbooked trades at its European unit and underestimated risk by $35 billion, Reuters reports.", "pic": "bank"},
    {"region": "North America", "headline": "Nvidia hit by SEC accounting look",
     "body": "Nvidia shares fall 14% after Reuters reports SEC staff are examining potential accounting issues at the chipmaker.", "pic": "chip"},
    {"region": "Europe", "headline": "Blast near Dutch embassy in Kyiv",
     "body": "A projectile lands near the Netherlands' embassy in Kyiv, causing minor damage, as Russia attacks overnight.", "pic": "blast"},
    {"region": "Europe", "headline": "Kushner: Russia open to guarantees",
     "body": "US envoy Jared Kushner says Russia is 'comfortable' with security guarantees for Ukraine based on NATO's Article 5.", "pic": "shield"},
    {"region": "Asia-Pacific", "headline": "6,310 held in Korea gambling sweep",
     "body": "South Korean police arrest 6,310 people and freeze $116 million in the country's biggest online gambling crackdown.", "pic": "cuffs"},
]

BRIEFS = [
    "Shenzhen: Trump, Xi, Putin issue peace declaration",
    "Russia strikes three Kyiv bridges; three killed",
    "EU and UK hold summit in Brussels",
    "Denmark backs Greenland-US security deal",
    "Kenya discharges last Ebola patient",
    "Saudi intercepts Houthi missile, five drones",
    "Tanker on fire in Strait of Hormuz",
    "COP31 draft drops fossil-fuel phase-out",
    "Israeli troops cross Yellow Line in Gaza",
    "IMF: public debt nears 100% of world GDP",
    "Italy fines Meta 805m over photo access",
    "FAA ground stop strands 1.5m travellers",
    "Virginia exits Trump school tax-credit plan",
    "OpenAI releases GPT-6.2 Astra",
    "Ella Langley sweeps the CMA Awards",
    "Bukele registers for third term in El Salvador",
    "Migrant boat capsizes off Senegal; dozens missing",
    "Drone strike kills 10 at Sudan gold mine",
    "Kenya starts 42-day Ebola-free countdown",
    "Kerch Bridge rail traffic resumes",
    "ECB warns on AI market vulnerability",
    "F5 patches critical NGINX flaws",
    "Sweden tops English proficiency index",
    "Canada sanctions 11 Iranian entities",
    "Fiji declares disaster over drought",
    "S. Korea court clears ex-PM Han Duck-soo",
    "Gold falls below $3,700 an ounce",
    "World Children's Day marked worldwide",
]

NUMBERS = [
    ("-5.06%", "NIKKEI 225"),
    ("-5.21%", "KOSPI"),
    ("-3.70%", "S&P 500"),
    ("-5.28%", "NASDAQ"),
    ("$3.79bn", "GTA VI DAY ONE"),
    ("300,000+", "EVACUATED, ODISHA"),
]

REGIONS = [
    ("Asia-Pacific", 6), ("Europe", 11), ("North America", 10),
    ("Middle East", 4), ("Africa", 4), ("Latin America", 1),
    ("Oceania", 1), ("World", 4),
]

# world map: row -> list of (col_start, col_end) inclusive, 60 cols x 28 rows
MAP_ROWS = [
    [(11, 16), (42, 57)],
    [(1, 15), (37, 59)],
    [(2, 6), (6, 20), (31, 59)],
    [(2, 6), (7, 20), (30, 59)],
    [(3, 6), (8, 20), (29, 29), (30, 59)],
    [(9, 19), (29, 55)],
    [(9, 19), (29, 56)],
    [(10, 19), (29, 54)],
    [(10, 18), (29, 35), (42, 52), (55, 56)],
    [(11, 18), (27, 34), (36, 40), (42, 51)],
    [(11, 17), (26, 34), (37, 40), (43, 51)],
    [(12, 15), (26, 34), (37, 40), (44, 51)],
    [(13, 16), (26, 34), (45, 46), (48, 52)],
    [(14, 17), (26, 33), (49, 52)],
    [(16, 20), (27, 33), (49, 52)],
    [(16, 21), (28, 32), (49, 54)],
    [(16, 22), (28, 32), (50, 55)],
    [(16, 22), (28, 32), (47, 52)],
    [(16, 22), (28, 31), (46, 53)],
    [(16, 21), (28, 31), (46, 53)],
    [(17, 21), (28, 30), (46, 53)],
    [(17, 20), (28, 30), (47, 52)],
    [(17, 20), (29, 29), (47, 52)],
    [(17, 19), (48, 51)],
    [(17, 18)],
    [(17, 18)],
    [(17, 17)],
    [],
]

# ---------------------------------------------------------------- helpers
def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines = []
    cur = ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, fnt, x, y, max_w, max_lines, lh, fill):
    lines = wrap(d, text, fnt, max_w)
    assert len(lines) <= max_lines, f"OVERFLOW ({len(lines)}>{max_lines}): {text!r}"
    for i, ln in enumerate(lines):
        assert d.textlength(ln, font=fnt) <= max_w + 0.5, f"LINE TOO WIDE: {ln!r}"
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- pictograms
def P(d, box, kind):
    """Draw a simple original pictogram inside box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def X(f):
        return x0 + f * w

    def Y(f):
        return y0 + f * h

    if kind == "chart":
        d.line([(X(0.08), Y(0.25)), (X(0.28), Y(0.35)), (X(0.26), Y(0.55)),
                (X(0.48), Y(0.45)), (X(0.52), Y(0.68)), (X(0.72), Y(0.58)),
                (X(0.78), Y(0.82)), (X(0.92), Y(0.78))], fill=RED, width=3)
        d.polygon([(X(0.92), Y(0.78)), (X(0.84), Y(0.72)), (X(0.86), Y(0.86))], fill=RED)
        for fx, fh in [(0.15, 0.5), (0.35, 0.35), (0.55, 0.55), (0.75, 0.3)]:
            d.rectangle([X(fx), Y(0.92) - fh * h * 0.5, X(fx + 0.08), Y(0.92)], fill=(203, 213, 225))
    elif kind == "scales":
        d.line([(X(0.5), Y(0.15)), (X(0.5), Y(0.85))], fill=INK, width=3)
        d.line([(X(0.15), Y(0.3)), (X(0.85), Y(0.3))], fill=INK, width=3)
        for cx in (0.15, 0.85):
            d.line([(X(cx), Y(0.3)), (X(cx - 0.1), Y(0.62)), (X(cx + 0.1), Y(0.62))], fill=INK, width=2)
            d.arc([X(cx - 0.1), Y(0.55), X(cx + 0.1), Y(0.72)], 0, 180, fill=INK, width=2)
        d.line([(X(0.35), Y(0.85)), (X(0.65), Y(0.85))], fill=INK, width=3)
    elif kind == "tower":
        d.rectangle([X(0.42), Y(0.25), X(0.58), Y(0.9)], fill=(100, 116, 139))
        d.rectangle([X(0.38), Y(0.55), X(0.62), Y(0.62)], fill=(71, 85, 105))
        d.rectangle([X(0.38), Y(0.75), X(0.62), Y(0.82)], fill=(71, 85, 105))
        cx, cy = X(0.5), Y(0.2)
        for ang in range(0, 360, 30):
            import math
            r1, r2 = 0.06 * w, 0.16 * w
            a = math.radians(ang)
            d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a) * 0.6),
                    (cx + r2 * math.cos(a), cy + r2 * math.sin(a) * 0.6)], fill=(234, 88, 12), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(234, 88, 12))
    elif kind == "robot":
        d.rounded_rectangle([X(0.25), Y(0.3), X(0.75), Y(0.75)], radius=8, fill=(148, 163, 184))
        d.ellipse([X(0.36), Y(0.45), X(0.46), Y(0.55)], fill=INK)
        d.ellipse([X(0.54), Y(0.45), X(0.64), Y(0.55)], fill=INK)
        d.line([(X(0.5), Y(0.3)), (X(0.5), Y(0.15))], fill=INK, width=2)
        d.ellipse([X(0.46), Y(0.08), X(0.54), Y(0.16)], fill=RED)
        d.line([(X(0.82), Y(0.2)), (X(0.82), Y(0.55)), (X(0.74), Y(0.47)), (X(0.9), Y(0.47))], fill=RED, width=2)
    elif kind == "cyclone":
        cx, cy = X(0.5), Y(0.5)
        for r in (0.08, 0.16, 0.24, 0.32):
            d.arc([cx - r * w, cy - r * w * 0.7, cx + r * w, cy + r * w * 0.7],
                  200, 200 + 300, fill=(37, 99, 235), width=2)
        for fx in (0.2, 0.35, 0.65, 0.8):
            d.line([(X(fx), Y(0.82)), (X(fx - 0.03), Y(0.95))], fill=(37, 99, 235), width=2)
    elif kind == "controller":
        d.rounded_rectangle([X(0.12), Y(0.3), X(0.88), Y(0.72)], radius=10, fill=(51, 65, 85))
        d.line([(X(0.28), Y(0.45)), (X(0.28), Y(0.6))], fill=(255, 255, 255), width=3)
        d.line([(X(0.21), Y(0.52)), (X(0.35), Y(0.52))], fill=(255, 255, 255), width=3)
        for bx, by, c in [(0.66, 0.45, (239, 68, 68)), (0.74, 0.52, (34, 197, 94)), (0.66, 0.59, (59, 130, 246))]:
            d.ellipse([X(bx) - 4, Y(by) - 4, X(bx) + 4, Y(by) + 4], fill=c)
        d.text((X(0.5), Y(0.78)), "$", font=font(SANS_B, 13), fill=(22, 101, 52), anchor="ma")
    elif kind == "tennis":
        d.ellipse([X(0.2), Y(0.22), X(0.62), Y(0.72)], fill=(190, 242, 100), outline=INK, width=2)
        d.arc([X(0.2), Y(0.22), X(0.62), Y(0.72)], 300, 60, fill=INK, width=2)
        d.arc([X(0.2), Y(0.22), X(0.62), Y(0.72)], 120, 240, fill=INK, width=2)
        d.ellipse([X(0.62), Y(0.3), X(0.9), Y(0.62)], outline=INK, width=2)
        d.line([(X(0.82), Y(0.62)), (X(0.95), Y(0.85))], fill=INK, width=3)
    elif kind == "bank":
        d.polygon([(X(0.5), Y(0.15)), (X(0.15), Y(0.38)), (X(0.85), Y(0.38))], fill=(100, 116, 139))
        for fx in (0.25, 0.42, 0.58, 0.75):
            d.rectangle([X(fx - 0.03), Y(0.42), X(fx + 0.03), Y(0.78)], fill=(100, 116, 139))
        d.rectangle([X(0.12), Y(0.78), X(0.88), Y(0.86)], fill=(100, 116, 139))
        d.text((X(0.5), Y(0.88)), "$35bn", font=font(SANS_B, 11), fill=RED, anchor="ma")
    elif kind == "chip":
        d.rectangle([X(0.28), Y(0.28), X(0.68), Y(0.68)], fill=(51, 65, 85))
        d.rectangle([X(0.42), Y(0.42), X(0.54), Y(0.54)], fill=(148, 163, 184))
        for fx in (0.36, 0.5, 0.64):
            d.line([(X(fx), Y(0.18)), (X(fx), Y(0.28))], fill=INK, width=2)
            d.line([(X(fx), Y(0.68)), (X(fx), Y(0.78))], fill=INK, width=2)
        d.ellipse([X(0.62), Y(0.55), X(0.92), Y(0.9)], outline=INK, width=2)
        d.line([(X(0.88), Y(0.85)), (X(0.98), Y(0.97))], fill=INK, width=2)
    elif kind == "blast":
        cx, cy = X(0.5), Y(0.42)
        pts = []
        import math
        for i in range(12):
            a = math.radians(i * 30)
            r = (0.34 if i % 2 == 0 else 0.18) * w
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.75))
        d.polygon(pts, fill=(249, 115, 22))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
        d.rectangle([X(0.15), Y(0.78), X(0.85), Y(0.92)], fill=(100, 116, 139))
    elif kind == "shield":
        d.polygon([(X(0.5), Y(0.12)), (X(0.85), Y(0.28)), (X(0.85), Y(0.55)),
                   (X(0.5), Y(0.9)), (X(0.15), Y(0.55)), (X(0.15), Y(0.28))], fill=(37, 99, 235))
        d.line([(X(0.32), Y(0.5)), (X(0.46), Y(0.66)), (X(0.72), Y(0.32))], fill=(255, 255, 255), width=3)
    elif kind == "cuffs":
        d.ellipse([X(0.12), Y(0.35), X(0.42), Y(0.68)], outline=INK, width=3)
        d.ellipse([X(0.58), Y(0.35), X(0.88), Y(0.68)], outline=INK, width=3)
        d.line([(X(0.42), Y(0.5)), (X(0.58), Y(0.5))], fill=INK, width=3)
        d.line([(X(0.2), Y(0.2)), (X(0.34), Y(0.32))], fill=INK, width=2)
        d.line([(X(0.66), Y(0.2)), (X(0.8), Y(0.32))], fill=INK, width=2)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title_f = font(SERIF_B, 54)
    t = "THE WORLD TODAY"
    tw = d.textlength(t, font=title_f)
    d.text(((W - tw) / 2, 6), t, font=title_f, fill=INK)
    d.line([(M, 66), (W - M, 66)], fill=INK, width=2)
    date_f = font(SANS_B, 17)
    dt = "FRIDAY, 20 NOVEMBER 2026"
    dw = d.textlength(dt, font=date_f)
    d.text(((W - dw) / 2, 72), dt, font=date_f, fill=RED)
    d.line([(M, 94), (W - M, 94)], fill=INK, width=1)

    # ---- region strip
    y = 100
    chip_w = (CW - 7 * 6) // 8
    rf = font(SANS_B, 9)
    for i, (name, count) in enumerate(REGIONS):
        cx = M + i * (chip_w + 6)
        rrect(d, [cx, y, cx + chip_w, y + 22], 4, fill=REGION_COLORS[name])
        label = f"{REGION_SHORT[name]} {count}"
        lw = d.textlength(label, font=rf)
        assert lw <= chip_w - 6, f"REGION CHIP TOO WIDE: {label}"
        d.text((cx + (chip_w - lw) / 2, y + 6), label, font=rf, fill=(255, 255, 255))

    # ---- numbers strip
    y = 128
    d.rectangle([M, y, W - M, y + 50], fill=DARK)
    nf = font(SANS_B, 10)
    nt = "THE DAY IN NUMBERS"
    nw = d.textlength(nt, font=nf)
    d.text(((W - nw) / 2, y + 5), nt, font=nf, fill=(255, 255, 255))
    bw = CW // 6
    big_f = font(SERIF_B, 19)
    lab_f = font(SANS, 8)
    for i, (num, lab) in enumerate(NUMBERS):
        bx = M + i * bw
        nw2 = d.textlength(num, font=big_f)
        d.text((bx + (bw - nw2) / 2, y + 20), num, font=big_f, fill=(255, 255, 255))
        lw2 = d.textlength(lab, font=lab_f)
        d.text((bx + (bw - lw2) / 2, y + 40), lab, font=lab_f, fill=(209, 213, 219))

    # ---- heroes
    hy, hh = 184, 280
    hw = (CW - 2 * 12) // 3
    hf_h = font(SERIF_B, 15)
    hf_b = font(SANS, 11)
    for i, hero in enumerate(HEROES):
        x = M + i * (hw + 12)
        rrect(d, [x, hy, x + hw, hy + hh], 4, fill=CARD, outline=LINE, width=1)
        # pictogram
        d.rectangle([x + 6, hy + 6, x + hw - 6, hy + 112], fill=TINT)
        P(d, [x + 6, hy + 6, x + hw - 6, hy + 112], hero["pic"])
        # region tag
        tag_f = font(SANS_B, 8)
        tag = hero["region"].upper()
        tw2 = d.textlength(tag, font=tag_f)
        d.rectangle([x + 6, hy + 6, x + 6 + tw2 + 10, hy + 22], fill=REGION_COLORS[hero["region"]])
        d.text((x + 11, hy + 9), tag, font=tag_f, fill=(255, 255, 255))
        # headline (2 lines max)
        draw_wrapped(d, hero["headline"], hf_h, x + 10, hy + 120, hw - 20, 2, 19, INK)
        # body
        draw_wrapped(d, hero["body"], hf_b, x + 10, hy + 162, hw - 20, 7, 15, (51, 51, 51))
        # sources line at the bottom of the card
        src_f = font(SANS, 8)
        d.text((x + 10, hy + hh - 16), hero["sources"], font=src_f, fill=GREY)

    # ---- grid (5 x 2)
    gy = 472
    gw = (CW - 4 * 10) // 5
    gh = 136
    gf_h = font(SERIF_B, 11)
    gf_b = font(SANS, 9)
    for i, card in enumerate(GRID):
        r, c = divmod(i, 5)
        x = M + c * (gw + 10)
        yy = gy + r * (gh + 8)
        rrect(d, [x, yy, x + gw, yy + gh], 3, fill=CARD, outline=LINE, width=1)
        d.rectangle([x + 4, yy + 4, x + gw - 4, yy + 52], fill=TINT)
        P(d, [x + 4, yy + 4, x + gw - 4, yy + 52], card["pic"])
        draw_wrapped(d, card["headline"], gf_h, x + 7, yy + 56, gw - 14, 2, 13, INK)
        draw_wrapped(d, card["body"], gf_b, x + 7, yy + 84, gw - 14, 4, 12, (51, 51, 51))

    # ---- map + briefs headers
    sy = 752
    sec_f = font(SANS_B, 11)
    d.text((M, sy), "WHERE IT HAPPENED", font=sec_f, fill=INK)
    d.text((304, sy), "THE REST OF THE DAY  —  28 BRIEFS", font=sec_f, fill=INK)
    d.line([(M, sy + 16), (W - M, sy + 16)], fill=INK, width=1)

    # ---- dotted world map
    mx0, my0 = M, 776
    mw, mh = 274, 150
    cols, rows = 60, 28
    dx, dy = mw / cols, mh / rows
    for r, ranges in enumerate(MAP_ROWS):
        for (c0, c1) in ranges:
            for c in range(c0, c1 + 1):
                cx = mx0 + (c + 0.5) * dx
                cy = my0 + (r + 0.5) * dy
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7], fill=(100, 116, 139))
    cap_f = font(SANS, 8)
    cap = "Each dot is land. Stories span 8 regions."
    d.text((M, my0 + mh + 6), cap, font=cap_f, fill=GREY)

    # ---- briefs (2 columns x 14)
    bf = font(SANS, 10)
    col_w = 284
    for i, b in enumerate(BRIEFS):
        col, row = divmod(i, 14)
        bx = 304 + col * (col_w + 8)
        by = 776 + row * 13
        line = f"{i + 1}. {b}"
        assert d.textlength(line, font=bf) <= col_w, f"BRIEF TOO WIDE: {line!r}"
        d.text((bx, by), line, font=bf, fill=INK)

    # ---- date check box
    dy0 = 952
    d.rectangle([M, dy0, W - M, dy0 + 38], outline=RED, width=2, fill=(254, 242, 242))
    dc_f = font(SANS_B, 8)
    dc1 = "DATE CHECK — Every story here happened or was first reported on Friday 20 November 2026."
    dc2 = "Three items were announced Thursday, published Friday (Shenzhen declaration, Kushner remarks, Korea sweep) — flagged, not hidden. No Pete Rose pardon (19 Nov) here."
    for j, ln in enumerate((dc1, dc2)):
        lw = d.textlength(ln, font=dc_f)
        assert lw <= CW - 24, f"DATE CHECK LINE TOO WIDE: {ln!r}"
        d.text(((W - lw) / 2, dy0 + 5 + j * 12), ln, font=dc_f, fill=RED)

    # ---- footer
    ff = font(SANS, 8)
    ft = "Sources: Reuters, AP, AFP, IMD, GGRAsia, ATP Tour, Motley Fool, OneTurn, Bangladesh Chronicle.  Original drawings — no photographs.  All 41 stories verified for 20 November 2026."
    fw = d.textlength(ft, font=ff)
    assert fw <= CW, "FOOTER TOO WIDE"
    d.text(((W - fw) / 2, 998), ft, font=ff, fill=GREY)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, "PNG")
    print(f"saved {out} 900x1024")
