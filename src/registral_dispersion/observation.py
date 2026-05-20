"""Temporal observation modes for registral dispersion (fixed windows vs score-state intervals)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

OBSERVATION_MODE_FIXED_WINDOW = "fixed_window"
OBSERVATION_MODE_EVENT_BOUNDARIES = "event_boundaries"

OBSERVATION_MODES = (OBSERVATION_MODE_FIXED_WINDOW, OBSERVATION_MODE_EVENT_BOUNDARIES)


def normalize_observation_mode(value: Any) -> str:
    """
    Return ``fixed_window`` or ``event_boundaries``.

    Raises ``ValueError`` if the string is non-empty and not a recognized mode.
    """
    if value is None or str(value).strip() == "":
        return OBSERVATION_MODE_FIXED_WINDOW
    s = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    if s in OBSERVATION_MODES:
        return s
    raise ValueError(
        f"Unknown observation_mode {value!r}; expected {OBSERVATION_MODE_FIXED_WINDOW!r} "
        f"or {OBSERVATION_MODE_EVENT_BOUNDARIES!r}."
    )


def collect_sorted_event_boundaries(events: Iterable[Any], score_end_time: float) -> list[float]:
    """
    All times where the set of overlapping ``Note`` / ``Chord`` objects can change, plus the score
    timeline endpoints ``0`` and ``score_end_time`` (quarterLength).

    Uses each event's ``offset`` and ``offset + quarterLength`` together with ``0`` and the score
    duration so gaps before the first attack and after the last release appear as intervals.
    """
    t_end = float(score_end_time)
    boundaries = [0.0, t_end]
    for e in events:
        onset = float(e.offset)
        dur = float(e.quarterLength) if hasattr(e, "quarterLength") else 0.0
        boundaries.append(onset)
        boundaries.append(onset + dur)
    return sorted(set(boundaries))


def iter_positive_duration_intervals(boundaries: list[float], *, eps: float = 1e-12):
    """Yield ``(start, end)`` for each consecutive pair with ``end > start + eps``."""
    for i in range(len(boundaries) - 1):
        a, b = float(boundaries[i]), float(boundaries[i + 1])
        if b > a + eps:
            yield a, b
