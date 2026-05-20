"""Benchmark manifest and frozen-output regression tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from registral_dispersion.profiles import ANALYSIS_PROFILE_COMPONENT_WEIGHTED, ANALYSIS_PROFILE_OCCUPIED_SPACE
from registral_dispersion.summarize import summarize_registral_dispersion
from registral_dispersion.tie_policy import TIE_POLICY_AS_IMPORTED, TIE_POLICY_MERGE_TIES

BENCH_ROOT = Path(__file__).resolve().parent.parent / "benchmarks"
MANIFEST = BENCH_ROOT / "manifest.json"
FROZEN = BENCH_ROOT / "frozen_outputs"


class TestBenchmarkManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MANIFEST.is_file():
            raise unittest.SkipTest("Benchmark manifest not found; run generate_frozen_outputs.py")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_loads(self):
        self.assertIn("benchmarks", self.manifest)
        self.assertGreaterEqual(len(self.manifest["benchmarks"]), 7)

    def test_all_fixture_files_exist(self):
        for entry in self.manifest["benchmarks"]:
            path = BENCH_ROOT / entry["file_path"]
            self.assertTrue(path.is_file(), msg=str(path))

    def test_frozen_outputs_exist(self):
        for entry in self.manifest["benchmarks"]:
            if not entry.get("include_in_regression", True):
                continue
            frozen = FROZEN / f"{entry['benchmark_id']}.json"
            self.assertTrue(frozen.is_file(), msg=str(frozen))

    def test_narrow_smaller_than_wide(self):
        narrow = summarize_registral_dispersion(str(BENCH_ROOT / "fixtures/narrow_cluster.musicxml"), {})
        wide = summarize_registral_dispersion(str(BENCH_ROOT / "fixtures/wide_span.musicxml"), {})
        self.assertLess(narrow["primary_value"], wide["primary_value"])

    def test_octave_doublings_profile_contrast(self):
        path = str(BENCH_ROOT / "fixtures/octave_doublings.musicxml")
        occ = summarize_registral_dispersion(path, {"analysis_profile": ANALYSIS_PROFILE_OCCUPIED_SPACE})
        comp = summarize_registral_dispersion(path, {"analysis_profile": ANALYSIS_PROFILE_COMPONENT_WEIGHTED})
        self.assertAlmostEqual(occ["primary_value"], 0.0)
        self.assertAlmostEqual(comp["secondary_value"], 0.0)
        self.assertEqual(comp["global_summary"]["max_active_note_count"], 2)

    def test_rest_gap_empty_interval(self):
        out = run_event(str(BENCH_ROOT / "fixtures/rest_gap.musicxml"))
        gs = out["global_summary"]
        self.assertGreaterEqual(gs["n_empty_intervals"], 1)

    def test_tie_policy_merge_fewer_intervals(self):
        path = str(BENCH_ROOT / "fixtures/tied_sustain.musicxml")
        imported = summarize_registral_dispersion(path, {"tie_policy": TIE_POLICY_AS_IMPORTED})
        merged = summarize_registral_dispersion(path, {"tie_policy": TIE_POLICY_MERGE_TIES})
        self.assertGreater(
            imported["global_summary"]["n_intervals"],
            merged["global_summary"]["n_intervals"],
        )


def run_event(score_path: str):
    return summarize_registral_dispersion(score_path, {})


if __name__ == "__main__":
    unittest.main()
