# Changelog — System Design (Văn Minh Việt)

## 2026-09-24

- **02-identity.md**: Bổ sung field `organization_name` vào object `employee` trong response `POST /auth/login` và `GET /auth/me` (mục 5.1), lấy qua JOIN `organization.name` trong `GetEmployeeWithRoles` (mục 4); ghi nhận thêm ở mục 6 (Vấn đề mở). Phát hiện khi thực thi partner-web: `Topbar` cần hiển thị tên Tổ chức của Nhân viên đang đăng nhập, nhưng không gọi được `/identity/organizations/{id}` (chỉ mount ở admin) để lấy tên Tổ chức.
- **02-identity.md**: Bổ sung mục 3.0 — cơ chế bootstrap tài khoản Quản trị hệ thống đầu tiên qua seed/migration lúc triển khai (chưa có trong đặc tả gốc). Ghi nhận thêm ở mục 6.

## 2026-09-26

- Đề xuất bổ sung từ luồng admin-web (màn hình 4.23–4.26):
  - **05-ai-assistant.md**: hợp đồng sự kiện SSE cho `POST /assistant/chat` (`token`/`citations`/`self_audit`/`done`/`error`); self-audit chạy sau khi stream, lỗi self-audit không làm hỏng lượt hỏi; `GET /assistant/query-logs`, `/query-logs/{id}`, `/conversations/{id}` trả thêm `asked_by`, `cited_entries`, `self_audit_flag_count`; filter `asked_by_employee_id`, `has_self_audit_flags` kèm index (mục 2.3, 3.2, 4.2, 5.1, 5.2, 6).
  - **04-encyclopedia.md**: thêm `GetEntryTitles` (mục 4.3); mở quyền đọc `GET /encyclopedia/cultural-domains` cho mọi Nhân viên kênh admin (mục 5.3, 6).
  - **01-architecture-and-tech-stack.md**: chốt hàng đợi job là river, Redis không bắt buộc (mục 1, 2, 5); sửa câu self-audit ở mục 6 bước 4 cho khớp luồng streaming; thêm tên loại job, ánh xạ trạng thái và API `/shared/jobs` (list/detail/retry/cancel, có audit log `job.retry`/`job.cancel`) ở mục 4; ghi vấn đề mở về retention job (mục 9).
  - **03-cultural-knowledge-base.md**: cơ chế coalesce webhook theo river (mục 4.2); enqueue `verification.run` cùng transaction (mục 4.3); làm rõ "không tạo job trùng" khi kích hoạt lại AI Verification (mục 3.3, 6).
  - **06-ai-gateway.md**: thời điểm gọi và xử lý lỗi `/v1/self-audit` (mục 3.4, 6); đổi tham chiếu asynq/river → river.
