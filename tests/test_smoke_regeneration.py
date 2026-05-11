"""Pipeline reproducibility smoke test.

Regenerates a tiny fixed cell from code and compares to the deposited
calibration JSON, excluding volatile fields. Distinct from
`test_data_integrity` (which only verifies the deposited file is unchanged):
this one verifies the *pipeline* can produce that result.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from connected_layer_sector import (
    evaluate_catalog,
    fermionic_orbital_rotation,
    hubbard_ground_state,
    tight_binding_eigenbasis,
)

ROOT = Path(__file__).resolve().parent.parent
CALIB = ROOT / "data" / "calibration_chemistry.json"


def _hubbard_at(n_sites: int, U: float) -> dict:
    n_orb = 2 * n_sites
    psi, e0 = hubbard_ground_state(n_sites, t=1.0, U=U, n_up=n_sites // 2, n_dn=n_sites // 2)
    eps, V_mat = tight_binding_eigenbasis(n_sites, t=1.0)
    W_full = np.zeros((n_orb, n_orb))
    W_full[:n_sites, :n_sites] = V_mat
    W_full[n_sites:, n_sites:] = V_mat
    V = fermionic_orbital_rotation(W_full, n_orb)
    psi_rot = V @ psi
    psi_rot = psi_rot / np.linalg.norm(psi_rot)
    rho = np.outer(psi_rot, psi_rot.conj())
    return {"E_ground": e0, **evaluate_catalog(rho, n_orb, r=4)}


def test_regenerate_hubbard_u0_baseline():
    """Run the pipeline at U=0 and confirm Delta^cat is floating-point zero
    AND the energy matches the closed-form -2*sum(2t cos(k pi/(n+1))) sum
    over k=1..n/2 per spin."""
    out = _hubbard_at(n_sites=4, U=0.0)
    # Closed-form half-filled n=4 open chain energy: 2 * (e_1 + e_2)
    # where e_k = -2 cos(k pi / 5).
    e_expected = 2 * (-2 * math.cos(math.pi / 5) - 2 * math.cos(2 * math.pi / 5))
    assert math.isclose(out["E_ground"], e_expected, abs_tol=1e-9)
    assert out["delta_cat"] < 1e-12
    assert out["max_tau"] < 1e-12


def test_regenerate_hubbard_u1_matches_deposit():
    """Run the pipeline at U=1 and compare to the deposited calibration
    row, excluding volatile fields. Tolerance: 1e-9 on each metric.

    Fails (does not silent-skip) if the deposit or its U/t=1 row is
    missing -- those conditions indicate a broken deposit, not an
    expected runtime state.
    """
    import pytest

    if not CALIB.exists():
        pytest.fail(
            f"Calibration deposit missing at {CALIB}; "
            "test_data_integrity should have caught this first"
        )
    rows = json.loads(CALIB.read_text(encoding="utf-8"))["hubbard"]
    deposit = next(
        (r for r in rows if r["U_over_t"] == 1.0 and r["n_sites"] == 4),
        None,
    )
    if deposit is None:
        pytest.fail(
            "Calibration deposit missing the U/t=1, n_sites=4 row; "
            "regenerate with `cls-calibrate --Ut 0 1 4 8 16`"
        )

    fresh = _hubbard_at(n_sites=4, U=1.0)
    for key in ("E_ground", "delta_cat", "max_tau"):
        assert math.isclose(fresh[key], deposit[key], abs_tol=1e-9), (
            f"smoke regeneration mismatch on {key}: "
            f"fresh={fresh[key]:.6e}, deposited={deposit[key]:.6e}"
        )
