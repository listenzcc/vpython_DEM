# -*- coding: utf-8 -*-
# Filename: local_tools.py

import tqdm
import numpy as np
from scipy.spatial.distance import cdist


# Compute shortest path based on poses: positions of nodes
# Here we use greedy strategy since there are
# full connections between each two nodes.
def compute_path(poses, uids=None):
    total = poses.shape[0]
    # Distance between cities
    dist_matrix = cdist(poses, poses)

    # Restore elements in dist_matrix into dist_list
    # Formate is ([dist], [p0], [p1])
    inds = np.triu_indices_from(dist_matrix, 1)
    dist_list = [e for e in zip(dist_matrix[inds], inds[0], inds[1])]
    # Sort dist_list in increasing order
    dist_list.sort()

    passed = set()
    remain = set(range(total))

    pbar = tqdm.tqdm(total=total)
    [passed.add(e) for e in dist_list[0][1:]]
    [remain.remove(e) for e in dist_list[0][1:]]
    a, b = dist_list[0][1], dist_list[0][2]
    # Path represented as positions and uid
    path_pos = [(poses[a][0], poses[a][1], poses[b][0], poses[b][1])]
    path_uid = set([tuple(sorted((a, b)))])
    # print(path, passed, remain)
    # Update 2 steps since we already added two nodes into path
    pbar.update(2)
    while remain:
        # Fetch shortest pair
        for x in dist_list:
            fetch_this = False

            if x[1] in passed and x[2] in remain:
                a, b = x[1], x[2]
                fetch_this = True

            if x[2] in passed and x[1] in remain:
                a, b = x[2], x[1]
                fetch_this = True

            if fetch_this:
                path_pos.append((poses[a][0], poses[a][1],
                                 poses[b][0], poses[b][1]))
                passed.add(b)
                remain.remove(b)
                if uids:
                    a, b = uids[a], uids[b]
                path_uid.add(tuple(sorted((a, b))))
                break

        pbar.update(1)
    pbar.close()
    # Transform path into np array 4 x [num]
    return np.array(path_pos).transpose(), path_uid, dist_matrix


# Trace shortest path from start to stop
def trace_shortest_path(start, stop, dist_matrix, all_path_uid, uid_connections):
    total = dist_matrix.shape[0]
    pbar = tqdm.tqdm(total=total)

    passed = dict()
    path = dict()
    passed[start] = 0

    for _ in range(total):
        pbar.update(1)
        edges = set()
        for a, b in [(0, 1), (1, 0)]:
            # from e[a] to e[b]
            [edges.add((dist_matrix[e[a]][e[b]] + passed[e[a]], e[a], e[b]))
             for e in all_path_uid if all([e[a] in passed,
                                           e[b] not in passed])]
        # _next is the best choice
        # format is ([dist], [from], [to])
        _next = sorted(edges)[0][1:]
        #  print(_next)

        path[_next[1]] = _next[0]
        if _next[1] == stop:
            pbar.close()
            print('Stop reached.')
            break
        passed[_next[1]] = dist_matrix[_next[0]][_next[1]] + passed[_next[0]]

    pbar.close()

    found_path = [stop]
    ptr = stop
    while True:
        found_path.append(path[ptr])
        ptr = path[ptr]
        if ptr == start:
            break

    found_path.reverse()
    return found_path
