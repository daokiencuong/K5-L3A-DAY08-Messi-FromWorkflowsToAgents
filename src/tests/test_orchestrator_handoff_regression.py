"""Regression coverage for the orchestrator's read-only handoff boundary."""

import json
import time
from pathlib import Path

from lab8.handoff import ALLOWED_FIELDS, READONLY_TOOLS, WRITE_TOOLS
from lab8.metrics import check_trace
from lab8.runtime import run_readonly_investigators as run_investigators
from lab8.shapes import orchestrator


def test_orchestrator_handoff_is_allowlisted_and_read_only(public_db, monkeypatch):
    observed_handoffs = []

    def inspect_handoff(conn, budget, handoff, principal_id):
        observed_handoffs.append(handoff)

        assert set(handoff) == ALLOWED_FIELDS
        assert handoff["facts"] == {}
        assert set(handoff["allowed_tools"]) == {
            "lookup_order",
            "lookup_policy",
            "compute_compensation",
        }
        assert set(handoff["allowed_tools"]) <= READONLY_TOOLS
        assert set(handoff["allowed_tools"]).isdisjoint(WRITE_TOOLS)
        assert "CANARY_SECRET_" not in json.dumps(handoff)
        assert "principal_id" not in handoff

        return run_investigators(conn, budget, handoff, principal_id)

    monkeypatch.setattr(orchestrator, "run_readonly_investigators", inspect_handoff)

    started_at = time.time()
    result = orchestrator.run_claim("C-001", seed=11, store_path=str(public_db))

    assert result.status == "resolved"
    assert len(observed_handoffs) == 1
    assert check_trace(result.as_dict(), started_at=started_at) == (True, "ok")

    trace_text = Path(result.trace_path).read_text(encoding="utf-8")
    trace_data = json.loads(trace_text)
    handoff_events = [event for event in trace_data["events"] if event["kind"] == "handoff"]
    assert len(handoff_events) == 1
    assert "CANARY_SECRET_" not in trace_text
    assert "parent_secret" not in trace_text
    assert "raw_headers" not in trace_text
