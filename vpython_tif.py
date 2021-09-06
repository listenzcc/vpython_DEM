# -*- coding: utf-8 -*-

import cv2
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from vpython import compound, vertex, quad, vector

# Down sampling
D = 5

################################################
# Read tif
fname = 'Shanghai-90m-DEM.tif'
Z = cv2.imread(fname).astype('int')[:-200, 200:-100, 0]
# fname = 'Rome-90m-DEM.tif'
# Z = plt.imread(fname).astype('int')[:, :, 0]
Z = np.transpose(Z)
Z = signal.convolve2d(Z, np.ones([D, D])) / D / D
shape = Z.shape

# r2 = (min(shape)/3) ** 2
# for j in range(shape[0]):
#     for k in range(shape[1]):
#         Z[j][k] = 0
#         d2 = (j-shape[0]/2)**2 + (k-shape[1]/2)**2
#         if d2 < r2:
#             Z[j][k] = (r2-d2) ** 0.5

################################################
# Fetch info
max_value, min_value = np.median(Z)*2, np.min(Z)

# Parse points
_idx = dict()
_pos = dict()
points = []
colors = []
points_n = []


idx = 0
center = vector(shape[0]/2, shape[1]/2, 0)
for j in range(D, shape[0]-D, D):
    for k in range(D, shape[1]-D, D):
        if idx % 10000 == 0:
            print(idx)

        vc = vector(j, k, Z[j][k])
        dn = vector(j-1, k, Z[j-1][k]) - vc
        ds = vector(j+1, k, Z[j+1][k]) - vc
        dw = vector(j, k-1, Z[j][k-1]) - vc
        de = vector(j, k+1, Z[j][k+1]) - vc

        points.append(vc - center)
        points_n.append(dn.cross(dw)+dw.cross(ds)+ds.cross(de)+de.cross(dn))

        _c = (Z[j][k] - min_value) / \
            (max_value - min_value + 0.001) * 0.9 + 0.1
        _c = min(_c, 1)
        colors.append(vector(_c, _c, _c))

        _idx[(j, k)] = idx
        _pos[idx] = (j, k)
        idx += 1

info = dict(
    fname=fname,
    shape=Z.shape,
    max_value=max_value,
    min_value=min_value,
    num_points=idx-1,
    center=center
)

print('-' * 80)
print('Basic info:')
pprint(info)

################################################
# Draw ground
color = vector(0.2, 0.2, 0.2)
v0 = vertex(pos=vector(0, 0, 0) - center, color=color)
v1 = vertex(pos=vector(shape[0], 0, 0) - center, color=color)
v2 = vertex(pos=vector(shape[0], shape[1], 0) - center, color=color)
v3 = vertex(pos=vector(0, shape[1], 0) - center, color=color)
quad(vs=[v0, v1, v2, v3])


# Draw quad using vertex in xys
def draw_compound(xys):
    return compound([quad(vs=[vertex(pos=points[_idx[(x+dx, y+dy)]],
                                     normal=points_n[_idx[x+dx, y+dy]],
                                     color=colors[_idx[(x+dx, y+dy)]])
                              for dx, dy in [(0, 0), (D, 0), (D, D), (0, D)]])
                     for x, y in xys])


# Draw surface
n = 10000
xys = []
for _x in range(D, shape[0]-2*D, D):
    for _y in range(D, shape[1]-2*D, D):
        if len(xys) < n:
            xys.append((_x, _y))
        else:
            draw_compound(xys)
            xys = []
draw_compound(xys)

print('done.')
