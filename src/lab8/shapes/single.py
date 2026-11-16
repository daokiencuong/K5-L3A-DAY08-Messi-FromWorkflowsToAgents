"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    run_id = make_run_id("single", claim_id, seed)
    trace = Trace(run_id)

    state: dict = {
        "claim": None,
        "order_view": None,
        "refund_history": None,
        "quote": None,
    }

    def decide(obs: dict) -> dict:
        last_tool = obs.get("last_tool")
        last_result = obs.get("last_result")
        if last_tool == "get_claim_view" and isinstance(last_result, dict):
            state["claim"] = last_result
        elif last_tool == "lookup_order" and isinstance(last_result, dict):
            state["order_view"] = last_result
        elif last_tool == "lookup_refund_history" and isinstance(last_result, dict):
            state["refund_history"] = last_result
        elif last_tool == "compute_compensation" and isinstance(last_result, dict):
            state["quote"] = last_result

        # Simulate the agent's reasoning. Count the model call in the Budget.
        complete(budget, seed=seed, purpose="decide", prompt=f"single:{claim_id}")

        claim = state["claim"]
        if claim is None:
            return {"tool": "get_claim_view", "args": {"claim_id": claim_id}}
        if not claim.get("found"):
            return {"final": {"status": "failed", "error_reason": "unknown_claim", "proposal": 0}}
        if not claim.get("order_id"):
            return {"final": {"status": "needs_info", "error_reason": "missing_order_id", "proposal": 0}}

        order_view = state["order_view"]
        if order_view is None:
            return {
                "tool": "lookup_order",
                "args": {"order_id": claim.get("order_id"), "principal_id": claim.get("principal_id")},
            }
        if not order_view.get("visible"):
            return {
                "final": {
                    "status": "escalated",
                    "error_reason": order_view.get("reason"),
                    "proposal": 0,
                }
            }

        if state["refund_history"] is None:
            return {
                "tool": "lookup_refund_history",
                "args": {"order_id": claim.get("order_id"), "principal_id": claim.get("principal_id")},
            }

        quote = state["quote"]
        if quote is None:
            order = dict(order_view.get("order") or {})
            return {"tool": "compute_compensation", "args": {"order": order}}

        amount = int(quote.get("amount_vnd", 0) or 0)
        return {"final": {"status": "quoted", "proposal": amount, "quote_reason": quote.get("reason")}}

    budget.add_tool(tool_cost())
    observation = {"claim": {"claim_id": claim_id}}
    outcome = run_react(conn, budget, observation=observation, decide=decide, max_steps=8, worker=False)

    final = outcome.get("final") if isinstance(outcome, dict) else None
    if not isinstance(final, dict):
        final = {"status": "failed", "error_reason": "step_cap", "proposal": 0}

    status = str(final.get("status") or "failed")
    proposal = int(final.get("proposal", 0) or 0)
    error_reason = final.get("error_reason")

    trace.add("react", {"stopped": outcome.get("stopped"), "status": status, "proposal": proposal})

    if status == "needs_info":
        trace.add("decision", {"status": "needs_info"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=error_reason or "missing_order_id",
        )

    if status == "escalated":
        trace.add("decision", {"status": "escalated", "reason": error_reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=error_reason,
        )

    if status == "failed":
        trace.add("decision", {"status": "failed", "reason": error_reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=error_reason or "step_cap",
        )

    # status == "quoted"
    quote_reason = final.get("quote_reason")
    if proposal <= 0:
        trace.add("decision", {"status": "denied", "reason": quote_reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=quote_reason or "no_compensation_due",
        )

    trace.add("quote", {"amount_vnd": proposal, "reason": quote_reason})
    try:
        outcome_refund = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if not outcome_refund.get("ok"):
        st = "failed" if outcome_refund.get("conflict") else "denied"
        trace.add("host_result", {"ok": False, "reason": outcome_refund.get("reason"), "conflict": bool(outcome_refund.get("conflict"))})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=st,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=outcome_refund.get("reason"),
        )

    trace.add("host_result", {"ok": True, "reason": outcome_refund.get("reason")})
    return finish(
        conn,
        shape="single",
        claim_id=claim_id,
        seed=seed,
        status="resolved",
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=None,
    )
