# Thiết Kế: Cấu Hình Hệ Thống (`/shared` — system settings)

## 1. Tổng quan

- Cho phép Nhân viên giữ role `quan_tri_he_thong` điều chỉnh các tham số vận hành và nghiệp vụ của hệ thống qua Admin nội bộ, không cần lập trình viên sửa code hay deploy lại.
- Cơ sở đặc tả: R-CFG-001 (§2.8) (Cấu hình hệ thống — chỉ Quản trị hệ thống, sửa và khôi phục mặc định từng tham số, có hiệu lực không cần triển khai lại, mọi thay đổi ghi audit log); R-CFG-003 (§2.8.2) (mỗi tham số có mô tả tác động); R-NFR-041 (§3.7.4) (hiển thị giá trị tham số chi phối thao tác cho cả Nhân viên không có quyền vào Cấu hình); R-KB-077 (§2.2.6.5) (kích hoạt AI Verification tự động/thủ công theo cấu hình); R-ID-022 (§2.1.5.5), R-ID-029 (§2.1.5.8), R-ID-030 (§2.1.5.9) (thời hạn đường dẫn, chính sách mật khẩu, tạm khoá đăng nhập); R-AI-007 (§2.4.6)–R-AI-010 (§2.4.9) (tham số AI Văn Minh Việt, thời hạn lưu nhật ký hỏi đáp); R-NFR-004 (§3.1.2) (thời hạn lưu audit log); R-NFR-008 (§3.1.6) (rate limit Trợ lý AI công khai). Danh sách tham số cụ thể, giá trị mặc định và giới hạn là quyết định của thiết kế (R-CFG-011 (§2.8.5)).
- Thuộc package `/shared` (cùng nhóm với `audit_log`, `usage_event`, API job nền — D-SD01-002 (¶2)): cấu hình dùng chung cho mọi module, không thuộc riêng module nghiệp vụ nào. Các package khác chỉ **đọc** qua hàm nội bộ của `/shared`, không chạm bảng.
- **Ngoài phạm vi** — không đưa lên giao diện, giữ ở biến môi trường/secret lúc triển khai: `AI_GATEWAY_MODE`, đường dẫn model, mọi shared secret (AI Gateway, webhook MinIO/S3), thông tin truy cập MinIO/S3 và SMTP/SES, allowlist CORS, thông tin tài khoản Quản trị hệ thống đầu tiên (D-SD02-002 (¶3.0)), prompt hệ thống của AI Gateway (quản lý theo phiên bản trong code, D-SD06-011 (¶5)), tham số chunking (`05` ¶6). Nội dung hiển thị trang chủ Web công khai (banner, mục nổi bật...) là nội dung của web, không thuộc cấu hình hệ thống.

## 2. Mô hình dữ liệu

### 2.1. [D-SD07-001] Danh mục tham số (registry) — khai báo trong code

Mỗi tham số được **khai báo trong code Go** (registry trong `/shared`), không phải dữ liệu seed: `key`, `group`, kiểu giá trị, giá trị mặc định, ràng buộc (min/max, tập giá trị hợp lệ, định dạng), phạm vi lộ ra client (`exposure`), và phần mô tả cho màn hình Cấu hình (R-CFG-003 (§2.8.2)):

- `label` — tên hiển thị tiếng Việt.
- `description` — mô tả ngắn: tham số ảnh hưởng tới vai trò và chức năng nào (cột "Ảnh hưởng" ở D-SD07-003 (¶2.3)), kèm ghi chú áp dụng nếu có.
- `applies_to` — `existing` (áp dụng cả cho dữ liệu đang có) hoặc `new_only` (chỉ áp dụng cho thao tác phát sinh sau khi lưu), theo cột "Áp dụng" ở D-SD07-003 (¶2.3).

Code soạn `label`/`description` theo các cột của bảng tham số. Thêm tham số mới = thêm khai báo trong code (kể cả 3 trường trên) + deploy; không cần migration dữ liệu.

