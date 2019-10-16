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
# uid counts from 0
uid = 0
for state_name, cities in locations.items():
    print(state_name)

    # Get city name and posesition
    name_list = []
    uid_list = []
    poses_list = []
    for name, poses_str in cities.items():
        name_list.append(name)
        # Setup uid for each city
        uid_list.append(uid)
        uid += 1
        poses_list.append([float(poses_str[0]), float(poses_str[1])])
    poses_array = np.array(poses_list)

    # Compute state boundary
    E_min, E_max = min(poses_array[:, 0]), max(poses_array[:, 0])
    N_min, N_max = min(poses_array[:, 1]), max(poses_array[:, 1])

    # Compute number of cities and set random color
    num = len(name_list)
    color = np.random.rand(4).reshape(1, 4) * 0.8
    color[0][-1] = 0.5

    # Record in info
    info_states[state_name] = dict(names=name_list,  # name list
                                   uids=uid_list,  # uid list
                                   poses=poses_array,  # pos array
                                   num=num,  # how many cities in the state
                                   color=color,  # color
                                   E_min=E_min,  # positions
                                   E_max=E_max,
                                   N_min=N_min,
                                   N_max=N_max)

# Setup uid system for global use
num_uid = uid
# A list for infomations for each city, hope for quick query
info_uid = [_ for _ in range(num_uid)]
for state_name, info in info_states.items():
    num = info['num']
    for j in range(num):
        ind = j
        uid = info['uids'][ind]
        full_name = ','.join([state_name, info['names'][ind]])
        pos = info['poses'][ind]
        info_uid[uid] = dict(state_name=state_name,  # state name
                             ind=ind,  # index in the state
                             num=num,  # how many cities in the state
                             full_name=full_name,  # full name
                             pos=pos,  # position of the city
                             extension=None)

# pprint(info_states)

# Compute country boundary
# Set padding
padding = 5
E_MIN = min(e['E_min'] for e in info_states.values()) - padding
E_MAX = max(e['E_max'] for e in info_states.values()) + padding
N_MIN = min(e['N_min'] for e in info_states.values()) - padding
N_MAX = max(e['N_max'] for e in info_states.values()) + padding
print(E_MIN, E_MAX, N_MIN, N_MAX)


# Compute shortest path based on poses: positions of nodes
def compute_path(poses):
    total = poses.shape[0]
    dist_matrix = cdist(poses, poses)

    inds = np.triu_indices_from(dist_matrix, 1)
    dist_list = [e for e in zip(dist_matrix[inds], inds[0], inds[1])]
    # dist_list = [(dist_matrix[j, k], j, k)
    #              for j in range(total) for k in range(j)]
    dist_list.sort()

    passed = set()
    remain = set(range(total))

    pbar = tqdm.tqdm(total=total)
    [passed.add(e) for e in dist_list[0][1:]]
    [remain.remove(e) for e in dist_list[0][1:]]
    a, b = dist_list[0][1], dist_list[0][2]
    # Path represented as positions and uid
    path_pos = [(poses[a][0], poses[a][1], poses[b][0], poses[b][1])]
    path_uid = [(a, b)]
    # print(path, passed, remain)
    # Update 2 steps since we already added two nodes into path
    pbar.update(2)
    while remain:
        for x in dist_list:
            if x[1] in passed and x[2] in remain:
                a, b = x[1], x[2]
                path_pos.append((poses[a][0], poses[a][1],
                                 poses[b][0], poses[b][1]))
                path_uid.append((a, b))
                passed.add(x[2])
                remain.remove(x[2])
                break
            if x[2] in passed and x[1] in remain:
                a, b = x[2], x[1]
                path_pos.append((poses[a][0], poses[a][1],
                                 poses[b][0], poses[b][1]))
                path_uid.append((a, b))
                passed.add(x[1])
                remain.remove(x[1])
                break
        pbar.update(1)
    pbar.close()
    # Transform path into np array 4 x [num]
    return np.array(path_pos).transpose(), path_uid


# Compute shortest path in each state
for state_name in info_states.keys():
    print(state_name, info_states[state_name]['num'])
    # Compute path within state
    info_states[state_name]['path'], _ = compute_path(
        info_states[state_name]['poses'])

# Compute shortest path across country
global_poses = np.concatenate([e['pos'].reshape(1, 2)
                               for e in info_uid], axis=0)
