"""Generate benchmark MusicXML fixtures and frozen summarize JSON outputs."""

from __future__ import annotations

import json
from pathlib import Path

from music21 import chord, note, stream
from music21.tie import Tie

from registral_dispersion.summarize import summarize_registral_dispersion

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures"
FROZEN = ROOT / "frozen_outputs"
MANIFEST = ROOT / "manifest.json"


def _write(name: str, sc: stream.Score) -> Path:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    path = FIXTURES / name
    sc.write("musicxml", fp=str(path))
    return path


def build_fixtures() -> dict[str, Path]:
    out: dict[str, Path] = {}

    p = stream.Part()
    p.insert(0, chord.Chord(["C4", "D4"], quarterLength=2.0))
    out["narrow_cluster"] = _write("narrow_cluster.musicxml", stream.Score([p]))

    p = stream.Part()
    p.insert(0, chord.Chord(["C3", "C6"], quarterLength=2.0))
    out["wide_span"] = _write("wide_span.musicxml", stream.Score([p]))

    p1 = stream.Part()
    p2 = stream.Part()
    p1.insert(0, note.Note("C4", quarterLength=2.0))
    p2.insert(0, note.Note("C4", quarterLength=2.0))
    sc = stream.Score()
    sc.insert(0, p1)
    sc.insert(0, p2)
    out["octave_doublings"] = _write("octave_doublings.musicxml", sc)

    p = stream.Part()
    p.insert(0, note.Note("C3", quarterLength=2.0))
    p.insert(2, note.Note("C6", quarterLength=2.0))
    out["register_shift"] = _write("register_shift.musicxml", stream.Score([p]))

    p = stream.Part()
    p.insert(0, note.Note("C4", quarterLength=1.0))
    p.insert(3, note.Note("D4", quarterLength=1.0))
    out["rest_gap"] = _write("rest_gap.musicxml", stream.Score([p]))

    p = stream.Part()
    n1 = note.Note("C4", quarterLength=1.0)
    n2 = note.Note("C4", quarterLength=1.0)
    n1.tie = Tie("start")
    n2.tie = Tie("stop")
    p.insert(0, n1)
    p.insert(1, n2)
    out["tied_sustain"] = _write("tied_sustain.musicxml", stream.Score([p]))

    p = stream.Part()
    p.insert(0, chord.Chord(["C4", "E4", "G4"], quarterLength=2.0))
    out["chord_texture"] = _write("chord_texture.musicxml", stream.Score([p]))

    return out


def generate_frozen() -> None:
    build_fixtures()
    FROZEN.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in manifest["benchmarks"]:
        bid = entry["benchmark_id"]
        path = ROOT / entry["file_path"]
        result = summarize_registral_dispersion(str(path), {})
        out_path = FROZEN / f"{bid}.json"
        payload = {
            "benchmark_id": bid,
            "score_path": entry["file_path"],
            "primary_metric": result["primary_metric"],
            "primary_value": result["primary_value"],
            "secondary_metric": result["secondary_metric"],
            "secondary_value": result["secondary_value"],
            "global_summary": result["global_summary"],
            "params": result["params"],
        }
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    generate_frozen()