`exposure` — một tham số có thể có nhiều giá trị:
- `server` — chỉ backend đọc (mặc định).
- `admin_client` — trả cho frontend Admin nội bộ qua `clientSettings.getSettings` — `GET /client-settings` — mọi Nhân viên đã đăng nhập ở kênh `admin`.
- `partner_client` — trả cho Cổng Tổ chức khác qua `clientSettings.getSettings` ở kênh `partner` — mọi Nhân viên đã đăng nhập ở kênh `partner`.
- `public_client` — trả cho Web công khai qua `clientSettings.getSettings` ở kênh `public` (không xác thực).

Tham số chi phối kết quả hoặc diễn biến của một thao tác của Nhân viên được lộ ra ở kênh có thao tác đó, để màn hình hiển thị giá trị hiện hành (R-NFR-041 (§3.7.4)). Không bao giờ lộ ra client: mẫu email, địa chỉ gửi, tham số rate limit, thời hạn token phiên.

### 2.2. [D-SD07-002] Bảng `system_setting` — chỉ lưu giá trị đã đổi khỏi mặc định

| Field | Kiểu | Ghi chú |
|---|---|---|
| `key` | text, PK | Trùng `key` trong registry (D-SD07-001 (¶2.1)). Key không có trong registry bị bỏ qua khi nạp (ghi log cảnh báo) — trường hợp tham số đã bị gỡ khỏi code |
| `value` | JSONB, NOT NULL | Giá trị đã validate theo kiểu của key |
| `updated_by` | UUID | `employee.id` người sửa gần nhất — không đặt FK sang bảng của `/identity` (cùng nguyên tắc `audit_log`, D-SD01-002 (¶2)) |
| `updated_at` | timestamptz | |

- Key **không có dòng** trong bảng → dùng giá trị mặc định khai báo trong code. "Khôi phục mặc định" = xoá dòng.
- Nhờ vậy, đổi giá trị mặc định trong code ở bản deploy sau sẽ tự áp dụng cho những key chưa từng bị chỉnh.

### 2.3. [D-SD07-003] Danh sách tham số

Cột **Áp dụng**: `existing` hoặc `new_only` (D-SD07-001 (¶2.1)), kèm ghi chú thời điểm có hiệu lực khi cần. Mọi thay đổi có hiệu lực cho thao tác tiếp theo sau khi lưu (D-SD07-008 (¶4.2)). Cột **Ảnh hưởng**: vai trò — chức năng chịu tác động, làm nguồn cho `description`.

**Nhóm `ai_verification` — AI Verification (R-KB-077 (§2.2.6.5))**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Ảnh hưởng | Exposure |
|---|---|---|---|---|---|---|
| `ai_verification.trigger_mode` | text | `auto` | `auto` / `manual` | `new_only` — chỉ các lần `submit-for-review` sau khi lưu (D-SD07-004 (¶3.1)) | Nghiên cứu — Gửi xét duyệt Hạng mục tri thức; các role kích hoạt AI Verification | server, admin_client, partner_client |
| `ai_verification.manual_trigger_roles` | text[] | `["nghien_cuu", "xet_duyet"]` | Tập con của `nghien_cuu`, `xet_duyet`, `chu_nhiem_de_tai`, `quan_tri_he_thong`; **không được rỗng khi `trigger_mode = manual`** | `existing` | Các role được chọn — Kích hoạt AI Verification thủ công | server, admin_client, partner_client |

