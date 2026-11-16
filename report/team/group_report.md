# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Tên nhóm: Messi
- Lớp: L3A
- Thành viên: xem `TEAM.md`.
- Commit code được benchmark: `5bd9052`.

## 2. Mục tiêu và cách tiếp cận

Nhóm triển khai cùng quy trình xử lý claim hoàn phí qua workflow, single agent, orchestrator và swarm tham chiếu. Cả bốn shape dùng cùng bộ claim public, năm seed `11, 22, 33, 44, 55`, cấu hình giá và evaluator. Nhóm giữ quyết định về policy, số tiền, approval, idempotency và ghi ledger ở code/host; model chỉ hỗ trợ luồng suy luận hoặc tạo nội dung giả lập. Sau khi hoàn thiện ba shape, nhóm chạy cổng host, ma trận student, crash suite và benchmark trước khi chọn kiến trúc dựa trên số liệu.

## 3. Giải pháp

- **Workflow:** đọc claim qua `get_claim_view`, kiểm tra order bằng `lookup_order`, tính quote bằng `compute_compensation`, rồi giao host kiểm duyệt và ghi refund. Các bước được cố định trong Python.
- **Single:** chạy vòng ReAct tối đa 8 bước. Agent chỉ chọn tool đọc; sau khi có quote, shape gọi host để kiểm tra approval và ghi refund.
- **Orchestrator:** tạo handoff qua allowlist, không chuyển ticket hoặc parent context nhạy cảm; investigator chỉ có các tool đọc order, policy và tính compensation. Orchestrator nhận kết quả đã giới hạn rồi gọi host ghi refund.
- **Swarm:** shape tham chiếu dùng làm đối chứng về cost và variance.

Trong cả ba shape, số tiền được tính bằng code; `durability.issue_refund` là điểm ghi duy nhất. Quote đầy đủ được chuyển cho host để host áp dụng approval, trần theo đơn và idempotency. Trace ghi trạng thái và dữ kiện cần thiết; không ghi `parent_secret`, raw headers, ticket nguyên văn, số điện thoại, địa chỉ, ghi chú nội bộ hay tên hàng.

## 4. Kết quả

Benchmark public gồm 14 claim × 5 seed = 70 trial cho mỗi shape. Số liệu lấy từ `src/reports/benchmark.json`.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND mô phỏng) | Mean / p95 steps |
|---|---:|---:|---:|---:|---:|---:|
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 1.00 / 1 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 48.19 | 2.64 / 3 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 46.43 | 4.71 / 5 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 |

Crash suite đạt `20/20` (`src/reports/crash.json`). Trên benchmark public, cả workflow, single và orchestrator đạt toàn bộ trial; swarm có một trial sai nhãn ở seed 55 như điểm yếu cố ý của starter. Mỗi trial public đều qua evaluator, trong đó có kiểm tra approval và trace; không có trial public nào bị báo lỗi. Bộ `student_drop/` không có trong workspace nên nhóm chưa chạy tự kiểm hidden. Hidden chính thức vẫn cần grader của giảng viên.

Nhóm đề xuất chọn **workflow**: trên benchmark public, workflow ngang pass rate với single và orchestrator, không có variance giữa seed, nhưng cost/success thấp nhất và số bước trung bình thấp nhất. Đây cũng là kiến trúc ít tự chủ nhất trong bốn shape mà vẫn xử lý đúng các claim public. Kết luận cần xem lại nếu hidden hoặc dữ liệu sản xuất cho thấy workflow không đạt ngưỡng chất lượng.

## 5. Khó khăn và cách xử lý

PowerShell không nhận lệnh `python`, còn môi trường `.venv` có interpreter Python 3.11 cũ không tồn tại. Nhóm dùng Python 3.12 qua `py -3` và cài các dependency trong `src/requirements.txt`. Sau đó `py -3 -m pytest -q` đạt `54 passed, 248 deselected`; `py -3 -m pytest -q -m student -o addopts=` đạt `248 passed, 54 deselected`.

## 6. Tổng hợp đóng góp

Danh sách thành viên, vai trò, commit và bằng chứng test được ghi trong bảng đóng góp của `TEAM.md`. Cần bảo đảm mỗi thành viên có ít nhất một commit kỹ thuật và một test được thêm hoặc sửa theo checklist nộp bài.

## 7. Hạn chế và hướng cải thiện

Benchmark public chỉ có 14 claim và MockLLM là mô phỏng xác định, không đại diện đầy đủ cho model sản xuất. Chi phí là giá mô phỏng, không phải hóa đơn API; latency là `unavailable`. Nhóm chưa có `student_drop/` để tự kiểm hidden, nên chưa thể khẳng định điểm hidden từ benchmark public. Có thể đổi quyết định nếu hidden có nhiều ticket mơ hồ mà cần khả năng thích ứng, hoặc nếu chi phí/độ trễ của orchestrator giảm mà vẫn giữ độ đúng.

## 8. Tài liệu tham khảo

- `README.md`, `CHECKPOINTS.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`, `docs/architecture.md`.
- Bogavelli, Subramani, Sharma (2026), *AgentArch: A Benchmark for Evaluating Agent Architectures in Enterprise Workflows*, AACL-IJCNLP 2026, https://aclanthology.org/2026.aacl-long.44/.