- **05-ai-assistant.md**: `channel` và `asked_by_employee_id` chỉ còn lưu ở `assistant_conversation` (bỏ khỏi `assistant_query_log`, chuyển index sang bảng hội thoại). Filter/hiển thị ở API rà soát lấy qua JOIN theo `conversation_id`. Thêm kiểm tra hội thoại khớp kênh/Nhân viên khi dùng lại `conversation_id` (lỗi `conversation_mismatch`) (mục 2.2, 2.3, 3.2, 4.4, 5.1, 5.2, 6).
- **07-system-settings.md** (mới): thiết kế Cấu hình hệ thống runtime cho Quản trị hệ thống — registry tham số trong code + bảng `system_setting` chỉ lưu giá trị đã đổi; 5 nhóm tham số (AI Verification §2.2.6.5, Tài khoản & bảo mật, Email, AI Văn Minh Việt, Vận hành); đồng bộ cache qua `LISTEN/NOTIFY`; audit `system_setting.update`/`system_setting.reset`; API `/shared/settings` (xem/sửa/khôi phục mặc định, xem trước và gửi thử mẫu email) và `GET /client-settings` (admin, public).
- **01-architecture-and-tech-stack.md**: thêm cấu hình hệ thống vào `/shared` (mục 2); thêm job `shared.job_cleanup`, `shared.apply_storage_lifecycle`, retention job theo cấu hình (mục 4); debounce đồng bộ theo cấu hình (mục 5); rate limit Chat AI công khai chuyển sang middleware Go theo cấu hình, bổ sung chính sách mật khẩu/tạm khoá đăng nhập (mục 7); cập nhật vấn đề mở (mục 9).
- **02-identity.md**: thêm `employee.failed_login_count`, `locked_until`; thời hạn token, chính sách mật khẩu, tạm khoá đăng nhập, mẫu email theo cấu hình (mục 2, 3.1–3.3); thêm `GET /auth/password-policy` (mục 5.1); thêm `POST /identity/employees/{id}/clear-login-lock` và trường `locked_until` trong response Nhân viên (mục 5.2); vấn đề mở (mục 6).
- **03-cultural-knowledge-base.md**: kích hoạt AI Verification theo chế độ `auto`/`manual` và danh sách role được kích hoạt thủ công (mục 3.3, 4.3, 5.4); thêm `can_trigger_ai_verification` ở chi tiết Hạng mục tri thức (mục 5.3); debounce theo cấu hình (mục 4.2, 4.5, 6).
- **05-ai-assistant.md**: top-K, số lượt lịch sử, bật/tắt Rewrite, câu trả lời khi không có ngữ cảnh theo cấu hình (mục 3.2); rate limit kênh `public` (HTTP 429 `rate_limited`), câu miễn trừ trách nhiệm và thời hạn hội thoại qua `GET /client-settings` (mục 5.1); vấn đề mở (mục 6).
- **06-ai-gateway.md**: thêm field tuỳ chọn `no_answer_text` cho `/v1/generate` (mục 3.2, 5).
- Đề xuất bổ sung từ luồng admin-web (màn hình 4.27 Đổi mật khẩu):
  - **02-identity.md**: thêm luồng đổi mật khẩu khi đang đăng nhập (mục 3.4) và `POST /auth/change-password` (mục 5.1), mount ở cả `admin`/`partner`. Sai mật khẩu hiện tại tính chung bộ đếm tạm khoá với đăng nhập, khi bị khoá thì thu hồi refresh token. Từ chối mật khẩu mới trùng mật khẩu hiện tại (`password_unchanged`). Đổi thành công thì thu hồi toàn bộ refresh token và ghi audit `auth.password_change` cùng transaction. Không gửi email thông báo. Mã lỗi `invalid_current_password`/`login_locked`/`password_unchanged`/`password_policy_violation`. Sửa mô tả `failed_login_count` (mục 2), ghi nhận ở mục 6.
  - **01-architecture-and-tech-stack.md**: thêm "đổi mật khẩu" vào danh sách nhóm `auth/*` (mục 2).