**Nhóm `identity` — Tài khoản & bảo mật (module 02)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Ảnh hưởng | Exposure |
|---|---|---|---|---|---|---|
| `identity.invite_token_ttl_hours` | int | 72 | 1–720 | `new_only` — token mời sinh sau khi lưu (R-ID-022 (§2.1.5.5)) | Quản trị hệ thống — Tạo Nhân viên, Gửi lại lời mời; Nhân viên được mời — đặt mật khẩu lần đầu | server, admin_client |
| `identity.password_reset_token_ttl_minutes` | int | 60 | 10–1440 | `new_only` — token đặt lại sinh sau khi lưu (R-ID-022 (§2.1.5.5)) | Mọi Nhân viên — Quên mật khẩu | server |
| `identity.access_token_ttl_minutes` | int | 15 | 5–120 | `new_only` — access token cấp sau khi lưu | Mọi Nhân viên — phiên đăng nhập | server |
| `identity.refresh_token_ttl_days` | int | 7 | 1–90 | `new_only` — refresh token cấp sau khi lưu | Mọi Nhân viên — phiên đăng nhập | server |
| `identity.password_min_length` | int | 8 | 8–64 | `new_only` — mật khẩu đặt mới sau khi lưu; không buộc đổi mật khẩu hiện có | Mọi Nhân viên — đặt mật khẩu lần đầu, đặt lại, đổi mật khẩu | server (client đọc qua `auth.getPasswordPolicy`) |
| `identity.password_require_letter_and_digit` | bool | `true` | | như trên | như trên | như trên |
| `identity.password_require_special_char` | bool | `false` | | như trên | như trên | như trên |
| `identity.login_max_failed_attempts` | int | 5 | 0–20; `0` = tắt cơ chế tạm khoá | `existing` | Mọi Nhân viên — Đăng nhập, Đổi mật khẩu; Quản trị hệ thống — Gỡ tạm khoá | server, admin_client |
| `identity.login_lockout_minutes` | int | 15 | 1–1440 | `new_only` — các lần tạm khoá phát sinh sau khi lưu | như trên | server, admin_client |

**Nhóm `email` — Email hệ thống (mời, đặt lại mật khẩu)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Ảnh hưởng | Exposure |
|---|---|---|---|---|---|---|
| `email.sender_name` | text | `Văn Minh Việt` | 1–100 ký tự | `new_only` — email gửi sau khi lưu | Nhân viên nhận email mời, đặt lại mật khẩu | server |
| `email.sender_address` | text | Giá trị biến môi trường `EMAIL_DEFAULT_SENDER` | Định dạng email; **tên miền phải thuộc** `EMAIL_ALLOWED_SENDER_DOMAINS` (biến môi trường — các tên miền đã xác minh gửi trên Amazon SES) | `new_only` — như trên | như trên | server |
| `email.template.invite` | object `{subject, body_html}` | Mẫu mặc định trong code | Xem D-SD07-010 (¶4.4) | `new_only` — như trên | Nhân viên được mời | server |
| `email.template.password_reset` | object `{subject, body_html}` | Mẫu mặc định trong code | Xem D-SD07-010 (¶4.4) | `new_only` — như trên | Nhân viên yêu cầu đặt lại mật khẩu | server |

