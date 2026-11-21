#!/usr/bin/env python3
"""Draw the 20 November 2026 news front page (900x1024 PNG). v4.

Winners' blueprint: masthead + date, region strip, numbers strip, 3 hero
cards, 10-card grid, dotted world map beside 28 numbered briefs, red
DATE CHECK box, sources footer. All illustrations are original flat
vector-style drawings made with Pillow primitives; no photographs.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
M = 24  # margin
CW = W - 2 * M  # content width = 852

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARK = (24, 32, 54)
GOLD = (212, 175, 55)
MUTED = (110, 105, 92)
CARD_BG = (255, 255, 255)
BORDER = (200, 192, 172)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

def wrap(text, fnt, max_w):
    """Greedy word wrap using real font metrics."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(d, x, y, text, fnt, fill, max_w, line_h):
    lines = wrap(text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += line_h
    return y

def text_h(text, fnt, max_w, line_h):
    return len(wrap(text, fnt, max_w)) * line_h

def rr(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- illustrations
def ill_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(122, 20, 20))
    # skyline
    for i, bh in enumerate([0.45, 0.7, 0.55, 0.85, 0.6, 0.75]):
        bx = x + 8 + i * (w - 16) / 6
        bw = (w - 16) / 6 - 4
        d.rectangle([bx, y + h - bh * h * 0.55, bx + bw, y + h],
                    fill=(60, 10, 10))
    # jagged falling chart
    pts = [(x + 10, y + 18), (x + w * 0.25, y + 30), (x + w * 0.4, y + 24),
           (x + w * 0.55, y + 48), (x + w * 0.7, y + 42), (x + w - 12, y + h - 18)]
    d.line(pts, fill=(255, 210, 63), width=4, joint="curve")
    # arrow head
    d.polygon([(x + w - 12, y + h - 18), (x + w - 26, y + h - 26),
               (x + w - 24, y + h - 10)], fill=(255, 210, 63))
    # red down bars
    for i, bh in enumerate([22, 34, 26, 44]):
        bx = x + 14 + i * 18
        d.rectangle([bx, y + h - 14 - bh, bx + 10, y + h - 14],
                    fill=(232, 72, 72))

def ill_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    # stars
    for sx, sy in [(0.12, 0.2), (0.3, 0.12), (0.55, 0.25), (0.78, 0.14),
                   (0.88, 0.32), (0.45, 0.38), (0.2, 0.45)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 255, 255))
    # missile trails
    d.line([(x + w * 0.1, y + h * 0.15), (x + w * 0.45, y + h * 0.62)],
           fill=(255, 200, 80), width=3)
    d.line([(x + w * 0.9, y + h * 0.1), (x + w * 0.62, y + h * 0.55)],
           fill=(255, 200, 80), width=3)
    # impact crater + burst
    cx, cy = x + w * 0.52, y + h * 0.68
    d.ellipse([cx - 26, cy - 10, cx + 26, cy + 10], fill=(40, 30, 20))
    d.ellipse([cx - 14, cy - 6, cx + 14, cy + 6], fill=(90, 50, 20))
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 16, 30
        a = math.radians(ang)
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a) * 0.5,
                cx + r2 * math.cos(a), cy + r2 * math.sin(a) * 0.5],
               fill=(255, 160, 40), width=3)
    # ground
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 42, 30))
    # NATO star (small compass)
    sx, sy = x + w - 26, y + 22
    d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], outline=(255, 255, 255), width=2)
    d.polygon([(sx, sy - 9), (sx + 2, sy), (sx, sy + 9), (sx - 2, sy)],
              fill=(255, 255, 255))

def ill_gta(d, x, y, w, h):
    # Vice City sunset: orange -> pink bands
    bands = [(255, 140, 66), (255, 110, 120), (200, 80, 160), (90, 50, 120)]
    bh = h / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=col)
    # sun
    d.ellipse([x + w * 0.62, y + h * 0.18, x + w * 0.82, y + h * 0.18 + w * 0.2],
              fill=(255, 230, 120))
    # skyline
    for i, bht in enumerate([0.35, 0.55, 0.42, 0.7, 0.5]):
        bx = x + 6 + i * (w - 12) / 5
        bw = (w - 12) / 5 - 4
        d.rectangle([bx, y + h - bht * h * 0.45 - 14, bx + bw, y + h - 14],
                    fill=(40, 20, 60))
    # palm silhouettes
    for px, ph in [(0.12, 0.5), (0.88, 0.55)]:
        tx, ty = x + px * w, y + h - 14
        d.line([(tx, ty), (tx, ty - ph * h * 0.6)], fill=(30, 15, 45), width=4)
        for dx in (-14, -7, 0, 7, 14):
            d.line([(tx, ty - ph * h * 0.6), (tx + dx, ty - ph * h * 0.6 - 12)],
                   fill=(30, 15, 45), width=3)
    # sea
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 60, 110))

