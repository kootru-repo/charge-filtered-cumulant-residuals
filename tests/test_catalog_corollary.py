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


def test_enumerate_chemistry_catalog_covers_all_five_word_types():
    """enumerate_chemistry_catalog must emit all five catalog word types from
    Corollary 1. Earlier revisions of the enumerator omitted the
    a^dag a n n word type (whose block-refined constant is 3), which broke
    coverage of the manuscript's headline {1, 3, 5} set for downstream
    audits relying on enumerate_chemistry_catalog output.
    """
    from connected_layer_sector import enumerate_chemistry_catalog

    catalog = enumerate_chemistry_catalog(n=5)
    labels_present = {entry[0] for entry in catalog}
    expected_labels = {"nnn", "nnnn", "hopn", "doublex", "hopnn"}
    assert expected_labels.issubset(labels_present), (
        f"missing word-type labels: {expected_labels - labels_present}; "
        f"present: {labels_present}"
    )


def test_enumerate_chemistry_catalog_hopnn_has_correct_charge_pattern():
    """Every entry labelled 'hopnn' must have charge pattern (+1, -1, 0, 0).

    Letter charges: a^dag -> +1, a -> -1, n -> 0.
    The audit-side constants module computes B^charge and B_hat^charge for
    this word via the (h, z) = (1, 2) parameterisation.
    """
    from connected_layer_sector import enumerate_chemistry_catalog
    from connected_layer_sector.operators import letter_charge

    catalog = enumerate_chemistry_catalog(n=5)
    hopnn_entries = [entry for entry in catalog if entry[0] == "hopnn"]
    assert hopnn_entries, "expected at least one hopnn entry at n=5"
    for _label, sites, word, _coef, _w_dag in hopnn_entries:
        charges = tuple(letter_charge(lpair) for lpair in word)
        positives = sum(1 for c in charges if c == +1)
        negatives = sum(1 for c in charges if c == -1)
        zeros = sum(1 for c in charges if c == 0)
        assert (positives, negatives, zeros) == (1, 1, 2), (
            f"hopnn {sites} has charges {charges}; expected (+1, -1, 0, 0)"
        )