**Nhóm `assistant` — AI Văn Minh Việt (module 05)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Ảnh hưởng | Exposure |
|---|---|---|---|---|---|---|
| `assistant.retrieve_top_k` | int | 8 | 1–30 | `new_only` — lượt hỏi sau khi lưu | Người dùng Web công khai, Nhân viên — chất lượng câu trả lời AI Văn Minh Việt | server |
| `assistant.history_turns` | int | 6 | 0–20; `0` = không dùng lịch sử (mỗi lượt hỏi độc lập, bỏ qua Rewrite) | `new_only` — như trên | như trên | server |
| `assistant.rewrite_query_enabled` | bool | `true` | | `new_only` — như trên | như trên | server |
| `assistant.conversation_ttl_hours` | int | 6 | 1–168 | `existing` — client đọc khi tải trang | Người dùng Web công khai, Nhân viên — thời gian giữ hội thoại trên trình duyệt | admin_client, public_client |
| `assistant.no_context_answer` | text | `Xin lỗi, Bách khoa Văn Minh Việt hiện chưa có thông tin về nội dung này.` | 1–500 ký tự | `new_only` — lượt hỏi sau khi lưu | Người dùng Web công khai, Nhân viên — câu trả lời khi không tìm thấy nội dung | server |
| `assistant.disclaimer_text` | text | `Câu trả lời do AI tạo ra dựa trên Bách khoa Văn Minh Việt và có thể chưa chính xác. Vui lòng đối chiếu với các Mục từ nguồn.` | 0–500 ký tự; rỗng = không hiển thị | `existing` — client đọc khi tải trang | Người dùng Web công khai, Nhân viên — câu miễn trừ dưới câu trả lời | admin_client, public_client |
| `assistant.query_log_retention_days` | int | 180 | 30–3650 | `existing` — lần dọn kế tiếp (D-SD07-009 (¶4.3)) | Quản trị hệ thống — Nhật ký hỏi đáp AI (tự xoá) | server, admin_client |
| `assistant.public_rate_limit_enabled` | bool | `false` | | `new_only` — request sau khi lưu | Người dùng Web công khai — Chat AI | server |
| `assistant.public_rate_limit_max_requests` | int | 20 | 1–1000 | `new_only` — như trên | như trên | server |
| `assistant.public_rate_limit_window_seconds` | int | 60 | 10–86400 | `new_only` — như trên | như trên | server |

**Nhóm `operations` — Vận hành**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Ảnh hưởng | Exposure |
|---|---|---|---|---|---|---|
| `operations.source_sync_debounce_seconds` | int | 45 | 10–600 | `new_only` — sự kiện webhook nhận và job hoãn sau khi lưu | Nhập liệu — đồng bộ Tư liệu gốc tự động | server, admin_client |
| `operations.job_retention_completed_hours` | int | 24 | 1–2160 | `existing` — lần dọn kế tiếp (D-SD07-009 (¶4.3)) | Quản trị hệ thống — Theo dõi job nền | server, admin_client |
| `operations.job_retention_cancelled_hours` | int | 24 | 1–2160 | như trên | như trên | server, admin_client |
| `operations.job_retention_discarded_hours` | int | 168 | 1–2160 | như trên | như trên | server, admin_client |
| `operations.audit_log_retention_months` | int | 24 | 12–120 (R-NFR-004 (§3.1.2): không dưới 12 tháng) | `existing` — lần dọn kế tiếp (D-SD07-009 (¶4.3)) | Quản trị hệ thống — Nhật ký hoạt động | server, admin_client |
| `operations.source_cold_storage_after_days` | int, nullable | `null` | `null` (không chuyển) hoặc 30–3650 | `existing` — khi lưu, enqueue job áp quy tắc lifecycle lên bucket (D-SD07-009 (¶4.3)) | Nhập liệu, Nghiên cứu — tốc độ mở phiên bản cũ của file Tư liệu gốc | server |
| `operations.admin_polling_interval_seconds` | int | 30 | 10–300 | `existing` — client đọc khi tải trang | Quản trị hệ thống — tần suất tự làm mới Nhật ký hoạt động, Theo dõi job nền | admin_client |

## 3. Luồng nghiệp vụ

### 3.1. [D-SD07-004] Kích hoạt AI Verification theo cấu hình (R-KB-077 (§2.2.6.5))

