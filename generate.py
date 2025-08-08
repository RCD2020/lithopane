import sys
import os
from zipfile import ZipFile
from tempfile import TemporaryFile
from uuid import uuid4
from datetime import datetime

from PIL import Image


MAX_DIM = 50
BACKING = .25


if (len(sys.argv) < 2):
    print(
        'Usage: generate.py {PATH OF IMAGE}\n'
        'Optional:\n'
        '   -d {DIMENSION OF LONGEST SIDE}'
    )
    exit()


path = sys.argv[1]

if (not os.path.isfile(path)):
    print(f'\033[31m"{path}" not found.\033[00m')
    exit()


dim_flag = False
for x in sys.argv[2:]:
    if dim_flag:
        try:
            MAX_DIM = int(x)
            dim_flag = False
        except:
            print(f'\033[31m"{x}" is an invalid value for MAX_DIM (-d)\033[00m')
            exit()

    if x == '-d':
        dim_flag = True


file_name = '.'.join(path.split('/')[-1].split('\\')[-1].split('.')[:-1])
file_name = file_name + f'_{MAX_DIM}mm'
out_path = file_name + '.3mf'

img = Image.open(path)
w, h   = img.size
s_modi = MAX_DIM / max(w, h)
pixels = img.load()
y_scale = 3

vertexes = []
vertex_map = {}
obj_uuid = uuid4()


def get_vertex(vert, f_model):
    vert = [f'{x:.4f}' for x in vert]

    pointer = vertex_map

    for i in range(len(vert)):

        if vert[i] not in pointer:
            if i == 2:
                pointer[vert[i]] = len(vertexes)
                vertexes.append(vert)

                f_model.write(
                    f'<vertex x="{vert[0]}" y="{vert[1]}" z="{vert[2]}"/>\n'.encode()
                )
            else:
                pointer[vert[i]] = {}

        pointer = pointer[vert[i]]

    return pointer


def tri_bytes(v1, v2, v3):
    return f'<triangle v1="{v1}" v2="{v2}" v3="{v3}" />\n'.encode()



print('Processing...')
with TemporaryFile() as f_model:
    f_model.write((
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        '<model unit="millimeter" '
        'xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
        'requiredextensions="p">\n'

        '<metadata name="BambuStudio:3mfVersion">1</metadata>\n'

        '<resources>\n'

        f'<object id="1" p:UUID="{obj_uuid}" '
        'type="model">\n'

        '<mesh>\n'

        '<vertices>\n'
    ).encode())

    with TemporaryFile() as f_tris:
        f_tris.write('<triangles>\n'.encode())

        i = 1
        for x in range(w-1):
            for y in range(h-1):
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
                
                v1 = get_vertex((x1+s_modi, y1       , yh[1][0]), f_model)
                v2 = get_vertex((x1       , y1       , yh[0][0]), f_model)
                v3 = get_vertex((x1       , y1+s_modi, yh[0][1]), f_model)
                v4 = get_vertex((x1+s_modi, y1+s_modi, yh[1][1]), f_model)

                v5 = get_vertex((x1       , y1       , -BACKING), f_model)
                v6 = get_vertex((x1       , y1+s_modi, -BACKING), f_model)
                v7 = get_vertex((x1+s_modi, y1+s_modi, -BACKING), f_model)
                v8 = get_vertex((x1+s_modi, y1       , -BACKING), f_model)


                f_tris.write(tri_bytes(v1, v2, v3))
                f_tris.write(tri_bytes(v4, v1, v3))

                f_tris.write(tri_bytes(v5, v8, v6))
                f_tris.write(tri_bytes(v8, v7, v6))

                if x == 0:
                    f_tris.write(tri_bytes(v5, v6, v2))
                    f_tris.write(tri_bytes(v2, v6, v3))
                
                if x+2 == w:
                    f_tris.write(tri_bytes(v7, v8, v1))
                    f_tris.write(tri_bytes(v7, v1, v4))

                if y == 0:
                    f_tris.write(tri_bytes(v8, v5, v2))
                    f_tris.write(tri_bytes(v8, v2, v1))

                if y+2 == h:
                    f_tris.write(tri_bytes(v6, v7, v3))
                    f_tris.write(tri_bytes(v3, v7, v4))


                i += 1
        

        f_tris.write('</triangles>\n'.encode())

        f_model.write('</vertices>\n'.encode())

        f_tris.seek(0)

        f_model.write(f_tris.read())

    f_model.write((
        '</mesh>\n'
        '</object>\n'
        '</resources>\n'
        '<build/>\n'
        '</model>'
    ).encode())

    f_model.seek(0)


    with ZipFile(out_path, 'w') as f:
        f.writestr('_rels/.rels', (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
            '</Relationships>'
        ))

        f.writestr('3D/_rels/3dmodel.model.rels', (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            ' <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
            '</Relationships>'
        ))

        f.writestr('3D/Objects/object_1.model', f_model.read())
        
        f.writestr('3D/3dmodel.model', (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n'
            ' <metadata name="Application">BambuStudio-02.01.01.52</metadata>\n'
            ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
            ' <metadata name="Copyright"></metadata>\n'
            f' <metadata name="CreationDate">{datetime.now().strftime("%Y-%m-%d")}</metadata>\n'
            ' <metadata name="Description">Model generated using https://github.com/RCD2020/lithopane .</metadata>\n'
            ' <metadata name="Designer"></metadata>\n'
            ' <metadata name="DesignerCover"></metadata>\n'
            ' <metadata name="DesignerUserId"></metadata>\n'
            ' <metadata name="License"></metadata>\n'
            f' <metadata name="ModificationDate">{datetime.now().strftime("%Y-%m-%d")}</metadata>\n'
            ' <metadata name="Origin">https://github.com/RCD2020/lithopane</metadata>\n'
            f' <metadata name="Title">{file_name}</metadata>\n'
            ' <resources>\n'
            f'  <object id="2" p:UUID="{uuid4()}" type="model">\n'
            '   <components>\n'
            f'    <component p:path="/3D/Objects/object_1.model" objectid="1" p:UUID="{uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n'
            '   </components>\n'
            '  </object>\n'
            ' </resources>\n'
            f' <build p:UUID="{uuid4()}">\n'
            f'  <item objectid="2" p:UUID="{uuid4()}" transform="1 0 0 0 1 0 0 0 1 128 128 1" printable="1"/>\n'
            ' </build>\n'
            '</model>\n'
        ))

        f.writestr('[Content_Types].xml', (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
            ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
            ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
            ' <Default Extension="png" ContentType="image/png"/>\n'
            ' <Default Extension="gcode" ContentType="text/x.gcode"/>\n'
            '</Types>'
        ))