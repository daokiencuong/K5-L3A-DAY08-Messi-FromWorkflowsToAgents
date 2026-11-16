# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Nhóm chọn R3 và dùng benchmark public như một so sánh topology có kiểm soát.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |

## Phiếu của nhóm

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R3 — Architecture choices |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng | Bogavelli, Subramani & Sharma (2026), *AgentArch: A Benchmark for Evaluating Agent Architectures in Enterprise Workflows*, AACL-IJCNLP 2026, https://aclanthology.org/2026.aacl-long.44/ — benchmark nghiên cứu, đánh giá 18 cấu hình agent trên hai use case doanh nghiệp. |
| CLAIM | Một kết luận gốc của nguồn | Nghiên cứu báo cáo sở thích kiến trúc thay đổi theo model và use case; không có một cấu hình tốt nhất cho mọi thiết lập. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Kết quả của paper thuộc hai use case doanh nghiệp và các model/cấu hình được benchmark trong paper; không tự động khái quát sang LogiX-VN, MockLLM hay dữ liệu sản xuất của nhóm. |
| HYPOTHESIS | Nếu đổi shape A→B, metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Workflow → orchestrator trên cùng claim/seed/corpus: dự đoán pass rate giữ gần như nhau (chênh lệch ≤ 0.05), còn cost/success và mean steps tăng ít nhất 25% do handoff và investigator bổ sung. |
| METHOD | Biến giữ cố định; biến duy nhất được thay đổi | Giữ nguyên 14 claim public, seed `11,22,33,44,55`, as_of, MockLLM backend, host, evaluator và bảng giá; chỉ đổi shape workflow ↔ orchestrator. Ghi nhận số tool/model call phát sinh như chi phí của topology. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo | Dự kiến orchestrator tốn thêm bước/tool mà không tăng độ đúng trên claim tuần tự; đo pass rate, pass^5, mean/p95 steps và cost/success. Đồng thời evaluator kiểm tra approval, ledger và trace. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `py -3 -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `R-workflow-C-001-s11` và `R-orchestrator-C-001-s11`; `src/reports/benchmark.json`.
- Kết quả so với hypothesis: phù hợp. Workflow và orchestrator cùng đạt pass rate/pass^5 `1.000/1.000`, seed variance `0.000000`. Cost/success tăng từ `27.86` lên `46.43` VND mô phỏng (+66.7%); mean steps tăng từ `1.00` lên `4.71` (+371%).
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`; benchmark chỉ có 14 claim public, nên kết luận không thay cho hidden grader hoặc dữ liệu sản xuất.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