- `trigger_mode = auto`: `submit-for-review` chuyển `dang_nghien_cuu → cho_xet_duyet` rồi kích hoạt AI Verification ngay trong cùng transaction (`cho_xet_duyet → dang_xet_duyet_ai`, enqueue `verification.run`) — D-SD03-018 (¶4.3).
- `trigger_mode = manual`: `submit-for-review` chỉ chuyển sang `cho_xet_duyet` và dừng ở đó. Hạng mục chờ tới khi một Nhân viên được phép gọi `trigger-ai-verification`.
- Quyền kích hoạt thủ công (áp dụng ở **cả 2 chế độ** — ở chế độ `auto` là kích hoạt lại): Nhân viên giữ ít nhất một role trong `manual_trigger_roles`. Role theo phạm vi (`nghien_cuu`, `xet_duyet`, `chu_nhiem_de_tai`) chỉ tính khi gắn với **đúng Đề tài nghiên cứu cha** của hạng mục. `quan_tri_he_thong` là role theo chức năng, chỉ có ở kênh `admin`.
- Đổi chế độ không tự xử lý lại các hạng mục đang có: hạng mục đang ở `cho_xet_duyet` khi chuyển `manual → auto` vẫn phải kích hoạt thủ công. Màn hình cấu hình hiển thị cảnh báo này khi đổi chế độ.

### 3.2. [D-SD07-005] Sửa cấu hình

1. Quản trị hệ thống mở màn hình Cấu hình, sửa một hoặc nhiều tham số trong một nhóm, bấm Lưu → `shared.updateSettings` — `PATCH /shared/settings`.
2. Backend validate từng key theo registry, sau đó validate ràng buộc liên key (ví dụ `manual_trigger_roles` không rỗng khi `trigger_mode = manual` — kiểm trên giá trị **sau khi** áp toàn bộ thay đổi của request). Có lỗi → từ chối cả request (không lưu một phần), trả lỗi theo từng key.
3. Hợp lệ → trong **một transaction**: upsert các dòng `system_setting` (giá trị trùng mặc định thì xoá dòng thay vì upsert); ghi một dòng `audit_log` cho mỗi key thay đổi (D-SD07-006 (¶3.3)); gửi `NOTIFY system_setting_changed` (D-SD07-008 (¶4.2)).
4. "Khôi phục mặc định" một key → `shared.resetSetting` — `DELETE /shared/settings/{key}`, cùng cơ chế validate liên key, audit và NOTIFY như trên.

### 3.3. [D-SD07-006] Audit log

- `action_type = system_setting.update` (sửa) / `system_setting.reset` (khôi phục mặc định); `entity_type = system_setting`; `entity_id = NULL` (key là text, không phải UUID — cùng cách xử lý job ở D-SD01-004 (¶4)); `detail = {key, old_value, new_value}` (`old_value`/`new_value` là giá trị hiệu lực trước/sau, kể cả khi đó là mặc định).
- Ghi cùng transaction với thao tác lưu, theo quy ước chung (D-SD01-002 (¶2), D-SD01-003 (¶3)).
- Hai sự kiện này nằm trong danh mục sự kiện audit chung (D-SD01-002 (¶2)).

## 4. Kiến trúc riêng

### 4.1. [D-SD07-007] Đọc cấu hình từ các package khác

- `/shared` expose getter có kiểu: `shared.Settings.Int(key)`, `Bool(key)`, `String(key)`, `Strings(key)`, `EmailTemplate(key)`... Getter đọc từ bộ nhớ đệm trong tiến trình, không truy vấn DB mỗi lần gọi.
- Package nghiệp vụ gọi getter tại **thời điểm dùng** (ví dụ lúc sinh token, lúc nhận webhook), không đọc một lần lúc khởi động rồi giữ lại — để thay đổi có hiệu lực mà không cần khởi động lại.
- Mọi key dùng trong code tham chiếu qua hằng số khai báo cùng registry, tránh gõ sai tên key.

### 4.2. [D-SD07-008] Đồng bộ bộ nhớ đệm giữa các tiến trình (`/cmd/api`, `/cmd/worker`)

- Khi khởi động: nạp toàn bộ bảng `system_setting` vào bộ nhớ, trộn với mặc định từ registry.
- Khi có thay đổi: transaction lưu cấu hình gửi `NOTIFY system_setting_changed`; mọi tiến trình `LISTEN` kênh này và nạp lại toàn bộ bảng (bảng nhỏ, vài chục dòng).
- Dự phòng mất kết nối LISTEN: nạp lại định kỳ mỗi 60 giây. Độ trễ tối đa để một thay đổi có hiệu lực ở mọi tiến trình vì vậy là ~60 giây trong trường hợp xấu nhất, thường là tức thời.

