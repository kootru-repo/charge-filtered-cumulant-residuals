# charge-filtered-cumulant-residuals

Reproducibility repository for the manuscript:

> **Charge- and block-refined bias bounds for second-order cumulant truncation on $\mathrm{U}(1)$-invariant fermionic states.**

[![Tests](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml)
[![Notebooks](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20129665.svg)](https://doi.org/10.5281/zenodo.20129665)

This repository reproduces every numerical claim in the manuscript. Math content is algebraic and proved in the manuscript itself; this repository is the operational reproducibility envelope.

## For peer reviewers of the manuscript

If you are a peer reviewer, the fastest verification path is:

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
pip install -e .[dev,notebooks]
pytest                                      # ~2 min: unit suite
jupyter lab notebooks/00_overview.ipynb     # open + run all cells
```

The pytest run confirms the manuscript's headline numerical claims (the partition-lattice constants $B_r$, $B^{\mathrm{charge}}_r(W)$, $\widehat B^{\mathrm{charge}}_r(W) \in \{1, 3, 5\}$ on the chemistry catalog, and the audit summary of $3679$ observables across $26$ fixed-$N$ states). Each notebook ends with `assert` cells that confirm the headline claim of that section.

For a claim-by-claim manuscript-to-repository map, see [`docs/claim_index.md`](docs/claim_index.md). For SHA256 verification of the deposited data only (no notebook execution, no Python install), see [Data integrity](#data-integrity) below.

## Two reproduction paths

| Path | Effort | What it verifies |
|---|---|---|
| **Local pip + pytest** | ~2 min on a laptop | Full unit-test suite + smoke regeneration of one cell |
| **Data-only check** | ~10 sec | SHA256 verification of deposited JSONs against `MANIFEST.json` |

### Local

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
pip install -e .[dev]
pytest
```

Tests pass on Linux + macOS + Windows under Python 3.11, 3.12, 3.13. Linux + Python 3.12 is the primary CI gate; macOS / Windows / 3.11 / 3.13 run unit tests only. The notebooks workflow (`notebooks.yml`) executes every notebook headlessly on each push, so a green badge above means the notebooks reproduce end-to-end on a clean machine.

### Data integrity

```bash
pytest tests/test_data_integrity.py
```

Hashes the five deposited JSONs in `data/` against the SHA256 entries in `MANIFEST.json`. Confirms the deposited results have not been corrupted.

## Layout

```
src/connected_layer_sector/   importable Python package
notebooks/                    six numbered notebooks, claim-indexed to manuscript sections
tests/                        pytest suite (39 tests at present, >90% coverage target)
tests/mutation_check.py       optional: 10-mutation sanity check on the implementation
data/                         five deposited JSON outputs + MANIFEST.json
docs/                         claim_index.md (manuscript claim → notebook + test + data)
.github/workflows/            tests.yml, notebooks.yml
```

See `docs/claim_index.md` for the manuscript-to-repository claim map.

## License

Code is MIT-licensed (see [`LICENSE`](LICENSE)). Notebooks, data, and documentation are CC-BY-4.0 (see [`LICENSE-DATA`](LICENSE-DATA)). Copyright held by Kootru Labs (a DBA of Kootru LLC).

## About

Maintained by **Kootru Labs**, Burlington, USA. Website: [labs.kootru.com](https://labs.kootru.com).

Author and Principal Researcher: **Andrew Craton** ([ORCID 0009-0001-2269-8599](https://orcid.org/0009-0001-2269-8599), [acraton@kootru.com](mailto:acraton@kootru.com)).

This repository is the canonical reproducibility envelope for the manuscript; its Zenodo deposit ([DOI 10.5281/zenodo.20129665](https://doi.org/10.5281/zenodo.20129665)) is the citable artefact for the numerical content. A user-facing companion library that calls the same primitives in production code is published at [`cumulant-residual-cert`](https://github.com/kootru-repo/cumulant-residual-cert); its catalog constants are continuously cross-checked against this repository in CI.

## How to cite

Please cite both the deposit and the manuscript. A machine-readable [`CITATION.cff`](CITATION.cff) is provided; the BibTeX below is the equivalent.

**Reproducibility deposit (this repository, Zenodo):**

```bibtex
@dataset{charge_filtered_cumulant_residuals,
  author       = {Craton, Andrew},
  title        = {{charge-filtered-cumulant-residuals}: reproducibility envelope},
  organization = {Kootru Labs},
  doi          = {10.5281/zenodo.20129665},
  url          = {https://doi.org/10.5281/zenodo.20129665},
  year         = {2026}
}
```

**Manuscript:**

```bibtex
@unpublished{craton_charge_filtered_cumulant_residuals_manuscript,
  author       = {Craton, Andrew},
  title        = {Charge- and block-refined bias bounds for second-order
                  cumulant truncation on {$U(1)$}-invariant fermionic states},
  organization = {Kootru Labs},
  year         = {2026},
  note         = {Manuscript in preparation}
}
```

**Companion library (optional, if you use the user-facing API):**

```bibtex
@software{cumulant_residual_cert,
  author       = {Craton, Andrew},
  title        = {{cumulant-residual-cert}: deterministic bias certificates for
                  charge-neutral fermionic-word observables},
  organization = {Kootru Labs},
  url          = {https://github.com/kootru-repo/cumulant-residual-cert},
  version      = {0.5.0},
  year         = {2026}
}
```

## How to verify a specific manuscript claim

1. Open `docs/claim_index.md`. Find the claim by manuscript section.
2. The table tells you which notebook to open, which test to run, and which JSON to inspect.
3. Each notebook ends with one or more `assert` cells that verify the claim numerically.

## Scope

This repository is the **operational reproducibility envelope**: it
reproduces every quoted numerical value in the manuscript, runs in
under five minutes on a laptop, and exposes a thin
pip-installable API so any reader can call the primitives directly.

It is intentionally NOT an adversarial verification surface. The
following are out of scope here:

- adversarial state-search optimization for bound saturation,
- mutation testing of the implementation modules beyond the
  lightweight `tests/mutation_check.py` sanity harness,
- cross-validation against an independent symbolic-arithmetic oracle,
- large-$n$ ($n \ge 5$) stress on the three-theorem chain,
- the diagnostic-UCB Monte-Carlo coverage simulation.

The manuscript's algebraic theorems are proved in the paper itself.
This repository confirms the deposited numerical values are
recomputable; it does not attempt to falsify the proofs.
