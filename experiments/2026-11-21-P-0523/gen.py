"""Draw a synthetic four-view pixel sheet (top, side, front, back in one row) of a small car:
24 long, 12 wide, 10 tall, a body 5 high and a cabin on top. Usage: gen.py OUT.png"""
import sys
from PIL import Image, ImageDraw

L, W, H = 24, 12, 10
GAP = 12  # the slicer dilates the mask before finding views; 2 px merged all four (first run)
sheet = Image.new("RGBA", (L + GAP + L + GAP + W + GAP + W, max(W, H)), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
RED, DARK, GLASS, LIGHT = (200, 40, 40, 255), (90, 20, 20, 255), (120, 180, 220, 255), (255, 230, 120, 255)

# top: body with a cabin roof in the middle
x0 = 0
d.rectangle([x0, 0, x0 + L - 1, W - 1], fill=RED)
d.rectangle([x0 + 7, 2, x0 + 16, W - 3], fill=DARK)
# side: body 5 high on the bottom, cabin 5 high in the middle, wheels
x0 = L + GAP
d.rectangle([x0, H - 5, x0 + L - 1, H - 1], fill=RED)
d.rectangle([x0 + 7, 0, x0 + 16, H - 6], fill=GLASS)
d.rectangle([x0 + 3, H - 2, x0 + 6, H - 1], fill=(20, 20, 20, 255))
d.rectangle([x0 + 17, H - 2, x0 + 20, H - 1], fill=(20, 20, 20, 255))
# front and back: body full width, cabin narrower
for k, lamp in ((0, LIGHT), (1, (255, 60, 60, 255))):
    x0 = 2 * (L + GAP) + k * (W + GAP)
    d.rectangle([x0, H - 5, x0 + W - 1, H - 1], fill=RED)
    d.rectangle([x0 + 2, 0, x0 + W - 3, H - 6], fill=GLASS)
    d.rectangle([x0 + 1, H - 4, x0 + 2, H - 3], fill=lamp)
    d.rectangle([x0 + W - 3, H - 4, x0 + W - 2, H - 3], fill=lamp)
sheet.save(sys.argv[1])
print("sheet", sheet.size)
