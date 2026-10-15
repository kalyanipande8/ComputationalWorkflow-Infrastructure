"""Real regression testing: runs every one of the 45 workflows twice and
verifies deterministic, reproducible output (same seed -> identical
result) -- the genuine reliability guarantee an HPC workflow regression
suite is meant to confirm."""
from __future__ import annotations

from .workflow_registry import WORKFLOWS, run_workflow


def run_regression_suite() -> list[dict]:
    results = []
    for wf in WORKFLOWS:
        try:
            run1 = run_workflow(wf)
            run2 = run_workflow(wf)
            passed = run1 == run2
            results.append({"workflow_id": wf["workflow_id"], "name": wf["name"], "passed": passed, "error": None})
        except Exception as e:
            results.append({"workflow_id": wf["workflow_id"], "name": wf["name"], "passed": False, "error": str(e)})
    return results


def reliability_report(results: list[dict]) -> dict:
    n_passed = sum(r["passed"] for r in results)
    return {"n_workflows": len(results), "n_passed": n_passed,
            "reliability_pct": round(100 * n_passed / len(results), 2),
            "failed_workflows": [r["workflow_id"] for r in results if not r["passed"]]}


if __name__ == "__main__":
    results = run_regression_suite()
    print(reliability_report(results))
