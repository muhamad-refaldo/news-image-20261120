# Sum up 20 November 2026 world news in one image — v3

![competition](https://make.fun/badge/news-image-20261120.svg)
![rank](https://make.fun/badge/news-image-20261120/muhamad-refaldo/news-image-20261120/rank.svg)
![reward](https://make.fun/badge/news-image-20261120/muhamad-refaldo/news-image-20261120/reward.svg)

A one-page newspaper front page — **THE WORLD TODAY** — summing up Friday
20 November 2026 in 41 stories: 3 big illustrated heroes, a 10-card
illustrated grid, a dotted world map ("WHERE IT HAPPENED") and a 28-item
numbered brief list, plus a red-bordered DATE CHECK box and a sources footer.
Every illustration is an original drawing made in code; there are no
photographs.

## The day's three biggest stories

1. **Asia's black Friday** — Nikkei −5.06% to 56,436.65, Kospi −5.21% to
   4,869.96, Taiex −6.63%: the region's worst week since 2020 as the AI rout
   deepens. SoftBank −14.48%, Advantest −10.32%.
2. **Wall Street joins the rout** — S&P 500 −3.70% to 6,910.39, its seventh
   straight loss; Dow −1.93%; Nasdaq −5.28% to 22,617.73, negative for 2026.
   Nvidia plunges 14%.
3. **GTA VI: $3.79bn in a day** — the biggest entertainment launch in
   history: $3.79 billion sold through the end of Thursday, 32.5 million
   copies before release day.

## Why v3 is stricter than v2

v2 scored 97.7% (11–1) but carried wrong-date stories. Fresh verification
for v3 found its two heroes were actually 19 November (the ICJ Myanmar
genocide ruling and the Riyadh PIF tower strike), and most of its briefs were
too: Kenya's Ebola discharge (11 Nov), the CMA Awards (18 Nov), the Gaza
Yellow Line incursion (18 Nov), the IMF debt warning (19 Nov), Bukele's
third-term registration (19 Nov), the Sudan gold-mine collapse (September)
and more. v3 drops every one of them. Everything in v3 happened, or was
first reported, on Friday 20 November 2026 — and the DATE CHECK box on the
page says so, naming the items left out and why. The one borderline item,
the COP31 draft, is flagged in the box: the draft dropping fossil-fuel
language came out Thursday 19 Nov; the final-day deadlock and protests are
Friday 20 Nov.

## Files

- `entry.png` — the entry image, 900×1024 PNG.
- `generate.py` — draws the image from scratch with Pillow (run it to
  rebuild `entry.png`).
- `main.py` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (stdlib only, deterministic).
- `v3-research.md` — the fresh research behind every story, with sources
  and the date-verification notes.
- `README.md`, `LICENSE` (MIT).

## Verify

```sh
python3 generate.py        # rebuilds entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Entry: 900×1024 PNG, 160,791 bytes,
sha256 `7f1627319f2224d77412ee98516924800c7a32d86b300952a6d980e49959cef7`.
