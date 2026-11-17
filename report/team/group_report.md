# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Tên nhóm: Messi; lớp: L3A.
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md).
- Commit nguồn đã dùng cho lượt kiểm chứng này: `11c3698`.
- Ngày chạy lại: 17-11-2026 (GMT+7), Python 3.12.10 trên Windows AMD64.

## 2. Mục tiêu và cách tiếp cận

Nhóm triển khai cùng quy trình xử lý claim hoàn phí qua workflow, single agent, orchestrator và swarm tham chiếu. Các shape dùng cùng bộ claim public, năm seed `11, 22, 33, 44, 55`, cấu hình giá và evaluator. Code/host quyết định policy, số tiền, approval, idempotency và ghi ledger; model không quyết định tiền và không trực tiếp ghi refund.

## 3. Phân công và giải pháp

- **Đào Kiên Cường — orchestrator:** tạo handoff qua allowlist, chạy investigator chỉ đọc, nhận dữ kiện/quote rồi gọi host. Không chuyển ticket hoặc parent context nhạy cảm cho investigator.
- **Nguyễn Thị Dung — workflow:** đọc claim và order theo các bước Python cố định, tính quote bằng `compute_compensation`, sau đó gọi host với quote đầy đủ.
- **Vũ Xuân Trường — single agent:** triển khai ReAct tối đa 8 bước, chỉ dùng tool đọc trong vòng lặp; sau đó code gọi host để xác thực và ghi refund.
- **Swarm:** shape tham chiếu để so sánh cost và variance.

Trong cả ba shape của nhóm, `durability.issue_refund` là điểm ghi duy nhất. Host áp dụng approval, trần theo đơn và idempotency. Trace tránh `parent_secret`, raw headers, ticket nguyên văn, principal ID, số điện thoại, địa chỉ, ghi chú nội bộ và tên hàng.

## 4. Kết quả kiểm chứng

### Test và checker

- Smoke: `py -3.12 -m lab8.smoke` — pass, Python 3.12.10.
- Host suite: `py -3.12 -m pytest -q` — `55 passed, 248 deselected`, gồm regression test orchestrator mới.
- Ma trận student: `py -3.12 -m pytest -q -m student -o addopts=` — `248 passed, 55 deselected` (62 test áp dụng cho mỗi shape). Output: [test_results_student_matrix.txt](test_results_student_matrix.txt).
- Checker: `py -3.12 -m lab8.check_submission` — `0 FAIL, 1 WARN`. Cảnh báo duy nhất là workspace còn thay đổi chưa commit; checker in HEAD `26e4a53`.
- Crash suite: `py -3.12 -m lab8.crash_test --count 20 --out reports/crash.json` — `20/20`.

### Benchmark public

Chạy lại 14 claim × 5 seed, tổng 70 trial mỗi shape. Kết quả được ghi trong `src/reports/benchmark.json`.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND mô phỏng) | Mean / p95 steps |
|---|---:|---:|---:|---:|---:|---:|
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 1.00 / 1 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 48.19 | 2.64 / 3 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 46.43 | 4.71 / 5 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 |

Workflow, single và orchestrator đạt toàn bộ 70 trial public. Swarm có một trial sai nhãn ở seed 55, đúng với điểm yếu được thiết kế trong shape tham chiếu. Không có trial public bị báo lỗi approval hoặc trace leak.

### Hidden self-check

Nhóm chạy lệnh self-check trên `src/student_drop/hidden_claims.jsonl` và `hidden_world_state.json`. Mỗi shape nhóm chạy 200 trial (40 claim × 5 seed). Workflow, single và orchestrator đều có `0` trial lỗi và `0` leak suspect. Các trạng thái trong ba shape khớp số lượng: 95 denied, 90 resolved, 5 needs_info, 10 escalated. Kết quả ở `src/reports/hidden_selfcheck.json`.

Hidden self-check không có nhãn, nên `passed` là chưa xác định và không thể tính pass rate, pass^5 hay approval bypass chính thức. Chỉ grader riêng của giảng viên mới xác định các điểm đó; nhóm không suy diễn điểm hidden từ trạng thái chạy thành công.

## 5. Quyết định kiến trúc

Nhóm chọn **workflow**. Trên corpus public, workflow ngang pass rate với single và orchestrator, có cost/success thấp nhất (`27.86` VND mô phỏng), mean steps thấp nhất (`1.00`) và variance bằng `0`. Kết quả này phù hợp với mục tiêu chọn shape ít tự chủ nhất mà vẫn xử lý đúng các claim đã kiểm tra. Chưa có bằng chứng public cho thấy thêm agent cải thiện độ đúng.

## 6. Khó khăn và cách xử lý

Lệnh `py -3` ban đầu trỏ tới Python 3.11 không còn tồn tại; Python 3.12 trong WindowsApps bị sandbox chặn. Sau khi được cấp quyền chạy Python ngoài sandbox, nhóm dùng `py -3.12` và xác nhận phiên bản `3.12.10`. Smoke, hai test suite, crash suite, benchmark, hidden self-check và checker đều chạy được.

## 7. Đóng góp và việc còn phải chốt

Ba commit triển khai shape lần lượt là `5c4ca67` (Cường), `4458db6` (Dung) và `5bd9052` (Trường). Nhóm bổ sung `src/tests/test_orchestrator_handoff_regression.py` cho handoff của orchestrator; test này pass. Ma trận student chạy lại đạt `248 passed, 55 deselected`, gồm 62 ca cho mỗi shape; output được đính kèm tại [test_results_student_matrix.txt](test_results_student_matrix.txt). Các test liên quan được liệt kê trong bảng [TEAM.md](../../TEAM.md) và từng báo cáo cá nhân.

## 8. Hạn chế

Benchmark public chỉ có 14 claim, MockLLM là mô phỏng xác định, cost là giá mô phỏng và latency là `unavailable`. Hidden self-check không có nhãn và không thay thế grader chính thức. Không thể kết luận pass rate hidden hay khẳng định mô hình sẽ cho kết quả tương tự trong môi trường sản xuất.

## 9. Tài liệu tham khảo

- `README.md`, `CHECKPOINTS.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`, `docs/architecture.md`.
- Bogavelli, Subramani, Sharma (2026), *AgentArch: A Benchmark for Evaluating Agent Architectures in Enterprise Workflows*, AACL-IJCNLP 2026, https://aclanthology.org/2026.aacl-long.44/.
