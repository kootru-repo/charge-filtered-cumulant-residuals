"""SHA256 verification of the deposited JSONs against MANIFEST.json.

Confirms the deposited results have not been corrupted. Distinct from
``test_smoke_regeneration``, which verifies the pipeline can regenerate a
representative cell from code.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST.json"


def test_manifest_present():
    assert MANIFEST.exists(), f"missing {MANIFEST}; run `cls-manifest` first"


def _load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_provenance_fields():
    """Schema v2 must include provenance, not just hashes."""
    m = _load_manifest()
    required = {
        "schema_version",
        "generated",
        "git_tag",
        "git_commit",
        "python_version",
        "platform",
        "deterministic_seed_policy",
        "files",
    }
    missing = required - set(m.keys())
    assert not missing, f"manifest missing fields: {missing}"
    assert m["schema_version"] >= 2


@pytest.mark.parametrize("rel_path", [
    "data/screen_sector_cumulant_theorem.json",
    "data/screen_sector_cumulant_extended.json",
    "data/screen_sector_audit_r5.json",
    "data/audit_sector_cumulant_results.json",
    "data/calibration_chemistry.json",
])
def test_deposited_json_sha256(rel_path):
    """Each deposited JSON's SHA256 matches the manifest entry."""
    m = _load_manifest()
    abs_path = ROOT / rel_path
    assert abs_path.exists(), f"missing data file: {rel_path}"
    if rel_path not in m["files"]:
        pytest.skip(f"{rel_path} not in manifest (regenerate with `cls-manifest`)")
    expected = m["files"][rel_path]["sha256"]
    actual = hashlib.sha256(abs_path.read_bytes()).hexdigest()
    assert actual == expected, (
        f"sha256 mismatch for {rel_path}: "
        f"manifest={expected[:16]}... actual={actual[:16]}..."
    )
