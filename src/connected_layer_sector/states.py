"""State factories: Slater determinants, Hubbard ground states, single-particle
eigenbases, and many-body orbital rotations."""

from __future__ import annotations

import numpy as np
from numpy import linalg as la
from scipy.linalg import expm, logm

from connected_layer_sector.operators import (
    jw_annihilation,
    jw_creation,
    number_op_site,
)


def determinant_state(n: int, occ_bits) -> np.ndarray:
    """Pure-state density matrix for a computational-basis Slater determinant
    described by occ_bits (length n, bit i = 1 means site i is filled)."""
    idx = 0
    for i, b in enumerate(occ_bits):
        if b:
            idx |= 1 << (n - 1 - i)
    psi = np.zeros(2**n, dtype=complex)
    psi[idx] = 1.0
    return np.outer(psi, psi.conj())


# ---------------------------------------------------------------------
# 1D Hubbard chain
# ---------------------------------------------------------------------


def hubbard_H(n_sites: int, t: float, U: float) -> np.ndarray:
    """Open-boundary 1D Hubbard Hamiltonian on 2*n_sites JW spin-orbitals.

    Convention: spin-up sites are qubits 0..n_sites-1; spin-down sites are
    qubits n_sites..2*n_sites-1.
    """
    n_orb = 2 * n_sites
    dim = 2**n_orb
    H = np.zeros((dim, dim), dtype=complex)
    # Hopping
    for i in range(n_sites - 1):
        for sigma in (0, 1):
            p = i + sigma * n_sites
            q = (i + 1) + sigma * n_sites
            ap_dag = jw_creation(n_orb, p)
            aq = jw_annihilation(n_orb, q)
            H -= t * ap_dag @ aq
            H -= t * ap_dag.conj().T @ aq.conj().T
    # On-site U
    for i in range(n_sites):
        nu = number_op_site(n_orb, i)
        nd = number_op_site(n_orb, i + n_sites)
        H += U * (nu @ nd)
    return H


def two_spin_fixed_N_projector(n_sites: int, n_up: int, n_dn: int) -> np.ndarray:
    """Projector onto the fixed-(N_up, N_dn) sector for the spin-orbital
    ordering used by `hubbard_H`."""
    n_orb = 2 * n_sites
    dim = 2**n_orb
    proj = np.zeros((dim, dim), dtype=complex)
    mask_up = (1 << n_sites) - 1
    mask_dn = ((1 << n_orb) - 1) ^ mask_up
    for idx in range(dim):
        if bin(idx & mask_up).count("1") == n_up and bin(idx & mask_dn).count("1") == n_dn:
            proj[idx, idx] = 1.0
    return proj


def hubbard_ground_state(
    n_sites: int,
    t: float,
    U: float,
    n_up: int,
    n_dn: int,
) -> tuple[np.ndarray, float]:
    """Return (psi_GS, E_GS) on the 2*n_sites JW Hilbert space."""
    H = hubbard_H(n_sites, t, U)
    pi = two_spin_fixed_N_projector(n_sites, n_up, n_dn)
    H_sub = pi @ H @ pi
    evals, evecs = la.eigh(H_sub)
    return evecs[:, 0], float(np.real(evals[0]))


# ---------------------------------------------------------------------
# U=0 noninteracting single-particle eigenbasis
# ---------------------------------------------------------------------


def tight_binding_eigenbasis(n_sites: int, t: float = 1.0):
    """Open-boundary 1D tight-binding single-particle eigenbasis.

    Returns
    -------
    eps : ndarray
        Single-particle energies (length n_sites). eps[k] = -2 t cos((k+1) pi /(n+1)).
    V_mat : ndarray
        Real orthogonal matrix V_mat[i, k] = <site i | mode k> with
        phi_k(i) = sqrt(2/(n+1)) sin((k+1) (i+1) pi / (n+1)).
    """
    n = n_sites
    sites = np.arange(1, n + 1)
    modes = np.arange(1, n + 1)
    V_mat = np.sqrt(2.0 / (n + 1)) * np.sin(np.outer(sites, modes) * np.pi / (n + 1))
    eps = -2.0 * t * np.cos(modes * np.pi / (n + 1))
    return eps, V_mat


def fermionic_orbital_rotation(W_mat: np.ndarray, n_orb: int) -> np.ndarray:
    """Build the many-body unitary V on 2^n_orb-dim Hilbert space that
    implements the one-body orbital rotation
        a_p^dag -> sum_q W_mat[q, p] a_q^dag.

    For a real orthogonal W_mat, V is constructed numerically by
    exponentiating the one-body anti-Hermitian generator K = log W in
    fermionic second quantization.

    `scipy.linalg.logm` is numerically fragile on orthogonal matrices
    with eigenvalue near -1; this function checks that W is unitary and
    that the principal logarithm is anti-Hermitian before exponentiating,
    so an unsafe input produces a clear error rather than silent drift.
    """
    if W_mat.shape != (n_orb, n_orb):
        raise ValueError(
            f"W_mat must be shape ({n_orb}, {n_orb}); got {W_mat.shape}"
        )
    eye = np.eye(n_orb, dtype=W_mat.dtype)
    unitarity_err = np.linalg.norm(W_mat @ W_mat.conj().T - eye)
    if unitarity_err > 1e-10:
        raise ValueError(
            "W_mat must be unitary; "
            f"||W W^* - I|| = {unitarity_err:.2e}"
        )
    K_one_body = logm(W_mat)
    anti_herm_err = np.linalg.norm(K_one_body + K_one_body.conj().T)
    if anti_herm_err > 1e-8:
        raise ValueError(
            "logm(W_mat) is not anti-Hermitian; W_mat may have an "
            "eigenvalue near -1 (logm branch ambiguity). "
            f"||K + K^*|| = {anti_herm_err:.2e}"
        )
    dim = 2**n_orb
    K_op = np.zeros((dim, dim), dtype=complex)
    for p in range(n_orb):
        ap_dag = jw_creation(n_orb, p)
        for q in range(n_orb):
            kpq = K_one_body[p, q]
            if abs(kpq) > 1e-12:
                aq = jw_annihilation(n_orb, q)
                K_op += kpq * (ap_dag @ aq)
    return expm(K_op)
