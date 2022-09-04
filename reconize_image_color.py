import os
import csv
from PIL import Image
from color_table import color_table

THUMBNAIL_WIDTH = 200
THUMBNAIL_HEIGHT = 200
REDUCE_BACKGROUND = 0.45
DIVIDE = 5
BG_COORDINATE = (5, 5)


def get_factor(n):
    if 255 % n == 0:
        return 255 // n
    else:
        raise Exception("Cannot Divide by n: %d", n)


def recreate_color_table(f):
    return {tuple((e // f) * f for e in v): k for k, v in color_table.items()}


def get_color(filename, step=1):
    f = get_factor(DIVIDE)

    with Image.open(filename) as img:
        d = dict()
        img.thumbnail([THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT])
        px = img.load()
        bg = tuple((e // f) * f for e in px[BG_COORDINATE])
        for w in range(0, img.width, step):
            for h in range(0, img.height, step):
                p = tuple((e // f) * f for e in px[w, h])
                if p not in d.keys():
                    d[p] = 1
                else:
                    d[p] += 1
        d[bg] *= (1 - REDUCE_BACKGROUND)
        sorted_d = sorted(d.items(), key=lambda kv: [kv[1], kv[0]], reverse=True)
    return sorted_d[0][0]


def color2name(color):
    f = get_factor(DIVIDE)

    ct = recreate_color_table(f)

    if color in ct.keys():
        return ct[color]

    return None


if __name__ == "__main__":
    csv_filename = input("请拖动csv文件到本窗口，然后确保已经把所有待识别的图片放置在和csv同目录下的名为images目录中，然后回车确认")
    if len(csv_filename) == 0:
        csv_filename = "test/product_data_color.csv"

    working_dir, fn = os.path.split(csv_filename)
    output_csv_filename = os.path.join(working_dir, 'new_' + fn)

    output_csv_file = open(output_csv_filename, 'w+', encoding='GBK', newline='')

    with open(csv_filename, 'r+', encoding='GBK') as csv_file:
        line_no = 1
        reader = csv.DictReader(csv_file)
        for row in reader:
            if line_no == 1:
                writer = csv.DictWriter(output_csv_file, fieldnames=row.keys())
                writer.writeheader()

            filename = os.path.join(working_dir, 'images', row['images'])
            if os.path.exists(filename):
                color_code = get_color(filename)
                color_name = color2name(color_code)
                print("[%06d] %s -- %s" % (line_no, color_name, filename))

                if color_name is None:
                    color_name += color_code

                row['color'] = color_name
            else:
                print("[%06d] %s -- %s" % (line_no, 'nofound', filename))
                row['nofound'] = 'no found'

            writer.writerow(row)

            # 分类存放
            #import os
            #import shutil
            #import pprint

            #new_dir = str(color_code)
            #path, file = os.path.split(filename)
            #if not os.path.exists(os.path.join(path, new_dir)):
            #    os.mkdir(os.path.join(path, new_dir))
            #shutil.copyfile(filename, os.path.join(path, new_dir, file))

            line_no += 1

    output_csv_file.close()
