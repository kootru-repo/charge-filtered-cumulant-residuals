"""Verify the manuscript's algebraic constants.

Manuscript reference: Section III, Theorem 1, and the closed-form computation
preceding the proof.

  M_r = max_{m <= r} sum_{pi in Pi_m} (|pi|-1)!
  B_r = max_{3 <= m <= r} sum_{pi: exists |B|>2} M_r^{|pi|-1}

  Manuscript values: M_3 = 6, M_4 = 26, M_5 = 150, B_4 = 105, B_5 = 227,251.
"""

from __future__ import annotations

from connected_layer_sector import B_r_const, M_r_const


def test_M_r_table():
    """Manuscript Section III, Theorem 1 closed-form values."""
    assert M_r_const(3) == 6.0
    assert M_r_const(4) == 26.0
    assert M_r_const(5) == 150.0


def test_B_r_table():
    """Manuscript Section III, Theorem 1 closed-form values."""
    assert B_r_const(3) == 1.0
    assert B_r_const(4) == 105.0
    assert B_r_const(5) == 227251.0


def test_M_r_monotone_nondecreasing():
    """M_r is non-decreasing in r (it is a max over [1, r])."""
    seq = [M_r_const(r) for r in range(1, 6)]
    assert all(seq[i + 1] >= seq[i] for i in range(len(seq) - 1))


def test_B_r_strict_increase_3_to_5():
    """B_r grows strictly between r=3 and r=5 on the chemistry-relevant range."""
    assert B_r_const(3) < B_r_const(4) < B_r_const(5)
