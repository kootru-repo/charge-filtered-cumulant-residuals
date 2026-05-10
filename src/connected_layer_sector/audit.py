"""Catalog evaluation pipeline: Delta^cat, max |tau|, B^eff, eta_universal."""

from __future__ import annotations

import math

import numpy as np

from connected_layer_sector.catalog import enumerate_chemistry_catalog
from connected_layer_sector.constants import B_r_const, M_r_const
from connected_layer_sector.moments import tau_word
from connected_layer_sector.partition_lattice import ordered_cumulant


def evaluate_catalog(rho: np.ndarray, n_orb: int, *, r: int = 4) -> dict:
    """Compute the catalog envelope and residual metrics on rho.

    Returns a dict with:
      - delta_cat: max over catalog words W of |kappa_{[|W|]}(W; rho)|
      - delta_cat_word: the word that attained that supremum
      - max_tau: max over catalog words of |tau^G_W(rho)|
      - max_tau_word: word attaining that supremum
      - B_eff_max: max_W |tau^G_W| / |kappa_{[|W|]}(W;rho)| over the catalog
      - eta_universal: max_tau / (B_r * delta_cat); NaN if delta_cat == 0
      - B_r_universal: integer-valued universal constant B_r
      - M_r_universal: integer-valued partition-lattice constant M_r
      - n_catalog_words: number of catalog entries enumerated
    """
    catalog = enumerate_chemistry_catalog(n_orb)
    M_r = M_r_const(r)
    B_r = B_r_const(r)

    delta_cat = 0.0
    delta_max_word = None
    max_tau = 0.0
    max_tau_word = None
    max_B_eff = 0.0

    for entry in catalog:
        word = entry[2]
        full_subset = list(range(len(word)))
        kappa_top = ordered_cumulant(rho, word, full_subset, n_orb)
        kappa_abs = abs(kappa_top)
        if kappa_abs > delta_cat:
            delta_cat = kappa_abs
            delta_max_word = word
        tau = tau_word(rho, word, n_orb)
        tau_abs = abs(tau)
        if tau_abs > max_tau:
            max_tau = tau_abs
            max_tau_word = word
        if kappa_abs > 1e-14:
            b_eff_word = tau_abs / kappa_abs
            if b_eff_word > max_B_eff:
                max_B_eff = b_eff_word

    if delta_cat > 1e-14:
        eta_universal = max_tau / (B_r * delta_cat)
    else:
        eta_universal = math.nan

    return {
        "delta_cat": float(delta_cat),
        "delta_cat_word": list(delta_max_word) if delta_max_word else None,
        "max_tau": float(max_tau),
        "max_tau_word": list(max_tau_word) if max_tau_word else None,
        "B_eff_max": float(max_B_eff),
        "eta_universal": float(eta_universal),
        "B_r_universal": int(B_r),
        "M_r_universal": int(M_r),
        "n_catalog_words": len(catalog),
    }