### 4.3. [D-SD07-009] Tham số cần cơ chế áp dụng riêng

- **Thời gian giữ job (`operations.job_retention_*`)**: river cấu hình thời gian giữ job lúc khởi tạo client, không đổi được khi đang chạy. Vì vậy khởi tạo river client với thời gian giữ rất lớn (vô hiệu hoá thực tế bộ dọn dẹp mặc định), và dọn bằng periodic job riêng `shared.job_cleanup` (river periodic job, chạy mỗi giờ): xoá dòng `river_job` ở trạng thái `completed`/`cancelled`/`discarded` có `finalized_at` quá thời gian giữ tương ứng đọc từ cấu hình.
- **Thời hạn lưu audit log (`operations.audit_log_retention_months`)** (R-NFR-004 (§3.1.2)): periodic job `shared.audit_log_cleanup` (river periodic job, chạy mỗi ngày) xoá các dòng `audit_log` có `created_at < now() - N tháng`, xoá theo lô để không khoá bảng lâu. Đây là thao tác DELETE duy nhất trên `audit_log` (D-SD01-007 (¶7)). Job không tự ghi audit log.
- **Thời hạn lưu nhật ký hỏi đáp AI (`assistant.query_log_retention_days`)** (R-AI-014 (§2.4.9.4)): periodic job `assistant.query_log_cleanup` (chạy mỗi ngày, thuộc `/assistant` — package sở hữu bảng) xoá các hội thoại có `last_message_at < now() - N ngày`, cùng toàn bộ lượt hỏi–đáp của hội thoại đó (D-SD05-006 (¶3.3)).
- **Chuyển tư liệu cũ sang cold storage (`operations.source_cold_storage_after_days`)**: khi lưu key này, enqueue job `shared.apply_storage_lifecycle` cùng transaction. Job gọi API lifecycle của S3/MinIO trên bucket Tư liệu gốc: đặt (hoặc gỡ, khi giá trị là `null`) quy tắc chuyển **các phiên bản không còn là bản hiện hành** (noncurrent versions) sang tầng lưu trữ lạnh sau N ngày. Tên tầng lưu trữ lạnh lấy từ biến môi trường `STORAGE_COLD_TIER` (cấu hình hạ tầng). Không xoá phiên bản nào (R-KB-029 (§2.2.3.4) — D-SD01-001 (¶1)).
- **Rate limit Chat AI công khai (`assistant.public_rate_limit_*`)**: middleware Go gắn trên route `assistant.chat` — `POST /api/v1/public/assistant/chat`. Đếm theo IP client lấy từ header `X-Forwarded-For` do Traefik gắn (chỉ tin header khi request đến từ Traefik). Thuật toán cửa sổ cố định, lưu bộ đếm trong bộ nhớ tiến trình. ⚠ Nếu chạy nhiều bản `/cmd/api` song song, giới hạn tính riêng cho từng bản — chấp nhận ở quy mô hiện tại (D-SD01-008 (¶8)); cần chuyển bộ đếm sang Postgres hoặc Redis nếu mở rộng ngang. Vượt ngưỡng → HTTP 429 với lỗi `rate_limited` (quy ước lỗi chung D-SD01-003 (¶3)), kèm header `Retry-After`; không ghi `assistant_query_log`.

### 4.4. [D-SD07-010] Mẫu email

