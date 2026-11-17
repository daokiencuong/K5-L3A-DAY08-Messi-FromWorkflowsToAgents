# Báo cáo cá nhân — Nguyễn Thị Dung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thị Dung
- MSSV: 2A202603508
- Email: dungthngn@gmail.com
- GitHub: [zoesayhii](https://github.com/zoesayhii)

## 2. Phần việc phụ trách

Phụ trách shape `workflow` trong `src/lab8/shapes/workflow.py`. Workflow thực hiện các bước xử lý claim tuần tự bằng Python, không giao quyền quyết định số tiền cho model.

## 3. Đóng góp cụ thể

- Đọc claim qua `get_claim_view` và kiểm tra quyền xem order bằng `lookup_order`.
- Tính quote từ order bằng `compute_compensation`, không dựa vào số ngày hoặc yêu cầu hoàn tiền trong nội dung ticket.
- Truyền quote đầy đủ vào `durability.issue_refund`; để host áp dụng approval, trần theo đơn, idempotency và ghi ledger.
- Xử lý các trạng thái `needs_info`, `escalated`, `denied`, `failed` và `resolved`, đồng thời ghi trace theo contract.
- Commit triển khai workflow: [`4458db6`](https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents/commit/4458db6336ed83263649291ea277a91c532b46a6).

## 4. Bằng chứng và kiểm thử

- File triển khai: `src/lab8/shapes/workflow.py`.
- Đã chạy lại ma trận student: `py -3.12 -m pytest -q -m student -o addopts=` — `248 passed, 54 deselected`; 62 test áp dụng cho workflow đều pass.
- Đã chạy lại host suite: `py -3.12 -m pytest -q` — `54 passed, 248 deselected`.
- Public benchmark: 70/70 trial pass; pass^5 `1.000`; cost/success `27.86` VND mô phỏng; run ID mẫu `R-workflow-C-001-s11`.
- Hidden self-check: 200 trial chạy hết, `0` lỗi và `0` leak suspect. Không có nhãn nên đây không phải điểm hidden.
- Crash suite: `20/20` toàn suite.

Test liên quan: `src/tests/test_public_matrix.py`, `test_crash_suite.py`, `test_authorization.py` và `test_order_cap_and_approval_binding.py`. Output ma trận student: [`test_results_student_matrix.txt`](test_results_student_matrix.txt) — `248 passed, 54 deselected` tổng thể; 62 ca áp dụng cho workflow đều pass.

## 5. Công cụ AI đã dùng

Đã sử dụng GitHub Copilot/Copilot SDK để giải thích yêu cầu, gợi ý cấu trúc workflow và rà soát logic. Kết quả được tự kiểm bằng cách đối chiếu business rules, contract và chạy test suite; không dựa vào AI để tạo số liệu benchmark.

## 6. Tự đánh giá

Workflow giữ ranh giới rõ giữa code và model: code tính entitlement, còn host xác thực và ghi refund. Ma trận student, authorization, order cap và crash suite kiểm tra các nhánh chính của workflow, bao gồm approval, retry và crash.
