# -*- coding: utf-8 -*-
# Filename: load_locations.py

import json
import numpy as np

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
    # print(state_name)

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

# Compute country boundary
# Set padding
padding = 5
E_MIN = min(e['E_min'] for e in info_states.values()) - padding
E_MAX = max(e['E_max'] for e in info_states.values()) + padding
N_MIN = min(e['N_min'] for e in info_states.values()) - padding
N_MAX = max(e['N_max'] for e in info_states.values()) + padding

info_global = dict(
    E_MIN=E_MIN,
    E_MAX=E_MAX,
    N_MIN=N_MIN,
    N_MAX=N_MAX,
    WIDTH=E_MAX - E_MIN,
    HEIGHT=N_MAX - N_MIN,
)
