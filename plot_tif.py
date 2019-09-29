# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

fname = 'Rome-90m-DEM.tif'
Z = plt.imread(fname)
shape = Z.shape

Z = Z[:, :, 0]

x = np.arange(shape[1])
y = np.arange(shape[0])
X, Y = np.meshgrid(x, y)

ax.plot_surface(X, Y, Z,
                rstride=1,
                cstride=1,
                cmap=cm.viridis)

plt.show()
