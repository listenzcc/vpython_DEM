# -*- coding: utf-8 -*-
# visualize_locations.py

import json
import numpy as np
import tqdm
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


# Compute shortest path based on pos: positions of nodes
def compute_path(pos):
    total = pos.shape[0]
    dist = cdist(pos, pos)
    dist += np.diag(np.array([np.inf for _ in range(total)]))
    passed = set()
    remain = set(range(total))
    path = []

    pbar = tqdm.tqdm(total=total)
    # Compute shortest path
    # Use fast iteration method, start from 0th city
    passed.add(0)
    remain.remove(0)
    pbar.update(1)
    while remain:
        _x, _y = tuple(passed), tuple(remain)
        _dist = dist[_x, :][:, _y]
        _a, _b = np.unravel_index(_dist.argmin(), _dist.shape)
        a, b = _x[_a], _y[_b]

        # formate of eath path [x_from, y_from, x_to, y_to]
        path.append([pos[a][0], pos[a][1], pos[b][0], pos[b][1]])
        # Record shortest edge
        passed.add(b)
        remain.remove(b)
        pbar.update(1)

    pbar.close()

    return path


# Compute shortest path in each state
for state_name in info_states.keys():
    print(state_name, info_states[state_name]['num'])
    # Compute path within state
    _path = compute_path(info_states[state_name]['pos'])
    # Transform path into np array 4 x [num]
    info_states[state_name]['path'] = np.array(_path).transpose()

# Compute shortest path across country
# global_pos = np.concatenate([e['pos'] for e in info_states.values()], axis=0)
# print('Global', global_pos.shape[0])
# _path = compute_path(global_pos)
# global_path = np.array(_path).transpose()


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
# Draw article

circle = ax.scatter(E_MIN+10, N_MIN+10, s=10, c='red', marker='o')


def onpick(event):
    ind = event.ind[0]
    state_name = event.artist.get_label()
    name = info_states[state_name]['names'][ind]
    pos = info_states[state_name]['pos'][ind]
    print(state_name, name, pos)
    circle._offsets[0][0] = pos[0]
    circle._offsets[0][1] = pos[1]
    fig.canvas.draw()


for state_name, info in info_states.items():
    # print(state_name, len(info['names']))
    names = set(info['names'])
    color = info['color']
    colors = np.repeat(color, info['num'], axis=0)

    # Draw cities
    x, y = info['pos'][:, 0], info['pos'][:, 1]
    ax.scatter(x, y, s=5, c=colors, label=state_name, picker=True)
    # for j, name in enumerate(names):
    #     ax.annotate(name, (x[j], y[j]))

    # Draw path
    path = info['path']
    color[0][-1] = 0.3
    ax.plot(path[(0, 2), :], path[(1, 3), :], c=tuple(color[0]))

# Draw global_path
# ax.plot(global_path[(0, 2), :], global_path[(1, 3), :], c='gray', alpha=0.3)

# Draw legend
ax.legend(loc='best', bbox_to_anchor=(1, 1))

fig.canvas.mpl_connect('pick_event', onpick)

# Plot on screen
plt.show()
