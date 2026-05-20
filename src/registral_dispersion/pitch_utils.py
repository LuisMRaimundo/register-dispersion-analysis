"""Note-name helpers and register-band presets."""

from __future__ import annotations

import music21 as m21

# Full practical notated range (piano + orchestral extremes).
DEFAULT_REGISTER_LOW = "A0"
DEFAULT_REGISTER_HIGH = "C8"

REGISTER_PRESET_FULL = "A0 to C8 (full notated range)"

# Legacy labels — not offered in UI; resolve to the full-range preset.
_LEGACY_REGISTER_PRESET_A0_B7 = "A0 to B7 (full notated range)"
_LEGACY_REGISTER_PRESET_ORCHESTRAL = "A1 to E7 (orchestral band)"

REGISTER_PRESETS: dict[str, tuple[str, str]] = {
    REGISTER_PRESET_FULL: ("A0", "C8"),
}


def note_name_to_midi_ps(note_name: str) -> float:
    """Convert a note name (e.g. 'A0', 'A1', 'C8') to MIDI pitch space (float)."""
    p = m21.pitch.Pitch(note_name.strip())
    return float(p.ps)


def resolve_register_preset(preset_label: str | None) -> tuple[str, str] | None:
    """Return ``(register_low, register_high)`` note names for a preset label, or ``None`` if unknown."""
    if preset_label is None:
        return None
    key = str(preset_label).strip()
    if key in (_LEGACY_REGISTER_PRESET_A0_B7, _LEGACY_REGISTER_PRESET_ORCHESTRAL):
        return REGISTER_PRESETS[REGISTER_PRESET_FULL]
    if key in REGISTER_PRESETS:
        return REGISTER_PRESETS[key]
    return None
