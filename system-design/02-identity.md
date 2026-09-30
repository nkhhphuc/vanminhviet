# Thiết Kế Module — Quản Lý Người Dùng (`/identity`)

> Trạng thái: ¶1–5 đã chốt: mô hình dữ liệu, cơ chế xác thực (R-ID-016 (§2.1.5) đặc tả gốc), các luồng nghiệp vụ chính (¶3), interface nội bộ tổng quát cho role theo phạm vi (D-SD02-008 (¶4)), và thiết kế API (¶5). ¶6 (Vấn đề mở) tiếp tục cập nhật khi có thay đổi.

## 1. Tổng quan module

Module Quản Lý Người Dùng (R-ID-001 (§2.1) đặc tả gốc) là nền tảng Nhân viên/Tổ chức/Role mà mọi module nghiệp vụ khác (03, 04, 05) phụ thuộc vào để xác thực và phân quyền. Không có phụ thuộc ngược lại — đây là module nền, build đầu tiên sau kiến trúc chung (`01`).

Phạm vi: quản lý Nhân viên (R-ID-002 (§2.1.1)–R-ID-005 (§2.1.3.1)), Tổ chức (R-ID-009 (§2.1.4)), và hai loại role — role theo chức năng và role theo phạm vi (R-ID-006 (§2.1.3.1.1)–R-ID-007 (§2.1.3.1.2)) — cùng cơ chế gán role. Không bao gồm: Người dùng công khai (R-ID-008 (§2.1.3.2), không có tài khoản/định danh nào ở giai đoạn này, không cần bảng riêng).

## 2. [D-SD02-001] Mô hình dữ liệu

**`organization`** (R-ID-009 (§2.1.4))

- `id` (UUID)
- `name` — tên tổ chức (R-ID-011 (§2.1.4.2))
- `address` (R-ID-012 (§2.1.4.3))
- `contact_email`, `contact_phone` (R-ID-013 (§2.1.4.4))
- `created_at`

Văn Minh Việt là một Tổ chức bình thường trong bảng này, không phải trường hợp đặc biệt (R-ID-014 (§2.1.4.5)).

**`employee`** (R-ID-002 (§2.1.1)–R-ID-003 (§2.1.2))

- `id` (UUID, tự sinh — R-ID-002 (§2.1.1))
- `email` (R-ID-003 (§2.1.2), duy nhất — dùng làm định danh đăng nhập, R-ID-017 (§2.1.5.1))
- `phone` (R-ID-003 (§2.1.2))
- `display_name` — tên gọi (R-ID-003 (§2.1.2))
- `organization_id` → `organization.id`, NOT NULL (mỗi Nhân viên thuộc đúng một Tổ chức — R-ID-014 (§2.1.4.5))
- `password_hash` — lưu mật khẩu đã hash, không lưu bản rõ (R-ID-017 (§2.1.5.1) đặc tả gốc: đăng nhập bằng email + mật khẩu; hash là thực hành kỹ thuật chuẩn khi lưu mật khẩu, không phải điểm cần đặc tả riêng)
- `status` — `invited` / `active` / `disabled`: Nhân viên ở trạng thái `invited` cho tới khi tự đặt mật khẩu lần đầu qua email mời thì chuyển `active` (R-ID-018 (§2.1.5.2)–R-ID-020 (§2.1.5.3) đặc tả gốc: tài khoản chỉ do Quản trị hệ thống tạo, kích hoạt sau khi hoàn tất đặt mật khẩu qua link mời)
- `failed_login_count` — int, mặc định 0. Số lần nhập sai mật khẩu liên tiếp, gồm cả lúc đăng nhập (D-SD02-004 (¶3.2)) và lúc đổi mật khẩu (D-SD02-006 (¶3.4)) — tạm khoá đăng nhập R-ID-030 (§2.1.5.9), R-ID-036 (§2.1.5.10.1)
- `locked_until` — timestamptz, nullable. Tạm khoá đăng nhập tới thời điểm này (R-ID-030 (§2.1.5.9)); khác `status = disabled` (vô hiệu hoá bởi Quản trị hệ thống, không tự hết hạn — R-ID-024 (§2.1.5.7), R-ID-033 (§2.1.5.9.3))
- `sessions_invalidated_at` — timestamptz, nullable. ⚠ Mốc vô hiệu hoá phiên: mọi access token có thời điểm cấp (`iat`) trước mốc này bị từ chối ngay (D-SD02-007 (¶3.5)). Đặt khi vô hiệu hoá tài khoản, đặt lại mật khẩu, đổi mật khẩu, hoặc bị tạm khoá trong lúc đổi mật khẩu
- `created_at`, `updated_at`

**`roles`** (R-ID-006 (§2.1.3.1.1)–R-ID-007 (§2.1.3.1.2)) — một bảng chung cho cả 2 loại role, theo nguyên tắc ở `00-claude-instructions.md` mục 6:

- `id` (UUID)
- `name` — tên role, ví dụ `nhap_lieu`, `xuat_ban`, `xuat_ban_muc_tu`, `bien_tap`, `xet_duyet_muc_tu`, `van_hanh`, `quan_tri_he_thong` (role theo chức năng — R-KB-069 (§2.2.5.1), R-KB-072 (§2.2.5.4), R-ENC-021 (§2.3.4.2), R-ENC-020 (§2.3.4.1), R-ENC-025 (§2.3.5.3), và các role vận hành/quản trị theo R-ID-006 (§2.1.3.1.1)); hoặc `chu_nhiem_de_tai`, `nghien_cuu`, `xet_duyet` (role theo phạm vi — R-KB-073 (§2.2.5.5), R-KB-070 (§2.2.5.2), R-KB-071 (§2.2.5.3))
- `scope_type` — phân loại phạm vi: `function` (role theo chức năng, không gắn phạm vi dữ liệu) hoặc `research_topic` (role theo phạm vi, gắn một Đề tài nghiên cứu cụ thể); để mở rộng cho phạm vi khác sau này (ví dụ Cương vực) theo đúng tinh thần "chưa đầy đủ" của R-ID-007 (§2.1.3.1.2)
- `scope_id` — nullable; NULL khi `scope_type = 'function'`; trỏ tới `research_topic.id` khi `scope_type = 'research_topic'` (bảng `research_topic` thuộc module 03, tham chiếu chéo module — chấp nhận được vì đây là khoá ngoại đơn thuần, không phải JOIN nghiệp vụ)
- `is_singular` — boolean, NOT NULL, default `false` — ⚠ Bổ sung: `true` cho role theo phạm vi mà tại một thời điểm chỉ đúng một Nhân viên được giữ trong cùng phạm vi (hiện tại: `chu_nhiem_de_tai`, R-KB-073 (§2.2.5.5)); `false` cho các role còn lại, kể cả role theo chức năng (không giới hạn số người giữ). Giá trị này do **module định nghĩa role đó** (ví dụ `/knowledge` cho role theo Đề tài nghiên cứu) quyết định và truyền tường minh khi tạo role qua `ProvisionScopeRoles` (D-SD02-008 (¶4)) — `/identity` không giữ bảng ánh xạ tên role → `is_singular` nào, chỉ lưu lại đúng giá trị đã nhận. Nhờ vậy `AssignScopeRole` (D-SD02-008 (¶4)) tự động áp dụng đúng ngữ nghĩa "thay thế" (singular) hay "thêm vào" (không singular) mà không cần biết hay hard-code theo tên role.
- `created_at`

⚠ Lưu ý đặt tên: có **2 cặp role dễ nhầm** vì cùng tên nghiệp vụ nhưng khác hẳn phạm vi — `xet_duyet_muc_tu` (Xét duyệt Mục từ, R-ENC-025 (§2.3.5.3)) vs. `xet_duyet` (Xét duyệt Hạng mục tri thức theo đề tài, R-KB-071 (§2.2.5.3)); và `xuat_ban_muc_tu` (quyết định bắt buộc Xuất bản/Không xuất bản tại "Đạt xét duyệt" + chọn phiên bản đang công khai của Mục từ, R-ENC-021 (§2.3.4.2)) vs. `xuat_ban` (quyết định bắt buộc Xuất bản/Không xuất bản tại "Đạt xét duyệt" + chọn phiên bản đang dùng của Hạng mục tri thức, R-KB-072 (§2.2.5.4)) — đây là 2 role **khác nhau**, không gộp chung, vì làm việc trên 2 entity khác nhau (Mục từ vs. Hạng mục tri thức). Đặc tả gốc nhấn mạnh cả hai sự phân biệt này — đặt tên code khác nhau rõ ràng khi implement.

