# -*- coding: utf-8 -*-
# visualize_locations.py

import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

from load_locations import info_states, info_uid, info_global
from figure_setup import fix_sz_fig
from local_tools import compute_path, trace_shortest_path


########################################################
# Compute pathes connect cities, and parse the pathes for further use
all_path_uid = set()

# Compute shortest path within each state
for state_name in info_states.keys():
    print(state_name, info_states[state_name]['num'])
    # Compute path within state
    info_states[state_name]['path'], path_uid, _ = compute_path(
        info_states[state_name]['poses'], info_states[state_name]['uids'])
    [all_path_uid.add(e) for e in path_uid]
    print(len(all_path_uid))

# Compute shortest path across country
global_poses = np.concatenate([e['pos'].reshape(1, 2)
                               for e in info_uid], axis=0)
print('Global', global_poses.shape[0])
global_path, global_path_uid, global_dist_matrix = compute_path(global_poses)
[all_path_uid.add(e) for e in global_path_uid]
print(len(all_path_uid))


####################################################
# Init size parameters, sizes are in inch.
width = 10  # Width of article
# Compute height of article
height = width / info_global['WIDTH'] * info_global['HEIGHT']
# Setup figure and axes
fig, ax = fix_sz_fig(width, height)


######################################################
# Draw article
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

# Init tracing dict to restore start and stop uid
tracing = dict(start=None, stop=None)


# OnClick event handler of scatters
def onpick(event):
    # Get infomations
    ind = event.ind[0]
    state_name = event.artist.get_label()
    name = info_states[state_name]['names'][ind]
    uid = info_states[state_name]['uids'][ind]
    num, pos = info_uid[uid]['num'], info_uid[uid]['pos']
    print('[Clicked]', uid, state_name, name, pos)

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
    if tracing['start'] is None:
        tracing['start'] = uid
        print('Tracing will start on', state_name, name, pos)
        reset_scatters()
        enlarge_clicked_scatter()
        fig.canvas.draw()
        return 0

    # 2nd element is None means [to uid] has not been set
    # Setup to uid and trace a path
    if tracing['stop'] is None:
        tracing['stop'] = uid
        print('Tracing will stop on', state_name, name, pos)
        enlarge_clicked_scatter()
        fig.canvas.draw()
        print('Tracing starts.')
        for e in trace_shortest_path(tracing['start'], tracing['stop'],
                                     global_dist_matrix, all_path_uid):
            enlarge_uid_scatter(e)
        fig.canvas.draw()
        return 0

    # 1st and 2nd elements are all set means it is time to restart a trace
    # Setup current clicked scatter as from uid
    # Reset to uid to continue
    print('Clear trace path.')
    tracing['start'] = uid
    tracing['stop'] = None
    print('Trace path from', state_name, name, pos)
    reset_scatters()
    enlarge_clicked_scatter()
    fig.canvas.draw()


# Connect Click handler onpick
fig.canvas.mpl_connect('pick_event', onpick)

# Plot on screen
plt.show()
