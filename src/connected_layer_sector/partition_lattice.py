"""Set partitions of a finite index set and Mobius-inversion ordered cumulants."""

from __future__ import annotations

import math

from connected_layer_sector.operators import word_matrix


def set_partitions(items):
    """Yield all set partitions of `items` as lists of disjoint blocks."""
    items = list(items)
    if not items:
        yield []
        return
    if len(items) == 1:
        yield [[items[0]]]
        return
    first = items[0]
    rest = items[1:]
    for sub in set_partitions(rest):
        for i in range(len(sub)):
            new_part = [list(b) for b in sub]
            new_part[i].append(first)
            yield new_part
        yield [[first]] + [list(b) for b in sub]


def _word_moment(rho, word, n):
    """Local copy to avoid an import cycle with the moments module."""
    if not word:
        return 1.0 + 0j
    import numpy as np

    return complex(np.trace(rho @ word_matrix(word, n)))


def ordered_cumulant(rho, word, subset, n):
    """kappa_B(W; rho) for an ordered subset B = (b_1<...<b_s) of [m].

    Computed via Mobius inversion on Pi(B):
      kappa_B = sum_pi (-1)^{|pi|-1} (|pi|-1)! prod_{C in pi} mu_C
    where mu_C = trace(rho * prod_{j in C, in B-order} L_{b_j}).
    """
    if not subset:
        return 1.0 + 0j
    subset = sorted(subset)
    if len(subset) == 1:
        return _word_moment(rho, (word[subset[0]],), n)
    total = 0.0 + 0.0j
    for pi in set_partitions(subset):
        prod = 1.0 + 0.0j
        for block in pi:
            block = sorted(block)
            sub_word = tuple(word[j] for j in block)
            prod *= _word_moment(rho, sub_word, n)
        k = len(pi)
        sign = (-1) ** (k - 1)
        total += math.factorial(k - 1) * sign * prod
    return total
