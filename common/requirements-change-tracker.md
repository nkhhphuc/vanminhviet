# Sổ Theo Dõi Thay Đổi (CR/DC)

> Chứa các dòng CR (thay đổi đặc tả) và DC (thay đổi chỉ ở tài liệu thiết kế) đang mở. Quy trình: xem `common/requirements-design-sync.md`. File này không xoá khi đồng bộ sang Code. Trạng thái xử lý ở Code nằm ở `planning/cr-status.md` trong repo `vanminhviet` (mục 4.1 của quy trình).

## Mốc đồng bộ

| Luồng | Đã đồng bộ đến |
|---|---|
| system-design | DC-20260929-04 |
| admin-web | DC-20260929-04 |
| partner-web | DC-20260929-04 |
| public-web | DC-20260929-04 |

## ID lớn nhất đã cấp

| Mã | ID lớn nhất đã cấp |
|---|---|
| GEN | R-GEN-016 |
| ID | R-ID-039 |
| KB | R-KB-094 |
| ENC | R-ENC-043 |
| AI | R-AI-014 |
| OOS | R-OOS-009 |
| PUB | R-PUB-012 |
| PTN | R-PTN-011 |
| CFG | R-CFG-011 |
| NFR | R-NFR-025 |

## ID thiết kế lớn nhất đã cấp

| Mã | ID lớn nhất đã cấp |
|---|---|
| SD01 | D-SD01-008 |
| SD02 | D-SD02-010 |
| SD03 | D-SD03-026 |
| SD04 | D-SD04-018 |
| SD05 | D-SD05-013 |
| SD06 | D-SD06-013 |
| SD07 | D-SD07-014 |
| ADM | D-ADM-029 |
| PRT | D-PRT-013 |
| PUB | D-PUB-012 |

## Danh sách thay đổi

| Mã | Ngày | Tóm tắt | ID ảnh hưởng | system-design | admin-web | partner-web | public-web |
|---|---|---|---|---|---|---|---|
| DC-20260929-01 | 2026-09-29 | Gắn ID `D-SD0X-NNN` cho các mục thiết kế của system-design 01–07 (102 ID). Đổi trích dẫn mục thiết kế sang dạng `D-… (¶…)` / `` `0X` ¶N `` / `¶N` theo `requirements-design-sync.md` mục 2.4, kể cả ở `00-claude-instructions.md` và `index.md`. Sửa 1 trích dẫn đặc tả thiếu ID (`01` ¶8 → R-NFR-009 (§3.2)). Không đổi nội dung cần hiện thực, không đánh số lại mục. | — | ✅ `01`: 1–9 · `02`: đầu tài liệu, 2, 3.0–3.5, 4, 5.1, 5.2, 6 · `03`: đầu tài liệu, 1, 2.1–2.9, 3.1–3.6, 4.1–4.5, 5, 5.1–5.6, 6 · `04`: đầu tài liệu, 1, 2.1–2.6, 3.1–3.4, 4.1–4.4, 5, 5.1–5.4, 6 · `05`: đầu tài liệu, 1, 2.1–2.3, 3.1–3.3, 4.1–4.5, 5.1, 5.2, 6 · `06`: đầu tài liệu, 1, 2, 3.1–3.7, 4–8 · `07`: 1, 2.1–2.3, 3.1–3.3, 4.1–4.5, 5.1–5.3, 6 | ✅ 3, 4.1, 4.2, 4.5, 4.6, 4.8, 4.10–4.16, 4.18, 4.20, 4.21, 4.23, 4.24, 4.26–4.28 · `00-claude-instructions.md`: 1, 3, 6 | ✅ 1, 3, 4.1, 4.2, 4.4, 4.6, 4.7, 4.12 · `00-claude-instructions.md`: 1 | — |
| DC-20260929-02 | 2026-09-29 | Gắn ID `D-ADM-NNN` cho `admin-web-design.md`: ¶3 → D-ADM-029, ¶4.1–¶4.28 → D-ADM-001–D-ADM-028. Đổi trích dẫn mục trong cùng file sang `D-ADM-… (¶…)` / `¶N`, kể cả số màn hình viết trần. Luồng khác đang trích `admin-web ¶4.x` cần thêm ID vào trích dẫn. Không đổi nội dung cần hiện thực, không đánh số lại mục. | — | ✅ `01`: 2, 9 · `02`: 6 · `03`: 5.1, 5.2 · `04`: 6 · `05`: 5.2 | ✅ 1, 2, 3, 4.1–4.28 · `00-claude-instructions.md`: 3, 6 | ✅ 3, 4.11 | — |
| DC-20260929-03 | 2026-09-29 | Gắn ID `D-PRT-NNN` cho `partner-web-design.md`: ¶4.1–¶4.12 → D-PRT-001–D-PRT-012, ¶3 → D-PRT-013. Đổi trích dẫn mục trong cùng file sang `D-PRT-… (¶…)` / `¶N`, kể cả số màn hình viết trần. Luồng khác đang trích `partner-web ¶4.x` cần thêm ID vào trích dẫn. Không đổi nội dung cần hiện thực, không đánh số lại mục. | — | ✅ `02`: 4 · `03`: 4.2, 5.1, 6 | — | ✅ 1, 3, 4.1–4.12, 6, 7 · `00-claude-instructions.md`: 3 | — |
| DC-20260929-04 | 2026-09-29 | Gắn ID `D-PUB-NNN` cho `public-web-layout.md`: ¶4.1–¶4.9 → D-PUB-001–D-PUB-009, ¶3 → D-PUB-010, ¶2.1 → D-PUB-011, ¶2.3 → D-PUB-012. Đổi trích dẫn mục trong cùng file sang `D-PUB-… (¶…)` / `¶N`, kể cả ở `00-claude-instructions.md`. Luồng khác đang trích `public-web ¶2.1`, `public-web ¶4.4` hoặc "`public-web-layout.md` mục 2.1" cần thêm ID vào trích dẫn. Không đổi nội dung cần hiện thực, không đánh số lại mục. | — | — | ✅ 3, 4.23 | ✅ 3 | ✅ 2.1, 2.3, 3, 4.1–4.9 · `00-claude-instructions.md`: 1, 3, 6, 7 |
