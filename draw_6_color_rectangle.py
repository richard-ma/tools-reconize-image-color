#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import matplotlib
import json

matplotlib.use('TKAgg')
from imageio import imread
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


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
    def process(self):
        image_dir = 'test/images'
        input_filename = 'data/3_10_colors_centers.csv'
        data = self.readCsvToDict(input_filename)

        for d in data:
            fig, ax = plt.subplots()
            ax.set_title(d['filename'])
            ax.plot([0, 60], [0, 10])

            x = 0
            interval = 10
            colors = json.loads(d["6 colors centers"])
            for i in range(6):
                ax.add_patch(Rectangle(
                    (x, 0),
                    interval-1,
                    10,
                    #fc=[90/255, 90/255, 90/255],
                    fc=[c/255 for c in colors[i]],
                    fill=True))
                x += interval

            plt.show()


if __name__ == "__main__":
    app = MyApp()
    app.run()
