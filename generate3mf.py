import sys
import os

from PIL import Image


MAX_DIM = 50
BACKING = .25
COLOR_BOTTOM_FACE = True


path = 'images/Superman Logo.png'
out_path = 'Reference/3D/Objects/object_1.model'
vertexes = []
vertex_map = {}
tris = []
colors = {
    'white': {'id': None, 'h_modi': 1},
    'red': {'id': '8', 'h_modi': .7},
    'yellow': {'id': '0C', 'h_modi': .9},
    'blue': {'id': '1C', 'h_modi': .1},
    'light_blue': {'id': '2C', 'h_modi': .3}
}
def color_map(rgb):
    r, g, b = rgb[0:3]

    def isRed(r, g, b):
        return (
            (g or b)
            and r / (g + b + r) > .3
            and r / (g + r) > .6
            and r / (b + r) > .6
        )
    
    def isYellow(r, g, b):
        return (
            (r or g or b)
            and (r + g) / (r + g + b) > .8
            and r > 128
            and g > 128
        )
    
    def isBlue(r, g, b):
        return (
            (g or r)
            and b / (g + b + r) > .3
            and b / (g + b) > .6
            and b / (r + b) > .6
        )

    
    if isRed(r, g, b):
        return colors['red']
    
    if isYellow(r, g, b):
        return colors['yellow']
    
    if isBlue(r, g, b):
        return colors['blue']
    

    return colors['white']


def get_vertex(vert):
    vert = [f'{x:.4f}' for x in vert]

    pointer = vertex_map

    for i in range(len(vert)):

        if vert[i] not in pointer:
            if i == 2:
                pointer[vert[i]] = len(vertexes)
                vertexes.append(vert)
            else:
                pointer[vert[i]] = {}

        pointer = pointer[vert[i]]

    return pointer
    



img = Image.open(path)

w, h   = img.size
s_modi = MAX_DIM / max(w, h)
pixels = img.load()
y_scale = 3


print('Reading Image...')
i = 1
for x in range(w-1):
    for y in range(h-1):
        x1 = x * s_modi
        y1 = y * s_modi

        print(f'\r{i}/{(w-1)*(h-1)}', end='')

        yh = [[], []]
        for p1 in range(2):
            for p2 in range(2):
                color = color_map(pixels[x+p1, y+p2])

                yh[p1].append(
                    (
                        -(sum(pixels[x+p1, y+p2]) / len(pixels[x, y]) / 255) + 1
                    ) * y_scale * color['h_modi']
                )

        v1 = get_vertex((x1+s_modi, yh[1][0], y1       ))
        v2 = get_vertex((x1       , yh[0][0], y1       ))
        v3 = get_vertex((x1       , yh[0][1], y1+s_modi))
        v4 = get_vertex((x1+s_modi, yh[1][1], y1+s_modi))

        v5 = get_vertex((x1       , -BACKING, y1       ))
        v6 = get_vertex((x1       , -BACKING, y1+s_modi))
        v7 = get_vertex((x1+s_modi, -BACKING, y1+s_modi))
        v8 = get_vertex((x1+s_modi, -BACKING, y1       ))

        

        tris.append((v1, v2, v3, color['id']))
        tris.append((v4, v1, v3, color['id']))

        if (not COLOR_BOTTOM_FACE):
            color = colors['white']

        tris.append((v5, v8, v6, color['id']))
        tris.append((v8, v7, v6, color['id']))

        if x == 0:
            tris.append((v5, v6, v2, color['id']))
            tris.append((v2, v6, v3, color['id']))
        
        if x+2 == w:
            tris.append((v7, v8, v1, color['id']))
            tris.append((v7, v1, v4, color['id']))

        if y == 0:
            tris.append((v8, v5, v2, color['id']))
            tris.append((v8, v2, v1, color['id']))

        if y+2 == h:
            tris.append((v6, v7, v3, color['id']))
            tris.append((v3, v7, v4, color['id']))




        i += 1

# print(vertex_map)
# print('\n', len(vertexes))
# print(w*h)
# print('\n', tris)

print('\nImage Processed!')

print('Writing file...')

with open(out_path, 'w') as f:
    f.write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        '<model unit="millimeter" '
        'xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
        'requiredextensions="p">\n'

        '<metadata name="BambuStudio:3mfVersion">1</metadata>\n'

        '<resources>\n'

        '<object id="1" p:UUID="00010000-81cb-4c03-9d28-80fed5dfa1dc" '
        'type="model">\n'

        '<mesh>\n'
    )


    print('Writing Vertices...')
    f.write('<vertices>\n')
    i_v = 1
    for x in vertexes:
        print(f'\r{i_v}/{len(vertexes)}', end='')

        f.write(f'<vertex x="{x[0]}" y="{x[1]}" z="{x[2]}"/>\n')

        i_v += 1
    f.write('</vertices>\n')
    
    print('\nSuccessfully wrote vertices!')


    print('Writing Triangles...')
    f.write('<triangles>\n')
    i_t = 1
    for x in tris:
        print(f'\r{i_t}/{len(tris)}', end='')

        tri = f'<triangle v1="{x[0]}" v2="{x[1]}" v3="{x[2]}" '
        
        if len(x) == 4 and x[3]:
            tri += 'paint_color="' + x[3] + '"'
        
        tri += '/>\n'


        f.write(tri)

        i_t += 1
    f.write('</triangles>\n')

    print('\nSuccessfully wrote triangles!')



    f.write(
        '</mesh>\n'
        '</object>\n'
        '</resources>\n'
        '<build/>\n'
        '</model>'
    )

print('Successfully wrote file!')