- **01-architecture-and-tech-stack.md**: thêm danh mục sự kiện audit đầy đủ (mục 2) — nguồn duy nhất cho `action_type`, nhãn, actor, entity và `detail` theo từng endpoint/job; mở rộng phạm vi audit thành mọi thao tác ghi thành công + thay đổi do hệ thống tự thực hiện; `audit_log.employee_id` nullable, thêm cột `actor_type` (`employee`/`system`); `entity` là đối tượng nghiệp vụ gốc, thành phần con đưa vào `detail`; filter/response `actor_type` ở `GET /shared/audit-logs`; liệt kê các trường hợp không ghi audit; vấn đề mở (mục 9).
- **02-identity.md**, **03-cultural-knowledge-base.md**, **04-encyclopedia.md**, **07-system-settings.md**: trỏ về danh mục sự kiện audit ở `01` thay cho câu "mọi endpoint ghi tự động có audit log"; `auth.login_locked` ghi với actor hệ thống (`02` mục 3.2, 3.4).
- Đồng bộ theo `business-requirements.md` (bổ sung ngày 2026-09-26: §2.1.5.2.1, §2.1.5.7–2.1.5.10, §2.2.5.5, §2.2.6.5.1–2, §2.3.3.1, §2.3.5.3–4, §2.3.7.5, §2.4.6–2.4.9, §2.8, §3.1.2, §3.1.6):
  - **02-identity.md**: thêm `employee.sessions_invalidated_at` và mục 3.5 — vô hiệu hoá phiên ngay; middleware xác thực từ chối token cấp trước mốc này hoặc khi tài khoản không `active` (HTTP 401 `session_revoked`); `disable` thu hồi refresh token và đặt mốc; làm mới phiên kiểm tra `status`; đặt lại/đổi mật khẩu và tạm khoá khi đổi mật khẩu đặt mốc; thay các ghi chú ⚠ đã có trong đặc tả bằng tham chiếu § (mục 2, 3.0, 3.2–3.5, 5.1, 5.2, 6).
  - **01-architecture-and-tech-stack.md**: cập nhật phạm vi audit tối thiểu theo §3.1.2; thời hạn lưu audit log theo cấu hình, dọn bằng job `shared.audit_log_cleanup`; thêm `cultural_domain.delete` vào danh mục audit; thêm job `shared.audit_log_cleanup`, `assistant.query_log_cleanup`; audit log append-only trừ job dọn quá hạn; xác thực kiểm tra phiên ở mỗi request; đóng vấn đề mở về dọn audit log (mục 2, 4, 7, 9).
  - **07-system-settings.md**: thêm `operations.audit_log_retention_months` (mặc định 24, 12–120) và `assistant.query_log_retention_days` (mặc định 180, 30–3650) cùng cơ chế dọn; cơ sở đặc tả chuyển sang §2.8; rút gọn vấn đề mở (mục 1, 2.3, 4.3, 6).
  - **04-encyclopedia.md**: xoá Cương vực (`DELETE /encyclopedia/cultural-domains/{id}`, `DeleteCulturalDomain`, `ON DELETE RESTRICT`, lỗi `cultural_domain_in_use`); `review_note` bắt buộc khi `reject` (lỗi `review_note_required`); §2.3.8 chuyển từ "treo" sang "cần thiết kế"; thay ghi chú ⚠ bằng tham chiếu § (mục 2.5, 2.6, 3.2, 4.4, 5.2, 5.3, 6).
  - **05-ai-assistant.md**: dọn nhật ký hỏi đáp quá hạn theo hội thoại (mục 3.3, job `assistant.query_log_cleanup`, `ON DELETE CASCADE`); thay ghi chú ⚠ bằng tham chiếu § (mục 2.3, 4.4, 6).
  - **03-cultural-knowledge-base.md**: `dang_xet_duyet_ai` và phạm vi kích hoạt lại trỏ về §2.2.6.5.1–2; `employee-search` trỏ về §2.2.5.5 (mục 3.3, 5.1, 6).

## 2026-09-28

- CR-20260928-01: đổi toàn bộ trích dẫn mục đặc tả `§...` sang dạng chuẩn `R-XXX-NNN (§...)`; khoảng mục ghi ID cho hai đầu mút `R-A (§X)–R-B (§Y)`. Không đổi nội dung thiết kế. File: **01-architecture-and-tech-stack.md** (103), **02-identity.md** (110), **03-cultural-knowledge-base.md** (293), **04-encyclopedia.md** (110), **05-ai-assistant.md** (29), **06-ai-gateway.md** (11), **07-system-settings.md** (22), **00-claude-instructions.md** (2).
- **06-ai-gateway.md**: dòng trạng thái — trích dẫn mục nội bộ của `03` ghi dạng "mục 4.2–4.4" thay cho `§`; bỏ câu kể lịch sử cập nhật.
- `00-claude-instructions.md`: bổ sung 06 (AI Gateway) và 07 (Cấu hình hệ thống) vào thứ tự build (mục 4); cấu trúc chuẩn mục 5 áp dụng cho 02–05 và 07, còn 01 và 06 có cấu trúc riêng; mục 7 thêm quy định về `index.md`.
- `index.md` (mới): mục lục bộ tài liệu thiết kế — file ↔ package/route ↔ phụ thuộc ↔ trạng thái, và bảng "đọc gì khi làm gì" cho Team Code.
- `index.md`: sửa phụ thuộc vòng 02 ↔ 07 — 07 chỉ phụ thuộc 01 (dùng xác thực/role của 02 và `GetEmployeeSummaries` ở tầng `/cmd/api`, không phải phụ thuộc package); thêm 07 vào sơ đồ chiều phụ thuộc ở mục 2.

