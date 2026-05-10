"""Jordan-Wigner fermionic operators on n qubits, fixed-N projectors,
and letter-to-matrix conversion for the chemistry-motivated catalog."""

from __future__ import annotations

import numpy as np

# Single-qubit Pauli matrices.
I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_chain(mats):
    out = np.array([[1.0 + 0j]])
    for m in mats:
        out = np.kron(out, m)
    return out


def jw_creation(n: int, i: int) -> np.ndarray:
    """a_i^dagger under Jordan-Wigner: (Z_0 ... Z_{i-1}) sigma_+ I ... I."""
    sigma_plus = (X2 - 1j * Y2) / 2  # |1><0|
    mats = [Z2] * i + [sigma_plus] + [I2] * (n - i - 1)
    return kron_chain(mats)


def jw_annihilation(n: int, i: int) -> np.ndarray:
    """a_i under Jordan-Wigner: (Z_0 ... Z_{i-1}) sigma_- I ... I."""
    sigma_minus = (X2 + 1j * Y2) / 2  # |0><1|
    mats = [Z2] * i + [sigma_minus] + [I2] * (n - i - 1)
    return kron_chain(mats)


def number_op_site(n: int, i: int) -> np.ndarray:
    """n_i = a_i^dagger a_i = (I - Z_i)/2."""
    mats = [I2] * n
    mats[i] = (I2 - Z2) / 2
    return kron_chain(mats)


def fixed_N_projector(n: int, N: int) -> np.ndarray:
    """Projector onto the fixed-particle-number sector of dimension binom(n, N)."""
    dim = 2**n
    proj = np.zeros((dim, dim), dtype=complex)
    for idx in range(dim):
        if bin(idx).count("1") == N:
            proj[idx, idx] = 1.0
    return proj


def project_to_sector(rho: np.ndarray, piN: np.ndarray) -> tuple[np.ndarray, float]:
    """Apply Pi_N rho Pi_N and renormalize. Returns (rho_proj, original_trace)."""
    rho_p = piN @ rho @ piN
    tr = float(np.real(np.trace(rho_p)))
    if tr < 1e-15:
        return rho_p, 0.0
    return rho_p / tr, tr


def letter_charge(letter) -> int:
    op, _ = letter
    return {"a": -1, "ad": +1, "n": 0}[op]


def word_charge(word) -> int:
    return sum(letter_charge(L) for L in word)


def letter_matrix(letter, n: int) -> np.ndarray:
    """Convert a single letter ('a'/'ad'/'n', site_index) to its JW matrix."""
    op, i = letter
    if op == "a":
        return jw_annihilation(n, i)
    if op == "ad":
        return jw_creation(n, i)
    if op == "n":
        return number_op_site(n, i)
    raise KeyError(f"unknown letter op {op!r}")


def word_matrix(word, n: int) -> np.ndarray:
    """Convert a word (tuple of letters) to its ordered product matrix."""
    if not word:
        return np.eye(2**n, dtype=complex)
    out = letter_matrix(word[0], n)
    for L in word[1:]:
        out = out @ letter_matrix(L, n)
    return out
