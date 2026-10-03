# Thiết Kế Module: Bách Khoa Toàn Thư (`/encyclopedia`)

> Trạng thái: ¶1–6 đã chốt. Tên bảng/field/hàm nội bộ và path API dùng tiếng Anh (theo `00-claude-instructions.md` mục 6); giá trị `status`/tên role vẫn dùng tiếng Việt không dấu để đối chiếu trực tiếp với đặc tả gốc. Lịch sử thay đổi ở `system-design/changelog.md`.

## 1. Tổng quan module

- Module tạo ra sản phẩm Bách Khoa Toàn Thư (R-ENC-001 (§2.3) đặc tả gốc) — tập các Mục từ, dùng làm nền tảng dữ liệu cho Người dùng công khai (R-PUB-001 (§2.6)) và AI Văn Minh Việt (R-AI-001 (§2.4), module 05).
- Phụ thuộc vào module 03 (`/knowledge`): đọc nội dung Hạng mục tri thức đang có phiên bản được chọn để sử dụng (R-KB-030 (§2.2.3.4.1)) qua interface nội bộ, để vai trò Biên tập tham chiếu khi soạn/đồng bộ Mục từ (R-ENC-017 (§2.3.3)). Không JOIN chéo bảng.
- Phụ thuộc vào module 02 (`/identity`): 3 role riêng của module này — `bien_tap`, `xuat_ban_muc_tu`, `xet_duyet_muc_tu` — đều là **role theo chức năng** (`scope_type = 'function'`), seed sẵn, không tự sinh theo sự kiện như `nghien_cuu`/`xet_duyet` ở module 03 (R-ENC-019 (§2.3.4) đặc tả gốc không mô tả phạm vi theo đề tài cho các role này).
- Là nguồn dữ liệu cho `/assistant` (module 05, đọc **phiên bản đang công khai**) và cho Web công khai/ứng dụng di động qua nhóm route `/api/v1/public/...` (đã chốt ranh giới ở D-SD01-002 (¶2)). Module 05 chỉ được phép phụ thuộc *vào* module này qua interface đọc (D-SD04-013 (¶4.3)) và qua job queue (D-SD04-014 (¶4.4)) — không có chiều ngược lại (`/encyclopedia` không import `/assistant`).
- Khác biệt lớn nhất so với module 03: **không có bước AI Verification** — đặc tả gốc R-ENC-022 (§2.3.5) không mô tả bước xét duyệt tự động nào cho Mục từ (khác hẳn R-KB-077 (§2.2.6.5)–R-KB-080 (§2.2.6.6) của Hạng mục tri thức); toàn bộ xét duyệt do **vai trò Xét duyệt Mục từ** thực hiện thủ công. Vì vậy không cần các bảng `claim`/`claim_reference` ở module này — nội dung Mục từ là sản phẩm biên tập lại (không cần truy vết từng phát biểu tới tư liệu gốc, việc đó đã làm ở module 03).
- Gọi AI Gateway (`06`) cho đúng một năng lực: sinh bản nháp nội dung Mục từ từ Hạng mục tri thức đã gán (R-ENC-038 (§2.3.8), D-SD04-019 (¶3.5)). Không phải bước xét duyệt — nội dung sinh ra là nội dung soạn thảo bình thường (R-ENC-043 (§2.3.8.5)).

## 2. Mô hình dữ liệu

Quy ước chung theo `00-claude-instructions.md` mục 6 (UUID, `snake_case`, tách bảng phiên bản, không ENUM, path API tiếng Anh...) áp dụng như module 03. Tên bảng/field dùng tiếng Anh; giá trị `status` dùng tiếng Việt không dấu theo đúng thuật ngữ đặc tả gốc.

### 2.1. [D-SD04-001] `entry` (Mục từ — bảng định danh cha, R-ENC-004 (§2.3.2.1))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | R-ENC-004 (§2.3.2.1) |
| `current_public_version_id` | UUID (nullable) | R-ENC-010 (§2.3.2.4.1) "Phiên bản đang công khai" — FK → `entry_version.id`, chỉ trỏ tới dòng đã chốt (`frozen_at IS NOT NULL`); do **vai trò Xuất bản Mục từ** chọn/đổi (R-ENC-021 (§2.3.4.2)b), độc lập với workflow; mặc định `NULL` |
| `first_public_at` | timestamptz (nullable) | ⚠ Đề xuất bổ sung — thời điểm Mục từ được chọn phiên bản công khai **lần đầu** (R-ENC-010 (§2.3.2.4.1)); `NULL` khi chưa từng có phiên bản công khai. `SetPublicVersion` (D-SD04-014 (¶4.4)) đặt `now()` khi `current_public_version_id` đang `NULL`; đổi sang phiên bản khác không đổi giá trị này. Dùng để sắp xếp "mới công khai" ở `public.listEntries` (D-SD04-018 (¶5.4)). Migration đặt giá trị cho dòng có sẵn bằng thời điểm của sự kiện audit `entry.set_public_version` sớm nhất của Mục từ; không có thì dùng `frozen_at` của phiên bản đang công khai |
| `public_version_set_at` | timestamptz (nullable) | Thời điểm chọn phiên bản đang công khai gần nhất; `SetPublicVersion` đặt `now()` mỗi lần chọn/đổi. Là "ngày cập nhật" trong dữ liệu có cấu trúc và sitemap (R-NFR-031 (§3.6.5), R-NFR-032 (§3.6.6)). Migration đặt bằng thời điểm sự kiện audit `entry.set_public_version` gần nhất; không có thì bằng `first_public_at` |
| `slug` | text (nullable, unique) | Đường dẫn dễ đọc của Mục từ (R-NFR-029 (§3.6.3)), sinh từ tiêu đề phiên bản đang công khai theo D-SD04-023 (¶3.7); `NULL` khi chưa từng có phiên bản công khai |
| `seo_title` | text (nullable) | Tiêu đề trang nhập đè (R-ENC-044 (§2.3.2.6), R-NFR-030 (§3.6.4)); `NULL` = dùng giá trị tự sinh. Tối đa 300 ký tự |
| `seo_description` | text (nullable) | Mô tả ngắn nhập đè; `NULL` = dùng giá trị tự sinh. Tối đa 1.000 ký tự |
| `seo_image_file_id` | UUID (nullable) | Hình chia sẻ đã chọn — FK → `entry_file.id`, phải là tệp hình ảnh của phiên bản đang công khai được nhúng trong `content_blocks`. `NULL` = dùng giá trị tự sinh. Bị xoá về `NULL` khi đổi phiên bản công khai (D-SD04-023 (¶3.7)) |
| `created_by` | UUID (nullable) | ⚠ Bổ sung — FK → `employee.id`, Nhân viên giữ vai trò Biên tập đã tạo Mục từ này |
| `created_at` | timestamptz | |

- **Tạo mới**: do **vai trò Biên tập** thực hiện (R-ENC-020 (§2.3.4.1)), gộp/tách một hoặc nhiều Hạng mục tri thức. Hệ thống tạo đồng thời 1 dòng `entry_version` là bản soạn thảo đầu tiên (`frozen_at = NULL`, `status = soan_thao`, `assignee_id = createdBy` — người tạo tự động là Người phụ trách đầu tiên, R-ENC-012 (§2.3.2.5.1), xem D-SD04-002 (¶2.2)).
- Không có cột `draft_version_id` — cùng lý do đã áp dụng ở module 03 (D-SD03-005 (¶2.5)): bản soạn thảo xác định bằng dòng duy nhất `frozen_at IS NULL`.