## 2026-09-29

- DC-20260929-01: chuyển sang quy ước ID và trích dẫn mục thiết kế (`common/requirements-design-sync.md` mục 2.4). Không đổi nội dung thiết kế, không đánh số lại mục.
  - Gắn ID cho 102 mục: **01** D-SD01-001–008 (¶1–8), **02** D-SD02-001–010 (¶2, 3.0–3.5, 4, 5.1, 5.2), **03** D-SD03-001–026 (¶2.1–2.9, 3.1–3.6, 4.1–4.5, 5.1–5.6), **04** D-SD04-001–018, **05** D-SD05-001–013, **06** D-SD06-001–013 (¶1, 2, 3.1–3.7, 4–7), **07** D-SD07-001–014.
  - Đổi trích dẫn "mục N", "`0X` mục N", "`0X-….md` mục N", "mục N tài liệu 0X" sang `D-… (¶…)`, `` `0X` ¶N `` hoặc `¶N`; trích dẫn luồng web sang `admin-web ¶N` / `partner-web ¶N` (kể cả tên file cũ `admin-web-layout.md`, `partner-web-layout.md`). File: **01** (93 dòng), **02** (89), **03** (170), **04** (69), **05** (76), **06** (74), **07** (44), `00-claude-instructions.md` (1), `index.md` (7).
  - Sửa trích dẫn trỏ sai: `04` dòng comment "mục 4.2 tài liệu 01" → D-SD05-008 (¶4.2); `06` dòng trạng thái "`03` … mục 8" → D-SD05-011 (¶4.5); `06` ¶3.6 "mục 2.8" → D-SD03-008 (¶2.8); `03` ¶4.1 "tài liệu 01 mục 5, mục 4.5" → D-SD01-005 (¶5), D-SD03-020 (¶4.5).
  - **01** ¶8: trích dẫn đặc tả "(mục 3.2)" → R-NFR-009 (§3.2).
  - Trích dẫn "mục N của `00-claude-instructions.md`" viết lại thành "`00-claude-instructions.md` mục N" (01, 02, 05).
- DC-20260929-02, DC-20260929-03: thêm ID vào trích dẫn màn hình luồng web — `admin-web ¶4.x` → `D-ADM-0xx (¶4.x)`, `partner-web ¶4.x` → `D-PRT-0xx (¶4.x)`; sửa tên file cũ `admin-web-layout.md`/`partner-web-layout.md` ở `03` ¶6 thành D-ADM-008 (¶4.8)/D-PRT-004 (¶4.4). Không đổi nội dung thiết kế. File: **01** (¶2, ¶9), **02** (¶4, ¶6), **03** (¶4.2, ¶5.1, ¶5.2, ¶6), **04** (¶6), **05** (¶5.2).
- DC-20260929-05: job nối tiếp cho `ingestion.sync_source` (theo báo cáo của Code: river luôn tính job `running` là trùng).
  - **03-cultural-knowledge-base.md** ¶4.2 (D-SD03-017): `HandleSourceReadyWebhook` — tính trùng theo payload, `ByState` gồm `available`, `pending`, `scheduled`, `running`, `retryable`; trùng với job đang `running` thì enqueue job nối tiếp `{source_id, follows_job_id}` với `id` lấy từ kết quả `InsertTx`, sự kiện sau gộp vào job nối tiếp; gặp advisory lock thì hoãn bằng `JobSnooze` trong `operations.source_sync_debounce_seconds`, áp dụng cho cả job thường và job nối tiếp. ¶6: bullet debounce/coalesce ghi thêm thời gian hoãn và job nối tiếp.
  - **01-architecture-and-tech-stack.md** ¶4 (D-SD01-004): payload `ingestion.sync_source` là `{source_id}` hoặc `{source_id, follows_job_id}`. ¶1 (D-SD01-001): river có thêm hoãn job (snooze).
  - **07-system-settings.md** ¶2.3 (D-SD07-003): `operations.source_sync_debounce_seconds` áp dụng cả cho job hoãn.

