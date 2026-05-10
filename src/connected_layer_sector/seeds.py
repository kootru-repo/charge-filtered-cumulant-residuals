"""Deterministic seed helper.

Internalized into this repository so reproducibility does not depend on any
file outside the repo. The seed is derived from a SHA256 hash of a string
label, truncated to a 64-bit unsigned integer suitable for
``numpy.random.default_rng``.
"""

from __future__ import annotations

import hashlib

_MASK_64 = (1 << 64) - 1


def deterministic_seed(label: str) -> int:
    """Return a stable 64-bit non-negative integer seed for a string label.

    The mapping is platform-independent (SHA256 of the UTF-8 encoded label,
    truncated to the low 64 bits), so two runs on different machines that
    pass the same label receive the same seed.

    Parameters
    ----------
    label : str
        Any string identifier (e.g., a state-spec, a screen-cell name, or a
        random-Pauli-shadow batch id).

    Returns
    -------
    int
        A 64-bit unsigned integer in [0, 2**64).
    """
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big") & _MASK_64
