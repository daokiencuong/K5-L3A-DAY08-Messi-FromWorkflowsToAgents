# Báo cáo cá nhân — Đào Kiên Cường

## 1. Thông tin thành viên

- Họ tên: Đào Kiên Cường
- MSSV: 2A202603396
- Email: 26ai.cuongdk@vinuni.edu.vn
- GitHub: [daokiencuong](https://github.com/daokiencuong)

## 2. Phần việc phụ trách

Phụ trách shape `orchestrator`, hỗ trợ handoff/investigator và phối hợp tích hợp báo cáo nhóm.

## 3. Đóng góp cụ thể

- Triển khai `run_claim` cho orchestrator: tạo handoff bằng `make_handoff` theo allowlist, gọi investigator chỉ đọc, dùng kết quả đã giới hạn để tính quote và gọi host.
- Giữ `parent_secret`, raw headers và dữ liệu claim nhạy cảm ngoài handoff/trace; không cấp tool ghi cho investigator.
- Để `durability.issue_refund` kiểm approval, trần theo đơn, idempotency và ghi ledger.
- Commit triển khai: [`5c4ca67`](https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents/commit/5c4ca6726fff300abee4ac3b4f547daebd29f211).
- Phối hợp tổng hợp số liệu benchmark, crash và hidden self-check vào báo cáo nhóm.

## 4. Bằng chứng và kiểm thử

- File triển khai: `src/lab8/shapes/orchestrator.py`.
- Test mới: `src/tests/test_orchestrator_handoff_regression.py` — `1 passed`.
- Đã chạy lại ma trận student: `py -3.12 -m pytest -q -m student -o addopts=` — `248 passed, 55 deselected`; 62 test áp dụng cho orchestrator đều pass.
- Đã chạy lại host suite: `py -3.12 -m pytest -q` — `55 passed, 248 deselected`.
- Public benchmark: 70/70 trial pass; pass^5 `1.000`; cost/success `46.43` VND mô phỏng; run ID mẫu `R-orchestrator-C-001-s11`.
- Hidden self-check: 200 trial chạy hết, `0` lỗi và `0` leak suspect. Không có nhãn nên không suy ra điểm hidden.
- Crash suite: `20/20` toàn suite.

Test liên quan: `src/tests/test_orchestrator_handoff_regression.py`, `src/tests/test_public_matrix.py`, `test_handoff_secret.py`, `test_trace_contract.py` và `test_crash_suite.py`. Output ma trận student: [`test_results_student_matrix.txt`](test_results_student_matrix.txt) — `248 passed, 55 deselected` tổng thể; 62 ca áp dụng cho orchestrator đều pass.

## 5. Công cụ AI đã dùng

Đã dùng ChatGPT để giải thích contract, seed/MockLLM, rà soát luồng orchestrator và hỗ trợ biên tập báo cáo. Tự kiểm bằng cách đọc code/contract và chạy lại smoke, test suite, ma trận student, crash suite, benchmark, hidden self-check và checker.

## 6. Tự đánh giá

Orchestrator dùng handoff giới hạn field và investigator chỉ đọc, còn host giữ quyền quyết định refund. Kết quả student matrix và crash suite cung cấp bằng chứng hồi quy cho luồng xử lý, bảo mật handoff và retry.
