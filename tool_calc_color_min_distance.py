#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import matplotlib
import json
import math
import numpy as np

matplotlib.use('TKAgg')
from imageio import imread


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
    def rgb_distance(v1, v2):
        assert len(v1) == len(v2)
        ans = 0
        for i in range(len(v1)):
            ans += (v1[i] - v2[i]) ** 2
        return math.sqrt(ans)

    @staticmethod
    def loads_rgb(s):
        return json.loads(s)

    def process(self):
        color_data_filename = './data/total_color_table.csv'

        data = self.readCsvToDict(color_data_filename)

        data = list(sorted(data, key=lambda x: x['rgb']))
        # print(data)

        ans = list()
        log = list()
        for idx in range(len(data)-1):
            v1, v2 = MyApp.loads_rgb(data[idx]['rgb']), MyApp.loads_rgb(data[idx+1]['rgb'])
            re = MyApp.rgb_distance(v1, v2)
            log.append([v1, v2, re])
            ans.append(re)

        output = min(ans)

        for l in log:
            if l[2] == output:
                print(l)


if __name__ == "__main__":
    app = MyApp()
    app.run()
