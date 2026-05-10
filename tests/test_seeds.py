"""Deterministic seed: stable, 64-bit, label-derived (no external dependency)."""

from __future__ import annotations

from connected_layer_sector import deterministic_seed


def test_determinism():
    """Same label produces the same seed across calls."""
    a = deterministic_seed("hubbard_n4_U0")
    b = deterministic_seed("hubbard_n4_U0")
    assert a == b


def test_distinct_labels_produce_distinct_seeds():
    """Realistic lookup labels collide negligibly often."""
    seen = set()
    for label in [
        "hubbard_n4_U0",
        "hubbard_n4_U1",
        "hubbard_n4_U4",
        "hubbard_n4_U8",
        "hubbard_n4_U16",
        "h2_R0.74",
        "h2_R3.0",
        "lih_eq",
        "shadow_batch_0",
        "shadow_batch_1",
    ]:
        s = deterministic_seed(label)
        assert s not in seen, f"collision on label={label!r}"
        seen.add(s)


def test_64_bit_range():
    """Seeds always fit in [0, 2**64)."""
    for label in ["a", "ab", "abc", "x" * 1000]:
        s = deterministic_seed(label)
        assert 0 <= s < (1 << 64)


def test_known_seed_value():
    """Pin one stable value so any change to the hashing logic is caught.

    SHA256("test")[0:8].big-endian = 0x9f86d081884c7d65 = 11495104353665842533.
    """
    assert deterministic_seed("test") == 11495104353665842533