## 2026-09-30

- DC-20260930-03: nguồn dữ liệu cho thông báo "AI Verification đang chạy" (theo báo cáo của luồng admin-web).
  - **03-cultural-knowledge-base.md** ¶5.3 (D-SD03-023): chi tiết Hạng mục tri thức thêm `ai_verification_running` (bool, còn job `verification.run` đang chờ/đang chạy theo định nghĩa job trùng ở D-SD03-012 (¶3.3) bước (3)). ¶5.4 (D-SD03-024): response `trigger-ai-verification` thêm `merged_into_running_job`; lệnh gộp thì không tạo job, không đổi trạng thái, không ghi audit.
  - **01-architecture-and-tech-stack.md** ¶2 (D-SD01-002): thêm trường hợp trigger bị gộp vào danh sách "Không ghi audit".

- DC-20260930-04: định danh endpoint API bằng operationId và quy ước hợp đồng OpenAPI.
  - `common/requirements-design-sync.md`: thêm mục 2.5 (operationId — phạm vi, định dạng `<tiền tố>.<tên>`, dùng chung khi mount nhiều nhóm route, quy tắc bất biến, cách trích `` `op` (D-…) ``); mục 5 thêm các lỗi operationId và lỗi trích endpoint chỉ bằng method + path; mục 7 thêm quy định dùng operationId trong hợp đồng OpenAPI, kế hoạch, code và test.
  - **01-architecture-and-tech-stack.md** ¶3 (D-SD01-003): thêm quy ước hợp đồng OpenAPI — một file cho mỗi nhóm route `admin`/`partner`/`public`, operationId theo thiết kế, kiểm tra tự động trong CI hợp đồng khớp code cả route lẫn schema (cách làm do Code chọn), 3 web app sinh API client từ hợp đồng, chat khai báo `text/event-stream`, webhook nội bộ và AI Gateway ngoài 3 file hợp đồng. ¶8 (D-SD01-008): dòng "Tài liệu kỹ thuật" trỏ về ¶3.
  - `00-claude-instructions.md` mục 6: thêm nguyên tắc operationId.
  - **01**–**07**: thêm cột `operationId` vào mọi bảng endpoint (133 endpoint); `07` ¶5.2 (D-SD07-013) ghi operationId dưới tiêu đề; `06` ¶7 gắn `gateway.getHealth` cho `GET /v1/health`.
  - **01**–**07**, `index.md`: đổi 216 chỗ trích endpoint sang dạng `` `op` (D-…) `` (văn xuôi có đủ method + path giữ thêm ` — METHOD /path`), bỏ trích dẫn cùng mục bị lặp ngay sau; danh mục sự kiện audit ở `01` ¶2 ghi operationId thay cho path viết tắt.
  - `common/tools/check-requirement-refs.py`: đọc operationId từ bảng endpoint; báo bảng thiếu cột, endpoint thiếu operationId, sai định dạng/tiền tố, trùng, endpoint trong mục chưa có ID, trích `op` sai hoặc sai ID mục, và trích endpoint chỉ bằng method + path.

