#!/usr/bin/env bash
#
# Post-create setup for the GitHub Codespaces / VS Code Dev Container.
# Installs uv to a known location, syncs dev + notebook extras, and runs
# tools/check_integrity.py as a smoke test so the very first prompt the
# user sees confirms the deposited data has not drifted on this image.
#
# Idempotent: safe to re-run.

set -euo pipefail

echo "==> installing uv"
if ! command -v uv >/dev/null 2>&1; then
    # Pin UV_INSTALL_DIR so PATH inheritance is deterministic (same lesson as
    # the Colab bootstrap; see notebook bootstrap cells for the writeup).
    export UV_INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$UV_INSTALL_DIR"
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
uv --version

echo "==> syncing dev + notebook extras"
uv sync --extra dev --extra notebooks

echo "==> running data-integrity smoke test"
uv run python3 tools/check_integrity.py

echo
echo "================================================================"
echo "  charge-filtered-cumulant-residuals devcontainer ready (Ubuntu)"
echo "================================================================"
echo
echo "Try one of:"
echo "  uv run pytest                                       # 39 unit tests, ~2 min"
echo "  uv run python tools/check_integrity.py              # SHA256 verifier"
echo "  uv run jupyter lab --ip=0.0.0.0 --no-browser        # JupyterLab on port 8888"
echo "  uv run jupyter execute notebooks/00_overview.ipynb  # headless notebook run"
echo
