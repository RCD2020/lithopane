from random import randint

from PIL import Image


# colors = [[], [], []]
# for x in range(256):
#     colors[0].append((255, x, 0))
#     colors[1].append((255, 0, x))

# for x in range(256*2):
#     colors[2].append((255, x//2, x//2))


# img1 = Image.new('RGB', (256, 10), (0, 0, 0))
# pixels1 = img1.load()

# for x in range(256):
#     for y in range(5):
#         pixels1[x, y] = colors[0][x]
#         pixels1[x, y+5] = colors[1][x]

# img1.save('palette_ref.png')


# img2 = Image.new('RGB', (512, 10), (0,0,0))
# pixels2 = img2.load()

# for x in range(512):
#     for y in range(10):
#         pixels2[x, y] = colors[2][x]

# img2.save('palette_ref2.png')


# img3 = Image.new('RGB', (256, 256), (0,0,0))
# pixels3 = img3.load()

# for x in range(256):
#     for y in range(256):
#         pixels3[x, y] = (x, y, 0)

# img3.save('palette_ref3.png')



# img4 = Image.new('RGB', (256, 256), (0,0,0))
# pixels4 = img4.load()

# for x in range(256):
#     for y in range(256):
#         pixels4[x, y] = (x, 0, y)

# img4.save('palette_ref4.png')


# img5 = Image.new('RGB', (256, 256), (0,0,0))
# pixels5 = img5.load()

# for x in range(256):
#     for y in range(256):
#         pixels5[x, y] = (x, y, y)

# img5.save('palette_ref5.png')


# img = Image.new('RGB', (256, 256), (0,0,0))
# pixels = img.load()

# for x in range(256):
#     for y in range(256):
#         if ((y or x) and x / (x+y) > .8):
#             pixels[x, y] = (x, y, y)

# img.save('palette_ref6.png')




# img = Image.new('RGB', (256, 256), (0,0,0))
# pixels = img.load()

# for x in range(256):
#     for y in range(256):
#         if x > 128 and y > 128:
#             pixels[x,y] = (x, y, 0)

# img.save('palette_ref7.png')


# img = Image.new('RGB', (256, 256), (0,0,0))
# pixels = img.load()

# for x in range(256):
#     for y in range(256):
#         if (x or y) and x*2 / (x*2 + y) > .8:
#             pixels[x,y] = (x, x, y)

# img.save('palette_ref8.png')

def randColor():
    return (randint(0, 255), randint(0,255), randint(0, 255))


def isRed(r, g, b):
    return (
        g and b
        and r / (g + b + r) > .3
        and r / (g + r) > .6
        and r / (b + r) > .6
    )



SIZE = 256

img = Image.new('RGB', (SIZE, SIZE), (0,0,0))
pixels = img.load()

for x in range(SIZE):
    for y in range(SIZE):
        color = randColor()
        while (not isRed(*color)):
            color = randColor()
        
        pixels[x, y] = color

img.save('palette_ref9.png')