#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import matplotlib
import json
import math
import numpy as np
from time import time

matplotlib.use('TKAgg')
from imageio import imread
from sklearn.utils import shuffle
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
    def distance(self, v1, v2):
        assert len(v1) == len(v2)
        z = zip(v1, v2)
        ans = 0
        for pair in z:
            ans += (pair[0] - pair[1]) ** 2
        return math.sqrt(ans)

    def center_score(self, c1, c2):
        assert len(c1) == len(c2)
        z = zip(c1, c2)

        ans = 0
        for pair in z:
            ans += self.distance(*pair)

        return ans

    def process(self):
        n_colors_range = range(3, 10+1)
        percent_range = range(5, 50 + 1, 5)
        standered_filename = 'data/3_10_colors_centers.csv'
        standered_data = self.readCsvToDict(standered_filename)

        image_dir = 'test/images'
        data = list()
        for input_data in standered_data:
            filename = input_data['filename']
            image_filename = os.path.join(image_dir, filename)
            img = imread(image_filename)
            w, h, d = img.shape
            assert d == 3
            pixel_len = w * h
            img = img.reshape(pixel_len, d)  # flatten array
            img = np.array(img, dtype=np.float64)

            for percent_int in percent_range:
                percent = percent_int / 100  # 转换成百分数
                da = dict()

                for n_colors in n_colors_range:
                    print("Fitting model on a small sub-sample(%d%%) of the %d colors" % (percent_int, n_colors))
                    t0 = time()

                    # 训练模型并使用模型进行预测
                    image_sample_array = shuffle(img, random_state=0)[:int(len(img) * percent)]  # 重新混洗后选择前1000个像素点
                    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample_array)  # 使用KMeans算法进行聚类
                    training_centers = [[int(v) for v in _] for _ in kmeans.cluster_centers_]
                    training_centers = sorted(training_centers)

                    t = time() - t0
                    print("Training done in %0.3fs: %s" % (t, training_centers))

                    # 读取标准数据
                    title = '%d colors centers' % (n_colors)
                    standered_centers = json.loads(input_data[title])
                    standered_centers = sorted(standered_centers)
                    print("Reading standered centers: %s" % (standered_centers))

                    # 评价模型
                    ans = self.center_score(training_centers, standered_centers)

                    # 记录评价数据
                    da['filename'] = filename
                    da['sample percents'] = percent_int
                    da['%d colors centers' % (n_colors)] = str(ans) + ' in ' + str(t) + 'seconds'

                data.append(da)  # add line

        output_filename = 'data/3_10_find_sample_rate.csv'

        fieldnames = list(data[0].keys())
        # pprint(fieldnames)
        self.writeCsvFromDict(output_filename, data, fieldnames=fieldnames)


if __name__ == "__main__":
    app = MyApp()
    app.run()
