import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.workflow_registry import WORKFLOWS, run_workflow
from src.regression_testing import run_regression_suite, reliability_report
from src.monitoring import monitor_execution, troubleshooting_summary


def test_exactly_45_workflows_registered():
    assert len(WORKFLOWS) == 45


def test_every_workflow_runs_without_error():
    for wf in WORKFLOWS:
        run_workflow(wf)  # raises if broken


def test_regression_suite_is_fully_reliable():
    results = run_regression_suite()
    report = reliability_report(results)
    assert report["reliability_pct"] == 100.0
    assert report["failed_workflows"] == []


def test_monitoring_times_every_workflow():
    results = monitor_execution()
    assert len(results) == 45
    assert all(r["elapsed_sec"] >= 0 for r in results)


def test_troubleshooting_summary_structure():
    results = monitor_execution()
    summary = troubleshooting_summary(results)
    assert summary["n_workflows"] == 45
    assert summary["mean_runtime_sec"] >= 0
