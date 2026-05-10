"""Moment-cumulant inversion identity on a small Slater determinant.

Section II of the manuscript: the ordered classical partition cumulants
satisfy mu_[m] = sum_{pi in Pi_m} prod_B kappa_B. This test verifies the
identity numerically on a 4-orbital determinant for length-3 and length-4
neutral words.
"""

from __future__ import annotations

import math

from connected_layer_sector import (
    determinant_state,
    ordered_cumulant,
    set_partitions,
    word_moment,
)


def test_moment_cumulant_identity_length_3():
    """mu_[3](W; rho) = sum_{pi in Pi_3} prod_B kappa_B(W; rho)."""
    n_orb = 4
    rho = determinant_state(n_orb, [1, 1, 0, 0])
    word = (("n", 0), ("n", 1), ("n", 2))

    mu_top = word_moment(rho, word, n_orb)
    rebuilt = 0.0 + 0.0j
    for pi in set_partitions(range(len(word))):
        prod = 1.0 + 0.0j
        for block in pi:
            prod *= ordered_cumulant(rho, word, tuple(block), n_orb)
        rebuilt += prod
    assert math.isclose(mu_top.real, rebuilt.real, abs_tol=1e-12)
    assert math.isclose(mu_top.imag, rebuilt.imag, abs_tol=1e-12)


def test_moment_cumulant_identity_length_4():
    """mu_[4](W; rho) = sum_{pi in Pi_4} prod_B kappa_B."""
    n_orb = 4
    rho = determinant_state(n_orb, [1, 1, 0, 0])
    word = (("n", 0), ("n", 1), ("n", 2), ("n", 3))

    mu_top = word_moment(rho, word, n_orb)
    rebuilt = 0.0 + 0.0j
    for pi in set_partitions(range(len(word))):
        prod = 1.0 + 0.0j
        for block in pi:
            prod *= ordered_cumulant(rho, word, tuple(block), n_orb)
        rebuilt += prod
    assert math.isclose(mu_top.real, rebuilt.real, abs_tol=1e-12)
    assert math.isclose(mu_top.imag, rebuilt.imag, abs_tol=1e-12)


def test_kappa_top_vanishes_on_determinant():
    """Section V worked example: every catalog cumulant of length 3 or 4
    vanishes on a Slater determinant, evaluated in the occupation basis."""
    n_orb = 4
    rho = determinant_state(n_orb, [1, 1, 0, 0])

    # Length-3 number-only word
    w3 = (("n", 0), ("n", 1), ("n", 2))
    k3 = ordered_cumulant(rho, w3, list(range(3)), n_orb)
    assert abs(k3) < 1e-12

    # Length-4 number-only word
    w4 = (("n", 0), ("n", 1), ("n", 2), ("n", 3))
    k4 = ordered_cumulant(rho, w4, list(range(4)), n_orb)
    assert abs(k4) < 1e-12
