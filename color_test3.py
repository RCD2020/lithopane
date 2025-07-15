from PIL import Image

import json
import colorsys


COLOR_MAP_PATH = 'color/super_color_map_2.json'
FILTER_PATH    = 'filters/super poster 3 resize_filter.png'


def load_colors(path):
    with open(path, 'r') as f:
        color_map = json.loads(f.read())
    
    colors = []
    for x in color_map['colors']:
        with open(x['path'], 'r') as f:
            color = json.loads(f.read())
            color['id'] = x['id']

            colors.append(color)

    return colors


def resolve_rgb(rgb, color_map):
    h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    def resolve_filter(filter, h, l, s):
        name = filter['type']

        if name == 'or':
            evaluation = resolve_filter(filter['filters'][0], h, l, s)

            for x in filter['filters'][1:]:
                evaluation = evaluation or resolve_filter(x, h, l, s)

            return evaluation
    
        type_mapping = {
            'hue': h,
            'lightness': l,
            'saturation': s
        }
        operation_mapping = {
            '<': lambda a, b : a < b,
            '>': lambda a, b : a > b
        }

        return operation_mapping[filter['operation']](
            type_mapping[name], filter['value']
        )

    for color in color_map:
        evaluation = resolve_filter(color['filters'][0], h, l, s)
        
        for filter in color['filters'][1:]:
            evaluation = evaluation and resolve_filter(filter, h, l, s)
        
        if evaluation:
            return color
    
    return {
        'id': None,
        'height_modifier': 1.0,
        'rgb': [255, 255, 255]
    }


def load_filter(filter_path):
    img = Image.open(filter_path)
    w, h = img.size

    filter = [[1] * h for _ in range(w)]

    pixels = img.load()

    for x in range(w):
        for y in range(h):
            if (pixels[x, y][0:3] == (0,0,0)):
                filter[x][y] = 0

    return filter

color_map  = load_colors(COLOR_MAP_PATH)
filter_map = load_filter(FILTER_PATH)
# print(resolve_rgb((10, 20, 30), color_map))


img = Image.open('images/super poster 3 resize.jpg')
pixels = img.load()
w, h = img.size

for x in range(w):
    for y in range(h):
        if filter_map[x][y]:
            color = resolve_rgb(pixels[x,y], color_map)
        else:
            color = {'id': None}

        avg_color = int(sum(pixels[x,y]) / len(pixels[x,y]))

        if (color['id']):
            rgb = resolve_rgb(pixels[x,y][0:3], color_map)['rgb']
            rgb = [int(x * avg_color/255*3) for x in rgb]
            pixels[x,y] = tuple(rgb)
        else:
            pixels[x,y] = (avg_color, avg_color, avg_color)

img.save('palette_ref15.png')