- DC-20260930-05: trích endpoint chỉ bằng operationId, bỏ ID mục đi kèm.
  - `common/requirements-design-sync.md`: mục 2.5 dạng chuẩn chỉ ghi operationId, trích mục hành vi thì ghi riêng theo mục 2.4, không ghi ID trần ngay sau operationId; mục 5 đổi lỗi tương ứng; mục 7 Code trích endpoint chỉ bằng operationId.
  - `common/tools/check-requirement-refs.py`: kiểm tra mọi operationId được trích; báo lỗi khi có ID mục trần ngay sau operationId.
  - **01**–**07**, `index.md`: bỏ ID mục đi kèm operationId ở 215 chỗ.

## 2026-10-01

- DC-20261001-01: API nhóm `public` của Bách khoa toàn thư (theo câu hỏi của Code ở PUBLICWEB-14, PUBLICWEB-17).
  - **04-encyclopedia.md** ¶5.4 (D-SD04-018): path `/encyclopedia/entries`, `/encyclopedia/entries/{id}`, `/encyclopedia/cultural-domains` dưới `/api/v1/public`, operationId giữ `public.*`; lọc `cultural_domain_id` lặp nhiều lần (OR); `public.listEntries` trả `excerpt` (200 ký tự), `cover_image`, `cultural_domain_ids` sắp theo tên; `public.getEntry` trả `cover_image`, `files[].url`/`url_expires_at` ký sẵn 60 phút, bỏ `storage_key`. ¶2.2 (D-SD04-002): cột `entry_version.cover_file_id` tính khi tạo dòng chốt. ¶4.3 (D-SD04-013): hàm `GetPublicCoverImages`. ¶5.3, ¶6: bỏ trích path `/public/...` cũ.
  - **05-ai-assistant.md** ¶5.1 (D-SD05-012): sự kiện `citations` thêm `cover_image`; bỏ trích path `/public/cultural-domains` cũ.
  - **01-architecture-and-tech-stack.md** ¶3 (D-SD01-003): ngoại lệ trả sẵn presigned GET URL cho nhóm `public`.
  - `common/requirements-design-sync.md` mục 2.5: ngoại lệ tiền tố `public` cho endpoint riêng nhóm `public`. `common/tools/check-requirement-refs.py`: chấp nhận tiền tố `public` với mọi path, endpoint `public.*` không đè endpoint cùng path ở bảng tra.

- DC-20261001-02: thiết kế R-ENC-038 (§2.3.8) "Khởi tạo nội dung Mục từ bằng AI".
  - **04-encyclopedia.md**: ¶3.5 mới (D-SD04-019) — kích hoạt thủ công `encyclopedia.generateEntryContent` (soan_thao, đúng Người phụ trách, xác nhận ghi đè, có nguồn, không trùng job), khoá sửa nội dung/file/gửi xét duyệt khi còn job, Release/ForceRelease huỷ job đang chờ, job `encyclopedia.generate_content` đọc phiên bản đang được sử dụng của Hạng mục tri thức, gọi `gateway.generateEntryDraft`, ghi khi vẫn soan_thao và đúng Người phụ trách (ngược lại bỏ kết quả), ảnh tạo `entry_file` dùng lại `storage_key`, cập nhật `last_synced_version_id`. ¶4.5 mới (D-SD04-020) — gọi AI Gateway, ánh xạ khối. ¶1: thêm gạch gọi AI Gateway. ¶4.4: hàm `RequestContentGeneration`, `ApplyGeneratedContent`, điều kiện khoá ở các hàm ghi nội dung/file/gửi xét duyệt, Release/ForceRelease huỷ job. ¶5.1, ¶5.2: endpoint mới, `content_generation` ở `encyclopedia.getEntry`, lỗi 409 `entry_content_generation_running`. ¶6: thay bullet "chưa thiết kế". Dòng trạng thái: đã chốt ¶1–6.
  - **06-ai-gateway.md**: ¶3.8 mới (D-SD06-014) `gateway.generateEntryDraft` — `POST /v1/generate-entry-draft`. ¶1: 3 năng lực. ¶2, ¶4, ¶5, ¶6, ¶8: thêm năng lực mới (timeout 300s, thuộc đường nền).
  - **01-architecture-and-tech-stack.md**: ¶6 (D-SD01-006) 3 năng lực, điểm gọi `/internal/encyclopedia`; ¶4 (D-SD01-004) loại job `encyclopedia.generate_content`; ¶2 (D-SD01-002) 3 sự kiện audit `entry.content_generation_request`/`_complete`/`_discard`.
  - `index.md`: `04` phụ thuộc thêm 06, trạng thái đã chốt ¶1–6; 06 được gọi bởi 04.

