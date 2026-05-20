"""Compare current summarize output against frozen benchmark JSON."""

from __future__ import annotations

import json
from pathlib import Path

from registral_dispersion.summarize import summarize_registral_dispersion

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "frozen_outputs"
MANIFEST = ROOT / "manifest.json"


def _close(a, b, rtol=0, atol=1e-9) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) <= atol + rtol * abs(float(b))


def compare() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = 0
    for entry in manifest["benchmarks"]:
        if not entry.get("include_in_regression", True):
            continue
        bid = entry["benchmark_id"]
        frozen_path = FROZEN / f"{bid}.json"
        if not frozen_path.is_file():
            print(f"MISSING frozen output: {frozen_path}")
            failures += 1
            continue
        frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
        live = summarize_registral_dispersion(str(ROOT / entry["file_path"]), {})
        if not _close(live["primary_value"], frozen["primary_value"]):
            print(
                f"FAIL {bid}: primary_value live={live['primary_value']} frozen={frozen['primary_value']}"
            )
            failures += 1
        else:
            print(f"OK {bid}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(compare())
