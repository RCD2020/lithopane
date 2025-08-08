import colorsys
import json

from PIL import Image


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


IMG_PATH = 'images/superman_red_blue.jpg'
COLOR_MAP_PATH = 'color/super_red_blue_color_map.json'


img = Image.open(IMG_PATH)
color_map = load_colors(COLOR_MAP_PATH)

w, h = img.size
pixels = img.load()


for x in range(w):
    for y in range(h):
        color = resolve_rgb(pixels[x, y], color_map)
        pixels[x, y] = tuple(color['rgb'])


img.save('palette_ref16.png')