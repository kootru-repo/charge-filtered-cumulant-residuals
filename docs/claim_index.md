# Claim index

Each numerical claim in the manuscript is mapped to a notebook, a test, and a deposited data file (when applicable). Any claim can be verified by following the corresponding row.

## Theorem and constant claims

| Manuscript section | Claim | Notebook | Test | Data |
|---|---|---|---|---|
| Sec III, Theorem 1 | $M_3 = 6$, $M_4 = 26$, $M_5 = 150$ | `01_partition_constants.ipynb` | `tests/test_constants.py::test_M_r_table` | — |
| Sec III, Theorem 1 | $B_3 = 1$, $B_4 = 105$, $B_5 = 227\,251$ | `01_partition_constants.ipynb` | `tests/test_constants.py::test_B_r_table` | — |
| Sec III, Theorem 1 derivation | $D_4(x) = 1 + 4x$, $B_4 = D_4(M_4) = 105$ | `01_partition_constants.ipynb` | `tests/test_partition_lattice.py::test_bell_numbers` (related) | — |
| Sec III, Lemma 1 (recurrence) | $P_{1,2}(x) = x + 3x^2 + x^3$, $Q_{1,2}(x) = x^2 + x^3$ | `01_partition_constants.ipynb` | `tests/test_charge_counting.py::test_worked_example_B_charge_4` | — |
| Sec III, worked example | $B^{\mathrm{charge}}_4(a^\dagger_i a_j n_k n_\ell) = 53$ | `01_partition_constants.ipynb` | `tests/test_charge_counting.py::test_worked_example_B_charge_4` | — |
| Sec III, worked example | $B^{\mathrm{charge}}_5(a^\dagger_i a_j n_k n_\ell) = 301$ | `01_partition_constants.ipynb` | `tests/test_charge_counting.py::test_worked_example_B_charge_5` | — |
| Sec III, Cor 1 | $\widehat B^{\mathrm{charge}}_4(W) \in \{1, 3, 5\}$ on the chemistry catalog | `02_chemistry_catalog.ipynb` | `tests/test_catalog_corollary.py::test_block_refined_constants_at_r4` | — |
| Sec II | Moment-cumulant identity $\mu_{[m]} = \sum_{\pi} \prod_B \kappa_B$ | — | `tests/test_moments_cumulants.py::test_moment_cumulant_identity_*` | — |

## Implementation-audit claims (Sec VI)

| Manuscript section | Claim | Notebook | Test | Data |
|---|---|---|---|---|
| Sec VI | $3679$ charge-neutral observables across $26$ fixed-$N$ states | `03_implementation_audit.ipynb` | `tests/test_data_integrity.py` + `tests/test_audit_results_structure.py::test_headline_per_cell_counts_consistent_with_headline` | `data/screen_sector_cumulant_theorem.json`, `data/screen_sector_cumulant_extended.json`, `data/screen_sector_audit_r5.json` |
| Sec VI | All $3679$ instances satisfy the bound at zero numerical violation | `03_implementation_audit.ipynb` | `tests/test_audit_results_structure.py::test_headline_zero_violations` | `data/audit_sector_cumulant_results.json` |
| Sec VI | $B^{\mathrm{eff}}_{\max} \approx 2.0$ on the audit suite | `03_implementation_audit.ipynb` | `tests/test_audit_results_structure.py` | `data/screen_sector_audit_r5.json` |

> **Note on word-type coverage.** The deposited audit JSONs above
> ($630 + 1960 + 1089 = 3679$ observables) were produced from an
> enumerator pass that covered four of the five Corollary 1 word
> types: `nnn`, `nnnn`, `hopn`, and `doublex`. The fifth word type
> (`hopnn` $= a^\dagger a n n$, whose block-refined constant is $3$)
> was added to `enumerate_chemistry_catalog` after the deposited
> screens were taken. Future audit runs via `evaluate_catalog`
> will cover all five word types; the headline $3679$ refers to the
> historical four-type screens. The Corollary 1 constants for the
> fifth word type are independently verified by
> `tests/test_catalog_corollary.py::test_block_refined_constants_at_r4`
> (which enumerates the partition-lattice contribution directly from
> the definition, not via `evaluate_catalog`) and by
> `tests/test_constants.py::test_Bhat_charge_r_chemistry_catalog_at_r_4`.

## Worked-example zero baseline (Sec V)

| Manuscript section | Claim | Notebook | Test | Data |
|---|---|---|---|---|
| Sec V | $\Delta^{\mathrm{cat}}_{4,U(1)}(\rho) = 0$ on every occupation-basis diagonal product state | `04_correlated_calibration.ipynb` (Hubbard $U=0$ row) | `tests/test_calibration.py::test_u0_baseline_is_floating_point_zero`, `tests/test_smoke_regeneration.py::test_regenerate_hubbard_u0_baseline`, `tests/test_moments_cumulants.py::test_kappa_top_vanishes_on_determinant` | `data/calibration_chemistry.json` |

## Correlated-state calibration (Sec V extension)

| Claim | Notebook | Test | Data |
|---|---|---|---|
| 1D Hubbard ground state at $n_{\mathrm{sites}} = 4$, half-filled, in the $U=0$ eigenbasis: $\Delta^{\mathrm{cat}}$ grows monotonically with $U/t$ | `04_correlated_calibration.ipynb` | `tests/test_calibration.py::test_delta_cat_monotone_in_U_over_t` | `data/calibration_chemistry.json` |
| Universal bound looseness: $\eta_{\mathrm{universal}} \approx 0.0095$ across the $U/t$ sweep (universal $B_4 = 105$ is loose by ~100×) | `04_correlated_calibration.ipynb` | `tests/test_calibration.py::test_eta_universal_below_one` | `data/calibration_chemistry.json` |

## Diagnostic UCB (Sec IV)

| Claim | Notebook | Test | Data |
|---|---|---|---|
| Sample-split, Bonferroni-corrected upper-confidence-bound for $\Delta^{\mathrm{cat}}_{r,U(1)}$ | `05_diagnostic_ucb_demo.ipynb` | (notebook `assert` cells) | — |

## Data integrity

`tests/test_data_integrity.py` hashes each file in `data/` against the SHA256 entry in `MANIFEST.json`. The manifest also records the git commit/tag, Python version, and platform that produced each archived run.

## Pipeline reproducibility

`tests/test_smoke_regeneration.py` regenerates the Hubbard $U=0$ baseline from code on the running machine and compares to the deposited result, confirming the pipeline (not just the deposited file) is reproducible.

## Status

All claims are verified by either a `pytest` test, a notebook `assert` cell, or a data-integrity SHA256 check. Run `pytest` and `pytest --nbval-lax notebooks/` to verify the full set in two commands.
