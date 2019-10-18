# -*- coding: utf-8 -*-
# Filename: figure_setup.py


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import Divider, Size
from mpl_toolkits.axes_grid1.mpl_axes import Axes


# Set up figure with fixed size axes
def fix_sz_fig(width, height, width_ext=2, padding=.5):
    # These code is to make fixed size article
    # Makesure matplotlib can draw Chinese characters
    plt.rcParams['font.sans-serif'] = ['SimHei']
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

    return fig, ax
