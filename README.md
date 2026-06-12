# viz_utils

Reusable visualisation utilities extracted from Twitter CSS projects (influencer data, Indian political landscape).

## Structure

```
viz_utils/
├── utils/
│   ├── scatter.py           # labelled scatter / bubble plots
│   ├── bar.py               # stacked horizontal + vertical bar charts
│   ├── timeline.py          # event timelines, scatter-line overlays
│   ├── geo.py               # Bokeh choropleth maps from GeoJSON
│   ├── network.py           # NetworkX retweet/mention graph utils
│   └── wordcloud_utils.py   # word cloud + comparison cloud (≈ R's comparison.cloud)
├── notebooks/
│   └── examples.ipynb       # single notebook covering all utils with realistic data
└── requirements.txt
```

## Install

```bash
pip install -r requirements.txt
```

PNG map export also needs `selenium` + `geckodriver`.

## Quick start

```python
import sys; sys.path.insert(0, 'path/to/viz_utils')

from utils.bar import stacked_hbar
from utils.scatter import labeled_scatter, log_transform
from utils.timeline import event_timeline, scatter_line_timeline, make_month_tick_labels
from utils.network import build_graph, draw_network, degree_to_size
from utils.wordcloud_utils import make_wordcloud, comparison_cloud, lda_topics_to_freqs
from utils.geo import build_choropleth
```

## API reference

### `scatter.py`
| Function | Description |
|---|---|
| `labeled_scatter(x, y, labels, ...)` | Scatter with per-point labels, colour map, bubble size, optional trendline |
| `log_transform(values)` | Element-wise log₁₀; non-positive → 0 |
| `map_colors(categories, color_map)` | Map category list → colour list |
| `annotate_points(ax, xs, ys, labels, left_set, right_set)` | Annotate with left/right nudging to reduce overlap |

### `bar.py`
| Function | Description |
|---|---|
| `stacked_hbar(labels, segments, colors, ...)` | Horizontal stacked bar (e.g. BJP vs non-BJP RTs per journalist) |
| `vbar(labels, values, ...)` | Simple vertical bar |

### `timeline.py`
| Function | Description |
|---|---|
| `event_timeline(df, x_col, y_cols, events, ...)` | Multi-series stacked subplots with vertical event markers |
| `scatter_line_timeline(df, x_col, y_col, ...)` | Combined line + scatter (trending hashtag volume) |
| `make_month_tick_labels(month_series)` | Compress repeated month names for weekly x-axes |

### `geo.py`
| Function | Description |
|---|---|
| `build_choropleth(geojson_data, value_field, ...)` | Bokeh choropleth from a GeoJSON dict |
| `save_choropleth_html(p, path)` | Standalone HTML |
| `save_choropleth_png(p, path)` | PNG (needs selenium) |
| `batch_export_png(loader, indices, ...)` | One PNG per index (weekly animation frames) |

### `network.py`
| Function | Description |
|---|---|
| `build_graph(df, source_col, target_col, ...)` | DiGraph from edge-list DataFrame |
| `draw_network(G, node_color_map, node_size, ...)` | Draw with matplotlib |
| `degree_to_size(G, scale, min_size)` | Node degree → size dict |
| `top_nodes_by_degree(G, n)` | Top-n nodes by degree |
| `export_gexf(G, path)` | Save for Gephi |

### `wordcloud_utils.py`
| Function | Description |
|---|---|
| `make_wordcloud(text=…, word_freq=…, ...)` | Single word cloud from text or freq dict |
| `plot_wordcloud(wc, ...)` | Display in matplotlib |
| `freq_from_token_lists(token_lists, ...)` | Counter from tokenised tweet lists |
| `comparison_cloud(topic_freqs, colors, ...)` | **Multi-topic comparison cloud** — Python port of R's `comparison.cloud(mat, colors=brewer.pal(...))` |
| `lda_topics_to_freqs(lda_top_topics)` | Convert gensim `model.top_topics()` output → dict for `comparison_cloud` |
