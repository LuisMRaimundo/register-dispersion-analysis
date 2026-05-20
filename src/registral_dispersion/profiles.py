"""Analysis profiles: link research interpretation to pitch sampling (no formula changes)."""

from __future__ import annotations

from registral_dispersion.sampling import (
    PITCH_SAMPLING_EVENT_INSTANCES,
    PITCH_SAMPLING_UNIQUE_PITCH_HEIGHTS,
    normalize_pitch_sampling_mode,
)

ANALYSIS_PROFILE_OCCUPIED_SPACE = "occupied_space"
ANALYSIS_PROFILE_COMPONENT_WEIGHTED = "component_weighted"

ANALYSIS_PROFILES = frozenset({ANALYSIS_PROFILE_OCCUPIED_SPACE, ANALYSIS_PROFILE_COMPONENT_WEIGHTED})

# Research-facing default: density-independent occupied registral geometry (implies unique_pitch_heights).
DEFAULT_ANALYSIS_PROFILE = ANALYSIS_PROFILE_OCCUPIED_SPACE


def normalize_analysis_profile(value) -> str:
    """Return a supported profile; default ``occupied_space`` if missing or unknown."""
    if value is None or value == "":
        return DEFAULT_ANALYSIS_PROFILE
    s = str(value).strip().lower().replace("-", "_")
    if s in ANALYSIS_PROFILES:
        return s
    return DEFAULT_ANALYSIS_PROFILE


def implied_pitch_sampling_mode(profile: str) -> str:
    """Sampling mode implied by ``analysis_profile`` (used when ``pitch_sampling_mode`` is not overridden)."""
    p = normalize_analysis_profile(profile)
    if p == ANALYSIS_PROFILE_OCCUPIED_SPACE:
        return PITCH_SAMPLING_UNIQUE_PITCH_HEIGHTS
    return PITCH_SAMPLING_EVENT_INSTANCES


def resolve_profile_and_pitch_sampling(
    analysis_profile: str | None,
    pitch_sampling_mode: str | None,
    *,
    pitch_sampling_explicit: bool,
) -> tuple[str, str, str]:
    """
    Single source of truth for profile + pitch sampling (matches :func:`resolve_registral_dispersion_params`).

    Returns ``(normalized_profile, normalized_pitch_sampling_mode, pitch_sampling_source)``.

    * If ``pitch_sampling_explicit`` is false, ``pitch_sampling_mode`` is ignored and implied from the profile
      (``pitch_sampling_source`` = ``\"analysis_profile\"``).
    * If true, the provided ``pitch_sampling_mode`` is normalized and used (``\"explicit_param\"``).
    """
    prof = normalize_analysis_profile(analysis_profile)
    if pitch_sampling_explicit:
        return prof, normalize_pitch_sampling_mode(pitch_sampling_mode), "explicit_param"
    return prof, implied_pitch_sampling_mode(prof), "analysis_profile"
