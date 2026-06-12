"""
bar.py — Bar chart utilities.

Covers horizontal stacked bars (e.g. party-wise retweet breakdown per user)
and simple vertical bar charts.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def stacked_hbar(
    labels,
    segments,
    colors,
    segment_labels=None,
    xlabel="",
    title="",
    figsize=(14, 12),
    savepath=None,
):
    """
    Horizontal stacked bar chart.

    Parameters
    ----------
    labels         : list[str] — y-axis tick labels (one per bar)
    segments       : list[array-like] — one array per stack segment,
                     each with len(labels) values
    colors         : list[str] — one colour per segment
    segment_labels : list[str], optional — legend labels for each segment
    xlabel         : str
    title          : str
    figsize        : tuple
    savepath       : str or None

    Returns
    -------
    fig, ax

    Example
    -------
    >>> stacked_hbar(
    ...     labels=['Alice', 'Bob'],
    ...     segments=[[10, 5], [3, 8]],
    ...     colors=['darkorange', 'skyblue'],
    ...     segment_labels=['BJP RTs', 'Other RTs'],
    ... )
    """
    fig, ax = plt.subplots(figsize=figsize)

    lefts = [0] * len(labels)
    for seg, color in zip(segments, colors):
        ax.barh(range(len(labels)), seg, left=lefts, color=color)
        lefts = [l + s for l, s in zip(lefts, seg)]

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    if segment_labels:
        patches = [mpatches.Patch(color=c, label=l)
                   for c, l in zip(colors, segment_labels)]
        ax.legend(handles=patches)

    if savepath:
        fig.savefig(savepath, bbox_inches='tight')

    return fig, ax


def vbar(
    labels,
    values,
    color='steelblue',
    xlabel="",
    ylabel="",
    title="",
    rotation=45,
    figsize=(10, 6),
    savepath=None,
):
    """
    Simple vertical bar chart.

    Parameters
    ----------
    labels   : list[str]
    values   : list[numeric]
    color    : str or list[str]
    rotation : int — x-tick label rotation
    savepath : str or None

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(range(len(labels)), values, color=color)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=rotation, ha='right')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if savepath:
        fig.savefig(savepath, bbox_inches='tight')

    return fig, ax
