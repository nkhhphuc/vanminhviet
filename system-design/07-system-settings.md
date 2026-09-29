# Thiết Kế: Cấu Hình Hệ Thống (`/shared` — system settings)

## 1. Tổng quan

- Cho phép Nhân viên giữ role `quan_tri_he_thong` điều chỉnh các tham số vận hành và nghiệp vụ của hệ thống qua Admin nội bộ, không cần lập trình viên sửa code hay deploy lại.
- Cơ sở đặc tả: R-CFG-001 (§2.8) (Cấu hình hệ thống — chỉ Quản trị hệ thống, sửa và khôi phục mặc định từng tham số, có hiệu lực không cần triển khai lại, mọi thay đổi ghi audit log); R-KB-077 (§2.2.6.5) (kích hoạt AI Verification tự động/thủ công theo cấu hình); R-ID-022 (§2.1.5.5), R-ID-029 (§2.1.5.8), R-ID-030 (§2.1.5.9) (thời hạn đường dẫn, chính sách mật khẩu, tạm khoá đăng nhập); R-AI-007 (§2.4.6)–R-AI-010 (§2.4.9) (tham số AI Văn Minh Việt, thời hạn lưu nhật ký hỏi đáp); R-NFR-004 (§3.1.2) (thời hạn lưu audit log); R-NFR-008 (§3.1.6) (rate limit Trợ lý AI công khai). Danh sách tham số cụ thể, giá trị mặc định và giới hạn là quyết định của thiết kế (R-CFG-011 (§2.8.5)).
- Thuộc package `/shared` (cùng nhóm với `audit_log`, `usage_event`, API job nền — D-SD01-002 (¶2)): cấu hình dùng chung cho mọi module, không thuộc riêng module nghiệp vụ nào. Các package khác chỉ **đọc** qua hàm nội bộ của `/shared`, không chạm bảng.
- **Ngoài phạm vi** — không đưa lên giao diện, giữ ở biến môi trường/secret lúc triển khai: `AI_GATEWAY_MODE`, đường dẫn model, mọi shared secret (AI Gateway, webhook MinIO/S3), thông tin truy cập MinIO/S3 và SMTP/SES, allowlist CORS, thông tin tài khoản Quản trị hệ thống đầu tiên (D-SD02-002 (¶3.0)), prompt hệ thống của AI Gateway (quản lý theo phiên bản trong code, D-SD06-011 (¶5)), tham số chunking (`05` ¶6). Nội dung hiển thị trang chủ Web công khai (banner, mục nổi bật...) là nội dung của web, không thuộc cấu hình hệ thống.

## 2. Mô hình dữ liệu

### 2.1. [D-SD07-001] Danh mục tham số (registry) — khai báo trong code

Mỗi tham số được **khai báo trong code Go** (registry trong `/shared`), không phải dữ liệu seed: `key`, `group`, kiểu giá trị, giá trị mặc định, ràng buộc (min/max, tập giá trị hợp lệ, định dạng), phạm vi lộ ra client (`exposure`), cách áp dụng (`apply_note`). Thêm tham số mới = thêm khai báo trong code + deploy; không cần migration dữ liệu.

`exposure`:
- `server` — chỉ backend đọc (mặc định).
- `admin_client` — trả thêm cho frontend Admin nội bộ qua `GET /client-settings` (D-SD07-013 (¶5.2)) — mọi Nhân viên đã đăng nhập ở kênh `admin`.
- `public_client` — trả thêm cho Web công khai qua `GET /client-settings` ở kênh `public` (không xác thực). Một tham số có thể thuộc cả `admin_client` và `public_client`.

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

Ký hiệu cột **Áp dụng**: *Ngay* = có hiệu lực cho thao tác tiếp theo sau khi lưu (D-SD07-008 (¶4.2)); ghi chú riêng nếu chỉ áp dụng cho bản ghi phát sinh sau đó.

**Nhóm `ai_verification` — AI Verification (R-KB-077 (§2.2.6.5))**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng |
|---|---|---|---|---|
| `ai_verification.trigger_mode` | text | `auto` | `auto` / `manual` | Ngay — chỉ ảnh hưởng các lần `submit-for-review` sau khi lưu (D-SD07-004 (¶3.1)) |
| `ai_verification.manual_trigger_roles` | text[] | `["nghien_cuu", "xet_duyet"]` | Tập con của `nghien_cuu`, `xet_duyet`, `chu_nhiem_de_tai`, `quan_tri_he_thong`; **không được rỗng khi `trigger_mode = manual`** | Ngay |

