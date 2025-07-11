from PIL import Image
import numpy as np


MAX_DIM = 100
BACK_THICKNESS = .25



img = Image.open('images\IMG_5660 reszied.jpg')


def stringify(v):
    return f'{v[0]:.02f} {v[1]:.02f} {v[2]:.02f}'



def normal(x):
    return x


def invert(x):
    return 255 - x



func = invert


w, h = img.size
size_modifier = MAX_DIM / max(w, h)
pixels = img.load()
y_scale = 3

squares = []

print('Reading Image...')
i = 1
for x in range(w-1):
    for y in range(h-1):
        x_coord = x * size_modifier
        y_coord = y * size_modifier

        print(f'\r{i}/{(w-1)*(h-1)}', end='')
        squares.append((
            (x_coord, func(sum(pixels[x,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
            (x_coord+size_modifier, func(sum(pixels[x+1,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
            (x_coord, func(sum(pixels[x,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
        ))
        squares.append((
            (x_coord+size_modifier, func(sum(pixels[x+1,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
            (x_coord+size_modifier, func(sum(pixels[x+1,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier),
            (x_coord, func(sum(pixels[x,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
        ))

        if x == 0:
            squares.append((
                (x_coord, -BACK_THICKNESS, y_coord),
                (x_coord, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord, func(sum(pixels[x,y])/len(pixels[x,y]))/255 * y_scale, y_coord)
            ))
            squares.append((
                (x_coord, func(sum(pixels[x,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
                (x_coord, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord, func(sum(pixels[x,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
            ))
        
        if x+2 == w:
            squares.append((
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord+size_modifier, func(sum(pixels[x+1,y])/len(pixels[x,y]))/255 * y_scale, y_coord)
            ))
            squares.append((
                (x_coord+size_modifier, func(sum(pixels[x+1,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord+size_modifier, func(sum(pixels[x+1,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
            ))

        if y == 0:
            squares.append((
                (x_coord, -BACK_THICKNESS, y_coord),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord),
                (x_coord, func(sum(pixels[x,y])/len(pixels[x,y]))/255 * y_scale, y_coord)
            ))
            squares.append((
                (x_coord, func(sum(pixels[x,y])/len(pixels[x,y]))/255 * y_scale, y_coord),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord),
                (x_coord+size_modifier, func(sum(pixels[x+1,y])/len(pixels[x,y]))/255 * y_scale, y_coord)
            ))

        if y+2 == h:
            squares.append((
                (x_coord, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord, func(sum(pixels[x,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
            ))
            squares.append((
                (x_coord, func(sum(pixels[x,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier),
                (x_coord+size_modifier, -BACK_THICKNESS, y_coord+size_modifier),
                (x_coord+size_modifier, func(sum(pixels[x+1,y+1])/len(pixels[x,y]))/255 * y_scale, y_coord+size_modifier)
            ))
        
        squares.append((
            (x_coord, -BACK_THICKNESS, y_coord),
            (x_coord+size_modifier, -BACK_THICKNESS, y_coord),
            (x_coord, -BACK_THICKNESS, y_coord+size_modifier)
        ))
        squares.append((
            (x_coord+size_modifier, -BACK_THICKNESS, y_coord),
            (x_coord+size_modifier, -BACK_THICKNESS, y_coord+size_modifier),
            (x_coord, -BACK_THICKNESS, y_coord+size_modifier)
        ))

        i += 1

print('\nImage Processed!')


print('Generating STL...')

with open('out.stl', 'w') as f:

    f.write('solid test\n')

    i = 1
    total = len(squares)
    for square in squares:
        print(f'\r{i}/{total}', end='')

        p1 = np.array(square[0])
        p2 = np.array(square[1])
        p3 = np.array(square[2])

        v1 = p2 - p1
        v2 = p3 - p1

        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)


        f.write('    facet normal ' + stringify(normal) + '\n')
        f.write('        outer loop\n')
        f.write('            vertex ' + stringify(p1) + '\n')
        f.write('            vertex ' + stringify(p2) + '\n')
        f.write('            vertex ' + stringify(p3) + '\n')
        f.write('        endloop\n')
        f.write('    endfacet\n')

        i += 1
        

    f.write('endsolid test')


print('\nSTL generated!')
# print('Writing file...')


# with open('out.stl', 'w') as f:
#     f.write(text)

# print('Successfully written!')