- Mỗi mẫu gồm `subject` (1 dòng, tối đa 200 ký tự) và `body_html` (tối đa 50.000 ký tự).
- Biến chèn được: `{{display_name}}` (tên Nhân viên nhận), `{{link}}` (đường dẫn có token), `{{expires_at}}` (thời điểm hết hạn link, định dạng `dd/MM/yyyy HH:mm`, giờ Việt Nam), `{{organization_name}}` (Tổ chức của Nhân viên nhận). Biến dùng được ở cả `subject` và `body_html`.
- Render bằng `html/template` của Go: giá trị biến được escape tự động. Phần văn bản thuần (plain-text) của email tự sinh từ `body_html` khi gửi.
- Validate khi lưu: (1) cú pháp mẫu hợp lệ; (2) chỉ dùng biến trong danh sách trên; (3) `body_html` **bắt buộc chứa `{{link}}`** — không có link thì Nhân viên không thể kích hoạt/đặt lại mật khẩu; (4) `body_html` không chứa `<script>`, `<iframe>`, thuộc tính sự kiện (`on*`) — lọc theo danh sách thẻ/thuộc tính cho phép.
- `{{link}}` trỏ về đúng giao diện của Nhân viên (Admin nội bộ hoặc Cổng Tổ chức khác, theo Tổ chức của Nhân viên nhận); base URL của từng giao diện là cấu hình triển khai (biến môi trường), không phải tham số trên màn hình.

### 4.5. [D-SD07-011] Tạm khoá đăng nhập

Chi tiết luồng ở D-SD02-004 (¶3.2) (dùng `identity.login_max_failed_attempts`, `identity.login_lockout_minutes`).

## 5. Thiết kế API

