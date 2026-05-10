# charge-filtered-cumulant-residuals

Reproducibility repository for the manuscript:

> **Charge-filtered cumulant residual bounds for charge-neutral fermionic-word observables on $\mathrm{U}(1)$-invariant states.**

[![Tests](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/tests.yml)
[![Notebooks](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml/badge.svg)](https://github.com/kootru-repo/charge-filtered-cumulant-residuals/actions/workflows/notebooks.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kootru-repo/charge-filtered-cumulant-residuals/HEAD?labpath=notebooks%2F00_overview.ipynb)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

This repository reproduces every numerical claim in the manuscript. Math content is algebraic and proved in the manuscript itself; this repository is the operational reproducibility envelope.

## Three reproduction paths

| Path | Effort | What it verifies |
|---|---|---|
| **Binder one-click** | ~3 min cold start | Notebooks execute end-to-end with explicit `assert` cells passing |
| **Local pip + pytest** | ~2 min on a laptop | Full unit-test suite + smoke regeneration of one cell |
| **Data-only check** | ~10 sec | SHA256 verification of deposited JSONs against `MANIFEST.json` |

### Binder

Click the Binder badge above. Open `notebooks/00_overview.ipynb` and follow the numbered notebook order (00 → 05). Each notebook ends with `assert` cells that confirm the headline claim of that section.

### Local

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
pip install -e .[dev]
pytest
```

Tests pass on Linux + macOS + Windows under Python 3.11, 3.12, 3.13. Linux + Python 3.12 is the primary CI gate (matches Binder); macOS / Windows / 3.11 / 3.13 run unit tests only.

### Data integrity

```bash
pytest tests/test_data_integrity.py
```

Hashes the five deposited JSONs in `data/` against the SHA256 entries in `MANIFEST.json`. Confirms the deposited results have not been corrupted.

## Layout

```
src/connected_layer_sector/   importable Python package
notebooks/                    six numbered notebooks, claim-indexed to manuscript sections
tests/                        pytest suite (~50 tests, >90% coverage target)
data/                         five deposited JSON outputs + MANIFEST.json
docs/                         claim_index.md (manuscript claim → notebook + test + data)
binder/                       environment.yml + runtime.txt + postBuild
.github/workflows/            tests.yml, notebooks.yml, lint.yml, dependabot
```

See `docs/claim_index.md` for the manuscript-to-repository claim map.

## License

Code is MIT-licensed (see `LICENSE`). Notebooks, data, and documentation are CC-BY-4.0 (see `LICENSE-DATA`).

## Citation

If you use this code or data, please cite the manuscript and the Zenodo deposit. See `CITATION.cff`.

## How to verify a specific manuscript claim

1. Open `docs/claim_index.md`. Find the claim by manuscript section.
2. The table tells you which notebook to open, which test to run, and which JSON to inspect.
3. Each notebook ends with one or more `assert` cells that verify the claim numerically.
