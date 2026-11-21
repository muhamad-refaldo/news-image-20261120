# Sum up 20 November 2026 world news in one image — v4

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/muhamad-refaldo/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/muhamad-refaldo/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page — **THE WORLD TODAY** — summing up Friday
20 November 2026 in 41 stories: 3 big illustrated heroes, a 10-card
illustrated grid, a dotted world map ("WHERE IT HAPPENED") and a 28-item
numbered brief list, plus a red-bordered DATE CHECK box and a sources footer.
Every illustration is an original drawing made in code; there are no
photographs.

## The day's three biggest stories

1. **Asia's black Friday** — Nikkei −5.06% to 56,436.65, Kospi −5.21% to
   4,869.96, Taiex −6.6%: the region's worst week since 2020 as the AI rout
   deepens. SoftBank −14.48%, Advantest −10.32%.
2. **Russian missiles land in Poland** — two Russian missiles and a
   jet-powered drone crash into NATO Poland during the massive Ukraine
   barrage. A Kh-101 comes down near Nowy Lipowiec; NATO chief Rutte calls
   it a "grave violation" and PM Tusk a deliberate provocation.
3. **GTA VI: $3.79bn in a day** — the biggest entertainment launch in
   history: $3.79 billion sold through the end of Thursday, 32.5 million
   copies before release day. Announced Friday 20 Nov.

## Why v4 is different from v2 and v3

v2 scored 97.7% (11–1) but its heroes 2 and 3 were actually 19 November
(the ICJ Myanmar genocide ruling and the Riyadh PIF tower strike), and most
of its briefs were wrong-date too. v3 fixed every date but scored 95.1%
(8–1–3) — its heroes were two market stories (Asia + Wall Street), the same
theme twice. v4 keeps v3's date discipline AND v2's drama and variety: one
market hero, one NATO-conflict hero, one culture hero, all genuinely
20 November. It also adds two big 20 November stories v2 and v3 both missed:
the magnitude 6.7 Peru earthquake and the daraxonrasib pancreatic-cancer
pill results presented in Barcelona. The DATE CHECK box on the page names
the items left out and why.

## Files

- `entry.png` — the entry image, 900×1024 PNG.
- `generate.py` — draws the image from scratch with Pillow (run it to
  rebuild `entry.png`).
- `main.py` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (stdlib only, deterministic).
- `v4-research.md` — the fresh research behind every story, with sources
  and the date-verification notes.
- `README.md`, `LICENSE` (MIT).

## Verify

```sh
python3 generate.py        # rebuilds entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Entry: 900×1024 PNG, 161,447 bytes,
sha256 `e3ce787c85499fcc6eb70d18b929010718a69b451d718e78aa5729efd9028f13`.
