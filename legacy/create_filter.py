import sys

from PIL import Image



if len(sys.argv) < 2:
    raise Exception('Usage: py create_filter.py {IMAGE_PATH}')

path = sys.argv[1]

file_name = '.'.join(path.split('/')[-1].split('\\')[-1].split('.')[:-1])
out_path = 'filters/' + file_name + '_filter.png'


img = Image.open(path)
# w, h = img.size
img.save(out_path)
# img.close()


# img = Image.new('1', (w, h), 0)
# img.save(out_path)