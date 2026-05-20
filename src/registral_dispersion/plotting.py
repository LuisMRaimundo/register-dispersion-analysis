"""Matplotlib / Plotly figures for registral dispersion (primary: dispersion_degree)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from registral_dispersion.metric_documentation import (
    PLOT_YAXIS_ENTROPY,
    PLOT_YAXIS_PAIRWISE,
    PLOT_YAXIS_PAIRWISE_NORMALIZED,
    PLOT_YAXIS_PRIMARY,
    PLOT_YAXIS_PRIMARY_NORMALIZED,
)
from registral_dispersion.visual_theme import (
    LINE_ENTROPY,
    LINE_PAIRWISE,
    LINE_SPAN,
    PANEL_BG_LIGHT,
    apply_plotly_dispersion_layout,
)

MPL_FIG_W, MPL_FIG_H = 13.0, 5.8
MPL_FACE = PANEL_BG_LIGHT


def _base_mpl_style(ax, xlabel: str, ylabel: str, title: str):
    ax.set_facecolor("#ffffff")
    ax.set_xlabel(xlabel, fontsize=11, color="#44403c", labelpad=8)
    ax.set_ylabel(ylabel, fontsize=11, color="#44403c", labelpad=8)
    if title:
        ax.set_title(title, fontsize=15, fontweight="500", color="#1c1917", pad=14, fontfamily="serif")
    ax.tick_params(axis="both", which="major", labelsize=10, colors="#78716c")
    ax.grid(True, axis="y", alpha=0.45, color="#e7e5e4", linestyle="-", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#d6d3d1")
        ax.spines[spine].set_linewidth(0.8)


def _primary_dispersion_series(results: dict, *, use_norm: bool) -> tuple[np.ndarray, str]:
    if use_norm:
        return (
            np.asarray(results["normalized_dispersion_degree"], dtype=float),
            PLOT_YAXIS_PRIMARY_NORMALIZED,
        )
    return np.asarray(results["dispersion_degree"], dtype=float), PLOT_YAXIS_PRIMARY


def _pairwise_overlay_series(results: dict, *, use_norm: bool) -> tuple[np.ndarray, str]:
    if use_norm:
        return (
            np.asarray(results["normalized_mean_pairwise_registral_distance"], dtype=float),
            PLOT_YAXIS_PAIRWISE_NORMALIZED,
        )
    return np.asarray(results["mean_pairwise_registral_distance"], dtype=float), PLOT_YAXIS_PAIRWISE


def make_dispersion_figure(
    results: dict,
    title: str = "Registral dispersion",
    show_registral_span: bool = False,
    show_mean_pairwise: bool | None = None,
    show_occupancy_entropy: bool = False,
    y_scale: str = "raw",
):
    """
    Matplotlib figure: primary = ``dispersion_degree`` (default: raw semitones).

    ``show_mean_pairwise`` overlays mean pairwise distance on a secondary axis.
    ``show_registral_span`` is a deprecated alias for ``show_mean_pairwise`` (span is already primary).
    """
    overlay_pairwise = show_mean_pairwise if show_mean_pairwise is not None else show_registral_span
    t = np.asarray(results["t"], dtype=float)
    use_norm = str(y_scale).strip().lower() == "normalized"
    d_primary, y_primary = _primary_dispersion_series(results, use_norm=use_norm)
    if show_occupancy_entropy:
        fig, (ax1, ax_e) = plt.subplots(
            2,
            1,
            sharex=True,
            figsize=(MPL_FIG_W, 6.2),
            facecolor=MPL_FACE,
            gridspec_kw={"height_ratios": [2.2, 1.0], "hspace": 0.12},
        )
    else:
        fig, ax1 = plt.subplots(figsize=(MPL_FIG_W, MPL_FIG_H), facecolor=MPL_FACE)
        ax_e = None
    ax1.plot(
        t,
        d_primary,
        color=LINE_SPAN,
        linewidth=2.4,
        solid_capstyle="round",
        label="Dispersion degree",
    )
    _base_mpl_style(ax1, "Time (quarter length)", y_primary, title)
    if overlay_pairwise:
        ax_pair = ax1.twinx()
        d_pair, y_pair = _pairwise_overlay_series(results, use_norm=use_norm)
        ax_pair.plot(
            t,
            d_pair,
            color=LINE_PAIRWISE,
            linestyle="--",
            linewidth=2.0,
            alpha=0.92,
            label="Mean pairwise distance",
        )
        ax_pair.set_ylabel(y_pair, fontsize=11, color=LINE_PAIRWISE)
        ax_pair.tick_params(axis="y", colors=LINE_PAIRWISE)
    if ax_e is not None:
        ent = np.asarray(results["occupancy_entropy"], dtype=float)
        ax_e.plot(t, ent, color=LINE_ENTROPY, linewidth=2.0, label="Occupancy entropy")
        _base_mpl_style(ax_e, "Time (quarter length)", PLOT_YAXIS_ENTROPY, "")
        ax_e.set_ylim(0, 1)
    if overlay_pairwise or ax_e is not None:
        fig.subplots_adjust(top=0.9, hspace=0.22 if ax_e is not None else 0.15)
    else:
        fig.tight_layout(pad=2.0)
    return fig


def make_dispersion_figure_plotly(
    results: dict,
    title: str = "Registral dispersion",
    show_registral_span: bool = False,
    show_mean_pairwise: bool | None = None,
    show_occupancy_entropy: bool = False,
    y_scale: str = "raw",
):
    """Plotly figure mirroring :func:`make_dispersion_figure` (optional secondary y for pairwise on row 1)."""
    overlay_pairwise = show_mean_pairwise if show_mean_pairwise is not None else show_registral_span
    t = np.asarray(results["t"], dtype=float)
    use_norm = str(y_scale).strip().lower() == "normalized"
    d_primary, y_primary = _primary_dispersion_series(results, use_norm=use_norm)
    if show_occupancy_entropy:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.68, 0.32],
            specs=[[{"secondary_y": bool(overlay_pairwise)}], [{}]],
        )
    else:
        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": bool(overlay_pairwise)}]])
    fig.add_trace(
        go.Scatter(
            x=t,
            y=d_primary,
            mode="lines",
            name="Dispersion degree",
            line=dict(color=LINE_SPAN, width=2.4, shape="spline", smoothing=0.35),
        ),
        row=1,
        col=1,
        secondary_y=False,
    )
    if overlay_pairwise:
        d_pair, y_pair = _pairwise_overlay_series(results, use_norm=use_norm)
        fig.add_trace(
            go.Scatter(
                x=t,
                y=d_pair,
                mode="lines",
                name="Mean pairwise distance",
                line=dict(color=LINE_PAIRWISE, width=2.2, dash="dash", shape="spline", smoothing=0.35),
            ),
            row=1,
            col=1,
            secondary_y=True,
        )
    fig.update_yaxes(title_text=y_primary, row=1, col=1, secondary_y=False)
    if overlay_pairwise:
        fig.update_yaxes(title_text=y_pair, row=1, col=1, secondary_y=True)
    rows = 2 if show_occupancy_entropy else 1
    fig.update_xaxes(title_text="Time (quarter length)", row=rows, col=1)
    if show_occupancy_entropy:
        ent = np.asarray(results["occupancy_entropy"], dtype=float)
        fig.add_trace(
            go.Scatter(x=t, y=ent, mode="lines", name="Occupancy entropy", line=dict(color=LINE_ENTROPY, width=2.2)),
            row=2,
            col=1,
        )
        fig.update_yaxes(title_text=PLOT_YAXIS_ENTROPY, range=[0, 1], row=2, col=1)
    apply_plotly_dispersion_layout(
        fig,
        title=title,
        height=580 if rows == 2 else 440,
        secondary_y=overlay_pairwise,
    )
    return fig


def make_register_figure(results_u, title="occupancy_entropy (legacy)"):
    """Deprecated: plot ``U`` = occupancy entropy only (0–1)."""
    t = np.array(results_u["t"], dtype=float)
    U = np.array(results_u["U"], dtype=float)
    fig, ax = plt.subplots(figsize=(MPL_FIG_W, MPL_FIG_H), facecolor=MPL_FACE)
    ax.plot(t, U, color=LINE_PAIRWISE, linewidth=2.4, solid_capstyle="round")
    _base_mpl_style(ax, "Time (quarter length)", "Occupancy entropy [0–1]", title)
    ax.set_ylim(0, 1)
    fig.tight_layout(pad=2.0)
    return fig


def make_register_figure_plotly(results_u, title="occupancy_entropy (legacy)"):
    """Deprecated Plotly occupancy-only plot."""
    t = np.array(results_u["t"], dtype=float)
    U = np.array(results_u["U"], dtype=float)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=U, mode="lines", line=dict(color=LINE_PAIRWISE, width=2.4)))
    apply_plotly_dispersion_layout(fig, title=title, height=400)
    return fig