def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 90, 120))
    # river
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(40, 70, 110))
    # bridge
    d.line([(x + 4, y + h * 0.55), (x + w - 4, y + h * 0.55)], fill=(230, 230, 230), width=4)
    for bx in [0.2, 0.4, 0.6, 0.8]:
        d.line([(x + bx * w, y + h * 0.55), (x + bx * w, y + h * 0.3)],
               fill=(230, 230, 230), width=2)
    d.line([(x + 4, y + h * 0.3), (x + w - 4, y + h * 0.3)], fill=(230, 230, 230), width=2)
    # explosion burst
    ex, ey = x + w * 0.68, y + h * 0.38
    for r, col in [(18, (255, 200, 60)), (11, (255, 120, 30)), (5, (255, 240, 180))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    # smoke
    for sx, sy, sr in [(0.3, 0.25, 7), (0.38, 0.2, 5), (0.55, 0.22, 6)]:
        d.ellipse([x + sx * w - sr, y + sy * h - sr, x + sx * w + sr, y + sy * h + sr],
                  fill=(90, 90, 95))

def ill_wallstreet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    # buildings
    for i, bh in enumerate([0.5, 0.8, 0.65, 0.9, 0.55]):
        bx = x + 4 + i * (w - 8) / 5
        bw = (w - 8) / 5 - 3
        d.rectangle([bx, y + h - bh * h * 0.6, bx + bw, y + h], fill=(52, 66, 96))
        for wy in range(3):
            d.rectangle([bx + 3, y + h - bh * h * 0.6 + 4 + wy * 8, bx + bw - 3,
                         y + h - bh * h * 0.6 + 8 + wy * 8], fill=(255, 210, 90))
    # big red down arrow
    d.line([(x + 12, y + 10), (x + w - 14, y + h - 22)], fill=(232, 60, 60), width=5)
    d.polygon([(x + w - 14, y + h - 22), (x + w - 30, y + h - 24),
               (x + w - 16, y + h - 38)], fill=(232, 60, 60))

def ill_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 60, 40))
    # chip
    cx, cy = x + w * 0.42, y + h * 0.5
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(30, 110, 70),
                outline=(120, 220, 150), width=2)
    d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=(20, 80, 50))
    for i in range(5):
        d.line([(cx - 26, cy - 18 + i * 9), (cx - 34, cy - 18 + i * 9)],
               fill=(120, 220, 150), width=2)
        d.line([(cx + 26, cy - 18 + i * 9), (cx + 34, cy - 18 + i * 9)],
               fill=(120, 220, 150), width=2)
    # magnifier
    mx, my = x + w * 0.78, y + h * 0.32
    d.ellipse([mx - 13, my - 13, mx + 13, my + 13], outline=(255, 255, 255), width=3)
    d.line([(mx + 9, my + 9), (mx + 20, my + 20)], fill=(255, 255, 255), width=3)
    # red down tick
    d.line([(x + 8, y + 12), (x + 26, y + 26)], fill=(255, 90, 90), width=3)

def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 200))
    # sea
    d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(30, 90, 130))
    # spiral
    cx, cy = x + w * 0.5, y + h * 0.42
    for r in [34, 26, 18, 10]:
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              start=200, end=200 + 260, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(255, 255, 255))
    # rain
    for i in range(6):
        rx = x + 10 + i * (w - 20) / 5
        d.line([(rx, y + 8), (rx - 4, y + 22)], fill=(255, 255, 255), width=2)

