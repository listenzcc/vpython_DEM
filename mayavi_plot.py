# -*- coding: utf-8 -*-

import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt

# Read tif and change it into 2-D matrix
# fname = 'Shanghai-90m-DEM.tif'
fname = 'Rome-30m-DEM.tif'
Z = plt.imread(fname).astype(np.float32)
print('Raw shape is', Z.shape)
print(np.min(Z), np.max(Z))
data = Z[:, :, 0]

data += 1500

# 渲染地形hgt的数据data
mlab.figure(size=(400, 320), bgcolor=(0.16, 0.28, 0.46))
colormap = 'gist_earth'
mlab.surf(data, colormap=colormap, warp_scale=0.2,
          vmin=1200, vmax=1610)
# mlab.surf(data)

# 清空内存
del data
# 创建交互式的可视化窗口
mlab.view(-5.9, 83, 570, [5.3, 20, 238])
mlab.show()