### 5.1. [D-SD07-012] Nhóm `shared/settings` — chỉ mount `admin`, role `quan_tri_he_thong`

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/shared/settings` | `shared.getSettings` | Toàn bộ tham số, nhóm theo `group` |
| PATCH | `/shared/settings` | `shared.updateSettings` | Sửa nhiều tham số một lần — body `{values: {"<key>": <value>, ...}}`; lưu nguyên khối hoặc từ chối cả khối (D-SD07-005 (¶3.2)) |
| DELETE | `/shared/settings/{key}` | `shared.resetSetting` | Khôi phục giá trị mặc định của một key |
| POST | `/shared/settings/email-templates/{template}/preview` | `shared.previewEmailTemplate` | `template ∈ {invite, password_reset}` — body `{subject, body_html}` (bản đang soạn, chưa lưu); trả `{subject, body_html, body_text}` đã render với dữ liệu mẫu, hoặc lỗi validate (D-SD07-010 (¶4.4)) |
| POST | `/shared/settings/email-templates/{template}/test` | `shared.testEmailTemplate` | Gửi thử bản đang soạn (body như trên) tới email của chính Quản trị hệ thống đang đăng nhập, dữ liệu mẫu, link giả không dùng được. Không ghi audit log (không thay đổi dữ liệu) |

Mỗi phần tử trong `shared.getSettings` — `GET /shared/settings`:

```json
{
  "key": "identity.invite_token_ttl_hours",
  "group": "identity",
  "type": "int",
  "value": 72,
  "default_value": 72,
  "is_default": true,
  "constraints": { "min": 1, "max": 720, "allowed_values": null, "nullable": false },
  "label": "string",
  "description": "string",
  "applies_to": "existing | new_only",
  "exposure": ["server", "admin_client"],
  "updated_by": { "id": "uuid", "display_name": "string" } | null,
  "updated_at": "timestamptz" | null
}
```

- `updated_by` ghép ở tầng handler (`/cmd/api`) bằng `identity.GetEmployeeSummaries` — cùng cách `shared.listAuditLogs` — `GET /shared/audit-logs`.
- `label`, `description`, `applies_to`, `exposure` lấy từ registry (D-SD07-001 (¶2.1)). Màn hình Cấu hình hiển thị `description` và `applies_to` cạnh từng tham số (R-CFG-003 (§2.8.2)).
- Lỗi validate (`PATCH`, `DELETE`): HTTP 422, `error_code = invalid_settings`, kèm `details: [{key, reason}]`.

### 5.2. [D-SD07-013] `GET /client-settings` — mount `admin`, `partner` và `public`

- operationId: `clientSettings.getSettings`.
- Kênh `admin` (yêu cầu JWT Nhân viên, mọi role): trả các key có exposure `admin_client`.
- Kênh `partner` (yêu cầu JWT Nhân viên, mọi role): trả các key có exposure `partner_client`.
- Kênh `public` (không xác thực): trả các key có exposure `public_client`.
- Response theo nhóm route (D-SD01-003 (¶3)):
  - `admin`, `partner`: `{"<key>": {value, label, description, applies_to}}` — `label`, `description`, `applies_to` lấy từ registry (D-SD07-001 (¶2.1)).
  - `public`: object phẳng `{"<key>": <value>, ...}`.
  - Cho phép cache ngắn phía trình duyệt/CDN (`Cache-Control: max-age=60`).
- Giao diện Nhân viên dùng endpoint này để hiển thị giá trị hiện hành của tham số tại nơi thao tác, bằng lời của từng màn hình (R-NFR-041 (§3.7.4)). Tham số nào hiển thị ở màn hình nào do tài liệu thiết kế của admin-web và partner-web xác định.

### 5.3. [D-SD07-014] Tổng hợp mount

| Endpoint | admin | partner | public |
|---|---|---|---|
| `/shared/settings/*` | ✓ (`quan_tri_he_thong`) | | |
| `clientSettings.getSettings` | ✓ | ✓ | ✓ |
| `auth.getPasswordPolicy` | ✓ | ✓ | |

## 6. Vấn đề mở / giả định

- Các nhóm tham số theo R-CFG-005 (§2.8.4). ⚠ Danh sách key cụ thể, giá trị mặc định và giới hạn là đề xuất của thiết kế (R-CFG-011 (§2.8.5)), điều chỉnh khi có số liệu thực tế. Riêng thời hạn access token/refresh token là tham số kỹ thuật, không nêu trong đặc tả.
- ⚠ **Rate limit bằng middleware Go, bộ đếm trong bộ nhớ** (D-SD07-009 (¶4.3)): chỉ đếm theo IP, mặc định tắt, người dùng chung một mạng dùng chung hạn mức — đúng R-NFR-008 (§3.1.6). Giới hạn tính theo từng bản `/cmd/api` là hệ quả kỹ thuật, cần chuyển bộ đếm sang Postgres hoặc Redis nếu mở rộng ngang.
- **Cho sửa toàn bộ mẫu email** có xem trước và gửi thử (R-CFG-008 (§2.8.4.3)). Rủi ro mẫu hiển thị lỗi trên một số trình đọc email được giảm thiểu bằng xem trước, gửi thử, và danh sách thẻ HTML cho phép (D-SD07-010 (¶4.4)).
- Không có lịch sử phiên bản cấu hình và không có "quay về giá trị trước" ngoài "Khôi phục mặc định" (R-CFG-003 (§2.8.2)); giá trị cũ tra cứu qua `audit_log` (`detail.old_value`).
- Tên tầng lưu trữ lạnh (`STORAGE_COLD_TIER`) và việc bucket Tư liệu gốc bật versioning là điều kiện hạ tầng, cần có trước khi dùng `operations.source_cold_storage_after_days`.
- **Mô tả tham số và lộ giá trị cho giao diện Nhân viên** (D-SD07-001 (¶2.1), D-SD07-003 (¶2.3), D-SD07-013 (¶5.2)) hiện thực R-CFG-003 (§2.8.2), R-NFR-041 (§3.7.4). ⚠ Phân loại `existing`/`new_only` của từng tham số và tập tham số lộ ra `admin_client`/`partner_client` là quyết định của thiết kế. `clientSettings.getSettings` ở `admin`/`partner` trả kèm `label`, `description`, `applies_to` để giao diện Nhân viên dùng khi hiển thị giá trị tại nơi thao tác.
