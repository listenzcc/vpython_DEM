# -*- coding: utf-8 -*-
# visualize_locations.py

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import Divider, Size
from mpl_toolkits.axes_grid1.mpl_axes import Axes
from pprint import pprint

# Makesure matplotlib can draw Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']

# Read locations
with open('locations.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)

# Correction
locations['山西省']['万荣'][1] = '37.20'

# pprint(locations)

num_cities = 0
N_range = [90, 0]
E_range = [180, 0]

####################################################
# These code is to make fixed size ax
fig = plt.figure(figsize=(6, 6))
# The first items are for padding and the second items are for the axes.
# sizes are in inch.
h = [Size.Fixed(0.5), Size.Fixed(5)]
v = [Size.Fixed(0.5), Size.Fixed(5)]
divider = Divider(fig, (0.0, 0.0, 1., 1.), h, v, aspect=False)
# the width and height of the rectangle is ignored.
ax = Axes(fig, divider.get_position())
ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
fig.add_axes(ax)

# For each state
colors = np.random.rand(100)
for state_name, cities in locations.items():
    print(state_name)
    # For each city
    color = np.random.rand(3).reshape(1, 3)
    for name, pos_str in cities.items():
        num_cities += 1
        # Formation is name: [E, N]
        # Compute position
        pos = [float(pos_str[0]), float(pos_str[1])]
        if pos[0] < E_range[0]:
            E_range[0] = pos[0]
        if pos[0] > E_range[1]:
            E_range[1] = pos[0]
        if pos[1] < N_range[0]:
            N_range[0] = pos[1]
        if pos[1] > N_range[1]:
            N_range[1] = pos[1]

        print(name, pos)
        # Draw a point
        ax.scatter(pos[0], pos[1], s=5, c=color, label=state_name,
                   marker='.', alpha=0.5, edgecolor=None)
        # Mark name
        # axe.text(pos[0], pos[1], u'%s' % name)
# ax.legend()

print(num_cities, N_range, E_range)

padding = 5
ax.set_ylim(N_range[0]-padding, N_range[0]+E_range[1]-E_range[0]+padding)
ax.set_xlim(E_range[0]-padding, E_range[0]+E_range[1]-E_range[0]+padding)

plt.show()
