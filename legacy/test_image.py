from PIL import Image
from random import randint

img = Image.new('RGB', (2, 2), (0,0,0))

# pixels = img.load()

# w, h = img.size

# # for x in range(w):
# #     for y in range(h):
# #         pixels[x,y] = randint(0,255)

img.save('out.png')