"""
Advised analysis presets (see docs/PARAMETERIZATION_GUIDE.md).

Each preset fills the Gradio UI with a coherent parameter set for a research stance.
"""

from __future__ import annotations

from dataclasses import dataclass

from registral_dispersion.concentration_map import (
    DEFAULT_COLORMAP,
    DEFAULT_CONCENTRATION_MODE,
    DISPLAY_NORMALIZATION_LOG1P,
)
from registral_dispersion.observation import (
    OBSERVATION_MODE_EVENT_BOUNDARIES,
    OBSERVATION_MODE_FIXED_WINDOW,
)
from registral_dispersion.pitch_utils import (
    DEFAULT_REGISTER_HIGH,
    DEFAULT_REGISTER_LOW,
    REGISTER_PRESET_FULL,
)
from registral_dispersion.profiles import ANALYSIS_PROFILE_OCCUPIED_SPACE
from registral_dispersion.summarize import DEFAULT_SUMMARIZE_PARAMS

PRESET_CUSTOM = "Custom (manual settings)"
PRESET_STATIC_VERTICAL = "Static vertical aggregate"
PRESET_MOVING_FRAGMENT = "Moving fragment"
PRESET_GLOBAL_SUMMARY = "Global summary / one-number"

ANALYSIS_PRESETS = (
    PRESET_CUSTOM,
    PRESET_STATIC_VERTICAL,
    PRESET_MOVING_FRAGMENT,
    PRESET_GLOBAL_SUMMARY,
)

_PITCH_FROM_PROFILE = "(from profile)"


@dataclass(frozen=True)
class AnalysisPresetSpec:
    """Full UI parameter bundle for one advised workflow."""

    key: str
    summary: str
    primary_metric: str
    register_preset: str
    register_low: str
    register_high: str
    time_step: float
    window_size: float
    analysis_profile: str
    observation_mode: str
    pitch_sampling_override: str
    show_registral_span: bool
    show_occupancy_entropy: bool
    plot_normalized_y: bool
    show_heatmap: bool
    heatmap_mode: str
    heatmap_normalization: str
    heatmap_colormap: str


PRESET_SPECS: dict[str, AnalysisPresetSpec] = {
    PRESET_STATIC_VERTICAL: AnalysisPresetSpec(
        key=PRESET_STATIC_VERTICAL,
        summary=(
            "**Static vertical aggregate** — one row per score interval where the active pitch set is "
            "constant (`event_boundaries`). No moving-window smoothing. "
            "Read **`dispersion_degree`** as the canonical metric; use CSV `interval_duration` "
            "for duration-weighted aggregates."
        ),
        primary_metric="dispersion_degree",
        register_preset=REGISTER_PRESET_FULL,
        register_low=DEFAULT_REGISTER_LOW,
        register_high=DEFAULT_REGISTER_HIGH,
        time_step=0.25,
        window_size=4.0,
        analysis_profile=ANALYSIS_PROFILE_OCCUPIED_SPACE,
        observation_mode=OBSERVATION_MODE_EVENT_BOUNDARIES,
        pitch_sampling_override=_PITCH_FROM_PROFILE,
        show_registral_span=False,
        show_occupancy_entropy=False,
        plot_normalized_y=False,
        show_heatmap=True,
        heatmap_mode=DEFAULT_CONCENTRATION_MODE,
        heatmap_normalization=DISPLAY_NORMALIZATION_LOG1P,
        heatmap_colormap=DEFAULT_COLORMAP,
    ),
    PRESET_MOVING_FRAGMENT: AnalysisPresetSpec(
        key=PRESET_MOVING_FRAGMENT,
        summary=(
            "**Moving fragment** — sliding windows on a regular time grid (`fixed_window`, Δt=0.25, w=4 qL). "
            "Tracks registral dispersion over time. Read **`dispersion_degree`** as the canonical curve; "
            "optionally overlay mean pairwise distance. Heatmap bins aligned with time step."
        ),
        primary_metric="dispersion_degree",
        register_preset=REGISTER_PRESET_FULL,
        register_low=DEFAULT_REGISTER_LOW,
        register_high=DEFAULT_REGISTER_HIGH,
        time_step=0.25,
        window_size=4.0,
        analysis_profile=ANALYSIS_PROFILE_OCCUPIED_SPACE,
        observation_mode=OBSERVATION_MODE_FIXED_WINDOW,
        pitch_sampling_override=_PITCH_FROM_PROFILE,
        show_registral_span=False,
        show_occupancy_entropy=False,
        plot_normalized_y=False,
        show_heatmap=True,
        heatmap_mode=DEFAULT_CONCENTRATION_MODE,
        heatmap_normalization=DISPLAY_NORMALIZATION_LOG1P,
        heatmap_colormap=DEFAULT_COLORMAP,
    ),
    PRESET_GLOBAL_SUMMARY: AnalysisPresetSpec(
        key=PRESET_GLOBAL_SUMMARY,
        summary=(
            "**Global summary / one-number** — duration-weighted whole-score summary via "
            "`event_boundaries` + `occupied_space`. Primary: duration-weighted registral span; "
            "secondary: duration-weighted mean pairwise distance. Prefer CLI `summarize` or "
            ":func:`summarize_registral_dispersion` for batch one-number output."
        ),
        primary_metric="duration_weighted_registral_span",
        register_preset=REGISTER_PRESET_FULL,
        register_low=DEFAULT_REGISTER_LOW,
        register_high=DEFAULT_REGISTER_HIGH,
        time_step=0.25,
        window_size=4.0,
        analysis_profile=ANALYSIS_PROFILE_OCCUPIED_SPACE,
        observation_mode=OBSERVATION_MODE_EVENT_BOUNDARIES,
        pitch_sampling_override=_PITCH_FROM_PROFILE,
        show_registral_span=False,
        show_occupancy_entropy=False,
        plot_normalized_y=False,
        show_heatmap=False,
        heatmap_mode=DEFAULT_CONCENTRATION_MODE,
        heatmap_normalization=DISPLAY_NORMALIZATION_LOG1P,
        heatmap_colormap=DEFAULT_COLORMAP,
    ),
}