**Nhóm `identity` — Tài khoản & bảo mật (module 02)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng |
|---|---|---|---|---|
| `identity.invite_token_ttl_hours` | int | 72 | 1–720 | Token mời sinh sau khi lưu (R-ID-022 (§2.1.5.5)) |
| `identity.password_reset_token_ttl_minutes` | int | 60 | 10–1440 | Token đặt lại sinh sau khi lưu (R-ID-022 (§2.1.5.5)) |
| `identity.access_token_ttl_minutes` | int | 15 | 5–120 | Access token cấp sau khi lưu |
| `identity.refresh_token_ttl_days` | int | 7 | 1–90 | Refresh token cấp sau khi lưu |
| `identity.password_min_length` | int | 8 | 8–64 | Mật khẩu đặt mới sau khi lưu — không buộc đổi mật khẩu hiện có |
| `identity.password_require_letter_and_digit` | bool | `true` | | như trên |
| `identity.password_require_special_char` | bool | `false` | | như trên |
| `identity.login_max_failed_attempts` | int | 5 | 0–20; `0` = tắt cơ chế tạm khoá | Ngay |
| `identity.login_lockout_minutes` | int | 15 | 1–1440 | Các lần tạm khoá phát sinh sau khi lưu |

**Nhóm `email` — Email hệ thống (mời, đặt lại mật khẩu)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng |
|---|---|---|---|---|
| `email.sender_name` | text | `Văn Minh Việt` | 1–100 ký tự | Ngay |
| `email.sender_address` | text | Giá trị biến môi trường `EMAIL_DEFAULT_SENDER` | Định dạng email; **tên miền phải thuộc** `EMAIL_ALLOWED_SENDER_DOMAINS` (biến môi trường — các tên miền đã xác minh gửi trên Amazon SES) | Ngay |
| `email.template.invite` | object `{subject, body_html}` | Mẫu mặc định trong code | Xem D-SD07-010 (¶4.4) | Email gửi sau khi lưu |
| `email.template.password_reset` | object `{subject, body_html}` | Mẫu mặc định trong code | Xem D-SD07-010 (¶4.4) | Email gửi sau khi lưu |

**Nhóm `assistant` — AI Văn Minh Việt (module 05)**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Exposure |
|---|---|---|---|---|---|
| `assistant.retrieve_top_k` | int | 8 | 1–30 | Ngay | server |
| `assistant.history_turns` | int | 6 | 0–20; `0` = không dùng lịch sử (mỗi lượt hỏi độc lập, bỏ qua Rewrite) | Ngay | server |
| `assistant.rewrite_query_enabled` | bool | `true` | | Ngay | server |
| `assistant.conversation_ttl_hours` | int | 6 | 1–168 | Ngay (client đọc khi tải trang) | admin_client, public_client |
| `assistant.no_context_answer` | text | `Xin lỗi, Bách khoa Văn Minh Việt hiện chưa có thông tin về nội dung này.` | 1–500 ký tự | Ngay | server |
| `assistant.disclaimer_text` | text | `Câu trả lời do AI tạo ra dựa trên Bách khoa Văn Minh Việt và có thể chưa chính xác. Vui lòng đối chiếu với các Mục từ nguồn.` | 0–500 ký tự; rỗng = không hiển thị | Ngay (client đọc khi tải trang) | admin_client, public_client |
| `assistant.query_log_retention_days` | int | 180 | 30–3650 | Lần dọn kế tiếp (D-SD07-009 (¶4.3)) | server |
| `assistant.public_rate_limit_enabled` | bool | `false` | | Ngay | server |
| `assistant.public_rate_limit_max_requests` | int | 20 | 1–1000 | Ngay | server |
| `assistant.public_rate_limit_window_seconds` | int | 60 | 10–86400 | Ngay | server |

**Nhóm `operations` — Vận hành**

