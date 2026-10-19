#!/usr/bin/env python3
"""The coin's image: a plain card that says what it is. 1000 x 1000 PNG, written next to this file.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-20-own-coin/image.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
W = 1000
INK, PAPER, RED = (20, 20, 20), (244, 241, 232), (190, 30, 30)


def centred(d, y, text, size, fill):
    f = ImageFont.truetype(FONT, size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([40, 40, W - 40, W - 40], outline=INK, width=8)
centred(d, 150, "PROTEUS LAB", 64, INK)
centred(d, 250, "EXPERIMENT", 110, INK)
d.rectangle([110, 420, W - 110, 600], fill=RED)
centred(d, 448, "DO NOT BUY", 120, PAPER)
centred(d, 680, "no team  no plan  no value", 40, INK)
centred(d, 740, "creator bought none", 40, INK)
centred(d, 840, "we are watching the bots", 40, INK)
img.save(os.path.join(HERE, "coin.png"))
print("coin.png written")
