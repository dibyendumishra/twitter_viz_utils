"""
wordcloud_utils.py — Word cloud and comparison cloud utilities.

Covers:
  - Single word cloud from text or frequency dict
  - Comparison cloud (matplotlib port of R's comparison.cloud):
    multiple topics/groups side-by-side, each with their own colour,
    sized by relative frequency within each group.
    Mirrors the comp_cloud.R usage:
        comparison.cloud(mat, colors=brewer.pal(6,"Paired"), max.words=100)
"""

from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from wordcloud import WordCloud, STOPWORDS


DEFAULT_STOPWORDS = set(STOPWORDS)


# ── Single word cloud ────────────────────────────────────────────────────────

def make_wordcloud(
    text=None,
    word_freq=None,
    extra_stopwords=(),
    background_color='white',
    max_words=200,
    width=800,
    height=400,
    colormap='viridis',
):
    """
    Generate a WordCloud from raw text or pre-computed frequencies.

    Pass either *text* (raw string) or *word_freq* (dict/Counter), not both.

    Parameters
    ----------
    text, word_freq  : raw corpus or {word: freq} dict
    extra_stopwords  : additional words to exclude on top of defaults
    background_color, max_words, width, height, colormap : standard WC params

    Returns
    -------
    WordCloud object
    """
    stopwords = DEFAULT_STOPWORDS | set(extra_stopwords)
    wc = WordCloud(
        background_color=background_color,
        max_words=max_words,
        width=width,
        height=height,
        colormap=colormap,
        stopwords=stopwords,
    )
    if word_freq is not None:
        wc.generate_from_frequencies(word_freq)
    elif text is not None:
        wc.generate(text)
    else:
        raise ValueError("Provide either 'text' or 'word_freq'.")
    return wc


def plot_wordcloud(wc, title="", figsize=(10, 5), savepath=None):
    """Display a WordCloud in matplotlib. Returns fig, ax."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    if savepath:
        fig.savefig(savepath, bbox_inches='tight')
    return fig, ax


def freq_from_token_lists(token_lists, extra_stopwords=()):
    """
    Build a word-frequency Counter from a list of token lists (e.g. tokenised tweets).

    Parameters
    ----------
    token_lists     : list[list[str]]
    extra_stopwords : iterable[str]

    Returns
    -------
    Counter
    """
    stopwords = DEFAULT_STOPWORDS | set(extra_stopwords)
    counter = Counter()
    for tokens in token_lists:
        counter.update(
            t.lower() for t in tokens
            if t.lower() not in stopwords and len(t) > 1
        )
    return counter


# ── Comparison cloud ─────────────────────────────────────────────────────────

def comparison_cloud(
    topic_freqs,
    colors=None,
    max_words=100,
    title_size=12,
    background_color='white',
    figsize=(14, 10),
    ncols=3,
    savepath=None,
):
    """
    Comparison cloud: one word cloud per topic/group, colour-coded, in a grid.

    This is a Python equivalent of R's ``comparison.cloud(mat, ...)``.
    Words are sized by their frequency *within* their topic and coloured
    by topic, making cross-topic differences easy to spot.

    Parameters
    ----------
    topic_freqs : dict[str, dict[str, float]]
        Mapping  topic_label → {word: frequency}.
        Mirrors the matrix passed to R's comparison.cloud where columns are
        topics and rows are words.
    colors : list[str], optional
        One colour per topic. Defaults to a qualitative palette.
    max_words : int
        Maximum words per topic cloud.
    title_size : int
        Font size for topic title within each subplot.
    background_color : str
    figsize : tuple
    ncols : int
        Number of columns in the subplot grid.
    savepath : str or None

    Returns
    -------
    fig, axes

    Example
    -------
    >>> # Mirrors comp_cloud.R:
    >>> #   df <- read.csv('celebs_INC.csv')  →  topic_freqs built from LDA output
    >>> topic_freqs = {
    ...     'Topic 1': {'farmers': 0.18, 'protest': 0.12, 'rights': 0.09},
    ...     'Topic 2': {'economy': 0.20, 'gdp': 0.15, 'growth': 0.10},
    ... }
    >>> comparison_cloud(topic_freqs, colors=['#e41a1c', '#377eb8'])
    """
    topics = list(topic_freqs.keys())
    n = len(topics)

    if colors is None:
        # default qualitative palette (mimics RColorBrewer "Paired")
        default_colors = [
            '#a6cee3', '#1f78b4', '#b2df8a',
            '#33a02c', '#fb9a99', '#e31a1c',
            '#fdbf6f', '#ff7f00', '#cab2d6',
        ]
        colors = [default_colors[i % len(default_colors)] for i in range(n)]

    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.array(axes).flatten()

    for i, (topic, color) in enumerate(zip(topics, colors)):
        ax = axes[i]
        freqs = topic_freqs[topic]

        # Keep only the top max_words by frequency
        top_freqs = dict(
            sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:max_words]
        )

        if not top_freqs:
            ax.axis('off')
            continue

        wc = WordCloud(
            background_color=background_color,
            max_words=max_words,
            color_func=lambda *args, **kwargs: color,
            width=400,
            height=300,
        ).generate_from_frequencies(top_freqs)

        ax.imshow(wc, interpolation='bilinear')
        ax.set_title(topic, fontsize=title_size, color=color, fontweight='bold')
        ax.axis('off')

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, bbox_inches='tight', dpi=150)

    return fig, axes


def lda_topics_to_freqs(lda_top_topics):
    """
    Convert gensim's ``model.top_topics()`` output into the dict format
    expected by ``comparison_cloud``.

    Parameters
    ----------
    lda_top_topics : list of ([(prob, word), ...], coherence)
        As returned by ``gensim.models.LdaModel.top_topics(corpus)``

    Returns
    -------
    dict[str, dict[str, float]]   e.g. {'Topic 1': {'india': 0.12, ...}, ...}
    """
    result = {}
    for i, (word_probs, _coherence) in enumerate(lda_top_topics):
        label = f'Topic {i + 1}'
        result[label] = {word: float(prob) for prob, word in word_probs}
    return result
