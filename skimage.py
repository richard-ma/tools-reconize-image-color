#!/usr/bin/env python

import skimage
from imageio import imread
import skimage
import matplotlib.pyplot as plt

if __name__ == '__main__':
    img = imread("test/images/black_0305_1024x1024@2x.jpg")
    plt.imshow(img)
    plt.show()
    print(skimage.__version__)

