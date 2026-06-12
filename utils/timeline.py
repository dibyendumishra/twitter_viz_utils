"""
timeline.py — Line plot and timeline utilities.

Covers:
  - Multi-series line plots with event annotations (vertical lines + labels)
  - Stacked (shared x-axis) subplot timelines
  - Scatter + line overlay (e.g. trending hashtag volume over time)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def event_timeline(
    df,
    x_col,
    y_cols,
    colors=None,
    y_labels=None,
    events=None,
    event_y_offsets=None,
    x_tick_labels=None,
    title="",
    xlabel="",
    figsize=(10, 6),
    savepath=None,
):
    """
    Stacked multi-series line chart with optional event markers.

    Each series in *y_cols* gets its own subplot sharing the x-axis.

    Parameters
    ----------
    df             : pd.DataFrame
    x_col          : str — column for x-axis
    y_cols         : list[str] — one series per subplot
    colors         : list[str], optional — one per series
    y_labels       : list[str], optional — y-axis labels per subplot
    events         : dict {x_value: label}, optional — vertical event lines
    event_y_offsets: list[numeric], optional — y positions for event text
                     per subplot; defaults to using axis data range midpoints
    x_tick_labels  : list[str], optional — custom x-tick labels for last axis
    title          : str — figure title
    xlabel         : str
    figsize        : tuple
    savepath       : str or None

    Returns
    -------
    fig, axes
    """
    n = len(y_cols)
    colors = colors or [None] * n
    y_labels = y_labels or y_cols
    events = events or {}

    fig, axes = plt.subplots(
        nrows=n, figsize=figsize,
        gridspec_kw={'hspace': 0}, sharex=True
    )
    if n == 1:
        axes = [axes]

    for i, (col, color, ylabel) in enumerate(zip(y_cols, colors, y_labels)):
        ax = axes[i]
        sns.lineplot(data=df, x=x_col, y=col, color=color, ax=ax)
        ax.set_ylabel(ylabel, color=color or 'black')
        ax.set_xlabel('')
        if i < n - 1:
            ax.set_xticks([])

        for ev_x, ev_label in events.items():
            ax.axvline(ev_x, linestyle='--', color='grey', alpha=0.3)
            y_range = ax.get_ylim()
            y_pos = (event_y_offsets[i]
                     if event_y_offsets and i < len(event_y_offsets)
                     else y_range[0] + 0.1 * (y_range[1] - y_range[0]))
            ax.text(ev_x, y_pos, ev_label,
                    verticalalignment='bottom', rotation=90,
                    alpha=0.5, fontsize=8)

    if x_tick_labels is not None:
        axes[-1].set_xticklabels(x_tick_labels, fontsize=8)
    axes[-1].set_xlabel(xlabel)

    fig.suptitle(title)
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, dpi=300, bbox_inches='tight')

    return fig, axes


def scatter_line_timeline(
    df,
    x_col,
    y_col,
    hue_col=None,
    annotate_mask=None,
    annotate_col=None,
    xlabel="",
    ylabel="",
    title="",
    figsize=(12, 5),
    rotation=90,
    savepath=None,
):
    """
    Combined line + scatter plot (e.g. trending hashtag volume over time).

    Parameters
    ----------
    df             : pd.DataFrame
    x_col          : str — x-axis column (e.g. hour group)
    y_col          : str — y-axis column (e.g. tweet_volume)
    hue_col        : str, optional — colour scatter by this column
    annotate_mask  : boolean Series or None — rows to annotate
    annotate_col   : str, optional — column with annotation text
    xlabel, ylabel : str
    title          : str
    figsize        : tuple
    rotation       : int — x-tick label rotation
    savepath       : str or None

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.lineplot(data=df, x=x_col, y=y_col, ax=ax, color='steelblue')
    sns.scatterplot(data=df, x=x_col, y=y_col,
                    hue=hue_col, ax=ax)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(rotation=rotation, fontsize=7, ha='left')

    if annotate_mask is not None and annotate_col is not None:
        for _, row in df[annotate_mask].iterrows():
            ax.text(row[x_col], row[y_col], row[annotate_col], fontsize=7)

    if savepath:
        fig.savefig(savepath, bbox_inches='tight')

    return fig, ax


def make_month_tick_labels(month_series):
    """
    Compress a per-week month column into sparse tick labels.

    Returns a list where only the first occurrence of each month is labelled;
    subsequent weeks in the same month get an empty string.

    Parameters
    ----------
    month_series : pd.Series[str]   e.g. ['Jan','Jan','Jan','Feb',...]

    Returns
    -------
    list[str]
    """
    labels = []
    last = None
    for m in month_series:
        if m != last:
            labels.append(m)
            last = m
        else:
            labels.append('')
    return labels
