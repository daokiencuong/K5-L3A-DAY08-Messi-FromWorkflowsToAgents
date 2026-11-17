# Báo cáo cá nhân — Vũ Xuân Trường

## 1. Thông tin thành viên

- Họ tên: Vũ Xuân Trường
- MSSV: 2A202603433
- Email: 26ai.truongvx@vinuni.edu.vn
- GitHub: TruongXuan-Vu

## 2. Phần việc phụ trách

Phụ trách shape single agent (shape B): một ReAct agent dùng `lab8.runtime.run_react` với `max_steps=8`, `decide` chỉ chọn read tool, host là nơi duy nhất ghi refund. Hỗ trợ so sánh với swarm reference và đảm bảo tuân thủ trace contract v1.

## 3. Đóng góp cụ thể

- Triển khai `run_claim` cho shape single: đọc claim qua `get_claim_view`, `lookup_order`, `lookup_refund_history`, `compute_compensation` trong vòng ReAct; quote lấy từ order row, không tin số ngày trong ticket; truyền full quote vào `durability.issue_refund`; forward `crash_at` và không bắt `InjectedCrash`.
- Commit triển khai shape: `5bd9052`.
- Chưa có test riêng do cá nhân thêm hoặc sửa trong commit; đã chạy ma trận student sau khi nhóm tích hợp, trong đó shape single đạt 62 test.
- Cùng nhóm tổng hợp benchmark public, crash safety và nghiên cứu architecture choices vào các báo cáo nhóm.

## 4. Bằng chứng

- Commit: `5bd9052`.
- Test đã chạy: `py -3 -m pytest -q -m student -o addopts=` — `248 passed, 54 deselected` tổng thể.
- Benchmark: `src/reports/benchmark.json`; run id ví dụ `R-single-C-001-s11`.
- Crash suite: `src/reports/crash.json`, `20/20`.

## 5. Công cụ AI đã dùng

Đã dùng ZCode để giải thích contract, rà soát luồng ReAct, và hỗ trợ triển khai shape single. Tự kiểm tra bằng cách chạy test suite, ma trận student, crash suite và đối chiếu số liệu trong JSON do benchmark sinh ra.

## 6. Tự đánh giá

Đã triển khai single agent theo ranh giới code/host, dùng ReAct giới hạn bước và giữ investigator chỉ đọc. Việc cần hoàn thiện tiếp là thêm hoặc sửa test có commit để đáp ứng yêu cầu đóng góp cá nhân của lab, đồng thời kiểm tra hidden chính thức khi được phát `student_drop/` hoặc grader.
