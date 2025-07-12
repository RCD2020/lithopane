import sys
import os

from PIL import Image


MAX_DIM = 50
BACK_THICKNESS = .25


path = 'images/Superman Logo.png'
out_path = '3mf_files/object_1.model'
vertexes = []
vertex_map = {}
tris = []

def get_vertex(vert):
    vert = [f'{x:.2f}' for x in vert]

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
for x in range(10):
    for y in range(5):
        x1 = x * s_modi
        y1 = y * s_modi

        print(f'\r{i}/{(w-1)*(h-1)}', end='')

        yh = [[], []]
        for p1 in range(2):
            for p2 in range(2):
                yh[p1].append(
                    (
                        -(sum(pixels[x+p1, y+p2]) / len(pixels[x, y]) / 255) + 1
                    ) * y_scale
                )

        v1 = (x1       , yh[0][0], y1       )
        v2 = (x1+s_modi, yh[1][0], y1       )
        v3 = (x1       , yh[0][1], y1+s_modi)
        v4 = (x1+s_modi, yh[1][1], y1+s_modi)

        v1 = get_vertex(v1)
        v2 = get_vertex(v2)
        v3 = get_vertex(v3)
        v4 = get_vertex(v4)

        tris.append((v1, v2, v3))
        tris.append((v2, v3, v4))


        i += 1

# print(vertex_map)
# print('\n', len(vertexes))
# print(w*h)
# print('\n', tris)