Các role theo chức năng là dữ liệu khởi tạo sẵn (seed data, tạo 1 lần khi triển khai), không tự sinh theo sự kiện nào. Các role theo phạm vi (`chu_nhiem_de_tai`, `nghien_cuu`, `xet_duyet`) được `/knowledge` (module 03) tự động tạo và **tự quyết định** `is_singular` cho từng role — 3 dòng mới trong bảng này (`chu_nhiem_de_tai` có `is_singular = true`, `nghien_cuu`/`xet_duyet` có `is_singular = false`) — mỗi khi một Đề tài nghiên cứu được tạo (R-KB-006 (§2.2.1.4)), truyền tường minh qua interface nội bộ tổng quát của `/identity` (chi tiết kỹ thuật ở D-SD02-008 (¶4), xem `ScopeRoleSpec`).

**`employee_role`** (bảng nối nhiều-nhiều, R-ID-005 (§2.1.3.1): "một Nhân viên có thể giữ nhiều role cùng lúc")

- `employee_id` → `employee.id`
- `role_id` → `roles.id`, khoá ngoại có `ON DELETE CASCADE` (xem D-SD02-008 (¶4)) — khi một role bị xoá (ví dụ role theo phạm vi khi Đề tài nghiên cứu bị xoá), các dòng `employee_role` liên quan tự động bị xoá theo
- `assigned_at`
- Khoá chính kép `(employee_id, role_id)`

Quy tắc ai được gán role theo phạm vi cho Nhân viên khác — logic nghiệp vụ ở tầng API/service, không phải ràng buộc CSDL:

- `chu_nhiem_de_tai`: chỉ Nhân viên giữ role `quan_tri_he_thong` (R-KB-006 (§2.2.1.4), R-KB-073 (§2.2.5.5), R-GEN-011 (§1.2.3.3)) — thực hiện qua endpoint `set-chair` ở `/knowledge` (D-SD03-021 (¶5.1) ), gọi `AssignScopeRole` (D-SD02-008 (¶4)) bên dưới.
- `nghien_cuu`/`xet_duyet`: Nhân viên giữ role `quan_tri_he_thong`, **hoặc** Nhân viên đang giữ `chu_nhiem_de_tai` của đúng đề tài đó (R-KB-073 (§2.2.5.5)) — thực hiện qua các endpoint riêng ở `/knowledge` (D-SD03-021 (¶5.1) : `researchers`/`reviewers`), không qua nhóm `identity/*` (D-SD02-010 (¶5.2) dưới đây — nhóm này chỉ mount ở `admin` theo R-PTN-010 (§2.7.4), Chủ nhiệm đề tài thuộc Tổ chức khác không vào được).
- Nhóm `identity/*` (`POST/DELETE /identity/employees/{id}/roles`, D-SD02-010 (¶5.2)) vẫn giữ nguyên: chỉ `quan_tri_he_thong` gọi được, dùng cho mọi role còn lại (role theo chức năng) và như một lối tắt quản trị chung cho role theo phạm vi khi cần.

**`employee_credential_token`** (hiện thực R-ID-020 (§2.1.5.3)–R-ID-022 (§2.1.5.5) đặc tả gốc: email mời đặt mật khẩu lần đầu, đặt lại mật khẩu qua cùng cơ chế, link có thời hạn và chỉ dùng một lần):

- `id` (UUID)
- `employee_id` → `employee.id`
- `token_hash` — hash của token gửi qua email, không lưu token thô
- `type` — `invite` (R-ID-020 (§2.1.5.3)) / `password_reset` (R-ID-021 (§2.1.5.4))
- `expires_at` — tính lúc sinh token theo tham số cấu hình: `identity.invite_token_ttl_hours` (mặc định 72 giờ) cho `invite`, `identity.password_reset_token_ttl_minutes` (mặc định 60 phút) cho `password_reset` — `07-system-settings.md` (R-ID-022 (§2.1.5.5) đặc tả gốc chỉ yêu cầu có thời hạn, không cố định con số)
- `used_at` — nullable, đánh dấu đã dùng để đảm bảo chỉ dùng được một lần (R-ID-022 (§2.1.5.5))
- `created_at`

**`refresh_token`** — ⚠ Đề xuất bổ sung (hiện thực cơ chế JWT + refresh token đã chốt ở D-SD01-007 (¶7), tài liệu đó chưa có bảng cụ thể):

- `id` (UUID)
- `employee_id` → `employee.id`
- `token_hash`
- `expires_at` — theo `identity.refresh_token_ttl_days` (mặc định 7 ngày, `07-system-settings.md`)
- `revoked_at` — nullable, phục vụ đăng xuất/thu hồi
- `created_at`

## 3. Luồng trạng thái / nghiệp vụ

### 3.0 [D-SD02-002] Khởi tạo tài khoản Quản trị hệ thống đầu tiên (bootstrap)

Hiện thực R-ID-019 (§2.1.5.2.1): tài khoản Quản trị hệ thống đầu tiên được tạo trong quá trình triển khai, thuộc Tổ chức Văn Minh Việt, dùng được ngay không qua email mời.

1. Một seed/migration chạy khi triển khai một môi trường mới — cùng cơ chế "seed data" đã dùng cho role theo chức năng (D-SD02-001 (¶2)) — đọc `email`, `password` (bản rõ, băm lúc chạy seed bằng cùng cơ chế hash dùng cho `employee.password_hash`), `display_name` từ biến môi trường/file cấu hình lúc chạy migration. Không hard-code giá trị mặc định trong code, tránh cùng một tài khoản/mật khẩu cố định lặp lại giữa các môi trường.
2. Seed kiểm tra Tổ chức "Văn Minh Việt" theo `name` đã tồn tại chưa — nếu chưa, tạo mới; nếu đã có (lần deploy sau, hoặc đã tạo tay), dùng lại `id` hiện có. Tài khoản Quản trị hệ thống đầu tiên thuộc Tổ chức này (R-ID-014 (§2.1.4.5): mọi Nhân viên thuộc đúng một Tổ chức).
3. Seed kiểm tra tồn tại `employee` theo `email` seed (email vốn unique — D-SD02-001 (¶2)) — nếu đã tồn tại thì bỏ qua, không tạo trùng hoặc ghi đè mật khẩu. Nhờ vậy an toàn khi chạy lại migration nhiều lần hoặc redeploy cùng môi trường (idempotent).
4. Nếu chưa tồn tại: insert `employee` với `status = active` ngay (bỏ qua luồng mời qua email ở D-SD02-003 (¶3.1) — không áp dụng được cho tài khoản đầu tiên vì chưa có ai để gửi lời mời), `password_hash` từ bước 1; gán role `quan_tri_he_thong` (đã có sẵn từ seed role theo chức năng, D-SD02-001 (¶2)) qua `employee_role`.
5. Không ghi `audit_log` cho bước này — audit log ghi nhận hành động của một Nhân viên đã xác thực (D-SD01-003 (¶3)); đây là thao tác vận hành hạ tầng trước khi hệ thống có Nhân viên nào, không có `employee_id` hợp lệ để gán làm actor.
6. Sau khi có tài khoản Quản trị hệ thống đầu tiên, mọi tài khoản tiếp theo tạo qua luồng bình thường (D-SD02-003 (¶3.1), `identity.createEmployee` — `POST /identity/employees`) — bootstrap này chỉ tạo đúng 1 Nhân viên Quản trị hệ thống đầu tiên cho cả hệ thống, không lặp lại cho mỗi Tổ chức mới.

