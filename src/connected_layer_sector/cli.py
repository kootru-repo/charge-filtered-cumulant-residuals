"""Console entry points referenced by pyproject.toml."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def calibrate() -> None:
    """Run the Hubbard correlated-state calibration and write the JSON."""
    parser = argparse.ArgumentParser(
        description="Hubbard correlated-state calibration of the residual certificate.",
    )
    parser.add_argument("--n-sites", type=int, default=4)
    parser.add_argument("--Ut", type=float, nargs="+", default=[0.0, 1.0, 4.0, 8.0, 16.0])
    parser.add_argument("--out", type=str, default="data/calibration_chemistry.json")
    args = parser.parse_args()

    import numpy as np

    from connected_layer_sector import (
        evaluate_catalog,
        fermionic_orbital_rotation,
        hubbard_ground_state,
        tight_binding_eigenbasis,
    )

    n_sites = args.n_sites
    n_orb = 2 * n_sites
    eps, V_mat = tight_binding_eigenbasis(n_sites, t=1.0)
    W_full = np.zeros((n_orb, n_orb))
    W_full[:n_sites, :n_sites] = V_mat
    W_full[n_sites:, n_sites:] = V_mat
    V_many_body = fermionic_orbital_rotation(W_full, n_orb)

    rows = []
    for U in args.Ut:
        psi, E0 = hubbard_ground_state(n_sites, 1.0, U, n_sites // 2, n_sites // 2)
        psi_rot = V_many_body @ psi
        psi_rot = psi_rot / np.linalg.norm(psi_rot)
        rho_rot = np.outer(psi_rot, psi_rot.conj())
        metrics = evaluate_catalog(rho_rot, n_orb, r=4)
        rows.append(
            {
                "cell": "hubbard_1d_open",
                "n_sites": n_sites,
                "n_orb": n_orb,
                "n_up": n_sites // 2,
                "n_dn": n_sites // 2,
                "U_over_t": U,
                "E_ground": E0,
                "basis": "U=0 noninteracting single-particle eigenbasis",
                **metrics,
            }
        )

    out = {
        "schema_version": 1,
        "generated": time.strftime("%Y-%m-%d"),
        "implementation_status": {
            "hubbard": "implemented",
            "h2_sto3g": "deferred (PySCF unavailable)",
            "lih_sto3g": "deferred (PySCF unavailable)",
        },
        "framing": (
            "Operational calibration on a correlated 1D Hubbard ground state. "
            "NOT a theorem validation, NOT a complete chemistry workflow, NOT "
            "a measurement-advantage claim."
        ),
        "hubbard": rows,
    }
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {args.out} ({len(rows)} rows)")


def generate_manifest() -> None:
    """Recompute SHA256 + provenance metadata for the data/ tree."""
    import hashlib
    import os
    import platform
    import subprocess
    import sys

    root = Path(".").resolve()
    excludes_ext = {".aux", ".log", ".out", ".bbl", ".blg", ".toc", ".pyc"}
    excludes_dir = {"__pycache__", ".ipynb_checkpoints", ".pytest_cache"}

    files: dict[str, dict] = {}
    for root_dir in ("data", "notebooks", "docs"):
        p = Path(root_dir)
        if not p.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in excludes_dir]
            for fn in sorted(filenames):
                if Path(fn).suffix in excludes_ext:
                    continue
                fp = Path(dirpath) / fn
                with open(fp, "rb") as f:
                    data = f.read()
                files[fp.as_posix()] = {
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": fp.stat().st_size,
                }

    git_tag = "unknown"
    git_commit = "unknown"
    try:
        git_tag = (
            subprocess.run(
                ["git", "describe", "--tags", "--always"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
            or "unknown"
        )
        git_commit = (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
            or "unknown"
        )
    except FileNotFoundError:
        pass

    manifest = {
        "schema_version": 2,
        "generated": time.strftime("%Y-%m-%d"),
        "git_tag": git_tag,
        "git_commit": git_commit,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "deterministic_seed_policy": (
            "SHA256(label) truncated to 64-bit unsigned int via "
            "connected_layer_sector.deterministic_seed"
        ),
        "files": files,
    }
    out = root / "MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"MANIFEST.json: {len(files)} files cataloged")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit("Use the console entry points: cls-calibrate, cls-manifest, ...")
