# charge-filtered-cumulant-residuals

Reproducibility repository for the manuscript:

> **Charge- and block-refined bias bounds for second-order cumulant truncation on $\mathrm{U}(1)$-invariant fermionic states.**

[![Tests](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml)
[![Notebooks](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20129665.svg)](https://doi.org/10.5281/zenodo.20129665)

Every numerical claim in the manuscript reproduces in your browser, in about a minute per notebook, with no install. The algebraic theorems are proved in the paper itself; this repository is the operational reproducibility envelope.

## Reproduce in your browser (no install required)

Two browser-based options, both running on real Linux infrastructure.

### Verify on Ubuntu Linux (GitHub Codespaces)

<a href="https://codespaces.new/kootru-repo/charge-filtered-cumulant-residuals?quickstart=1"><img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces" width="200"/></a>

One click opens an Ubuntu 22.04 / Debian Bookworm container with VS Code in your browser. The devcontainer's `postCreateCommand` ([.devcontainer/setup.sh](.devcontainer/setup.sh)) installs `uv`, syncs dev + notebook extras, and runs `tools/check_integrity.py` automatically. After ~60 seconds you get a full Linux shell:

```bash
uv run pytest                                  # 39 unit tests, ~2 minutes
uv run python tools/check_integrity.py         # SHA256 verifier
uv run jupyter lab --ip=0.0.0.0 --no-browser   # JupyterLab on port 8888 (auto-forwarded)
```

Same OS family as the `tests.yml` / `notebooks.yml` CI runners, so a green Codespace verification matches the experience of a fresh Linux user cloning the repo. Free for 60 hours per month on a personal GitHub account (120h with GitHub Pro).

### Per-notebook (Google Colab)

Click any badge in the table below. The notebook opens in Colab, finishes in about a minute on the free CPU tier, and ends with `assert` cells that pass when the manuscript claim it verifies is reproduced. If a notebook finishes without an `AssertionError`, every claim cited in that row reproduced bit-exactly under the deposited environment.

| # | Notebook | What this notebook reproduces from the manuscript | Run |
|---|---|---|---|
| 00 | [`00_overview.ipynb`](notebooks/00_overview.ipynb) | Every headline partition-lattice and chemistry-catalog constant in one pass; orient before drilling into 01-05. | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/00_overview.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |
| 01 | [`01_partition_constants.ipynb`](notebooks/01_partition_constants.ipynb) | M\_r and B\_r partition-lattice constants and the charge-counting recurrence (Sec III, Thm 1). | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/01_partition_constants.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |
| 02 | [`02_chemistry_catalog.ipynb`](notebooks/02_chemistry_catalog.ipynb) | Block-refined constants take values in {1, 3, 5} on every word of the chemistry catalog (Sec III, Cor 1). | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/02_chemistry_catalog.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |
| 03 | [`03_implementation_audit.ipynb`](notebooks/03_implementation_audit.ipynb) | 3679-observable audit across 26 fixed-N states; effective constant near 2.0 vs the universal bound of 105 (Sec VI). | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/03_implementation_audit.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |
| 04 | [`04_correlated_calibration.ipynb`](notebooks/04_correlated_calibration.ipynb) | Sec V zero baseline at U=0 and correlation-controlled growth across a Hubbard U/t sweep. | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/04_correlated_calibration.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |
| 05 | [`05_diagnostic_ucb_demo.ipynb`](notebooks/05_diagnostic_ucb_demo.ipynb) | Sample-split upper confidence bound on synthetic shadows; one-sided coverage of the Sec V zero baseline (Sec IV). | <a href="https://colab.research.google.com/github/kootru-repo/charge-filtered-cumulant-residuals/blob/main/notebooks/05_diagnostic_ucb_demo.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" width="200"/></a> |

**Claim-to-notebook map.** For a row-by-row table mapping every manuscript claim (Theorems, Corollaries, headline numbers) to the specific notebook cell + assert + JSON file that reproduces it, see [`docs/claim_index.md`](docs/claim_index.md).

**No execution at all.** If you want to confirm only that the deposited JSON outputs are unmodified, the [data-integrity](#data-integrity-offline-no-python-needed) path below is a single stdlib-only Python script that hashes them against `MANIFEST.json`.

## Data integrity (offline, stdlib only)

A SHA256 verification of the five deposited JSONs in `data/` against the entries in `MANIFEST.json`. Stdlib-only; no `uv`, no `pip`, no project install required. From the repository root:

```bash
python3 tools/check_integrity.py
```

Expected output:

```
OK    data/audit_sector_cumulant_results.json
OK    data/calibration_chemistry.json
OK    data/screen_sector_audit_r5.json
OK    data/screen_sector_cumulant_extended.json
OK    data/screen_sector_cumulant_theorem.json

all 5 deposited file(s) match MANIFEST.json
```

Exit code 0 on success, 1 on any mismatch. The pytest-based equivalent at `tests/test_data_integrity.py` runs the same check inside the full local install.

**When to run this:**

- *Referee or auditor:* verify the deposited JSONs match what the manuscript references, before reading the audit notebooks. No install, no internet beyond the initial `git clone`.
- *Researcher who set `REGEN = True` in [`04_correlated_calibration.ipynb`](notebooks/04_correlated_calibration.ipynb):* confirm your freshly-regenerated `calibration_chemistry.json` matches the deposited SHA before quoting numbers downstream. (If it doesn't, you've drifted from the deposit and the manuscript's quoted values may not apply to your output.)
- *CI gate in a derived pipeline:* the script's exit code is wired for any runner. Drop into GitHub Actions as `- run: python3 tools/check_integrity.py`; the run fails loudly with per-file detail on any tampering.
- *Single-file partial check:* for a one-off verification, hash by hand and compare against the corresponding `sha256` entry in [`MANIFEST.json`](MANIFEST.json):

  ```bash
  sha256sum data/screen_sector_audit_r5.json
  ```

## Local install (only if you want to dig deeper)

Most referees will be served by the Colab path above. If you instead want to execute the full unit test suite, regenerate cells, or modify the code, install locally with [uv](https://docs.astral.sh/uv/) (one-line install: `curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS; `irm https://astral.sh/uv/install.ps1 | iex` on Windows).

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
uv sync --extra dev                                # core install
uv run pytest                                      # ~2 min: 39 unit tests + smoke regeneration
uv sync --extra dev --extra notebooks              # add Jupyter + matplotlib
uv run jupyter lab notebooks/00_overview.ipynb     # open + run all cells locally
```

Tests pass on Linux + macOS + Windows under Python 3.11, 3.12, 3.13. Linux + Python 3.12 is the primary CI gate; macOS / Windows / 3.11 / 3.13 run unit tests only. The `notebooks.yml` workflow runs every notebook headlessly on each push, so a green notebooks badge above means the notebooks reproduce end-to-end on a clean machine.

Core dependencies (`numpy >= 1.26`, `scipy >= 1.11`) and dev / notebook extras (`pytest`, `nbval`, `jupyterlab`, `matplotlib`, `ruff`) are declared in [`pyproject.toml`](pyproject.toml) and pinned in [`uv.lock`](uv.lock).

## Layout

```
src/connected_layer_sector/   importable Python package
notebooks/                    six numbered notebooks, claim-indexed to manuscript sections
tests/                        pytest suite (39 tests at present)
tests/mutation_check.py       optional: 10-mutation sanity check on the implementation
data/                         five deposited JSON outputs + MANIFEST.json
docs/claim_index.md           manuscript claim -> notebook + test + data file
tools/check_integrity.py      stdlib-only SHA256 verifier (data integrity, no install)
.devcontainer/                GitHub Codespaces + VS Code Dev Container config (Ubuntu)
.github/workflows/            tests.yml, notebooks.yml
```

## License

Code is MIT-licensed (see [`LICENSE`](LICENSE)). Notebooks, data, and documentation are CC-BY-4.0 (see [`LICENSE-DATA`](LICENSE-DATA)). Copyright held by Kootru Labs (a DBA of Kootru LLC).

## About

Maintained by **Kootru Labs**, Burlington, USA. Website: [labs.kootru.com](https://labs.kootru.com).

Author: **Andrew Craton** ([ORCID 0009-0001-2269-8599](https://orcid.org/0009-0001-2269-8599), [acraton@kootru.com](mailto:acraton@kootru.com)).

This repository is the canonical reproducibility envelope for the manuscript; its Zenodo deposit ([concept DOI 10.5281/zenodo.20129664](https://doi.org/10.5281/zenodo.20129664), auto-tracks the latest version) is the citable artefact for the numerical content. A user-facing companion library that calls the same primitives in production code is published at [`cumulant-residual-cert`](https://github.com/kootru-repo/cumulant-residual-cert) (full API reference + scaling characteristics: <https://kootru-repo.github.io/cumulant-residual-cert/>); its catalog constants are continuously cross-checked against this repository in CI.

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
  year         = {2026}
}
```

## Scope

This repository is the **operational reproducibility envelope**: it reproduces every quoted numerical value in the manuscript and runs in under five minutes on a laptop or in Colab. The `src/connected_layer_sector/` package is an internal artefact, structured for `pytest` to import its primitives during verification; it is **not** a user-facing library. Readers who want a stable API for production use should install the companion library [`cumulant-residual-cert`](https://github.com/kootru-repo/cumulant-residual-cert), which exposes the supported `certify()` entry point and the chemistry-workflow adapters.

It is intentionally NOT an adversarial verification surface. The following are out of scope here:

- adversarial state-search optimization for bound saturation,
- mutation testing of the implementation modules beyond the lightweight `tests/mutation_check.py` sanity harness,
- cross-validation against an independent symbolic-arithmetic oracle,
- large-$n$ ($n \ge 5$) stress on the three-theorem chain,
- the diagnostic-UCB Monte-Carlo coverage simulation.

The manuscript's algebraic theorems are proved in the paper itself. This repository confirms the deposited numerical values are recomputable; it does not attempt to falsify the proofs.
