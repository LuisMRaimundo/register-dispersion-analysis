"""Qualitative invariant tests for controlled registral-regression MusicXML fixtures."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from registral_dispersion.concentration_map import build_registral_concentration_matrix
from registral_dispersion.observation import OBSERVATION_MODE_EVENT_BOUNDARIES
from registral_dispersion.profiles import ANALYSIS_PROFILE_OCCUPIED_SPACE
from registral_dispersion.service import run_registral_dispersion_analysis

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "corpus" / "fixtures" / "registral_regression"
DOCS = REPO_ROOT / "docs" / "REGISTRAL_REGRESSION_FIXTURES.md"

ANALYSIS_PARAMS = {
    "observation_mode": OBSERVATION_MODE_EVENT_BOUNDARIES,
    "analysis_profile": ANALYSIS_PROFILE_OCCUPIED_SPACE,
    "register_low": "A0",
    "register_high": "C8",
    "time_step": 0.25,
    "window_size": 4.0,
    "tie_policy": "as_imported",
}

FIXTURE_NAMES = (
    "unison_register",
    "cluster_middle_register",
    "wide_bipolar_register",
    "registral_expansion",
    "registral_contraction",
    "high_register_concentration",
    "low_register_concentration",
    "same_span_sparse_extremes",
    "same_span_filled_middle",
)


def _fixture_path(name: str) -> Path:
    return FIXTURES / f"{name}.musicxml"


def _analyze(name: str) -> dict:
    path = _fixture_path(name)
    if not path.is_file():
        pytest.skip(f"Fixture not found: {path}")
    out = run_registral_dispersion_analysis(str(path), ANALYSIS_PARAMS)
    assert out.get("error") is None, out.get("error")
    return out


def _finite_spans(results: dict) -> np.ndarray:
    spans = np.asarray(results["registral_span"], dtype=float)
    return spans[np.isfinite(spans)]


def _single_row_metrics(name: str) -> dict[str, float]:
    results = _analyze(name)["results"]
    spans = _finite_spans(results)
    assert spans.size >= 1
    idx = int(np.argmax(np.asarray(results["registral_span"], dtype=float) == spans[0]))
    return {
        "span": float(results["registral_span"][idx]),
        "pairwise": float(results["mean_pairwise_registral_distance"][idx]),
        "entropy": float(results["occupancy_entropy"][idx]),
        "active_note_count": float(results["active_note_count"][idx]),
    }


def _concentration_mean_midi(name: str) -> float:
    path = _fixture_path(name)
    bundle = build_registral_concentration_matrix(
        str(path),
        21.0,
        108.0,
        time_bin_size=1.0,
        concentration_mode="unique_pitch_heights",
    )
    mat = np.asarray(bundle["matrix"], dtype=float)
    mids = np.asarray(bundle["pitch_midi"], dtype=int)
    active = mids[np.any(mat > 0, axis=1)]
    assert active.size > 0
    weights = mat[np.any(mat > 0, axis=1)].sum(axis=1)
    return float(np.average(active, weights=weights))


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_all_registral_regression_fixtures_parse(name: str) -> None:
    out = _analyze(name)
    assert "results" in out
    assert len(out["results"]["t"]) >= 1


def test_unison_register_has_zero_or_minimal_span() -> None:
    m = _single_row_metrics("unison_register")
    assert m["span"] == 0.0
    assert m["pairwise"] == 0.0
    assert m["entropy"] == 0.0


def test_cluster_middle_less_spread_than_wide_bipolar() -> None:
    cluster = _single_row_metrics("cluster_middle_register")
    wide = _single_row_metrics("wide_bipolar_register")
    assert cluster["span"] < wide["span"]
    assert cluster["pairwise"] < wide["pairwise"]


def test_wide_bipolar_has_largest_span_in_fixture_set() -> None:
    wide_span = _single_row_metrics("wide_bipolar_register")["span"]
    others = [_single_row_metrics(name)["span"] for name in FIXTURE_NAMES if name != "wide_bipolar_register"]
    assert wide_span >= max(others)


def test_registral_expansion_increases_span_over_time() -> None:
    spans = _finite_spans(_analyze("registral_expansion")["results"])
    assert spans.size >= 2
    assert spans[-1] > spans[0]
    assert np.all(np.diff(spans) >= 0)


def test_registral_contraction_decreases_span_over_time() -> None:
    spans = _finite_spans(_analyze("registral_contraction")["results"])
    assert spans.size >= 2
    assert spans[-1] < spans[0]
    assert np.all(np.diff(spans) <= 0)


def test_high_low_register_concentration_same_dispersion_different_location() -> None:
    high = _single_row_metrics("high_register_concentration")
    low = _single_row_metrics("low_register_concentration")
    assert high["span"] == pytest.approx(low["span"])
    assert high["pairwise"] == pytest.approx(low["pairwise"])
    assert high["entropy"] == pytest.approx(low["entropy"])
    assert _concentration_mean_midi("high_register_concentration") > _concentration_mean_midi(
        "low_register_concentration"
    )


def test_same_span_different_internal_distribution() -> None:
    sparse = _single_row_metrics("same_span_sparse_extremes")
    filled = _single_row_metrics("same_span_filled_middle")
    assert sparse["span"] == pytest.approx(filled["span"])
    assert filled["pairwise"] < sparse["pairwise"]
    assert filled["entropy"] > sparse["entropy"]
    assert filled["active_note_count"] > sparse["active_note_count"]


def test_concentration_map_reflects_high_vs_low_register_location() -> None:
    high_mean = _concentration_mean_midi("high_register_concentration")
    low_mean = _concentration_mean_midi("low_register_concentration")
    assert high_mean > 72
    assert low_mean < 48


def test_documentation_lists_all_fixtures() -> None:
    if not DOCS.is_file():
        pytest.skip("Documentation not found")
    text = DOCS.read_text(encoding="utf-8")
    for name in FIXTURE_NAMES:
        assert name in text
