import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image, get_data_home
from sklearn.utils import shuffle
from time import time

print(get_data_home())

n_colors = 10

# Load the Summer Palace photo
img = load_sample_image("./test/images/black_0305_1024x1024@2x.jpg")

# Convert to floats instead of the default 8 bits integer coding. Dividing by
# 255 is important so that plt.imshow behaves works well on float data (need to
# be in the range [0-1])
# 将图片数组转换为64位浮点型数据，plt.Imshow函数处理浮点型更好一些。
china = np.array(img, dtype=np.float64) / 255

# Load Image and transform to a 2D numpy array.
w, h, d = original_shape = tuple(img.shape)
assert d == 3  # 确认颜色数据为rgb格式
image_array = np.reshape(img, (w * h, d))  # 将数组转换为一维数组，每个元素包括rgb数据

print("Fitting model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array)[:1000]  # 重新混洗后选择前1000个像素点
kmeans = KMeans(n_colors).fit(image_array_sample)  # 使用KMeans算法进行聚类
print("done in %0.3fs." % (time() - t0))

# Get labels for all points
print("Predicting color indices on the full image (k-means)")
t0 = time()
labels = kmeans.predict(image_array)  # 使用1000个像素点的聚类预测整幅图片
print("done in %0.3fs." % (time() - t0))

print(kmeans)
print(labels)
