"""Gradio upload validation and numeric coercion."""

from __future__ import annotations

import os

import gradio as gr

from registral_dispersion.score_io import ScoreValidationError, validate_score_path

VALID_SCORE_EXTENSIONS_UI = frozenset({".xml", ".musicxml", ".mxl", ".mid", ".midi"})


def coerce_float(x, default: float) -> float:
    """Coerce to float; use default if None or empty."""
    if x is None or x == "":
        return float(default)
    try:
        return float(x)
    except (TypeError, ValueError):
        return float(default)


def validate_uploaded_score(file_obj) -> str:
    """Return path to uploaded score or raise gr.Error."""
    if file_obj is None:
        raise gr.Error("Upload a MusicXML (.xml/.musicxml/.mxl) or MIDI (.mid/.midi) file.")
    score_path = file_obj.name
    if not os.path.exists(score_path):
        raise gr.Error("Uploaded file path not found.")
    ext = os.path.splitext(score_path)[1].lower()
    if ext not in VALID_SCORE_EXTENSIONS_UI:
        raise gr.Error("Unsupported file type. Use MusicXML or MIDI.")
    try:
        validate_score_path(score_path)
    except ScoreValidationError as e:
        raise gr.Error(str(e)) from e
    return score_path
