# Team

## Thông tin nhóm

* Tên nhóm: Messi
* Lớp: L3A
* Repo nhóm: `K5-L3A-DAY08-Messi-FromWorkflowsToAgents`
* URL repo: <https://github.com/daokiencuong/K5-L3A-DAY08-Messi-FromWorkflowsToAgents>
* Nhánh nộp: `main`
* Commit nguồn dùng để chạy lại benchmark: `11c3698`

## Thành viên và phân công

| STT | Họ tên          | MSSV        | Email                          | GitHub                                            | Vai trò                            |
| --: | --------------- | ----------- | ------------------------------ | ------------------------------------------------- | ---------------------------------- |
|   1 | Đào Kiên Cường  | 2A202603396 | <26ai.cuongdk@vinuni.edu.vn>   | [daokiencuong](https://github.com/daokiencuong)   | Nhóm trưởng, orchestrator, báo cáo |
|   2 | Nguyễn Thị Dung | 2A202603508 | <dungthngn@gmail.com>          | [zoesayhii](https://github.com/zoesayhii)         | Workflow                           |
|   3 | Vũ Xuân Trường  | 2A202603433 | <vuxuantruong170204@gmail.com> | [TruongXuan-Vu](https://github.com/TruongXuan-Vu) | Single agent                       |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Cột cuối liệt kê test liên quan và output của ma trận student đã chạy lại.

| Người           | Vai                    | Commit    | Test đã thêm hoặc sửa                                                                                            |
| --------------- | ---------------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| Đào Kiên Cường  | Orchestrator + báo cáo | `5c4ca67` | `src/tests/test_orchestrator_handoff_regression.py`, `src/tests/test_public_matrix.py`; targeted test 1 passed; output: [student matrix log](report/team/test_results_student_matrix.txt) — 248 passed. |
| Nguyễn Thị Dung | Workflow               | `4458db6` | `src/tests/test_public_matrix.py`, `test_authorization.py`, `test_order_cap_and_approval_binding.py`; output: [student matrix log](report/team/test_results_student_matrix.txt) — 248 passed. |
| Vũ Xuân Trường  | Single agent           | `5bd9052` | `src/tests/test_public_matrix.py`, `test_refund_idempotency.py`; output: [student matrix log](report/team/test_results_student_matrix.txt) — 248 passed. |

Ma trận được chạy lại bằng `py -3.12 -m pytest -q -m student -o addopts=`: `248 passed, 55 deselected`. Tổng số gồm 62 ca cho mỗi shape; output console được đính kèm tại `report/team/test_results_student_matrix.txt`.

## Báo cáo cá nhân

* [Đào Kiên Cường — orchestrator](report/team/2A202603396_DaoKienCuong.md)
* [Nguyễn Thị Dung — workflow](report/team/2A202603508_NguyenThiDung.md)
* [Vũ Xuân Trường — single agent](report/team/2A202603433_VuXuanTruong.md)

