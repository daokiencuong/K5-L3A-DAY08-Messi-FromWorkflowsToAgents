# Báo cáo cá nhân — Đào Kiên Cường

## 1. Thông tin thành viên

- Họ tên: Đào Kiên Cường
- MSSV: 2A202603396
- Email: 26ai.cuongdk@vinuni.edu.vn
- GitHub: daokiencuong

## 2. Phần việc phụ trách

Phụ trách shape orchestrator, hỗ trợ handoff/investigator và phối hợp hoàn thiện báo cáo nhóm.

## 3. Đóng góp cụ thể

- Triển khai `run_claim` cho shape orchestrator: tạo handoff theo allowlist, gọi investigator chỉ đọc, nhận quote từ tool/code và gọi host để kiểm tra approval, trần hoàn tiền, idempotency và ghi ledger.
- Commit triển khai shape: `5c4ca67`.
- Chưa có test riêng do cá nhân thêm hoặc sửa trong commit; đã chạy ma trận student sau khi nhóm tích hợp, trong đó shape orchestrator đạt 62 test.
- Cùng nhóm tổng hợp benchmark public, crash safety và nghiên cứu architecture choices vào các báo cáo nhóm.

## 4. Bằng chứng

- Commit: `5c4ca67`.
- Test đã chạy: `py -3 -m pytest -q -m student -o addopts=` — `248 passed, 54 deselected` tổng thể.
- Benchmark: `src/reports/benchmark.json`; run id ví dụ `R-orchestrator-C-001-s11`.
- Crash suite: `src/reports/crash.json`, `20/20`.

## 5. Công cụ AI đã dùng

Đã dùng ChatGPT để giải thích contract, seed/MockLLM, rà soát luồng orchestrator và hỗ trợ cấu trúc báo cáo. Tự kiểm tra bằng cách chạy test suite, ma trận student, crash suite và đối chiếu số liệu trong JSON do benchmark sinh ra.

## 6. Tự đánh giá

Đã triển khai orchestrator theo ranh giới code/host, dùng handoff giới hạn field và giữ investigator chỉ đọc. Việc cần hoàn thiện tiếp là thêm hoặc sửa test có commit để đáp ứng yêu cầu đóng góp cá nhân của lab, đồng thời kiểm tra hidden chính thức khi được phát `student_drop/` hoặc grader.
