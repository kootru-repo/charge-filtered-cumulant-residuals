"""Charge-counting recurrence (Lemma 1) and worked example
B^charge_4(a^d a n n) = 53.

Manuscript reference: Section III, Lemma 1 and the "Worked example for the
recurrence" paragraph immediately after.
"""

from __future__ import annotations

import math

from connected_layer_sector.constants import (
    B_charge_r,
    charge_filtered_polynomial,
    evaluate_polynomial,
)


def test_worked_example_B_charge_4():
    """Manuscript Section III worked example.

    For W = a^dagger_i a_j n_k n_l with charge multiset (h=1, z=2):
      P_{1,2}(x) = x + 3 x^2 + x^3
      Q_{1,2}(x) = x^2 + x^3
      B^charge_4(W) = (P_{1,2}(M_4) - Q_{1,2}(M_4)) / M_4
                    = (P_{1,2}(26) - Q_{1,2}(26)) / 26 = (19630 - 18252)/26 = 53.
    """
    P, Q = charge_filtered_polynomial(1, 2)
    # Polynomials match the manuscript closed forms.
    # P = x + 3 x^2 + x^3, so coeffs = [0, 1, 3, 1]
    assert math.isclose(P[0], 0.0, abs_tol=1e-12)
    assert math.isclose(P[1], 1.0, abs_tol=1e-12)
    assert math.isclose(P[2], 3.0, abs_tol=1e-12)
    assert math.isclose(P[3], 1.0, abs_tol=1e-12)
    # Q = x^2 + x^3, coeffs = [0, 0, 1, 1]
    assert math.isclose(Q[0], 0.0, abs_tol=1e-12)
    assert math.isclose(Q[1], 0.0, abs_tol=1e-12)
    assert math.isclose(Q[2], 1.0, abs_tol=1e-12)
    assert math.isclose(Q[3], 1.0, abs_tol=1e-12)

    # Closed-form arithmetic at M_4 = 26
    P_26 = evaluate_polynomial(P, 26.0)
    Q_26 = evaluate_polynomial(Q, 26.0)
    assert math.isclose(P_26, 19630.0, abs_tol=1e-9)
    assert math.isclose(Q_26, 18252.0, abs_tol=1e-9)

    # The headline charge-filtered constant
    assert math.isclose(B_charge_r(1, 2, 4), 53.0, abs_tol=1e-9)


def test_worked_example_B_charge_5():
    """Same word, r=5. Manuscript: B^charge_5 = 301."""
    assert math.isclose(B_charge_r(1, 2, 5), 301.0, abs_tol=1e-9)


def test_zero_charge_word_recurrence_consistency():
    """For h=0 (no charged letters) the recurrence reduces to ordinary
    set-partition counts, weighted by x^{|pi|}. P_{0,z} should evaluate to a
    polynomial whose value at x=1 equals the Bell number B_z, since every
    set partition of [z] has zero charge."""
    from connected_layer_sector.partition_lattice import set_partitions

    for z in range(1, 5):
        P, _ = charge_filtered_polynomial(0, z)
        assert math.isclose(
            evaluate_polynomial(P, 1.0),
            sum(1 for _ in set_partitions(range(z))),
            abs_tol=1e-9,
        )
