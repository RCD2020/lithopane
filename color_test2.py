import colorsys

from PIL import Image


SIZE = 100
SIZE_Y = int(SIZE/10)

img = Image.new('RGB', (SIZE, SIZE_Y), (0,0,0))
pixels = img.load()

for x in range(SIZE):
    r, g, b = colorsys.hls_to_rgb(1.0, x/SIZE, 0.0)
    
    for y in range(SIZE_Y):
        pixels[x, y] = (int(r*255), int(g*255), int(b*255))

img.save('palette_ref13.png')