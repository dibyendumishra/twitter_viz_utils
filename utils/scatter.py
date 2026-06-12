"""
scatter.py — Labelled scatter plot utilities.

Typical use case: plotting entities (users, accounts) by two numeric axes
(e.g. log-follower count vs log-retweet count) with colour-coded categories
and optional point-size encoding.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def log_transform(values, base=10, zero_fallback=0):
    """Return log-transformed values; non-positive values become zero_fallback."""
    return [math.log(v, base) if v > 0 else zero_fallback for v in values]


def map_colors(categories, color_map):
    """
    Map a list of category strings to colours using *color_map*.

    Parameters
    ----------
    categories : list[str]
    color_map  : dict[str, str]   e.g. {'BJP': 'darkorange', 'INC': 'teal'}

    Returns
    -------
    list[str]  — one colour per entry; unknown categories get 'grey'.
    """
    return [color_map.get(c, 'grey') for c in categories]


def annotate_points(ax, xs, ys, labels, left_set=(), right_set=(), fontsize=8):
    """
    Annotate scatter points with text labels.

    Points whose labels appear in *left_set* are placed to the left;
    points in *right_set* to the right; everything else above the point.

    Parameters
    ----------
    ax         : matplotlib Axes
    xs, ys     : sequences of x/y coordinates
    labels     : sequence of label strings
    left_set   : collection of labels to place on the left
    right_set  : collection of labels to place on the right
    fontsize   : font size for annotations
    """
    left_set, right_set = set(left_set), set(right_set)
    for x, y, label in zip(xs, ys, labels):
        if label in left_set:
            ax.annotate(label, xy=(x, y), xytext=(x - 0.01, y),
                        fontsize=fontsize,
                        horizontalalignment='right', verticalalignment='center',
                        annotation_clip=True)
        elif label in right_set:
            ax.annotate(label, xy=(x, y), xytext=(x + 0.01, y),
                        fontsize=fontsize,
                        horizontalalignment='left', verticalalignment='center',
                        annotation_clip=True)
        else:
            ax.annotate(label, xy=(x, y), xytext=(x, y + 0.01),
                        fontsize=fontsize, ha='center')


def labeled_scatter(
    x, y, labels,
    sizes=None,
    colors=None,
    color_map=None,
    categories=None,
    trendline=False,
    xlabel="", ylabel="", title="",
    left_labels=(), right_labels=(),
    figsize=(14, 12),
    alpha=0.7,
    savepath=None,
):
    """
    Scatter plot with per-point labels, optional size encoding and trendline.

    Parameters
    ----------
    x, y       : array-like — coordinates
    labels     : array-like[str] — point labels
    sizes      : array-like, optional — raw values used as bubble size
    colors     : array-like[str], optional — explicit colour per point
    color_map  : dict, optional — mapping from category → colour
    categories : array-like[str], optional — used with color_map
    trendline  : bool — draw a dashed polynomial trendline (degree 1)
    xlabel, ylabel, title : str
    left_labels, right_labels : collections — labels to nudge left/right
    figsize    : tuple
    alpha      : float — scatter alpha
    savepath   : str or None — if given, save figure to this path

    Returns
    -------
    fig, ax
    """
    x = list(x)
    y = list(y)
    labels = list(labels)

    if colors is None and color_map is not None and categories is not None:
        colors = map_colors(list(categories), color_map)

    if sizes is not None:
        sizes = list(sizes)

    fig, ax = plt.subplots(figsize=figsize)

    if trendline and sizes is not None:
        z = np.polyfit(sizes, y, 1)
        p = np.poly1d(z)
        ax.plot(sizes, p(sizes), '--', color='whitesmoke')

    scatter_x = sizes if (trendline and sizes is not None) else x
    ax.scatter(scatter_x, y, s=x if sizes is not None else None,
               c=colors, alpha=alpha)

    annotate_points(ax, scatter_x, y, labels,
                    left_set=left_labels, right_set=right_labels)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if color_map:
        patches = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
        ax.legend(handles=patches)

    if savepath:
        fig.savefig(savepath, bbox_inches='tight')

    return fig, ax
