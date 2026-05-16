# charge-filtered-cumulant-residuals

Reproducibility repository for the manuscript:

> **Charge- and block-refined bias bounds for second-order cumulant truncation on $\mathrm{U}(1)$-invariant fermionic states.**

[![Tests](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml)
[![Notebooks](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20129664.svg)](https://doi.org/10.5281/zenodo.20129664)

This repository reproduces every numerical claim in the manuscript. Math content is algebraic and proved in the manuscript itself; this repository is the operational reproducibility envelope.

## Requirements

- Python `>=3.11` (CI runs 3.11, 3.12, 3.13; Linux + 3.12 is the primary gate).
- [uv](https://docs.astral.sh/uv/) (one-line install: `curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS; `irm https://astral.sh/uv/install.ps1 | iex` on Windows).
- No other system prerequisites. UV manages the Python toolchain itself.

Core dependencies (`numpy >= 1.26`, `scipy >= 1.11`) and dev / notebook extras (`pytest`, `nbval`, `jupyterlab`, `matplotlib`, `ruff`) are declared in [`pyproject.toml`](pyproject.toml) and pinned in [`uv.lock`](uv.lock). The lockfile is the durable execution record; the manuscript's reproducibility claims are anchored against this exact resolution.

## For peer reviewers of the manuscript

If you are a peer reviewer, the fastest verification path is:

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
uv sync --extra dev --extra notebooks
uv run pytest                                       # ~2 min: unit suite
uv run jupyter lab notebooks/00_overview.ipynb      # open + run all cells
```

The pytest run confirms the manuscript's headline numerical claims (the partition-lattice constants $B_r$, $B^{\mathrm{charge}}_r(W)$, $\widehat B^{\mathrm{charge}}_r(W) \in \{1, 3, 5\}$ on the chemistry catalog, and the audit summary of $3679$ observables across $26$ fixed-$N$ states). Each notebook ends with `assert` cells that confirm the headline claim of that section.

For a claim-by-claim manuscript-to-repository map, see [`docs/claim_index.md`](docs/claim_index.md). For SHA256 verification of the deposited data only (no notebook execution, no Python install), see [Data integrity](#data-integrity) below.

## Three reproduction paths

| Path | Effort | What it verifies |
|---|---|---|
| **Local uv + pytest** | ~2 min on a laptop | Full unit-test suite + smoke regeneration of one cell |
| **Open any notebook on Colab** | one click, ~30 s bootstrap | Notebook end-to-end on Colab's free CPU tier; no local install |
| **Data-only check** | ~10 sec, no Python needed | SHA256 verification of deposited JSONs against `MANIFEST.json` |

### Local

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
uv sync --extra dev
uv run pytest
```

Tests pass on Linux + macOS + Windows under Python 3.11, 3.12, 3.13. Linux + Python 3.12 is the primary CI gate; macOS / Windows / 3.11 / 3.13 run unit tests only. The notebooks workflow (`notebooks.yml`) executes every notebook headlessly on each push, so a green badge above means the notebooks reproduce end-to-end on a clean machine.

### Colab

The bootstrap cell at the top of each notebook clones this repo to `/content`, installs the package via `uv`, and runs the rest of the notebook unchanged. All six notebooks run end-to-end on Colab's free CPU tier in under five minutes.

| # | Notebook | Manuscript section | Open in Colab |
|---|---|---|---|
| 00 | [`00_overview.ipynb`](notebooks/00_overview.ipynb) | orientation + headline constants | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/00_overview.ipynb) |
| 01 | [`01_partition_constants.ipynb`](notebooks/01_partition_constants.ipynb) | Sec III, Theorem 1 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/01_partition_constants.ipynb) |
| 02 | [`02_chemistry_catalog.ipynb`](notebooks/02_chemistry_catalog.ipynb) | Sec III, Cor 1 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/02_chemistry_catalog.ipynb) |
| 03 | [`03_implementation_audit.ipynb`](notebooks/03_implementation_audit.ipynb) | Sec VI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/03_implementation_audit.ipynb) |
| 04 | [`04_correlated_calibration.ipynb`](notebooks/04_correlated_calibration.ipynb) | Sec V baseline + Hubbard $U/t$ sweep | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/04_correlated_calibration.ipynb) |
| 05 | [`05_diagnostic_ucb_demo.ipynb`](notebooks/05_diagnostic_ucb_demo.ipynb) | Sec IV | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/05_diagnostic_ucb_demo.ipynb) |

### Data integrity

```bash
uv run pytest tests/test_data_integrity.py
```

Hashes the five deposited JSONs in `data/` against the SHA256 entries in `MANIFEST.json`. Confirms the deposited results have not been corrupted. (The hashing logic itself is stdlib-only, so this path also runs against a hand-curated environment if uv is not available.)

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

This repository is the canonical reproducibility envelope for the manuscript; its Zenodo deposit ([concept DOI 10.5281/zenodo.20129664](https://doi.org/10.5281/zenodo.20129664), auto-tracks the latest version) is the citable artefact for the numerical content. A user-facing companion library that calls the same primitives in production code is published at [`cumulant-residual-cert`](https://github.com/kootru-repo/cumulant-residual-cert); its catalog constants are continuously cross-checked against this repository in CI.

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
reproduces every quoted numerical value in the manuscript and runs
in under five minutes on a laptop. The `src/connected_layer_sector/`
package is an internal artefact, structured for `pytest` to import
its primitives during verification; it is **not** a user-facing
library. Readers who want a stable API for production use should
install the companion library
[`cumulant-residual-cert`](https://github.com/kootru-repo/cumulant-residual-cert),
which exposes the supported `certify()` entry point and the
chemistry-workflow adapters.

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
