from glob import glob

from PIL import Image

from color_table import color_table

THUMBNAIL_WIDTH = 200
THUMBNAIL_HEIGHT = 200
REDUCE_BACKGROUND = 0.60
DIVIDE = 5


def get_factor(n):
    if 255 % n == 0:
        return 255 // n
    else:
        raise Exception("Cannot Divide by n: %d", n)


def recreate_color_table(f):
    return {tuple((e // f) * f for e in v): k for k, v in color_table.items()}


def get_color(filename, step=2):
    f = get_factor(DIVIDE)

    with Image.open(filename) as img:
        d = dict()
        img.thumbnail([THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT])
        px = img.load()
        bg = tuple((e // f) * f for e in px[0, 0])
        for w in range(0, img.width, step):
            for h in range(0, img.height, step):
                p = tuple((e // f) * f for e in px[w, h])
                if p not in d.keys():
                    d[p] = 1
                else:
                    d[p] += 1
        d[bg] *= (1 - REDUCE_BACKGROUND)
        sorted_d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        #print(sorted_d)
    return sorted_d[0][0], color2name(sorted_d[0][0])


def color2name(color):
    f = get_factor(DIVIDE)

    ct = recreate_color_table(f)

    if color in ct.keys():
        return ct[color]

    return None


if __name__ == "__main__":
    filenames = [
        "./test/images/12b-9661-10340.jpg",
    ]

    import os
    import shutil

    i = 1
    for filename in glob('C:\\Users\\richa\\Desktop\\images\\*.jpg'):
    #for filename in filenames:
        color_code, color_name = get_color(filename)
        print("[%06d] %s -- %s" % (i, color_name, filename))
        #print(color_code, color_name)
        #if color_name is None:
            #print(color_code, filename)

        # 分类存放
        new_dir = str(color_code)
        path, file = os.path.split(filename)
        if not os.path.exists(os.path.join(path, new_dir)):
            os.mkdir(os.path.join(path, new_dir))
        shutil.copyfile(filename, os.path.join(path, new_dir, file))
        i += 1
