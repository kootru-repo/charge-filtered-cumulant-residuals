"""Word moments mu_B(W;rho), order-<=2 closure F^G_<=2, and residual tau^G_W."""

from __future__ import annotations

import numpy as np

from connected_layer_sector.operators import word_matrix
from connected_layer_sector.partition_lattice import (
    ordered_cumulant,
    set_partitions,
)


def trace_op(rho: np.ndarray, op: np.ndarray) -> complex:
    return complex(np.trace(rho @ op))


def word_moment(rho: np.ndarray, word, n: int) -> complex:
    """mu_W(rho) = Tr(rho * A_W), where A_W is the JW-encoded word matrix."""
    if not word:
        return 1.0 + 0j
    return trace_op(rho, word_matrix(word, n))


def closure_order2_word(rho: np.ndarray, word, n: int) -> complex:
    """F^G_{<=2}(W; rho): sum over partitions of [m] with all blocks |B| <= 2
    of products of cumulants kappa_B."""
    m = len(word)
    if m == 0:
        return 1.0 + 0j
    if m == 1:
        return word_moment(rho, word, n)
    total = 0.0 + 0.0j
    for pi in set_partitions(range(m)):
        if any(len(block) > 2 for block in pi):
            continue
        prod = 1.0 + 0.0j
        for block in pi:
            prod *= ordered_cumulant(rho, word, tuple(block), n)
        total += prod
    return total


def tau_word(rho: np.ndarray, word, n: int) -> complex:
    """tau^G_W(rho) = mu_[m](W; rho) - F^G_{<=2}(W; rho), the residual that
    Theorems 1, 2, 3 of the manuscript bound."""
    return word_moment(rho, word, n) - closure_order2_word(rho, word, n)
