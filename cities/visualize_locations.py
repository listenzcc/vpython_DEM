# -*- coding: utf-8 -*-
# visualize_locations.py

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import Divider, Size
from mpl_toolkits.axes_grid1.mpl_axes import Axes
from pprint import pprint
from scipy.spatial.distance import cdist

# Makesure matplotlib can draw Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']

# Read locations
with open('locations.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)

# Correction
locations['山西省']['万荣'][1] = '37.20'

# pprint(locations)

################################################################
# Get data
info_states = dict()
# For each state
for state_name, cities in locations.items():
    print(state_name)

    # Get city name and position
    name_list = []
    pos_list = []
    for name, pos_str in cities.items():
        name_list.append(name)
        pos_list.append([float(pos_str[0]), float(pos_str[1])])
    pos_array = np.array(pos_list)

    # Compute state boundary
    E_min, E_max = min(pos_array[:, 0]), max(pos_array[:, 0])
    N_min, N_max = min(pos_array[:, 1]), max(pos_array[:, 1])

    # Compute number of cities and set random color
    num = len(name_list)
    color = np.random.rand(4).reshape(1, 4) * 0.8
    color[0][-1] = 0.5

    # Record in info
    info_states[state_name] = dict(names=name_list,
                                   pos=pos_array,
                                   num=num,
                                   color=color,
                                   E_min=E_min,
                                   E_max=E_max,
                                   N_min=N_min,
                                   N_max=N_max)

# pprint(info_states)

# Compute country boundary
# Set padding
padding = 5
E_MIN = min(e['E_min'] for e in info_states.values()) - padding
E_MAX = max(e['E_max'] for e in info_states.values()) + padding
N_MIN = min(e['N_min'] for e in info_states.values()) - padding
N_MAX = max(e['N_max'] for e in info_states.values()) + padding
print(E_MIN, E_MAX, N_MIN, N_MAX)

# Compute shortest path in each state
for state_name in info_states.keys():
    info = info_states[state_name]
    dist = cdist(info['pos'], info['pos'])
    num = len(info['names'])

    passed = set()
    remain = set(range(num))
    path = []

    passed.add(0)
    remain.remove(0)
    while remain:
        min_value = 1e10
        a, b = -1, -1
        for j in passed:
            for k in remain:
                if dist[j][k] < min_value:
                    min_value = dist[j][k]
                    a, b = j, k
        path.append((info['pos'][a], info['pos'][b]))
        passed.add(b)
        remain.remove(b)

    info_states[state_name]['path'] = path

####################################################
# Init size parameters, sizes are in inch.
width = 10  # Width of article
# Compute height of article
height = width / (E_MAX - E_MIN) * (N_MAX - N_MIN)
# Width extension for legend
width_ext = 2
# Padding
padding = 0.5

# These code is to make fixed size article
# Init figure
fig = plt.figure(figsize=(width + 2 * padding + width_ext,
                          height + 2 * padding))
# The first items are for padding and the second items are for the axes.
# Article width and height
w = [Size.Fixed(padding), Size.Fixed(width)]
h = [Size.Fixed(padding), Size.Fixed(height)]
divider = Divider(fig, (0.0, 0.0, 1., 1.), w, h, aspect=False)
# the width and height of the rectangle is ignored.
ax = Axes(fig, divider.get_position())
ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
fig.add_axes(ax)

######################################################
# Draw cities
for state_name, info in info_states.items():
    # print(state_name, len(info['names']))
    color = info['color']
    colors = np.repeat(color, info['num'], axis=0)
    x, y = info['pos'][:, 0], info['pos'][:, 1]
    ax.scatter(x, y, s=5, c=colors, label=state_name)

    for p in info['path']:
        ax.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], c=tuple(color[0]))


ax.legend(loc='best', bbox_to_anchor=(1, 1))

# for p in path:
#     print(p)
#     plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]])

plt.show()
