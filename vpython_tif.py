# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from vpython import compound, vertex, quad, vector, color

fname = 'Rome-90m-DEM.tif'
Z = plt.imread(fname)
shape = Z.shape
print(shape)
r = shape[1] / shape[0]

Z = Z[:, :, 0]
print(Z)

c = vector(0.2, 0.2, 0.2)
v0 = vertex(pos=vector(0, 0, 0), color=c)
v1 = vertex(pos=vector(shape[0], 0, 0), color=c)
v2 = vertex(pos=vector(shape[0], shape[1], 0), color=c)
v3 = vertex(pos=vector(0, shape[1], 0), color=c)
quad(vs=[v0, v1, v2, v3])

_idx = dict()
_pos = dict()

points = []
points_n = []

D = 10

idx = 0
for j in range(0, shape[0]-D, D):
    for k in range(0, shape[1]-D, D):
        points.append(vector(j, k, Z[j][k]))
        v10 = vector(j, k, Z[j][k])-vector(j+D, k, Z[j+D][k])
        v01 = vector(j, k, Z[j][k])-vector(j, k+D, Z[j][k+D])
        norm = v10.cross(v01)
        points_n.append(norm)
        _idx[(j, k)] = idx
        _pos[idx] = (j, k)
        idx += 1
print(len(points))

compound([quad(vs=[vertex(pos=points[_idx[(x+dx, y+dy)]],
                          normal=points_n[_idx[x+dx, y+dy]],
                          color=vector(1, 0.7, 0.2))
                   for dx, dy in [(0, 0), (D, 0), (D, D), (0, D)]])
          for x in range(0, shape[0]-2*D, D)
          for y in range(0, shape[1]-2*D, D)])


print('done.')
