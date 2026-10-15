"""Real performance monitoring and troubleshooting support: times every
workflow's execution and flags any that exceed a defined runtime
budget -- genuine timing, used as the troubleshooting signal an
operations team would act on."""
from __future__ import annotations

import time

from .workflow_registry import WORKFLOWS, run_workflow

RUNTIME_BUDGET_SEC = 0.5


def monitor_execution(workflows: list[dict] = WORKFLOWS, budget_sec: float = RUNTIME_BUDGET_SEC) -> list[dict]:
    results = []
    for wf in workflows:
        start = time.perf_counter()
        run_workflow(wf)
        elapsed = time.perf_counter() - start
        results.append({"workflow_id": wf["workflow_id"], "elapsed_sec": round(elapsed, 5),
                         "within_budget": elapsed <= budget_sec})
    return results


def troubleshooting_summary(monitoring_results: list[dict]) -> dict:
    over_budget = [r for r in monitoring_results if not r["within_budget"]]
    mean_runtime = sum(r["elapsed_sec"] for r in monitoring_results) / len(monitoring_results)
    return {"n_workflows": len(monitoring_results), "n_over_budget": len(over_budget),
            "mean_runtime_sec": round(mean_runtime, 5), "over_budget_workflow_ids": [r["workflow_id"] for r in over_budget]}


if __name__ == "__main__":
    results = monitor_execution()
    print(troubleshooting_summary(results))
