# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.

- Shape chọn: workflow
- Commit hash: 5bd9052
- Run id dẫn chứng: R-workflow-C-001-s11 (đối chiếu cùng claim/seed: R-orchestrator-C-001-s11)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 (70 trial public)
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0 trial lỗi trên benchmark public

## Vì sao shape này

Trên cùng 14 claim public và năm seed, workflow đạt pass rate 1.000 và pass^5 1.000, bằng single và orchestrator. Workflow có cost/success thấp nhất (27.86 VND mô phỏng, so với 46.43 của orchestrator, 48.19 của single và 49.57 của swarm), mean steps thấp nhất (1.00), đồng thời variance bằng 0. Vì mục tiêu là chọn kiến trúc ít tự chủ nhất mà vẫn làm được việc, workflow là lựa chọn phù hợp với kết quả public hiện có.

## Có đáng đổi lấy multi-agent không

Trên bộ public này, pass rate không tăng khi chuyển từ workflow sang single hoặc orchestrator, trong khi cost và số bước tăng. Vì vậy nhóm chưa thấy lợi ích đủ để trả thêm chi phí cho nhiều agent. Quyết định sẽ được xem lại nếu hidden hoặc dữ liệu thực tế cho thấy workflow không đạt ngưỡng chất lượng, hoặc nếu orchestrator cải thiện đáng kể độ đúng trên các claim mơ hồ mà mức cost tăng vẫn chấp nhận được.

## Trace và bằng chứng

Trace của các shape ghi các sự kiện xử lý cần cho grader, như tra claim/order, quote, handoff/investigation (với orchestrator) và kết quả host. Trace không ghi `parent_secret`, raw headers, ticket nguyên văn, principal ID, số điện thoại, địa chỉ, ghi chú nội bộ hay tên hàng. Benchmark public qua evaluator trên 280 trial; crash suite đạt 20/20. `student_drop/` không có trong workspace nên kết quả hidden chưa được tự kiểm.

## Giới hạn

MockLLM không phải model sản xuất. Chi phí là mô phỏng và latency là `unavailable`. Kết luận hiện dựa trên 14 claim public, chưa bao gồm nhãn hidden chính thức; không sửa JSON cho đủ ngưỡng.
