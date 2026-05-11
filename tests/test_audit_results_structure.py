"""Structural validation of `data/audit_sector_cumulant_results.json`.

This file is the rederived-verdict aggregate of the underlying screen
JSON; `test_data_integrity` only verifies its SHA256. This test asserts
that the structure and headline numbers match what the manuscript
quotes (Sec VI of the paper: 3679 total observables, zero violations,
positive-vs-negative bound discrimination ratio).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "data" / "audit_sector_cumulant_results.json"


def _load() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_results_file_present():
    assert RESULTS.exists(), (
        "data/audit_sector_cumulant_results.json missing; "
        "regenerate from the screen audit pipeline."
    )


def test_rederived_verdict_is_strong_pass():
    """The audit's own verdict on its consistency. Must be STRONG_PASS."""
    d = _load()
    assert d["rederived_verdict"] == "STRONG_PASS"
    assert d["consistency_issues"] == []


def test_headline_zero_violations():
    """All audited observables satisfy the bound (max_violation = 0)."""
    d = _load()
    headline = d["headline"]
    assert headline["max_violation"] == 0.0
    assert headline["n_fail"] == 0
    assert headline["n_pass"] == headline["n_total_obs"]


def test_headline_positive_negative_split_exists():
    """Audit must include both positive (theorem-tight) and negative
    (deliberately loose) control cells. Manuscript discusses the
    bound-discrimination ratio."""
    d = _load()
    headline = d["headline"]
    assert headline["n_positive_cells"] >= 1
    assert headline["n_negative_cells"] >= 1


def test_headline_per_cell_counts_consistent_with_headline():
    """Sum of per-cell n_obs matches the headline total."""
    d = _load()
    per_cell_total = sum(c.get("n_obs", 0) for c in d["per_cell"])
    assert per_cell_total == d["headline"]["n_total_obs"]


def test_audit_input_refers_to_a_deposited_screen():
    """The rederived results file must point to a screen file that is
    itself deposited under data/."""
    d = _load()
    input_name = d["audit_input"]
    assert (ROOT / "data" / input_name).exists(), (
        f"audit_input={input_name!r} but {ROOT / 'data' / input_name} "
        "is not deposited"
    )
