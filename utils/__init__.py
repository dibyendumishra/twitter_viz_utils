"""
viz_utils — Social-media visualization utilities.

Modules
-------
scatter         Labelled scatter / bubble plots
bar             Stacked horizontal and vertical bar charts
timeline        Line plots, event timelines, scatter-line overlays
geo             Bokeh choropleth maps from GeoJSON
network         NetworkX graph construction and drawing
wordcloud_utils Word cloud + comparison cloud (port of R comparison.cloud)
"""

from .scatter import labeled_scatter, log_transform, map_colors, annotate_points
from .bar import stacked_hbar, vbar
from .timeline import event_timeline, scatter_line_timeline, make_month_tick_labels
from .wordcloud_utils import (
    make_wordcloud, plot_wordcloud, freq_from_token_lists,
    comparison_cloud, lda_topics_to_freqs,
)
from .network import build_graph, draw_network, degree_to_size, top_nodes_by_degree

__all__ = [
    # scatter
    "labeled_scatter", "log_transform", "map_colors", "annotate_points",
    # bar
    "stacked_hbar", "vbar",
    # timeline
    "event_timeline", "scatter_line_timeline", "make_month_tick_labels",
    # wordcloud
    "make_wordcloud", "plot_wordcloud", "freq_from_token_lists",
    "comparison_cloud", "lda_topics_to_freqs",
    # network
    "build_graph", "draw_network", "degree_to_size", "top_nodes_by_degree",
]