def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 120, 90))
    # Andes triangles
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.25), (x + w * 0.5, y + h)],
              fill=(90, 70, 55))
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.62, y + h * 0.15),
               (x + w * 0.9, y + h)], fill=(70, 55, 45))
    d.polygon([(x + w * 0.55, y + h * 0.15), (x + w * 0.62, y + h * 0.15),
               (x + w * 0.585, y + h * 0.3)], fill=(255, 255, 255))
    # seismograph line
    pts = [(x + 6, y + h * 0.72), (x + w * 0.2, y + h * 0.72),
           (x + w * 0.3, y + h * 0.55), (x + w * 0.38, y + h * 0.88),
           (x + w * 0.46, y + h * 0.5), (x + w * 0.54, y + h * 0.9),
           (x + w * 0.62, y + h * 0.6), (x + w * 0.72, y + h * 0.72),
           (x + w - 6, y + h * 0.72)]
    d.line(pts, fill=(220, 40, 40), width=3)
    # crack
    d.line([(x + w * 0.5, y + h), (x + w * 0.55, y + h * 0.85),
            (x + w * 0.48, y + h * 0.7)], fill=(40, 25, 15), width=2)

def ill_cancer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
    # cells shrinking
    for cx, cy, r, col in [(0.3, 0.35, 14, (200, 60, 60)),
                           (0.55, 0.3, 10, (200, 60, 60)),
                           (0.75, 0.45, 8, (200, 60, 60)),
                           (0.4, 0.62, 6, (150, 150, 150))]:
        d.ellipse([x + cx * w - r, y + cy * h - r, x + cx * w + r, y + cy * h + r],
                  fill=col)
    # pill capsule
    px, py = x + w * 0.5, y + h * 0.72
    d.rounded_rectangle([px - 34, py - 10, px + 34, py + 10], radius=10,
                        fill=(255, 255, 255), outline=(200, 60, 60), width=2)
    d.rectangle([px - 34, py - 10, px, py + 10], fill=(230, 80, 60))
    d.rounded_rectangle([px - 34, py - 10, px + 34, py + 10], radius=10,
                        outline=(120, 40, 40), width=2)

def ill_arch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 190, 170))
    # arch
    ax, ay = x + w * 0.5, y + h * 0.75
    d.rectangle([ax - 34, ay - 34, ax - 22, ay], fill=(120, 105, 85))
    d.rectangle([ax + 22, ay - 34, ax + 34, ay], fill=(120, 105, 85))
    d.arc([ax - 34, ay - 58, ax + 34, ay + 10], start=180, end=360,
          fill=(120, 105, 85), width=12)
    # red block slash
    d.line([(x + 8, y + h - 8), (x + w - 8, y + 8)], fill=(200, 30, 30), width=5)
    d.ellipse([x + w - 22, y + 8, x + w - 6, y + 24], fill=(200, 30, 30))
    d.text((x + w - 20, y + 9), "!", font=SANS_B(13), fill=(255, 255, 255))

def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 90, 160))
    # court lines
    d.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], outline=(255, 255, 255), width=2)
    d.line([(x + w / 2, y + 8), (x + w / 2, y + h - 8)], fill=(255, 255, 255), width=2)
    # ball
    cx, cy = x + w * 0.5, y + h * 0.5
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(200, 230, 60))
    d.arc([cx - 20, cy - 20, cx + 20, cy + 20], start=300, end=60,
          fill=(255, 255, 255), width=3)
    d.arc([cx - 20, cy - 20, cx + 20, cy + 20], start=120, end=240,
          fill=(255, 255, 255), width=3)

def ill_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 60, 70))
    # sea
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(20, 40, 70))
    # tanker
    d.polygon([(x + 10, y + h * 0.68), (x + w - 10, y + h * 0.68),
               (x + w - 22, y + h * 0.82), (x + 22, y + h * 0.82)],
              fill=(40, 40, 45))
    d.rectangle([x + w * 0.62, y + h * 0.5, x + w * 0.72, y + h * 0.68],
                fill=(200, 200, 200))
    # flames
    for fx, fy, fr in [(0.3, 0.5, 12), (0.42, 0.42, 15), (0.55, 0.5, 10)]:
        d.ellipse([x + fx * w - fr, y + fy * h - fr, x + fx * w + fr, y + fy * h + fr],
                  fill=(255, 140, 30))
        d.ellipse([x + fx * w - fr * 0.5, y + fy * h - fr * 0.5,
                   x + fx * w + fr * 0.5, y + fy * h + fr * 0.5], fill=(255, 220, 80))
    # smoke
    for sx, sy, sr in [(0.35, 0.25, 8), (0.45, 0.18, 6), (0.55, 0.28, 7)]:
        d.ellipse([x + sx * w - sr, y + sy * h - sr, x + sx * w + sr, y + sy * h + sr],
                  fill=(120, 120, 125))

