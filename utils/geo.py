"""
geo.py — Choropleth map utilities using Bokeh + GeoJSON.

Builds static or interactive choropleth maps from GeoJSON files that carry a
numeric property (e.g. language proportion per Indian state).
"""

import json
from pathlib import Path

from bokeh.plotting import figure, output_file, save
from bokeh.models import (
    GeoJSONDataSource,
    LinearColorMapper,
    ColorBar,
    HoverTool,
)
from bokeh.palettes import brewer
from bokeh.io import export_png


def load_geojson(path):
    """Load a GeoJSON file and return as dict."""
    with open(path) as f:
        return json.load(f)


def build_choropleth(
    geojson_data,
    value_field,
    palette_name='YlOrBr',
    palette_size=8,
    low=0,
    high=1,
    title="Choropleth Map",
    plot_size=600,
    hover_tooltips=None,
):
    """
    Build a Bokeh choropleth figure from a GeoJSON dict.

    Parameters
    ----------
    geojson_data   : dict  — already-loaded GeoJSON (with features)
    value_field    : str   — property name in each feature to colour by
    palette_name   : str   — Bokeh brewer palette name (e.g. 'YlOrBr', 'BuPu')
    palette_size   : int   — number of palette colours (3–9)
    low, high      : float — data range for colour mapper
    title          : str
    plot_size      : int   — width and height in pixels
    hover_tooltips : list[tuple], optional
                     e.g. [('State', '@state'), ('Value', '@count')]

    Returns
    -------
    bokeh.plotting.figure
    """
    palette = list(reversed(brewer[palette_name][palette_size]))
    color_mapper = LinearColorMapper(palette=palette, low=low, high=high)

    source = GeoJSONDataSource(geojson=json.dumps(geojson_data))

    p = figure(
        title=title,
        plot_height=plot_size,
        plot_width=plot_size,
    )
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.patches(
        'xs', 'ys',
        source=source,
        fill_color={'field': value_field, 'transform': color_mapper},
        line_color='black',
        line_width=0.25,
        fill_alpha=1,
    )

    color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))
    p.add_layout(color_bar, 'right')

    if hover_tooltips:
        p.add_tools(HoverTool(tooltips=hover_tooltips))

    return p


def save_choropleth_png(p, output_path):
    """Export a Bokeh figure to PNG (requires selenium + geckodriver)."""
    export_png(p, filename=str(output_path))


def save_choropleth_html(p, output_path):
    """Save a Bokeh figure as a standalone HTML file."""
    output_file(str(output_path))
    save(p)


def batch_export_png(geojson_loader, indices, value_field, output_dir, **kwargs):
    """
    Export a PNG for each index (e.g. week number) by calling geojson_loader(i).

    Parameters
    ----------
    geojson_loader : callable(int) -> dict  — returns geojson dict for index i
    indices        : iterable[int]
    value_field    : str
    output_dir     : str or Path
    **kwargs       : passed to build_choropleth
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for i in indices:
        data = geojson_loader(i)
        p = build_choropleth(data, value_field, **kwargs)
        save_choropleth_png(p, output_dir / f"{i}.png")
        print(f"Exported {i}.png")