| Key | Kiểu | Mặc định | Ràng buộc | Áp dụng | Exposure |
|---|---|---|---|---|---|
| `operations.source_sync_debounce_seconds` | int | 45 | 10–600 | Sự kiện webhook nhận và job hoãn sau khi lưu | server |
| `operations.job_retention_completed_hours` | int | 24 | 1–2160 | Lần dọn dẹp kế tiếp (D-SD07-009 (¶4.3)) | server |
| `operations.job_retention_cancelled_hours` | int | 24 | 1–2160 | như trên | server |
| `operations.job_retention_discarded_hours` | int | 168 | 1–2160 | như trên | server |
| `operations.audit_log_retention_months` | int | 24 | 12–120 (R-NFR-004 (§3.1.2): không dưới 12 tháng) | Lần dọn kế tiếp (D-SD07-009 (¶4.3)) | server |
| `operations.source_cold_storage_after_days` | int, nullable | `null` | `null` (không chuyển) hoặc 30–3650 | Khi lưu, enqueue job áp quy tắc lifecycle lên bucket (D-SD07-009 (¶4.3)) | server |
| `operations.admin_polling_interval_seconds` | int | 30 | 10–300 | Client đọc khi tải trang — màn hình Nhật ký hoạt động, Theo dõi job nền | admin_client |

## 3. Luồng nghiệp vụ

### 3.1. [D-SD07-004] Kích hoạt AI Verification theo cấu hình (R-KB-077 (§2.2.6.5))

- `trigger_mode = auto`: `submit-for-review` chuyển `dang_nghien_cuu → cho_xet_duyet` rồi kích hoạt AI Verification ngay trong cùng transaction (`cho_xet_duyet → dang_xet_duyet_ai`, enqueue `verification.run`) — D-SD03-018 (¶4.3).
- `trigger_mode = manual`: `submit-for-review` chỉ chuyển sang `cho_xet_duyet` và dừng ở đó. Hạng mục chờ tới khi một Nhân viên được phép gọi `trigger-ai-verification`.
- Quyền kích hoạt thủ công (áp dụng ở **cả 2 chế độ** — ở chế độ `auto` là kích hoạt lại): Nhân viên giữ ít nhất một role trong `manual_trigger_roles`. Role theo phạm vi (`nghien_cuu`, `xet_duyet`, `chu_nhiem_de_tai`) chỉ tính khi gắn với **đúng Đề tài nghiên cứu cha** của hạng mục. `quan_tri_he_thong` là role theo chức năng, chỉ có ở kênh `admin`.
- Đổi chế độ không tự xử lý lại các hạng mục đang có: hạng mục đang ở `cho_xet_duyet` khi chuyển `manual → auto` vẫn phải kích hoạt thủ công. Màn hình cấu hình hiển thị cảnh báo này khi đổi chế độ.

### 3.2. [D-SD07-005] Sửa cấu hình

1. Quản trị hệ thống mở màn hình Cấu hình, sửa một hoặc nhiều tham số trong một nhóm, bấm Lưu → `PATCH /shared/settings` (D-SD07-012 (¶5.1)).
2. Backend validate từng key theo registry, sau đó validate ràng buộc liên key (ví dụ `manual_trigger_roles` không rỗng khi `trigger_mode = manual` — kiểm trên giá trị **sau khi** áp toàn bộ thay đổi của request). Có lỗi → từ chối cả request (không lưu một phần), trả lỗi theo từng key.
3. Hợp lệ → trong **một transaction**: upsert các dòng `system_setting` (giá trị trùng mặc định thì xoá dòng thay vì upsert); ghi một dòng `audit_log` cho mỗi key thay đổi (D-SD07-006 (¶3.3)); gửi `NOTIFY system_setting_changed` (D-SD07-008 (¶4.2)).
4. "Khôi phục mặc định" một key → `DELETE /shared/settings/{key}`, cùng cơ chế validate liên key, audit và NOTIFY như trên.

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
- **Rate limit Chat AI công khai (`assistant.public_rate_limit_*`)**: middleware Go gắn trên route `POST /api/v1/public/assistant/chat` (D-SD05-012 (¶5.1)). Đếm theo IP client lấy từ header `X-Forwarded-For` do Traefik gắn (chỉ tin header khi request đến từ Traefik). Thuật toán cửa sổ cố định, lưu bộ đếm trong bộ nhớ tiến trình. ⚠ Nếu chạy nhiều bản `/cmd/api` song song, giới hạn tính riêng cho từng bản — chấp nhận ở quy mô hiện tại (D-SD01-008 (¶8)); cần chuyển bộ đếm sang Postgres hoặc Redis nếu mở rộng ngang. Vượt ngưỡng → HTTP 429 với lỗi `rate_limited` (quy ước lỗi chung D-SD01-003 (¶3)), kèm header `Retry-After`; không ghi `assistant_query_log`.

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

