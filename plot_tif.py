# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

fname = 'Rome-30m-DEM.tif'
Z = plt.imread(fname)
shape = Z.shape
Z = Z[:, :, 0]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# x = np.arange(shape[1])
# y = np.arange(shape[0])
# X, Y = np.meshgrid(x, y)

# ax.plot_surface(X, Y, Z,
#                 rstride=1,
#                 cstride=1,
#                 cmap=cm.viridis)

fig, axes = plt.subplots(1, 1)
axes.imshow(Z)

plt.show()
