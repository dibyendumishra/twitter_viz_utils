"""
network.py — Retweet / mention network graph utilities using networkx.

Builds directed graphs from edge lists (sourceID → targetID),
then renders them with matplotlib or exports to formats like GEXF for Gephi.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


try:
    import networkx as nx
    _NX_AVAILABLE = True
except ImportError:
    _NX_AVAILABLE = False


def _require_nx():
    if not _NX_AVAILABLE:
        raise ImportError("networkx is required: pip install networkx")


def build_graph(df, source_col, target_col, weight_col=None, directed=True):
    """
    Build a networkx graph from a DataFrame of edges.

    Parameters
    ----------
    df         : pd.DataFrame
    source_col : str
    target_col : str
    weight_col : str, optional — if given, edges carry a 'weight' attribute
    directed   : bool — DiGraph if True, Graph otherwise

    Returns
    -------
    networkx.Graph or DiGraph
    """
    _require_nx()
    G = nx.DiGraph() if directed else nx.Graph()
    for _, row in df.iterrows():
        kwargs = {}
        if weight_col:
            kwargs['weight'] = row[weight_col]
        G.add_edge(row[source_col], row[target_col], **kwargs)
    return G


def draw_network(
    G,
    node_color_map=None,
    node_size=50,
    edge_alpha=0.3,
    layout='spring',
    layout_kwargs=None,
    title="",
    figsize=(12, 12),
    legend_patches=None,
    savepath=None,
):
    """
    Draw a networkx graph with matplotlib.

    Parameters
    ----------
    G               : networkx.Graph
    node_color_map  : dict {node: color} or None (defaults to steelblue)
    node_size       : int or dict {node: size}
    edge_alpha      : float
    layout          : str — 'spring', 'kamada_kawai', 'circular', 'random'
    layout_kwargs   : dict, optional — passed to the layout function
    title           : str
    figsize         : tuple
    legend_patches  : list[matplotlib.patches.Patch], optional
    savepath        : str or None

    Returns
    -------
    fig, ax
    """
    _require_nx()
    layout_fns = {
        'spring': nx.spring_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'circular': nx.circular_layout,
        'random': nx.random_layout,
    }
    layout_fn = layout_fns.get(layout, nx.spring_layout)
    pos = layout_fn(G, **(layout_kwargs or {}))

    nodes = list(G.nodes())
    if isinstance(node_color_map, dict):
        node_colors = [node_color_map.get(n, 'steelblue') for n in nodes]
    else:
        node_colors = 'steelblue'

    if isinstance(node_size, dict):
        node_sizes = [node_size.get(n, 50) for n in nodes]
    else:
        node_sizes = node_size

    fig, ax = plt.subplots(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=node_sizes, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=edge_alpha, ax=ax)
    ax.set_title(title)
    ax.axis('off')

    if legend_patches:
        ax.legend(handles=legend_patches)

    if savepath:
        fig.savefig(savepath, bbox_inches='tight', dpi=150)

    return fig, ax


def degree_to_size(G, scale=10, min_size=20):
    """Return a dict {node: size} based on degree, useful for node_size."""
    _require_nx()
    return {n: max(min_size, G.degree(n) * scale) for n in G.nodes()}


def top_nodes_by_degree(G, n=20):
    """Return the top-n nodes by (out-)degree as a list of (node, degree)."""
    _require_nx()
    degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    return degrees[:n]


def export_gexf(G, path):
    """Save graph to GEXF format (readable by Gephi)."""
    _require_nx()
    nx.write_gexf(G, str(path))
