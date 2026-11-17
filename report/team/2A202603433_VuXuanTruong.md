# Báo cáo cá nhân — Vũ Xuân Trường

## 1. Thông tin thành viên

- Họ tên: Vũ Xuân Trường
- MSSV: 2A202603433
- Email theo metadata commit: vuxuantruong170204@gmail.com
- GitHub: [TruongXuan-Vu](https://github.com/TruongXuan-Vu)
- Tên tác giả trong metadata commit shape: `TruongVu`

## 2. Phần việc phụ trách

Phụ trách shape `single` trong `src/lab8/shapes/single.py`: triển khai vòng ReAct có giới hạn bước, dùng tool đọc để thu thập dữ kiện/quote, rồi để code gọi host xử lý refund.

## 3. Đóng góp cụ thể

- Triển khai `run_claim` và vòng lặp ReAct tối đa 8 bước.
- Agent chỉ chọn tool đọc; không được gọi `issue_refund` hoặc tự quyết định tiền.
- Sau khi có quote, code chuyển quote đầy đủ cho `durability.issue_refund` để host xác thực approval, trần theo đơn, idempotency và ghi ledger.
- Xử lý các trạng thái kết thúc và ghi trace theo contract.
- Commit triển khai: [`5bd9052`](https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents/commit/5bd9052ac65231c818e1a9793ae68793c06fb516).

## 4. Bằng chứng và kiểm thử

- File triển khai: `src/lab8/shapes/single.py`.
- Đã chạy lại ma trận student: `py -3.12 -m pytest -q -m student -o addopts=` — `248 passed, 54 deselected`; 62 test áp dụng cho single đều pass.
- Đã chạy lại host suite: `py -3.12 -m pytest -q` — `54 passed, 248 deselected`.
- Public benchmark: 70/70 trial pass; pass^5 `1.000`; cost/success `48.19` VND mô phỏng; run ID mẫu `R-single-C-001-s11`.
- Hidden self-check: 200 trial chạy hết, `0` lỗi và `0` leak suspect. Do hidden không có nhãn, kết quả không cho biết pass rate hay approval bypass chính thức.
- Crash suite: `20/20` toàn suite.

Test liên quan: `src/tests/test_public_matrix.py`, `test_authorization.py`, `test_refund_idempotency.py` và `test_crash_suite.py`. Output ma trận student: [`test_results_student_matrix.txt`](test_results_student_matrix.txt) — `248 passed, 54 deselected` tổng thể; 62 ca áp dụng cho single đều pass.

## 5. Công cụ AI đã dùng

Bản báo cáo này được ChatGPT hỗ trợ biên tập theo thông tin trong repo và kết quả kiểm thử vừa chạy. Repo chưa ghi công cụ AI mà Trường đã dùng khi triển khai shape; Trường cần xác nhận công cụ/mục đích và cách tự kiểm trước khi nộp để đáp ứng RULES.md.

## 6. Tự đánh giá

Shape single giữ quyền chọn tool đọc trong vòng ReAct và giữ quyết định ghi tiền ở code/host. Trường cần đọc lại phần mô tả để xác nhận đúng với quá trình triển khai và bổ sung thông tin về công cụ AI đã dùng khi làm shape.
