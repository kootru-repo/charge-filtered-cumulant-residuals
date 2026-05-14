"""Chemistry-motivated word catalog (Definition 3 of the manuscript).

Words are tuples of letters of the form ('a', i), ('ad', i), or ('n', i),
with site indices in 0..n-1. Each catalog entry is

    (label, sites_tuple, word, coefficient, hermitian_partner_or_None)

where the Hermitian partner is set for non-Hermitian words (hopping and
excitation types) and None for Hermitian words (number-only types).
"""

from __future__ import annotations

from itertools import combinations


def enumerate_chemistry_catalog(
    n: int,
    *,
    cap_hopping: int = 200,
    cap_double: int = 350,
    cap_hop_density: int = 250,
):
    """Enumerate the chemistry-motivated catalog at orbital count n.

    Emits all five chemistry-catalog word types from Corollary 1 of the
    manuscript:

      label        word                       (h, z)   block-refined constant
      "nnn"        n_i n_j n_k                (0, 3)   1
      "hopn"       a^dag_i a_j n_k            (1, 1)   1
      "doublex"    a^dag_i a^dag_j a_k a_m    (2, 0)   1
      "hopnn"      a^dag_i a_j n_k n_l        (1, 2)   3
      "nnnn"       n_i n_j n_k n_l            (0, 4)   5

    Note on the deposited data. The audit JSONs deposited in
    ``data/screen_sector_*.json`` (summing to 3679 observables across 26
    fixed-N states) were produced from an earlier version of this
    enumerator that omitted the ``hopn n`` word type, before the full
    five-type listing was wired up. Future audit runs from
    :func:`evaluate_catalog` will cover all five word types; the
    deposited headline number 3679 reflects the historical 4-type
    enumeration. See ``docs/claim_index.md`` for the per-word-type
    breakdown.

    Parameters
    ----------
    n : int
        Number of orbitals / qubits in the JW encoding.
    cap_hopping : int
        Maximum number of ``a^dag a n`` entries to include before stopping
        the triple-index sweep early.
    cap_double : int
        Maximum total catalog size before stopping the
        ``a^dag a^dag a a`` excitation sweep early.
    cap_hop_density : int
        Maximum number of ``a^dag a n n`` entries to include before
        stopping the four-index sweep early.

    Returns
    -------
    list of (label, sites_tuple, word, coefficient, hermitian_partner)
    """
    catalog = []
    sites = list(range(n))

    # n_i n_j n_k  (length 3, charge 0)
    for triple in combinations(sites, 3):
        w = tuple(("n", i) for i in triple)
        catalog.append(("nnn", triple, w, 1.0, None))

    # n_i n_j n_k n_l  (length 4, charge 0)
    for quad in combinations(sites, 4):
        w = tuple(("n", i) for i in quad)
        catalog.append(("nnnn", quad, w, 1.0, None))

    # a^dag_i a_j n_k + h.c.
    for i in sites:
        for j in sites:
            if j == i:
                continue
            for k in sites:
                if k in {i, j}:
                    continue
                w = (("ad", i), ("a", j), ("n", k))
                w_dag = (("n", k), ("ad", j), ("a", i))
                catalog.append(("hopn", (i, j, k), w, 1.0, w_dag))
                if len(catalog) >= cap_hopping:
                    break
            if len(catalog) >= cap_hopping:
                break
        if len(catalog) >= cap_hopping:
            break

    # a^dag_i a^dag_j a_k a_m + h.c.  (double excitation)
    pairs_in = list(combinations(sites, 2))
    for i, j in pairs_in:
        for k, m in pairs_in:
            if {i, j} & {k, m}:
                continue
            w = (("ad", i), ("ad", j), ("a", k), ("a", m))
            w_dag = (("ad", m), ("ad", k), ("a", j), ("a", i))
            catalog.append(("doublex", (i, j, k, m), w, 1.0, w_dag))
            if len(catalog) >= cap_double:
                break
        if len(catalog) >= cap_double:
            break

    # a^dag_i a_j n_k n_l + h.c.  (hopping with double density; h=1, z=2)
    # This is the fifth chemistry-catalog word type from Corollary 1, whose
    # block-refined constant is 3 (the largest non-trivial value in the
    # catalog's block-refined set besides the all-number length-4 word).
    hopnn_start = len(catalog)
    for i in sites:
        if len(catalog) - hopnn_start >= cap_hop_density:
            break
        for j in sites:
            if j == i:
                continue
            if len(catalog) - hopnn_start >= cap_hop_density:
                break
            remaining = [s for s in sites if s not in {i, j}]
            for k, l in combinations(remaining, 2):
                w = (("ad", i), ("a", j), ("n", k), ("n", l))
                w_dag = (("n", k), ("n", l), ("ad", j), ("a", i))
                catalog.append(("hopnn", (i, j, k, l), w, 1.0, w_dag))
                if len(catalog) - hopnn_start >= cap_hop_density:
                    break

    return catalog
