# -*- coding: utf8 -*-

import scipy as sp

data_path = '../ch01/data/web_traffic.tsv'

# 预处理数据
data = sp.genfromtxt(data_path, delimiter="\t")
x = data[:, 0]
y = data[:, 1]
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

# 通过图像观察数据
import matplotlib.pyplot as plt
plt.scatter(x, y, s=10)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/Hour")
plt.xticks([w*7*24 for w in range(10)], ['week %i' % w for w in range(10)])
plt.autoscale(tight=True)
plt.grid(True, linestyle='-', color='0.75')
plt.show()
