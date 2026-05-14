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


def test_Bhat_charge_r_chemistry_catalog_at_r_4():
    """Block-refined charge-filtered constants on the chemistry catalog at r=4.

    Manuscript abstract: $\\widehat B^{\\mathrm{charge}}_4(W) \\in \\{1, 3, 5\\}$.

    The five catalog words map to four distinct (h, z) parameter combinations:
       n n n              -> (h, z) = (0, 3) -> 1
       a_dag a n          -> (h, z) = (1, 1) -> 1
       a_dag a n n        -> (h, z) = (1, 2) -> 3
       a_dag a_dag a a    -> (h, z) = (2, 0) -> 1
       n n n n            -> (h, z) = (0, 4) -> 5
    """
    from connected_layer_sector import Bhat_charge_r

    cases = [
        ((0, 3), 1.0),
        ((1, 1), 1.0),
        ((1, 2), 3.0),
        ((2, 0), 1.0),
        ((0, 4), 5.0),
    ]
    for (h, z), expected in cases:
        actual = Bhat_charge_r(h, z, 4)
        assert actual == expected, f"(h={h}, z={z}): got {actual}, expected {expected}"


def test_Bhat_charge_r_is_no_larger_than_B_charge_r():
    """Block-refinement only tightens. For every (h, z, r), Bhat <= B_charge."""
    from connected_layer_sector import B_charge_r, Bhat_charge_r

    # Sweep small parameter combos. Skip (0, 0) where both are 0 by definition.
    for h in range(3):
        for z in range(5):
            if h == 0 and z == 0:
                continue
            for r in (3, 4):
                if 2 * h + z < 3:
                    continue  # bound undefined for too-short words
                if 2 * h + z > r:
                    continue  # word length must be <= r
                Bc = B_charge_r(h, z, r)
                Bh = Bhat_charge_r(h, z, r)
                assert Bh <= Bc + 1e-9, (
                    f"(h={h}, z={z}, r={r}): Bhat={Bh} should be <= B_charge={Bc}"
                )


def test_Bhat_charge_r_zero_word_returns_zero():
    """The empty / no-word case returns 0 (no contributing partitions)."""
    from connected_layer_sector import Bhat_charge_r

    assert Bhat_charge_r(0, 0, 4) == 0.0