### 3.1 [D-SD02-003] Luồng mời & kích hoạt tài khoản (R-ID-018 (§2.1.5.2)–R-ID-020 (§2.1.5.3))

1. Quản trị hệ thống tạo Nhân viên mới (nhập `email`, `display_name`, `phone`, `organization_id`, gán role ban đầu) → tạo bản ghi `employee` với `status = invited`, `password_hash` để trống cho tới khi kích hoạt (R-ID-018 (§2.1.5.2) đặc tả gốc: tài khoản chỉ do Quản trị hệ thống tạo).
2. Hệ thống sinh một token ngẫu nhiên, lưu vào `employee_credential_token` (`type = invite`, `token_hash` — hash của token, `expires_at`), gửi email mời chứa link kèm token thô (chỉ gửi qua email, không lưu bản rõ ở DB) — dùng cơ chế gửi email dùng chung ở `/shared` (D-SD01-002 (¶2)). Nội dung email render từ mẫu cấu hình được `email.template.invite` / `email.template.password_reset`, người gửi theo `email.sender_*` (D-SD07-010 (¶4.4)).
3. Nhân viên mở link → hệ thống xác thực token (đúng hash, chưa hết hạn theo `expires_at`, chưa `used_at`) → hiển thị màn hình đặt mật khẩu lần đầu.
4. Khi Nhân viên submit mật khẩu: hash mật khẩu mới → ghi vào `employee.password_hash`, chuyển `employee.status` → `active`, đánh dấu `used_at = now()` trên token vừa dùng (R-ID-020 (§2.1.5.3) đặc tả gốc: kích hoạt sau khi hoàn tất đặt mật khẩu). Mật khẩu mới phải thoả chính sách mật khẩu đang cấu hình (`identity.password_*`, `07-system-settings.md`); không thoả → từ chối, trả lỗi `password_policy_violation` kèm các điều kiện chưa đạt.
5. Token sai/hết hạn/đã dùng → báo lỗi, hướng dẫn liên hệ Quản trị hệ thống gửi lại lời mời.
6. ⚠ Gửi lại lời mời (Quản trị hệ thống bấm "gửi lại"): sinh token `invite` mới cho employee đó, đồng thời đánh dấu `used_at = now()` trên các token `invite` cũ chưa dùng của employee này để vô hiệu hoá — tránh tình trạng nhiều link mời cùng hợp lệ một lúc. Đây là quyết định kỹ thuật của thiết kế, không phải yêu cầu từ đặc tả gốc.

### 3.2 [D-SD02-004] Luồng đăng nhập (R-ID-017 (§2.1.5.1))

1. Nhân viên nhập `email` + mật khẩu tại form đăng nhập (Admin nội bộ hoặc Cổng Nhân viên Tổ chức khác — D-SD01-001 (¶1)).
2. Hệ thống tìm `employee` theo `email`; kiểm tra `status`:
   - `invited` → chưa kích hoạt, báo cần hoàn tất đặt mật khẩu qua email mời (không cho đăng nhập).
   - `disabled` → tài khoản đã bị khoá, báo liên hệ Quản trị hệ thống.
   - `active` → tiếp tục bước 2a.

   2a. Tạm khoá đăng nhập (R-ID-031 (§2.1.5.9.1)): nếu `locked_until > now()` → từ chối, báo tài khoản đang tạm khoá do đăng nhập sai nhiều lần, thử lại sau thời điểm `locked_until` (không so khớp mật khẩu).
3. So khớp mật khẩu nhập vào với `password_hash`.
   - Sai: tăng `failed_login_count`. Nếu `identity.login_max_failed_attempts > 0` và `failed_login_count` đạt ngưỡng này → đặt `locked_until = now() + identity.login_lockout_minutes`, đặt lại `failed_login_count = 0`, gọi `shared.RecordAudit` ghi sự kiện `auth.login_locked` với actor là hệ thống (`actor_type = system`, `entity_type = employee`) trong cùng transaction cập nhật bộ đếm (D-SD01-002 (¶2)).
   - Đúng: đặt lại `failed_login_count = 0`, `locked_until = NULL`.
   - Chỉ đếm sai cho `employee` tồn tại và đang `active`; email không tồn tại không đếm (không có bản ghi để đếm).
4. ⚠ Nếu email không tồn tại, hoặc `status` không hợp lệ, hoặc sai mật khẩu — trả về cùng một thông báo lỗi chung ("Email hoặc mật khẩu không đúng"), không phân biệt rõ lý do — thực hành bảo mật chuẩn để tránh lộ thông tin email nào đã có tài khoản trong hệ thống. Đây là bổ sung của thiết kế, không phải yêu cầu đặc tả gốc.
5. Đăng nhập thành công: sinh access token JWT (ngắn hạn) + refresh token (dài hạn, lưu `token_hash` vào bảng `refresh_token` — D-SD01-007 (¶7)), trả về client. Ngay sau khi xử lý xong, gọi `shared.RecordAudit` ghi nhận sự kiện đăng nhập (`employee_id`, thời điểm) — theo phạm vi audit log đã chốt ở D-SD01-002 (¶2) (R-NFR-004 (§3.1.2) đặc tả gốc); đây là **ngoại lệ duy nhất** không ghi cùng transaction DB với một thao tác nghiệp vụ khác, vì đăng nhập không có bản ghi nghiệp vụ nào khác đi kèm để dùng chung transaction (đã giải thích ở D-SD01-002 (¶2)). Thời hạn access token theo `identity.access_token_ttl_minutes` (mặc định 15 phút), refresh token theo `identity.refresh_token_ttl_days` (`07-system-settings.md`).
6. Làm mới phiên: khi access token hết hạn, client gọi endpoint refresh kèm refresh token hiện có → hệ thống kiểm tra `refresh_token` còn hợp lệ (chưa `revoked_at`, chưa hết hạn) **và** Nhân viên sở hữu đang `status = active` → cấp access token mới. Không thoả thì trả 401 `session_revoked`. Không ghi audit log cho bước làm mới phiên (danh mục sự kiện audit, D-SD01-002 (¶2)).
7. Đăng xuất: đánh dấu `revoked_at = now()` trên `refresh_token` hiện tại của phiên đó. Ngay sau khi xử lý xong, gọi `shared.RecordAudit` ghi nhận sự kiện đăng xuất — cùng cơ chế (không cùng transaction, gọi ngay sau khi xử lý xong) như bước 5.

### 3.3 [D-SD02-005] Luồng quên mật khẩu (R-ID-021 (§2.1.5.4))

1. Nhân viên nhập `email` tại màn hình quên mật khẩu.
2. ⚠ Hệ thống luôn trả về cùng một thông báo chung ("Nếu email tồn tại, một link đặt lại mật khẩu đã được gửi") bất kể email có tồn tại trong hệ thống hay không — cùng lý do bảo mật như bước đăng nhập ở D-SD02-004 (¶3.2). Đây là bổ sung của thiết kế.
3. Nếu `email` khớp một `employee` đang `active`: sinh token `password_reset` (cùng cơ chế token/hash/hết hạn/dùng một lần như luồng mời — R-ID-022 (§2.1.5.5)), gửi email chứa link. Nội dung email render từ mẫu cấu hình được `email.template.invite` / `email.template.password_reset`, người gửi theo `email.sender_*` (D-SD07-010 (¶4.4)).
4. Nếu `employee` đang `invited` (chưa từng đặt mật khẩu) — không tạo token `password_reset`, mà xử lý như một lượt gửi lại lời mời (D-SD02-003 (¶3.1) bước 6), vì Nhân viên đó chưa có mật khẩu nào để "quên".
5. Nhân viên mở link → xác thực token → nhập mật khẩu mới → hash → cập nhật `employee.password_hash`, đánh dấu `used_at` trên token — `employee.status` giữ nguyên `active` (không đổi). Mật khẩu mới phải thoả chính sách mật khẩu đang cấu hình (`identity.password_*`, `07-system-settings.md`); không thoả → từ chối, trả lỗi `password_policy_violation` kèm các điều kiện chưa đạt. Đặt lại mật khẩu thành công cũng xoá tạm khoá (`failed_login_count = 0`, `locked_until = NULL`).
6. Sau khi đặt lại mật khẩu thành công, trong cùng transaction: thu hồi toàn bộ `refresh_token` đang hoạt động của Nhân viên (`revoked_at = now()`), và đặt `sessions_invalidated_at = now()` — mọi phiên đang mở bị đăng xuất ngay (R-ID-034 (§2.1.5.9.4), D-SD02-007 (¶3.5)).

