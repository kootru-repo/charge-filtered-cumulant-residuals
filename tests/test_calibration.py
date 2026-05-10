"""Calibration sanity checks (matching the asserts in
notebooks/04_correlated_calibration.ipynb)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CALIB = ROOT / "data" / "calibration_chemistry.json"


def _load_calibration() -> dict:
    return json.loads(CALIB.read_text(encoding="utf-8"))


def test_calibration_present():
    assert CALIB.exists()


def test_u0_baseline_is_floating_point_zero():
    """Manuscript Section V worked example: in the U=0 noninteracting
    eigenbasis the Hubbard half-filled ground state is occupation-diagonal,
    so Delta^cat must be zero. Numerical floor: < 1e-12."""
    rows = _load_calibration()["hubbard"]
    u0 = next(r for r in rows if r["U_over_t"] == 0.0)
    assert u0["delta_cat"] < 1e-12, (
        f"U=0 baseline failed Sec V: delta_cat = {u0['delta_cat']:.2e}"
    )


def test_delta_cat_monotone_in_U_over_t():
    """Delta^cat should grow non-decreasingly with U/t (Mott build-up)."""
    rows = _load_calibration()["hubbard"]
    rows = sorted(rows, key=lambda r: r["U_over_t"])
    deltas = [r["delta_cat"] for r in rows]
    for i in range(len(deltas) - 1):
        assert deltas[i + 1] >= deltas[i] - 1e-12, (
            f"non-monotonic at U/t={rows[i+1]['U_over_t']}: "
            f"prev={deltas[i]:.4f} next={deltas[i+1]:.4f}"
        )


def test_eta_universal_below_one():
    """The universal partition-lattice constant B_4 = 105 is loose on this
    catalog and state; eta_universal must stay well below 1."""
    rows = _load_calibration()["hubbard"]
    etas = [r["eta_universal"] for r in rows
            if r["eta_universal"] == r["eta_universal"]]  # filter NaN
    assert max(etas) < 0.1, (
        f"eta_universal exceeded 0.1: max={max(etas):.4f}"
    )
