# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from vpython import compound, vertex, quad, vector

################################################
# Read tif
fname = 'Rome-90m-DEM.tif'
Z = plt.imread(fname)
Z = Z[:, :, 0]
Z = np.transpose(Z)
# Z = np.zeros_like(Z) + 10

################################################
# Fetch info
shape = Z.shape
max_value, min_value = np.max(Z), np.min(Z)

# Parse points
_idx = dict()
_pos = dict()
points = []
colors = []
points_n = []

# Down sampling
D = 5
idx = 0
for j in range(D, shape[0]-D, D):
    for k in range(D, shape[1]-D, D):
        print(idx)
        if idx % 1000 == 0:
            print(idx)

        # Z[j][k] = j + k

        vc = vector(j, k, Z[j][k])
        dn = vector(j-1, k, Z[j-1][k]) - vc
        ds = vector(j+1, k, Z[j+1][k]) - vc
        dw = vector(j, k-1, Z[j][k-1]) - vc
        de = vector(j, k+1, Z[j][k+1]) - vc

        points.append(vc)
        points_n.append(dn.cross(dw)+dw.cross(ds)+ds.cross(de)+de.cross(dn))

        _c = (Z[j][k] - min_value) / (max_value - min_value) * 0.9 + 0.1
        _c = 0.5
        colors.append(vector(_c, _c, _c))

        _idx[(j, k)] = idx
        _pos[idx] = (j, k)
        idx += 1

info = dict(
    fname=fname,
    shape=Z.shape,
    max_value=max_value,
    min_value=min_value,
    num_points=idx-1
)

print('-' * 80)
print('Basic info:')
pprint(info)

################################################
# Draw ground
c = vector(0.2, 0.2, 0.2)
v0 = vertex(pos=vector(0, 0, 0), color=c)
v1 = vertex(pos=vector(shape[0], 0, 0), color=c)
v2 = vertex(pos=vector(shape[0], shape[1], 0), color=c)
v3 = vertex(pos=vector(0, shape[1], 0), color=c)
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
todo = []
for _x in range(D, shape[0]-2*D, D):
    for _y in range(D, shape[1]-2*D, D):
        if len(xys) < n:
            xys.append((_x, _y))
        else:
            draw_compound(xys)
            xys = []
for t in todo:
    print(t)
    t.start()
draw_compound(xys)

# compound([quad(vs=[vertex(pos=points[_idx[(x+dx, y+dy)]],
#                           normal=points_n[_idx[x+dx, y+dy]],
#                           color=vector(0.5, 0.7, 0.6))
#                    for dx, dy in [(0, 0), (D, 0), (D, D), (0, D)]])
#           for x in range(0, shape[0]-2*D, D)
#           for y in range(0, shape[1]-2*D, D)])


print('done.')