### 3.4 [D-SD02-006] Luồng đổi mật khẩu khi đang đăng nhập

Hiện thực R-ID-035 (§2.1.5.10): Nhân viên đang đăng nhập tự đổi mật khẩu của chính mình, ở cả Admin nội bộ và Cổng Nhân viên Tổ chức khác.

1. Nhân viên đã đăng nhập (có access token hợp lệ) gửi `current_password` và `new_password`. Nhân viên chỉ đổi được mật khẩu của chính mình, lấy theo `employee_id` trong access token. Request không nhận `employee_id` từ client.
2. Tạm khoá: nếu `locked_until > now()` thì từ chối với lỗi `login_locked` kèm `locked_until`, và không so khớp mật khẩu.
3. So khớp `current_password` với `password_hash`. Bước này dùng chung bộ đếm với luồng đăng nhập (D-SD02-004 (¶3.2) bước 3):
   - Sai: tăng `failed_login_count`. Nếu `identity.login_max_failed_attempts > 0` và `failed_login_count` đạt ngưỡng: đặt `locked_until = now() + identity.login_lockout_minutes`, đặt lại `failed_login_count = 0`, thu hồi toàn bộ `refresh_token` đang hoạt động của Nhân viên (`revoked_at = now()`) và đặt `sessions_invalidated_at = now()` (R-ID-036 (§2.1.5.10.1), D-SD02-007 (¶3.5)), ghi audit `auth.login_locked` (actor hệ thống, như D-SD02-004 (¶3.2) bước 3) và trả lỗi `login_locked`. Nếu chưa đạt ngưỡng thì trả lỗi `invalid_current_password`. Các thay đổi trong nhánh này nằm trong một transaction riêng và được commit dù request trả lỗi.
   - Đúng: đặt lại `failed_login_count = 0`, rồi sang bước 4.
4. Nếu `new_password` trùng mật khẩu hiện tại thì từ chối với lỗi `password_unchanged` (R-ID-037 (§2.1.5.10.2)). Hệ thống chỉ so với mật khẩu hiện tại, không lưu lịch sử mật khẩu. Bước này chạy sau bước 3 để lỗi này không bị dùng để dò mật khẩu hiện tại.
5. `new_password` phải thoả chính sách mật khẩu đang cấu hình (`identity.password_*`, `07-system-settings.md`). Nếu không thoả thì trả lỗi `password_policy_violation` kèm các điều kiện chưa đạt, giống D-SD02-003 (¶3.1) bước 4 và D-SD02-005 (¶3.3) bước 5.
6. Thành công: trong cùng một transaction, hash `new_password` rồi ghi vào `employee.password_hash`, thu hồi toàn bộ `refresh_token` đang hoạt động của Nhân viên kể cả phiên hiện tại, đặt `sessions_invalidated_at = now()` (R-ID-038 (§2.1.5.10.3), D-SD02-007 (¶3.5)), và gọi `shared.RecordAudit` với `action_type = auth.password_change`, `entity_type = employee`, `entity_id = employee.id`. `detail` không chứa mật khẩu dưới bất kỳ dạng nào. Client xử lý như đăng xuất và yêu cầu đăng nhập lại.
7. Không gửi email thông báo sau khi đổi mật khẩu (R-ID-039 (§2.1.5.10.4)).

### 3.5 [D-SD02-007] Vô hiệu hoá phiên ngay lập tức

Hiện thực yêu cầu đăng xuất ngay ở R-ID-025 (§2.1.5.7.1) (vô hiệu hoá tài khoản), R-ID-034 (§2.1.5.9.4) (đặt lại mật khẩu), R-ID-036 (§2.1.5.10.1) (tạm khoá khi đổi mật khẩu) và R-ID-038 (§2.1.5.10.3) (đổi mật khẩu). Chỉ thu hồi refresh token là chưa đủ, vì access token JWT đã cấp vẫn còn hiệu lực tới khi hết hạn.

1. Các thao tác trên, trong cùng transaction nghiệp vụ, đều: thu hồi toàn bộ `refresh_token` đang hoạt động của Nhân viên, và đặt `employee.sessions_invalidated_at = now()`.
2. ⚠ Middleware xác thực của `/cmd/api` (mọi route yêu cầu access token, ở cả `admin` và `partner`), sau khi kiểm chữ ký và hạn của JWT, đọc `status` và `sessions_invalidated_at` của Nhân viên theo `employee_id` trong token (truy vấn theo khoá chính, không cache). Từ chối với HTTP 401 `session_revoked` nếu:
   - `status <> active`, hoặc
   - `sessions_invalidated_at IS NOT NULL` và `iat` của token < `sessions_invalidated_at`.
3. Client xử lý `session_revoked` như hết phiên: xoá token, chuyển về màn hình đăng nhập. Client không thử làm mới phiên, vì refresh token cũng đã bị thu hồi.
4. Kích hoạt lại tài khoản (`enable`) không xoá `sessions_invalidated_at`: token cũ vẫn bị từ chối, Nhân viên đăng nhập lại để lấy token mới (R-ID-026 (§2.1.5.7.2)).
5. Chi phí: thêm 1 truy vấn theo khoá chính mỗi request. Tải Nhân viên đồng thời ≤ 200 (R-NFR-013 (§3.2.4)), nên chấp nhận được. Nếu cần, có thể thêm bộ đệm trong tiến trình, làm mới qua `LISTEN/NOTIFY` (cùng cơ chế D-SD07-008 (¶4.2)), mà không đổi hợp đồng API.

> Lưu ý: việc tự sinh/xoá role theo phạm vi khi tạo/xoá Đề tài nghiên cứu (R-KB-006 (§2.2.1.4)) không phải luồng nghiệp vụ của `/identity` — sự kiện khởi phát thuộc module 03 (`/knowledge`, Cơ sở dữ liệu văn hóa, xem D-SD03-001 (¶2.1)). Ở đây chỉ mô tả phần `/identity` tham gia (phía bị gọi vào) dưới dạng interface nội bộ ở D-SD02-008 (¶4).

## 4. [D-SD02-008] Kiến trúc riêng của module

**Interface nội bộ `/identity` cho việc tạo/xoá role theo phạm vi** — thiết kế tổng quát, dùng chung cho mọi loại phạm vi (hiện tại là Đề tài nghiên cứu — `scope_type = 'research_topic'`; mở rộng được cho loại phạm vi khác sau này, ví dụ Cương vực, không cần thêm hàm mới), theo đúng nguyên tắc biên giới package đã chốt ở D-SD01-002 (¶2) (giao tiếp cross-domain qua hàm/interface nội bộ, không JOIN chéo) — chỉ là lời gọi hàm trong cùng process, không qua HTTP/API nội bộ:

```go
package identity

type ScopeRoleProvisioner interface {
    // Gọi ngay sau khi bên gọi insert xong entity mang phạm vi mới (ví dụ research_topic), trong cùng transaction.
    // Bên gọi tự quyết định is_singular cho từng role qua ScopeRoleSpec — /identity không giữ
    // bảng ánh xạ tên role → is_singular nào, chỉ lưu lại đúng giá trị được truyền vào.
    ProvisionScopeRoles(ctx context.Context, tx pgx.Tx, scopeType string, scopeID uuid.UUID, roles []ScopeRoleSpec) ([]ScopeRole, error)

    // Gọi trước khi bên gọi xoá entity mang phạm vi đó, trong cùng transaction.
    RevokeScopeRoles(ctx context.Context, tx pgx.Tx, scopeID uuid.UUID) error
}

type ScopeRoleSpec struct {
    Name       string
    IsSingular bool
}

type ScopeRole struct {
    ID   uuid.UUID
    Name string
}
```