def one_number_summarize_params() -> dict:
    """Resolved parameter dict for the one-number global summary path (API/CLI defaults)."""
    return dict(DEFAULT_SUMMARIZE_PARAMS)


def preset_guidance_text(preset_key: str | None) -> str:
    """Short markdown blurb for the UI guidance panel."""
    if preset_key == PRESET_CUSTOM or not preset_key:
        return (
            "**Custom** — adjust parameters manually. "
            "See `docs/PARAMETERIZATION_GUIDE.md` for advised static vs moving setups."
        )
    spec = PRESET_SPECS.get(str(preset_key).strip())
    if spec is None:
        return preset_guidance_text(PRESET_CUSTOM)
    return (
        f"### {spec.key}\n\n"
        f"{spec.summary}\n\n"
        f"**Primary metric:** `{spec.primary_metric}` · "
        f"**Profile:** `{spec.analysis_profile}` · "
        f"**Register:** {spec.register_low}–{spec.register_high} · "
        f"**Observation:** `{spec.observation_mode}`"
    )


def apply_analysis_preset(preset_key: str | None):
    """
    Return ``gr.update(...)`` values for all controls affected by a preset.

    ``PRESET_CUSTOM`` leaves controls unchanged (no-op updates).
    """
    import gradio as gr

    noop = gr.update()
    if preset_key == PRESET_CUSTOM or not preset_key:
        return (
            preset_guidance_text(PRESET_CUSTOM),
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
            noop,
        )
    spec = PRESET_SPECS.get(str(preset_key).strip())
    if spec is None:
        return apply_analysis_preset(PRESET_CUSTOM)
    return (
        preset_guidance_text(spec.key),
        gr.update(value=spec.register_preset),
        gr.update(value=spec.register_low),
        gr.update(value=spec.register_high),
        gr.update(value=spec.time_step),
        gr.update(value=spec.window_size),
        gr.update(value=spec.analysis_profile),
        gr.update(value=spec.observation_mode),
        gr.update(value=spec.pitch_sampling_override),
        gr.update(value=spec.show_registral_span),
        gr.update(value=spec.show_occupancy_entropy),
        gr.update(value=spec.plot_normalized_y),
        gr.update(value=spec.show_heatmap),
        gr.update(value=spec.heatmap_mode),
        gr.update(value=spec.heatmap_normalization),
        gr.update(value=spec.heatmap_colormap),
    )
