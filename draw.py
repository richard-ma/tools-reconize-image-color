#!/usr/bin/env python

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import image

if __name__ == "__main__":
    filename = "./test/images/black_0305_1024x1024@2x.jpg"
    data = image.load_image(filename)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    total = len(list(data.keys()))
    counter = 0
    for point in list(data.keys()):
        ax.scatter(*point)
        print("%d/%d" % (counter, total))
        counter += 1
    plt.show()