1. **Tạo role** (`ProvisionScopeRoles`): nhận `scope_type`, `scope_id`, và danh sách `ScopeRoleSpec{Name, IsSingular}` cần tạo — insert mỗi phần tử thành một dòng `roles` với `name`, `scope_type`, `scope_id`, `is_singular` tương ứng (giá trị `is_singular` lấy **trực tiếp** từ phần tử được truyền vào, không tra cứu gì thêm trong `/identity` — bên gọi là nơi duy nhất quyết định giá trị này, vì bên gọi mới biết ngữ nghĩa nghiệp vụ của từng role nó định nghĩa), trả về danh sách `(id, name)` của các role vừa tạo. Ví dụ gọi cho Đề tài nghiên cứu (R-KB-006 (§2.2.1.4)): `/knowledge` bắt đầu transaction, insert `research_topic`, rồi gọi `ProvisionScopeRoles(ctx, tx, "research_topic", researchTopicID, []ScopeRoleSpec{{Name: "chu_nhiem_de_tai", IsSingular: true}, {Name: "nghien_cuu", IsSingular: false}, {Name: "xet_duyet", IsSingular: false}})` — truyền cùng transaction (`tx`) làm tham số, giống nguyên tắc đã áp dụng cho `shared.RecordAudit`/`shared.RecordUsage` (D-SD01-002 (¶2)), để tạo entity và tạo role theo phạm vi là một thao tác atomic: lỗi ở bước nào cũng rollback toàn bộ.
2. **Xoá role** (`RevokeScopeRoles`): chỉ cần `scope_id` — xoá mọi dòng `roles` có `scope_id` này, không cần biết `scope_type`, vì `scope_id` là UUID của một entity cụ thể (duy nhất trên toàn hệ thống, không trùng giữa các loại phạm vi khác nhau) nên không có nguy cơ xoá nhầm. Bên gọi (ví dụ `/knowledge`) gọi hàm này **trước** khi xoá dòng entity mang phạm vi đó (cùng transaction) — bắt buộc theo thứ tự này vì `roles.scope_id` có khoá ngoại trỏ tới bảng entity đó, xoá entity trước sẽ vi phạm ràng buộc khoá ngoại nếu còn role tham chiếu.
3. ⚠ Để việc xoá role tự động kéo theo xoá `employee_role` liên quan mà không cần round-trip riêng, thêm ràng buộc `ON DELETE CASCADE` cho khoá ngoại `employee_role.role_id → roles.id` (đã cập nhật vào mô hình dữ liệu D-SD02-001 (¶2)) — khi `/identity` xoá dòng `roles`, Postgres tự xoá các dòng `employee_role` tương ứng. Chi tiết kỹ thuật của thiết kế, không phải yêu cầu đặc tả gốc.
4. Không cần entry `audit_log` riêng cho việc tạo/xoá role theo phạm vi — thao tác tạo/xoá entity mang phạm vi (ví dụ Đề tài nghiên cứu ở `/knowledge`) đã tự ghi audit log cho hành động đó (quy ước chung D-SD01-003 (¶3)); role/employee_role theo phạm vi được xem là chi tiết hiện thực nội bộ đi kèm, không ghi trùng.
5. Interface tổng quát này chỉ có 2 hàm, đặt trực tiếp trong `/identity` — bất kỳ module nào cần tạo role theo phạm vi mới (hiện tại chỉ `/knowledge` cho Đề tài nghiên cứu) đều gọi qua cùng 2 hàm này, không cần thêm interface riêng cho từng loại phạm vi; bên gọi giữ tham chiếu interface (dependency injection lúc khởi tạo service) để dễ mock khi unit test.
6. ⚠ **Bổ sung — gán/gỡ một Nhân viên vào một role theo phạm vi cụ thể đã tồn tại** (khác với `ProvisionScopeRoles` ở trên — hàm đó chỉ *tạo dòng role rỗng*, không gán người):

```go
package identity

type ScopeRoleAssigner interface {
    // Gán employeeID vào role (scopeType, scopeID, roleName). Nếu roles.is_singular = true,
    // xoá mọi employee_role hiện có của role đó trước khi insert dòng mới, trong cùng transaction
    // (đảm bảo đúng 1 người giữ — ví dụ chu_nhiem_de_tai, R-KB-073 (§2.2.5.5)). Nếu is_singular = false,
    // insert thêm (không xoá ai) — lỗi nếu đã tồn tại đúng cặp (employee, role) đó.
    AssignScopeRole(ctx context.Context, tx pgx.Tx, scopeType string, scopeID uuid.UUID, roleName string, employeeID uuid.UUID) error

    // Gỡ employeeID khỏi role (scopeType, scopeID, roleName). Không có ngữ nghĩa đặc biệt theo is_singular.
    RevokeScopeRole(ctx context.Context, tx pgx.Tx, scopeType string, scopeID uuid.UUID, roleName string, employeeID uuid.UUID) error

    // Liệt kê Nhân viên đang giữ mỗi role theo phạm vi của một scope_id, gộp theo tên role — phục vụ
    // màn hình quản lý nhân sự đề tài (D-SD03-021 (¶5.1) , endpoint `members`).
    ListEmployeesByScope(ctx context.Context, scopeID uuid.UUID) (map[string][]EmployeeSummary, error)
}

type EmployeeSummary struct {
    ID             uuid.UUID
    DisplayName    string
    Email          string
    OrganizationID uuid.UUID
}
```

Bên gọi (`/knowledge`) chịu trách nhiệm kiểm tra quyền (quan_tri_he_thong hay Chủ nhiệm đề tài đúng phạm vi) **trước** khi gọi `AssignScopeRole`/`RevokeScopeRole` — 2 hàm này chỉ thực hiện đúng thao tác ghi, không tự kiểm role người gọi (cùng nguyên tắc đã áp dụng cho `ProvisionScopeRoles`/`RevokeScopeRoles`). Dùng cho việc: Quản trị hệ thống gán/đổi Chủ nhiệm đề tài (`roleName = "chu_nhiem_de_tai"`, luôn có hiệu ứng thay thế nhờ `is_singular`); Quản trị hệ thống hoặc Chủ nhiệm đề tài gán/gỡ Nghiên cứu/Xét duyệt (`roleName = "nghien_cuu"`/`"xet_duyet"`). Cùng một interface tổng quát này có thể tái dùng cho bất kỳ role theo phạm vi mới nào sau này (ví dụ theo Cương vực), không cần thêm hàm riêng.

7. ⚠ **Bổ sung — đọc thông tin Nhân viên kèm toàn bộ role, và tìm kiếm Nhân viên** (hoàn thiện kỹ thuật cho luồng đăng nhập trả về role, D-SD02-004 (¶3.2), và luồng Chủ nhiệm đề tài tìm người thêm Nghiên cứu/Xét duyệt, D-PRT-009 (¶4.9)/D-PRT-010 (¶4.10)):

```go
package identity

// Trả thông tin Nhân viên + toàn bộ role đang giữ (chức năng lẫn phạm vi), kèm JOIN organization
// lấy organization.name (dùng cho field organization_name ở response, D-SD02-009 (¶5.1)).
// Dùng cho POST /auth/login và GET /auth/me (D-SD02-009 (¶5.1)).
func GetEmployeeWithRoles(ctx context.Context, employeeID uuid.UUID) (*EmployeeWithRoles, error)

type EmployeeWithRoles struct {
    Employee Employee
    Roles    []ScopeRoleWithScope // ScopeRole (D-SD02-008 (¶4)) + ScopeType/ScopeID
}

// Tìm Nhân viên theo từ khoá (display_name/email), không giới hạn organization_id,
// không lọc theo role đang giữ. Dùng cho Chủ nhiệm đề tài tìm người thêm Nghiên cứu/Xét duyệt
// (D-PRT-009 (¶4.9)/D-PRT-010 (¶4.10) đã chốt "không giới hạn Tổ chức").
func SearchEmployees(ctx context.Context, query string, cursor string) ([]EmployeeSummary, string, error)

// Tra cứu hàng loạt tên/email Nhân viên theo id — dùng cho tầng handler ghép dữ liệu hiển thị
// vào response của module khác (ví dụ GET /shared/audit-logs, 01-architecture-and-tech-stack.md
// D-SD02-001 (¶2)), tránh cross-package JOIN và tránh import cycle Go giữa /shared và /identity.
// Id không khớp Nhân viên nào (hiếm — hiện chưa có xoá cứng, D-SD02-010 (¶5.2)) thì bỏ qua, không lỗi.
func GetEmployeeSummaries(ctx context.Context, employeeIDs []uuid.UUID) (map[uuid.UUID]EmployeeSummary, error)
```