print('Global', global_poses.shape[0])
global_path, global_path_uid = compute_path(global_poses)
# Fill global_path_uid into a dict
# Formate is {[from]: [to]},
# the unique of [from] is guaranteed by the algorithm used in compute_path
global_path_uid_dict = {e[1]: e[0] for e in global_path_uid}

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

# From and To locations of a tracing
# Trace [from_uid, to_uid]
trace_from_to = [None, None]


# Trace the path of trace_from_to
def trace_path():

    # Trace back to start
    def trace_back(this):
        path = [this]
        while this in global_path_uid_dict:
            this = global_path_uid_dict[this]
            path.append(this)
        path.reverse()
        return path

    # Trace From and To locations to start
    a, b = trace_from_to
    pa, pb = trace_back(a), trace_back(b)

    # Cut two pathes until the match
    while pa[0] == pb[0]:
        x = pa[0]
        pa.pop(0)
        pb.pop(0)
        if any([not pa, not pb]):
            break
    pa.reverse()

    # Return the whole path
    return pa + [x] + pb


# OnClick event handler of scatters
def onpick(event):
    # Get infomations
    ind = event.ind[0]
    state_name = event.artist.get_label()
    name = info_states[state_name]['names'][ind]
    uid = info_states[state_name]['uids'][ind]
    num, pos = info_uid[uid]['num'], info_uid[uid]['pos']
    print(uid, state_name, name, pos)

    # Reset enlarged scatters
    def reset_scatters():
        for info in info_states.values():
            info['scatters'].set_sizes([5])

    # Enlarge selected scatter
    def enlarge_clicked_scatter():
        scatters = info_states[state_name]['scatters']
        sizes = np.zeros(num) + 5
        sizes[ind] = 20
        scatters.set_sizes(sizes)

    # Enlarge uid scatter
    def enlarge_uid_scatter(uid):
        state_name = info_uid[uid]['state_name']
        ind = info_uid[uid]['ind']
        num = info_uid[uid]['num']
        scatters = info_states[state_name]['scatters']
        sizes = scatters.get_sizes()
        # Do not reset scatters that has been enlarged
        # If sizes is list with one element,
        # means there are not enlarged scatters
        if len(sizes) == 1:
            sizes = np.zeros(num) + 5
        sizes[ind] = 20
        scatters.set_sizes(sizes)

    ########################################################
    # Interface logistics
    # 1st element is None means [from uid] has not been set
    # Setup from uid and return 0
    if trace_from_to[0] is None:
        trace_from_to[0] = uid
        print('Trace path from', state_name, name, pos)
        reset_scatters()
        enlarge_clicked_scatter()
        fig.canvas.draw()
        return 0

    # 2nd element is None means [to uid] has not been set
    # Setup to uid and trace a path
    if trace_from_to[1] is None:
        trace_from_to[1] = uid
        print('Trace path to', state_name, name, pos)
        enlarge_clicked_scatter()
        for e in trace_path():
            enlarge_uid_scatter(e)
        fig.canvas.draw()
        return 0

    # 1st and 2nd elements are all set means it is time to restart a trace
    # Setup current clicked scatter as from uid
    # Reset to uid to continue
    print('Clear trace path.')
    trace_from_to[0] = uid
    trace_from_to[1] = None
    print('Trace path from', state_name, name, pos)
    reset_scatters()
    enlarge_clicked_scatter()
    fig.canvas.draw()


for state_name, info in info_states.items():
    # print(state_name, len(info['names']))
    names = set(info['names'])
    color = info['color']
    colors = np.repeat(color, info['num'], axis=0)

    # Draw cities
    x, y = info['poses'][:, 0], info['poses'][:, 1]
    scatters = ax.scatter(x, y, s=5, c=colors, label=state_name, picker=True)
    info_states[state_name]['scatters'] = scatters
    # for j, name in enumerate(names):
    #     ax.annotate(name, (x[j], y[j]))

    # Draw path
    path = info['path']
    color[0][-1] = 0.3
    ax.plot(path[(0, 2), :], path[(1, 3), :], c=tuple(color[0]))

# Draw global_path
ax.plot(global_path[(0, 2), :], global_path[(1, 3), :], c='gray', alpha=0.3)

# Draw legend
ax.legend(loc='best', bbox_to_anchor=(1, 1))

# Connect Click handler onpick
fig.canvas.mpl_connect('pick_event', onpick)

# Plot on screen
plt.show()
