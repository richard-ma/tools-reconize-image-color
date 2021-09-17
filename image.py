#!/usr/bin/env python

from PIL import Image
from collections import Counter
from pprint import pprint


def load_image(filename):
    im = Image.open(filename)
    width, height = im.size

    pixels = list()
    for x in range(width):
        for y in range(height):
            pixel = im.getpixel((x, y))
            pixels.append(pixel)

    return Counter(pixels)


if __name__ == "__main__":
    filename = "./test/images/black_0305_1024x1024@2x.jpg"
    data = load_image(filename)
    pprint(data)
