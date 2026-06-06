"""Generate deterministic MusicXML fixtures for registral-regression qualitative tests."""

from __future__ import annotations

from pathlib import Path

from music21 import chord, note, stream

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures" / "registral_regression"


def _write(name: str, sc: stream.Score) -> Path:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    path = FIXTURES / name
    sc.write("musicxml", fp=str(path))
    return path


def build_unison_register() -> Path:
    sc = stream.Score()
    for i in range(4):
        p = stream.Part(id=f"P{i + 1}")
        p.partName = f"Unison {i + 1}"
        p.insert(0, note.Note("C4", quarterLength=2.0))
        sc.insert(0, p)
    return _write("unison_register.musicxml", sc)


def build_cluster_middle_register() -> Path:
    p = stream.Part()
    p.partName = "Cluster"
    p.insert(0, chord.Chord(["C4", "D4", "E4", "F4"], quarterLength=2.0))
    return _write("cluster_middle_register.musicxml", stream.Score([p]))


def build_wide_bipolar_register() -> Path:
    p = stream.Part()
    p.partName = "Bipolar"
    p.insert(0, chord.Chord(["C2", "C6"], quarterLength=2.0))
    return _write("wide_bipolar_register.musicxml", stream.Score([p]))


def _expansion_notes() -> list[tuple[float, stream.GeneralObject]]:
    return [
        (0.0, note.Note("C4", quarterLength=1.0)),
        (1.0, chord.Chord(["B3", "D4"], quarterLength=1.0)),
        (2.0, chord.Chord(["A3", "E4"], quarterLength=1.0)),
        (3.0, chord.Chord(["G3", "G4"], quarterLength=1.0)),
        (4.0, chord.Chord(["C3", "C5"], quarterLength=1.0)),
    ]


def build_registral_expansion() -> Path:
    p = stream.Part()
    p.partName = "Expansion"
    for offset, el in _expansion_notes():
        p.insert(offset, el)
    return _write("registral_expansion.musicxml", stream.Score([p]))


def build_registral_contraction() -> Path:
    p = stream.Part()
    p.partName = "Contraction"
    for i, (_offset, el) in enumerate(reversed(_expansion_notes())):
        p.insert(float(i), el)
    return _write("registral_contraction.musicxml", stream.Score([p]))


def build_high_register_concentration() -> Path:
    p = stream.Part()
    p.partName = "High cluster"
    p.insert(0, chord.Chord(["C6", "E6", "G6"], quarterLength=2.0))
    return _write("high_register_concentration.musicxml", stream.Score([p]))


def build_low_register_concentration() -> Path:
    p = stream.Part()
    p.partName = "Low cluster"
    p.insert(0, chord.Chord(["C2", "E2", "G2"], quarterLength=2.0))
    return _write("low_register_concentration.musicxml", stream.Score([p]))


def build_same_span_sparse_extremes() -> Path:
    p = stream.Part()
    p.partName = "Sparse extremes"
    p.insert(0, chord.Chord(["C3", "C5"], quarterLength=2.0))
    return _write("same_span_sparse_extremes.musicxml", stream.Score([p]))


def build_same_span_filled_middle() -> Path:
    p = stream.Part()
    p.partName = "Filled middle"
    p.insert(0, chord.Chord(["C3", "G3", "C4", "E4", "G4", "C5"], quarterLength=2.0))
    return _write("same_span_filled_middle.musicxml", stream.Score([p]))


def build_all() -> dict[str, Path]:
    builders = {
        "unison_register": build_unison_register,
        "cluster_middle_register": build_cluster_middle_register,
        "wide_bipolar_register": build_wide_bipolar_register,
        "registral_expansion": build_registral_expansion,
        "registral_contraction": build_registral_contraction,
        "high_register_concentration": build_high_register_concentration,
        "low_register_concentration": build_low_register_concentration,
        "same_span_sparse_extremes": build_same_span_sparse_extremes,
        "same_span_filled_middle": build_same_span_filled_middle,
    }
    return {name: fn() for name, fn in builders.items()}


def main() -> None:
    paths = build_all()
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
