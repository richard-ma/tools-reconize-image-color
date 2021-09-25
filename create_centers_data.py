#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import matplotlib
import json
import numpy as np

matplotlib.use('TKAgg')
from imageio import imread
from sklearn import preprocessing
from sklearn.cluster import KMeans


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def process(self):
        pass


class MyApp(App):
    @staticmethod
    def vector_distance(v1, v2):
        assert len(v1) == len(v2)
        ans = 0
        for i in range(len(v1)):
            ans += v1[i] - v2[i]
        return ans

    def process(self):
        n_colors_range = range(3, 10+1) # 3-10
        image_dir = 'test/images'
        data = list()
        for filename in os.listdir(image_dir):
            da = dict()
            da['filename'] = filename

            image_filename = os.path.join(image_dir, filename)
            img = imread(image_filename)
            w, h, d = img.shape
            assert d == 3
            pixel_len = w * h
            img = img.reshape(pixel_len, d)  # flatten array

            image_sample_array = np.array(img, dtype=np.float64)
            #image_sample_array = preprocessing.scale(image_sample_array)

            for n_colors in n_colors_range:
                kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample_array)
                centers = [[int(v) for v in _] for _ in kmeans.cluster_centers_]
                print(centers)

                da['%d colors centers' % (n_colors)] = json.dumps(centers)

            data.append(da)  # add line

        output_filename = 'data/3_10_colors_centers.csv'

        fieldnames = list(data[0].keys())
        # pprint(fieldnames)
        self.writeCsvFromDict(output_filename, data, fieldnames=fieldnames)


if __name__ == "__main__":
    app = MyApp()
    app.run()
