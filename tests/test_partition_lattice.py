"""Partition lattice combinatorics: set_partitions enumerates Pi_m correctly.

Bell numbers B_m = |Pi_m|: B_1=1, B_2=2, B_3=5, B_4=15, B_5=52, B_6=203,
B_7=877, B_8=4140.
"""

from __future__ import annotations

from connected_layer_sector.partition_lattice import set_partitions

BELL = [1, 1, 2, 5, 15, 52, 203, 877, 4140]


def test_bell_numbers():
    for m in range(0, 9):
        n = sum(1 for _ in set_partitions(range(m)))
        assert n == BELL[m], f"|Pi_{m}| = {n}, expected B_{m} = {BELL[m]}"


def test_partitions_disjoint_and_cover():
    """For every m and every partition pi of [m], the blocks of pi must be
    disjoint and their union must equal [m]."""
    for m in range(1, 6):
        items = set(range(m))
        for pi in set_partitions(range(m)):
            seen = set()
            for block in pi:
                assert not (set(block) & seen), \
                    f"overlap in partition {pi} of [{m}]"
                seen.update(block)
            assert seen == items, f"miss in partition {pi} of [{m}]"


def test_singletons_partition_present():
    """For every m, Pi_m contains exactly one all-singleton partition."""
    for m in range(1, 6):
        n_singletons = sum(
            1 for pi in set_partitions(range(m))
            if all(len(b) == 1 for b in pi)
        )
        assert n_singletons == 1


def test_top_partition_present():
    """For every m, Pi_m contains exactly one one-block partition."""
    for m in range(1, 6):
        n_top = sum(
            1 for pi in set_partitions(range(m))
            if len(pi) == 1
        )
        assert n_top == 1
