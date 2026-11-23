#!/usr/bin/env python3
"""Render the news-image-20261123 front page: Monday 23 November 2026.
Draws entry.png (1024x1024, <=1 MiB) with Pillow. Dev-time only.
Written fresh for this edition; layout follows the top-5 front-page pattern
(masthead = giant date, stat strip, region bar, DATE CHECK with exclusions,
source chips, world map, ALSO list)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
BLUE = (28, 68, 128)
BORDER = (178, 172, 158)
PANEL = (252, 250, 244)
SEA = (178, 208, 224)
LAND = (216, 198, 158)
PIN = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, font, max_w):
    """Word-wrap text to lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, text, font=None):
    """Black source chip; returns width."""
    f = font or F(SANS_B, 9)
    tw = d.textlength(text, font=f)
    w = int(tw) + 12
    h = 17
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(0, 0, 0))
    d.text((x + 6, y + 3), text, font=f, fill=(255, 255, 255))
    return w


def hline(d, x0, x1, y, fill=INK, w=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def vgrad(d, box, top, bottom):
    """Vertical gradient fill inside box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def building(d, x, y, w, h, body, win_lit, win_dark, cols=4, rows=5):
    """Block building with lit/dark windows."""
    d.rectangle([x, y, x + w, y + h], fill=body, outline=(60, 55, 45))
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            wx = x + c * cw + cw * 0.22
            wy = y + r * ch + ch * 0.22
            ww, wh = cw * 0.56, ch * 0.52
            col = win_lit if (r + c) % 3 == 0 else win_dark
            d.rectangle([wx, wy, wx + ww, wy + wh], fill=col)


def smoke(d, x, y, s=1.0):
    g = (150, 148, 142)
    d.ellipse([x, y, x + 16 * s, y + 12 * s], fill=g)
    d.ellipse([x + 8 * s, y - 8 * s, x + 22 * s, y + 4 * s], fill=g)
    d.ellipse([x + 16 * s, y - 16 * s, x + 28 * s, y - 4 * s], fill=g)


def waves(d, x0, x1, y, n=3, gap=9, col=(255, 255, 255)):
    for i in range(n):
        yy = y + i * gap
        d.line([(x0, yy), (x1, yy)], fill=col, width=2)
        d.line([(x0 + 8, yy + 3), (x1 - 8, yy + 3)], fill=col, width=1)


def flame(d, cx, cy, s=1.0):
    """Orange flame teardrop."""
    d.polygon([(cx, cy - 26 * s), (cx + 13 * s, cy + 2 * s),
               (cx + 6 * s, cy + 12 * s), (cx - 6 * s, cy + 12 * s),
               (cx - 13 * s, cy + 2 * s)], fill=(235, 120, 20))
    d.polygon([(cx, cy - 12 * s), (cx + 7 * s, cy + 6 * s),
               (cx - 7 * s, cy + 6 * s)], fill=(250, 200, 60))

# ---------------------------------------------------------------- illustrations
def ill_dymer(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (18, 28, 58), (58, 74, 110))
    for sx, sy in [(30, 18), (90, 10), (150, 22), (210, 12), (270, 20)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 220))
    # collapsed apartment block, tilted
    d.polygon([(x0 + 40, y1), (x0 + 52, y0 + 34), (x0 + 150, y0 + 44),
               (x0 + 158, y1)], fill=(96, 92, 86))
    d.polygon([(x0 + 150, y0 + 44), (x0 + 210, y0 + 60), (x0 + 220, y1),
               (x0 + 158, y1)], fill=(72, 68, 62))
    for wx in range(58, 140, 18):
        d.rectangle([x0 + wx, y0 + 52, x0 + wx + 9, y0 + 62], fill=(250, 210, 90))
    # rubble pile
    d.polygon([(x0 + 120, y1), (x0 + 160, y1 - 26), (x0 + 205, y1 - 8),
               (x0 + 235, y1)], fill=(120, 114, 104))
    d.polygon([(x0 + 165, y1 - 24), (x0 + 185, y1 - 34), (x0 + 200, y1 - 20)],
              fill=(150, 144, 132))
    # rescue lights: two beams + floodlight
    d.polygon([(x0 + 250, y0 + 30), (x0 + 258, y0 + 30), (x0 + 300, y1 - 6),
               (x0 + 285, y1 - 6)], fill=(250, 230, 140))
    d.polygon([(x0 + 40, y0 + 26), (x0 + 46, y0 + 26), (x0 + 90, y1 - 10),
               (x0 + 78, y1 - 10)], fill=(250, 230, 140))
    d.rectangle([x0 + 246, y0 + 22, x0 + 262, y0 + 34], fill=(40, 40, 40))
    smoke(d, x0 + 60, y0 + 30, 1.1)


def ill_benghazi(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (10, 22, 48), (30, 58, 96))
    d.ellipse([x0 + 260, y0 + 10, x0 + 286, y0 + 36], fill=(235, 225, 190))
    # sea
    d.rectangle([x0, y0 + 62, x1, y1], fill=(16, 42, 78))
    waves(d, x0 + 8, x1 - 8, y0 + 78, 3, 10, (140, 180, 220))
    # corvette hull, listing
    d.polygon([(x0 + 30, y0 + 58), (x0 + 190, y0 + 52), (x0 + 210, y0 + 66),
               (x0 + 40, y0 + 74)], fill=(52, 58, 64))
    d.rectangle([x0 + 70, y0 + 40, x0 + 120, y0 + 56], fill=(70, 76, 82))
    d.rectangle([x0 + 128, y0 + 46, x0 + 140, y0 + 56], fill=(70, 76, 82))
    # explosion + flames on deck
    flame(d, x0 + 165, y0 + 46, 1.3)
    flame(d, x0 + 195, y0 + 52, 0.9)
    d.ellipse([x0 + 150, y0 + 8, x0 + 205, y0 + 40], fill=(250, 160, 40))
    smoke(d, x0 + 150, y0 + 6, 1.2)
    # two sea drones with wakes
    for dx in (240, 275):
        d.polygon([(x0 + dx, y0 + 88), (x0 + dx + 18, y0 + 88),
                   (x0 + dx + 14, y0 + 96), (x0 + dx + 4, y0 + 96)],
                  fill=(200, 200, 200))
        d.line([(x0 + dx - 14, y0 + 94), (x0 + dx, y0 + 94)],
               fill=(180, 210, 240), width=2)


def ill_ai_rout(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(238, 234, 222))
    # chart grid
    for gx in range(x0 + 20, x1 - 10, 30):
        d.line([(gx, y0 + 12), (gx, y1 - 26)], fill=(210, 204, 188), width=1)
    for gy in range(y0 + 12, y1 - 20, 18):
        d.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(210, 204, 188), width=1)
    # falling red line with markers
    pts = [(x0 + 16, y0 + 22), (x0 + 70, y0 + 34), (x0 + 120, y0 + 30),
           (x0 + 175, y0 + 52), (x0 + 225, y0 + 48), (x0 + 275, y0 + 78),
           (x0 + 305, y0 + 92)]
    d.line(pts, fill=(178, 34, 34), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(178, 34, 34))
    # big down arrow
    d.polygon([(x0 + 262, y0 + 84), (x0 + 292, y0 + 84), (x0 + 292, y0 + 104),
               (x0 + 306, y0 + 104), (x0 + 277, y1 - 6), (x0 + 248, y0 + 104),
               (x0 + 262, y0 + 104)], fill=(178, 34, 34))
    d.text((x0 + 14, y0 + 8), "KOSPI  -5.8%", font=F(SANS_B, 13), fill=(178, 34, 34))


def ill_cop31(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (140, 190, 225), (200, 225, 240))
    # globe
    d.ellipse([x0 + 12, y0 + 8, x0 + 78, y0 + 74], fill=(70, 140, 200),
              outline=(20, 60, 110), width=2)
    d.ellipse([x0 + 26, y0 + 18, x0 + 48, y0 + 38], fill=(90, 180, 90))
    d.ellipse([x0 + 46, y0 + 44, x0 + 68, y0 + 64], fill=(90, 180, 90))
    # sun
    d.ellipse([x0 + 120, y0 + 10, x0 + 150, y0 + 40], fill=(250, 200, 60))
    for a in range(0, 360, 45):
        import math
        x_ = x0 + 135 + int(22 * math.cos(math.radians(a)))
        y_ = y0 + 25 + int(22 * math.sin(math.radians(a)))
        d.line([(x0 + 135, y0 + 25), (x_, y_)], fill=(250, 200, 60), width=2)
    # three delegates at a table
    d.rectangle([x0 + 12, y0 + 58, x1 - 12, y0 + 66], fill=(120, 80, 50))
    for dx, c in [(30, (40, 40, 40)), (80, (120, 30, 30)), (130, (30, 60, 120))]:
        d.ellipse([x0 + dx, y0 + 34, x0 + dx + 16, y0 + 50], fill=(232, 200, 160))
        d.rectangle([x0 + dx - 4, y0 + 50, x0 + dx + 20, y0 + 60], fill=c)


def ill_kyiv_drones(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (12, 20, 44), (44, 58, 92))
    for sx, sy in [(20, 10), (70, 16), (120, 8), (160, 14)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(255, 255, 220))
    # drones: small X quadcopters with red lights
    for dx, dy in [(30, 22), (75, 14), (120, 26), (155, 16)]:
        d.line([(x0 + dx - 7, y0 + dy - 5), (x0 + dx + 7, y0 + dy + 5)],
               fill=(220, 220, 220), width=2)
        d.line([(x0 + dx - 7, y0 + dy + 5), (x0 + dx + 7, y0 + dy - 5)],
               fill=(220, 220, 220), width=2)
        d.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2],
                  fill=(255, 60, 60))
    # searchlight beam
    d.polygon([(x0 + 150, y1), (x0 + 158, y1), (x0 + 120, y0 + 30),
               (x0 + 108, y0 + 30)], fill=(250, 240, 170))
    # apartment block below
    building(d, x0 + 14, y0 + 46, 84, 30, (96, 92, 86), (250, 210, 90),
             (40, 40, 48), 4, 2)
    d.rectangle([x0 + 110, y0 + 58, x1 - 14, y1 - 4], fill=(70, 68, 62))
    flame(d, x0 + 150, y0 + 56, 0.8)


def ill_hormuz(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (150, 185, 215), (190, 215, 230))
    d.rectangle([x0, y0 + 44, x1, y1], fill=(24, 64, 110))
    waves(d, x0 + 6, x1 - 6, y0 + 56, 2, 10, (150, 190, 230))
    # tanker hull + containers
    d.polygon([(x0 + 10, y0 + 40), (x0 + 170, y0 + 40), (x0 + 178, y0 + 56),
               (x0 + 18, y0 + 56)], fill=(120, 40, 30))
    for cx, cc in [(24, (200, 60, 40)), (52, (40, 120, 60)), (80, (220, 180, 60)),
                   (108, (60, 90, 160)), (136, (200, 60, 40))]:
        d.rectangle([x0 + cx, y0 + 24, x0 + cx + 24, y0 + 40], fill=cc)
    d.rectangle([x0 + 164, y0 + 18, x1 - 10, y0 + 40], fill=(230, 230, 230))
    flame(d, x0 + 96, y0 + 22, 1.0)
    smoke(d, x0 + 88, y0 + 6, 1.0)


def ill_nvidia(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(14, 22, 44))
    # circuit traces
    for ty in (14, 30, 46, 62):
        d.line([(x0 + 8, y0 + ty), (x0 + 60, y0 + ty)], fill=(40, 90, 160), width=2)
        d.line([(x0 + 60, y0 + ty), (x0 + 60, y0 + ty + 8)], fill=(40, 90, 160), width=2)
    # chip
    d.rectangle([x0 + 66, y0 + 12, x0 + 138, y0 + 64], fill=(30, 60, 110),
                outline=(90, 160, 230), width=2)
    d.rectangle([x0 + 84, y0 + 26, x0 + 120, y0 + 50], fill=(120, 200, 250))
    d.text((x0 + 92, y0 + 30), "AI", font=F(SANS_B, 14), fill=(10, 30, 60))
    for px in range(74, 134, 12):
        d.line([(x0 + px, y0 + 8), (x0 + px, y0 + 12)], fill=(150, 200, 250), width=2)
        d.line([(x0 + px, y0 + 64), (x0 + px, y0 + 68)], fill=(150, 200, 250), width=2)
    # magnifier
    d.ellipse([x0 + 138, y0 + 8, x0 + 176, y0 + 46], outline=(250, 200, 60), width=3)
    d.line([(x0 + 168, y0 + 38), (x0 + 182, y0 + 56)], fill=(250, 200, 60), width=3)
    d.text((x0 + 146, y0 + 18), "?", font=F(SANS_B, 16), fill=(250, 200, 60))


def ill_delta(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (130, 180, 220), (200, 225, 240))
    d.ellipse([x0 + 140, y0 + 8, x0 + 172, y0 + 40], fill=(250, 240, 200))
    # plane
    d.ellipse([x0 + 18, y0 + 30, x0 + 130, y0 + 52], fill=(240, 240, 240),
              outline=(60, 60, 60))
    d.polygon([(x0 + 60, y0 + 30), (x0 + 84, y0 + 12), (x0 + 96, y0 + 30)],
              fill=(30, 60, 140))
    d.polygon([(x0 + 118, y0 + 34), (x0 + 138, y0 + 18), (x0 + 142, y0 + 34)],
              fill=(30, 60, 140))
    d.rectangle([x0 + 24, y0 + 38, x0 + 120, y0 + 42], fill=(30, 60, 140))
    # departure board
    d.rectangle([x0 + 138, y0 + 48, x1 - 8, y1 - 6], fill=(20, 20, 20))
    for i, col in enumerate([(255, 80, 80), (255, 200, 60), (255, 80, 80)]):
        d.rectangle([x0 + 144, y0 + 54 + i * 7, x0 + 176, y0 + 59 + i * 7], fill=col)


def ill_belgium(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (180, 180, 170), (220, 220, 210))
    # airport terminal
    d.rectangle([x0 + 10, y0 + 30, x1 - 10, y0 + 58], fill=(150, 145, 135))
    d.polygon([(x0 + 10, y0 + 30), (x0 + 60, y0 + 12), (x1 - 10, y0 + 30)],
              fill=(110, 105, 95))
    for wx in range(20, 170, 22):
        d.rectangle([x0 + wx, y0 + 40, x0 + wx + 12, y0 + 54], fill=(60, 80, 110))
    # picket signs
    for px, txt in [(30, "NO"), (80, "STOP"), (130, "NO")]:
        d.line([(x0 + px + 8, y0 + 58), (x0 + px + 8, y1 - 6)],
               fill=(80, 60, 40), width=2)
        d.rectangle([x0 + px, y0 + 46, x0 + px + 20, y0 + 60], fill=(255, 255, 255),
                    outline=(178, 34, 34), width=2)
        d.text((x0 + px + 3, y0 + 49), txt, font=F(SANS_B, 8), fill=(178, 34, 34))


def ill_cricket(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(120, 180, 90))
    d.rectangle([x0, y0 + 52, x1, y1], fill=(90, 150, 70))
    # pitch strip
    d.rectangle([x0 + 60, y0 + 10, x0 + 128, y1 - 6], fill=(210, 185, 140))
    # stumps
    for sx in (70, 78, 86):
        d.line([(x0 + sx, y0 + 18), (x0 + sx, y0 + 34)], fill=(250, 220, 120), width=3)
    # bat
    d.polygon([(x0 + 104, y0 + 14), (x0 + 118, y0 + 20), (x0 + 112, y0 + 52),
               (x0 + 100, y0 + 48)], fill=(230, 200, 150))
    # ball
    d.ellipse([x0 + 140, y0 + 44, x0 + 156, y0 + 60], fill=(200, 40, 40))
    d.ellipse([x0 + 146, y0 + 50, x0 + 150, y0 + 54], fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 58), "720/9", font=F(SANS_B, 13), fill=(255, 255, 255))


def ill_house(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (150, 190, 225), (205, 225, 240))
    # capitol dome
    d.rectangle([x0 + 30, y0 + 40, x0 + 158, y0 + 66], fill=(240, 240, 235))
    d.pieslice([x0 + 74, y0 + 8, x0 + 114, y0 + 46], 180, 360, fill=(240, 240, 235))
    d.rectangle([x0 + 92, y0 + 2, x0 + 96, y0 + 12], fill=(60, 60, 60))
    for cx in range(38, 156, 16):
        d.rectangle([x0 + cx, y0 + 44, x0 + cx + 6, y0 + 62], fill=(200, 200, 195))
    # ballot box
    d.rectangle([x0 + 150, y0 + 48, x1 - 10, y0 + 68], fill=(40, 80, 160))
    d.rectangle([x0 + 158, y0 + 40, x0 + 166, y0 + 50], fill=(255, 255, 255),
                outline=(40, 80, 160))
    d.text((x0 + 152, y0 + 52), "258", font=F(SANS_B, 11), fill=(255, 255, 255))


def ill_gaza(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (90, 80, 70), (140, 125, 105))
    # broken wall
    d.polygon([(x0 + 10, y1), (x0 + 14, y0 + 26), (x0 + 70, y0 + 18),
               (x0 + 78, y0 + 40), (x0 + 60, y1)], fill=(110, 100, 88))
    d.polygon([(x0 + 78, y0 + 40), (x0 + 120, y0 + 30), (x0 + 150, y1),
               (x0 + 60, y1)], fill=(90, 82, 72))
    # rubble
    d.polygon([(x0 + 90, y1), (x0 + 120, y1 - 22), (x0 + 150, y1 - 6),
               (x0 + 175, y1)], fill=(150, 140, 125))
    d.polygon([(x0 + 130, y1 - 20), (x0 + 148, y1 - 30), (x0 + 162, y1 - 16)],
              fill=(170, 160, 145))
    smoke(d, x0 + 30, y0 + 14, 1.1)
    smoke(d, x0 + 110, y0 + 20, 0.9)
    d.ellipse([x0 + 150, y0 + 8, x0 + 172, y0 + 30], fill=(220, 200, 150))


def ill_paredes(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(60, 140, 70))
    d.ellipse([x0 + 20, y0 + 10, x0 + 168, y0 + 66], outline=(255, 255, 255), width=2)
    # trophy
    d.polygon([(x0 + 78, y0 + 12), (x0 + 110, y0 + 12), (x0 + 104, y0 + 34),
               (x0 + 96, y0 + 46), (x0 + 92, y0 + 46), (x0 + 84, y0 + 34)],
              fill=(250, 200, 60))
    d.ellipse([x0 + 76, y0 + 16, x0 + 86, y0 + 30], outline=(250, 200, 60), width=3)
    d.ellipse([x0 + 102, y0 + 16, x0 + 112, y0 + 30], outline=(250, 200, 60), width=3)
    d.rectangle([x0 + 80, y0 + 46, x0 + 108, y0 + 52], fill=(250, 200, 60))
    # football
    d.ellipse([x0 + 126, y0 + 38, x0 + 162, y0 + 70], fill=(255, 255, 255),
              outline=(40, 40, 40))
    d.polygon([(x0 + 140, y0 + 48), (x0 + 148, y0 + 48), (x0 + 152, y0 + 55),
               (x0 + 146, y0 + 61), (x0 + 138, y0 + 58)], fill=(40, 40, 40))
    # microphone
    d.ellipse([x0 + 24, y0 + 40, x0 + 44, y0 + 60], fill=(60, 60, 60))
    d.line([(x0 + 34, y0 + 60), (x0 + 34, y1 - 6)], fill=(60, 60, 60), width=3)

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(8, 38), (30, 18), (70, 14), (92, 26), (88, 44), (70, 52), (48, 58), (22, 56), (6, 48)],
    [(78, 6), (96, 4), (100, 12), (84, 16)],
    [(52, 66), (78, 64), (92, 76), (84, 100), (66, 118), (54, 100), (48, 82)],
    [(150, 28), (168, 16), (190, 18), (196, 32), (182, 44), (162, 44), (150, 36)],
    [(150, 52), (176, 48), (198, 56), (206, 72), (196, 92), (176, 108), (158, 96), (148, 72)],
    [(200, 20), (240, 10), (290, 14), (308, 30), (296, 48), (260, 58), (220, 52), (200, 38)],
    [(268, 66), (282, 62), (292, 68), (280, 74)],
    [(268, 96), (296, 92), (308, 102), (296, 116), (272, 114), (262, 104)],
]
# pins: (number, x, y) in absolute page coords; map box x20-338 y766-946
PINS = [
    (1, 204, 802), (2, 194, 856), (3, 293, 827), (4, 208, 830),
    (5, 220, 818), (6, 242, 850), (7, 52, 831), (8, 64, 848),
    (9, 184, 806), (10, 319, 906), (11, 84, 830), (12, 224, 844),
    (13, 96, 896),
]
PIN_NAMES = [
    "1 Dymer", "2 Benghazi", "3 Seoul", "4 Antalya", "5 Kyiv", "6 Hormuz",
    "7 Silicon Valley", "8 Atlanta", "9 Brussels", "10 Wellington",
    "11 Raleigh", "12 Gaza", "13 Buenos Aires",
]


def draw_map(d):
    mx0, my0, mx1, my1 = 20, 766, 338, 946
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=BORDER)
    sx = (mx1 - mx0) / 318.0
    sy = (my1 - my0) / 126.0
    for poly in CONTINENTS:
        pts = [(mx0 + px * sx, my0 + py * sy) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(170, 150, 110))
    for num, px, py in PINS:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=PIN, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=F(SANS_B, 9))
        d.text((px - tw / 2, py - 6), t, font=F(SANS_B, 9), fill=(255, 255, 255))


# ---------------------------------------------------------------- content
FEATURES = [
    ("1 DYMER · WAR", "DYMER ATTACK KILLS 15",
     "Russia strikes the Kyiv region; a block collapses and rescuers dig through rubble.",
     "Reported · AFP", ill_dymer),
    ("2 BENGHAZI · WAR", "CORVETTE SUNK OFF BENGHAZI",
     "Ukraine sinks the Russian corvette Merkury with seven sea drones; cargo ship MV Angara also hit.",
     "Reported · CNN", ill_benghazi),
    ("3 SEOUL · MARKETS", "ASIAN MARKETS ROUT",
     "KOSPI dives 5.8% as Taiwan bans short-selling; Nasdaq's worst week since March 2020.",
     "Reported · Reuters", ill_ai_rout),
]
TILES = [
    ("4 ANTALYA · CLIMATE", "COP31 AFTERMATH", "Backlash in Australia, calls for Bowen to quit, Pacific despair.", "Reported · Reuters", ill_cop31),
    ("5 KYIV · WAR", "153 DRONES OVER KYIV", "Russia launches 153 drones overnight; Ukraine downs 134.", "Reported · AFP", ill_kyiv_drones),
    ("6 HORMUZ · ENERGY", "HORMUZ SHIPPING HIT", "Record maritime attacks; Bahrain blames Iran for a civilian site hit.", "Reported · France 24", ill_hormuz),
    ("7 SILICON VALLEY · TECH", "TRUMP: REHIRE HUANG", "Trump urges Nvidia to rehire Huang; SEC and California probe.", "Reported · Reuters", ill_nvidia),
    ("8 ATLANTA · TRANSPORT", "DELTA OUTAGE CHAOS", "1,600+ flights delayed at the Thanksgiving rush; Atlanta hub hit.", "Official · AP", ill_delta),
    ("9 BRUSSELS · EUROPE", "BELGIUM GRINDS TO HALT", "Airports at a total standstill in a national austerity strike.", "Official · AP", ill_belgium),
    ("10 WELLINGTON · SPORT", "INDIA–NZ TEST DRAW", "Draw at Basin Reserve; India 720/9 declared, NZ 239/5.", "Reported · AFP", ill_cricket),
    ("11 RALEIGH · POLITICS", "DEMOCRATS TAKE 258", "North Carolina recount confirms Hubbard; a historic 258-seat majority.", "Confirmed · BBC", ill_house),
    ("12 GAZA · WAR", "GAZA 'TOXIC WASTELAND'", "A new report calls Gaza a toxic wasteland; death toll 74,742.", "Reported · AP", ill_gaza),
    ("13 BUENOS AIRES · SPORT", "PAREDES COLLAPSES", "Boca captain faints in an interview after winning the Copa Sudamericana.", "Reported · ESPN", ill_paredes),
]
ALSO = [
    "COP31: 90 nations sign 35% electrification pledge",
    "Trump signs Common Cents Act — penny ends after 232 years",
    "Denmark: Russia plotted to kill Ukrainian-American rapper",
    "Russia: 792 drones downed; Kyiv: 1,392 destroyed",
    "Sparta II cargo ship burns in Baltic, drifts to Finland",
    "Trump–Putin–Xi summit fails on Ukraine",
    "Syria–EU seek normalisation",
    "S. Korea education minister quits in AI exam scandal",
    "Eisenkot calls settler attacks \"Jewish terrorism\"",
    "Drone hits home + UN building in Khartoum",
    "NATO sovereignty dilemma over private tech + AI",
    "METR: AI capability outpaces safety testing",
    "OpenAI proposes Perplexity as shared metric",
    "Taiwan $15bn fund buys shares since 6 Nov",
    "S. Korea readies $8bn rescue fund; KOSPI triggers sidecar",
    "NYC Thanksgiving: heavy rain + wind (Thu 26 Nov)",
    "California on alert for extreme tides + rain",
    "US Army to detonate unstable lead stock in Iowa",
    "Lean/Mathlib confirm Riemann proof is correct",
    "Wagyu XMR1 token plunges 99.8%",
    "CBI: Heathrow third runway £49bn \"doomed\"",
    "FedEx pilot David Sanders dies at 82 (foiled 1994 hijack)",
]
STATS = [("15", "dead in Dymer attack"), ("153", "drones fired at Kyiv"),
         ("5.8%", "KOSPI falls"), ("1,600", "Delta flights delayed"),
         ("258", "Democrat seats in US House"), ("74,742", "dead in Gaza")]
REGIONS = [("EUROPE", 9, (28, 68, 128)), ("MIDDLE EAST", 4, (140, 20, 20)),
           ("ASIA-PACIFIC", 4, (200, 120, 30)), ("AMERICAS", 11, (40, 120, 60)),
           ("AFRICA", 2, (110, 60, 140)), ("OCEANIA", 1, (40, 130, 140)),
           ("WORLD", 4, (60, 60, 60))]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # --- top bar
    d.text((14, 6), "THE WORLD TODAY", font=F(SANS_B, 11), fill=INK)
    rt = "No. 327 · 35 STORIES · 7 REGIONS · ALL FROM THIS ONE DAY"
    d.text((1010 - d.textlength(rt, font=F(SANS, 10)), 7), rt, font=F(SANS, 10), fill=INK)
    hline(d, 14, 1010, 24, INK, 2)
    # --- masthead = giant date
    size = 56
    while size > 30:
        f = F(SERIF_B, size)
        if d.textlength("Monday 23 November 2026", font=f) <= 990:
            break
        size -= 2
    d.text((512, 28), "Monday 23 November 2026", font=F(SERIF_B, size),
           fill=INK, anchor="ma")
    d.text((512, 88), "Dymer attack kills 15  ·  Benghazi corvette sunk  ·  Asian markets rout",
           font=F(SERIF, 15), fill=INK, anchor="ma")
    hline(d, 14, 1010, 108, INK, 1)
    hline(d, 14, 1010, 111, INK, 1)
    # --- stat strip
    cell = 996 / 6.0
    for i, (num, lab) in enumerate(STATS):
        cx = 14 + cell * i + cell / 2
        d.text((cx, 114), num, font=F(SANS_B, 20), fill=RED, anchor="ma")
        d.text((cx, 138), lab, font=F(SANS, 8), fill=INK, anchor="ma")
    hline(d, 14, 1010, 148, INK, 1)
    # --- region bar
    total = sum(n for _, n, _ in REGIONS)
    widths = [996 * n / total for _, n, _ in REGIONS]
    widths[5] = max(widths[5], 56)
    widths[3] -= widths[5] - 996 * 1 / total
    x = 14
    for (name, n, col), w in zip(REGIONS, widths):
        d.rectangle([x, 150, x + w, 166], fill=col)
        t = f"{name} {n}"
        f = F(SANS_B, 9)
        if d.textlength(t, font=f) > w - 4:
            f = F(SANS_B, 8)
        d.text((x + w / 2, 154), t, font=f, fill=(255, 255, 255), anchor="ma")
        x += w
    # --- features
    fx = [14, 344, 674]
    for (kicker, head, deck, src, ill), x0 in zip(FEATURES, fx):
        d.rectangle([x0, 170, x0 + 322, 390], fill=PANEL, outline=BORDER)
        ill(d, (x0 + 1, 171, x0 + 321, 285))
        d.text((x0 + 8, 289), kicker, font=F(SANS_B, 10), fill=RED)
        y = draw_lines(d, wrap(d, head, F(SANS_B, 19), 306), x0 + 8, 303,
                       F(SANS_B, 19), INK, 19)
        y = draw_lines(d, wrap(d, deck, F(SANS, 11), 306), x0 + 8, y + 2,
                       F(SANS, 11), INK, 12)
        chip(d, x0 + 8, max(368, min(y + 4, 372)), src)
    # --- tiles (2 rows x 5)
    tx = [14, 212, 410, 608, 806]
    for row, y0 in enumerate((396, 562)):
        for (kicker, head, deck, src, ill), x0 in zip(TILES[row * 5:(row + 1) * 5], tx):
            d.rectangle([x0, y0, x0 + 190, y0 + 160], fill=PANEL, outline=BORDER)
            ill(d, (x0 + 1, y0 + 1, x0 + 189, y0 + 77))
            chip(d, x0 + 4, y0 + 58, src, F(SANS_B, 8))
            d.text((x0 + 6, y0 + 82), kicker, font=F(SANS_B, 9), fill=RED)
            y = draw_lines(d, wrap(d, head, F(SANS_B, 12), 178), x0 + 6, y0 + 94,
                           F(SANS_B, 12), INK, 13)
            draw_lines(d, wrap(d, deck, F(SANS, 9), 178), x0 + 6, y + 1,
                       F(SANS, 9), INK, 11)
    # --- bottom band
    # map
    d.rectangle([14, 728, 344, 988], fill=PANEL, outline=BORDER)
    d.text((20, 732), "THE WORLD IN ONE DAY", font=F(SANS_B, 12), fill=INK)
    d.text((20, 748), "13 stories mapped — red pins", font=F(SANS, 9), fill=INK)
    draw_map(d)
    leg1 = " · ".join(PIN_NAMES[:7])
    leg2 = " · ".join(PIN_NAMES[7:])
    d.text((20, 952), leg1, font=F(SANS, 8), fill=INK)
    d.text((20, 964), leg2, font=F(SANS, 8), fill=INK)
    # DATE CHECK
    d.rectangle([352, 728, 676, 988], outline=RED, width=2, fill=PANEL)
    d.text((362, 734), "DATE CHECK", font=F(SANS_B, 14), fill=RED)
    d.text((362, 752), "READ THIS FIRST", font=F(SANS_B, 10), fill=RED)
    y = 774
    y = draw_lines(d, wrap(d, "Wires read to 07:00 UTC, Monday 23 November 2026. "
                           "Every story here happened, or was first reported, "
                           "on 23 November in at least one time zone.",
                           F(SANS, 10), 300), 362, y, F(SANS, 10), INK, 12) + 6
    y = draw_lines(d, ["LEFT OUT ON PURPOSE —"], 362, y, F(SANS_B, 10), INK, 12) + 1
    y = draw_lines(d, wrap(d, "'El Chapo Isidro' seized (Fri 20 Nov) · Alcaraz wins "
                           "ATP Finals (Sun 22 Nov) · Kyiv flat hit, 8 dead "
                           "(Sun 22 Nov) · Cikande factory fire, 36 missing "
                           "(Sun 22 Nov) · BepiColombo reaches Mercury "
                           "(Sat 21 Nov) · Peru quake (Fri 20 Nov).",
                           F(SANS, 10), 300), 362, y, F(SANS, 10), INK, 12) + 8
    y = draw_lines(d, wrap(d, "Tonight's barrage was 153 drones, not 400.",
                           F(SANS_B, 11), 300), 362, y, F(SANS_B, 11), DARKRED, 13) + 8
    draw_lines(d, wrap(d, "NOT YET: Thanksgiving Day (Thu 26 Nov) · India–NZ "
                        "2nd Test, Christchurch (Fri 27 Nov).",
                        F(SANS, 10), 300), 362, y, F(SANS, 10), INK, 12)
    d.text((362, 950), "All 35 stories were first reported on 23 November 2026.",
           font=F(SERIF, 9), fill=INK)
    # ALSO TODAY
    d.rectangle([684, 728, 1010, 988], fill=PANEL, outline=BORDER)
    d.text((692, 732), "ALSO TODAY", font=F(SANS_B, 12), fill=INK)
    hline(d, 692, 1002, 750, RED, 2)
    y = 754
    for i, item in enumerate(ALSO, start=14):
        t = f"{i}  {item}"
        f = F(SANS, 9)
        if d.textlength(t, font=f) > 306:
            f = F(SANS, 8)
        d.text((692, y), t, font=f, fill=INK)
        y += 10.5
    # --- footer
    hline(d, 14, 1010, 992, INK, 1)
    d.text((512, 998), "HOW WE CHECKED — every story carries its source. Chips show "
           "status: REPORTED · OFFICIAL · CONFIRMED. Sources: AFP · AP · Reuters · "
           "BBC · CNN · France 24 · ESPN · ANI", font=F(SANS, 9), fill=INK, anchor="ma")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
