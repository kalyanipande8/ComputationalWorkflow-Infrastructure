"""End-to-end: run the 45-workflow regression suite and the performance
monitoring/troubleshooting pass."""
import json
import os

from src.regression_testing import run_regression_suite, reliability_report
from src.monitoring import monitor_execution, troubleshooting_summary

os.makedirs("results", exist_ok=True)

print("=== Running 45-workflow regression suite ===")
regression_results = run_regression_suite()
reliability = reliability_report(regression_results)
print(reliability)

print("\n=== Performance monitoring ===")
monitoring_results = monitor_execution()
troubleshooting = troubleshooting_summary(monitoring_results)
print(troubleshooting)

summary = {
    "n_workflows": reliability["n_workflows"],
    "reliability_pct": reliability["reliability_pct"],
    "mean_runtime_sec": troubleshooting["mean_runtime_sec"],
    "n_over_budget": troubleshooting["n_over_budget"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
