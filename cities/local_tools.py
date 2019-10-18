# -*- coding: utf-8 -*-
# Filename: local_tools.py

import time
import tqdm
import numpy as np
from functools import wraps
from scipy.spatial.distance import cdist


def my_timer(func):
    @wraps(func)
    def func_timer(*args, **kwargs):
        timestamp_start = time.time()
        print('[%s]' % str(timestamp_start),
              '%s begins.' % func.__name__)

        result = func(*args, **kwargs)

        timestamp_stop = time.time()
        passed = timestamp_stop - timestamp_start
        print('[%s]' % str(timestamp_start),
              '%s stops, %f passed.' % (func.__name__, passed),
              '[%s]' % str(timestamp_stop))

        return result
    return func_timer


# Compute shortest path based on poses: positions of nodes
# Here we use greedy strategy since there are
# full connections between each two nodes.
@my_timer
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
# about .5 seconds for a very far trace
@my_timer
def trace_shortest_path(start, stop, dist_matrix, uid_connections):
    total = dist_matrix.shape[0]
    pbar = tqdm.tqdm(total=total)

    passed = dict()
    path = dict()
    passed[start] = 0

    for _ in range(total):
        pbar.update(1)
        edges = set()
        # For each element in passed set
        for p in passed:
            # Add its direct connections into edges set
            for e in uid_connections[p]:
                # What is already in passed can not be edge
                if e in passed:
                    continue
                # format is ([dist], [from], [to])
                edges.add((dist_matrix[p][e] + passed[p], p, e))

        # _next is the best choice
        _next = sorted(edges)[0][1:]
        #  print(_next)

        path[_next[1]] = _next[0]
        if _next[1] == stop:
            pbar.close()
            print('Destination reached.')
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
