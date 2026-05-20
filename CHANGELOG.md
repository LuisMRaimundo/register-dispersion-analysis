# Changelog

## 0.3.0 (2026-05-20)

- Built-in **global summary** (`global_summary`) on every analysis run.
- **One-number API:** `summarize_registral_dispersion`.
- **One-number CLI:** `python -m registral_dispersion summarize`.
- **`tie_policy`:** `as_imported` (default) and `merge_ties` via music21 `stripTies()`.
- **Interpretation warnings** for profile/sampling overrides and fixed-window one-number use.
- **JSON schema 1.8:** `global_summary`, `warnings`, `tie_policy`, `symbolic_score_only`.
- Separate **global summary CSV** export on batch `analyze`.
- **Benchmarks/** synthetic fixtures with frozen summarize outputs (regression only).
- No change to per-row dispersion **formulas**; defaults preserved (`occupied_space`, `fixed_window` for full analysis).

## 0.2.1

- Canonical **`dispersion_degree`** field (alias of `registral_span`).

## 0.2.0

- Initial registral-dispersion release with profiles, event boundaries, concentration map.
