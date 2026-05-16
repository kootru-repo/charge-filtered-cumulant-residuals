"""Standalone SHA256 integrity check for the deposited data.

Stdlib-only. Works on any environment with a python3 binary; no project
install required. Invoke from the repository root:

    python3 tools/check_integrity.py

Exits 0 on success (all hashes match MANIFEST.json), 1 on any mismatch.
Portable replacement for the inline `python3 -c '...'` snippet in README.md
(some Windows shells reject the embedded multi-line heredoc).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "MANIFEST.json"
    if not manifest_path.exists():
        print(f"FAIL: MANIFEST.json not found at {manifest_path}", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        print(
            "FAIL: MANIFEST.json has no `files` dict (expected schema: "
            '{"files": {"<path>": {"sha256": "..."}, ...}})',
            file=sys.stderr,
        )
        return 1

    failures = 0
    for rel_path, entry in files.items():
        target = repo_root / rel_path
        if not target.exists():
            print(f"FAIL  {rel_path:<48s}  (file missing)")
            failures += 1
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        expected = entry["sha256"]
        if actual == expected:
            print(f"OK    {rel_path}")
        else:
            print(f"FAIL  {rel_path}")
            print(f"      expected {expected}")
            print(f"      got      {actual}")
            failures += 1

    print()
    if failures:
        print(f"{failures} of {len(files)} file(s) failed SHA256 verification")
        return 1
    print(f"all {len(files)} deposited file(s) match MANIFEST.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