`GetEmployeeWithRoles` chỉ đọc — gộp 1 lượt cả thông tin `employee` và toàn bộ dòng `roles` đang giữ (qua `employee_role`, không rút gọn theo `scope_type`), tránh việc tầng gọi (`auth.login` — `POST /auth/login`, `auth.getMe` — `GET /auth/me`) phải tự JOIN hoặc gọi nhiều hàm rời rạc, đồng thời JOIN `organization` lấy `name` (phục vụ field `organization_name` ở response, D-SD02-009 (¶5.1)). `SearchEmployees` dùng chung 1 hàm cho mọi nơi cần tìm Nhân viên hệ thống-rộng (không giới hạn theo Tổ chức hay role đang giữ) — validate quyền gọi (ai được tìm) là trách nhiệm của bên gọi (ví dụ `/knowledge.SearchEmployeesForTopic`, D-SD03-017 (¶4.2)), không tự kiểm ở đây, cùng nguyên tắc đã áp dụng cho `AssignScopeRole`/`RevokeScopeRole`. `GetEmployeeSummaries` dùng cho đúng 1 điểm gọi hiện tại: tầng handler HTTP ghép tên/email vào response `shared.listAuditLogs` — `GET /shared/audit-logs` — không phải interface đọc dùng chung rộng rãi như `GetEmployeeWithRoles`/`SearchEmployees`.

## 5. Thiết kế API

### 5.1 [D-SD02-009] Nhóm `auth/*` — mount ở cả `/api/v1/admin/auth/...` và `/api/v1/partner/auth/...`

Ranh giới mount đã chốt ở D-SD01-002 (¶2): nhóm `auth/*` là ngoại lệ duy nhất của `/identity` được mount ở cả 2 giao diện Nhân viên, vì Nhân viên Tổ chức khác cũng cần tự xác thực (R-ID-023 (§2.1.5.6) đặc tả gốc) dù không được vào nhóm `identity/*`.

| Method | Path | operationId | Mô tả | Xác thực |
|---|---|---|---|---|
| POST | `/auth/login` | `auth.login` | Đăng nhập — R-ID-017 (§2.1.5.1), D-SD02-004 (¶3.2) | Không |
| POST | `/auth/refresh` | `auth.refresh` | Làm mới access token — D-SD02-004 (¶3.2) bước 6 | Refresh token |
| POST | `/auth/logout` | `auth.logout` | Đăng xuất, thu hồi refresh token — D-SD02-004 (¶3.2) bước 7 | Access token |
| POST | `/auth/forgot-password` | `auth.forgotPassword` | Yêu cầu đặt lại mật khẩu — D-SD02-005 (¶3.3) bước 1–2 | Không |
| POST | `/auth/reset-password` | `auth.resetPassword` | Đặt lại mật khẩu bằng token — D-SD02-005 (¶3.3) bước 5 | Không (token trong body) |
| GET | `/auth/invite/{token}` | `auth.getInvite` | Kiểm tra token mời hợp lệ, trả về email để hiển thị form — D-SD02-003 (¶3.1) bước 3 | Không |
| POST | `/auth/accept-invite` | `auth.acceptInvite` | Đặt mật khẩu lần đầu, kích hoạt tài khoản — D-SD02-003 (¶3.1) bước 4 | Không (token trong body) |
| GET | `/auth/me` | `auth.getMe` | ⚠ Bổ sung — trả thông tin Nhân viên hiện tại + role đang giữ dựa trên access token; dùng để FE khôi phục trạng thái đăng nhập khi tải lại trang | Access token |
| GET | `/auth/password-policy` | `auth.getPasswordPolicy` | ⚠ Bổ sung — trả chính sách mật khẩu đang cấu hình `{min_length, require_letter_and_digit, require_special_char}` (`07-system-settings.md`) để màn hình đặt mật khẩu lần đầu/đặt lại mật khẩu hiển thị yêu cầu và kiểm tra trước khi gửi | Không |
| POST | `/auth/change-password` | `auth.changePassword` | ⚠ Bổ sung — Nhân viên đang đăng nhập tự đổi mật khẩu của mình, body `{current_password, new_password}`, D-SD02-006 (¶3.4) | Access token |

`auth.changePassword` — `POST /auth/change-password` (⚠ bổ sung, D-SD02-006 (¶3.4)) trả `204 No Content` khi thành công. Các lỗi theo quy ước lỗi chung (D-SD01-003 (¶3)):

| HTTP | `error_code` | Khi nào |
|---|---|---|
| 422 | `invalid_current_password` | Sai mật khẩu hiện tại, chưa đạt ngưỡng tạm khoá |
| 423 | `login_locked` | Đang tạm khoá, hoặc vừa bị tạm khoá do lần sai này. Kèm `locked_until`. Mọi refresh token đã bị thu hồi, nên client xử lý như hết phiên |
| 422 | `password_unchanged` | Mật khẩu mới trùng mật khẩu hiện tại |
| 422 | `password_policy_violation` | Mật khẩu mới không thoả chính sách, kèm các điều kiện chưa đạt |

Lỗi sai mật khẩu hiện tại không dùng HTTP 401, để client không nhầm với access token hết hạn (401 sẽ kích hoạt luồng làm mới phiên hoặc đăng xuất).

Mọi endpoint yêu cầu access token (cả nhóm `auth/*` lẫn các module khác) có thể trả HTTP 401 `session_revoked` khi phiên đã bị vô hiệu hoá (D-SD02-007 (¶3.5)). Lỗi này khác 401 do access token hết hạn: client không gọi `auth.refresh`, mà chuyển thẳng về màn hình đăng nhập.

Response body của `auth.login` — `POST /auth/login` và `auth.getMe` — `GET /auth/me` (⚠ bổ sung — hoàn thiện kỹ thuật, phục vụ FE biết menu/màn hình nào hiển thị theo role đang giữ):

```json
// POST /auth/login (200)
{
  "employee": {
    "id": "uuid", "email": "string", "display_name": "string",
    "phone": "string", "organization_id": "uuid", "organization_name": "string", "status": "active"
  },
  "roles": [
    { "id": "uuid", "name": "nghien_cuu", "scope_type": "research_topic", "scope_id": "uuid" },
    { "id": "uuid", "name": "quan_tri_he_thong", "scope_type": "function", "scope_id": null }
  ],
  "access_token": "string",
  "refresh_token": "string"
}
// GET /auth/me (200) — giống hệt trên, bỏ access_token/refresh_token
```

`roles` trả toàn bộ role Nhân viên đang giữ (không rút gọn) — dùng `GetEmployeeWithRoles` (D-SD02-008 (¶4)). `auth.getMe` — `GET /auth/me` mount ở cả `admin`/`partner`, cùng nhóm ngoại lệ `auth/*` (D-SD01-002 (¶2) ) — không ghi audit log cho `auth.getMe` — `GET /auth/me` (request đọc).

`organization_name` (⚠ bổ sung) lấy từ `organization.name` qua JOIN trong `GetEmployeeWithRoles` (D-SD02-008 (¶4)) — dùng để Cổng Nhân viên Tổ chức khác hiển thị tên Tổ chức (ví dụ Topbar) mà không cần gọi `identity.getOrganization` (chỉ mount ở admin, D-SD02-010 (¶5.2)).

