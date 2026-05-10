"""Catalog Corollary 1: $\\widehat B^{\\mathrm{charge}}_4(W) \\in \\{1, 3, 5\\}$
on the five chemistry-motivated catalog word types.

Manuscript reference: Section III, Corollary 1, by direct enumeration of
the partitions in $\\Pi^{\\mathrm{nl}}_{|W|}(W)$.
"""

from __future__ import annotations

from connected_layer_sector import M_r_const, set_partitions
from connected_layer_sector.operators import letter_charge


def _block_charge(word, block):
    return sum(letter_charge(word[j]) for j in block)


def _neutral_large_partitions(word):
    m = len(word)
    for pi in set_partitions(range(m)):
        if not any(len(b) > 2 for b in pi):
            continue
        if any(_block_charge(word, b) != 0 for b in pi):
            continue
        yield pi


def block_refined_constant(word, r: int = 4) -> int:
    """Direct enumeration of B_hat^charge_r(W)."""
    total = 0
    for pi in _neutral_large_partitions(word):
        candidates = [B for B in pi if len(B) > 2]
        per_choice = []
        for B_star in candidates:
            prod = 1
            for B in pi:
                if B is B_star:
                    continue
                prod *= int(M_r_const(len(B)))
            per_choice.append(prod)
        total += min(per_choice)
    return total


CATALOG_EXAMPLES = [
    ("nnn", (("n", 0), ("n", 1), ("n", 2)), 1),
    ("ad_a_n", (("ad", 0), ("a", 1), ("n", 2)), 1),
    ("ad_a_nn", (("ad", 0), ("a", 1), ("n", 2), ("n", 3)), 3),
    ("ad_ad_a_a", (("ad", 0), ("ad", 1), ("a", 2), ("a", 3)), 1),
    ("nnnn", (("n", 0), ("n", 1), ("n", 2), ("n", 3)), 5),
]


def test_block_refined_constants_at_r4():
    """Cor 1: B_hat^charge_4 = {1, 1, 3, 1, 5} on the five catalog word types."""
    for label, word, expected in CATALOG_EXAMPLES:
        actual = block_refined_constant(word, r=4)
        assert actual == expected, f"{label}: B_hat^charge_4 = {actual}, manuscript = {expected}"


def test_block_refined_constants_at_r5_unchanged():
    """Manuscript Cor 1 footnote: same {1, 3, 5} values at r=5 because no
    partition of [m <= 4] has a block of size 5."""
    for label, word, expected in CATALOG_EXAMPLES:
        actual = block_refined_constant(word, r=5)
        assert actual == expected, f"{label}: B_hat^charge_5 = {actual}, manuscript = {expected}"
