# Sổ Theo Dõi Thay Đổi (CR/DC)

> Chứa các dòng CR (thay đổi đặc tả) và DC (thay đổi chỉ ở tài liệu thiết kế) đang mở. Quy trình: xem `common/requirements-design-sync.md`. File này không xoá khi đồng bộ sang Code. Trạng thái xử lý ở Code nằm ở `planning/cr-status.md` trong repo `vanminhviet` (mục 4.1 của quy trình).

## Mốc đồng bộ

| Luồng | Đã đồng bộ đến |
|---|---|
| system-design | DC-20260930-05 |
| admin-web | DC-20260930-07 |
| partner-web | DC-20260930-06 |
| public-web | DC-20260930-02 |

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
| DC-20260929-05 | 2026-09-29 | Job `ingestion.sync_source`: khi trùng với job đang `running`, tạo job nối tiếp payload `{source_id, follows_job_id}` (lấy `id` từ kết quả `InsertTx`, không đọc `river_job`), sự kiện sau gộp vào job nối tiếp; `ByState` gồm `available`, `pending`, `scheduled`, `running`, `retryable`, không gồm `completed`/`cancelled`/`discarded`; khi advisory lock theo `source_id` đang bị giữ, worker hoãn job bằng `JobSnooze` trong `operations.source_sync_debounce_seconds` thay vì bỏ qua. Payload trong bảng loại job thêm dạng `{source_id, follows_job_id}`. | — | ✅ `01`: 1, 4 · `03`: 4.2, 6 · `07`: 2.3 | ✅ 4.26, 4.28 | — | — |
| DC-20260930-01 | 2026-09-30 | admin-web căn theo cơ chế kích hoạt AI Verification theo cấu hình (D-SD07-004 (¶3.1), D-SD03-023 (¶5.3)): nút kích hoạt ở 4.13/4.14 hiện theo `can_trigger_ai_verification` thay cho danh sách role cố định; tách nhãn "Kích hoạt AI Verification" (`cho_xet_duyet`) / "Kích hoạt lại AI Verification"; "Gửi xét duyệt" hiển thị kết quả theo `status` trả về (`dang_xet_duyet_ai` hoặc `cho_xet_duyet`), không mặc định tự chạy AI; 4.14 gọi thêm `GET /knowledge/knowledge-objects/{id}`; Dashboard 4.22 ghi cụm "Chờ & Xác minh AI" là tự động hoặc thủ công theo cấu hình. partner-web cần kiểm tra các màn hình Nghiên cứu/Xét duyệt Hạng mục tri thức tương ứng. | D-ADM-013, D-ADM-014, D-ADM-022 | — | ✅ 4.13, 4.14, 4.22 · `00-claude-instructions.md`: 6 | ✅ 4.7, 4.8, 4.11 | — |
| DC-20260930-02 | 2026-09-30 | Nhật ký hoạt động admin-web căn theo D-SD01-002 (¶2): 4.21 hiển thị và lọc theo `actor_type` (Nhân viên/Hệ thống), lọc theo `entity_type`, lọc theo đối tượng cụ thể (`entity_type` + `entity_id`) qua icon trên dòng hoặc nút "Lịch sử hoạt động" mới ở các màn hình chi tiết (chỉ `quan_tri_he_thong`; 4.28 lọc `entity_type = system_setting`), bộ lọc phản ánh lên URL; nhãn hành động lấy từ Danh mục sự kiện audit của SD01 (mã lạ hiện nguyên mã); popup `detail` trình bày theo quy ước `detail` của SD01. Không đổi API. | D-ADM-029, D-ADM-005, D-ADM-007, D-ADM-009, D-ADM-011, D-ADM-013, D-ADM-014, D-ADM-015, D-ADM-017, D-ADM-018, D-ADM-019, D-ADM-021, D-ADM-028 | — | ✅ 3, 4.5, 4.7, 4.9, 4.11, 4.13–4.15, 4.17–4.19, 4.21, 4.28 · `00-claude-instructions.md`: 6 | — | — |
| DC-20260930-03 | 2026-09-30 | Nguồn dữ liệu cho thông báo "AI Verification đang chạy": chi tiết Hạng mục tri thức (`GET /knowledge/knowledge-objects/{id}`) thêm `ai_verification_running` — `true` khi còn job `verification.run` đang chờ/đang chạy theo định nghĩa job trùng ở D-SD03-012 (¶3.3) bước (3); response `POST …/trigger-ai-verification` thêm `merged_into_running_job` — `true` khi lệnh gộp vào job đang có: không tạo job, không đổi trạng thái, **không ghi audit** (thêm vào danh sách "Không ghi audit" của D-SD01-002 (¶2)). admin-web 4.13 và partner-web 4.7 (nút kích hoạt lại tại `dang_xet_duyet_ai`) cần căn theo 2 field này. | — | ✅ `01`: 2 · `03`: 5.3, 5.4 | ✅ 4.13, 4.14 · `00-claude-instructions.md`: 6 | ✅ 4.7, 4.8 | — |
| DC-20260930-04 | 2026-09-30 | Định danh endpoint API bằng operationId (`common/requirements-design-sync.md` mục 2.5): mỗi endpoint trong system-design có một operationId dạng `<tiền tố path>.<tênCamelCase>` (133 endpoint + `gateway.getHealth`), ghi ở cột `operationId` ngay sau cột Path của bảng endpoint; endpoint mount nhiều nhóm route dùng chung một operationId; operationId bất biến. Trích endpoint theo dạng `` `op` (D-…) ``, kèm ` — METHOD /path` khi cần; không trích chỉ bằng method + path. D-SD01-003 (¶3) thêm quy ước hợp đồng OpenAPI: mỗi nhóm route `admin`/`partner`/`public` một file hợp đồng, operationId theo thiết kế, CI kiểm tra tự động hợp đồng khớp code cả route lẫn schema (cách làm do Code chọn), 3 web app sinh API client từ hợp đồng. Script kiểm tra tham chiếu báo thêm lỗi operationId và lỗi trích endpoint chỉ bằng method + path. admin-web, partner-web cần đổi các trích dẫn endpoint sang operationId. Code cần: thêm operationId theo thiết kế vào `api-contracts/*.yaml` (và OpenAPI của AI Gateway), dựng kiểm tra khớp hợp đồng–code trong CI, trích endpoint bằng operationId trong kế hoạch/code/test. | — | ✅ `01`: 2, 3, 4, 7, 8, 9 · `02`: 3.0, 4, 5.1, 5.2, 6 · `03`: 2.7, 3.6, 4.2, 4.4, 5.1–5.6, 6 · `04`: 2.2, 2.4, 3.2, 3.4, 5.1–5.4, 6 · `05`: 3.2, 4.5, 5.1, 5.2, 6 · `06`: 1, 2, 3.2–3.4, 4–8 · `07`: 2.1, 3.2, 4.3, 5.1–5.3 · `00-claude-instructions.md`: 6 · `index.md`: 2 | ✅ 3, 4.1–4.21, 4.23–4.28 · `00-claude-instructions.md`: 3, 6 | ✅ 3, 4.1–4.10, 4.12, 6 · `00-claude-instructions.md`: 6 | — |
| DC-20260930-05 | 2026-09-30 | Trích endpoint chỉ bằng operationId, không kèm ID mục thiết kế (`common/requirements-design-sync.md` mục 2.5): dạng chuẩn `` `op` ``, kèm ` — METHOD /path` khi cần. Ghi ID mục trần ngay sau operationId là lỗi; cần dẫn tới mục mô tả hành vi thì trích mục đó theo mục 2.4. Script kiểm tra mọi operationId được trích. Thay cho dạng `` `op` (D-…) `` của DC-20260930-04: admin-web, partner-web khi xử lý DC-20260930-04 trích theo dạng mới. Code: trong kế hoạch, code, test trích endpoint chỉ bằng operationId, không kèm ID mục. | — | ✅ `01`: 2, 4, 7, 9 · `02`: 3.0, 4, 5.1, 5.2, 6 · `03`: 2.7, 3.6, 4.2, 4.4, 5.1–5.3, 5.6, 6 · `04`: 2.2, 2.4, 3.2, 3.4, 5.3, 6 · `05`: 3.2, 4.5, 5.1, 5.2, 6 · `06`: 1, 2, 3.2–3.4, 4, 5, 6, 8 · `07`: 2.1, 3.2, 4.3, 5.1, 5.3 · `index.md`: 2 | — | — | — |
| DC-20260930-06 | 2026-09-30 | partner-web bổ sung vào danh sách API các endpoint đã có ở system-design, mount `partner`: presigned URL tải lên/tải xuống file Nội dung và file Tư liệu gốc (4.7–4.9), `knowledge.listClaims` ở 4.9, `knowledge.searchResearchTopicEmployees` ở 4.10. Không đổi API, không đổi hành vi màn hình. Code: partner app gọi đủ các endpoint này. | D-PRT-007, D-PRT-008, D-PRT-009, D-PRT-010 | — | — | ✅ 4.7–4.10 | — |
| DC-20260930-07 | 2026-09-30 | admin-web bổ sung vào danh sách API các endpoint đã có ở system-design, mount `admin`: `auth.getMe` (¶3 — khôi phục phiên khi tải lại trang), `identity.getEmployee` (4.5), `identity.getOrganization` (4.7), `knowledge.searchResearchTopicEmployees` (4.9 — ô tìm Nhân viên ở khối Chủ nhiệm đề tài và Quản lý nhân sự đề tài), `knowledge.getSourceFileDownloadUrl` (4.11 — nút "Xem/Tải" từng file, disable khi `is_missing`). Không đổi API. Code: admin app gọi đủ các endpoint này. | D-ADM-029, D-ADM-005, D-ADM-007, D-ADM-009, D-ADM-011 | — | ✅ 3, 4.5, 4.7, 4.9, 4.11 · `00-claude-instructions.md`: 6 | — | — |