def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 80, 70))
    # globe
    cx, cy = x + w * 0.5, y + h * 0.45
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(60, 140, 200))
    d.ellipse([cx - 14, cy - 18, cx + 2, cy - 2], fill=(70, 160, 90))
    d.ellipse([cx - 4, cy + 6, cx + 16, cy + 20], fill=(70, 160, 90))
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(255, 255, 255), width=2)
    # clock (overtime)
    kx, ky = x + w * 0.78, y + h * 0.78
    d.ellipse([kx - 11, ky - 11, kx + 11, ky + 11], fill=(255, 255, 255))
    d.line([(kx, ky), (kx, ky - 8)], fill=(200, 30, 30), width=2)
    d.line([(kx, ky), (kx + 7, ky + 2)], fill=(200, 30, 30), width=2)
    # empty chairs (small)
    for i in range(3):
        bx = x + 12 + i * 18
        d.rectangle([bx, y + h - 16, bx + 12, y + h - 6], fill=(200, 200, 200))

# ---------------------------------------------------------------- content
REGIONS = [("MIDDLE EAST", (178, 34, 34)), ("ASIA", (200, 110, 20)),
           ("MARKETS", (40, 120, 60)), ("EUROPE", (40, 80, 160)),
           ("SPORT", (120, 70, 160)), ("SCIENCE", (20, 140, 140)),
           ("AMERICAS", (150, 90, 40)), ("CLIMATE", (30, 110, 80))]

NUMBERS = [("-5.06%", "Nikkei 225, Tokyo"),
           ("-5.21%", "Kospi, Seoul"),
           ("$4tn", "Nasdaq value wiped in a week"),
           ("$3.79bn", "GTA VI day-one sales"),
           ("400+", "drones fired at Ukraine"),
           ("6.7", "Peru quake magnitude")]

HEROES = [
    dict(kicker="MARKETS · TOKYO", ill=ill_market,
         head="Asia's Black Friday",
         body="Tokyo's Nikkei plunges 5.06% and Seoul's Kospi falls 5.21%, "
              "closing below 5,000, as an AI sell-off sweeps Asia. Taiwan's "
              "Taiex drops 6.6%. Worst week since 2020."),
    dict(kicker="CONFLICT · POLAND", ill=ill_poland,
         head="Russian missiles land in Poland",
         body="Two Russian missiles and a jet drone crash into NATO Poland. "
              "A Kh-101 lands near Nowy Lipowiec; Rutte calls it a "
              "\u201cgrave violation\u201d and Tusk a deliberate provocation."),
    dict(kicker="CULTURE · LOS SANTOS", ill=ill_gta,
         head="GTA VI: $3.79bn in a day",
         body="Rockstar announces GTA VI took $3.79 billion in day-one sales, "
              "the biggest entertainment launch ever. 32.5 million copies sold "
              "before release day."),
]

