"""Shared pytest fixtures."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def small_slater_state():
    """A 4-orbital determinant |1,1,0,0> as a pure-state density matrix.

    Returned as (rho, n_orb) ready for the catalog pipeline. Used as a
    Sec V baseline for tests that need a fixed-N occupation-diagonal
    product state.
    """
    from connected_layer_sector import determinant_state
    n_orb = 4
    rho = determinant_state(n_orb, [1, 1, 0, 0])
    return rho, n_orb


@pytest.fixture
def hubbard_n4_u0():
    """Hubbard ground state at n_sites=4, U/t=0, half-filled.

    Returned in the U=0 noninteracting eigenbasis (the dictionary basis
    where the Sec V worked-example zero applies). Used as the principal
    smoke-regeneration fixture.
    """
    from connected_layer_sector import (
        fermionic_orbital_rotation,
        hubbard_ground_state,
        tight_binding_eigenbasis,
    )

    n_sites = 4
    n_orb = 2 * n_sites
    psi, e0 = hubbard_ground_state(n_sites, t=1.0, U=0.0, n_up=2, n_dn=2)

    eps, V_mat = tight_binding_eigenbasis(n_sites, t=1.0)
    W_full = np.zeros((n_orb, n_orb))
    W_full[:n_sites, :n_sites] = V_mat
    W_full[n_sites:, n_sites:] = V_mat
    V = fermionic_orbital_rotation(W_full, n_orb)
    psi_rot = V @ psi
    psi_rot = psi_rot / np.linalg.norm(psi_rot)
    rho = np.outer(psi_rot, psi_rot.conj())
    return rho, n_orb, e0
