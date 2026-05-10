# Reproducibility

Every numerical claim in the manuscript can be verified through one of three reproduction paths.

## Path 1: Binder one-click

Click the Binder badge in the README. Wait for the cold start (~3-5 minutes). Open `notebooks/00_overview.ipynb`. Click "Run All".

Each notebook ends with `assert` cells. Every `assert` should pass. If any fails, the failing cell prints which manuscript claim is affected.

**Expected runtimes on free-tier Binder** (cold start excluded):
- `00_overview.ipynb`: < 30 seconds
- `01_partition_constants.ipynb`: < 1 minute
- `02_chemistry_catalog.ipynb`: < 1 minute
- `03_implementation_audit.ipynb` (smoke subset): < 2 minutes
- `04_correlated_calibration.ipynb`: ~ 4 minutes
- `05_diagnostic_ucb_demo.ipynb`: < 2 minutes

Total full-notebook run on Binder: ~10 minutes after cold start.

## Path 2: Local pip install + pytest

```bash
git clone https://github.com/kootru-repo/charge-filtered-cumulant-residuals
cd charge-filtered-cumulant-residuals
pip install -e ".[dev]"
cls-manifest    # generate MANIFEST.json with provenance
pytest          # ~30 unit tests, ~2 minutes on a laptop
```

Tests pass on Linux + macOS + Windows under Python 3.11, 3.12, 3.13. Linux + Python 3.12 is the primary CI gate (matches Binder); the other combinations run unit tests only.

To execute notebooks programmatically:

```bash
pytest --nbval-lax notebooks/
```

## Path 3: Data integrity verification only

If you only want to confirm the deposited results have not been corrupted:

```bash
pip install -e .
cls-manifest
pytest tests/test_data_integrity.py
```

This hashes the five deposited JSONs against the SHA256 entries in `MANIFEST.json` and validates the manifest's provenance fields (schema version, git commit/tag, Python version, platform, deterministic-seed policy).

## Smoke regeneration

`tests/test_smoke_regeneration.py` regenerates the Hubbard $U=0$ baseline from code, in your local environment, and compares it to the deposited calibration JSON. This confirms the *pipeline* is reproducible, not just that the deposited file is unchanged. Runs in ~30 seconds.

## What if Binder is slow or unavailable?

Free-tier Binder occasionally evicts or rebuilds. If the badge is slow or unresponsive, fall back to Path 2 (local install). All claims are reachable from `pytest`; the notebooks are illustrative but not the only verification surface.

## Determinism

All numerical claims are deterministic given the seed. The seed helper is in `connected_layer_sector.deterministic_seed` (a SHA256-derived 64-bit integer of a string label). It is platform-independent and does not depend on any file outside the repository.

## Reporting reproducibility issues

If a `pytest` test or a notebook `assert` fails on your machine, please file an issue with:

- Operating system + Python version
- Output of `pip list` for `numpy`, `scipy`, the package itself
- Full pytest output for the failing test (or the notebook traceback)
- Whether `tests/test_data_integrity.py` passed (file integrity is a precondition)

This narrows whether the issue is data corruption, dependency drift, or a genuine pipeline regression.
