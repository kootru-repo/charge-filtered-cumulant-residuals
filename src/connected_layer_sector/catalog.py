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
):
    """Enumerate the chemistry-motivated catalog at orbital count n.

    Parameters
    ----------
    n : int
        Number of orbitals / qubits in the JW encoding.
    cap_hopping : int
        Maximum number of (a^dag a n) entries to include before stopping the
        triple-index sweep early. Matches the existing audit pipeline.
    cap_double : int
        Maximum total catalog size before stopping the (a^dag a^dag a a)
        excitation sweep early.

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

    return catalog