⚠ `auth.getInvite` — `GET /auth/invite/{token}` không bắt buộc theo đặc tả gốc — thêm để FE hiển thị lỗi rõ ràng trước khi người dùng nhập mật khẩu (token hết hạn/đã dùng), thay vì chỉ báo lỗi sau khi submit. Có thể bỏ nếu muốn tối giản, gộp việc kiểm tra vào bước submit `accept-invite`.

Sự kiện audit của nhóm `auth/*` (`auth.login`, `auth.logout`, `auth.login_locked`, `auth.accept_invite`, `auth.password_reset`, `auth.password_change`) và thời điểm ghi: xem danh mục sự kiện audit ở D-SD01-002 (¶2).

### 5.2 [D-SD02-010] Nhóm `identity/*` — chỉ mount ở `/api/v1/admin/identity/...` (R-PTN-010 (§2.7.4) đặc tả gốc)

Yêu cầu JWT hợp lệ + role `quan_tri_he_thong` cho mọi endpoint dưới đây (R-GEN-011 (§1.2.3.3) đặc tả gốc — quản lý người dùng/Tổ chức là việc của Quản trị hệ thống).

**Nhân viên**

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/identity/employees` | `identity.listEmployees` | Danh sách Nhân viên — cursor pagination, filter `organization_id`, `status`; mỗi dòng trả kèm `roles: [{id, name, scope_type, scope_id}]` (toàn bộ role đang giữ — chức năng lẫn phạm vi, cùng cấu trúc `auth.login` D-SD02-009 (¶5.1)) — ⚠ bổ sung |
| POST | `/identity/employees` | `identity.createEmployee` | Tạo Nhân viên mới → trạng thái `invited`, gửi email mời (D-SD02-003 (¶3.1) bước 1–2) |
| GET | `/identity/employees/{id}` | `identity.getEmployee` | Chi tiết 1 Nhân viên, kèm danh sách role đang giữ |
| PATCH | `/identity/employees/{id}` | `identity.updateEmployee` | Cập nhật `display_name`/`phone`/`organization_id` |
| POST | `/identity/employees/{id}/disable` | `identity.disableEmployee` | Vô hiệu hoá tài khoản (R-ID-024 (§2.1.5.7)): chuyển `status` → `disabled`; trong cùng transaction thu hồi toàn bộ refresh token và đặt `sessions_invalidated_at = now()` — đăng xuất ngay mọi phiên (R-ID-025 (§2.1.5.7.1), D-SD02-007 (¶3.5)). Không gỡ role, không nhả các Hạng mục tri thức/Mục từ đang phụ trách (R-ID-026 (§2.1.5.7.2)–R-ID-027 (§2.1.5.7.3)) |
| POST | `/identity/employees/{id}/enable` | `identity.enableEmployee` | Kích hoạt lại tài khoản (R-ID-024 (§2.1.5.7)): chuyển `status` → `active`; giữ nguyên mật khẩu và role (R-ID-026 (§2.1.5.7.2)) |
| POST | `/identity/employees/{id}/clear-login-lock` | `identity.clearEmployeeLoginLock` | Quản trị hệ thống gỡ tạm khoá đăng nhập trước thời hạn (R-ID-032 (§2.1.5.9.2); `failed_login_count = 0`, `locked_until = NULL`); chỉ hợp lệ khi `locked_until > now()`. `identity.listEmployees` và chi tiết Nhân viên trả thêm `locked_until` (null nếu không bị tạm khoá) để hiển thị trạng thái tạm khoá |
| POST | `/identity/employees/{id}/resend-invite` | `identity.resendEmployeeInvite` | Gửi lại lời mời (D-SD02-003 (¶3.1) bước 6) — chỉ hợp lệ khi `status = invited` |

**Role & gán role**

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/identity/roles` | `identity.listRoles` | Danh sách role — filter `scope_type`, `scope_id` (ví dụ xem role của 1 Đề tài nghiên cứu) |
| GET | `/identity/employees/{id}/roles` | `identity.listEmployeeRoles` | Role đang giữ của 1 Nhân viên |
| POST | `/identity/employees/{id}/roles` | `identity.addEmployeeRole` | Gán 1 role cho Nhân viên — body `{ role_id }` |
| DELETE | `/identity/employees/{id}/roles/{role_id}` | `identity.removeEmployeeRole` | Gỡ 1 role khỏi Nhân viên |