| Method | Path | Mô tả |
|---|---|---|
| GET | `/shared/settings` | Toàn bộ tham số, nhóm theo `group` |
| PATCH | `/shared/settings` | Sửa nhiều tham số một lần — body `{values: {"<key>": <value>, ...}}`; lưu nguyên khối hoặc từ chối cả khối (D-SD07-005 (¶3.2)) |
| DELETE | `/shared/settings/{key}` | Khôi phục giá trị mặc định của một key |
| POST | `/shared/settings/email-templates/{template}/preview` | `template ∈ {invite, password_reset}` — body `{subject, body_html}` (bản đang soạn, chưa lưu); trả `{subject, body_html, body_text}` đã render với dữ liệu mẫu, hoặc lỗi validate (D-SD07-010 (¶4.4)) |
| POST | `/shared/settings/email-templates/{template}/test` | Gửi thử bản đang soạn (body như trên) tới email của chính Quản trị hệ thống đang đăng nhập, dữ liệu mẫu, link giả không dùng được. Không ghi audit log (không thay đổi dữ liệu) |

Mỗi phần tử trong `GET /shared/settings`:

```json
{
  "key": "identity.invite_token_ttl_hours",
  "group": "identity",
  "type": "int",
  "value": 72,
  "default_value": 72,
  "is_default": true,
  "constraints": { "min": 1, "max": 720, "allowed_values": null, "nullable": false },
  "apply_note": "string",
  "updated_by": { "id": "uuid", "display_name": "string" } | null,
  "updated_at": "timestamptz" | null
}
```

- `updated_by` ghép ở tầng handler (`/cmd/api`) bằng `identity.GetEmployeeSummaries` — cùng cách `GET /shared/audit-logs` (D-SD01-002 (¶2)).
- Nhãn hiển thị tiếng Việt và mô tả của từng tham số do frontend quản lý (theo `key`), không trả từ API.
- Lỗi validate (`PATCH`, `DELETE`): HTTP 422, `error_code = invalid_settings`, kèm `details: [{key, reason}]`.

### 5.2. [D-SD07-013] `GET /client-settings` — mount `admin` và `public`

- Kênh `admin` (yêu cầu JWT Nhân viên, mọi role): trả các key có exposure `admin_client`.
- Kênh `public` (không xác thực): trả các key có exposure `public_client`.
- Response: object phẳng `{"<key>": <value>, ...}`. Cho phép cache ngắn phía trình duyệt/CDN (`Cache-Control: max-age=60`).
- Không mount ở `partner` — hiện chưa có tham số nào Cổng Tổ chức khác cần đọc.

### 5.3. [D-SD07-014] Tổng hợp mount

| Endpoint | admin | partner | public |
|---|---|---|---|
| `/shared/settings/*` | ✓ (`quan_tri_he_thong`) | | |
| `GET /client-settings` | ✓ | | ✓ |
| `GET /auth/password-policy` (D-SD02-009 (¶5.1)) | ✓ | ✓ | |

## 6. Vấn đề mở / giả định

- Các nhóm tham số theo R-CFG-005 (§2.8.4). ⚠ Danh sách key cụ thể, giá trị mặc định và giới hạn là đề xuất của thiết kế (R-CFG-011 (§2.8.5)), điều chỉnh khi có số liệu thực tế. Riêng thời hạn access token/refresh token là tham số kỹ thuật, không nêu trong đặc tả.
- ⚠ **Rate limit bằng middleware Go, bộ đếm trong bộ nhớ** (D-SD07-009 (¶4.3)): chỉ đếm theo IP, mặc định tắt, người dùng chung một mạng dùng chung hạn mức — đúng R-NFR-008 (§3.1.6). Giới hạn tính theo từng bản `/cmd/api` là hệ quả kỹ thuật, cần chuyển bộ đếm sang Postgres hoặc Redis nếu mở rộng ngang.
- **Cho sửa toàn bộ mẫu email** có xem trước và gửi thử (R-CFG-008 (§2.8.4.3)). Rủi ro mẫu hiển thị lỗi trên một số trình đọc email được giảm thiểu bằng xem trước, gửi thử, và danh sách thẻ HTML cho phép (D-SD07-010 (¶4.4)).
- Không có lịch sử phiên bản cấu hình và không có "quay về giá trị trước" ngoài "Khôi phục mặc định" (R-CFG-003 (§2.8.2)); giá trị cũ tra cứu qua `audit_log` (`detail.old_value`).
- Tên tầng lưu trữ lạnh (`STORAGE_COLD_TIER`) và việc bucket Tư liệu gốc bật versioning là điều kiện hạ tầng, cần có trước khi dùng `operations.source_cold_storage_after_days`.
