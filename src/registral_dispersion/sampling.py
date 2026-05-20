"""Pitch sampling modes for registral dispersion (notational aggregation)."""

from __future__ import annotations

PITCH_SAMPLING_EVENT_INSTANCES = "event_instances"
PITCH_SAMPLING_UNIQUE_PITCH_HEIGHTS = "unique_pitch_heights"

PITCH_SAMPLING_MODES = frozenset({PITCH_SAMPLING_EVENT_INSTANCES, PITCH_SAMPLING_UNIQUE_PITCH_HEIGHTS})

DEFAULT_PITCH_SAMPLING_MODE = PITCH_SAMPLING_EVENT_INSTANCES


def normalize_pitch_sampling_mode(value) -> str:
    """Return a supported mode string; default to ``event_instances`` if missing or unknown."""
    if value is None or value == "":
        return DEFAULT_PITCH_SAMPLING_MODE
    s = str(value).strip().lower().replace("-", "_")
    if s in PITCH_SAMPLING_MODES:
        return s
    return DEFAULT_PITCH_SAMPLING_MODE


NOTATIONAL_SAMPLING_SUMMARY = (
    "Active components are drawn from ``music21.stream.Stream.flatten().notes`` on the parsed score: "
    "each ``Note`` and each ``Chord`` overlapping the analysis window contributes pitch values. "
    "Window membership uses **notated overlap**: a component is active if its onset is before the window end "
    "and its onset plus **notated quarterLength** is after the window start (sustained soundings count without "
    "requiring an attack inside the window). Chord members are read as separate MIDI heights. "
    "All parts are merged via ``flatten()`` before listing, so cross-part aggregates are joint. "
    "**Ties:** the engine uses whatever objects the importer leaves in the flat stream; tied chains may appear "
    "as one long ``Note`` or as several tied segments depending on the file and music21; each overlapping "
    "``Note``/``Chord`` object contributes once per object (no extra tie-aware merge in this step). "
    "**Sampling mode:** ``event_instances`` keeps every contributed MIDI value (duplicate heights from "
    "different parts or repeated noteheads both count separately). ``unique_pitch_heights`` collapses to "
    "distinct MIDI pitch numbers within the window before span/pairwise/entropy."
)