**Tổ chức**

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/identity/organizations` | `identity.listOrganizations` | Danh sách Tổ chức — mỗi dòng trả kèm `employee_count` (int, đếm mọi `employee.organization_id` khớp Tổ chức này, không phân biệt `status`) — ⚠ bổ sung |
| POST | `/identity/organizations` | `identity.createOrganization` | Tạo Tổ chức mới (R-ID-009 (§2.1.4)) |
| GET | `/identity/organizations/{id}` | `identity.getOrganization` | Chi tiết 1 Tổ chức |
| PATCH | `/identity/organizations/{id}` | `identity.updateOrganization` | Cập nhật thông tin Tổ chức |

Không có endpoint xoá Nhân viên hay xoá Tổ chức, và Tổ chức không có trạng thái ngừng hoạt động (R-ID-028 (§2.1.5.7.4)) — chỉ `disable`/`enable` cho Nhân viên. Không xoá cũng giữ nguyên tham chiếu từ `audit_log`/`employee_role`/`employee_credential_token`.

Mọi endpoint ghi ở D-SD02-010 (¶5.2) có audit log — `action_type` và `detail` từng endpoint theo danh mục sự kiện audit ở D-SD01-002 (¶2).

## 6. Vấn đề mở / giả định

- Cơ chế xác thực Nhân viên (email + mật khẩu, mời qua email) — được System Design đề xuất, nay đã được đặc tả gốc xác nhận tại R-ID-016 (§2.1.5). Các trường `employee.password_hash`, `employee.status`, bảng `employee_credential_token` (D-SD02-001 (¶2)) là thực thi kỹ thuật của R-ID-016 (§2.1.5) — đã chốt, không còn là đề xuất chờ xác nhận.
- Không dùng SSO/OAuth bên thứ ba ở giai đoạn này, kể cả cho Nhân viên Tổ chức khác (R-ID-023 (§2.1.5.6) đặc tả gốc) — nhất quán với cơ chế email + mật khẩu duy nhất ở trên, không cần thiết kế thêm route/luồng xác thực khác.
- Bảng `refresh_token` là thiết kế kỹ thuật để hiện thực quyết định JWT + refresh token đã có ở D-SD01-007 (¶7) — không cần xác nhận thêm từ Requirements (thuộc phạm vi kỹ thuật thuần tuý), nhưng ghi nhận ở đây vì chưa có trong tài liệu 01.
- Khi Đề tài nghiên cứu bị xoá, xoá luôn 3 role theo phạm vi liên quan (`chu_nhiem_de_tai`, `nghien_cuu`, `xet_duyet`) và các `employee_role` tương ứng (D-SD02-008 (¶4)) — quyết định thiết kế, không thuộc phạm vi đặc tả gốc (lifecycle Đề tài nghiên cứu do module 03 quản lý; xoá role là hệ quả kỹ thuật đi kèm ở `/identity`, cơ chế cụ thể: `ON DELETE CASCADE` + interface tổng quát `RevokeScopeRoles`, D-SD02-008 (¶4)).
- Các quyết định bảo mật bổ sung ở ¶3 (thông báo lỗi đăng nhập/quên mật khẩu dùng chung để tránh dò email hợp lệ, vô hiệu hoá token mời cũ khi gửi lại lời mời, thu hồi toàn bộ refresh token khi đổi mật khẩu) là thực hành chuẩn do thiết kế đề xuất thêm, không phải yêu cầu trực tiếp từ đặc tả gốc — không cần xác nhận từ Requirements vì thuộc phạm vi kỹ thuật/bảo mật thuần tuý.
- Vô hiệu hoá/kích hoạt lại tài khoản (`disable`/`enable`, D-SD02-010 (¶5.2)) hiện thực R-ID-024 (§2.1.5.7); không xoá Nhân viên/Tổ chức theo R-ID-028 (§2.1.5.7.4).
- Nhóm route `auth/*` mount ở cả `/api/v1/admin/...` và `/api/v1/partner/...` (D-SD02-009 (¶5.1)) là một ngoại lệ riêng cho `auth/*` trong ranh giới route đã chốt ở D-SD01-002 (¶2) — không phải mở lại toàn bộ `identity` cho partner.
- Role `van_hanh` (vận hành, R-ID-006 (§2.1.3.1.1) đặc tả gốc) là seed data dự phòng — chưa được module nghiệp vụ nào (03/04/05) dùng cụ thể, đúng tinh thần "chưa đầy đủ" của R-ID-005 (§2.1.3.1).
- **Vai trò Chủ nhiệm đề tài (`chu_nhiem_de_tai`) và cột `roles.is_singular`** (D-SD02-001 (¶2), D-SD02-008 (¶4)) — theo yêu cầu mới từ `requirements/business-requirements.md` R-KB-073 (§2.2.5.5) (bổ sung 2026-09-22): role theo phạm vi thứ 3 bên cạnh `nghien_cuu`/`xet_duyet`, tự sinh cùng lúc khi tạo Đề tài nghiên cứu. ⚠ Cột `is_singular` và interface `AssignScopeRole`/`RevokeScopeRole`/`ListEmployeesByScope` (D-SD02-008 (¶4)) là quyết định kỹ thuật để hiện thực đúng ràng buộc "đúng 1 Chủ nhiệm/đề tài" và cơ chế phân quyền gán Nghiên cứu/Xét duyệt cho Chủ nhiệm đề tài — không có trong đặc tả gốc ở mức chi tiết kỹ thuật này, do thiết kế đề xuất thêm.
- **`GetEmployeeWithRoles`/`SearchEmployees` và response body `auth.login` — `POST /auth/login`/`auth.getMe` — `GET /auth/me`** (D-SD02-008 (¶4), D-SD02-009 (¶5.1)) — ⚠ đề xuất bổ sung, ghi nhận 2026-09-23: hoàn thiện kỹ thuật thuần tuý, giải quyết 2 khoảng trống thực thi phát hiện khi đối chiếu code với thiết kế — (1) response đăng nhập trước đó chưa đặc tả cụ thể có trả `roles` hay không, khiến FE không biết menu nào hiển thị theo role; (2) Chủ nhiệm đề tài (partner-web) trước đó không có API nào để tìm Nhân viên khi thêm Nghiên cứu/Xét duyệt. Không đổi hành vi nghiệp vụ, không phát sinh mô hình phân quyền mới.
- **Đóng điểm treo (H) từ đợt rà soát chéo 2026-09-23** — mâu thuẫn giữa D-SD02-001 (¶2) ("`is_singular` giúp `AssignScopeRole` không cần hard-code theo tên role") và D-SD02-008 (¶4) ("`ProvisionScopeRoles` đặt `is_singular` theo cấu hình mặc định của từng tên role" — không rõ cấu hình này nằm ở đâu). Người dùng chọn hướng: **caller truyền tường minh** — đổi chữ ký `ProvisionScopeRoles` nhận `[]ScopeRoleSpec{Name, IsSingular}` thay vì `[]string`; module định nghĩa role theo phạm vi (ví dụ `/knowledge`) tự quyết định `is_singular` cho từng role nó tạo, truyền thẳng vào lúc gọi. `/identity` không giữ bất kỳ bảng ánh xạ tên role → `is_singular` nào — giữ đúng tinh thần interface tổng quát, không mang kiến thức nghiệp vụ của từng loại phạm vi (D-SD02-008 (¶4) điểm 5).
- **`roles` ở `identity.listEmployees` — `GET /identity/employees`, `employee_count` ở `identity.listOrganizations` — `GET /identity/organizations`** (D-SD02-010 (¶5.2)) — ⚠ bổ sung 2026-09-23: hoàn thiện kỹ thuật cho màn hình Admin nội bộ (D-ADM-004 (¶4.4), D-ADM-006 (¶4.6)) — danh sách Nhân viên cần hiển thị role đang giữ dạng chip, danh sách Tổ chức cần đếm số Nhân viên trực thuộc; trước đó 2 endpoint danh sách chưa trả các trường này. `roles` lấy toàn bộ (chức năng + phạm vi). `employee_count` đếm không phân biệt trạng thái. Không đổi hành vi nghiệp vụ, không phát sinh mô hình phân quyền mới.
- **`GetEmployeeSummaries`** (D-SD02-008 (¶4)) — ⚠ bổ sung 2026-09-23: hàm tra cứu hàng loạt tên/email Nhân viên theo id, phục vụ tầng handler (`/cmd/api`) ghép dữ liệu hiển thị cho `shared.listAuditLogs` — `GET /shared/audit-logs` mà không JOIN chéo hay tạo phụ thuộc vòng giữa `/shared` và `/identity`.
- **`organization_name` trong response `auth.login` — `POST /auth/login`/`auth.getMe` — `GET /auth/me`** (D-SD02-008 (¶4), D-SD02-009 (¶5.1)) — ⚠ đề xuất bổ sung: hoàn thiện kỹ thuật thuần tuý, phục vụ Cổng Nhân viên Tổ chức khác (partner-web) hiển thị tên Tổ chức mà không cần gọi `identity.getOrganization` (chỉ mount ở admin, D-SD02-010 (¶5.2)). Không đổi hành vi nghiệp vụ, không phát sinh mô hình phân quyền mới.
- **Tài khoản Quản trị hệ thống đầu tiên** (D-SD02-002 (¶3.0)) hiện thực R-ID-019 (§2.1.5.2.1). Cách làm cụ thể — seed/migration lúc triển khai, đọc credential từ biến môi trường, idempotent theo `email` — là quyết định kỹ thuật.
- **Chính sách mật khẩu, tạm khoá đăng nhập, thời hạn đường dẫn và mẫu email** (D-SD02-001 (¶2), D-SD02-003 (¶3.1)–D-SD02-006 (¶3.4), D-SD02-009 (¶5.1), D-SD02-010 (¶5.2)) hiện thực R-ID-022 (§2.1.5.5), R-ID-029 (§2.1.5.8), R-ID-030 (§2.1.5.9); tham số đọc từ cấu hình hệ thống (R-CFG-007 (§2.8.4.2)–R-CFG-008 (§2.8.4.3), `07-system-settings.md`). Thông báo tạm khoá (D-SD02-004 (¶3.2) bước 2a) cho biết email đó có tài khoản — chấp nhận theo R-ID-031 (§2.1.5.9.1). ⚠ Thời hạn access token/refresh token là tham số kỹ thuật của thiết kế (R-CFG-007 (§2.8.4.2) chỉ nêu "thời hạn phiên đăng nhập").
- **Đổi mật khẩu khi đang đăng nhập, `auth.changePassword` — `POST /auth/change-password`** (D-SD02-001 (¶2), D-SD02-006 (¶3.4), D-SD02-009 (¶5.1)) hiện thực R-ID-035 (§2.1.5.10). Audit `auth.password_change` ghi cùng transaction theo quy ước chung. Mã lỗi và thứ tự kiểm tra (tạm khoá → mật khẩu hiện tại → trùng → chính sách) là quyết định kỹ thuật.
- ⚠ **Vô hiệu hoá phiên ngay bằng `sessions_invalidated_at` + kiểm tra ở middleware** (D-SD02-001 (¶2), D-SD02-007 (¶3.5), D-SD02-009 (¶5.1), D-SD02-010 (¶5.2)) — cách hiện thực yêu cầu "đăng xuất ngay" của R-ID-025 (§2.1.5.7.1), R-ID-034 (§2.1.5.9.4), R-ID-036 (§2.1.5.10.1), R-ID-038 (§2.1.5.10.3). Đánh đổi: thêm 1 truy vấn theo khoá chính mỗi request có xác thực. Không áp dụng cho lần đăng nhập bị tạm khoá ở luồng đăng nhập (D-SD02-004 (¶3.2) bước 3): đặc tả không yêu cầu đăng xuất các phiên khác trong trường hợp này.
