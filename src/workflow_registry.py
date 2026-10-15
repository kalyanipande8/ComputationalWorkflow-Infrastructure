"""A registry of 45 HPC computational workflows, each a real, runnable
Python function (not a shell-script stub) -- genuine small computations
representative of common HPC pipeline steps, so regression testing has
something real to execute and verify."""
from __future__ import annotations

import hashlib

import numpy as np


def _checksum_step(seed: int) -> str:
    rng = np.random.default_rng(seed)
    data = rng.integers(0, 256, 1000).astype(np.uint8).tobytes()
    return hashlib.md5(data).hexdigest()


def _matrix_step(seed: int) -> float:
    rng = np.random.default_rng(seed)
    m = rng.normal(0, 1, (30, 30))
    return float(np.trace(m @ m.T))


def _sort_step(seed: int) -> bool:
    rng = np.random.default_rng(seed)
    arr = rng.normal(0, 1, 500)
    sorted_arr = np.sort(arr)
    return bool(np.all(np.diff(sorted_arr) >= 0))


def _aggregation_step(seed: int) -> float:
    rng = np.random.default_rng(seed)
    arr = rng.normal(50, 10, 200)
    return float(arr.mean())


STEP_FUNCTIONS = {"checksum": _checksum_step, "matrix": _matrix_step, "sort": _sort_step, "aggregation": _aggregation_step}

WORKFLOWS = [
    {"workflow_id": f"WF-{i+1:03d}", "name": f"{step_type}_workflow_{i+1}", "step_type": step_type, "seed": i}
    for i, step_type in enumerate(
        ["checksum"] * 12 + ["matrix"] * 11 + ["sort"] * 11 + ["aggregation"] * 11
    )
]

assert len(WORKFLOWS) == 45, f"expected 45 workflows, got {len(WORKFLOWS)}"


def run_workflow(workflow: dict):
    fn = STEP_FUNCTIONS[workflow["step_type"]]
    return fn(workflow["seed"])


if __name__ == "__main__":
    for wf in WORKFLOWS[:5]:
        print(wf["workflow_id"], run_workflow(wf))
