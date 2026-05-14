"""Algebraic partition-lattice constants M_r, B_r, and the charge-counting
recurrence for the charge-filtered constants B^charge_r(W)."""

from __future__ import annotations

import math
from functools import lru_cache
from math import comb

from connected_layer_sector.partition_lattice import set_partitions


@lru_cache(maxsize=64)
def M_r_const(r: int) -> float:
    """M_r = max_{m <= r} sum_{pi in Pi_m} (|pi|-1)!.

    Closed form via Stirling numbers of the second kind: M_3=6, M_4=26, M_5=150.
    """
    out = 0
    for m in range(1, r + 1):
        s = 0
        for pi in set_partitions(range(m)):
            s += math.factorial(len(pi) - 1)
        out = max(out, s)
    return float(out)


@lru_cache(maxsize=64)
def B_r_const(r: int) -> float:
    """B_r = max_{3 <= m <= r} sum_{pi: exists B with |B|>2} M_r^{|pi|-1}.

    Closed form: B_3 = 1, B_4 = 105, B_5 = 227251.
    """
    Mr = M_r_const(r)
    out = 0.0
    for m in range(3, r + 1):
        s = 0.0
        for pi in set_partitions(range(m)):
            if any(len(block) > 2 for block in pi):
                s += Mr ** (len(pi) - 1)
        out = max(out, s)
    return float(out)


def _P_recurrence(h: int, z: int):
    """P_{h,z}(x) = sum over neutral partitions of the multiset (h+, h-, z*0)
    of x^|pi|.

    Recurrence (manuscript Lemma 1):
      P_{0,0}(x) = 1
      P_{0,z}(x) = sum_{v=1}^z C(z-1, v-1) x P_{0, z-v}(x)
      P_{h,z}(x) = sum_{u=1}^h sum_{v=0}^z C(h-1, u-1) C(h, u) C(z, v)
                   x P_{h-u, z-v}(x)
    Returned as a list of coefficients [c_0, c_1, ...] where the polynomial is
    sum_i c_i x^i.
    """
    cache: dict[tuple[int, int], list[float]] = {}

    def _add(a, b):
        out = list(a)
        if len(b) > len(out):
            out = out + [0.0] * (len(b) - len(out))
        for i, bi in enumerate(b):
            out[i] += bi
        return out

    def _scalar_mul(c, p):
        return [c * x for x in p]

    def _x_times(p):
        return [0.0] + list(p)

    def go(hh: int, zz: int) -> list[float]:
        key = (hh, zz)
        if key in cache:
            return cache[key]
        if hh == 0 and zz == 0:
            res = [1.0]
        elif hh == 0:
            res = [0.0]
            for v in range(1, zz + 1):
                term = _x_times(go(0, zz - v))
                term = _scalar_mul(comb(zz - 1, v - 1), term)
                res = _add(res, term)
        else:
            res = [0.0]
            for u in range(1, hh + 1):
                for v in range(0, zz + 1):
                    term = _x_times(go(hh - u, zz - v))
                    coeff = comb(hh - 1, u - 1) * comb(hh, u) * comb(zz, v)
                    term = _scalar_mul(coeff, term)
                    res = _add(res, term)
        cache[key] = res
        return res

    return go(h, z)


def _Q_polynomial(h: int, z: int) -> list[float]:
    """Q_{h,z}(x) = h! sum_{j=0}^{floor(z/2)}
                   z! / ((z - 2j)! j! 2^j) x^{h + z - j}.

    Counts neutral partitions of (h+, h-, z*0) with all blocks of size <= 2.
    """
    out: list[float] = [0.0] * (h + z + 1)
    h_fact = math.factorial(h)
    z_fact = math.factorial(z)
    for j in range(z // 2 + 1):
        coeff = h_fact * z_fact / (math.factorial(z - 2 * j) * math.factorial(j) * (2**j))
        out[h + z - j] += coeff
    return out


def charge_filtered_polynomial(h: int, z: int) -> tuple[list[float], list[float]]:
    """Return (P_{h,z}, Q_{h,z}) as coefficient lists.

    The charge-filtered word constant is then
      B^charge_r(W) = (P_{h,z}(M_r) - Q_{h,z}(M_r)) / M_r
    for any word W with h(W) creation/annihilation balance and z(W) zero-charge
    letters.
    """
    return _P_recurrence(h, z), _Q_polynomial(h, z)


def evaluate_polynomial(coeffs: list[float], x: float) -> float:
    """Horner evaluation of sum_i coeffs[i] * x^i at x."""
    out = 0.0
    for c in reversed(coeffs):
        out = out * x + c
    return out


def B_charge_r(h: int, z: int, r: int) -> float:
    """B^charge_r(W) for a word with charge multiset (h+, h-, z*0)."""
    Mr = M_r_const(r)
    P, Q = charge_filtered_polynomial(h, z)
    return (evaluate_polynomial(P, Mr) - evaluate_polynomial(Q, Mr)) / Mr


def Bhat_charge_r(h: int, z: int, r: int) -> float:
    """Block-refined charge-filtered constant for a word with charge multiset
    (h+, h-, z*0).

    Manuscript definition (Theorem 3): each contributing partition's
    contribution is the minimum over the choice of distinguished large
    block $B^*$ of $\\prod_{B \\ne B^*} M_{|B|}$:

    .. math::
        \\widehat B^{\\mathrm{charge}}_r(W) =
        \\sum_{\\pi \\in \\Pi^{nl}_{|W|}(W)}
        \\;\\min_{B^* \\in \\pi,\\, |B^*| > 2}
        \\;\\prod_{B \\in \\pi,\\, B \\ne B^*} M_{|B|}.

    Here $\\Pi^{nl}_m(W)$ are neutral-block partitions of [m] with at least
    one block of size > 2. The min over choices of $B^*$ produces the
    tightest charge-filtered constant by exploiting the fact that one
    distinguished large block can serve as the "envelope-absorbing" block
    while the rest are bounded by the partition-lattice Mobius constants
    $M_{|B|}$.

    Closed-form values on the chemistry catalog at r = 4:
      h=0, z=3 (n n n):                 1
      h=1, z=1 (a_dag a n):             1
      h=1, z=2 (a_dag a n n):           3
      h=2, z=0 (a_dag a_dag a a):       1
      h=0, z=4 (n n n n):               5
    """
    if h == 0 and z == 0:
        return 0.0
    m = 2 * h + z
    # Representative charge sequence: h positives, h negatives, z zeros.
    charges = [+1] * h + [-1] * h + [0] * z
    total = 0.0
    for pi in set_partitions(range(m)):
        if not any(len(b) > 2 for b in pi):
            continue
        # Neutral-block filter.
        if any(sum(charges[i] for i in block) != 0 for block in pi):
            continue
        # Min over distinguished-large-block choice of product over non-B*.
        large_blocks = [b for b in pi if len(b) > 2]
        best = None
        for B_star in large_blocks:
            prod = 1.0
            for B in pi:
                if B is B_star:
                    continue
                prod *= M_r_const(len(B))
            if best is None or prod < best:
                best = prod
        total += float(best)
    return total
