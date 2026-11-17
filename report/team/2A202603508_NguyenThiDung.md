# Báo cáo cá nhân — 2A202603508_NguyenThiDung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thị Dung
- MSSV: 2A202603508
- Email: dungthngn@gmail.com
- GitHub: [@zoesayhii](https://github.com/zoesayhii)

## 2. Phần việc phụ trách

Phụ trách triển khai shape `workflow` trong `src/lab8/shapes/workflow.py`.

Workflow thực hiện các bước cố định bằng code: đọc claim, kiểm tra order, tính compensation bằng `compute_compensation`, gọi `issue_refund`, xử lý các trạng thái `needs_info`, `escalated`, `denied`, `failed` và `resolved`, đồng thời ghi trace theo contract.

...

## 3. Đóng góp cụ thể

Commit chính (hash), test đã thêm hoặc sửa, quyết định kỹ thuật bạn đưa ra.


- Triển khai logic xử lý claim cho shape `workflow`.
- Đảm bảo số tiền hoàn được tính bởi code, không do model quyết định.
- Truyền đầy đủ quote vào `issue_refund`.
- Xử lý idempotency, crash injection và các nhánh lỗi theo yêu cầu của bài.
- Commit được thực hiện bằng tài khoản GitHub `zoeng`.
- Commit chính: `https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents/commit/4458db6336ed83263649291ea277a91c532b46a6`.
- Test đã chạy: `python -m pytest -q -m student -o addopts= -k workflow`.

...

## 4. Bằng chứng

- File triển khai: `src/lab8/shapes/workflow.py`
- Test liên quan: `src/tests/test_public_matrix.py`
- Các test kiểm tra thêm về cap, approval và idempotency: `src/tests/test_order_cap_and_approval_binding.py`
- Link commit: `https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents/commit/4458db6336ed83263649291ea277a91c532b46a6`

...

## 5. Công cụ AI đã dùng

Công cụ, dùng vào việc gì, và bạn đã tự kiểm tra kết quả thế nào (xem [RULES.md](../../RULES.md)).

Có sử dụng GitHub Copilot/Copilot SDK để giải thích yêu cầu, gợi ý cấu trúc xử lý workflow và rà soát logic.

Kết quả được tự kiểm tra bằng cách đọc lại code, đối chiếu với `RULES.md`, docstring của `workflow.py`, sau đó chạy các test workflow và kiểm tra các nhánh xử lý lỗi.


...

## 6. Tự đánh giá

Hoàn thành phần việc được phân công. Tôi hiểu được ranh giới giữa code quyết định số tiền hoàn và model chỉ hỗ trợ tạo phản hồi, cũng như vai trò của ledger và cơ chế idempotency trong việc tránh hoàn tiền trùng.

Hạn chế là chưa có nhiều kinh nghiệm với xử lý crash giữa các bước ghi dữ liệu. Hướng cải thiện là bổ sung thêm test cho các tình huống cạnh tranh, retry và lỗi giao dịch.
...
