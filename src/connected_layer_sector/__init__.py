"""Reproducibility package for the charge-filtered cumulant residual manuscript.

Public API (kept small intentionally; helpers are module-private):

- Operators (Jordan-Wigner, fermionic letters):
    jw_creation, jw_annihilation, number_op_site, fixed_N_projector

- Partition lattice (Mobius inversion, set partitions):
    set_partitions, ordered_cumulant

- Word machinery:
    letter_matrix, word_matrix, word_moment, tau_word

- Constants and catalog:
    M_r_const, B_r_const, charge_filtered_polynomial,
    enumerate_chemistry_catalog

- Reproducible randomness:
    deterministic_seed

- States:
    determinant_state, hubbard_ground_state,
    tight_binding_eigenbasis, fermionic_orbital_rotation

- Audit pipeline:
    evaluate_catalog
"""

from connected_layer_sector.audit import evaluate_catalog
from connected_layer_sector.catalog import enumerate_chemistry_catalog
from connected_layer_sector.constants import (
    B_charge_r,
    B_r_const,
    Bhat_charge_r,
    M_r_const,
    charge_filtered_polynomial,
)
from connected_layer_sector.moments import (
    tau_word,
    word_moment,
)
from connected_layer_sector.operators import (
    fixed_N_projector,
    jw_annihilation,
    jw_creation,
    letter_matrix,
    number_op_site,
    word_matrix,
)
from connected_layer_sector.partition_lattice import (
    ordered_cumulant,
    set_partitions,
)
from connected_layer_sector.seeds import deterministic_seed
from connected_layer_sector.states import (
    determinant_state,
    fermionic_orbital_rotation,
    hubbard_ground_state,
    tight_binding_eigenbasis,
)

__version__ = "0.1.0"

__all__ = [
    "B_charge_r",
    "B_r_const",
    "Bhat_charge_r",
    "M_r_const",
    "charge_filtered_polynomial",
    "deterministic_seed",
    "determinant_state",
    "enumerate_chemistry_catalog",
    "evaluate_catalog",
    "fermionic_orbital_rotation",
    "fixed_N_projector",
    "hubbard_ground_state",
    "jw_annihilation",
    "jw_creation",
    "letter_matrix",
    "number_op_site",
    "ordered_cumulant",
    "set_partitions",
    "tau_word",
    "tight_binding_eigenbasis",
    "word_matrix",
    "word_moment",
    "__version__",
]