GRID = [
    dict(kicker="UKRAINE · KYIV", ill=ill_kyiv,
         head="Kyiv's bridges hit",
         body="Three killed, ~15 hurt as missiles hit three Dnipro bridges — "
              "the biggest attack on the capital's crossings."),
    dict(kicker="MARKETS · NEW YORK", ill=ill_wallstreet,
         head="Wall Street joins the rout",
         body="S&P −3.70%, seventh straight loss, into correction. Nasdaq "
              "−5.28%, erasing all 2026 gains. Nvidia −14%."),
    dict(kicker="TECH · WASHINGTON", ill=ill_nvidia,
         head="SEC probes Nvidia",
         body="SEC enforcement is examining accounting issues, Reuters reports. "
              "Shares −14% to $125.53, ~$491bn wiped."),
    dict(kicker="WEATHER · ODISHA", ill=ill_cyclone,
         head="Cyclone Akvan slams Odisha",
         body="Landfall Friday near Gopalpur, winds gusting 90 km/h. 300,000+ "
              "evacuated; 9,341 shelters; no deaths at first."),
    dict(kicker="DISASTER · PERU", ill=ill_quake,
         head="Peru quake 6.7 shakes Andes",
         body="Magnitude 6.7 at 7:09 p.m., 34 km north of Junín. Felt across "
              "Lima; hundreds into the streets. No casualties."),
    dict(kicker="SCIENCE · BARCELONA", ill=ill_cancer,
         head="Cancer pill hope",
         body="Daraxonrasib plus chemo, presented Friday in Barcelona: tumours "
              "undetectable in 1 in 12. Early trial, not a cure."),
    dict(kicker="POLITICS · VIRGINIA", ill=ill_arch,
         head="Judge blocks Trump's arch",
         body="Judge Brinkema blocks the 250-foot triumphal arch indefinitely. "
              "The second judge to rule against it this week."),
    dict(kicker="TENNIS · TURIN", ill=ill_tennis,
         head="Medvedev into Turin semis",
         body="Medvedev beats Tiafoe 6–3, 6–4 on Friday night to reach the ATP "
              "Finals semis. He faces Zverev on Saturday."),
    dict(kicker="ENERGY · HORMUZ", ill=ill_tanker,
         head="Tanker burns in Hormuz",
         body="An oil tanker burns in the Strait of Hormuz. Brent +2.3% to "
              "$64.01; the IEA calls it the largest supply shock on record."),
    dict(kicker="CLIMATE · ANTALYA", ill=ill_cop31,
         head="COP31: no deal on final day",
         body="Talks in Antalya enter their final day past the deadline with no "
              "deal. The draft dropping fossil fuels came out Thursday."),
]

BRIEFS = [
    "US Senate blocks Iran war-powers vote, 51–48.",
    "Hungary lifts veto on Ukraine EU talks.",
    "Ukraine retakes 14 villages in Kharkiv push.",
    "Merz: no new Yalta deal over Europe's head.",
    "Estonia to shut Russia border for six months.",
    "Trump floats penalties for AI centres abroad.",
    "US and China agree human control of war AI.",
    "TSMC, Samsung pause advanced chips for China.",
    "Gold crashes to $3,514, a 14-month low.",
    "Bitcoin falls for third day to $61,700.",
    "Dollar hits 19-month high; real yields soar.",
    "Alcaraz beats Cobolli 6–4, 6–1 in Turin.",
    "Wagner's 35 lift Magic past Nets, 113–111.",
    "Raptors snap slide, beat Pistons 105–102.",
    "World Children's Day marked worldwide.",
    "US approved 880,000 AI chips for China firms.",
    "Anthropic slides day two, −8.5% to $88.91.",
    "EU and UK strike new food, carbon deals.",
    "Moscow rejects NATO-style guarantees.",
    "Saudi defences stop missile, 5 drones.",
    "Kryvyi Rih strike kills boy, 7, paramedic.",
    "Trump tells Europe to defund Ukraine.",
    "Fiona the hippo dies at Cincinnati Zoo.",
    "Oracle says OpenAI funding is fully secured.",
    "CrowdStrike in talks to buy Zscaler.",
    "SEC charges fake crypto platforms in $37m.",
    "Canada's Liberal budget passes 162–151.",
    "BC's first Tory government in a century.",
]

DATE_CHECKS = [
    ("ICJ MYANMAR RULING", "was Thu 19 Nov — NOT used as a hero."),
    ("RIYADH TOWER STRIKE", "was Thu 19 Nov — NOT used as a hero."),
    ("COP31 DRAFT", "was Thu 19 Nov; only the Fri deadlock is shown."),
    ("GTA VI $3.79bn", "covers sales through end of Thu 19 Nov — announced Fri 20 Nov."),
    ("CANCER PILL", "data presented Fri 20 Nov in Barcelona (company release Thu 19 Nov)."),
]

MAP_ROWS = [
    "                                              ",
    "   #########        #####    ############      ",
    "  ###########      #######  ################   ",
    "   ##########       #####   ###############    ",
    "    ########         ###     ############      ",
    "     ######          ##  ##   #########        ",
    "      ####           ########  ######          ",
    "       ##            ######    ####            ",
    "        #   ##       #####      ##             ",
    "           ####      ####                       ",
    "            ###       ##        ####           ",
    "             ##       #         ######         ",
    "              #                 ####           ",
    "                                              ",
]

