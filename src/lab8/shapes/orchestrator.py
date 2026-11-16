"""Shape C — orchestrator plus read-only investigators. Student work.

1. Build a handoff with `lab8.handoff.make_handoff`. Allowed tools are read-only.
   Never put parent_secret, raw headers, or the full claim row into facts.
2. `lab8.runtime.run_readonly_investigators` runs those tools.
3. The orchestrator quotes from the investigator's order view and calls
   `durability.issue_refund`. Investigators have no write registry.
   Pass the full quote; the host subtracts earlier refunds on the same order.
   `lookup_refund_history` is a read-only tool you may hand to an investigator.
4. Trace the sanitized handoff, not the parent context.

An LLM summary of the parent context is not a sanitizer. Use the allowlist.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.handoff import make_handoff
from lab8.runtime import run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import get_claim_view, tool_cost
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
        budget = Budget()
        run_id = make_run_id("orchestrator", claim_id, seed)
        trace = Trace(run_id)

        # Keep the parent context in memory only. In particular, never trace
        # the ticket, principal id, or complete claim view.
        budget.add_tool(tool_cost())
        claim = get_claim_view(conn, claim_id)
        trace.add(
            "claim_lookup",
            {
                "found": bool(claim.get("found")),
                "claim_id": claim_id,
                "has_order_id": bool(claim.get("order_id")),
            },
        )

        if not claim.get("found"):
            trace.add("decision", {"status": "failed", "reason": "unknown_claim"})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status="failed",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason="unknown_claim",
            )

        if not claim.get("order_id"):
            trace.add("decision", {"status": "needs_info", "reason": "missing_order_id"})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status="needs_info",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason="missing_order_id",
            )

        # make_handoff enforces the field allowlist and rejects write tools.
        # Do not forward ticket text or other parent-context fields as facts.
        handoff = make_handoff(
            request_id=f"REQ-{claim_id}",
            claim_id=claim_id,
            task="check_applicable_policy_and_quote",
            facts={},
            allowed_tools=["lookup_order", "lookup_policy", "compute_compensation"],
        )
        trace.add("handoff", safe_dump(handoff))

        investigation = run_readonly_investigators(
            conn,
            budget,
            handoff,
            principal_id=str(claim["principal_id"]),
        )
        tools = investigation.get("tools", {})
        order_result = tools.get("lookup_order") or {}
        trace.add(
            "investigation",
            {
                "lookup_order": safe_dump(order_result),
                "policy_count": len((tools.get("lookup_policy") or {}).get("policies") or []),
            },
        )

        if not order_result.get("visible"):
            reason = str(order_result.get("reason") or "order_not_visible")
            trace.add("decision", {"status": "escalated", "reason": reason})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status="escalated",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason=reason,
            )

        quote_result = tools.get("compute_compensation")
        if not isinstance(quote_result, dict) or "amount_vnd" not in quote_result:
            trace.add("decision", {"status": "failed", "reason": "missing_quote"})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status="failed",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason="missing_quote",
            )

        proposal = int(quote_result["amount_vnd"])
        trace.add("quote", safe_dump(quote_result))
        if proposal <= 0:
            reason = str(quote_result.get("reason") or "no_compensation_due")
            trace.add("decision", {"status": "denied", "reason": reason})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status="denied",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason=reason,
            )

        # The quote is the full entitlement. Host code enforces approval,
        # per-order cap, idempotency, and the actual ledger write.
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
        if not outcome["ok"]:
            status = "failed" if outcome.get("conflict") else "denied"
            reason = str(outcome.get("reason") or "refund_rejected")
            trace.add("host_result", {"ok": False, "reason": reason, "conflict": bool(outcome.get("conflict"))})
            return finish(
                conn,
                shape="orchestrator",
                claim_id=claim_id,
                seed=seed,
                status=status,
                proposal_amount=proposal,
                budget=budget,
                trace=trace,
                error_reason=reason,
            )

        trace.add("host_result", {"ok": True, "reason": str(outcome.get("reason") or "accepted")})
        return finish(
            conn,
            shape="orchestrator",
            claim_id=claim_id,
            seed=seed,
            status="resolved",
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=None,
        )
    finally:
        conn.close()
