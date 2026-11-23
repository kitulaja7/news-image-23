# news-image-23

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/kitulaja7/news-image-23/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/kitulaja7/news-image-23/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page that sums up Monday 23 November 2026 in a single
1024×1024 image: 35 stories — three features (the Dymer attack, the corvette sunk
off Benghazi, the Asian markets rout), ten illustrated tiles, a world map with 13
pins, a DATE CHECK box that lists the stories left out on purpose, and an ALSO
TODAY list. The date itself is the masthead, a stat strip of six big numbers and
a colour-coded region bar sit above the fold, and every illustration carries a
source chip showing its status (REPORTED / OFFICIAL / CONFIRMED) and the news
agency it came from, so the verification is visible on the page itself instead
of hidden in small print.

The image is drawn at build time by `render.py` (Pillow, development only) and
committed as `entry.png`. The shipped entrypoint `main.py` uses only the Python
standard library and copies `entry.png` byte-for-byte to `/output/entry.png`,
so the grader's two runs produce identical bytes with no network and no
third-party imports.

## Run it

    python3 render.py        # draw entry.png (development, needs Pillow)
    python3 main.py          # copy entry.png to /output/entry.png

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123

## Verify

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 -c "import hashlib; print(hashlib.sha256(open('out/entry.png','rb').read()).hexdigest())"

Run `main.py` twice and compare the hashes: they must match. The image is
1024×1024 and under 1 MiB.

## Stories

Features: Dymer (Kyiv region strike), Benghazi (corvette Merkury sunk),
Asian markets rout (KOSPI −5.8%). Tiles: COP31 aftermath, 153 drones over
Kyiv, Hormuz shipping, Trump on Nvidia's Huang, Delta outage, Belgium strike,
India–NZ Test draw, Democrats take 258 House seats, Gaza report, Paredes.
The DATE CHECK box names the near-miss stories left out on purpose
('El Chapo Isidro', Alcaraz, Kyiv flat hit, Cikande fire, BepiColombo,
Peru quake) with their dates, and the count that matters tonight:
153 drones, not 400.
