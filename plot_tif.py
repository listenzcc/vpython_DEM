# -*- coding: utf-8 -*-

# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# %%
fname = 'Shanghai-90m-DEM.tif'
# fname = 'Rome-30m-DEM.tif'
Z = cv2.imread(fname)
print('Raw shape is', Z.shape)
Z = Z[:, :, 0]
print(Z.shape)


# %%
# Computing histogram and threshold idx for covering population
# Output:
# 0 log histogram counting
# 1 bin edges
# 2 threshold index of population rate
def compute_histogram(d, bins=100, rate=1-0.002):
    d = d[d > 0]
    bins = min(len(np.unique(d)), bins)
    print('bins is', bins)
    # Compute histogram
    hist, bins = np.histogram(d, bins=bins)
    # Adjust bins since it stores bin edges and its length is len(hist)+1
    bins = bins[:-1]
    # Compute threshold idx covers rate on population
    n, m = len(hist), sum(hist) * rate
    for j in range(n):
        if m <= 0:
            break
        m -= hist[j]
    # Return outputs
    return np.log(hist), bins, j


# Plot Z and its histogram
def plot_geometric(Z, hist, bins, idx, fig, axes_map, axes_hist):
    # Plot histogram on hist panel
    axes_hist.bar(bins, hist)
    # Draw red line on idx
    axes_hist.bar(bins[idx], hist[idx], color='red')
    axes_hist.text(bins[idx], hist[idx],
                   'Cut on %d' % (bins[idx]), color='red')

    # Plot Z on map panel
    cut = bins[idx]
    Z_cut = Z.copy()
    Z_cut[Z > cut] = cut
    fig.colorbar(axes_map.imshow(Z_cut), ax=axes_map)

# %%


# Read tif and change it into 2-D matrix
fname = 'Shanghai-90m-DEM.tif'
# fname = 'Rome-30m-DEM.tif'
Z = cv2.imread(fname)
print('Raw shape is', Z.shape)
Z = Z[:, :, 0]
print(Z.shape)

# %%

# Prepare painting
fig, axes = plt.subplots(2, 2, figsize=(10, 5))


# Compute and display on raw Z
print('Working on Z, shape', Z.shape)
hist, bins, idx = compute_histogram(Z.copy())
plot_geometric(Z, hist, bins, idx, fig, axes[0][0], axes[0][1])

# Compute and display on box Z
box = [(100, 1000), 400, 300]
# Draw box on raw map
axes[0][0].add_patch(plt.Rectangle((box[0][1], box[0][0]), box[2], box[1],
                                   facecolor='None', edgecolor='red'))
# Fetch Z in box
box_Z = Z[box[0][0]:box[0][0]+box[1], box[0][1]:box[0][1]+box[2]]
# Working on box_Z
print('Working on box_Z, shape', box_Z.shape)
hist, bins, idx = compute_histogram(box_Z.copy())
plot_geometric(box_Z, hist, bins, idx, fig, axes[1][0], axes[1][1])

# Paint axes
fig.tight_layout()
plt.show()

# %%