# (label, lon, lat, dx, dy) — dx/dy optional pin offset in px with leader line
PINS = [
    ("1 Tokyo", 139.7, 35.7, 0, 0),
    ("2 Poland", 22.5, 50.5, -14, -10),
    ("3 Kyiv", 30.5, 50.4, 0, 0),
    ("4 Riyadh", 46.7, 24.6, 0, 0),
    ("5 Odisha", 85.5, 20.0, 0, 0),
    ("6 Junín", -75.2, -11.2, 0, 0),
    ("7 Turin", 7.7, 45.1, 0, 0),
    ("8 Hormuz", 56.5, 26.5, 0, 0),
    ("9 Antalya", 30.7, 36.9, 0, 0),
    ("10 New York", -74.0, 40.7, 0, 0),
]

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 12

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = SERIF_B(54)
    tw = tf.getlength(title)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 60
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 6
    dateline = "FRIDAY, 20 NOVEMBER 2026  ·  41 STORIES FROM ONE DAY  ·  ALL DRAWINGS, NO PHOTOGRAPHS"
    df = SANS_B(12.5)
    dw = df.getlength(dateline)
    d.text(((W - dw) / 2, y), dateline, font=df, fill=RED)
    y += 20

    # ---- region strip
    rf = SANS_B(11)
    chip_w = []
    for label, _ in REGIONS:
        chip_w.append(rf.getlength(label) + 18)
    total = sum(chip_w) + 6 * (len(REGIONS) - 1)
    cx = (W - total) / 2
    for (label, col), wch in zip(REGIONS, chip_w):
        rr(d, [cx, y, cx + wch, y + 22], 11, fill=col)
        twl = rf.getlength(label)
        d.text((cx + (wch - twl) / 2, y + 4), label, font=rf, fill=(255, 255, 255))
        cx += wch + 6
    y += 28

    # ---- numbers strip
    band_h = 44
    d.rectangle([M, y, W - M, y + band_h], fill=DARK)
    lab = "THE DAY IN NUMBERS"
    lf = SANS_B(10)
    d.text((M + 10, y + 5), lab, font=lf, fill=GOLD)
    ncols = len(NUMBERS)
    colw = (CW - 20) / ncols
    nf = SANS_B(18)
    sf = SANS(8.5)
    for i, (num, sub) in enumerate(NUMBERS):
        nx = M + 10 + i * colw
        nw = nf.getlength(num)
        d.text((nx + (colw - nw) / 2, y + 17), num, font=nf, fill=(255, 210, 63))
        sw = sf.getlength(sub)
        d.text((nx + (colw - sw) / 2, y + 34), sub, font=sf, fill=(220, 220, 220))
    y += band_h + 6

    # ---- heroes
    hw = (CW - 2 * 12) / 3
    hh = 224
    hero_y = y
    for i, hero in enumerate(HEROES):
        hx = M + i * (hw + 12)
        d.rectangle([hx, hero_y, hx + hw, hero_y + hh], fill=CARD_BG,
                    outline=BORDER, width=1)
        hero["ill"](d, hx + 1, hero_y + 1, hw - 2, 100)
        ty = hero_y + 108
        kf = SANS_B(10)
        d.text((hx + 10, ty), hero["kicker"], font=kf, fill=RED)
        ty += 16
        hf = SERIF_B(16)
        ty = draw_wrapped(d, hx + 10, ty, hero["head"], hf, INK, hw - 20, 19)
        ty += 3
        bf = SANS(10)
        draw_wrapped(d, hx + 10, ty, hero["body"], bf, (60, 60, 60), hw - 20, 13)
    y = hero_y + hh + 6

    # ---- grid 5x2
    gw = (CW - 4 * 10) / 5
    gh = 152
    grid_y = y
    for idx, card in enumerate(GRID):
        r, c = divmod(idx, 5)
        gx = M + c * (gw + 10)
        gy = grid_y + r * (gh + 6)
        d.rectangle([gx, gy, gx + gw, gy + gh], fill=CARD_BG, outline=BORDER, width=1)
        card["ill"](d, gx + 1, gy + 1, gw - 2, 50)
        ty = gy + 56
        kf = SANS_B(8)
        d.text((gx + 7, ty), card["kicker"], font=kf, fill=RED)
        ty += 12
        hf = SERIF_B(11.5)
        ty = draw_wrapped(d, gx + 7, ty, card["head"], hf, INK, gw - 14, 13.5)
        ty += 2
        bf = SANS(8.5)
        draw_wrapped(d, gx + 7, ty, card["body"], bf, (60, 60, 60), gw - 14, 11)
    y = grid_y + 2 * gh + 6 + 6

    # ---- map + briefs
    sec_h = 196
    sec_top = y
    sec_y = y
    d.text((M, sec_y), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((M + 330, sec_y), "THE REST OF THE DAY — 28 MORE STORIES",
           font=SANS_B(12), fill=INK)
    sec_y += 18
    map_w, map_h = 300, 148
    mx, my = M, sec_y
    # dotted land
    rows = len(MAP_ROWS)
    cols = len(MAP_ROWS[0])
    dx = map_w / cols
    dy = map_h / rows
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                px = mx + ci * dx + dx / 2
                py = my + ri * dy + dy / 2
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(120, 120, 115))
    # pins
    pf = SANS_B(8)
    for label, lon, lat, ox, oy in PINS:
        px = mx + (lon + 180) / 360 * map_w
        py = my + (90 - lat) / 180 * map_h
        qx, qy = px + ox, py + oy
        if ox or oy:
            d.line([(px, py), (qx, qy)], fill=RED, width=1)
        num = label.split()[0]
        d.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        nw = pf.getlength(num)
        d.text((qx - nw / 2, qy - 5.5), num, font=pf, fill=(255, 255, 255))
    # legend
    leg = "1 Tokyo · 2 Poland · 3 Kyiv · 4 Riyadh · 5 Odisha · 6 Junín · 7 Turin · 8 Hormuz · 9 Antalya · 10 New York"
    lf2 = SANS(8.5)
    ly = my + map_h + 6
    draw_wrapped(d, mx, ly, leg, lf2, MUTED, map_w, 11)
    # briefs, two columns
    bx = M + 330
    bw = (CW - 330) / 2 - 6
    bf = SANS(8.5)
    for col in range(2):
        items = BRIEFS[col * 14:(col + 1) * 14]
        by = sec_y
        for j, item in enumerate(items):
            n = col * 14 + j + 1
            d.text((bx + col * (bw + 12), by), f"{n}.", font=SANS_B(8.5), fill=RED)
            nlines = len(wrap(item, bf, bw - 20))
            draw_wrapped(d, bx + col * (bw + 12) + 20, by, item, bf,
                         INK, bw - 20, 10.5)
            by += nlines * 10.5 + 2
    y = sec_top + sec_h + 4

    # ---- DATE CHECK
    dc_h = 64
    d.rectangle([M, y, W - M, y + dc_h], outline=RED, width=2)
    d.text((M + 10, y + 6), "DATE CHECK — WHAT WE LEFT OUT, AND WHY",
           font=SANS_B(11), fill=RED)
    cf = SANS(9)
    cbf = SANS_B(9)
    col_w = (CW - 20) / 2
    for i, (head, rest) in enumerate(DATE_CHECKS):
        cx2 = M + 10 + (i % 2) * col_w
        cy2 = y + 24 + (i // 2) * 13
        if i == 4:
            cy2 = y + 24 + 2 * 13
            cx2 = M + 10
        d.text((cx2, cy2), head + " ", font=cbf, fill=INK)
        d.text((cx2 + cbf.getlength(head + " "), cy2), rest, font=cf, fill=(60, 60, 60))
    y += dc_h + 5

    # ---- footer
    foot = ("Sources: Reuters · AP · AFP · Bloomberg · CNBC · Nikkei · ATP Tour · USGS · "
            "IGP · EORTC-NCI-AACR. All illustrations are original drawings; no photographs.")
    ff = SANS(8.5)
    draw_wrapped(d, M, y, foot, ff, MUTED, CW, 11)
    y += 12
    assert y <= H, f"layout overflow: y={y}"
    return img, y

if __name__ == "__main__":
    img, final_y = build()
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, "final_y", final_y)