- DC-20261001-03: chốt các điểm còn mở của DC-20261001-01 và DC-20261001-02.
  - **04-encyclopedia.md** ¶2.6 (D-SD04-006): `entry_cultural_domain` thêm `created_at` (thời điểm gán), migration đặt giá trị cho dòng có sẵn theo tên Cương vực. ¶5.4 (D-SD04-018): `cultural_domain_ids` ở nhóm `public` sắp theo thứ tự gán. ¶3.5 (D-SD04-019) bước 4: lỗi `source_content_too_long` dừng job, không thử lại. ¶5.1: `content_generation` thêm `error_code`.
  - **06-ai-gateway.md** ¶3.8 (D-SD06-014): nguồn vượt giới hạn ngữ cảnh → HTTP 422 `source_content_too_long`, không cắt bớt; model LLM/VLM cấu hình riêng, mặc định dùng model của `gateway.generate`/`gateway.verifyImageRegion`. ¶7: biến môi trường `ENTRY_DRAFT_LLM_MODEL`, `ENTRY_DRAFT_VLM_MODEL`.
  - Giữ nguyên, đã chốt: thời hạn URL tệp công khai 60 phút; kích hoạt lại khi đang chạy trả 409; Release/ForceRelease huỷ job đang chờ; timeout `gateway.generateEntryDraft` 300 giây; ảnh xếp cuối khi không có VLM; tự cập nhật `last_synced_version_id` sau khi sinh nội dung.

- DC-20261001-05: chế độ phát triển và tài khoản Quản trị hệ thống gốc.
  - **01-architecture-and-tech-stack.md**: ¶9 mới (D-SD01-009) Chế độ phát triển — biến `DEV_MODE`, `DEV_RESET_ON_START`, `DEV_MAILBOX_URL`, `ROOT_ADMIN_*`; thứ tự khởi động `/cmd/api`; xoá sạch dữ liệu khi khởi động (drop/tạo lại schema, không xoá MinIO/S3, worker không chạy lúc xoá); xem email qua Mailpit sau reverse proxy có basic auth. "Vấn đề mở" đổi số 9 → 10. ¶1: dòng Email/SMTP thêm giao diện Mailpit ở Dev. ¶2: danh sách không ghi audit thêm xoá sạch dữ liệu, cập nhật dòng tài khoản gốc.
  - **02-identity.md**: ¶3.0 (D-SD02-002) viết lại thành Tài khoản Quản trị hệ thống gốc — `/cmd/api` tạo khi khởi động theo `ROOT_ADMIN_*` thay cho seed/migration; `DEV_MODE` đặt lại mật khẩu mỗi lần khởi động, không áp dụng chính sách mật khẩu; bảo vệ tài khoản gốc (không khoá, không gỡ `quan_tri_he_thong`, không đổi Tổ chức — 422 `root_admin_protected`). ¶5.1: `dev_mailbox_url` trong response `auth.login`/`auth.getMe`. ¶5.2: điều kiện chặn ở `identity.disableEmployee`, `identity.removeEmployeeRole`, `identity.updateEmployee`; `is_root_admin` ở `identity.listEmployees`/`identity.getEmployee`. ¶6: cập nhật ghi chú tài khoản gốc.
  - **05-ai-assistant.md** ¶2.1, **06-ai-gateway.md** ¶3.1, ¶5, ¶7, ¶8: trích "Vấn đề mở" của `01` đổi ¶9 → ¶10.
