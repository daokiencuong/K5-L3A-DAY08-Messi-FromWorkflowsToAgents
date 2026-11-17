import pytest

from lab8.db import connect
from lab8.shapes.workflow import run_claim


@pytest.mark.student
def test_workflow_missing_order_does_not_write_ledger(public_db):
    result = run_claim(
        "C-004",
        seed=11,
        store_path=str(public_db),
    )

    assert result.status == "needs_info"
    assert result.proposal_amount == 0
    assert result.trace_path

    conn = connect(public_db)
    try:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-004'"
        ).fetchone()["n"]
    finally:
        conn.close()

    assert count == 0
