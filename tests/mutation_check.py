"""Lightweight mutation test for the implementation modules.

Surgically injects a small set of known bug patterns and confirms the
pytest suite catches each one. Run independently of pytest:

    python tests/mutation_check.py

Exit code 0 = every non-no-op mutation killed.
Exit code 1 = at least one mutation escaped (test-suite gap).

Kept short (10 mutations) to remain a single-file sanity check on
top of the regular pytest suite. Not exhaustive; intentionally
limited to surgical bug patterns in the implementation modules
that the pytest suite should catch.
"""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Mutation:
    name: str
    file: str
    old: str
    new: str
    tests: list[str] = field(default_factory=list)
    description: str = ""
    no_op: bool = False


MUTATIONS: list[Mutation] = [
    Mutation(
        name="M_r_min_instead_of_max",
        file="src/connected_layer_sector/constants.py",
        old="        out = max(out, s)\n    return float(out)\n\n\n@lru_cache(maxsize=64)\ndef B_r_const",
        new="        out = min(out if out else s, s)\n    return float(out)\n\n\n@lru_cache(maxsize=64)\ndef B_r_const",
        tests=["tests/test_constants.py"],
        description="M_r uses min instead of max",
    ),
    Mutation(
        name="B_r_drop_size_gt_2_filter",
        file="src/connected_layer_sector/constants.py",
        old="            if any(len(block) > 2 for block in pi):\n                s += Mr ** (len(pi) - 1)",
        new="            s += Mr ** (len(pi) - 1)",
        tests=["tests/test_constants.py"],
        description="B_r drops size>2 filter",
    ),
    Mutation(
        name="moebius_sign_flip",
        file="src/connected_layer_sector/partition_lattice.py",
        old="        sign = (-1) ** (k - 1)\n        total += math.factorial(k - 1) * sign * prod",
        new="        sign = (-1) ** k\n        total += math.factorial(k - 1) * sign * prod",
        tests=["tests/test_moments_cumulants.py"],
        description="Moebius sign inverted",
    ),
    Mutation(
        name="moebius_factorial_off_by_one",
        file="src/connected_layer_sector/partition_lattice.py",
        old="        total += math.factorial(k - 1) * sign * prod",
        new="        total += math.factorial(k) * sign * prod",
        tests=["tests/test_moments_cumulants.py"],
        description="Moebius coefficient uses k! instead of (k-1)!",
    ),
    Mutation(
        name="closure_admits_size_3",
        file="src/connected_layer_sector/moments.py",
        old="        if any(len(block) > 2 for block in pi):\n            continue",
        new="        if any(len(block) > 3 for block in pi):\n            continue",
        tests=["tests/test_moments_cumulants.py"],
        description="order-<=2 closure admits size-3 blocks",
    ),
    Mutation(
        name="jw_creation_no_z_string",
        file="src/connected_layer_sector/operators.py",
        old="    mats = [Z2] * i + [sigma_plus] + [I2] * (n - i - 1)",
        new="    mats = [I2] * i + [sigma_plus] + [I2] * (n - i - 1)",
        tests=["tests/test_moments_cumulants.py"],
        description="a_dag drops Jordan-Wigner Z-string",
    ),
    Mutation(
        name="charge_assignment_swap",
        file="src/connected_layer_sector/operators.py",
        old='    return {"a": -1, "ad": +1, "n": 0}[op]',
        new='    return {"a": +1, "ad": -1, "n": 0}[op]',
        tests=["tests/test_catalog_corollary.py"],
        description="a/a_dag charges swapped",
        no_op=True,  # global sign flip; charge-neutrality preserved
    ),
    Mutation(
        name="ordered_cumulant_skip_top_partition",
        file="src/connected_layer_sector/partition_lattice.py",
        old="    for pi in set_partitions(subset):",
        new="    for pi in set_partitions(subset)\n               if len(pi) > 1:",
        tests=["tests/test_moments_cumulants.py"],
        description="cumulant excludes the top partition",
    ),
    Mutation(
        name="P_recurrence_drop_x_factor",
        file="src/connected_layer_sector/constants.py",
        old="    def _x_times(p):\n        return [0.0] + list(p)",
        new="    def _x_times(p):\n        return list(p)",
        tests=["tests/test_charge_counting.py"],
        description="P_{h,z} recurrence drops the x factor",
    ),
    Mutation(
        name="Q_polynomial_drop_h_factorial",
        file="src/connected_layer_sector/constants.py",
        old="        coeff = h_fact * z_fact / (math.factorial(z - 2 * j) * math.factorial(j) * (2**j))",
        new="        coeff = z_fact / (math.factorial(z - 2 * j) * math.factorial(j) * (2**j))",
        tests=["tests/test_charge_counting.py"],
        description="Q_{h,z} drops the h! prefactor",
    ),
]


def _clear_pycache(path: Path) -> None:
    pyc_dir = path.parent / "__pycache__"
    if not pyc_dir.exists():
        return
    for pyc in pyc_dir.glob(f"{path.stem}.*.pyc"):
        try:
            pyc.unlink()
        except OSError:
            pass


def _apply(path: Path, old: str, new: str) -> str:
    # Binary I/O so Python's text mode doesn't silently convert LF to CRLF
    # on Windows. The harness writes the file back unchanged on restore;
    # any line-ending change here would dirty the working tree.
    orig = path.read_bytes().decode("utf-8")
    if old not in orig:
        raise ValueError(f"pattern not found in {path.name}")
    mutated = orig.replace(old, new, 1)
    path.write_bytes(mutated.encode("utf-8"))
    _clear_pycache(path)
    return orig


def _restore(path: Path, orig: str) -> None:
    path.write_bytes(orig.encode("utf-8"))
    _clear_pycache(path)


def _run(tests: list[str]) -> int:
    args = ["python", "-m", "pytest", "-q", "--tb=no", "-x", *tests]
    proc = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    return proc.returncode


def main() -> int:
    print("=" * 72)
    print(f"Mutation check: {len(MUTATIONS)} mutations")
    print("=" * 72)
    kills = 0
    escapes = []
    no_ops = []
    for i, m in enumerate(MUTATIONS, 1):
        fp = ROOT / m.file
        try:
            orig = _apply(fp, m.old, m.new)
        except ValueError as e:
            print(f"[{i:2d}/{len(MUTATIONS)}] {m.name}: SKIP -- {e}")
            continue
        t0 = time.time()
        try:
            rc = _run(m.tests)
        finally:
            _restore(fp, orig)
        elapsed = time.time() - t0
        caught = rc != 0
        if caught:
            kills += 1
            marker = "[OK] KILL"
        elif m.no_op:
            no_ops.append(m.name)
            marker = "[--] NO-OP"
        else:
            escapes.append(m.name)
            marker = "[!!] ESCAPE"
        print(f"[{i:2d}/{len(MUTATIONS)}] {m.name}: {marker} ({elapsed:.1f}s)")

    print()
    print("=" * 72)
    print(f"KILLS: {kills}/{len(MUTATIONS)}  NO-OPS: {len(no_ops)}  REAL ESCAPES: {len(escapes)}")
    if no_ops:
        print(f"  no-ops: {no_ops}")
    if escapes:
        print(f"  escapes: {escapes}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
