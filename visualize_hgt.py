# coding: utf-8

import gzip
import numpy as np
from mayavi import mlab

# data from https://s3.amazonaws.com/elevation-tiles-prod/skadi/N41/N41E012.hgt.gz
gzfilename = 'N41E012.hgt.gz'

with gzip.open(gzfilename, 'rb') as f:
    file_content = f.read()
data = np.frombuffer(file_content, '>i2')

data.shape = (3601, 3601)

# Cut data from N41.8 E21.35 to N42 to E12.65
data = data[: int((1-0.8)*3600):, int((1-0.65)*3600):int((1-0.35)*3600)]
data = data.astype(np.float32)

# Draw data
mlab.figure(size=(400, 320), bgcolor=(0.16, 0.28, 0.46))
mlab.surf(data, colormap='gist_earth', warp_scale=0.2,)

# Clear data
del data

# mlab show
mlab.view(-5.9, 83, 570, [5.3, 20, 238])

print('Showing.')
mlab.show()
