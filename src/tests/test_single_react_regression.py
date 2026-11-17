"""Regression coverage for the single shape's ReAct boundary."""

import json
import time
from pathlib import Path

from lab8.durability import InjectedCrash
from lab8.metrics import check_trace
from lab8.shapes import single


def test_single_trace_is_clean_and_no_write_tool_in_trace(public_db, monkeypatch):
    # Ensure the runtime never dispatches a write tool for the agent.
    from lab8 import runtime as rt

    original_dispatch = rt.dispatch

    def guarded_dispatch(conn, budget, name, args, *, worker):
        assert name != "issue_refund", "single agent must not call issue_refund via runtime"
        return original_dispatch(conn, budget, name, args, worker=worker)

    monkeypatch.setattr(rt, "dispatch", guarded_dispatch)
    # single imports dispatch by reference through runtime module already; ensure shapes.single uses patched
    monkeypatch.setattr(single, "run_react", rt.run_react)

    started_at = time.time()
    result = single.run_claim("C-001", seed=11, store_path=str(public_db))

    assert result.status == "resolved"
    assert check_trace(result.as_dict(), started_at=started_at) == (True, "ok")

    trace_text = Path(result.trace_path).read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in trace_text
    assert "parent_secret" not in trace_text
    assert "raw_headers" not in trace_text
    assert "issue_refund" not in trace_text


def test_single_forwards_crash_at_and_propagates(public_db):
    crashed = False
    try:
        single.run_claim(
            "C-012", seed=11, store_path=str(public_db),
            crash_at="after_effect_before_checkpoint",
        )
    except InjectedCrash:
        crashed = True
    assert crashed, "single must forward crash_at and let InjectedCrash propagate"


def test_single_step_cap_respected(public_db):
    result = single.run_claim("C-001", seed=11, store_path=str(public_db))
    # model_calls + tool_calls combined must not exceed a sane bound (max_steps=8 + bookkeeping)
    assert result.model_calls + result.tool_calls <= 32
    assert result.status in {"resolved", "denied", "escalated", "needs_info", "failed"}
