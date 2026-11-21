#!/usr/bin/env python3
"""v3 entry image generator — news-image-20261120 (20 Nov 2026).
Draws a one-page newspaper front page, 900x1024 PNG, with PIL only.
Everything is drawn fresh in this session; no external assets.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
OUT = "entry.png"

D = "/usr/share/fonts/truetype/dejavu/"
SERIF = D + "DejaVuSerif.ttf"
SERIF_B = D + "DejaVuSerif-Bold.ttf"
SANS = D + "DejaVuSans.ttf"
SANS_B = D + "DejaVuSans-Bold.ttf"

PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (22, 35, 59)
RED = (185, 28, 28)
CARD_LINE = (216, 210, 196)
MUTED = (90, 86, 76)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
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


def vgrad(d, box, c1, c2):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line([(x0, y), (x1, y)], fill=c)


def arrow(d, pts, fill, width=4):
    d.line(pts, fill=fill, width=width, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    L = 12
    d.polygon([(x2, y2),
               (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45)),
               (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))],
              fill=fill)


# ---------------------------------------------------------------- illustrations
def ill_asia(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (13, 27, 62), (96, 22, 34))
    # stars
    for sx, sy in [(20, 12), (60, 22), (120, 10), (180, 18), (240, 12), (270, 26)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    # Tokyo skyline
    base = y + h
    for bx, bw, bh in [(0, 26, 34), (30, 20, 52), (54, 30, 40), (88, 18, 60),
                       (110, 34, 46), (148, 22, 66), (174, 28, 38), (206, 20, 56),
                       (230, 30, 42), (264, 26, 50)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 10, 26))
    # tower with antenna
    d.rectangle([x + 138, base - 88, x + 146, base], fill=(8, 10, 26))
    d.line([(x + 142, base - 88), (x + 142, base - 104)], fill=(8, 10, 26), width=2)
    d.ellipse([x + 139, base - 108, x + 145, base - 102], fill=(255, 80, 80))
    # falling chart
    arrow(d, [(x + 12, y + 18), (x + 70, y + 30), (x + 130, y + 26),
              (x + 190, y + 52), (x + 250, y + 66), (x + 282, y + 88)],
          (255, 70, 70), 5)
    d.text((x + 10, y + 6), "NIKKEI  −5.06%", font=F(SANS_B, 13), fill=(255, 255, 255))


def ill_wallst(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (28, 28, 34), (70, 18, 18))
    base = y + h
    # exchange columns
    for cx in range(0, w, 34):
        d.rectangle([x + cx + 4, base - 26, x + cx + 26, base], fill=(120, 118, 112))
        d.rectangle([x + cx + 4, base - 30, x + cx + 26, base - 26], fill=(150, 148, 140))
    # falling red candles
    tops = [14, 22, 18, 34, 44, 58, 52, 74]
    bw = 26
    for i, t in enumerate(tops):
        cx = x + 10 + i * 34
        d.rectangle([cx, y + t, cx + bw, y + t + 26], fill=(220, 50, 50))
        d.line([(cx + bw // 2, y + t - 8), (cx + bw // 2, y + t + 34)],
               fill=(220, 50, 50), width=2)
    d.text((x + 10, y + 6), "S&P 500  −3.70%", font=F(SANS_B, 13), fill=(255, 255, 255))


def ill_gta(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (88, 24, 94), (255, 140, 60))
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=(255, 214, 130))
    base = y + h
    for bx, bw, bh in [(0, 30, 40), (34, 22, 62), (60, 34, 48), (98, 20, 70),
                       (122, 30, 44), (156, 24, 58), (184, 32, 40), (220, 26, 64),
                       (250, 40, 46)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(30, 8, 40))
    # palm trees
    for px in (46, 232):
        d.line([(x + px, base), (x + px + 6, base - 34)], fill=(30, 8, 40), width=3)
        for dx, dy in [(-16, -30), (-10, -40), (0, -44), (12, -40), (18, -30)]:
            d.line([(x + px + 6, base - 34), (x + px + 6 + dx, base - 34 + dy)],
                   fill=(30, 8, 40), width=2)
    # badge band
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 8, 30))
    d.text((x + 10, y + h - 22), "$3.79BN — BIGGEST LAUNCH EVER",
           font=F(SANS_B, 13), fill=(255, 214, 130))


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 120, 120))
    cx, cy = x + w // 2, y + h // 2
    for r in (6, 12, 18):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 90))


def ill_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 42, 54))
    arrow(d, [(x + 14, y + 10), (x + 60, y + 16), (x + 110, y + 14),
              (x + 150, y + 34)], (255, 90, 90), 4)
    d.ellipse([x + 146, y + 30, x + 154, y + 38], fill=(255, 90, 90))


def ill_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 90, 44))
    cx, cy = x + w // 2 - 14, y + h // 2
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(120, 200, 90))
    for i in (-1, 0, 1):
        d.line([(cx - 18, cy + i * 8), (cx - 12, cy + i * 8)], fill=(120, 200, 90), width=2)
        d.line([(cx + 12, cy + i * 8), (cx + 18, cy + i * 8)], fill=(120, 200, 90), width=2)
    d.ellipse([x + w - 52, y + 4, x + w - 18, y + 38], outline=(255, 255, 255), width=3)
    d.line([(x + w - 50, y + 34), (x + w - 62, y + 44)], fill=(255, 255, 255), width=3)


def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 140, 70))
    d.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], outline=(255, 255, 255), width=2)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)], fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 46, y + 8, x + w - 20, y + 34], fill=(220, 235, 60))
    d.arc([x + w - 46, y + 8, x + w - 20, y + 34], 300, 60, fill=(255, 255, 255), width=2)


def ill_shield_x(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 97, 141))
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx - 14, cy - 14), (cx + 14, cy - 14), (cx + 14, cy + 2),
               (cx, cy + 16), (cx - 14, cy + 2)], fill=(255, 255, 255))
    d.line([(cx - 7, cy - 7), (cx + 7, cy + 7)], fill=RED, width=3)
    d.line([(cx + 7, cy - 7), (cx - 7, cy + 7)], fill=RED, width=3)


def ill_bridges(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 180, 220))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 110, 180))
    d.line([(x + 10, y + h - 14), (x + w - 10, y + h - 14)], fill=(40, 40, 40), width=3)
    for ax in (30, 86, 142):
        d.arc([x + ax - 22, y + h - 36, x + ax + 22, y + h - 6], 180, 360,
              fill=(40, 40, 40), width=3)
    cx, cy = x + w // 2, y + 14
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 4, 12
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(255, 140, 0), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 140, 0))


def ill_saudi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 60))
    cx, cy = x + w // 2 - 16, y + h // 2
    d.polygon([(cx - 14, cy - 14), (cx + 14, cy - 14), (cx + 14, cy + 2),
               (cx, cy + 16), (cx - 14, cy + 2)], outline=(255, 255, 255), width=2)
    arrow(d, [(x + w - 52, y + h - 8), (x + w - 34, y + 16), (x + w - 22, y + 8)],
          (255, 90, 90), 3)


def ill_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 110, 40))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(140, 60, 20))
    d.rectangle([x + 30, y + 18, x + w - 30, y + 34], fill=(25, 25, 25))
    d.polygon([(x + w - 30, y + 18), (x + w - 14, y + 26), (x + w - 30, y + 34)],
              fill=(25, 25, 25))
    d.rectangle([x + 52, y + 8, x + 62, y + 18], fill=(25, 25, 25))
    d.polygon([(x + 84, y + 2), (x + 90, y + 12), (x + 96, y + 2), (x + 92, y + 14),
               (x + 98, y + 8), (x + 90, y + 20), (x + 82, y + 8), (x + 88, y + 14)],
              fill=(255, 220, 60))


def ill_euuk(d, x, y, w, h):
    d.rectangle([x, y, x + w // 2, y + h], fill=(0, 51, 153))
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(1, 33, 105))
    import math
    cx, cy = x + w // 4, y + h // 2
    for k in range(12):
        a = math.radians(k * 30)
        d.ellipse([cx + 13 * math.cos(a) - 2, cy + 13 * math.sin(a) - 2,
                   cx + 13 * math.cos(a) + 2, cy + 13 * math.sin(a) + 2],
                  fill=(255, 204, 0))
    ux = x + 3 * w // 4
    d.line([(ux, y + 4), (ux, y + h - 4)], fill=(255, 255, 255), width=7)
    d.line([(x + w // 2 + 4, cy), (x + w - 4, cy)], fill=(255, 255, 255), width=7)
    d.line([(ux, y + 4), (ux, y + h - 4)], fill=(200, 16, 46), width=3)
    d.line([(x + w // 2 + 4, cy), (x + w - 4, cy)], fill=(200, 16, 46), width=3)


def ill_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 210))
    cx, cy = x + w // 2 - 18, y + h // 2
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(40, 120, 200))
    d.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(60, 180, 90))
    d.ellipse([cx + 2, cy + 2, cx + 12, cy + 12], fill=(60, 180, 90))
    d.rectangle([x + w - 34, y + 8, x + w - 28, y + h - 12], fill=(255, 255, 255))
    d.rectangle([x + w - 34, y + 8, x + w - 28, y + 18], fill=RED)
    d.ellipse([x + w - 38, y + h - 16, x + w - 24, y + h - 2], fill=RED)


# ---------------------------------------------------------------- world map
# (latitude, [(lon_start, lon_end), ...]) — coarse land mask, equirectangular
LAND = [
    (75, [(-168, -140), (-58, -20), (40, 110), (150, 180)]),
    (70, [(-165, -140), (-140, -90), (-55, -20), (35, 180)]),
    (65, [(-168, -125), (-135, -60), (-55, -25), (5, 30), (30, 180)]),
    (60, [(-165, -130), (-135, -55), (-45, -40), (5, 30), (28, 180)]),
    (55, [(-130, -55), (-6, 180)]),
    (50, [(-125, -55), (-5, 142), (156, 162)]),
    (45, [(-125, -65), (-2, 30), (45, 90), (128, 142)]),
    (40, [(-125, -70), (-10, 30), (45, 75), (115, 127), (139, 142)]),
    (35, [(-120, -75), (-10, 36), (36, 62), (105, 122), (129, 141)]),
    (30, [(-120, -80), (-10, 35), (35, 60), (68, 122)]),
    (25, [(-115, -80), (-17, 35), (35, 58), (66, 90), (100, 122)]),
    (20, [(-105, -87), (-17, 35), (38, 58), (72, 88), (95, 110)]),
    (15, [(-95, -83), (-17, 42), (42, 55), (73, 80), (94, 105)]),
    (10, [(-85, -78), (-78, -60), (-15, 42), (75, 78), (98, 105)]),
    (5, [(-78, -50), (-10, 42), (95, 105), (112, 120)]),
    (0, [(-80, -35), (8, 42), (95, 141)]),
    (-5, [(-80, -35), (10, 40), (100, 141)]),
    (-10, [(-75, -35), (12, 40), (105, 141), (113, 130)]),
    (-15, [(-70, -38), (12, 40), (43, 50), (114, 145)]),
    (-20, [(-70, -40), (12, 35), (44, 50), (114, 150)]),
    (-25, [(-70, -48), (15, 35), (113, 153)]),
    (-30, [(-70, -55), (17, 32), (115, 150)]),
    (-35, [(-72, -58), (18, 28), (115, 140), (167, 178)]),
    (-40, [(-73, -62), (168, 175)]),
    (-45, [(-73, -65)]),
    (-50, [(-73, -66)]),
    (-55, [(-70, -66)]),
]
# story locations (lon, lat)
MARKERS = [(139.7, 35.7), (127.0, 37.5), (-74.0, 40.7), (-122.4, 37.8),
           (7.7, 45.1), (4.35, 50.85), (30.5, 50.45), (46.7, 24.6),
           (56.5, 26.5), (84.9, 19.3), (30.7, 36.9)]

# ---------------------------------------------------------------- content
HEROES = [
    ("ASIA  •  MARKETS", "ASIA'S BLACK FRIDAY",
     "Tokyo's Nikkei sinks 5.06% to 56,436.65 and Seoul's Kospi 5.21% to "
     "4,869.96, with Taiwan's Taiex down 6.63% — the region's worst week "
     "since 2020. SoftBank crashes 14.48% and chipmaker Advantest 10.32%.",
     ill_asia),
    ("AMERICAS  •  MARKETS", "WALL STREET JOINS THE ROUT",
     "The S&P 500 falls 3.70% to 6,910.39, its seventh straight loss — the "
     "longest since February 2020. The Dow drops 1.93% and the Nasdaq 5.28% "
     "to 22,617.73, turning negative for 2026. Nvidia plunges 14%.",
     ill_wallst),
    ("TECH  •  CULTURE", "GTA VI: $3.79BN IN A DAY",
     "Grand Theft Auto VI becomes the biggest entertainment launch in "
     "history, selling $3.79 billion through the end of Thursday — 32.5 "
     "million copies before release day. No film, album or game ever opened "
     "bigger.", ill_gta),
]

GRID = [
    ("ASIA  •  WEATHER", "CYCLONE AKVAN SLAMS ODISHA",
     "Cyclone Akvan hits Odisha near Gopalpur, winds to 90 km/h. Over "
     "300,000 people flee to 9,341 shelters as 423 rescue teams deploy. No "
     "deaths at first.", ill_cyclone),
    ("TECH", "ANTHROPIC SLIDES ON DAY TWO",
     "Shares close at $88.91, down 8.5% on day two after the record IPO, "
     "which closes Friday: 1.127 billion shares sold at $83, raising "
     "$93.5 billion.", ill_anthropic),
    ("TECH  •  MARKETS", "SEC PROBES NVIDIA",
     "US regulators are examining Nvidia's accounting, Reuters reports. "
     "Shares fall 14% to $125.53 — down 23% on the week, wiping about "
     "$491 billion.", ill_nvidia),
    ("SPORT", "MEDVEDEV INTO TURIN SEMIS",
     "Daniil Medvedev beats Frances Tiafoe 6–3, 6–4 on Friday night to "
     "reach the ATP Finals semi-finals in Turin. He faces Alexander Zverev "
     "on Saturday.", ill_tennis),
    ("EUROPE", "MOSCOW REJECTS GUARANTEES",
     "Russia rejects NATO-style security guarantees for Ukraine, a senior "
     "diplomat says, dismissing a claim by US envoy Jared Kushner a day "
     "earlier.", ill_shield_x),
    ("EUROPE  •  WAR", "KYIV'S BRIDGES HIT",
     "Russia's overnight barrage kills three in Kyiv and hits three bridges "
     "over the Dnipro — the biggest attack on the city's crossings since "
     "the war began.", ill_bridges),
    ("MIDDLE EAST", "SAUDI DEFENCES HOLD",
     "Saudi air defences intercept a missile and five drones on Friday, the "
     "military says, as Houthi attacks on the kingdom continue into a "
     "second day.", ill_saudi),
    ("MIDDLE EAST  •  ENERGY", "TANKER BURNS IN HORMUZ",
     "An oil tanker catches fire in the Strait of Hormuz, pushing Brent "
     "crude up 2.3% to $64.01. The IEA calls it the largest energy supply "
     "shock on record.", ill_tanker),
    ("EUROPE", "EU AND UK STRIKE NEW DEALS",
     "Britain's PM Andy Burnham meets EU chiefs Costa and von der Leyen in "
     "Brussels for the second EU–UK summit, agreeing food, carbon and "
     "youth deals.", ill_euuk),
    ("CLIMATE", "COP31: NO DEAL ON FINAL DAY",
     "Climate talks in Antalya enter their final day with no deal, running "
     "past the deadline. A draft released Thursday had dropped fossil-fuel "
     "phase-out language.", ill_cop),
]

BRIEFS = [
    "Russian missiles land in Poland; no one hurt",
    "US Senate blocks Iran war-powers vote, 51–48",
    "Hungary lifts veto on Ukraine EU talks",
    "Ukraine retakes 14 villages in Kharkiv push",
    "Merz: no new Yalta deal over Europe's head",
    "Estonia to shut Russia border for six months",
    "Trump floats penalties for AI centres abroad",
    "US and China agree human control of war AI",
    "TSMC, Samsung pause advanced chips for China",
    "Gold crashes to $3,514, a 14-month low",
    "Bitcoin falls for a third day to about $61,700",
    "Dollar hits 19-month high; real yields soar",
    "Alcaraz beats Cobolli 6–4, 6–1 in Turin",
    "Wagner's 35 lift Magic past Nets, 113–111",
    "Raptors snap six-game slide, beat Pistons",
    "World Children's Day marked around the globe",
    "US approved 880,000 AI chips for China firms",
    "Oracle says OpenAI funding is fully secured",
    "CrowdStrike in talks to buy Zscaler",
    "Cognition AI eyes $2bn round at $75bn value",
    "Danaher, Microsoft build shared AI lab platform",
    "Google brings grocery shopping to Gemini",
    "MIT keeps AI chaos models within real bounds",
    "Cursor maker weighs dropping Chinese AI models",
    "Binance hacker moves $600m of Ether in 2 days",
    "SEC charges fake crypto platforms in $37m fraud",
    "Canada's Liberal budget passes Commons 162–151",
    "BC swears in first Tory government in a century",
]

REGIONS = [
    ("ASIA", (192, 57, 43)), ("AMERICAS", (31, 97, 141)),
    ("EUROPE", (46, 134, 193)), ("MIDDLE EAST", (183, 149, 11)),
    ("AFRICA", (30, 132, 73)), ("TECH", (125, 60, 152)),
    ("MARKETS", (202, 111, 30)), ("SPORT", (20, 143, 119)),
]

NUMBERS = ["NIKKEI −5.06%", "KOSPI −5.21%", "S&P 500 −3.70%",
           "NASDAQ −5.28%", "GOLD $3,514", "BITCOIN $61,700", "GTA VI $3.79BN"]

DATE_CHECK = [
    "Every story here happened or was",
    "first reported on Friday 20 Nov 2026.",
    "COP31 draft: out Thu 19 Nov; the",
    "final-day deadlock is Fri 20 Nov.",
    "LEFT OUT: ICJ Myanmar ruling, Riyadh",
    "tower strike, Bukele bid, IMF warning",
    "— all Thu 19 Nov. CMA Awards (18 Nov),",
    "Kenya Ebola (11 Nov), Sudan mine (Sept).",
]


def draw_map(d, x, y, w, h):
    for lat, ranges in LAND:
        my = y + (75 - lat) / 135 * h
        for lo0, lo1 in ranges:
            lon = lo0
            while lon <= lo1:
                mx = x + (lon + 180) / 360 * w
                d.ellipse([mx - 1.6, my - 1.6, mx + 1.6, my + 1.6], fill=(138, 155, 174))
                lon += 4
    for lon, lat in MARKERS:
        mx = x + (lon + 180) / 360 * w
        my = y + (75 - lat) / 135 * h
        d.ellipse([mx - 3.5, my - 3.5, mx + 3.5, my + 3.5], fill=RED,
                  outline=(255, 255, 255), width=1)


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = F(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 4), title, font=tf, fill=INK)
    sf = F(SANS_B, 13)
    d.text((8, 72), "FRIDAY, 20 NOVEMBER 2026", font=sf, fill=INK)
    rt = "ONE DAY  •  ONE PAGE  •  41 STORIES"
    d.text((W - 8 - d.textlength(rt, font=F(SANS, 11)), 74), rt,
           font=F(SANS, 11), fill=MUTED)
    d.line([(8, 92), (W - 8, 92)], fill=INK, width=2)
    d.line([(8, 96), (W - 8, 96)], fill=INK, width=1)

    # ---- region strip
    rf = F(SANS_B, 10)
    widths = [d.textlength(n, font=rf) + 20 for n, _ in REGIONS]
    total = sum(widths) + 6 * (len(REGIONS) - 1)
    cx = (W - total) / 2
    for (name, col), wch in zip(REGIONS, widths):
        d.rounded_rectangle([cx, 102, cx + wch, 122], radius=4, fill=col)
        d.text((cx + 10, 106), name, font=rf, fill=(255, 255, 255))
        cx += wch + 6

    # ---- numbers strip
    d.rectangle([8, 128, W - 8, 158], fill=NAVY)
    label = "THE DAY IN NUMBERS"
    items = "  •  ".join(NUMBERS)
    line = label + "   " + items
    nf = F(SANS_B, 12)
    while d.textlength(line, font=nf) > W - 24 and nf.size > 8:
        nf = F(SANS_B, nf.size - 1)
    lw = d.textlength(line, font=nf)
    lx = (W - lw) / 2
    d.text((lx, 137), label, font=nf, fill=(245, 197, 24))
    d.text((lx + d.textlength(label + "   ", font=nf), 137), items,
           font=nf, fill=(255, 255, 255))

    # ---- heroes
    hf = F(SERIF_B, 18)
    hb = F(SANS, 10)
    hk = F(SANS_B, 9)
    for i, (kick, head, body, ill) in enumerate(HEROES):
        x = 8 + i * 296
        d.rectangle([x, 164, x + 292, 402], fill=(255, 255, 255),
                    outline=CARD_LINE, width=1)
        ill(d, x + 1, 165, 290, 112)
        d.text((x + 10, 282), kick, font=hk, fill=RED)
        for j, ln in enumerate(wrap(d, head, hf, 272)):
            d.text((x + 10, 296 + j * 22), ln, font=hf, fill=INK)
        by = 296 + len(wrap(d, head, hf, 272)) * 22 + 4
        for j, ln in enumerate(wrap(d, body, hb, 272)):
            d.text((x + 10, by + j * 13), ln, font=hb, fill=(40, 40, 40))

    # ---- grid
    gf = F(SERIF_B, 12)
    gb = F(SANS, 8)
    gk = F(SANS_B, 8)
    for i, (kick, head, body, ill) in enumerate(GRID):
        col, row = i % 5, i // 5
        x = 8 + col * 178
        y = 408 + row * 142
        d.rectangle([x, y, x + 172, y + 138], fill=(255, 255, 255),
                    outline=CARD_LINE, width=1)
        ill(d, x + 1, y + 1, 170, 44)
        d.text((x + 7, y + 49), kick, font=gk, fill=RED)
        hl = wrap(d, head, gf, 158)
        for j, ln in enumerate(hl):
            d.text((x + 7, y + 61 + j * 15), ln, font=gf, fill=INK)
        by = y + 61 + len(hl) * 15 + 2
        for j, ln in enumerate(wrap(d, body, gb, 158)):
            d.text((x + 7, by + j * 11), ln, font=gb, fill=(40, 40, 40))

    # ---- map panel
    mf = F(SANS_B, 11)
    d.text((8, 698), "WHERE IT HAPPENED", font=mf, fill=INK)
    d.line([(8, 716), (330, 716)], fill=INK, width=1)
    draw_map(d, 12, 722, 314, 106)

    # ---- date check
    d.rectangle([8, 838, 330, 958], outline=RED, width=2)
    d.text((18, 846), "DATE CHECK — WHAT WE VERIFIED", font=F(SANS_B, 10), fill=RED)
    for j, ln in enumerate(DATE_CHECK):
        d.text((18, 864 + j * 11), ln, font=F(SANS, 9), fill=INK)

    # ---- briefs
    d.text((338, 698), "THE DAY IN BRIEF — 28 MORE STORIES", font=mf, fill=INK)
    d.line([(338, 716), (W - 8, 716)], fill=INK, width=1)
    bf = F(SANS, 9)
    bfn = F(SANS_B, 9)
    for i, b in enumerate(BRIEFS):
        col, row = i // 14, i % 14
        x = 338 + col * 280
        y = 722 + row * 17
        d.text((x, y), f"{i + 1:2d}.", font=bfn, fill=RED)
        d.text((x + 22, y), b, font=bf, fill=INK)

    # ---- footer
    d.line([(8, 966), (W - 8, 966)], fill=INK, width=1)
    ff = F(SANS, 9)
    f1 = ("Original drawings — no photographs. Sources: Reuters, AP, Bloomberg, "
          "Nikkei, Yonhap, AFP, The Guardian, CoinDesk.")
    f2 = "All 41 stories were announced, published or played on Friday 20 November 2026."
    f3 = "THE WORLD TODAY  •  FRIDAY 20 NOVEMBER 2026  •  ONE DAY, ONE PAGE"
    for j, ln in enumerate((f1, f2, f3)):
        d.text(((W - d.textlength(ln, font=ff)) / 2, 974 + j * 15), ln,
               font=ff, fill=MUTED if j < 2 else INK)
    return img


def main():
    img = build()
    img.save(OUT, "PNG", optimize=True)
    data = open(OUT, "rb").read()
    print(f"saved {OUT}: {len(data)} bytes, {img.size[0]}x{img.size[1]}")
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