### 2.2. [D-SD04-002] `entry_version` (bản soạn thảo + các phiên bản đã chốt, R-ENC-009 (§2.3.2.4))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `entry_id` | UUID | FK → `entry.id` |
| `version_number` | int (nullable) | Chỉ cấp cho dòng đã chốt (1, 2, 3…), `NULL` với bản soạn thảo — cùng cơ chế module 03 |
| `title` | text | R-ENC-005 (§2.3.2.2) |
| `content_blocks` | JSONB | R-ENC-007 (§2.3.2.3.1) — danh sách khối (block) có thứ tự, mỗi khối có `type` + dữ liệu (tiêu đề, đoạn văn, chú thích, khối nhúng ảnh/âm thanh/phim...). Khối nhúng file tham chiếu `entry_file.id` (D-SD04-003 (¶2.3)), không nhúng blob trực tiếp |
| `content_plain_text` | text (nullable) | ⚠ Đề xuất bổ sung — bản trích xuất text thuần từ `content_blocks` (đoạn văn, chú thích...), do tầng ứng dụng đồng bộ mỗi khi `content_blocks` đổi; dùng làm nguồn cho chỉ mục full-text (R-PUB-004 (§2.6.2.1) đặc tả gốc: tìm theo tiêu đề + nội dung) — JSONB không tự đánh index full-text tốt. Cũng là nguồn dữ liệu để `/assistant` (module 05) cắt đoạn/sinh embedding cho RAG |
| `cover_file_id` | UUID (nullable) | ⚠ Đề xuất bổ sung — ảnh đại diện của phiên bản, dùng cho card Mục từ và trích dẫn ở Web công khai. FK → `entry_file.id`. Chỉ dòng đã chốt mang giá trị: khi tạo dòng chốt ("Xuất bản"), lấy khối nhúng file **đầu tiên** trong `content_blocks` (theo thứ tự khối) tham chiếu tới `entry_file` có `file_type` là hình ảnh; không có thì `NULL`. Bản soạn thảo luôn `NULL`. Dòng chốt không đổi nội dung nên giá trị không phải tính lại |
| `status` | text (nullable) | R-ENC-006 (§2.3.2.3) — chỉ bản soạn thảo mang giá trị, dòng đã chốt `status = NULL`, cùng cơ chế đã chốt ở module 03 (D-SD03-006 (¶2.6)). 7 mã, xem D-SD04-007 (¶3.1) |
| `assignee_id` | UUID (nullable) | R-ENC-011 (§2.3.2.5) "Người phụ trách" — ⚠ Bổ sung. FK → `employee.id`. Ghi nhận đúng một Nhân viên đang chịu trách nhiệm chính tại thời điểm hiện tại, **xuyên suốt vòng đời** bản soạn thảo (mọi trạng thái ở D-SD04-007 (¶3.1)). Đối xứng hoàn toàn với `knowledge_object_version.assignee_id` ở module 03 (D-SD03-006 (¶2.6)) — đặt trực tiếp trên bản soạn thảo vì đây là **cùng một dòng ổn định** suốt vòng đời. **Không tự động bị xoá khi chuyển trạng thái** — ở các trạng thái chờ thuần tuý (`cho_xet_duyet`, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban`) giữ nguyên giá trị của lần nhận gần nhất, chỉ mang tính hiển thị (R-ENC-015 (§2.3.2.5.4)). Chỉ bị xoá qua 2 thao tác tường minh `Release`/`ForceRelease` (D-SD04-014 (¶4.4)) |
| `review_note` | text (nullable) | ⚠ Đề xuất bổ sung — nhận định tổng thể của vai trò Xét duyệt Mục từ khi chuyển `dat_xet_duyet` hoặc `khong_dat_xet_duyet` (module này không có cấu trúc claim để gắn ghi chú như module 03, nên cần 1 trường ghi chú tự do cấp Mục từ). Trả về ở `encyclopedia.getEntry` để vai trò Biên tập đọc khi Mục từ đang `khong_dat_xet_duyet` |
| `frozen_at` | timestamptz (nullable) | Thời điểm chốt (= thời điểm vai trò Xuất bản Mục từ chọn "Xuất bản", R-ENC-029 (§2.3.5.7)); `NULL` với bản soạn thảo |
| `frozen_by` | UUID (nullable) | FK → `employee.id`, giữ vai trò Xuất bản Mục từ |
| `created_at` | timestamptz | |

**Ràng buộc**: partial unique index `(entry_id) WHERE frozen_at IS NULL` — mỗi Mục từ luôn có đúng một bản soạn thảo, cùng cơ chế module 03.

**Cơ chế chốt phiên bản** (R-ENC-009 (§2.3.2.4), R-ENC-027 (§2.3.5.5)–R-ENC-030 (§2.3.5.8) — mô hình quyết định bắt buộc, giống hệt module 03):

- Khi bản soạn thảo đạt `dat_xet_duyet`, vai trò Xuất bản Mục từ bắt buộc chọn đúng 1 trong 2:
  - **"Xuất bản"**: sao chép bản soạn thảo (`content_blocks`, và toàn bộ `entry_file` liên quan — tái dùng nguyên `storage_key`, không upload lại, cùng nguyên tắc D-SD03-019 (¶4.4)) thành dòng mới `frozen_at = now()`, `frozen_by = <employee>`, `version_number` = số lớn nhất hiện có + 1, `status = NULL` (dòng chốt không có `assignee_id`), `cover_file_id` tính theo quy tắc ở bảng trên. Bản soạn thảo (dòng gốc) chuyển `status → da_xuat_ban`, `assignee_id` giữ nguyên.
  - **"Không xuất bản"**: không sao chép; bản soạn thảo chuyển `status → khong_xuat_ban`, kèm cảnh báo xác nhận bắt buộc (R-ENC-009 (§2.3.2.4) đặc tả gốc).
- Dòng đã chốt bất biến — không UPDATE/DELETE, chặn ở tầng ứng dụng (`/encyclopedia`).
- **Khoá nội dung**: 4 trạng thái `dang_xet_duyet`, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban` khoá `content_blocks`/`entry_file` trên chính bản soạn thảo — khác với module 03, đặc tả gốc **đã nêu rõ trực tiếp** cả 4 trạng thái này cho Mục từ (R-ENC-025 (§2.3.5.3), R-ENC-027 (§2.3.5.5), R-ENC-029 (§2.3.5.7), R-ENC-030 (§2.3.5.8) đều có câu "Nội dung bị khoá"), **không phải đề xuất ⚠** như trường hợp `dang_xet_duyet` ở module 03. Riêng `soan_thao` có thêm điều kiện khoá **theo người gọi** (chỉ `assignee_id` hiện tại được sửa, R-ENC-013 (§2.3.2.5.2)) — khác về bản chất với 4 trạng thái khoá hoàn toàn ở trên.

### 2.3. [D-SD04-003] `entry_file` (đính kèm, R-ENC-008 (§2.3.2.3.2))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | |
| `entry_version_id` | UUID | FK → `entry_version.id` |
| `file_type` | text | hình ảnh / âm thanh / phim |
| `storage_key` | text | Object storage + presigned URL, cùng quy ước `source_file`/`knowledge_object_file` |
| `created_at` | timestamptz | |

- Khác với `knowledge_object_file` (các file ngang hàng) — ở đây file chỉ là **tài nguyên đính kèm phụ**, nội dung chính là `content_blocks` (R-ENC-006 (§2.3.2.3), đặc tả gốc nêu rõ khác biệt này).

### 2.4. [D-SD04-004] `entry_knowledge_object` (bảng nối nhiều-nhiều, R-ENC-017 (§2.3.3))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `entry_id` | UUID | FK → `entry.id` |
| `knowledge_object_id` | UUID | FK → `knowledge_object.id` (module 03 — tham chiếu chéo module, chấp nhận được vì là khoá ngoại đơn thuần, cùng nguyên tắc đã áp dụng cho `roles.scope_id`) |
| `last_synced_version_id` | UUID (nullable) | ⚠ Đề xuất bổ sung — ghi nhận `knowledge_object_version.id` (bản đã chốt) mà vai trò Biên tập dùng làm nguồn lần đồng bộ gần nhất; dùng để hiển thị cảnh báo "đã lỗi thời" khi `knowledge_object.used_version_id` khác giá trị này (R-ENC-017 (§2.3.3): "không tự động cập nhật — vai trò Biên tập phải chủ động đồng bộ") |

- Khoá chính composite `(entry_id, knowledge_object_id)`.
- Vai trò Biên tập gộp nhiều Hạng mục tri thức thành 1 Mục từ, hoặc tách 1 Hạng mục tri thức thành nhiều Mục từ (R-ENC-017 (§2.3.3)) — chính là thêm/bớt dòng ở bảng này.
- Cờ `is_outdated` được **tính ở tầng ứng dụng** khi trả `encyclopedia.getEntry` — `GET /encyclopedia/entries/{id}` — so `last_synced_version_id` với `used_version_id` hiện tại của Hạng mục tri thức, lấy qua `knowledge.GetUsedVersionIDs` (D-SD03-017 (¶4.2)); không lưu thành cột riêng.
- ⚠ Khoá ngoại `knowledge_object_id` dùng **`ON DELETE RESTRICT`**: một Hạng mục tri thức đang được Mục từ tham chiếu thì **không xoá được** ở module 03 (D-SD03-005 (¶2.5), D-SD03-017 (¶4.2)) — ràng buộc thực thi ở tầng CSDL để `/knowledge` không phải gọi ngược sang `/encyclopedia`, giữ đúng hướng phụ thuộc một chiều 04 → 03.

### 2.5. [D-SD04-005] `cultural_domain` (Cương vực — taxonomy, R-ENC-031 (§2.3.6)–R-ENC-032 (§2.3.7))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | |
| `code` | text (unique) | ví dụ `dinh_lang`, `gia_le`, `quan_su`, `trong_dong` |
| `name` | text | Tên hiển thị — "Văn minh đình làng việt", "Văn minh gia lễ việt", "Văn minh quân sự việt", "Văn minh trống đồng" (R-ENC-033 (§2.3.7.1)–R-ENC-036 (§2.3.7.4)) |
| `slug` | text (unique) | Đường dẫn dễ đọc sinh từ `name` (R-NFR-029 (§3.6.3), D-SD04-023 (¶3.7)). Migration sinh cho dòng có sẵn |
| `updated_at` | timestamptz | Thời điểm sửa gần nhất; là "ngày cập nhật" của trang Cương vực trong sitemap |
| `created_at` | timestamptz | |

- Mô hình hoá thành bảng riêng vì danh sách Cương vực có thể thay đổi (R-ENC-037 (§2.3.7.5)): vai trò Biên tập thêm, sửa tên và xoá qua API (D-SD04-017 (¶5.3)). 4 giá trị hiện tại là seed data ban đầu (R-ENC-033 (§2.3.7.1)–R-ENC-036 (§2.3.7.4)).
- Dùng chung cho cả module 05 (AI Văn Minh Việt, R-AI-004 (§2.4.3)/R-AI-006 (§2.4.5) đặc tả gốc — cùng danh sách).

### 2.6. [D-SD04-006] `entry_cultural_domain` (bảng nối, R-ENC-031 (§2.3.6))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `entry_id` | UUID | FK → `entry.id` |
| `cultural_domain_id` | UUID | FK → `cultural_domain.id`, `ON DELETE RESTRICT` — chặn xoá Cương vực còn Mục từ đang gán (R-ENC-037 (§2.3.7.5)) |
| `created_at` | timestamptz | Thời điểm gán. Thứ tự gán dùng làm thứ tự hiển thị Cương vực của Mục từ ở nhóm `public` (D-SD04-018 (¶5.4)) |

- Khoá chính composite. Một Mục từ có thể thuộc nhiều Cương vực. Do **vai trò Biên tập gán thủ công** (R-ENC-031 (§2.3.6) — "có thể tự động hoá/gợi ý trong tương lai", ngoài phạm vi hiện tại).
- Dòng có sẵn trước khi thêm cột `created_at`: migration đặt giá trị theo tên Cương vực tăng dần, để giữ thứ tự hiện có.

### 2.7. [D-SD04-022] `public_slug_history` (slug cũ, R-NFR-029 (§3.6.3))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `object_type` | text | `entry` / `cultural_domain` |
| `slug` | text | Slug cũ |
| `object_id` | UUID | `entry.id` hoặc `cultural_domain.id` |
| `created_at` | timestamptz | Thời điểm slug này thôi là slug hiện hành |

- Khoá chính `(object_type, slug)`. Không đặt FK đa hình; xoá Cương vực thì xoá các dòng `cultural_domain` của nó trong cùng transaction.
- Khi slug của một đối tượng đổi, slug cũ được ghi vào bảng này. Nếu slug mới trùng một dòng lịch sử của **chính** đối tượng đó thì xoá dòng đó (slug quay lại làm slug hiện hành).

## 3. Luồng trạng thái / nghiệp vụ

### 3.1. [D-SD04-007] Sơ đồ tổng quan (R-ENC-022 (§2.3.5))

```
[vai trò Biên tập tạo Mục từ (gộp/tách Hạng mục tri thức)
 → khởi tạo bản soạn thảo, assignee_id = người tạo]
         ↓
soan_thao → cho_xet_duyet → (Claim) → dang_xet_duyet (vai trò Xét duyệt Mục từ)  [NỘI DUNG BỊ KHOÁ]
                           → (Release) → cho_xet_duyet
    → khong_dat_xet_duyet → soan_thao
    → dat_xet_duyet   [NỘI DUNG BỊ KHOÁ]
          → (chỉ vai trò Xuất bản Mục từ, bắt buộc đúng 1 quyết định)
               ├─ "Xuất bản"       → da_xuat_ban      [tạo phiên bản mới]      [NỘI DUNG BỊ KHOÁ]
               └─ "Không xuất bản" → khong_xuat_ban   [không tạo, có cảnh báo] [NỘI DUNG BỊ KHOÁ]

da_xuat_ban | khong_xuat_ban
    → (chỉ vai trò Xét duyệt Mục từ) mở lại về một trạng thái trước đó bất kỳ:
       soan_thao | cho_xet_duyet | dang_xet_duyet
```

Không có bước AI Verification (khác module 03) — chỉ **7** mã trạng thái:

| # | Trạng thái (đặc tả) | Mã `status` | Trích dẫn |
|---|---|---|---|
| 1 | Soạn thảo | `soan_thao` | R-ENC-023 (§2.3.5.1) |
| 2 | Chờ xét duyệt | `cho_xet_duyet` | R-ENC-024 (§2.3.5.2) |
| 3 | Đang xét duyệt | `dang_xet_duyet` | R-ENC-025 (§2.3.5.3) |
| 4 | Không đạt xét duyệt | `khong_dat_xet_duyet` | R-ENC-026 (§2.3.5.4) |
| 5 | Đạt xét duyệt | `dat_xet_duyet` | R-ENC-027 (§2.3.5.5) |
| 6 | Đã xuất bản | `da_xuat_ban` | R-ENC-029 (§2.3.5.7) |
| 7 | Không xuất bản | `khong_xuat_ban` | R-ENC-030 (§2.3.5.8) |

**Khoá nội dung** — cả 4 trạng thái `dang_xet_duyet`/`dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban` đều **có căn cứ trực tiếp trong đặc tả gốc** (không có ⚠ nào ở đây, khác module 03). Riêng `soan_thao` khoá theo người gọi (chỉ `assignee_id`), xem D-SD04-002 (¶2.2).

⚠ **Cơ chế "Người phụ trách" (`assignee_id`, R-ENC-011 (§2.3.2.5))** — áp dụng **xuyên suốt vòng đời** bản soạn thảo qua 3 thao tác `Claim`/`Release`/`ForceRelease` (D-SD04-014 (¶4.4)) — đối xứng hoàn toàn với module 03 (D-SD03-011 (¶3.2)):

- **`soan_thao`**: chỉ `assignee_id` hiện tại được sửa nội dung Mục từ (R-ENC-013 (§2.3.2.5.2)). Một Nhân viên khác giữ vai trò Biên tập `Claim` được khi `assignee_id` đang `NULL` (đã được `Release`).
- **`cho_xet_duyet → dang_xet_duyet`**: vai trò Xét duyệt Mục từ `Claim` để nhận xử lý — độc lập với `assignee_id` còn sót lại từ giai đoạn soạn thảo (khác vai trò, khác lần nhận, R-ENC-014 (§2.3.2.5.3)) — `Claim` ghi đè trực tiếp. Trong `dang_xet_duyet`, `Release` bất kỳ lúc nào để lùi về `cho_xet_duyet`, không cần Quản trị hệ thống can thiệp.
- Ở các trạng thái chờ thuần tuý (`dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban`) — `assignee_id` **giữ nguyên giá trị của lần nhận gần nhất**, chỉ mang tính hiển thị (R-ENC-015 (§2.3.2.5.4)).
- Quản trị hệ thống có thể `ForceRelease` ở bất kỳ trạng thái nào đang có `assignee_id`, nếu người đang nhận không tự `Release` (R-ENC-016 (§2.3.2.5.5)).

### 3.2. [D-SD04-008] Chi tiết từng bước

**(1) `soan_thao`** — R-ENC-023 (§2.3.5.1). Khởi tạo khi vai trò Biên tập tạo Mục từ; người tạo tự động là Người phụ trách đầu tiên (`assignee_id`, R-ENC-012 (§2.3.2.5.1)). Chỉ **Người phụ trách hiện tại** biên tập nội dung (`content_blocks`), gán `entry_file`, gán Cương vực (D-SD04-006 (¶2.6)) — R-ENC-013 (§2.3.2.5.2); một Nhân viên khác giữ vai trò Biên tập `Claim` được khi `assignee_id` đang `NULL`. Quay lại từ `khong_dat_xet_duyet` (sửa theo góp ý) — cùng bản soạn thảo, `assignee_id` giữ nguyên. **Không** quay thẳng từ `da_xuat_ban`/`khong_xuat_ban` — phải qua vai trò Xét duyệt Mục từ mở lại (bước (6)/(7)), `assignee_id` cũng giữ nguyên.

**(2) `cho_xet_duyet`** — R-ENC-024 (§2.3.5.2). Vai trò Biên tập bật cờ sẵn sàng. Mục từ ở trạng thái này chưa có ai phụ trách xét duyệt — để chuyển sang `dang_xet_duyet`, một Nhân viên giữ vai trò Xét duyệt Mục từ phải `Claim` (bước (3)).

**(3) `dang_xet_duyet`** — R-ENC-025 (§2.3.5.3). Vai trò Xét duyệt Mục từ (nhóm chuyên gia riêng, khác vai trò Xét duyệt Hạng mục tri thức ở module 03) `Claim` một Mục từ đang ở `cho_xet_duyet` để chuyển sang trạng thái này — thao tác **khoá độc quyền**: tại một thời điểm, mỗi Mục từ chỉ có đúng một chuyên gia đang xử lý; chuyên gia khác không nhận được cho tới khi được `Release`. Chuyên gia đã nhận có thể **tự `Release`** bất kỳ lúc nào, đưa Mục từ quay lại `cho_xet_duyet`; nếu không tự nhả, Quản trị hệ thống có thể `ForceRelease` (R-ENC-016 (§2.3.2.5.5)). Xét duyệt thủ công toàn bộ nội dung — không có cấu trúc phát biểu/tham chiếu như module 03, nên xét duyệt ở cấp tổng thể (`review_note`).

**(4) `khong_dat_xet_duyet`** — R-ENC-026 (§2.3.5.4). Bị từ chối bởi vai trò Xét duyệt Mục từ (`RejectReview`, ghi `review_note` — bắt buộc khi không đạt, R-ENC-025 (§2.3.5.3)). Vai trò Biên tập xem `review_note` (trả về ở `encyclopedia.getEntry` — `GET /encyclopedia/entries/{id}`), quay lại `soan_thao` trên cùng bản soạn thảo qua endpoint `resume-editing` (⚠ bổ sung, D-SD04-016 (¶5.2)) — bất kỳ Nhân viên nào giữ vai trò Biên tập đều gọi được (không giới hạn riêng theo `assignee_id`, nhất quán với `submit-for-review`); `assignee_id` giữ nguyên giá trị cũ (không tự xoá).

**(5) `dat_xet_duyet`** — R-ENC-027 (§2.3.5.5). Vai trò Xét duyệt Mục từ xác nhận đạt. **Chỉ vai trò Xuất bản Mục từ** đưa Mục từ rời khỏi đây, bằng đúng 1 trong 2 quyết định (D-SD04-002 (¶2.2)).

**(6)/(7) `da_xuat_ban` / `khong_xuat_ban`** — R-ENC-029 (§2.3.5.7)–R-ENC-030 (§2.3.5.8). Nội dung khoá. Chỉ vai trò Xét duyệt Mục từ mở lại về `soan_thao`/`cho_xet_duyet`/`dang_xet_duyet`.

### 3.3. [D-SD04-009] Hai thao tác của vai trò Xuất bản Mục từ (R-ENC-021 (§2.3.4.2))

Giống hệt cấu trúc D-SD03-013 (¶3.4):

- **(a) Quyết định Xuất bản/Không xuất bản** — bắt buộc, cách duy nhất rời `dat_xet_duyet`.
- **(b) Chọn/đổi phiên bản đang công khai** (`entry.current_public_version_id`, R-ENC-010 (§2.3.2.4.1)) — độc lập với (a), điều kiện duy nhất: dòng đích đã chốt (`frozen_at IS NOT NULL`).

### 3.4. [D-SD04-010] Đồng bộ khi Hạng mục tri thức nguồn có phiên bản mới (R-ENC-017 (§2.3.3))

- **Không tự động** — vai trò Biên tập chủ động vào Mục từ, xem nội dung `used_version` hiện tại của (các) Hạng mục tri thức liên quan (đọc qua interface `/knowledge`, D-SD04-012 (¶4.2)), tự cập nhật `content_blocks` nếu cần, rồi cập nhật `last_synced_version_id` (D-SD04-004 (¶2.4)) để tắt cảnh báo "đã lỗi thời" (cờ `is_outdated` ở `encyclopedia.getEntry` — `GET /encyclopedia/entries/{id}`).
- Việc đồng bộ này **không đổi `status`** của Mục từ — vẫn phải qua lại toàn bộ luồng xét duyệt (R-ENC-022 (§2.3.5)) nếu Mục từ đã `da_xuat_ban`/`khong_xuat_ban` và cần sửa nội dung (phải được vai trò Xét duyệt Mục từ mở lại trước).


### 3.5. [D-SD04-019] Khởi tạo nội dung bằng AI (R-ENC-038 (§2.3.8))

**Kích hoạt** (R-ENC-039 (§2.3.8.1)) — `encyclopedia.generateEntryContent`, thao tác thủ công, không tự chạy khi tạo Mục từ. Điều kiện:

- `status = soan_thao` và người gọi là `assignee_id` hiện tại — cùng điều kiện với `UpdateDraftContent` (D-SD04-014 (¶4.4)).
- Body `{confirmed: true}` — giao diện cảnh báo nội dung hiện tại sẽ bị ghi đè và chỉ gọi khi vai trò Biên tập xác nhận (R-ENC-041 (§2.3.8.3)). Thiếu hoặc `false` → HTTP 422 `overwrite_confirmation_required`.
- Ít nhất một Hạng mục tri thức đã gán có phiên bản đang được sử dụng; không có → HTTP 422 `no_source_content`.
- Không còn job `encyclopedia.generate_content` của Mục từ đang chờ/đang chạy (tính trùng như D-SD03-018 (¶4.3): `ByState` gồm `available`, `pending`, `scheduled`, `running`, `retryable`); nếu có → HTTP 409 `entry_content_generation_running`.
- Hợp lệ thì enqueue job `encyclopedia.generate_content` payload `{entry_id, requested_by}` trong cùng transaction, trả HTTP 202 `{job_id}`. Kích hoạt lại được nhiều lần (R-ENC-040 (§2.3.8.2)).

**Trong lúc xử lý** (R-ENC-042 (§2.3.8.4)) ⚠:

- `encyclopedia.getEntry` trả `content_generation` (D-SD04-015 (¶5.1)) để giao diện hiện "Đang sinh nội dung bằng AI".
- Khoá nội dung khi còn job đang chờ/đang chạy: `UpdateDraftContent`, `RequestEntryFileUpload`, `AddFile`, `RemoveFile`, `SubmitForReview` trả HTTP 409 `entry_content_generation_running`. Các thao tác khác (gán Cương vực, gộp/tách Hạng mục tri thức, đánh dấu đồng bộ, `Release`, `ForceRelease`) không bị chặn.
- `Release`/`ForceRelease` huỷ job đang chờ (chưa chạy) của Mục từ; job đang chạy thì kết quả bị bỏ ở bước ghi (bước 3 dưới đây).

**Job `encyclopedia.generate_content`** (D-SD04-020 (¶4.5)):

1. Đọc nội dung phiên bản đang được sử dụng của từng Hạng mục tri thức đã gán qua `knowledge.GetUsedVersionContent` (D-SD04-012 (¶4.2)); bỏ qua Hạng mục chưa có phiên bản đang được sử dụng. Không còn nguồn nào → job kết thúc, không ghi nội dung, audit `entry.content_generation_discard` (`reason = no_source_content`).
2. Gọi `gateway.generateEntryDraft` (D-SD06-014 (¶3.8)) với: tiêu đề Mục từ; với mỗi Hạng mục — `title`, danh sách `claim.text`, `transcript_storage_key` của file văn bản/âm thanh/phim (có transcript), `storage_key` của file hình ảnh.
3. Ghi kết quả trong một transaction, chỉ khi bản soạn thảo vẫn `soan_thao` **và** `assignee_id = requested_by`; ngược lại bỏ kết quả, audit `entry.content_generation_discard` (`reason = status_changed | assignee_changed`). Khi ghi:
   - Thay toàn bộ `content_blocks` bằng các khối sinh ra (đồng bộ `content_plain_text`); `title` không đổi. Nội dung không đánh dấu là do AI sinh (R-ENC-043 (§2.3.8.5)).
   - Mỗi khối ảnh trong kết quả: tạo `entry_file` mới trên bản soạn thảo, `file_type` hình ảnh, **dùng lại `storage_key`** của `knowledge_object_file` (không sao chép object — cùng nguyên tắc D-SD03-019 (¶4.4)); khối nhúng tham chiếu `entry_file.id` mới. Chỉ ảnh được dùng trong kết quả mới tạo `entry_file`. `entry_file` có sẵn của bản soạn thảo giữ nguyên.
   - ⚠ Cập nhật `last_synced_version_id` của từng Hạng mục đã dùng bằng `used_version_id` đã đọc ở bước 1 (tắt cờ `is_outdated`, D-SD04-004 (¶2.4)).
   - Audit `entry.content_generation_complete`.
4. Lỗi gọi AI Gateway: job thất bại và thử lại theo river (D-SD06-012 (¶6)); hết lượt thì `content_generation.status = failed`, nội dung không đổi. Vai trò Biên tập kích hoạt lại được. AI Gateway trả `source_content_too_long` (D-SD06-014 (¶3.8)) thì job dừng, không thử lại; `content_generation.status = failed`, `error_code = source_content_too_long`. Vai trò Biên tập tách bớt Hạng mục tri thức khỏi Mục từ rồi kích hoạt lại.

### 3.6. [D-SD04-021] Danh sách thao tác (R-NFR-039 (§3.7.2), R-NFR-040 (§3.7.3))

Giá trị `actions` của `encyclopedia.getEntry`, theo quy ước ở D-SD01-003 (¶3) và cách đọc bảng như D-SD03-027 (¶3.7). "Người phụ trách" là `assignee_id` của bản soạn thảo; "đang sinh nội dung" là còn job `encyclopedia.generate_content` đang chờ hoặc đang chạy (D-SD04-019 (¶3.5)).

| `action` | `operation_ids` | Hiển thị khi | Thực hiện được khi | `reason_code` | `transitions` |
|---|---|---|---|---|---|
| `claim` | `encyclopedia.claimEntry` | Giữ `bien_tap` hoặc `xet_duyet_muc_tu`; người gọi không phải Người phụ trách | `bien_tap`: `status = soan_thao` và chưa có Người phụ trách. `xet_duyet_muc_tu`: `status = cho_xet_duyet` | `invalid_status`, `assigned_to_other` | Tại `cho_xet_duyet`: → `dang_xet_duyet`, `next_roles = [xet_duyet_muc_tu]`. Tại `soan_thao`: rỗng |
| `release` | `encyclopedia.releaseEntry` | Người gọi là Người phụ trách | `status ∈ {soan_thao, dang_xet_duyet}` | `invalid_status` | Tại `dang_xet_duyet`: → `cho_xet_duyet`, `next_roles = [xet_duyet_muc_tu]`. Tại `soan_thao`: rỗng |
| `force_release` | `encyclopedia.forceReleaseEntry` | Giữ `quan_tri_he_thong` | Có Người phụ trách | `no_assignee` | Như `release` |
| `edit_content` | `encyclopedia.updateEntryContent`, `encyclopedia.addEntryKnowledgeObject`, `encyclopedia.removeEntryKnowledgeObject`, `encyclopedia.markEntryKnowledgeObjectSynced`, `encyclopedia.createEntryFileUploadUrl`, `encyclopedia.createEntryFile`, `encyclopedia.deleteEntryFile`, `encyclopedia.addEntryCulturalDomain`, `encyclopedia.removeEntryCulturalDomain` | Giữ `bien_tap` | `status = soan_thao`, người gọi là Người phụ trách, không đang sinh nội dung | `invalid_status`, `not_assigned`, `assigned_to_other`, `job_running` | — |
| `generate_content` | `encyclopedia.generateEntryContent` | Giữ `bien_tap` | Như `edit_content`, và có ít nhất một Hạng mục tri thức đã gán có phiên bản đang được sử dụng | `invalid_status`, `not_assigned`, `assigned_to_other`, `job_running`, `no_source_content` | — |
| `submit_for_review` | `encyclopedia.submitEntryForReview` | Giữ `bien_tap` | `status = soan_thao`, không đang sinh nội dung | `invalid_status`, `job_running` | → `cho_xet_duyet`, `next_roles = [xet_duyet_muc_tu]` |
| `approve` | `encyclopedia.approveEntry` | Giữ `xet_duyet_muc_tu` | `status = dang_xet_duyet` | `invalid_status` | → `dat_xet_duyet`, `next_roles = [xuat_ban_muc_tu]` |
| `reject` | `encyclopedia.rejectEntry` | Giữ `xet_duyet_muc_tu` | `status = dang_xet_duyet` | `invalid_status` | → `khong_dat_xet_duyet`, `next_roles = [bien_tap]` |
| `resume_editing` | `encyclopedia.resumeEntryEditing` | Giữ `bien_tap` | `status = khong_dat_xet_duyet` | `invalid_status` | → `soan_thao`, `next_roles = [bien_tap]` |
| `publish` | `encyclopedia.publishEntry` | Giữ `xuat_ban_muc_tu` | `status = dat_xet_duyet` | `invalid_status` | → `da_xuat_ban`, `next_roles = []` |
| `skip_publish` | `encyclopedia.skipEntryPublish` | Giữ `xuat_ban_muc_tu` | `status = dat_xet_duyet` | `invalid_status` | → `khong_xuat_ban`, `next_roles = []` |
| `reopen` | `encyclopedia.reopenEntry` | Giữ `xet_duyet_muc_tu` | `status ∈ {da_xuat_ban, khong_xuat_ban}` | `invalid_status` | 3 phần tử: → `soan_thao` `[bien_tap]`; → `cho_xet_duyet` `[xet_duyet_muc_tu]`; → `dang_xet_duyet` `[xet_duyet_muc_tu]` |
| `set_public_version` | `encyclopedia.setEntryPublicVersion` | Giữ `xuat_ban_muc_tu` | Có ít nhất một phiên bản chốt | `no_frozen_version` | — |
| `edit_seo` | `encyclopedia.updateEntrySeo` | Giữ `xuat_ban_muc_tu` | Mục từ có phiên bản đang công khai | `no_public_version` | — |

- `generate_content` không đổi trạng thái. Cảnh báo ghi đè nội dung vẫn theo D-SD04-019 (¶3.5) (`overwrite_confirmation_required`).
- `edit_seo` không phụ thuộc trạng thái bản soạn thảo (D-SD04-023 (¶3.7)).

### 3.7. [D-SD04-023] Đường dẫn và thông tin SEO (R-NFR-026 (§3.6)–R-NFR-035 (§3.6.9), R-ENC-044 (§2.3.2.6))

**Sinh slug** (R-NFR-029 (§3.6.3)):

- Từ chuỗi nguồn: bỏ dấu tiếng Việt (`đ` → `d`), chữ thường, mọi chuỗi ký tự không phải chữ/số đổi thành một `-`, bỏ `-` ở hai đầu, cắt tối đa 80 ký tự tại ranh giới `-`. Chuỗi rỗng sau khi xử lý thì dùng `muc-tu` / `cuong-vuc`.
- Trùng thì thêm `-2`, `-3`… cho tới khi không trùng. "Trùng" là trùng slug hiện hành của đối tượng cùng loại khác, hoặc trùng slug trong `public_slug_history` (D-SD04-022 (¶2.7)) của đối tượng cùng loại khác.
- Mục từ: chuỗi nguồn là `title` của phiên bản đang công khai. `SetPublicVersion` sinh lại slug khi Mục từ chưa có slug, hoặc khi slug sinh từ tiêu đề mới khác slug hiện tại (bỏ qua phần `-N`). Mục từ chưa từng công khai không có slug.
- Cương vực: chuỗi nguồn là `name`. Sinh khi tạo; sinh lại khi sửa `name`.
- Slug đổi thì slug cũ vào `public_slug_history`. Slug không bao giờ sửa tay.

**Chuyển hướng**: `public.resolveEntrySlug`, `public.resolveCulturalDomainSlug` (D-SD04-018 (¶5.4)) trả `id` và slug hiện hành. Web công khai gặp slug khác slug hiện hành thì trả 301 tới đường dẫn với slug hiện hành; không tìm thấy thì 404. Mỗi trang khai báo `canonical` theo slug hiện hành.

**Thông tin SEO của Mục từ** (R-ENC-044 (§2.3.2.6), R-NFR-030 (§3.6.4)):

- Giá trị hiệu lực của từng trường = giá trị nhập đè nếu khác `NULL`, ngược lại = giá trị tự sinh:
  - Tiêu đề: `title` phiên bản đang công khai.
  - Mô tả: tối đa 160 ký tự đầu `content_plain_text` phiên bản đang công khai, cắt ở ranh giới từ, thêm `…` nếu bị cắt.
  - Hình: `cover_file_id` của phiên bản đang công khai (D-SD04-002 (¶2.2)); `NULL` thì Web công khai dùng hình mặc định của website.
- Độ dài khuyến nghị: tiêu đề ≤ 60 ký tự, mô tả ≤ 160 ký tự. Màn hình nhập cảnh báo khi vượt, không chặn lưu; backend chỉ chặn ở giới hạn tối đa của cột (D-SD04-001 (¶2.1)).
- Chỉ vai trò Xuất bản Mục từ sửa, qua `encyclopedia.updateEntrySeo`; chỉ khi Mục từ có phiên bản đang công khai. Không tạo phiên bản, không qua quy trình xét duyệt, không phụ thuộc trạng thái bản soạn thảo, có hiệu lực ngay.
- Đổi phiên bản đang công khai: `seo_image_file_id` về `NULL` (vì tệp thuộc phiên bản cũ); `seo_title`, `seo_description` giữ nguyên.

**Phần do Web công khai dựng** (dữ liệu từ D-SD04-018 (¶5.4)):

- Thẻ `<title>`, `meta description`, Open Graph (`og:title`, `og:description`, `og:image`, `og:url`), `canonical` theo giá trị hiệu lực ở trên (R-NFR-034 (§3.6.8)).
- Dữ liệu có cấu trúc schema.org (R-NFR-031 (§3.6.5)): `Article` với tiêu đề, mô tả, hình, `dateModified` = `public_version_set_at`; `BreadcrumbList` Cương vực đầu tiên → Mục từ.
- `sitemap.xml` sinh động từ `public.listSitemapItems`; `robots.txt` tĩnh, chặn trang trò chuyện AI và trang kết quả tìm kiếm; hai loại trang này còn có `meta robots noindex` (R-NFR-028 (§3.6.2), R-NFR-032 (§3.6.6)).
- Xác minh quyền sở hữu với công cụ quản trị website của máy tìm kiếm bằng thẻ meta, giá trị lấy từ biến môi trường của Web công khai (R-NFR-032 (§3.6.6)).

**Mục từ liên quan** (R-NFR-035 (§3.6.9)) — `public.listRelatedEntries`:

1. `/assistant` tìm theo độ gần nội dung (D-SD05-010 (¶4.4) `FindRelatedEntryIDs`): lấy trung bình vector các đoạn `is_active` của Mục từ gốc; tìm các đoạn `is_active` gần nhất của Mục từ khác; điểm của mỗi Mục từ là độ tương đồng cao nhất trong các đoạn của nó, cộng 0,1 nếu có chung ít nhất một Cương vực với Mục từ gốc; lấy theo điểm giảm dần.
2. Chưa đủ số lượng (kể cả khi Mục từ gốc chưa được đánh chỉ mục) thì bù bằng Mục từ cùng Cương vực, `first_public_at` mới nhất trước, không trùng (`ListLatestPublicInDomains`, D-SD04-013 (¶4.3)).
3. Chỉ gồm Mục từ đang công khai, không gồm chính Mục từ gốc.

## 4. Kiến trúc riêng của module

### 4.1. [D-SD04-011] Sở hữu bảng

| Package | Bảng sở hữu |
|---|---|
| `/encyclopedia` | `entry`, `entry_version`, `entry_file`, `entry_knowledge_object`, `cultural_domain`, `entry_cultural_domain` |

Không có package con nào khác cho module này (khác module 03 vốn tách `/knowledge`/`/provenance`/`/gate`/`/verification`) — vì không có bước AI Verification, và cấu trúc claim/reference không cần thiết ở tầng Mục từ.

### 4.2. [D-SD04-012] Interface nội bộ gọi sang `/knowledge` (module 03)

```go
package knowledge

// Đọc nội dung phiên bản đang được sử dụng của một Hạng mục tri thức,
// phục vụ vai trò Biên tập tham chiếu khi soạn/đồng bộ Mục từ (R-ENC-017 (§2.3.3)).
// Chỉ đọc — không có quyền ghi ngược lại /knowledge.
func GetUsedVersionContent(ctx context.Context, knowledgeObjectID uuid.UUID) (*UsedVersionContent, error)

// Đọc nhẹ dạng batch: chỉ lấy used_version_id hiện tại của từng Hạng mục tri thức,
// để tính cờ "nguồn đã lỗi thời" (is_outdated) cho màn hình Mục từ — D-SD04-004 (¶2.4), D-SD04-015 (¶5.1).
func GetUsedVersionIDs(ctx context.Context, knowledgeObjectIDs []uuid.UUID) (map[uuid.UUID]*uuid.UUID, error)
```

- `UsedVersionContent` gồm `title`, danh sách `knowledge_object_file`, danh sách `claim` (chỉ đọc, để Biên tập tham khảo phát biểu gốc khi viết lại nội dung Mục từ).
- `/encyclopedia` **không** JOIN chéo bảng `knowledge_object*`/`claim*` — chỉ gọi 2 hàm này.

### 4.3. [D-SD04-013] Interface nội bộ `/encyclopedia` expose (cho `/assistant`, module 05)

```go
package encyclopedia

// Đọc nội dung phiên bản đang công khai của 1 Mục từ — dùng cho RAG (D-SD05-008 (¶4.2))
// và cho route /api/v1/public/... Trả lỗi not-found nếu current_public_version_id = NULL.
func GetPublicVersion(ctx context.Context, entryID uuid.UUID) (*EntryVersion, error)

// Liệt kê mọi Mục từ đang có phiên bản công khai, lọc theo Cương vực — dùng cho embedding job
// nền (D-SD01-004 (¶4)) và cho AI Văn Minh Việt giới hạn theo Cương vực (R-AI-004 (§2.4.3)).
func ListPublicByScope(ctx context.Context, culturalDomainID *uuid.UUID, cursor string) ([]EntrySummary, string, error)

// Đọc danh sách Cương vực đang gán cho 1 Mục từ (R-ENC-031 (§2.3.6)) — dùng cho job nền
// assistant.refresh_domain_tags (D-SD05-004 (¶3.1) bước 4 ) đồng bộ lại cột denormalize
// assistant_chunk.cultural_domain_ids. Chỉ đọc, không phụ thuộc phiên bản công khai.
func ListCulturalDomainsByEntry(ctx context.Context, entryID uuid.UUID) ([]CulturalDomain, error)

// Tra cứu hàng loạt tiêu đề Mục từ theo id — dùng cho /assistant: gắn title vào context_chunks
// gửi AI Gateway, sự kiện citations của chat, và cited_entries ở API rà soát log (D-SD05-005 (¶3.2), D-SD05-012 (¶5.1), D-SD05-013 (¶5.2)).
// Tiêu đề lấy từ phiên bản đang công khai (IsPublic = true); nếu Mục từ không còn phiên bản
// công khai, lấy tiêu đề phiên bản đã chốt mới nhất (IsPublic = false). Id không tồn tại hoặc
// chưa có phiên bản đã chốt nào thì bỏ qua, không lỗi.
func GetEntryTitles(ctx context.Context, entryIDs []uuid.UUID) (map[uuid.UUID]EntryTitle, error)

type EntryTitle struct {
    Title    string
    IsPublic bool
    Slug     string // slug hiện hành, rỗng khi Mục từ chưa có slug — dùng cho liên kết trong citations của chat
}

// Ảnh đại diện của phiên bản đang công khai, dạng URL ổn định — dùng cho sự kiện citations
// của chat (D-SD05-012 (¶5.1)). Mục từ không có phiên bản công khai hoặc cover_file_id = NULL
// thì không có trong map, không lỗi. Dạng URL theo D-SD04-018 (¶5.4).
func GetPublicCoverImages(ctx context.Context, entryIDs []uuid.UUID) (map[uuid.UUID]PublicFile, error)

type PublicFile struct {
    FileID uuid.UUID
    URL    string
}

// Thẻ Mục từ đang công khai theo id, cùng tập trường với phần tử của public.listEntries
// (D-SD04-018 (¶5.4)). Id không công khai thì bỏ qua. Giữ đúng thứ tự đầu vào.
// Dùng cho public.listRelatedEntries.
func GetPublicEntryCards(ctx context.Context, entryIDs []uuid.UUID) ([]PublicEntryCard, error)

// Mục từ đang công khai gắn ít nhất một Cương vực trong danh sách, first_public_at mới nhất trước,
// bỏ các id trong excludeIDs. Dùng bù danh sách Mục từ liên quan (D-SD04-023 (¶3.7)).
func ListLatestPublicInDomains(ctx context.Context, culturalDomainIDs []uuid.UUID, excludeIDs []uuid.UUID, limit int) ([]uuid.UUID, error)
```

### 4.4. [D-SD04-014] Các hàm ghi chính trong `/encyclopedia`

- `CreateEntry(ctx, tx, title, knowledgeObjectIDs []uuid.UUID, createdBy) (*Entry, error)` — vai trò Biên tập tạo mới (R-ENC-004 (§2.3.2.1), R-ENC-020 (§2.3.4.1)), tạo đồng thời bản soạn thảo (`status = soan_thao`, `assignee_id = createdBy` — R-ENC-012 (§2.3.2.5.1)) và các dòng `entry_knowledge_object` ban đầu.
- `UpdateDraftContent(ctx, tx, entryID, contentBlocks, callerID) error` — cập nhật `content_blocks` (đồng bộ `content_plain_text`); từ chối nếu bản soạn thảo đang ở 1 trong 4 trạng thái khoá (D-SD04-007 (¶3.1)), **hoặc nếu `callerID` không phải `assignee_id` hiện tại khi `status = soan_thao`** (R-ENC-013 (§2.3.2.5.2)). Từ chối khi còn job sinh nội dung đang chờ/đang chạy (D-SD04-019 (¶3.5)).
- `AddKnowledgeObjectLink` / `RemoveKnowledgeObjectLink(ctx, tx, entryID, knowledgeObjectID) error` — gộp/tách (R-ENC-017 (§2.3.3)).
- `MarkSynced(ctx, tx, entryID, knowledgeObjectID, syncedVersionID) error` — cập nhật `last_synced_version_id` (D-SD04-010 (¶3.4)).
- `RequestContentGeneration(ctx, tx, entryID, callerID, confirmed bool) (jobID int64, error)` — kiểm điều kiện và enqueue job `encyclopedia.generate_content` theo D-SD04-019 (¶3.5).
- `ApplyGeneratedContent(ctx, tx, entryID, requestedBy, blocks, images, syncedVersions) error` — bước 3 của job ở D-SD04-019 (¶3.5); chỉ gọi từ job.
- `RequestEntryFileUpload(ctx, entryID, fileType, fileName, callerID) (*UploadTicket, error)` — ⚠ Bổ sung: bước 1 của quy ước 2 bước presigned upload (D-SD01-003 (¶3)) áp dụng cho `entry_file` — sinh `storage_key`, ký presigned PUT URL có thời hạn ngắn, trả `{upload_url, storage_key, expires_at}`, chưa tạo dòng DB; cùng điều kiện khoá nội dung/`assignee_id` như `AddFile` bên dưới. `UploadTicket`/`DownloadTicket` dùng chung định nghĩa đã có ở D-SD03-017 (¶4.2) (không định nghĩa lại). Từ chối khi còn job sinh nội dung đang chờ/đang chạy (D-SD04-019 (¶3.5)).
- `GetEntryFileDownloadURL(ctx, fileID, callerID) (*DownloadTicket, error)` — ⚠ Bổ sung: ký presigned GET URL ngắn hạn cho 1 `entry_file` đã có, gọi theo yêu cầu (khi người dùng bấm xem/tải), không trả sẵn trong response danh sách/chi tiết — cùng cơ chế D-SD01-003 (¶3).
- `AddFile` / `RemoveFile(ctx, tx, ..., callerID) error` — quản lý `entry_file`; `AddFile` là bước 3 của quy ước upload (xác nhận `storage_key` đã nhận từ `RequestEntryFileUpload`, tạo dòng bản ghi), cùng ràng buộc khoá nội dung và điều kiện `assignee_id` ở `soan_thao`. Từ chối khi còn job sinh nội dung đang chờ/đang chạy (D-SD04-019 (¶3.5)).
- `AssignCulturalDomain` / `UnassignCulturalDomain(ctx, tx, entryID, culturalDomainID) error` — R-ENC-031 (§2.3.6). ⚠ Bổ sung (phối hợp với D-SD05-009 (¶4.3)): sau khi ghi thay đổi trong cùng transaction, enqueue job `assistant.refresh_domain_tags` với payload `{entry_id}` — chỉ enqueue tên job + payload (river `InsertTx`, cùng transaction — D-SD01-001 (¶1)/D-SD01-004 (¶4)), không import package `/assistant`, giữ đúng chiều phụ thuộc một chiều 05 → 04 (¶1).
- `CreateCulturalDomain` / `UpdateCulturalDomain` / `DeleteCulturalDomain(ctx, tx, ...) error` — quản lý danh mục Cương vực, chỉ vai trò Biên tập (R-ENC-037 (§2.3.7.5)). `CreateCulturalDomain` sinh `slug`; `UpdateCulturalDomain` sinh lại `slug` khi `name` đổi và ghi slug cũ vào `public_slug_history`; `DeleteCulturalDomain` xoá các dòng lịch sử slug của Cương vực (D-SD04-022 (¶2.7), D-SD04-023 (¶3.7)). `DeleteCulturalDomain` chỉ thành công khi không còn dòng `entry_cultural_domain` nào gắn Cương vực đó; nếu còn thì trả lỗi `cultural_domain_in_use` kèm `entry_count` (ràng buộc `ON DELETE RESTRICT`, D-SD04-006 (¶2.6), là lớp chặn cuối). Không cần enqueue job cho `/assistant`: Cương vực không gán Mục từ nào thì không có trong `assistant_chunk.cultural_domain_ids`.
- `SubmitForReview(ctx, tx, entryID) error` — `soan_thao → cho_xet_duyet`; `assignee_id` giữ nguyên (R-ENC-015 (§2.3.2.5.4)). Từ chối khi còn job sinh nội dung đang chờ/đang chạy (D-SD04-019 (¶3.5)).
- `Claim(ctx, tx, entryID, employeeID) error` — ⚠ Tổng quát cho cả `soan_thao` và `dang_xet_duyet` (R-ENC-011 (§2.3.2.5)): validate `status ∈ {soan_thao, cho_xet_duyet}`. Nếu `status = soan_thao`: validate thêm `assignee_id IS NULL` (R-ENC-013 (§2.3.2.5.2)), rồi ghi `assignee_id = employeeID`, **không đổi `status`**. Nếu `status = cho_xet_duyet`: ghi đè `assignee_id = employeeID` (không yêu cầu `NULL` trước, R-ENC-014 (§2.3.2.5.3)) và đồng thời chuyển `status → dang_xet_duyet` (D-SD04-008 (¶3.2) bước (3)).
- `Release(ctx, tx, entryID, employeeID) error` — ⚠ Bổ sung: validate `assignee_id = employeeID` và `status ∈ {soan_thao, dang_xet_duyet}`. Ghi `assignee_id = NULL`. Nếu `status = dang_xet_duyet`, đồng thời chuyển `status → cho_xet_duyet`; nếu `status = soan_thao`, không đổi `status`. Huỷ job `encyclopedia.generate_content` đang chờ của Mục từ (D-SD04-019 (¶3.5)).
- `ForceRelease(ctx, tx, entryID) error` — ⚠ Bổ sung (R-ENC-016 (§2.3.2.5.5)): cùng hành vi `Release` nhưng **không yêu cầu khớp `employeeID`** — chỉ gọi được bởi Nhân viên giữ role `quan_tri_he_thong` (route `admin`). Validate `assignee_id IS NOT NULL` và `status ∈ {soan_thao, dang_xet_duyet}`. Huỷ job `encyclopedia.generate_content` đang chờ của Mục từ (D-SD04-019 (¶3.5)).
- `RejectReview(ctx, tx, entryID, note) error` — `dang_xet_duyet → khong_dat_xet_duyet`, ghi `review_note`. `note` bắt buộc khác rỗng sau khi bỏ khoảng trắng; nếu rỗng thì trả lỗi `review_note_required` (R-ENC-025 (§2.3.5.3)).
- `ResumeEditing(ctx, tx, entryID) error` — ⚠ Bổ sung: `khong_dat_xet_duyet → soan_thao` (R-ENC-026 (§2.3.5.4)) — vai trò Biên tập xem `review_note` rồi soạn thảo lại. Không giới hạn theo `assignee_id` (nhất quán với `SubmitForReview`); `assignee_id` giữ nguyên. Chỉ hợp lệ khi `status = khong_dat_xet_duyet`.
- `ApproveReview(ctx, tx, entryID, note) error` — `dang_xet_duyet → dat_xet_duyet`, ghi `review_note`; `note` không bắt buộc (R-ENC-025 (§2.3.5.3)).
- `PublishVersion(ctx, tx, entryID, employeeID) (*EntryVersion, error)` — quyết định "Xuất bản" (D-SD04-002 (¶2.2)), chỉ vai trò Xuất bản Mục từ.
- `SkipPublish(ctx, tx, entryID, employeeID, confirmed bool) error` — quyết định "Không xuất bản".
- `ReopenFromPublished(ctx, tx, entryID, targetStatus, employeeID) error` — chỉ vai trò Xét duyệt Mục từ; `targetStatus ∈ {soan_thao, cho_xet_duyet, dang_xet_duyet}`; `assignee_id` giữ nguyên (R-ENC-015 (§2.3.2.5.4)).
- `SetPublicVersion(ctx, tx, entryID, versionID) error` — chỉ vai trò Xuất bản Mục từ; validate `frozen_at IS NOT NULL`. Trong cùng transaction: cập nhật `entry.current_public_version_id`, đặt `public_version_set_at = now()` (và `first_public_at = now()` nếu đang `NULL`); sinh lại `slug` theo D-SD04-023 (¶3.7), ghi slug cũ vào `public_slug_history`; nếu phiên bản đổi thì đặt `seo_image_file_id = NULL`. ⚠ Bổ sung (phối hợp với D-SD05-009 (¶4.3)): enqueue job `assistant.reindex_entry` với payload `{entry_id}` — cùng nguyên tắc enqueue thuần tuý như trên, không import `/assistant`.
- `UpdateEntrySeo(ctx, tx, entryID, changes, employeeID) error` — chỉ vai trò Xuất bản Mục từ (R-ENC-021 (§2.3.4.2)); validate Mục từ có phiên bản đang công khai; `seo_image_file_id` (nếu khác `NULL`) phải là tệp hình ảnh thuộc phiên bản đang công khai và được nhúng trong `content_blocks` của phiên bản đó. Không đụng tới bản soạn thảo hay trạng thái (D-SD04-023 (¶3.7)).

### 4.5. [D-SD04-020] Gọi AI Gateway sinh nội dung

- `/encyclopedia` gọi trực tiếp AI Gateway từ `/cmd/worker`, cùng cách `/verification` (D-SD03-018 (¶4.3)): job `encyclopedia.generate_content`, `related_entity = entry`.
- Ánh xạ kết quả `gateway.generateEntryDraft` sang `content_blocks`: `heading` → khối tiêu đề (cấp 2–3), `paragraph` → khối đoạn văn, `image` → khối nhúng ảnh. Tên kiểu khối cụ thể theo schema TipTap đang dùng cho `content_blocks` (do Code chọn).
- `image_id` trong kết quả phải là một trong các ảnh đã gửi đi; giá trị lạ bị bỏ qua.

## 5. Thiết kế API

Nhóm `encyclopedia/*` chỉ mount ở `/api/v1/admin/encyclopedia/...` (đã chốt ở D-SD01-002 (¶2) — không mount ở `partner`). Path dùng tiếng Anh theo `00-claude-instructions.md` mục 6.

### 5.1. [D-SD04-015] Mục từ (`entries`)

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/encyclopedia/entries` | `encyclopedia.listEntries` | Danh sách (filter `status`, `cultural_domain_id`, từ khoá) — cursor pagination; mỗi dòng trả `assignee: {id, display_name} \| null` (Người phụ trách bản soạn thảo) và `created_by: {id, display_name} \| null` — ⚠ bổ sung |
| POST | `/encyclopedia/entries` | `encyclopedia.createEntry` | Tạo mới — body `{title, knowledge_object_ids[]}` |
| GET | `/encyclopedia/entries/{id}` | `encyclopedia.getEntry` | Chi tiết bản soạn thảo (`status`, `title`, **`assignee: {id, display_name} \| null`**, **`created_by: {id, display_name} \| null`** — ⚠ bổ sung, **`review_note`** — ghi chú xét duyệt gần nhất, Biên tập cần đọc khi ở `khong_dat_xet_duyet`, D-SD04-008 (¶3.2) bước (4)) + danh sách phiên bản đã chốt + **danh sách Hạng mục tri thức đã gán, mỗi dòng kèm `last_synced_version_id` và cờ `is_outdated`** (⚠ bổ sung — so `last_synced_version_id` với `used_version_id` hiện tại lấy qua `knowledge.GetUsedVersionIDs`, D-SD04-004 (¶2.4)/D-SD04-010 (¶3.4)) + `content_generation` — `{status: pending \| running \| failed, job_id, requested_at, error_code?, error_message?} \| null` của job `encyclopedia.generate_content` gần nhất; `null` khi chưa có job hoặc job gần nhất đã xong/đã huỷ (D-SD04-019 (¶3.5)) + `slug`, `public_version_set_at`, `seo` — `{title: {override, auto}, description: {override, auto}, image: {override_file_id, auto_file_id, candidates: [{file_id}]}}` (giá trị nhập đè và giá trị tự sinh, D-SD04-023 (¶3.7)); `candidates` là các hình chọn được làm hình chia sẻ: `entry_file` hình ảnh được chèn trong `content_blocks` của phiên bản đang công khai, theo thứ tự xuất hiện, không lặp — đúng tập `UpdateEntrySeo` chấp nhận (D-SD04-014 (¶4.4)); mảng rỗng khi phiên bản không có hình; ảnh xem qua `encyclopedia.getEntryFileDownloadUrl`; `seo` là `null` khi Mục từ chưa có phiên bản công khai + `actions` (D-SD04-021 (¶3.6)) |
| PATCH | `/encyclopedia/entries/{id}/content` | `encyclopedia.updateEntryContent` | Cập nhật `content_blocks` (chặn nếu đang khoá, hoặc nếu người gọi không phải `assignee_id` hiện tại khi `status = soan_thao`); 409 `entry_content_generation_running` khi đang sinh nội dung bằng AI |
| POST | `/encyclopedia/entries/{id}/knowledge-objects` | `encyclopedia.addEntryKnowledgeObject` | Thêm ánh xạ tới 1 Hạng mục tri thức |
| DELETE | `/encyclopedia/entries/{id}/knowledge-objects/{knowledge_object_id}` | `encyclopedia.removeEntryKnowledgeObject` | Gỡ ánh xạ |
| GET | `/encyclopedia/entries/{id}/knowledge-objects/{knowledge_object_id}/source` | `encyclopedia.getEntryKnowledgeObjectSource` | Đọc nội dung `used_version` của Hạng mục tri thức nguồn (qua `GetUsedVersionContent`) để tham khảo/đồng bộ |
| POST | `/encyclopedia/entries/{id}/knowledge-objects/{knowledge_object_id}/mark-synced` | `encyclopedia.markEntryKnowledgeObjectSynced` | Đánh dấu đã đồng bộ xong |
| POST | `/encyclopedia/entries/{id}/generate-content` | `encyclopedia.generateEntryContent` | Khởi tạo nội dung bằng AI (R-ENC-038 (§2.3.8)) — body `{confirmed}`; 202 `{job_id}`; lỗi 422 `overwrite_confirmation_required`/`no_source_content`, 409 `entry_content_generation_running` (D-SD04-019 (¶3.5)) |
| POST | `/encyclopedia/entries/{id}/files/upload-url` | `encyclopedia.createEntryFileUploadUrl` | ⚠ Bổ sung — bước 1 quy ước presigned upload (D-SD01-003 (¶3)): xin `{upload_url, storage_key, expires_at}` cho 1 `entry_file` mới, body tối thiểu `{file_type, file_name}`; 409 `entry_content_generation_running` khi đang sinh nội dung bằng AI |
| POST | `/encyclopedia/entries/{id}/files` | `encyclopedia.createEntryFile` | Xác nhận file đã upload qua presigned URL (bước 3, body gồm `storage_key`) — cùng điều kiện khoá/`assignee_id`; 409 `entry_content_generation_running` khi đang sinh nội dung bằng AI |
| GET | `/encyclopedia/entries/{id}/files/{file_id}/download-url` | `encyclopedia.getEntryFileDownloadUrl` | ⚠ Bổ sung — URL tải/xem 1 `entry_file` đã có, ký presigned GET URL ngắn hạn, gọi theo yêu cầu |
| DELETE | `/encyclopedia/entries/{id}/files/{file_id}` | `encyclopedia.deleteEntryFile` | Gỡ file đính kèm; 409 `entry_content_generation_running` khi đang sinh nội dung bằng AI |
| POST | `/encyclopedia/entries/{id}/cultural-domains` | `encyclopedia.addEntryCulturalDomain` | Gán Cương vực — body `{cultural_domain_id}` |
| DELETE | `/encyclopedia/entries/{id}/cultural-domains/{cultural_domain_id}` | `encyclopedia.removeEntryCulturalDomain` | Gỡ Cương vực |
| PATCH | `/encyclopedia/entries/{id}/seo` | `encyclopedia.updateEntrySeo` | Sửa thông tin SEO (R-ENC-044 (§2.3.2.6), R-NFR-030 (§3.6.4)) — body chứa các trường cần đổi trong `seo_title`, `seo_description`, `seo_image_file_id`; giá trị `null` = về tự sinh. Chỉ vai trò Xuất bản Mục từ. 409 `entry_not_public` khi chưa có phiên bản công khai; 422 `invalid_seo_image` khi tệp không hợp lệ (D-SD04-023 (¶3.7)) |

### 5.2. [D-SD04-016] Luồng xét duyệt & Người phụ trách

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| POST | `/encyclopedia/entries/{id}/submit-for-review` | `encyclopedia.submitEntryForReview` | `soan_thao → cho_xet_duyet`; 409 `entry_content_generation_running` khi đang sinh nội dung bằng AI |
| POST | `/encyclopedia/entries/{id}/claim` | `encyclopedia.claimEntry` | Người phụ trách "nhận xử lý" (R-ENC-011 (§2.3.2.5)) — hợp lệ tại `soan_thao` (chỉ gán `assignee_id`) hoặc `cho_xet_duyet` (gán `assignee_id` **và** chuyển `status → dang_xet_duyet`, D-SD04-008 (¶3.2) bước (3)) |
| POST | `/encyclopedia/entries/{id}/release` | `encyclopedia.releaseEntry` | Người phụ trách hiện tại tự "nhả" — hợp lệ tại `soan_thao` (chỉ xoá `assignee_id`) hoặc `dang_xet_duyet` (xoá `assignee_id` **và** lùi `status → cho_xet_duyet`) |
| POST | `/encyclopedia/entries/{id}/force-release` | `encyclopedia.forceReleaseEntry` | Quản trị hệ thống cưỡng chế nhả (R-ENC-016 (§2.3.2.5.5)) — hợp lệ ở bất kỳ trạng thái nào đang có `assignee_id`, không cần khớp người gọi |
| POST | `/encyclopedia/entries/{id}/reject` | `encyclopedia.rejectEntry` | `dang_xet_duyet → khong_dat_xet_duyet` — body `{note}`, `note` bắt buộc (R-ENC-025 (§2.3.5.3)); thiếu thì HTTP 422 `review_note_required` |
| POST | `/encyclopedia/entries/{id}/resume-editing` | `encyclopedia.resumeEntryEditing` | ⚠ Bổ sung — `khong_dat_xet_duyet → soan_thao` — vai trò Biên tập xem `review_note` rồi soạn thảo lại; không giới hạn theo `assignee_id`, nhất quán với `submit-for-review` |
| POST | `/encyclopedia/entries/{id}/approve` | `encyclopedia.approveEntry` | `dang_xet_duyet → dat_xet_duyet` — body `{note?}` |
| POST | `/encyclopedia/entries/{id}/publish` | `encyclopedia.publishEntry` | Quyết định "Xuất bản" |
| POST | `/encyclopedia/entries/{id}/skip-publish` | `encyclopedia.skipEntryPublish` | Quyết định "Không xuất bản" — body `{confirmed}` |
| POST | `/encyclopedia/entries/{id}/reopen` | `encyclopedia.reopenEntry` | Mở lại từ `da_xuat_ban`/`khong_xuat_ban` — body `{target_status}` |
| POST | `/encyclopedia/entries/{id}/set-public-version` | `encyclopedia.setEntryPublicVersion` | Chọn phiên bản công khai — body `{version_id}` |

### 5.3. [D-SD04-017] Cương vực (`cultural-domains`)

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/encyclopedia/cultural-domains` | `encyclopedia.listCulturalDomains` | Danh sách — mỗi dòng trả kèm `entry_count` (int, đếm mọi dòng `entry_cultural_domain` gắn Cương vực này, không phân biệt `status` bản soạn thảo) — ⚠ bổ sung; mỗi dòng kèm `slug` |
| POST | `/encyclopedia/cultural-domains` | `encyclopedia.createCulturalDomain` | Tạo mới (mở rộng danh sách "dự kiến", R-ENC-032 (§2.3.7)) |
| PATCH | `/encyclopedia/cultural-domains/{id}` | `encyclopedia.updateCulturalDomain` | Sửa tên/mã |
| DELETE | `/encyclopedia/cultural-domains/{id}` | `encyclopedia.deleteCulturalDomain` | Xoá Cương vực (R-ENC-037 (§2.3.7.5)) — chỉ khi chưa gán Mục từ nào; còn Mục từ đang gán thì HTTP 409 `cultural_domain_in_use` kèm `entry_count`. Giao diện cảnh báo và yêu cầu xác nhận trước khi gọi |

**Quyền** (R-ENC-037 (§2.3.7.5)): xem (`GET`) — mọi Nhân viên đã đăng nhập ở kênh `admin` (dùng cho bộ lọc Cương vực khi chat AI — R-AI-004 (§2.4.3), D-SD05-012 (¶5.1) — và màn hình rà soát nhật ký hỏi đáp); Người dùng công khai xem qua `public.listCulturalDomains` (D-SD04-018 (¶5.4)). Tạo/sửa/xoá (`POST`/`PATCH`/`DELETE`) — chỉ role `bien_tap`.

### 5.4. [D-SD04-018] Nhóm `public` — `/api/v1/public/...`, không xác thực (R-PUB-002 (§2.6.1))

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/encyclopedia/entries` | `public.listEntries` | Tìm kiếm/lọc — chỉ Mục từ có `current_public_version_id` khác NULL (R-PUB-006 (§2.6.2.3)); filter `q` (từ khoá, R-PUB-004 (§2.6.2.1)), `cultural_domain_id` (R-PUB-005 (§2.6.2.2)); sắp xếp `sort`, phân trang `limit`/`cursor` |
| GET | `/encyclopedia/entries/{id}` | `public.getEntry` | Nội dung phiên bản công khai (R-PUB-007 (§2.6.3)) |
| GET | `/encyclopedia/cultural-domains` | `public.listCulturalDomains` | Danh sách Cương vực, cho bộ lọc |
| GET | `/encyclopedia/entries/slug/{slug}` | `public.resolveEntrySlug` | Tra Mục từ đang công khai theo slug hiện hành hoặc slug cũ → `{id, slug}` (slug hiện hành); không có thì 404 (D-SD04-023 (¶3.7)) |
| GET | `/encyclopedia/cultural-domains/slug/{slug}` | `public.resolveCulturalDomainSlug` | Như trên, cho Cương vực → `{id, slug}` |
| GET | `/encyclopedia/entries/{id}/related` | `public.listRelatedEntries` | Mục từ liên quan (R-NFR-035 (§3.6.9)) — `limit` 1–12, mặc định 6; phần tử cùng dạng `public.listEntries`. Handler ở `/cmd/api` ghép `assistant.FindRelatedEntryIDs`, `encyclopedia.ListLatestPublicInDomains`, `encyclopedia.GetPublicEntryCards` (D-SD04-023 (¶3.7)) |
| GET | `/sitemap-items` | `public.listSitemapItems` | `{entries: [{slug, updated_at}], cultural_domains: [{slug, updated_at}]}` — mọi Mục từ đang công khai (`updated_at` = `public_version_set_at`) và mọi Cương vực (`updated_at`). Không phân trang (R-NFR-032 (§3.6.6)) |
| GET | `/files/{file_id}` | `public.getFile` | Tệp của phiên bản Mục từ đang công khai: 302 tới presigned GET URL thời hạn 10 phút, `Cache-Control: public, max-age=300`. Tệp không thuộc phiên bản đang công khai nào thì 404 |
| GET | `/today/items` | `public.listTodayItems` | Tin "Hôm nay" đang trong thời gian hiển thị (R-PUB-013 (§2.6.6), R-PUB-017 (§2.6.6.4)) — chi tiết ở bullet `public.listTodayItems` dưới bảng |

- URL đầy đủ: `/api/v1/public/encyclopedia/...`. Path trùng với endpoint nhóm `admin` ở D-SD04-015 (¶5.1), D-SD04-017 (¶5.3) nhưng là endpoint riêng, operationId tiền tố `public` (`common/requirements-design-sync.md` mục 2.5): chỉ đọc phiên bản đang công khai, không trả bản soạn thảo hay trường nội bộ (`status`, `assignee_id`, `entry_count`…).
- **Lọc Cương vực đa chọn**: `cultural_domain_id` lặp được nhiều lần (`?cultural_domain_id=a&cultural_domain_id=b`); trả Mục từ gắn **ít nhất một** Cương vực đã chọn (OR). Không truyền thì không lọc. ⚠
- **Sắp xếp và phân trang `public.listEntries`** ⚠:
  - `sort`:
    - `latest`: theo `entry.first_public_at` giảm dần, Mục từ được công khai lần đầu gần nhất đứng trước; đổi phiên bản công khai không làm thay đổi thứ tự. Cùng thời điểm thì theo `id`.
    - `relevance`: theo mức khớp từ khoá, chỉ dùng khi có `q`.
    - Không truyền `sort`: có `q` thì dùng `relevance`, không có `q` thì dùng `latest`. Truyền `relevance` mà không có `q` thì trả 400.
  - `limit`: số phần tử mỗi trang, 1–50, mặc định 20.
  - `cursor`: cursor pagination (D-SD01-003 (¶3)). Cursor gắn với `sort` của lượt gọi đầu; dùng cursor với `sort` khác thì trả 400.
  - Section "Mục từ nổi bật" ở Trang chủ (D-PUB-001 (¶4.1)) gọi `sort=latest&limit=4`.
- **Response `public.listEntries`** — mỗi phần tử: ⚠
  - `id`, `slug`, `title` (tiêu đề phiên bản công khai);
  - `excerpt` — tối đa 200 ký tự đầu của `content_plain_text` phiên bản công khai, cắt ở ranh giới từ, thêm `…` nếu bị cắt; `null` khi không có nội dung text;
  - `cover_image` — `{file_id, url}` của `cover_file_id` (D-SD04-002 (¶2.2)), hoặc `null`; `url` theo bullet "URL tệp" dưới đây;
  - `cultural_domain_ids` — sắp theo thứ tự gán (`entry_cultural_domain.created_at`, D-SD04-006 (¶2.6)); phần tử đầu là "Cương vực đầu tiên" hiển thị trên card.
- **Response `public.getEntry`**: `id`, `slug`, `title`, `content_blocks`, `cultural_domain_ids` (cùng thứ tự như trên), `cover_image` (như trên), `files` — mỗi file `{id, file_type, url}` của phiên bản công khai, `first_public_at`, `public_version_set_at`, `seo` — `{title, description, image}` là giá trị hiệu lực (D-SD04-023 (¶3.7)), `image` dạng `{file_id, url}` hoặc `null`. Không trả `storage_key`. ⚠
- **URL tệp** ⚠ (ngoại lệ của quy ước "ký theo yêu cầu" ở D-SD01-003 (¶3), chỉ áp dụng nhóm `public`): `url` là URL ổn định `<PUBLIC_FILE_BASE_URL>/files/{file_id}` (biến môi trường, địa chỉ tuyệt đối của nhóm route `public`), trỏ tới `public.getFile`. URL không hết hạn, dùng được cho Open Graph và cho trang được cache. Khi đổi phiên bản công khai, tệp của phiên bản cũ trả 404; hình chia sẻ mà mạng xã hội đã lưu từ trước có thể mất cho tới khi mạng xã hội đọc lại trang.
- `public.listCulturalDomains`: `{id, name, code, slug}` mỗi Cương vực, không có `entry_count`.
- **`public.listTodayItems`** ⚠ — section "Hôm nay" trên trang chủ:
  - Response `{items: [{id, title, source_name, published_at, url, entries}]}`. `title` là tiêu đề gốc của tin, `source_name` là tên nguồn, `published_at` là thời gian đăng, `url` là đường dẫn bài gốc trên website nguồn. `entries` là các Mục từ liên quan, mỗi phần tử cùng dạng phần tử của `public.listEntries`.
  - Chỉ gồm tin đã duyệt và đang trong khoảng thời gian hiển thị, sắp theo `published_at` giảm dần. `entries` chỉ gồm Mục từ đang công khai; tin không còn Mục từ công khai nào thì không có trong danh sách. Không trả nội dung bài viết của nguồn.
  - `items` rỗng thì Web công khai ẩn section. Số tin hiển thị cùng lúc do Web công khai quyết định.
  - Web công khai ghi lượt bấm vào Mục từ của một tin bằng sự kiện Umami `today_entry_click`, thuộc tính `{item_id, entry_id}` (R-NFR-036 (§3.6.10)).
  - Phần quản lý tin chưa thiết kế. Tới khi có, endpoint trả `{items: []}`. Riêng khi `DEV_MODE=true` (D-SD01-009 (¶9)), endpoint trả 3 tin mẫu cố định trong code, `url` trỏ tới `https://example.com/…`, mỗi tin gắn 1–2 Mục từ đang công khai chọn ngẫu nhiên ở mỗi lần gọi; chưa có Mục từ công khai nào thì trả rỗng.

Mọi endpoint ghi ở 5.1–5.3 có audit log — `action_type` và `detail` theo danh mục sự kiện audit ở D-SD01-002 (¶2).

## 6. Vấn đề mở / giả định

- **Khởi tạo nội dung bằng AI** (D-SD04-019 (¶3.5)) ⚠ các điểm do thiết kế chọn: khoá sửa nội dung khi job còn chạy; bỏ kết quả khi đổi trạng thái/Người phụ trách; tự cập nhật `last_synced_version_id`; ảnh của Hạng mục tri thức được gắn sẵn vào Mục từ.
- **`content_plain_text`** (D-SD04-002 (¶2.2)) — ⚠ cột mirror phục vụ full-text search, đồng bộ ở tầng ứng dụng mỗi khi `content_blocks` đổi — chi tiết kỹ thuật, không ảnh hưởng nghiệp vụ. Nay cũng là nguồn dữ liệu cho `/assistant` (module 05) đánh chỉ mục RAG.
- **`last_synced_version_id`** (D-SD04-004 (¶2.4)) và cờ **`is_outdated`** ở `encyclopedia.getEntry` — `GET /encyclopedia/entries/{id}` hiện thực cảnh báo nguồn lỗi thời R-ENC-018 (§2.3.3.1) — so với phiên bản đang được sử dụng của Hạng mục tri thức nguồn. Cờ tính tại chỗ qua `knowledge.GetUsedVersionIDs` (D-SD03-017 (¶4.2)), không thêm cột lưu trữ.
- **`review_note`** (D-SD04-002 (¶2.2), D-SD04-014 (¶4.4), D-SD04-015 (¶5.1), D-SD04-016 (¶5.2)) hiện thực nhận xét tổng thể của vai trò Xét duyệt Mục từ (R-ENC-025 (§2.3.5.3)–R-ENC-026 (§2.3.5.4)): bắt buộc khi không đạt, tuỳ chọn khi đạt; trả về ở `encyclopedia.getEntry` — `GET /encyclopedia/entries/{id}` để vai trò Biên tập đọc.
- **`ListCulturalDomainsByEntry` (D-SD04-013 (¶4.3))** — ⚠ bổ sung 2026-09-23: D-SD05-004 (¶3.1) bước 4 đã mô tả job `assistant.refresh_domain_tags` "đọc lại danh sách Cương vực hiện tại của Mục từ qua interface đọc của `/encyclopedia`", nhưng D-SD04-013 (¶4.3) trước đó chỉ expose `GetPublicVersion`/`ListPublicByScope` — không hàm nào trả Cương vực. Thêm hàm này để job có đúng thứ cần gọi; không đổi hành vi nghiệp vụ.
- **`entry_knowledge_object.knowledge_object_id` dùng `ON DELETE RESTRICT`** (D-SD04-004 (¶2.4)) — ⚠ bổ sung 2026-09-23, hệ quả của cơ chế xoá Hạng mục tri thức mới ở module 03 (D-SD03-005 (¶2.5), D-SD03-017 (¶4.2)): một Hạng mục tri thức đang được Mục từ tham chiếu thì không xoá được, ràng buộc chặn ở tầng CSDL để `/knowledge` không phải gọi ngược sang `/encyclopedia` (giữ hướng phụ thuộc một chiều 04 → 03). Không đổi hành vi nào của module 04.
- **Quản lý Cương vực** (D-SD04-005 (¶2.5), D-SD04-006 (¶2.6), D-SD04-014 (¶4.4), D-SD04-017 (¶5.3)) hiện thực R-ENC-037 (§2.3.7.5): vai trò Biên tập thêm/sửa/xoá, chỉ xoá được khi chưa gán Mục từ nào (`ON DELETE RESTRICT` + kiểm tra ở tầng service).
- **Không áp dụng ngoại lệ "xem toàn bộ" của Quản trị hệ thống** (khác R-KB-007 (§2.2.1.5) module 03) — 3 role của module này đều là role theo chức năng (không theo phạm vi Đề tài), nên Nhân viên giữ các role này vốn đã thấy toàn bộ Mục từ, không cần cơ chế ngoại lệ riêng. Ngoại lệ: `force-release` (R-ENC-016 (§2.3.2.5.5)) vẫn chỉ dành riêng cho `quan_tri_he_thong`, như module 03.
- Chưa có cơ chế gợi ý/tự động gán Cương vực (R-ENC-031 (§2.3.6): "có thể tự động hoá/gợi ý trong tương lai") — ngoài phạm vi hiện tại, chỉ gán thủ công.
- Tên bảng/field/hàm nội bộ dùng tiếng Anh (`entry`, `entry_version`, `cultural_domain`...) và path API dùng tiếng Anh (`/encyclopedia/entries`, `/encyclopedia/cultural-domains`...) theo nguyên tắc chung ở `00-claude-instructions.md` mục 6.
- **Enqueue job cho `/assistant` ở `AssignCulturalDomain`/`UnassignCulturalDomain`/`SetPublicVersion` (D-SD04-014 (¶4.4))** — để module 05 biết khi nào cần re-index mà không phải phụ thuộc ngược vào `/encyclopedia`. Chi tiết cơ chế job (`assistant.reindex_entry`, `assistant.refresh_domain_tags`) xem D-SD05-004 (¶3.1) và D-SD05-009 (¶4.3).
- **Endpoint `resume-editing` cho transition `khong_dat_xet_duyet → soan_thao`** (D-SD04-008 (¶3.2) bước (4), D-SD04-014 (¶4.4), D-SD04-016 (¶5.2)) — ⚠ bổ sung: hành vi nghiệp vụ có sẵn trong đặc tả gốc (R-ENC-026 (§2.3.5.4)), thực thi nhất quán với cách xử lý điểm tương tự ở module 03 (`resume-research`) — hàm không giới hạn quyền gọi theo `assignee_id`, bất kỳ Nhân viên nào giữ vai trò Biên tập đều gọi được, nhất quán với `submit-for-review`.
- **Upload/download file qua presigned URL cho `entry_file`, tên hiển thị (`display_name`) kèm `assignee`/`created_by` trong response** (D-SD04-014 (¶4.4), D-SD04-015 (¶5.1)) — ⚠ bổ sung 2026-09-23: hoàn thiện kỹ thuật cho quy ước presigned URL đã chốt ở D-SD01-003 (¶3) (áp dụng cụ thể cho `entry_file`, song song `knowledge_object_file`/`source_file` ở module 03), và cho việc hiển thị tên người phụ trách/người tạo ở giao diện Admin nội bộ thay vì chỉ có UUID thô — không đổi hành vi nghiệp vụ nào.
- **`entry_count` ở `encyclopedia.listCulturalDomains` — `GET /encyclopedia/cultural-domains`** (D-SD04-017 (¶5.3)) — ⚠ bổ sung 2026-09-23: hoàn thiện kỹ thuật cho màn hình Quản lý Cương vực (D-ADM-020 (¶4.20)) cần hiển thị số Mục từ đang gán mỗi Cương vực; trước đó endpoint danh sách chưa trả trường này. Đếm mọi dòng `entry_cultural_domain`, không phân biệt `status` (màn hình quản trị nội bộ, khác `public.listEntries` chỉ lọc Mục từ đã có phiên bản công khai, D-SD04-018 (¶5.4)).
- **`GetEntryTitles`** (D-SD04-013 (¶4.3)) — ⚠ bổ sung: interface đọc hàng loạt tiêu đề Mục từ cho `/assistant` — D-SD06-004 (¶3.2) yêu cầu `title` trong `context_chunks` nhưng `assistant_chunk` không lưu tiêu đề, và API rà soát log cần tiêu đề cho cả lượt hỏi cũ. Fallback về phiên bản đã chốt mới nhất khi Mục từ không còn công khai, kèm cờ `IsPublic`.
- **Danh sách thao tác** (D-SD04-021 (¶3.6)) hiện thực R-NFR-039 (§3.7.2)–R-NFR-040 (§3.7.3). ⚠ Mã `action` và cách nhóm endpoint theo thao tác là quyết định của thiết kế.
- **Slug, thông tin SEO, URL tệp công khai, Mục từ liên quan** (D-SD04-001 (¶2.1), D-SD04-005 (¶2.5), D-SD04-022 (¶2.7), D-SD04-023 (¶3.7), D-SD04-018 (¶5.4)) hiện thực R-NFR-028 (§3.6.2)–R-NFR-035 (§3.6.9), R-ENC-044 (§2.3.2.6). ⚠ Quyết định của thiết kế: quy tắc sinh slug; độ dài khuyến nghị 60/160 ký tự; xoá hình chia sẻ đã chọn khi đổi phiên bản công khai; công thức điểm Mục từ liên quan và số lượng mặc định 6; thời hạn presigned URL 10 phút của `public.getFile`.
- **Section "Hôm nay"** (R-PUB-013 (§2.6.6)–R-PUB-018 (§2.6.6.5)): mới có hợp đồng `public.listTodayItems` (D-SD04-018 (¶5.4)). Chưa thiết kế: nơi đặt module, dữ liệu nguồn tin và tin, đọc tin định kỳ, agent AI gợi ý Mục từ (dự kiến chạy ở AI Gateway, dữ liệu và duyệt ở Go), duyệt và gỡ tin, tham số cấu hình (R-CFG-010 (§2.8.4.5)), audit (R-NFR-004 (§3.1.2)), thời hạn tin theo R-NFR-042 (§3.7.5).
