# Thiết Kế Module: Cơ Sở Dữ Liệu Văn Hóa (Văn Minh Việt)

> **Trạng thái**: ¶1–6 đã chốt — Module 03 hoàn tất toàn bộ 6 mục (cập nhật 2026-09-23: bổ sung quyền xem tiến độ của Chủ nhiệm đề tài, cơ chế xoá Đề tài nghiên cứu rỗng/xoá Hạng mục tri thức, và hoàn thiện kỹ thuật cho upload/download file qua presigned URL, tên hiển thị/số đếm kèm trong response danh sách, tìm kiếm Nhân viên cho Chủ nhiệm đề tài, và làm rõ quyền `sources`/`mark-ready` — xem D-SD03-017 (¶4.2), D-SD03-021 (¶5.1)–D-SD03-023 (¶5.3), ¶6; cùng ngày, đã đồng bộ trích dẫn — Requirements chính thức chốt các đề nghị trên thành R-KB-012 (§2.2.1.7), R-KB-047 (§2.2.3.12)–R-KB-049 (§2.2.3.14), R-KB-073 (§2.2.5.5), R-PTN-009 (§2.7.3.5), R-NFR-004 (§3.1.2), khớp đúng nội dung đã thiết kế).
>
> Tên file dùng `cultural-knowledge-base` thay vì dịch sát nghĩa "cultural-database", để tránh gây hiểu nhầm với hạ tầng lưu trữ/hệ quản trị cơ sở dữ liệu (DBMS) — nội dung module này là mô hình nghiệp vụ cho kho tri thức văn hoá (tư liệu → nghiên cứu → dữ liệu chuẩn), không phải thiết kế hạ tầng CSDL.

## 1. Tổng quan module

- Module lõi của hệ thống, hiện thực chuỗi giá trị `Tư liệu Hán Nôm → Nghiên cứu → Dữ liệu chuẩn` (đặc tả gốc R-KB-001 (§2.2) — đoạn mở đầu, mô tả tổng quan luồng nghiệp vụ chính).
- Ánh xạ tới các package Go đã chốt ở D-SD01-002 (¶2): `/ingestion` (đồng bộ Tư liệu gốc từ MinIO/S3 — nhận tín hiệu qua webhook đã debounce, gọi `/knowledge.SyncSourceFiles`, xem D-SD03-020 (¶4.5)), `/knowledge` (Đề tài nghiên cứu, Tư liệu gốc, Hạng mục tri thức), `/provenance` (truy vết claim ↔ tư liệu), `/gate` (workflow xét duyệt Hạng mục tri thức), `/verification` (AI Verification). Module 03 mô tả mô hình dữ liệu và nghiệp vụ dùng chung cho toàn bộ nhóm package này; ranh giới kỹ thuật chi tiết giữa các package ở ¶4.
- Phụ thuộc vào module 02 (`/identity`): dùng interface nội bộ tổng quát `ProvisionScopeRoles`/`RevokeScopeRoles` (đã chốt ở D-SD02-008 (¶4)) để tự sinh role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` khi tạo Đề tài nghiên cứu (R-KB-006 (§2.2.1.4)); `AssignScopeRole`/`RevokeScopeRole`/`ListEmployeesByScope` (⚠ bổ sung, D-SD02-008 (¶4)) để quản lý nhân sự của đề tài (gán/gỡ Chủ nhiệm đề tài, Nghiên cứu, Xét duyệt — R-KB-073 (§2.2.5.5), D-SD03-017 (¶4.2) bên dưới); và `SearchEmployees` (⚠ bổ sung, D-SD02-008 (¶4)) để Chủ nhiệm đề tài tìm Nhân viên khi thêm Nghiên cứu/Xét duyệt.
- Không phụ thuộc ngược từ module 02, 04, 05 vào module 03 ngoài các interface nội bộ đã liệt kê ở tài liệu 01 (ví dụ `/encyclopedia` gọi sang `/knowledge` để đọc Hạng mục tri thức khi tạo Mục từ).

## 2. Mô hình dữ liệu

Quy ước chung (khoá chính UUID, `snake_case`, tách bảng phiên bản khỏi bảng định danh cha, tránh ENUM cứng...) áp dụng theo `00-claude-instructions.md` mục 6, không nhắc lại ở từng bảng bên dưới trừ khi cần làm rõ cách áp dụng cụ thể.

### 2.1. [D-SD03-001] `research_topic` (Đề tài nghiên cứu, R-KB-002 (§2.2.1))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `name` | text | R-KB-004 (§2.2.1.2) |
| `status` | text | R-KB-009 (§2.2.1.6) — `chuan_bi_tu_lieu` / `tu_lieu_san_sang`; kiểu `text` theo `00-claude-instructions.md` mục 6 (không dùng ENUM). Chi tiết luồng ở D-SD03-010 (¶3.1) |
| `created_at` | timestamptz | |

- Khi tạo mới: gọi `identity.ProvisionScopeRoles(ctx, tx, "research_topic", id, []identity.ScopeRoleSpec{{Name: "chu_nhiem_de_tai", IsSingular: true}, {Name: "nghien_cuu", IsSingular: false}, {Name: "xet_duyet", IsSingular: false}})` (R-KB-006 (§2.2.1.4)) — `/knowledge` tự quyết định `is_singular` cho từng role nó định nghĩa, truyền tường minh qua `ScopeRoleSpec` (D-SD02-008 (¶4), `02` ¶6) — chi tiết giao dịch/atomic ở ¶4.
- **Xoá đề tài (xoá cứng)** (R-KB-012 (§2.2.1.7)): chỉ Nhân viên giữ role `quan_tri_he_thong`, và **chỉ khi đề tài đang rỗng** — không còn dòng `knowledge_object` nào thuộc đề tài (chưa từng tạo, hoặc đã xoá hết — D-SD03-005 (¶2.5)). Không có điều kiện nào khác: vẫn xoá được dù đề tài đã ở `tu_lieu_san_sang` và dù còn Tư liệu gốc đã gán (R-KB-013 (§2.2.1.7.1)). Trình tự trong một giao dịch: gọi `identity.RevokeScopeRoles(ctx, tx, id)` **trước** (R-KB-014 (§2.2.1.7.2)) (gỡ 3 role theo phạm vi + `employee_role` tương ứng — cơ chế `ON DELETE CASCADE` phía `employee_role` đã chốt ở D-SD02-008 (¶4)), rồi xoá dòng `research_topic`, kéo theo `research_topic_source` (chỉ gỡ liên kết). **Tư liệu gốc (`source`/`source_file`) không bị xoá** (R-KB-015 (§2.2.1.7.3)) — một tư liệu dùng chung nhiều đề tài (D-SD03-002 (¶2.2)), và file vật lý nằm ngoài hệ thống (D-SD03-020 (¶4.5)). Hàm ở D-SD03-017 (¶4.2), endpoint ở D-SD03-021 (¶5.1).
- **Quyền tạo**: chỉ Nhân viên giữ role `quan_tri_he_thong` được tạo Đề tài nghiên cứu (R-KB-006 (§2.2.1.4), R-GEN-011 (§1.2.3.3)) — kiểm ở tầng service, chỉ mở route ở nhóm `admin`.
- **Quyền quản lý nhân sự đề tài** (R-KB-073 (§2.2.5.5), D-SD03-017 (¶4.2)): gán/đổi **Chủ nhiệm đề tài** — chỉ Quản trị hệ thống. Gán/gỡ **Nghiên cứu**/**Xét duyệt** — Quản trị hệ thống hoặc Chủ nhiệm đề tài của chính đề tài đó.
- **Có trạng thái riêng** (R-KB-009 (§2.2.1.6)), tách biệt hoàn toàn với `status` của bản soạn thảo Hạng mục tri thức (D-SD03-006 (¶2.6)) — phản ánh tiến độ chuẩn bị tư liệu cho đề tài, xem D-SD03-010 (¶3.1).

### 2.2. [D-SD03-002] `research_topic_source` (bảng nối, R-KB-005 (§2.2.1.3))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `research_topic_id` | UUID | FK → `research_topic.id` |
| `source_id` | UUID | FK → `source.id` |

- Khoá chính composite `(research_topic_id, source_id)` — quan hệ nhiều-nhiều giữa Đề tài nghiên cứu và Tư liệu gốc.
- Việc nhập Tư liệu gốc và gán/gỡ cho đề tài do **vai trò Nhập liệu** (`nhap_lieu`, R-KB-069 (§2.2.5.1)) thực hiện — role theo chức năng, **không giới hạn theo phạm vi đề tài** (vì một Tư liệu gốc có thể được nhiều đề tài cùng sử dụng). Gán bổ sung được bất kỳ lúc nào, kể cả sau khi đề tài đã ở `tu_lieu_san_sang` (R-KB-011 (§2.2.1.6.2)) và đang có Hạng mục tri thức được nghiên cứu/xét duyệt.

### 2.3. [D-SD03-003] `source` (Tư liệu gốc, R-KB-017 (§2.2.2))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | R-KB-018 (§2.2.2.1) |
| `name` | text | R-KB-019 (§2.2.2.2) — tên/tiêu đề tư liệu |
| `type` | text | R-KB-020 (§2.2.2.3) — danh sách loại tư liệu mở, theo nguyên tắc chung ở `00-claude-instructions.md` mục 6 (không dùng ENUM) |
| `storage_prefix` | text | ⚠ Bổ sung — đường dẫn thư mục gốc trong MinIO/S3 chứa toàn bộ file của tư liệu này; việc nạp file vào thư mục nằm ngoài hệ thống, hệ thống chỉ đọc lại qua `SyncSourceFiles` (D-SD03-017 (¶4.2), D-SD03-020 (¶4.5)) |
| `last_synced_at` | timestamptz (nullable) | ⚠ Bổ sung — thời điểm lần `SyncSourceFiles` gần nhất chạy xong (thủ công hoặc qua webhook debounce) |
| `created_at` | timestamptz | |

- Cơ chế đồng bộ nội dung thư mục MinIO/S3 tương ứng (file mới/mất) — xem D-SD03-020 (¶4.5).

### 2.4. [D-SD03-004] `source_file` (R-KB-021 (§2.2.2.4) — không có cột thứ tự)

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | R-KB-022 (§2.2.2.4.1) |
| `source_id` | UUID | FK → `source.id` |
| `file_type` | text | R-KB-023 (§2.2.2.4.2) — lưu tường minh loại file (text/image/audio/video) để `claim_reference.location` biết cách diễn giải (xem 2.9) |
| `storage_key` | text | Đường dẫn đầy đủ file trong MinIO/S3 (nằm trong `storage_prefix` của `source` cha) — do `SyncSourceFiles` phát hiện và ghi khi liệt kê thư mục, không qua presigned URL/app upload (xem D-SD01-003 (¶3), D-SD01-005 (¶5)) — không lưu blob trong DB |
| `is_missing` | boolean, default `false` | `SyncSourceFiles` bật cờ này khi không còn thấy file tại `storage_key` trong lần liệt kê thư mục gần nhất; **không xoá dòng** để giữ nguyên vẹn FK từ `claim_reference` (truy vết không được vỡ). Về nguyên tắc Tư liệu gốc không được để mất file; đây là cơ chế phòng hộ cho trường hợp phát sinh ngoài dự kiến — xem D-SD03-012 (¶3.3) bước (4), D-SD03-023 (¶5.3)/D-SD03-024 (¶5.4) |
| `missing_since` | timestamptz (nullable) | Thời điểm phát hiện file biến mất; dùng để cảnh báo Quản trị hệ thống/vai trò Xét duyệt khi họ **mở xem** Hạng mục tri thức có Tham chiếu trỏ tới file này (D-SD03-023 (¶5.3)/D-SD03-024 (¶5.4) — chỉ cần cảnh báo khi mở xem, không cần thông báo chủ động). Khi file xuất hiện lại tại đúng `storage_key`, `SyncSourceFiles` tự gỡ cờ (`is_missing = false`, `missing_since = NULL`) |
| `metadata` | JSONB | Kết quả job nền trích metadata khi ingest (đã chốt ở D-SD01-004 (¶4)), phục vụ R-KB-081 (§2.2.6.6.1) |
| `transcript_storage_key` | text (nullable) | ⚠ Đề xuất bổ sung — trỏ tới file JSON transcript trích xuất khi ingest, trong Object storage, cấu trúc tuỳ `file_type`: văn bản `[{page, line, text}, ...]`; âm thanh/phim `[{start_time, end_time, text}, ...]` (transcript ASR theo đoạn thời gian). Chỉ tạo khi phù hợp (ví dụ audio phỏng vấn/bài hát có lời thì có, tiếng ồn nền/nhạc không lời thì có thể bỏ trống). Dùng chung cho giao diện nghiên cứu (chọn đúng vị trí/thời điểm khi tạo Tham chiếu) và AI Verification (tra cứu nhanh, không phải chạy lại ASR/phân tích file gốc mỗi lần — R-KB-077 (§2.2.6.5) cho phép chạy lại nhiều lần). Riêng phần khung ảnh (hình ảnh/khung hình video) vẫn cần VLM đọc trực tiếp pixel, transcript không thay thế được. |
| `created_at` | timestamptz | |

### 2.5. [D-SD03-005] `knowledge_object` (Hạng mục tri thức — bảng định danh cha, R-KB-026 (§2.2.3.1))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | R-KB-026 (§2.2.3.1) |
| `research_topic_id` | UUID | NOT NULL, FK → `research_topic.id` (R-KB-039 (§2.2.3.9)) |
| `used_version_id` | UUID (nullable) | R-KB-030 (§2.2.3.4.1) "Phiên bản đang được sử dụng" — FK → `knowledge_object_version.id`, **chỉ được trỏ tới dòng đã chốt** (`frozen_at IS NOT NULL`); do **vai trò Xuất bản** (R-KB-072 (§2.2.5.4)) chọn/đổi, độc lập với workflow đang diễn ra (D-SD03-013 (¶3.4)); mặc định `NULL` cho tới lần chọn đầu tiên |
| `created_by` | UUID | R-KB-047 (§2.2.3.12) "Người tạo" — FK → `employee.id`, Nhân viên giữ vai trò Nghiên cứu đã tạo hạng mục này (R-KB-040 (§2.2.3.10)); bất biến sau khi tạo, không đổi khi Người phụ trách (`assignee_id`) được nhận/nhả lại bởi người khác |
| `created_at` | timestamptz | R-KB-048 (§2.2.3.13) "Ngày giờ tạo" — bất biến, khác với `created_at` của `knowledge_object_version` (R-KB-031 (§2.2.3.5) "Ngày giờ tạo phiên bản", gắn với từng phiên bản đã chốt) |

- Bản đang soạn thảo được xác định bằng dòng duy nhất có `frozen_at IS NULL` của hạng mục (D-SD03-006 (¶2.6)), không cần cột con trỏ riêng — nhờ vậy cũng không cần khoá ngoại vòng giữa `knowledge_object` và `knowledge_object_version`.
- **Tạo mới**: do **vai trò Nghiên cứu** của đề tài thực hiện (R-KB-040 (§2.2.3.10)), kể cả đặt Tiêu đề. **Điều kiện: Đề tài nghiên cứu cha phải đang ở `tu_lieu_san_sang`** (R-KB-011 (§2.2.1.6.2)) — khi đề tài còn ở `chuan_bi_tu_lieu` thì không tạo được hạng mục nào. Hệ thống tạo đồng thời 1 dòng `knowledge_object_version` là bản soạn thảo đầu tiên (`frozen_at = NULL`, `status = dang_nghien_cuu`, `assignee_id = createdBy` — người tạo tự động là Người phụ trách đầu tiên, R-KB-042 (§2.2.3.11.1), xem D-SD03-006 (¶2.6)).
- **Xoá (xoá cứng)** (R-KB-049 (§2.2.3.14)): được phép khi **cả 3 điều kiện** đúng — (a) hạng mục **chưa có phiên bản nào đã chốt** (không tồn tại dòng `knowledge_object_version` có `frozen_at IS NOT NULL`, kéo theo `used_version_id IS NULL`) (R-KB-050 (§2.2.3.14.1)); (b) bản soạn thảo đang ở `dang_nghien_cuu` (D-SD03-011 (¶3.2)) (R-KB-051 (§2.2.3.14.2)); (c) chưa bị Mục từ nào tham chiếu (bảng nối `entry_knowledge_object`, module 04 — cơ chế kiểm ở D-SD03-017 (¶4.2)) (R-KB-052 (§2.2.3.14.3)). Người gọi: Nhân viên giữ role `quan_tri_he_thong`, **hoặc** Chủ nhiệm đề tài (`chu_nhiem_de_tai`) của đề tài cha, **hoặc** `assignee_id` hiện tại của bản soạn thảo (vai trò Nghiên cứu đang phụ trách) (R-KB-053 (§2.2.3.14.4)). ⚠ Khi `assignee_id IS NULL` (chưa ai `Claim`), điều kiện (c) trong danh sách người gọi không thoả mãn được bởi bất kỳ ai — nên trên thực tế chỉ Quản trị hệ thống hoặc Chủ nhiệm đề tài xoá được; một Nhân viên Nghiên cứu bình thường phải `Claim` trước để trở thành `assignee_id` rồi mới xoá được (R-KB-053 (§2.2.3.14.4)). Xoá kéo theo bản soạn thảo và toàn bộ `knowledge_object_file`/`claim`/`claim_reference` của nó (D-SD03-017 (¶4.2)). Mục đích chính: đưa Đề tài nghiên cứu về trạng thái rỗng để xoá được (D-SD03-001 (¶2.1)).

### 2.6. [D-SD03-006] `knowledge_object_version` (bản soạn thảo + các phiên bản đã chốt, R-KB-029 (§2.2.3.4))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `knowledge_object_id` | UUID | FK → `knowledge_object.id` |
| `version_number` | int (nullable) | ⚠ Bổ sung để sắp thứ tự — chỉ cấp cho dòng đã chốt (1, 2, 3…), `NULL` với bản soạn thảo |
| `title` | text | R-KB-027 (§2.2.3.2) |
| `status` | text (nullable) | R-KB-028 (§2.2.3.3) — trạng thái workflow (R-KB-074 (§2.2.6), chi tiết D-SD03-011 (¶3.2)–D-SD03-012 (¶3.3)). **Chỉ bản soạn thảo** (`frozen_at IS NULL`) mang giá trị — kể cả 2 trạng thái cuối `da_xuat_ban`/`khong_xuat_ban` (D-SD03-011 (¶3.2)), vì bản soạn thảo vẫn là chính dòng này, không bị thay thế khi chốt phiên bản (xem "Cơ chế chốt phiên bản" bên dưới). Dòng đã chốt (`frozen_at IS NOT NULL`) là snapshot bất biến, **không còn vận hành workflow**, nên `status = NULL` — bản thân việc tồn tại của dòng chốt đã tương đương với "đã qua quyết định Xuất bản", không cần snapshot lại giá trị này. Kiểu `text` theo `00-claude-instructions.md` mục 6 (không dùng ENUM) |
| `assignee_id` | UUID (nullable) | R-KB-041 (§2.2.3.11) "Người phụ trách" — ⚠ Bổ sung. FK → `employee.id`. Ghi nhận đúng một Nhân viên đang chịu trách nhiệm chính tại thời điểm hiện tại, **xuyên suốt vòng đời** bản soạn thảo (mọi trạng thái ở D-SD03-011 (¶3.2)). Chỉ bản soạn thảo mang giá trị — vì bản soạn thảo là **cùng một dòng duy nhất, ổn định** suốt cả vòng đời (chỉ dòng đã chốt mới là bản sao mới, xem "Cơ chế chốt phiên bản"), nên đặt cột này trực tiếp ở đây khớp đúng ngữ nghĩa "xuyên suốt vòng đời" của đặc tả, không cần đưa lên bảng cha `knowledge_object`. **Không tự động bị xoá khi chuyển trạng thái** — ở các trạng thái chờ thuần tuý (`cho_xet_duyet`, `da_qua_xet_duyet_ai`, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban`) giữ nguyên giá trị của lần nhận gần nhất, chỉ mang tính hiển thị (R-KB-045 (§2.2.3.11.4)). Chỉ bị xoá qua 2 thao tác tường minh `Release`/`ForceRelease` (D-SD03-017 (¶4.2)). Chi tiết cơ chế `Claim`/`Release`/`ForceRelease` xem D-SD03-011 (¶3.2)–D-SD03-012 (¶3.3), D-SD03-017 (¶4.2) |
| `frozen_at` | timestamptz (nullable) | R-KB-031 (§2.2.3.5) — thời điểm chốt phiên bản (= thời điểm vai trò Xuất bản chọn "Xuất bản", R-KB-093 (§2.2.6.11)); `NULL` với bản soạn thảo. Dùng trực tiếp `frozen_at IS NULL` / `IS NOT NULL` làm điều kiện, không cần cột boolean riêng |
| `frozen_by` | UUID (nullable) | ⚠ Bổ sung — FK → `employee.id`, Nhân viên giữ vai trò Xuất bản đã chốt (R-KB-072 (§2.2.5.4), R-KB-093 (§2.2.6.11)) |
| `created_at` | timestamptz | Thời điểm tạo dòng |
| `ai_missed_claims_suggestions` | JSONB (nullable) | R-KB-085 (§2.2.6.6.5) — danh sách gợi ý phát biểu tiềm năng bị bỏ sót do AI phát hiện khi rà soát Nội dung; chỉ mang tính gợi ý, không tự động gây "Không đạt xét duyệt"; chuyên gia tham khảo khi rà soát thủ công (R-KB-089 (§2.2.6.8.2)) |

**Một ràng buộc duy nhất thực thi ở tầng CSDL**:

- Partial unique index trên `(knowledge_object_id) WHERE frozen_at IS NULL` — mỗi Hạng mục tri thức luôn có **đúng một** bản đang soạn thảo.

**Cơ chế chốt phiên bản** (R-KB-029 (§2.2.3.4), R-KB-092 (§2.2.6.10)–R-KB-094 (§2.2.6.12)):

- Việc tạo phiên bản (chốt) là **một phần bắt buộc** của chính đồ thị trạng thái Hạng mục tri thức. Khi bản soạn thảo đạt `dat_xet_duyet` (R-KB-092 (§2.2.6.10)), vai trò Xuất bản **bắt buộc** phải đưa ra đúng 1 trong 2 quyết định để hạng mục rời khỏi trạng thái này (D-SD03-011 (¶3.2)–D-SD03-012 (¶3.3)):
  - **"Xuất bản"** (R-KB-093 (§2.2.6.11)): **sao chép** bản soạn thảo (kèm toàn bộ `knowledge_object_file`, `claim`, `claim_reference` — gồm cả kết quả xét duyệt `ai_*`/`expert_*`/`content_*`) thành một dòng mới `frozen_at = now()`, `frozen_by = <employee>`, `version_number` = số lớn nhất hiện có + 1, `status = NULL`. Đồng thời bản soạn thảo (dòng gốc, `frozen_at` vẫn `NULL`) chuyển `status` sang `da_xuat_ban`.
  - **"Không xuất bản"** (R-KB-094 (§2.2.6.12)): **không** sao chép, không tạo dòng mới; bản soạn thảo chuyển `status` sang `khong_xuat_ban`. Kèm cảnh báo xác nhận bắt buộc trước khi thực hiện (đặc tả yêu cầu cảnh báo, R-KB-094 (§2.2.6.12)).
- Vì mỗi hạng mục luôn có đúng 1 dòng chưa chốt (bản soạn thảo, `frozen_at IS NULL`) và quyết định Xuất bản/Không xuất bản chỉ thực hiện được đúng 1 lần cho mỗi lần bản soạn thảo đạt `dat_xet_duyet` (đồ thị trạng thái không cho thoát khỏi `dat_xet_duyet` bằng đường nào khác), ràng buộc "tối đa 1 phiên bản cho mỗi vòng xét duyệt" **tự động được đảm bảo bởi chính đồ thị trạng thái** — không cần đếm vòng riêng.
- Dòng đã chốt (`frozen_at IS NOT NULL`) **bất biến**: không cho phép UPDATE/DELETE trên chính nó và trên các bảng con của nó — chặn ở tầng ứng dụng (`/knowledge`, `/provenance`).
- ⚠ **Khoá nội dung trên chính bản soạn thảo** (tách biệt với tính bất biến của dòng đã chốt ở trên): kể từ khi bản soạn thảo vào `dat_xet_duyet` và xuyên suốt `da_xuat_ban`/`khong_xuat_ban`, **chính dòng bản soạn thảo** (vẫn `frozen_at IS NULL`) cũng bị khoá ghi ở `knowledge_object_file`/`claim`/`claim_reference` — dù chưa "chốt" theo nghĩa `frozen_at`. Xem chi tiết 4 trạng thái khoá ở D-SD03-011 (¶3.2). Mở lại (do vai trò Xét duyệt, R-KB-093 (§2.2.6.11)–R-KB-094 (§2.2.6.12)) đưa bản soạn thảo về một trạng thái không khoá thì mới sửa lại được.
- Chỉ vai trò Xét duyệt (không phải vai trò Xuất bản) mới được đưa bản soạn thảo rời khỏi `da_xuat_ban`/`khong_xuat_ban`, quay về một trong các trạng thái trước đó — xem D-SD03-011 (¶3.2)–D-SD03-012 (¶3.3).
- Không có trường `language`: Nội dung Hạng mục tri thức mặc định tiếng Việt, không cần cột riêng (đặc tả gốc không có mục ngôn ngữ ở entity này).
- ⚠ Lưu ý: mã `da_xuat_ban` (R-KB-093 (§2.2.6.11)) là trạng thái workflow của bản soạn thảo — khác với "phiên bản đang dùng" (`used_version_id`, D-SD03-013 (¶3.4) thao tác (b)), không nên nhầm lẫn hai khái niệm này.

### Ghi chú chung cho 2.7 – 2.9

Ba bảng `knowledge_object_file`, `claim`, `claim_reference` luôn gắn vào một dòng `knowledge_object_version` cụ thể. Với bản đang soạn thảo (`frozen_at IS NULL`) chúng sửa được, **trừ khi** `status` của bản soạn thảo đang ở một trong 4 trạng thái khoá nội dung (`dang_xet_duyet`, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban` — D-SD03-011 (¶3.2)), **và** — riêng khi `status = dang_nghien_cuu` — **trừ khi** người gọi chính là `assignee_id` hiện tại của bản soạn thảo (R-KB-043 (§2.2.3.11.2), D-SD03-006 (¶2.6), D-SD03-017 (¶4.2)); khi vai trò Xuất bản ra quyết định "Xuất bản", toàn bộ các bản ghi này được **sao chép** sang dòng đã chốt mới và từ đó bất biến vĩnh viễn (D-SD03-006 (¶2.6)).

### 2.7. [D-SD03-007] `knowledge_object_file` (R-KB-032 (§2.2.3.6) — không có cột thứ tự)

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | R-KB-033 (§2.2.3.6.1) |
| `knowledge_object_version_id` | UUID | FK → `knowledge_object_version.id` |
| `file_type` | text | R-KB-034 (§2.2.3.6.2) |
| `storage_key` | text | R-KB-035 (§2.2.3.6.3) — Object storage + presigned URL, cùng quy ước với `source_file.storage_key` |
| `transcript_storage_key` | text (nullable) | ⚠ Đề xuất bổ sung — cùng cơ chế/cấu trúc với `source_file.transcript_storage_key` (tuỳ `file_type`). Phục vụ hiển thị nhanh cho người xét duyệt tại `claim.content_location`, và cho AI Verification kiểm Vị trí trong Nội dung (R-KB-082 (§2.2.6.6.2) — đề xuất đã được Requirements chấp thuận) |
| `created_at` | timestamptz | |

- Nội dung Hạng mục tri thức là **sản phẩm biên tập của vai trò Nghiên cứu** (R-KB-032 (§2.2.3.6), R-KB-075 (§2.2.6.3)), **không phải tư liệu thô đầu vào** — tư liệu thô là `source`/`source_file`, quản lý ở cấp Đề tài nghiên cứu (R-KB-005 (§2.2.1.3)) bởi vai trò Nhập liệu.
- ⚠ Giao diện Nghiên cứu: tạo Nội dung là **upload file trực tiếp** — nhà nghiên cứu tải lên file tài liệu đã hoàn chỉnh (soạn sẵn bằng công cụ quen dùng bên ngoài: Word, PDF, ảnh, ghi âm/video...), **không phải một Rich Text Editor/trình soạn thảo trực tuyến** như TipTap dùng cho Mục từ (module 04, `content_blocks`) — lý do: nhà nghiên cứu vốn không quen/không thích soạn thảo trên web, và bản chất Nội dung ở đây chỉ là tài liệu làm việc nội bộ giữa nhà nghiên cứu và chuyên gia xét duyệt, không cần trình bày công khai đẹp như Mục từ. Cơ chế upload dùng presigned URL theo quy ước 2 bước đã chốt ở D-SD01-003 (¶3) — xin URL qua `knowledge.createKnowledgeObjectFileUploadUrl` rồi xác nhận qua `knowledge.createKnowledgeObjectFile`; xem/tải file đã có qua `GET .../files/{file`knowledge.getKnowledgeObjectFileDownloadUrl`. Hệ quả trực tiếp: "Vị trí trong Nội dung" (`claim.content_location`, D-SD03-008 (¶2.8)) luôn trỏ vào **một vị trí trong file tĩnh đã upload sẵn** (trang/dòng cho văn bản, khung toạ độ cho ảnh, mốc thời gian cho audio/video — cùng cấu trúc `location` ở D-SD03-009 (¶2.9)), nên giao diện cần một **bộ chọn vị trí trong file đã upload** (page/line picker cho văn bản, vẽ khung cho ảnh, kéo timeline cho audio/video) — tái dùng đúng loại component đã cần cho việc gắn Tham chiếu vào Tư liệu gốc, không cần xây thêm trình soạn thảo văn bản trực tuyến nào cho module này.

### 2.8. [D-SD03-008] `claim` (R-KB-036 (§2.2.3.7))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `knowledge_object_version_id` | UUID | FK → `knowledge_object_version.id` |
| `text` | text | Nội dung luận điểm/nhận định |
| `content_file_id` | UUID (nullable) | FK → `knowledge_object_file.id` (R-KB-037 (§2.2.3.7.1) — **không bắt buộc**, "có thể khai báo thêm") — file trong Nội dung (D-SD03-007 (¶2.7)) chứa phát biểu này |
| `content_location` | JSONB (nullable) | R-KB-037 (§2.2.3.7.1) — vị trí phát biểu trong file đó, tái dùng cấu trúc `location` ở R-KB-058 (§2.2.4.2) (xem D-SD03-009 (¶2.9) bên dưới). Khác với `claim_reference.location`: trường này trỏ **vào trong** Nội dung đã biên tập, không phải Tư liệu gốc |
| `content_ai_verdict` | text (nullable) | `dat`/`khong_dat` (R-KB-082 (§2.2.6.6.2)) — chỉ có giá trị khi `content_location` được khai báo; **ghi đè trực tiếp** mỗi lần AI Verification chạy lại, cùng cơ chế với `claim_reference.ai_verdict` |
| `content_ai_note` | text (nullable) | R-KB-083 (§2.2.6.6.3) — cùng cơ chế ghi đè |
| `content_ai_checked_at` | timestamptz (nullable) | R-KB-083 (§2.2.6.6.3) — cùng cơ chế ghi đè |
| `content_expert_verdict` | text (nullable) | `dat`/`khong_dat` (R-KB-088 (§2.2.6.8.1) — đặc tả nêu rõ: chuyên gia ghi nhận kết luận đạt/không đạt riêng cho từng Vị trí trong Nội dung, tương tự AI Verification) |
| `content_expert_note` | text (nullable) | R-KB-088 (§2.2.6.8.1) (mở rộng cho Vị trí trong Nội dung) — không bị AI Verification ghi đè |
| `content_expert_reviewed_at` | timestamptz (nullable) | R-KB-088 (§2.2.6.8.1) |
| `content_expert_reviewer_id` | UUID (nullable) | FK → `employee.id` (R-KB-071 (§2.2.5.3)) |
| `created_at` | timestamptz | |

### 2.9. [D-SD03-009] `claim_reference` (claim-mappings, R-KB-038 (§2.2.3.8) / chi tiết vị trí R-KB-056 (§2.2.4))

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `claim_id` | UUID | FK → `claim.id` |
| `source_file_id` | UUID | FK → `source_file.id` (R-KB-057 (§2.2.4.1)) |
| `location` | JSONB | Cấu trúc tuỳ theo `file_type` của `source_file` — xem chi tiết bên dưới |
| `ai_verdict` | text (nullable) | `dat` / `khong_dat` (R-KB-081 (§2.2.6.6.1)) — **ghi đè trực tiếp** mỗi lần AI Verification chạy lại (R-KB-077 (§2.2.6.5)), theo quyết định đã xác nhận |
| `ai_note` | text (nullable) | Ghi chú của AI kèm `ai_verdict` — cùng cơ chế ghi đè |
| `ai_checked_at` | timestamptz (nullable) | Thời điểm AI chạy lần gần nhất — cùng cơ chế ghi đè |
| `expert_verdict` | text (nullable) | `dat`/`khong_dat` (R-KB-088 (§2.2.6.8.1) — đặc tả nêu rõ: chuyên gia ghi nhận kết luận đạt/không đạt riêng cho từng Tham chiếu, tương tự cách AI Verification ghi ở R-KB-081 (§2.2.6.6.1)), theo nguyên tắc chung ở `00-claude-instructions.md` mục 6 (không dùng ENUM) |
| `expert_note` | text (nullable) | R-KB-088 (§2.2.6.8.1) — cột riêng với `ai_note`, **không bị ghi đè** khi AI Verification chạy lại, theo quyết định đã xác nhận |
| `expert_reviewed_at` | timestamptz (nullable) | R-KB-088 (§2.2.6.8.1) |
| `expert_reviewer_id` | UUID (nullable) | FK → `employee.id` (R-KB-071 (§2.2.5.3)) |

Cấu trúc `location` theo `file_type` (không ép chung một schema, theo `00-claude-instructions.md` mục 6):

- Văn bản (R-KB-059 (§2.2.4.2.1)): `{page, line_start, line_end}`
- Hình ảnh (R-KB-060 (§2.2.4.2.2)): `{top, left, right, bottom}`
- Âm thanh (R-KB-061 (§2.2.4.2.3)): `{start_time, end_time?}`
- Phim/video (R-KB-062 (§2.2.4.2.4)): `{start_time, end_time?, top?, left?, right?, bottom?}` (khung ảnh không bắt buộc)

Ví dụ minh hoạ ở đặc tả gốc: "Trống đồng Đông Sơn" (R-KB-063 (§2.2.4.3)).

- Kết quả AI (`ai_*`) và ghi chú chuyên gia (`expert_*`) nằm ở **hai nhóm cột tách biệt** trên cùng bảng — mỗi lần AI Verification chạy lại chỉ ghi đè nhóm `ai_*`, không đụng tới nhóm `expert_*`. Đây là lý do không cần một bảng lịch sử/append-only riêng cho ghi chú chuyên gia.

## 3. Luồng trạng thái / nghiệp vụ

### 3.1. [D-SD03-010] Trạng thái Đề tài nghiên cứu (R-KB-009 (§2.2.1.6))

```
chuan_bi_tu_lieu → tu_lieu_san_sang     [một chiều, không quay lại]
```

| # | Trạng thái (đặc tả) | Mã `status` | Trích dẫn |
|---|---|---|---|
| 1 | Chuẩn bị tư liệu | `chuan_bi_tu_lieu` | R-KB-010 (§2.2.1.6.1) |
| 2 | Tư liệu sẵn sàng | `tu_lieu_san_sang` | R-KB-011 (§2.2.1.6.2) |

- **`chuan_bi_tu_lieu`** — trạng thái khởi tạo khi Quản trị hệ thống tạo đề tài (R-KB-006 (§2.2.1.4)). **Vai trò Nhập liệu** (R-KB-069 (§2.2.5.1)) nhập Tư liệu gốc vào hệ thống và gán vào đề tài (`research_topic_source`, D-SD03-002 (¶2.2)); có thể kéo dài, thực hiện nhiều lần.
- **`tu_lieu_san_sang`** — vai trò Nhập liệu tự bật cờ khi hoàn tất, bàn giao cho vai trò Nghiên cứu. Cờ này **mở khoá** việc tạo Hạng mục tri thức của đề tài (R-KB-040 (§2.2.3.10), D-SD03-005 (¶2.5)) — trước đó vai trò Nghiên cứu không tạo được hạng mục nào.
- ⚠ Đây là một **chuyển tiếp một chiều**: đặc tả nêu rõ việc bổ sung Tư liệu gốc sau đó **không** đưa đề tài quay lại `chuan_bi_tu_lieu` và không chặn việc nghiên cứu đang diễn ra (R-KB-011 (§2.2.1.6.2)). Về kỹ thuật: đồ thị trạng thái của đề tài chỉ có đúng 1 transition, không có đường về; gọi bật cờ lần thứ hai trả lỗi.
- ⚠ **Đề xuất bổ sung**: state machine cấp đề tài đặt ở `/knowledge` (cùng package sở hữu bảng `research_topic`), **không** ở `/gate` — `/gate` giữ đúng phạm vi workflow xét duyệt Hạng mục tri thức (R-KB-074 (§2.2.6)), vốn có bản chất khác hẳn (nhiều trạng thái, có AI Verification, có vòng lặp quay lại).

### 3.2. [D-SD03-011] Sơ đồ tổng quan — Hạng mục tri thức (R-KB-074 (§2.2.6))

```
[Đề tài ở tu_lieu_san_sang → vai trò Nghiên cứu tạo Hạng mục tri thức
                            → khởi tạo bản soạn thảo, assignee_id = người tạo]
         ↓
dang_nghien_cuu → cho_xet_duyet
    → dang_xet_duyet_ai → da_qua_xet_duyet_ai → (Claim) → dang_xet_duyet (chuyên gia)  [NỘI DUNG BỊ KHOÁ]
        → (Release) → da_qua_xet_duyet_ai
        → khong_dat_xet_duyet → dang_nghien_cuu
        → dat_xet_duyet   [NỘI DUNG BỊ KHOÁ]
              → (chỉ vai trò Xuất bản, bắt buộc đúng 1 quyết định)
                   ├─ "Xuất bản"       → da_xuat_ban      [tạo phiên bản mới]      [NỘI DUNG BỊ KHOÁ]
                   └─ "Không xuất bản" → khong_xuat_ban   [không tạo, có cảnh báo] [NỘI DUNG BỊ KHOÁ]

da_xuat_ban | khong_xuat_ban
    → (chỉ vai trò Xét duyệt) mở lại về một trạng thái trước đó bất kỳ:
       dang_nghien_cuu | cho_xet_duyet | da_qua_xet_duyet_ai | dang_xet_duyet
```

Mọi chuyển trạng thái đều diễn ra trên **bản đang soạn thảo** (`frozen_at IS NULL`) — các phiên bản đã chốt không tham gia workflow.

⚠ **Cơ chế "Người phụ trách" (`assignee_id`, R-KB-041 (§2.2.3.11))** — áp dụng **xuyên suốt vòng đời** bản soạn thảo qua 3 thao tác `Claim`/`Release`/`ForceRelease` (D-SD03-017 (¶4.2)):

- **`dang_nghien_cuu`**: chỉ `assignee_id` hiện tại được sửa Nội dung/Phát biểu/Tham chiếu (R-KB-043 (§2.2.3.11.2)). Một Nhân viên khác giữ vai trò Nghiên cứu của đề tài `Claim` được khi `assignee_id` đang `NULL` (đã được `Release`).
- **`da_qua_xet_duyet_ai → dang_xet_duyet`**: vai trò Xét duyệt `Claim` để nhận xử lý — đây là một lần "nhận" **độc lập** với `assignee_id` còn sót lại từ giai đoạn nghiên cứu (khác vai trò, khác lần nhận, R-KB-044 (§2.2.3.11.3)) — `Claim` ghi đè trực tiếp, không yêu cầu `assignee_id` phải `NULL` trước (vì đã được đảm bảo duy nhất qua chính `status`). Trong `dang_xet_duyet`, chỉ `assignee_id` hiện tại mới ghi được `expert_verdict`/`content_expert_verdict` (bước 8.1); `Release` bất kỳ lúc nào để lùi về `da_qua_xet_duyet_ai`, không cần Quản trị hệ thống can thiệp (khác cơ chế "gỡ nghẽn" ở R-KB-008 (§2.2.1.5.1) — đó dành riêng cho vai trò Xuất bản).
- Ở các trạng thái chờ thuần tuý (`cho_xet_duyet`, `dang_xet_duyet_ai` trước khi Claim, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban`) — `assignee_id` **giữ nguyên giá trị của lần nhận gần nhất**, chỉ mang tính hiển thị/tham khảo (R-KB-045 (§2.2.3.11.4)), không tự động xoá khi chuyển trạng thái.
- Quản trị hệ thống có thể `ForceRelease` ở bất kỳ trạng thái nào đang có `assignee_id`, nếu người đang nhận không tự `Release` (nghỉ việc, thu hồi quyền...) — R-KB-046 (§2.2.3.11.5).

Giá trị `status` (cột `text`/`varchar`, không ENUM — theo `00-claude-instructions.md` mục 6), có **9** mã:

| # | Trạng thái (đặc tả) | Mã `status` | Trích dẫn |
|---|---|---|---|
| 1 | Đang nghiên cứu | `dang_nghien_cuu` | R-KB-075 (§2.2.6.3) |
| 2 | Chờ xét duyệt | `cho_xet_duyet` | R-KB-076 (§2.2.6.4) |
| 3 | *(đang chạy AI Verification)* | `dang_xet_duyet_ai` | ⚠ Đề xuất bổ sung — xem 3.3 mục (3) |
| 4 | Đã qua xét duyệt AI | `da_qua_xet_duyet_ai` | R-KB-086 (§2.2.6.7) |
| 5 | Đang xét duyệt (chuyên gia) | `dang_xet_duyet` | R-KB-087 (§2.2.6.8) |
| 6 | Không đạt xét duyệt | `khong_dat_xet_duyet` | R-KB-091 (§2.2.6.9) |
| 7 | Đạt xét duyệt | `dat_xet_duyet` | R-KB-092 (§2.2.6.10) |
| 8 | Đã xuất bản | `da_xuat_ban` | R-KB-093 (§2.2.6.11) |
| 9 | Không xuất bản | `khong_xuat_ban` | R-KB-094 (§2.2.6.12) |

⚠ Việc chuẩn bị tư liệu được quản lý ở **cấp Đề tài nghiên cứu** (R-KB-009 (§2.2.1.6), D-SD03-010 (¶3.1)), không phải ở quy trình Hạng mục tri thức — đặc tả gốc không đánh số lại nên R-KB-074 (§2.2.6) bắt đầu từ 2.2.6.3. Mã `da_xuat_ban` (R-KB-093 (§2.2.6.11)) là một khái niệm khác với các trạng thái workflow — xem D-SD03-006 (¶2.6).

**Khoá nội dung** — 4 trạng thái khoá ghi ở `knowledge_object_file`/`claim`/`claim_reference` (chặn ở tầng ứng dụng, `/knowledge` và `/provenance`):

| Trạng thái | Căn cứ |
|---|---|
| `dang_xet_duyet` | R-KB-087 (§2.2.6.8) — đặc tả nêu rõ |
| `dat_xet_duyet` | R-KB-092 (§2.2.6.10) — đặc tả nêu rõ |
| `da_xuat_ban` | R-KB-093 (§2.2.6.11) — đặc tả nêu rõ |
| `khong_xuat_ban` | R-KB-094 (§2.2.6.12) — đặc tả nêu rõ |

Ngoài 4 trạng thái khoá này, riêng `dang_nghien_cuu` còn có thêm điều kiện khoá theo `assignee_id` (chỉ người đang phụ trách mới sửa được, R-KB-043 (§2.2.3.11.2) — không phải "khoá hoàn toàn" như 4 trạng thái trên, mà là khoá **theo người gọi**).

### 3.3. [D-SD03-012] Chi tiết từng bước — Hạng mục tri thức

**(1) `dang_nghien_cuu`** — R-KB-075 (§2.2.6.3). Hạng mục tri thức được **khởi tạo** ở trạng thái này, do **vai trò Nghiên cứu** (R-KB-070 (§2.2.5.2)) tạo, kể cả đặt Tiêu đề (R-KB-040 (§2.2.3.10)) — chỉ tạo được khi Đề tài nghiên cứu cha đang ở `tu_lieu_san_sang` (R-KB-011 (§2.2.1.6.2), D-SD03-010 (¶3.1)). Người tạo tự động là Người phụ trách đầu tiên (`assignee_id`, R-KB-042 (§2.2.3.11.1)). Chỉ **Người phụ trách hiện tại** biên tập Nội dung (`knowledge_object_file` — R-KB-032 (§2.2.3.6), là **sản phẩm biên tập**, không phải tư liệu thô đầu vào), tạo `claim` và `claim_reference` (R-KB-043 (§2.2.3.11.2)) — một Nhân viên khác giữ vai trò Nghiên cứu của đề tài `Claim` được khi `assignee_id` đang `NULL`. Trạng thái này còn được quay về theo 2 đường, đều trên **cùng bản soạn thảo**:

  - Từ `khong_dat_xet_duyet` (R-KB-091 (§2.2.6.9)): sửa tiếp bình thường; `assignee_id` giữ nguyên giá trị cũ (không tự xoá).
  - Từ `da_xuat_ban` hoặc `khong_xuat_ban`, **chỉ do vai trò Xét duyệt** mở lại (R-KB-093 (§2.2.6.11)–R-KB-094 (§2.2.6.12), xem bước (9)–(10)) — không phải vai trò Nghiên cứu tự quay lại như đường trên; `assignee_id` cũng giữ nguyên giá trị cũ. ⚠ Việc rời `dat_xet_duyet` bắt buộc phải đi qua quyết định Xuất bản/Không xuất bản trước (bước (8)) — không thể quay thẳng về `dang_nghien_cuu`.

**(2) `cho_xet_duyet`** — R-KB-076 (§2.2.6.4). Vai trò Nghiên cứu bật cờ sẵn sàng xét duyệt.

**(3) Kích hoạt AI Verification** — R-KB-077 (§2.2.6.5). Đây là một **hành động/transition**, không phải trạng thái ổn định trong đặc tả gốc. Chế độ kích hoạt theo cấu hình hệ thống `ai_verification.trigger_mode` (D-SD07-004 (¶3.1)): `auto` — tự động kích hoạt ngay khi vào `cho_xet_duyet`; `manual` — hạng mục dừng ở `cho_xet_duyet` cho tới khi được kích hoạt thủ công. Ở cả 2 chế độ, Nhân viên giữ một role trong `ai_verification.manual_trigger_roles` (role theo phạm vi tính theo đúng Đề tài nghiên cứu cha) được kích hoạt thủ công, và có thể kích hoạt lại nhiều lần.

  - Trạng thái `dang_xet_duyet_ai` (R-KB-078 (§2.2.6.5.1)): hạng mục ở trạng thái này trong lúc `/verification` xử lý bất đồng bộ (job `verification.run`, D-SD01-004 (¶4)); nội dung bị khoá.
  - Kích hoạt lại (R-KB-079 (§2.2.6.5.2)) từ `cho_xet_duyet`, `dang_xet_duyet_ai`, `da_qua_xet_duyet_ai`, `khong_dat_xet_duyet` — quay về `dang_xet_duyet_ai`, rồi tới `da_qua_xet_duyet_ai`/`khong_dat_xet_duyet` theo kết quả mới. Không tạo job trùng: chỉ tính job `verification.run` của cùng hạng mục đang chờ/đang chạy; job đã huỷ hoặc đã hết lượt thử lại không tính là trùng, nên kích hoạt lại được — đây cũng là đường khôi phục khi job bị huỷ/thất bại hẳn (D-SD01-004 (¶4)).

**(4) AI Verification xử lý (R-KB-081 (§2.2.6.6.1)–R-KB-085 (§2.2.6.6.5))** — thực hiện bởi `/verification`, nhận kích hoạt từ `/gate`:

  - **6.6.1**: duyệt từng `claim_reference` theo 2 tiêu chí (vị trí hợp lệ trong `source_file` + khớp ngữ nghĩa) → ghi `ai_verdict`/`ai_note`/`ai_checked_at`. Nếu `source_file.is_missing = true`, tiêu chí "vị trí hợp lệ" tự động ghi `khong_dat` kèm `ai_note` giải thích — không gọi AI Gateway để kiểm phần này. Về nguyên tắc file không thể mất; nếu phát sinh, xử lý đúng theo cơ chế này (tự động không đạt khi AI Verification chạy lại) — không cần chặn gì thêm ở các bước khác (D-SD03-004 (¶2.4), ¶6).
  - **6.6.2**: nếu `claim.content_location` có khai báo, duyệt tương tự nhưng đối chiếu với `knowledge_object_file` (Nội dung) thay vì `source_file` → ghi `content_ai_verdict`/`content_ai_note`/`content_ai_checked_at`.
  - **6.6.3**: ghi nhận thời điểm xét duyệt và ghi chú của AI cho mỗi Tham chiếu và mỗi Vị trí trong Nội dung đã khai báo (gộp vào việc ghi ở 6.6.1/6.6.2).
  - **6.6.4**: **tất cả** `claim_reference` liên quan **và** mọi `content_location` đã khai báo đều đạt → `da_qua_xet_duyet_ai`; ngược lại → thẳng `khong_dat_xet_duyet` (bỏ qua bước chuyên gia).
  - **6.6.5**: đồng thời rà soát Nội dung, ghi gợi ý phát biểu bị bỏ sót vào `knowledge_object_version.ai_missed_claims_suggestions` — chỉ mang tính tham khảo, **không** ảnh hưởng kết quả đạt/không đạt ở 6.6.4.

**(5) `da_qua_xet_duyet_ai`** — R-KB-086 (§2.2.6.7). Đã qua AI Verification, sẵn sàng cho chuyên gia. Chưa có ai phụ trách xét duyệt — để chuyển sang `dang_xet_duyet`, một Nhân viên giữ vai trò Xét duyệt phải `Claim` (bước (6)).

**(6) `dang_xet_duyet`** — R-KB-087 (§2.2.6.8). Thực hiện bởi **vai trò Xét duyệt** (chuyên gia, R-KB-071 (§2.2.5.3)). Vào trạng thái này qua thao tác `Claim` (R-KB-044 (§2.2.3.11.3), D-SD03-011 (¶3.2), D-SD03-017 (¶4.2)) — vai trò Xét duyệt chủ động "nhận xử lý" một Hạng mục tri thức đang ở `da_qua_xet_duyet_ai`, đồng thời gán `assignee_id`. Thao tác **khoá độc quyền**: tại một thời điểm, mỗi hạng mục chỉ có đúng một chuyên gia đang xử lý; chuyên gia khác không nhận hay ghi nhận verdict được cho tới khi được `Release`. Chuyên gia đã nhận có thể **tự `Release`** bất kỳ lúc nào, đưa hạng mục quay lại `da_qua_xet_duyet_ai`; nếu không tự nhả, Quản trị hệ thống có thể `ForceRelease` (R-KB-046 (§2.2.3.11.5)). **Nội dung bị khoá** trong trạng thái này (R-KB-087 (§2.2.6.8) — đặc tả nêu rõ; xem bảng khoá nội dung ở D-SD03-011 (¶3.2)):

  - **8.1**: xét duyệt từng `claim` — với mỗi `claim_reference` và `content_location` (nếu có khai báo), ghi `expert_verdict`/`expert_note`/`expert_reviewed_at`/`expert_reviewer_id` tương ứng (`claim_reference.expert_*` hoặc `claim.content_expert_*`) — **không ghi đè** các trường AI. Chỉ `assignee_id` hiện tại mới ghi được (R-KB-088 (§2.2.6.8.1)).
  - **8.2**: rà soát phát biểu bị bỏ sót, tham khảo `ai_missed_claims_suggestions` (6.6.5) nếu có.
  - **8.3**: thẩm định, đánh giá tổng thể Hạng mục tri thức, dựa trên các kết luận đạt/không đạt riêng lẻ ở 8.1.

**(7) `khong_dat_xet_duyet`** — R-KB-091 (§2.2.6.9). Bị từ chối bởi AI (6.6.4) hoặc bởi chuyên gia (8.3). Vai trò Nghiên cứu xem ghi chú, quay lại `dang_nghien_cuu` trên cùng bản soạn thảo qua endpoint `resume-research` (⚠ bổ sung, D-SD03-024 (¶5.4)) — bất kỳ Nhân viên nào giữ vai trò Nghiên cứu của đề tài đều gọi được (không giới hạn riêng theo `assignee_id`, nhất quán với `submit-for-review`); `assignee_id` giữ nguyên giá trị cũ (không tự xoá, xem bước (1)).

**(8) `dat_xet_duyet`** — R-KB-092 (§2.2.6.10). Chuyên gia xác nhận đạt. **Nội dung bị khoá**: vai trò Nghiên cứu không sửa được Nội dung (R-KB-032 (§2.2.3.6)), Phát biểu (R-KB-036 (§2.2.3.7)) hay Tham chiếu (R-KB-038 (§2.2.3.8)). Đây là trạng thái duy nhất mà **chỉ vai trò Xuất bản** được đưa hạng mục rời khỏi, bằng **đúng một** trong hai quyết định (R-KB-092 (§2.2.6.10)):

  - **"Xuất bản"** → tạo phiên bản (D-SD03-006 (¶2.6)) và chuyển sang `da_xuat_ban` (bước (9)).
  - **"Không xuất bản"** → không tạo phiên bản và chuyển sang `khong_xuat_ban` (bước (10)), kèm cảnh báo bắt buộc xác nhận trước khi thực hiện.

  ⚠ **Không có đường quay thẳng** từ `dat_xet_duyet` về `dang_nghien_cuu`; phải qua `da_xuat_ban`/`khong_xuat_ban` rồi được vai trò Xét duyệt mở lại.

**(9) `da_xuat_ban`** — R-KB-093 (§2.2.6.11). Vai trò Xuất bản đã chọn "Xuất bản": một phiên bản mới được tạo (D-SD03-006 (¶2.6)), gắn `frozen_at`/`frozen_by`. **Không** đồng nghĩa với việc phiên bản đó đang được sử dụng công khai — việc chọn "phiên bản đang dùng" (`knowledge_object.used_version_id`) là thao tác độc lập khác của vai trò Xuất bản (D-SD03-013 (¶3.4) thao tác (b)), có thể trỏ tới phiên bản này, một phiên bản cũ hơn, hoặc chưa trỏ tới đâu cả. Nội dung vẫn bị khoá. **Chỉ vai trò Xét duyệt** được mở lại về một trong các trạng thái trước đó: `dang_nghien_cuu` | `cho_xet_duyet` | `da_qua_xet_duyet_ai` | `dang_xet_duyet`.

**(10) `khong_xuat_ban`** — R-KB-094 (§2.2.6.12). Vai trò Xuất bản đã chọn "Không xuất bản": vòng xét duyệt này không để lại phiên bản chốt nào. Nội dung vẫn bị khoá. Cùng cơ chế mở lại như bước (9) — **chỉ vai trò Xét duyệt**, về một trong 4 trạng thái trước đó.

### 3.4. [D-SD03-013] Hai thao tác của vai trò Xuất bản (R-KB-072 (§2.2.5.4))

Thao tác (a) **là một phần của** đồ thị trạng thái `/gate`; thao tác (b) nằm ngoài, độc lập.

**(a) Quyết định Xuất bản / Không xuất bản** (R-KB-092 (§2.2.6.10)–R-KB-094 (§2.2.6.12)) — **bắt buộc**, là cách duy nhất để hạng mục rời khỏi `dat_xet_duyet` (D-SD03-012 (¶3.3) bước (8)).

**(b) Chọn/đổi phiên bản đang được sử dụng** (R-KB-030 (§2.2.3.4.1)) — ghi `knowledge_object.used_version_id`. Điều kiện duy nhất: dòng đích phải đã chốt (`frozen_at IS NOT NULL`); không nhất thiết là phiên bản mới nhất, có thể quay lại phiên bản cũ hơn. Đổi lại được nhiều lần, không có thao tác "gỡ" — vì `used_version_id` không phải một trạng thái workflow phải thoát ra để sửa tiếp; việc vai trò Nghiên cứu tiếp tục soạn thảo (sau khi được vai trò Xét duyệt mở lại, D-SD03-012 (¶3.3) bước (9)–(10)) diễn ra hoàn toàn độc lập với con trỏ này. **Tách rời nhau**: đổi phiên bản đang dùng không đụng tới `status` của bản soạn thảo, và ngược lại.

### 3.5. [D-SD03-014] Quyền xem toàn bộ của Quản trị hệ thống (R-KB-007 (§2.2.1.5))

Nhân viên giữ role `quan_tri_he_thong` có quyền **xem** tiến độ, nội dung Hạng mục tri thức và kết quả xét duyệt của **mọi** Đề tài nghiên cứu, không cần được gán vai trò Nghiên cứu/Xét duyệt của đề tài đó. Về kỹ thuật:

- Mọi truy vấn đọc trong module bỏ qua bộ lọc phạm vi theo đề tài khi người gọi giữ role này.
- Quyền này **chỉ đọc** — không mở bất kỳ hành động Nghiên cứu (R-KB-075 (§2.2.6.3)–R-KB-076 (§2.2.6.4)) hay Xét duyệt (R-KB-087 (§2.2.6.8)–R-KB-094 (§2.2.6.12)) nào, trừ khi Nhân viên đó được gán thêm role theo phạm vi tương ứng; **ngoại lệ duy nhất là `ForceRelease`** (R-KB-046 (§2.2.3.11.5), D-SD03-017 (¶4.2)) — Quản trị hệ thống được cưỡng chế nhả `assignee_id` ở bất kỳ trạng thái nào đang có người phụ trách, không cần role Nghiên cứu/Xét duyệt của đề tài đó.
- **Cơ chế gỡ nghẽn vai trò Xuất bản** (R-KB-008 (§2.2.1.5.1) — đặc tả nêu rõ): nếu không còn ai giữ vai trò Xuất bản (khiến các Hạng mục tri thức ở `dat_xet_duyet` không thể xử lý tiếp), Quản trị hệ thống có thể **tự cấp** vai trò Xuất bản cho chính mình hoặc Nhân viên khác qua cơ chế gán role sẵn có (R-ID-006 (§2.1.3.1.1)) — không cần thêm cơ chế đặc biệt nào trong `/gate`.
- Chỉ áp dụng cho nhóm route `admin`; nhóm `partner` (Nhân viên Tổ chức khác — R-PTN-001 (§2.7)) **không** được hưởng ngoại lệ này, vì role `quan_tri_he_thong` không tồn tại ở giao diện đó (R-PTN-003 (§2.7.2)).

### 3.6. [D-SD03-015] Quyền xem tiến độ của Chủ nhiệm đề tài

Theo R-KB-073 (§2.2.5.5) (đoạn tiến độ) và R-PTN-009 (§2.7.3.5) đặc tả gốc — Requirements đã chính thức chốt nội dung này ngày 2026-09-23, đúng theo đề nghị 03 đã gửi (xem ¶6).

Nhân viên giữ role `chu_nhiem_de_tai` của một Đề tài nghiên cứu có quyền **xem tiến độ** của đúng đề tài đó, không cần được gán thêm vai trò Nghiên cứu/Xét duyệt. Phạm vi — **chỉ đọc, chỉ ở mức tiến độ**:

- Thống kê số Hạng mục tri thức của đề tài theo từng trạng thái (9 mã ở D-SD03-011 (¶3.2)).
- Danh sách Hạng mục tri thức của đề tài, mỗi dòng gồm `id`, `title` (R-KB-027 (§2.2.3.2)), `status` (R-KB-028 (§2.2.3.3)), `assignee_id` (Người phụ trách hiện tại, R-KB-041 (§2.2.3.11)), `created_by` (R-KB-047 (§2.2.3.12)), `created_at` (R-KB-048 (§2.2.3.13)) — đúng các trường R-KB-073 (§2.2.5.5) liệt kê; ngoài ra còn có số phiên bản đã chốt và đã có `used_version_id` hay chưa, là 2 trường mở rộng thêm ngoài những gì R-KB-073 (§2.2.5.5) liệt kê tường minh.
- **Không** gồm: Nội dung (`knowledge_object_file`), Phát biểu (`claim`), Tham chiếu (`claim_reference`), kết quả xét duyệt AI/chuyên gia (`ai_*`/`expert_*`/`content_*`), `ai_missed_claims_suggestions`, và snapshot các phiên bản đã chốt.
- **Không** mở hành động nghiên cứu/xét duyệt/xuất bản nào (D-SD03-011 (¶3.2)–D-SD03-013 (¶3.4)). Ngoại lệ duy nhất theo chiều ghi là quyền xoá Hạng mục tri thức ở D-SD03-005 (¶2.5), phục vụ việc dọn đề tài trước khi xoá.
- Kỹ thuật: phục vụ bằng **một endpoint đọc riêng lồng theo đề tài** (`knowledge.getResearchTopicProgress` — `GET /knowledge/research-topics/{id}/progress`), **không** nới bộ lọc phạm vi của nhóm route `knowledge-objects` (D-SD03-023 (¶5.3)) — nhờ đó Chủ nhiệm đề tài vẫn không vào được bất kỳ route đọc Hạng mục tri thức nào (chi tiết, `claims`, snapshot phiên bản, các route ghi), đúng phạm vi hẹp ở trên.

## 4. Kiến trúc riêng của module

### 4.1. [D-SD03-016] Sở hữu bảng theo package

Theo nguyên tắc chung đã chốt ở D-SD01-002 (¶2) ("mỗi package chỉ thao tác trực tiếp bảng do chính nó sở hữu, giao tiếp cross-domain qua hàm/interface nội bộ"):

| Package | Bảng sở hữu (¶2) | Ghi chú |
|---|---|---|
| `/knowledge` | `research_topic`, `research_topic_source`, `source`, `source_file`, `knowledge_object`, `knowledge_object_version`, `knowledge_object_file` | Gồm cả cột `status` của `research_topic` (state machine cấp đề tài, D-SD03-010 (¶3.1)) và của `knowledge_object_version` (kể cả `assignee_id`) — `/gate` **không** UPDATE trực tiếp, xem 4.3. Cũng là nơi đặt logic đồng bộ thư mục Tư liệu gốc (`SyncSourceFiles`, D-SD03-020 (¶4.5)) và logic quản lý nhân sự đề tài (Chủ nhiệm/Nghiên cứu/Xét duyệt, D-SD03-017 (¶4.2)) |
| `/provenance` | `claim`, `claim_reference` | Gồm cả các cột `ai_*`/`content_ai_*`/`expert_*`/`content_expert_*` |
| `/gate` | *(không sở hữu bảng riêng)* | Chỉ chứa đồ thị trạng thái của **Hạng mục tri thức** (state machine, thư viện dùng chung ở `/shared`) và logic điều phối — đọc/ghi qua interface của `/knowledge`, `/provenance` |
| `/verification` | *(không sở hữu bảng riêng)* | Gọi AI service qua AI Gateway (D-SD01-006 (¶6)); ghi kết quả qua interface của `/provenance`, `/knowledge` |
| `/ingestion` | *(không sở hữu bảng riêng)* | Nhận webhook tín hiệu "thư mục có thay đổi" từ MinIO/S3 (đã debounce/coalesce, D-SD01-005 (¶5), D-SD03-020 (¶4.5)), gọi `/knowledge.SyncSourceFiles` |

### 4.2. [D-SD03-017] Interface nội bộ giữa các package

Theo đúng mẫu đã áp dụng ở module 02 (`ProvisionScopeRoles`/`RevokeScopeRoles`) — mọi hàm ghi đều nhận `tx` của bên gọi làm tham số, đảm bảo atomic:

**`/knowledge` expose:**

- `CreateSource(ctx, tx, name, sourceType, storagePrefix) (*Source, error)` / `AddSourceToResearchTopic(ctx, tx, researchTopicID, sourceID) error` / `RemoveSourceFromResearchTopic(ctx, tx, researchTopicID, sourceID) error` — ⚠ Bổ sung: **vai trò Nhập liệu** khai báo tư liệu mới, trỏ tới thư mục MinIO/S3 đã có sẵn qua `storagePrefix` (R-KB-005 (§2.2.1.3), R-KB-069 (§2.2.5.1), D-SD03-020 (¶4.5)).
- `MarkResearchTopicReady(ctx, tx, researchTopicID, employeeID) error` — ⚠ Bổ sung: vai trò Nhập liệu bật cờ `tu_lieu_san_sang` (R-KB-011 (§2.2.1.6.2)); một chiều, gọi lần thứ hai trả lỗi (D-SD03-010 (¶3.1)).
- `DeleteResearchTopic(ctx, tx, researchTopicID, actingEmployeeID) error` — (R-KB-012 (§2.2.1.7), D-SD03-001 (¶2.1)): xoá cứng Đề tài nghiên cứu **rỗng**. Validate `actingEmployeeID` giữ role `quan_tri_he_thong` (kiểm ở tầng service, route chỉ mở ở `admin`); validate không còn dòng `knowledge_object` nào thuộc đề tài; gọi `identity.RevokeScopeRoles(ctx, tx, researchTopicID)` rồi xoá dòng `research_topic` (kéo theo `research_topic_source`, không xoá `source`/`source_file`). Trả lỗi nghiệp vụ rõ ràng kèm số Hạng mục tri thức còn lại nếu đề tài chưa rỗng.
- `SetTopicChair(ctx, tx, researchTopicID, employeeID, actingEmployeeID) error` — ⚠ Bổ sung (R-KB-073 (§2.2.5.5)): gán/đổi Chủ nhiệm đề tài. Validate `actingEmployeeID` giữ role `quan_tri_he_thong` (kiểm ở tầng service, route chỉ mở ở `admin`) → gọi `identity.AssignScopeRole(ctx, tx, "research_topic", researchTopicID, "chu_nhiem_de_tai", employeeID)` — nhờ `roles.is_singular = true` (D-SD02-001 (¶2)), Chủ nhiệm cũ tự động bị gỡ trong cùng giao dịch.
- `AssignResearcher(ctx, tx, researchTopicID, employeeID, actingEmployeeID) error` / `RemoveResearcher(ctx, tx, researchTopicID, employeeID, actingEmployeeID) error` — ⚠ Bổ sung (R-KB-070 (§2.2.5.2), R-KB-073 (§2.2.5.5)): gán/gỡ Nhân viên vào vai trò Nghiên cứu của đề tài. Validate `actingEmployeeID` giữ role `quan_tri_he_thong`, **hoặc** đang là Chủ nhiệm đề tài của đúng `researchTopicID` này → gọi `identity.AssignScopeRole`/`RevokeScopeRole(ctx, tx, "research_topic", researchTopicID, "nghien_cuu", employeeID)`.
- `AssignReviewer(ctx, tx, researchTopicID, employeeID, actingEmployeeID) error` / `RemoveReviewer(ctx, tx, researchTopicID, employeeID, actingEmployeeID) error` — ⚠ Bổ sung (R-KB-071 (§2.2.5.3), R-KB-073 (§2.2.5.5)): tương tự `AssignResearcher`/`RemoveResearcher`, cho vai trò Xét duyệt (`roleName = "xet_duyet"`).
- `ListTopicMembers(ctx, researchTopicID) (map[string][]identity.EmployeeSummary, error)` — ⚠ Bổ sung: gọi `identity.ListEmployeesByScope(ctx, researchTopicID)`, trả về Nhân viên đang giữ từng role (`chu_nhiem_de_tai`, `nghien_cuu`, `xet_duyet`) của đề tài — phục vụ endpoint `members` (D-SD03-021 (¶5.1)).
- `GetResearchTopicProgress(ctx, researchTopicID) (*ResearchTopicProgress, error)` — (R-KB-073 (§2.2.5.5), R-PTN-009 (§2.7.3.5), D-SD03-015 (¶3.6)): **chỉ đọc**; trả số Hạng mục tri thức theo từng `status` + danh sách hạng mục ở mức tiến độ (`id`, `title`, `status`, `assignee_id`, `created_by`, `created_at`, `frozen_version_count`, `has_used_version`). **Không** trả Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt — phục vụ endpoint `progress` (D-SD03-021 (¶5.1)), dùng chung cho Chủ nhiệm đề tài, vai trò Nghiên cứu/Xét duyệt của đề tài và Quản trị hệ thống.
- `SearchEmployeesForTopic(ctx, researchTopicID, query, cursor, actingEmployeeID) ([]identity.EmployeeSummary, string, error)` — ⚠ Bổ sung: validate `actingEmployeeID` giữ role `quan_tri_he_thong` hoặc đang là `chu_nhiem_de_tai` của `researchTopicID` (cùng điều kiện `AssignResearcher`), rồi gọi `identity.SearchEmployees` (D-SD02-008 (¶4)) — không lọc theo Tổ chức, không lọc theo role đang giữ; phục vụ Chủ nhiệm đề tài tìm người thêm Nghiên cứu/Xét duyệt (D-PRT-009 (¶4.9)/D-PRT-010 (¶4.10) đã chốt "không giới hạn Tổ chức").
- `SyncSourceFiles(ctx, tx, sourceID, triggeredBy *uuid.UUID) (*SyncResult, error)` — ⚠ Bổ sung: liệt kê toàn bộ object dưới `storage_prefix` của `source`, so khớp với các dòng `source_file` hiện có theo `storage_key`; file mới → tạo dòng (`is_missing = false`), enqueue job trích metadata + transcript (D-SD03-019 (¶4.4)); file cũ không còn thấy → `is_missing = true, missing_since = now()`; file từng mất nay thấy lại → gỡ cờ. Ghi `source.last_synced_at = now()`. Dùng advisory lock theo `source_id` để tránh 2 lần sync chạy chồng nhau — nếu đang có lần chạy khác, trả về ngay kèm cờ "đã có sync đang chạy" thay vì đợi. `triggeredBy = nil` khi gọi từ webhook tự động (D-SD03-020 (¶4.5)), khác `nil` khi vai trò Nhập liệu bấm "Đồng bộ lại" thủ công.
- `UpdateSourceFileTranscript(ctx, tx, sourceFileID, transcriptKey) error` / `UpdateKnowledgeObjectFileTranscript(...)` — gọi bởi job nền ASR/OCR sau khi trích transcript (D-SD03-004 (¶2.4), D-SD03-007 (¶2.7)).
- `CreateKnowledgeObject(ctx, tx, researchTopicID, title, createdBy) (*KnowledgeObject, error)` — ⚠ Bổ sung: vai trò Nghiên cứu tạo Hạng mục tri thức (R-KB-040 (§2.2.3.10)); **validate đề tài cha đang ở `tu_lieu_san_sang`**, rồi tạo kèm bản soạn thảo đầu tiên (`frozen_at = NULL`, `status = dang_nghien_cuu`, `assignee_id = createdBy` — R-KB-042 (§2.2.3.11.1)).
- `DeleteKnowledgeObject(ctx, tx, knowledgeObjectID, actingEmployeeID) error` — (R-KB-049 (§2.2.3.14), D-SD03-005 (¶2.5)): xoá cứng Hạng mục tri thức. Validate quyền — `actingEmployeeID` giữ role `quan_tri_he_thong`, **hoặc** đang là `chu_nhiem_de_tai` của đề tài cha, **hoặc** chính là `assignee_id` hiện tại của bản soạn thảo; validate **không tồn tại** dòng `knowledge_object_version` nào có `frozen_at IS NOT NULL`, và bản soạn thảo đang ở `dang_nghien_cuu`. ⚠ Khi `assignee_id IS NULL`, không có "assignee hiện tại" nào thoả điều kiện gọi — chỉ `quan_tri_he_thong`/`chu_nhiem_de_tai` gọi được cho tới khi có người `Claim` (R-KB-053 (§2.2.3.14.4)). Trong cùng giao dịch: gọi `/provenance.DeleteClaimsForVersion` cho bản soạn thảo (không tự thao tác bảng của package khác), tự xoá `knowledge_object_file` của bản soạn thảo, rồi xoá dòng `knowledge_object_version` và `knowledge_object`. Khoá ngoại `entry_knowledge_object.knowledge_object_id` (module 04) dùng **`ON DELETE RESTRICT`** — nếu còn Mục từ tham chiếu thì lệnh xoá bị chặn ở tầng CSDL, trả lỗi "đang được Mục từ tham chiếu"; `/knowledge` **không** gọi ngược sang `/encyclopedia` để kiểm, giữ đúng hướng phụ thuộc một chiều (04 → 03) đã chốt ở tài liệu 01.
- `TransitionDraftStatus(ctx, tx, knowledgeObjectID, newStatus) error` — ⚠ Thao tác trên bản soạn thảo của hạng mục (không nhận `versionID`, vì bản soạn thảo là duy nhất, xác định qua `frozen_at IS NULL`). Chỉ ghi `status`, không tự validate transition hợp lệ (thuộc về đồ thị trạng thái ở `/gate`, xem 4.3), và không đụng tới `assignee_id` (giữ nguyên giá trị hiện có, R-KB-045 (§2.2.3.11.4)). Không nhận tham số `confirmed` — logic cảnh báo thuộc về `SkipPublish` bên dưới. Hàm này **không** dùng để chuyển vào/ra `dat_xet_duyet` ↔ `da_xuat_ban`/`khong_xuat_ban` — 2 hướng đó đi qua `PublishVersion`/`SkipPublish`/`ReopenFromPublished` bên dưới, vì có kèm hiệu ứng phụ (tạo phiên bản, validate role Xuất bản/Xét duyệt) mà hàm chuyển trạng thái thuần tuý này không xử lý. Đây là hàm nền dùng chung cho mọi transition thuần tuý (không hiệu ứng phụ) trên bản soạn thảo — role + trạng thái nguồn hợp lệ được validate ở tầng gọi (`/gate`) trước khi gọi hàm này: luồng AI Verification (`cho_xet_duyet`/`dang_xet_duyet_ai`/`da_qua_xet_duyet_ai`/`khong_dat_xet_duyet`, D-SD03-018 (¶4.3)), `reject`/`approve` (D-SD03-024 (¶5.4)), và **`khong_dat_xet_duyet → dang_nghien_cuu`** qua endpoint `resume-research` (⚠ bổ sung, D-SD03-024 (¶5.4)) — vai trò Nghiên cứu xem ghi chú từ chối rồi nghiên cứu lại (R-KB-091 (§2.2.6.9), D-SD03-012 (¶3.3) bước (7)); bất kỳ Nhân viên nào giữ vai trò Nghiên cứu của đề tài gọi được, không giới hạn theo `assignee_id`.
- `Claim(ctx, tx, knowledgeObjectID, employeeID) error` — ⚠ Tổng quát cho cả `dang_nghien_cuu` và `dang_xet_duyet` (R-KB-041 (§2.2.3.11)): validate `status ∈ {dang_nghien_cuu, da_qua_xet_duyet_ai}`. Nếu `status = dang_nghien_cuu`: validate thêm `assignee_id IS NULL` (R-KB-043 (§2.2.3.11.2)), rồi ghi `assignee_id = employeeID`, **không đổi `status`**. Nếu `status = da_qua_xet_duyet_ai`: ghi đè `assignee_id = employeeID` (không yêu cầu `NULL` trước — mỗi hạng mục chỉ có 1 dòng, tính duy nhất đã đảm bảo qua `status`, R-KB-044 (§2.2.3.11.3)) và đồng thời chuyển `status → dang_xet_duyet`.
- `Release(ctx, tx, knowledgeObjectID, employeeID) error` — ⚠ Bổ sung: validate `assignee_id = employeeID` và `status ∈ {dang_nghien_cuu, dang_xet_duyet}`. Ghi `assignee_id = NULL`. Nếu `status = dang_xet_duyet`, đồng thời chuyển `status → da_qua_xet_duyet_ai`; nếu `status = dang_nghien_cuu`, không đổi `status`.
- `ForceRelease(ctx, tx, knowledgeObjectID) error` — ⚠ Bổ sung (R-KB-046 (§2.2.3.11.5)): cùng hành vi `Release` nhưng **không yêu cầu khớp `employeeID`** — chỉ gọi được bởi Nhân viên giữ role `quan_tri_he_thong` (route `admin`, D-SD03-014 (¶3.5)). Validate `assignee_id IS NOT NULL` và `status ∈ {dang_nghien_cuu, dang_xet_duyet}`.
- `PublishVersion(ctx, tx, knowledgeObjectID, employeeID) (*KnowledgeObjectVersion, error)` — ⚠ Bổ sung: hiện thực quyết định **"Xuất bản"** (R-KB-092 (§2.2.6.10)–R-KB-093 (§2.2.6.11)). Validate bản soạn thảo đang `status = dat_xet_duyet`. Trong cùng 1 giao dịch: sao chép bản soạn thảo (gọi `/provenance.CopyClaimsToVersion` cho `claim`/`claim_reference`, tự sao chép `knowledge_object_file`) thành dòng mới `frozen_at = now()`, `frozen_by = employeeID`, `version_number` = số lớn nhất hiện có + 1, `status = NULL` (dòng chốt không có `assignee_id`); đồng thời chuyển `status` của bản soạn thảo (dòng gốc) sang `da_xuat_ban`, `assignee_id` giữ nguyên. Trả về dòng vừa chốt. Chỉ gọi được bởi Nhân viên giữ vai trò Xuất bản của đề tài.
- `SkipPublish(ctx, tx, knowledgeObjectID, employeeID, confirmed bool) error` — ⚠ Bổ sung: hiện thực quyết định **"Không xuất bản"** (R-KB-094 (§2.2.6.12)). Validate `status = dat_xet_duyet`; `confirmed = false` trả lỗi kèm mã cảnh báo (đặc tả yêu cầu cảnh báo trước khi bỏ qua, R-KB-094 (§2.2.6.12) — chi tiết API ở ¶5); `confirmed = true` thì chuyển `status` sang `khong_xuat_ban`, không tạo dòng phiên bản nào. Chỉ gọi được bởi vai trò Xuất bản.
- `ReopenFromPublished(ctx, tx, knowledgeObjectID, targetStatus, employeeID) error` — ⚠ Bổ sung: vai trò Xét duyệt mở lại từ `da_xuat_ban`/`khong_xuat_ban` (R-KB-093 (§2.2.6.11)–R-KB-094 (§2.2.6.12)). Validate bản soạn thảo đang ở 1 trong 2 trạng thái này; validate `targetStatus` ∈ {`dang_nghien_cuu`, `cho_xet_duyet`, `da_qua_xet_duyet_ai`, `dang_xet_duyet`}; ghi `status = targetStatus`, **`assignee_id` giữ nguyên** (R-KB-045 (§2.2.3.11.4)). Chỉ gọi được bởi Nhân viên giữ vai trò Xét duyệt của đề tài — **không phải** vai trò Xuất bản.
- `SetUsedVersion(ctx, tx, knowledgeObjectID, versionID) error` — validate dòng đích `frozen_at IS NOT NULL` rồi ghi `knowledge_object.used_version_id`; gọi trực tiếp bởi API handler của vai trò Xuất bản (R-KB-072 (§2.2.5.4), D-SD03-013 (¶3.4) thao tác (b)).
- `GetUsedVersionContent(ctx, knowledgeObjectID) (*UsedVersionContent, error)` — **chỉ đọc**, gọi bởi `/encyclopedia` (module 04, D-SD04-012 (¶4.2) ). Trả `title`, danh sách `knowledge_object_file`, danh sách `claim` của **phiên bản đang được sử dụng** (`used_version_id`, D-SD03-005 (¶2.5)); trả lỗi not-found nếu `used_version_id IS NULL`. Phục vụ vai trò Biên tập tham chiếu phát biểu gốc khi soạn/đồng bộ nội dung Mục từ (R-ENC-017 (§2.3.3)). `/encyclopedia` **không** JOIN chéo bảng `knowledge_object*`/`claim*`, chỉ gọi hàm này.
- `GetUsedVersionIDs(ctx, knowledgeObjectIDs []uuid.UUID) (map[uuid.UUID]*uuid.UUID, error)` — ⚠ Bổ sung: đọc nhẹ, chỉ trả `used_version_id` hiện tại của từng Hạng mục tri thức (không kéo nội dung như `GetUsedVersionContent`). Gọi bởi `/encyclopedia` để tính cờ "nguồn đã lỗi thời" cho màn hình Mục từ (R-ENC-017 (§2.3.3), D-SD04-004 (¶2.4)/D-SD04-010 (¶3.4) ) — dạng batch để không phải gọi lặp cho từng Hạng mục tri thức đã gán.
- `RequestKnowledgeObjectFileUpload(ctx, knowledgeObjectID, fileType, fileName, callerID) (*UploadTicket, error)` — ⚠ Bổ sung: bước 1 của quy ước 2 bước presigned upload đã chốt ở D-SD01-003 (¶3) — chỉ sinh `storage_key` + ký presigned PUT URL ngắn hạn, **chưa tạo dòng `knowledge_object_file`** (dòng đó chỉ tạo khi client xác nhận qua `knowledge.createKnowledgeObjectFile`). Validate cùng điều kiện khoá nội dung/`assignee_id` như mọi hàm ghi khác vào `knowledge_object_file` (ghi chú chung trước D-SD03-007 (¶2.7)).
- `GetKnowledgeObjectFileDownloadURL(ctx, fileID, callerID) (*DownloadTicket, error)` — ⚠ Bổ sung: ký presigned GET URL ngắn hạn để xem/tải 1 `knowledge_object_file` đã có, gọi theo yêu cầu (không trả sẵn trong response danh sách/chi tiết — D-SD01-003 (¶3)).
- `GetSourceFileDownloadURL(ctx, sourceFileID, callerID) (*DownloadTicket, error)` — ⚠ Bổ sung: cùng cơ chế cho `source_file` (Tư liệu gốc) — dù không upload qua app, vẫn cần xem/tải để chọn vị trí tham chiếu (D-SD01-003 (¶3); D-SD03-007 (¶2.7), D-SD03-009 (¶2.9) ).

Hai kiểu dữ liệu dùng chung cho upload/download URL (định nghĩa tại `/knowledge`, tái dùng ở D-SD04-014 (¶4.4)):

```go
type UploadTicket struct {
    UploadURL, StorageKey string
    ExpiresAt             time.Time
}

type DownloadTicket struct {
    DownloadURL string
    ExpiresAt   time.Time
}
```

- `SetMissedClaimsSuggestions(ctx, tx, versionID, suggestions) error` — gọi bởi `/verification` (R-KB-085 (§2.2.6.6.5)).
- Mọi hàm ghi vào `knowledge_object_file` (tạo/sửa/xoá) đều **từ chối** nếu bản soạn thảo đích đang ở 1 trong 4 trạng thái khoá nội dung (`dang_xet_duyet`, `dat_xet_duyet`, `da_xuat_ban`, `khong_xuat_ban` — D-SD03-011 (¶3.2)), ngoài điều kiện bất biến sẵn có với dòng đã chốt (`frozen_at IS NOT NULL`) — **và**, khi `status = dang_nghien_cuu`, **từ chối thêm** nếu người gọi không phải `assignee_id` hiện tại (R-KB-043 (§2.2.3.11.2)).

**`/ingestion` expose:**

- `HandleSourceReadyWebhook(ctx, sourceID) error` — ⚠ Bổ sung: nhận sự kiện từ MinIO/S3 bucket notification (mỗi lần có object mới/xoá dưới `storage_prefix`) và **debounce theo `source_id`** bằng job `ingestion.sync_source` trên river (D-SD01-001 (¶1), D-SD01-004 (¶4)). Mục đích: tránh sync dồn dập khi user upload liên tục nhiều file.
  - **Tính trùng**: job unique theo payload, `ByState` gồm `available`, `pending`, `scheduled`, `running`, `retryable`; không gồm `completed`, `cancelled`, `discarded`. River luôn tính job `running` là trùng.
  - **Enqueue**: `InsertTx` với payload `{source_id}`, lịch chạy trễ `operations.source_sync_debounce_seconds` (mặc định 45s, `07-system-settings.md`). Có 3 trường hợp:
    - Không trùng: tạo job mới.
    - Trùng với job chưa chạy (`available`/`pending`/`scheduled`/`retryable`): sự kiện gộp vào job đó (coalesce), không tạo job mới.
    - Trùng với job đang `running`: tạo **job nối tiếp**. Lấy `id` của job đang chạy từ kết quả `InsertTx`, rồi enqueue payload `{source_id, follows_job_id}` với `follows_job_id` là `id` đó, cùng lịch chạy trễ. Các sự kiện đến sau gộp vào job nối tiếp này. Nếu lần enqueue job nối tiếp lại trùng với một job nối tiếp đang `running`, lặp lại cùng cách với `id` của job đó.

    `/ingestion` chỉ dùng kết quả trả về của `InsertTx`, không đọc bảng `river_job` (D-SD01-004 (¶4)).
  - **Khi job chạy**: gọi `/knowledge.SyncSourceFiles(ctx, tx, sourceID, nil)`. Khoảng trễ tính từ sự kiện đầu tiên; job liệt kê lại toàn bộ thư mục nên thấy được cả các file ghi sau đó. Nếu `SyncSourceFiles` trả cờ "đã có sync đang chạy" (advisory lock theo `source_id` đang bị giữ, do một job khác hoặc do "Đồng bộ lại" thủ công), worker hoãn job bằng `JobSnooze` trong `operations.source_sync_debounce_seconds` rồi chạy lại, không bỏ qua. Quy tắc này áp dụng cho cả job thường lẫn job nối tiếp. Job đang hoãn ở trạng thái `scheduled` nên sự kiện mới vẫn gộp vào nó.

**`/provenance` expose:**

- `ListClaimsForVersion(ctx, versionID) ([]Claim, error)` — đọc, gọi bởi `/gate` (hiển thị cho chuyên gia, R-KB-087 (§2.2.6.8)) và `/verification` (lấy danh sách cần duyệt).
- `RecordAIVerdict(ctx, tx, claimReferenceID, verdict, note) error` — ghi đè `ai_verdict`/`ai_note`/`ai_checked_at` (R-KB-081 (§2.2.6.6.1)), gọi bởi `/verification`.
- `RecordContentAIVerdict(ctx, tx, claimID, verdict, note) error` — tương tự cho `content_ai_*` (R-KB-082 (§2.2.6.6.2)).
- `RecordExpertReview(ctx, tx, claimReferenceID, reviewerID, verdict, note) error` / `RecordContentExpertReview(...)` — ghi `expert_*`/`content_expert_*` (R-KB-088 (§2.2.6.8.1)), gọi bởi `/gate` khi chuyên gia thao tác — 2 nhóm hàm tách biệt theo thiết kế, không chia sẻ cùng 1 hàm ghi với nhóm AI. **Chỉ `assignee_id` hiện tại của bản soạn thảo mới gọi được** (R-KB-088 (§2.2.6.8.1), D-SD03-006 (¶2.6), D-SD03-011 (¶3.2)) — validate `reviewerID = knowledge_object_version.assignee_id` khi `status = dang_xet_duyet`.
- `CopyClaimsToVersion(ctx, tx, fromVersionID, toVersionID) error` — ⚠ Bổ sung: sao chép `claim`/`claim_reference` (kèm mọi cột `ai_*`/`expert_*`) khi `/knowledge.PublishVersion` chốt phiên bản.
- `DeleteClaimsForVersion(ctx, tx, versionID) error` — ⚠ Bổ sung: xoá toàn bộ `claim`/`claim_reference` của một dòng `knowledge_object_version`, dùng trong luồng xoá Hạng mục tri thức (D-SD03-005 (¶2.5), `DeleteKnowledgeObject`). **Từ chối nếu dòng đích đã chốt** (`frozen_at IS NOT NULL`) — giữ nguyên tính bất biến của phiên bản đã chốt.
- Mọi hàm ghi ở trên đều **từ chối** nếu dòng `knowledge_object_version` đích đã chốt (`frozen_at IS NOT NULL`), **và** từ chối nếu bản soạn thảo đích đang ở 1 trong 4 trạng thái khoá nội dung nêu trên (áp dụng cho `RecordExpertReview`/`RecordContentExpertReview` khi gọi ngoài luồng `dang_xet_duyet` hợp lệ — trong luồng bình thường, các hàm này chính là thao tác **được phép** tại `dang_xet_duyet`, xem bước (6) D-SD03-012 (¶3.3); khoá chỉ chặn ghi `claim`/`claim_reference` **mới** hoặc **sửa nội dung `text`/`content_location`**, không chặn việc ghi kết quả xét duyệt `expert_*`/`ai_*` vào các trường vốn dành riêng cho việc đó).

### 4.3. [D-SD03-018] Luồng `/gate` kích hoạt `/verification` (R-KB-077 (§2.2.6.5)–R-KB-080 (§2.2.6.6))

1. `/gate` expose `TriggerAIVerification(ctx, knowledgeObjectID, triggeredBy) error`: gọi tự động từ `submit-for-review` khi `ai_verification.trigger_mode = auto`, hoặc thủ công qua `trigger-ai-verification` — khi thủ công, kiểm `triggeredBy` giữ một role trong `ai_verification.manual_trigger_roles` (D-SD07-004 (¶3.1); R-KB-077 (§2.2.6.5)) → gọi `/knowledge.TransitionDraftStatus(knowledgeObjectID, "dang_xet_duyet_ai")` → enqueue job `verification.run` trong cùng transaction với việc đổi trạng thái (river `InsertTx`, `/cmd/worker`, D-SD01-001 (¶1), D-SD01-004 (¶4)).
2. Job nền `/verification.RunVerification(ctx, knowledgeObjectID)`: đọc bản soạn thảo và `claim`/`claim_reference` qua `/provenance.ListClaimsForVersion`, đọc `source_file`/`knowledge_object_file` (kèm `transcript_storage_key` nếu có) qua `/knowledge` → gọi AI service qua AI Gateway (D-SD01-006 (¶6)) → với từng kết quả: ghi qua `/provenance.RecordAIVerdict`/`RecordContentAIVerdict` (R-KB-081 (§2.2.6.6.1)–R-KB-083 (§2.2.6.6.3)), ghi gợi ý bỏ sót qua `/knowledge.SetMissedClaimsSuggestions` (R-KB-085 (§2.2.6.6.5)).
3. Theo kết quả tổng hợp (R-KB-084 (§2.2.6.6.4)): gọi `/knowledge.TransitionDraftStatus(knowledgeObjectID, "da_qua_xet_duyet_ai")` hoặc `"khong_dat_xet_duyet"`.
4. Vì chạy trong `/cmd/worker` (bất đồng bộ), `/gate` không block chờ kết quả — khớp đúng trạng thái trung gian `dang_xet_duyet_ai` đã thống nhất ở D-SD03-011 (¶3.2)–D-SD03-012 (¶3.3).

### 4.4. [D-SD03-019] Sinh `transcript_storage_key` (D-SD03-004 (¶2.4), D-SD03-007 (¶2.7))

Không phải luôn luôn là một lệnh gọi AI Gateway — tuỳ `file_type`:

- **`file_type = audio`/`video`**: job nền gọi AI Gateway `gateway.transcribe` — `POST /v1/transcribe` (ASR — `06` ¶3) để sinh transcript.
- **`file_type = text`**: chỉ là trích xuất/parse kỹ thuật thuần tuý (vd. `pdfplumber`, không gọi AI Gateway) — vì nội dung Hán Nôm dạng text đã được OCR sẵn từ hệ thống thượng nguồn (R-GEN-003 (§1.1.1)), hệ thống chỉ cần đọc lại text đã có trong file, không cần AI nhận dạng lại.
- **`file_type = image`**: không sinh transcript ở bước này (ảnh hiện vật/tư liệu không có văn bản để trích) — nếu về sau cần OCR ảnh thì thuộc phạm vi AI Gateway `gateway.verifyImageRegion` hoặc mở rộng riêng, chưa nằm trong phạm vi mục này.

Điểm kích hoạt khác nhau theo nguồn gốc file (áp dụng chung cho cả 3 nhánh trên khi phù hợp với `file_type`):

- `source_file`: kích hoạt ngay sau khi `SyncSourceFiles` phát hiện file mới (không áp dụng cho file đã có từ trước, kể cả khi được đồng bộ lại — song song với job trích metadata đã có, D-SD01-004 (¶4)).
- `knowledge_object_file`: kích hoạt ngay sau khi **vai trò Nghiên cứu** tạo file Nội dung trong `/knowledge` khi biên tập (R-KB-075 (§2.2.6.3)) — không qua `/ingestion`, vì đây là sản phẩm biên tập của nhà nghiên cứu (R-KB-032 (§2.2.3.6)), không phải tư liệu Hán Nôm nạp từ hệ thống thượng nguồn.
- Khi vai trò Xuất bản chốt phiên bản (D-SD03-013 (¶3.4) thao tác (a), `PublishVersion`), bản sao `knowledge_object_file` **dùng lại nguyên `storage_key`/`transcript_storage_key`** của bản gốc — không sinh transcript lại, không nhân bản file trong Object storage.

Cả 2 trường hợp (source_file/knowledge_object_file) ghi kết quả ngược qua đúng hàm cập nhật tương ứng ở 4.2. Chi tiết cấu hình AI Gateway (mode `mock`/`cpu-small`/`gpu-onprem`, xử lý lỗi/timeout) xem tài liệu 06.

### 4.5. [D-SD03-020] Đồng bộ Tư liệu gốc từ MinIO/S3 (R-KB-005 (§2.2.1.3), R-KB-017 (§2.2.2))

**Việc nạp file vật lý vào MinIO/S3 nằm hoàn toàn ngoài hệ thống** — dù nguồn là hệ thống OCR thượng nguồn tự ghi file vào bucket (R-GEN-003 (§1.1.1)), hay Nhân viên Nhập liệu copy file thủ công cho các loại tư liệu còn lại (R-KB-020 (§2.2.2.3) sách, hiện vật, điền dã, phỏng vấn nghệ nhân). Hệ thống không còn nhận file/payload qua API/webhook — chỉ quản lý metadata trỏ tới thư mục và tự đồng bộ lại nội dung:

1. **Vai trò Nhập liệu** tạo `source` trỏ tới thư mục đã có sẵn trong MinIO/S3 qua `CreateSource(..., storagePrefix)` (D-SD03-017 (¶4.2)), rồi gán cho đề tài (R-KB-005 (§2.2.1.3)). Là CRUD thường trên bảng `/knowledge` tự sở hữu, route ở nhóm `admin`.
2. Nội dung thư mục được đồng bộ vào `source_file` qua `SyncSourceFiles` (D-SD03-017 (¶4.2), sở hữu bởi `/knowledge`), kích hoạt bằng 2 cách bổ trợ nhau:
   - **Tự động** — MinIO/S3 bucket notification báo "thư mục có thay đổi" → `/ingestion.HandleSourceReadyWebhook` debounce/coalesce theo `source_id` (theo `operations.source_sync_debounce_seconds`, D-SD03-017 (¶4.2)) → gọi `SyncSourceFiles`. Tránh sync dồn dập khi có nhiều file được ghi liên tục vào bucket.
   - **Thủ công** — nút "Đồng bộ lại" trong giao diện vai trò Nhập liệu, gọi thẳng `SyncSourceFiles` không qua debounce; dùng khi cần thấy kết quả ngay, hoặc khi bucket notification lỗi/chưa cấu hình.
3. File biến mất khỏi thư mục **không bị xoá dòng** `source_file` — chỉ đánh dấu `is_missing`/`missing_since` (D-SD03-004 (¶2.4)), giữ nguyên vẹn truy vết từ `claim_reference` đã trỏ tới file đó trước đây (D-SD03-009 (¶2.9)).
4. Sau khi đồng bộ, file mới dùng chung các job nền hậu xử lý sẵn có (trích metadata, sinh transcript — D-SD03-019 (¶4.4)).

Đối lập với `knowledge_object_file` (**không đổi**) — vẫn là file do vai trò Nghiên cứu upload trực tiếp qua app khi biên tập Nội dung (presigned URL, D-SD01-003 (¶3)), không qua cơ chế đồng bộ MinIO/S3 ngoài này, vì đây là sản phẩm biên tập của nhà nghiên cứu (R-KB-032 (§2.2.3.6)), không phải tư liệu gốc nạp từ bên ngoài.

## 5. Thiết kế API

Theo ranh giới mount đã chốt ở D-SD01-002 (¶2): nhóm `admin` mount đầy đủ mọi package (gồm cả `ingestion`); nhóm `partner` chỉ mount phần Nghiên cứu/Xét duyệt trong `knowledge`/`gate`, và phần quản lý nhân sự đề tài dành cho Chủ nhiệm đề tài (R-KB-073 (§2.2.5.5), D-SD03-021 (¶5.1): `members`/`researchers`/`reviewers`), giới hạn theo Đề tài nghiên cứu được gán (R-PTN-003 (§2.7.2)–R-PTN-004 (§2.7.3)) — **không mount** phần quản lý `sources`/tạo `research-topics`/`set-chair` (dành cho vai trò Nhập liệu/Quản trị hệ thống, chỉ có ở Tổ chức Văn Minh Việt). Path dùng tiếng Anh theo `00-claude-instructions.md` mục 6; giá trị `status`/tên role vẫn tiếng Việt không dấu để đối chiếu trực tiếp với đặc tả gốc.

### 5.1. [D-SD03-021] Đề tài nghiên cứu (`research-topics`)

| Method | Path | operationId | Mount | Mô tả |
|---|---|---|---|---|
| GET | `/knowledge/research-topics` | `knowledge.listResearchTopics` | admin, partner | Danh sách — mỗi dòng kèm `source_count`, `knowledge_object_count` (⚠ bổ sung, khớp cột đã có ở D-ADM-008 (¶4.8) / D-PRT-004 (¶4.4)) và `chair: {id, display_name} \| null` — `partner` chỉ thấy đề tài mà Nhân viên đang giữ **ít nhất một vai trò theo phạm vi** của đề tài đó: `chu_nhiem_de_tai`, `nghien_cuu` hoặc `xet_duyet` (lọc theo `employee_role`) — ⚠ **phải gồm cả `chu_nhiem_de_tai`**, vì R-KB-073 (§2.2.5.5) nêu rõ Chủ nhiệm đề tài không tự động có vai trò Nghiên cứu/Xét duyệt; nếu lọc thiếu, một Chủ nhiệm thuộc Tổ chức khác sẽ không thấy chính đề tài mình phụ trách và không vào được các route `members`/`researchers`/`reviewers` bên dưới. `admin` với role `quan_tri_he_thong` thấy toàn bộ, không lọc (D-SD03-014 (¶3.5)) |
| POST | `/knowledge/research-topics` | `knowledge.createResearchTopic` | admin | Tạo mới — chỉ Quản trị hệ thống (R-KB-006 (§2.2.1.4)); tự sinh role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` theo phạm vi qua `identity.ProvisionScopeRoles` |
| GET | `/knowledge/research-topics/{id}` | `knowledge.getResearchTopic` | admin, partner | Chi tiết — `status`, `chair: {id, display_name} \| null` (⚠ bổ sung — Chủ nhiệm đề tài hiện tại dạng object kèm tên hiển thị, nếu đã gán, R-KB-073 (§2.2.5.5)), danh sách Tư liệu gốc đã gán, thống kê số Hạng mục tri thức theo từng trạng thái |
| DELETE | `/knowledge/research-topics/{id}` | `knowledge.deleteResearchTopic` | admin | R-KB-012 (§2.2.1.7) — xoá cứng Đề tài nghiên cứu **rỗng** (`DeleteResearchTopic`, D-SD03-001 (¶2.1), D-SD03-017 (¶4.2)) — chỉ Quản trị hệ thống; trả lỗi nếu đề tài còn Hạng mục tri thức. Tư liệu gốc đã gán chỉ bị gỡ liên kết, không bị xoá |
| POST | `/knowledge/research-topics/{id}/sources` | `knowledge.addResearchTopicSource` | admin | Gán Tư liệu gốc cho đề tài — body `{source_id}` (`AddSourceToResearchTopic`, vai trò Nhập liệu) |
| DELETE | `/knowledge/research-topics/{id}/sources/{source_id}` | `knowledge.removeResearchTopicSource` | admin | Gỡ Tư liệu gốc khỏi đề tài |
| POST | `/knowledge/research-topics/{id}/mark-ready` | `knowledge.markResearchTopicReady` | admin | `chuan_bi_tu_lieu → tu_lieu_san_sang` (một chiều, gọi lần 2 trả lỗi — D-SD03-010 (¶3.1)) |
| GET | `/knowledge/research-topics/{id}/progress` | `knowledge.getResearchTopicProgress` | admin, partner | R-KB-073 (§2.2.5.5), R-PTN-009 (§2.7.3.5) — tiến độ đề tài: thống kê theo trạng thái + danh sách Hạng mục tri thức ở mức tiến độ, mỗi dòng `assignee`/`created_by` dạng object `{id, display_name} \| null` (⚠ bổ sung) thay vì chỉ ID (`GetResearchTopicProgress`, D-SD03-015 (¶3.6), D-SD03-017 (¶4.2)). Mở cho Nhân viên giữ **bất kỳ vai trò phạm vi nào** của đề tài (`chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet`) và Quản trị hệ thống; **không** trả Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt |
| GET | `/knowledge/research-topics/{id}/sources/{source_id}` | `knowledge.getResearchTopicSource` | admin, partner | ⚠ Bổ sung — chi tiết một Tư liệu gốc **đã gán cho đề tài này** (kèm `last_synced_at` + danh sách `source_file`: `is_missing`/`missing_since`) — dùng khi chọn file + vị trí để tạo Tham chiếu (màn hình Nghiên cứu, R-KB-075 (§2.2.6.3)). Trả lỗi nếu `source_id` chưa được gán cho đề tài `{id}` (`research_topic_source`, D-SD03-002 (¶2.2)). Phạm vi tự động giới hạn theo Đề tài được gán — vì phải qua `research-topics/{id}` (đã kiểm quyền theo `employee_role`, D-SD03-021 (¶5.1) dòng đầu), không cần thêm điều kiện phân quyền rời rạc trên `source_id` |
| GET | `/knowledge/research-topics/{id}/sources/{source_id}/files/{file_id}/download-url` | `knowledge.getResearchTopicSourceFileDownloadUrl` | admin, partner | ⚠ Bổ sung — URL tải/xem 1 `source_file` (`GetSourceFileDownloadURL`, D-SD03-017 (¶4.2)) |
| GET | `/knowledge/research-topics/{id}/members` | `knowledge.listResearchTopicMembers` | admin, partner | ⚠ Bổ sung — danh sách Nhân viên đang giữ từng vai trò theo phạm vi của đề tài (`chu_nhiem_de_tai`, `nghien_cuu`, `xet_duyet`, R-KB-073 (§2.2.5.5)) — `ListTopicMembers` (D-SD03-017 (¶4.2)); `partner` giới hạn theo đề tài được gán (nhất quán dòng đầu D-SD03-021 (¶5.1)) |
| GET | `/knowledge/research-topics/{id}/employee-search` | `knowledge.searchResearchTopicEmployees` | admin, partner | Tìm Nhân viên theo từ khoá (`q`), không giới hạn Tổ chức, chỉ trả tên gọi và email (R-KB-073 (§2.2.5.5)) — phục vụ Chủ nhiệm đề tài thêm Nghiên cứu/Xét duyệt (`SearchEmployeesForTopic`, D-SD03-017 (¶4.2)) — quyền gọi giống `researchers`/`reviewers` |
| POST | `/knowledge/research-topics/{id}/set-chair` | `knowledge.setResearchTopicChair` | admin | Gán/đổi Chủ nhiệm đề tài — body `{employee_id}` (`SetTopicChair`, D-SD03-017 (¶4.2)) — chỉ Quản trị hệ thống (R-KB-073 (§2.2.5.5)) |
| POST | `/knowledge/research-topics/{id}/researchers` | `knowledge.addResearchTopicResearcher` | admin, partner | Gán Nhân viên vào vai trò Nghiên cứu — body `{employee_id}` (`AssignResearcher`) — Quản trị hệ thống hoặc Chủ nhiệm đề tài của đề tài này (R-KB-073 (§2.2.5.5)) |
| DELETE | `/knowledge/research-topics/{id}/researchers/{employee_id}` | `knowledge.removeResearchTopicResearcher` | admin, partner | Gỡ Nhân viên khỏi vai trò Nghiên cứu (`RemoveResearcher`) — cùng điều kiện quyền như trên |
| POST | `/knowledge/research-topics/{id}/reviewers` | `knowledge.addResearchTopicReviewer` | admin, partner | Gán Nhân viên vào vai trò Xét duyệt — body `{employee_id}` (`AssignReviewer`) — cùng điều kiện quyền như `researchers` |
| DELETE | `/knowledge/research-topics/{id}/reviewers/{employee_id}` | `knowledge.removeResearchTopicReviewer` | admin, partner | Gỡ Nhân viên khỏi vai trò Xét duyệt (`RemoveReviewer`) — cùng điều kiện quyền như trên |

**Phạm vi từng vai trò ở `partner`** (R-PTN-003 (§2.7.2)–R-PTN-004 (§2.7.3)): Nhân viên chỉ giữ `chu_nhiem_de_tai` của một đề tài thấy được đề tài đó trong danh sách và chi tiết (`knowledge.getResearchTopic`), xem được **tiến độ** đề tài (`knowledge.getResearchTopicProgress`, D-SD03-015 (¶3.6), R-PTN-009 (§2.7.3.5)), và dùng được `members`/`researchers`/`reviewers`/`employee-search` (R-PTN-008 (§2.7.3.4)) — nhưng **không** mở thêm quyền nào khác: không đọc `sources/{source_id}` (thuộc R-PTN-005 (§2.7.3.1), gắn với vai trò Nghiên cứu/Xét duyệt), không vào bất kỳ route đọc Hạng mục tri thức nào (D-SD03-023 (¶5.3)), tức không xem được Nội dung/Phát biểu/kết quả xét duyệt. Ngoại lệ duy nhất: `knowledge.deleteKnowledgeObject` — `DELETE /knowledge/knowledge-objects/{id}` cho hạng mục đủ điều kiện xoá (D-SD03-005 (¶2.5), D-SD03-023 (¶5.3), R-KB-049 (§2.2.3.14), R-PTN-009 (§2.7.3.5)) — phục vụ việc dọn đề tài trước khi xoá. Muốn nghiên cứu/xét duyệt, Chủ nhiệm phải tự gán thêm vai trò Nghiên cứu/Xét duyệt cho chính mình (R-KB-073 (§2.2.5.5)) — xem thêm ghi chú ở ¶6.

### 5.2. [D-SD03-022] Tư liệu gốc (`sources`)

Route CRUD/quản lý dưới đây (`/knowledge/sources`) chỉ mount ở `admin` — vai trò Nhập liệu là Nhân viên Tổ chức Văn Minh Việt, không tồn tại ở `partner` (R-PTN-003 (§2.7.2)). Vai trò Nghiên cứu/Xét duyệt ở `partner` đọc Tư liệu gốc theo 2 cách: (a) **gián tiếp** qua `knowledge-objects/{id}/claims` (Tham chiếu đã tạo, trỏ tới `source_file`, D-SD03-024 (¶5.4)); và (b) **trực tiếp nhưng có giới hạn phạm vi** qua route `knowledge.getResearchTopicSource` — `GET /knowledge/research-topics/{id}/sources/{source_id}` (⚠ bổ sung) — dùng khi **chọn** file + vị trí để tạo Tham chiếu mới ở màn hình Nghiên cứu; không mở route đọc `sources` độc lập/không giới hạn (danh sách đầy đủ, tra cứu tự do) ở `partner`.

| Method | Path | operationId | Mount | Mô tả |
|---|---|---|---|---|
| GET | `/knowledge/sources` | `knowledge.listSources` | admin | Danh sách — filter `type`, từ khoá theo `name` |
| POST | `/knowledge/sources` | `knowledge.createSource` | admin | Tạo mới — body `{name, type, storage_prefix}` (`CreateSource`, trỏ tới thư mục MinIO/S3 đã có sẵn — D-SD03-020 (¶4.5)) |
| GET | `/knowledge/sources/{id}` | `knowledge.getSource` | admin | Chi tiết + `last_synced_at` + danh sách `source_file` (kèm `is_missing`/`missing_since`) |
| POST | `/knowledge/sources/{id}/sync` | `knowledge.syncSource` | admin | "Đồng bộ lại" thủ công — gọi `SyncSourceFiles(..., triggeredBy = <employee>)`, không qua debounce (D-SD03-020 (¶4.5)); trả về số file mới/mất/không đổi, hoặc báo "đã có sync đang chạy" nếu advisory lock đang giữ (D-SD03-017 (¶4.2)) |
| GET | `/knowledge/sources/{id}/files/{file_id}/download-url` | `knowledge.getSourceFileDownloadUrl` | admin | ⚠ Bổ sung — URL tải/xem 1 `source_file` cho màn D-ADM-011 (¶4.11) (`GetSourceFileDownloadURL`, D-SD03-017 (¶4.2)) |

**Quyền** (làm rõ để tránh lặp lại lệch code vs thiết kế đã xảy ra — xem ¶6): mọi endpoint nhóm này (`sources` CRUD/`sync`, và `mark-ready` ở D-SD03-021 (¶5.1)) yêu cầu role `nhap_lieu` **hoặc** `quan_tri_he_thong` ở tầng service. Mount ở nhóm route `admin` chỉ nghĩa là Nhân viên Tổ chức khác không gọi được — **không** đồng nghĩa giới hạn role trong `admin` chỉ còn `quan_tri_he_thong`.

### 5.3. [D-SD03-023] Hạng mục tri thức (`knowledge-objects`) — CRUD & Nội dung

Mount cả `admin` và `partner` — `partner` giới hạn theo đề tài được gán vai trò `nghien_cuu`/`xet_duyet` (⚠ **không** gồm `chu_nhiem_de_tai`, khác bộ lọc ở D-SD03-021 (¶5.1) — Chủ nhiệm đề tài không kiêm 2 vai trò này thì không thấy Hạng mục tri thức nào, đúng phạm vi R-PTN-004 (§2.7.3); xem ghi chú ở ¶6); `admin` phục vụ Nhân viên Tổ chức Văn Minh Việt giữ 2 role này, và Quản trị hệ thống xem toàn bộ, chỉ đọc (D-SD03-014 (¶3.5)). ⚠ Ngoại lệ duy nhất trong nhóm này dành cho `chu_nhiem_de_tai` (R-KB-049 (§2.2.3.14), R-PTN-009 (§2.7.3.5)): endpoint `knowledge.deleteKnowledgeObject` (xoá hạng mục đủ điều kiện, D-SD03-005 (¶2.5)) — Chủ nhiệm đề tài gọi được endpoint này dù không đọc được các route còn lại của nhóm.

| Method | Path | operationId | Mount | Mô tả |
|---|---|---|---|---|
| GET | `/knowledge/knowledge-objects` | `knowledge.listKnowledgeObjects` | admin, partner | Danh sách — filter `research_topic_id`, `status`; mỗi dòng kèm `assignee`/`created_by` dạng object `{id, display_name} \| null` (⚠ bổ sung) thay vì chỉ ID |
| POST | `/knowledge/knowledge-objects` | `knowledge.createKnowledgeObject` | admin, partner | Tạo mới — body `{research_topic_id, title}` (`CreateKnowledgeObject`; chỉ khi đề tài đang `tu_lieu_san_sang`) |
| GET | `/knowledge/knowledge-objects/{id}` | `knowledge.getKnowledgeObject` | admin, partner | Chi tiết bản soạn thảo (`status`, `title`, `assignee`/`created_by` dạng object `{id, display_name} \| null` — ⚠ bổ sung, thay cho `assignee_id`/`created_by` dạng ID thuần, `ai_missed_claims_suggestions`) + danh sách phiên bản đã chốt (`version_number`, `frozen_at`, `frozen_by` dạng object `{id, display_name} \| null` — ⚠ bổ sung) + `has_missing_source_files` (⚠ bổ sung — cờ tổng hợp: có Tham chiếu nào trong bản soạn thảo trỏ tới `source_file.is_missing = true` không, để hiển thị cảnh báo ngay khi mở xem — chỉ cần cảnh báo khi mở xem, không cần thông báo chủ động) + `can_trigger_ai_verification` (⚠ bổ sung — bool, người gọi có quyền kích hoạt AI Verification thủ công theo cấu hình `ai_verification.manual_trigger_roles` và trạng thái hiện tại có hợp lệ để kích hoạt không; frontend dùng để hiện/ẩn nút, vì Cổng Tổ chức khác không đọc được cấu hình — D-SD07-004 (¶3.1)) + `ai_verification_running` (⚠ bổ sung — bool, `true` khi hạng mục còn job `verification.run` đang chờ/đang chạy theo đúng định nghĩa job trùng ở D-SD03-012 (¶3.3) bước (3); tại `dang_xet_duyet_ai`, frontend dùng để phân biệt job còn chạy với job đã huỷ/thất bại hẳn cần kích hoạt lại, vì API job nền chỉ dành cho Quản trị hệ thống — D-SD01-004 (¶4)) |
| DELETE | `/knowledge/knowledge-objects/{id}` | `knowledge.deleteKnowledgeObject` | admin, partner | R-KB-049 (§2.2.3.14) — xoá cứng Hạng mục tri thức khi chưa có phiên bản chốt, đang ở `dang_nghien_cuu`, và chưa bị Mục từ tham chiếu (`DeleteKnowledgeObject`, D-SD03-005 (¶2.5), D-SD03-017 (¶4.2)); người gọi: Quản trị hệ thống, Chủ nhiệm đề tài của đề tài cha, hoặc `assignee_id` hiện tại (R-KB-053 (§2.2.3.14.4)). Kéo theo Nội dung/Phát biểu/Tham chiếu của bản soạn thảo |
| GET | `/knowledge/knowledge-objects/{id}/versions/{version_id}` | `knowledge.getKnowledgeObjectVersion` | admin, partner | Đọc snapshot một phiên bản đã chốt (bất biến) — dùng cho vai trò Xuất bản chọn phiên bản (D-SD03-013 (¶3.4) thao tác (b)) hoặc tra cứu lịch sử |
| POST | `/knowledge/knowledge-objects/{id}/files/upload-url` | `knowledge.createKnowledgeObjectFileUploadUrl` | admin, partner | ⚠ Bổ sung — xin presigned upload URL cho file Nội dung (`RequestKnowledgeObjectFileUpload`, D-SD03-017 (¶4.2); quy ước 2 bước, D-SD01-003 (¶3)) — bước 1, chưa tạo dòng DB |
| POST | `/knowledge/knowledge-objects/{id}/files` | `knowledge.createKnowledgeObjectFile` | admin, partner | Xác nhận `knowledge_object_file` đã upload xong qua presigned URL (bước 3 của quy ước, D-SD01-003 (¶3)) — chặn nếu bản soạn thảo đang ở 1 trong 4 trạng thái khoá (D-SD03-011 (¶3.2)), hoặc nếu người gọi không phải `assignee_id` hiện tại khi `status = dang_nghien_cuu` |
| GET | `/knowledge/knowledge-objects/{id}/files/{file_id}/download-url` | `knowledge.getKnowledgeObjectFileDownloadUrl` | admin, partner | ⚠ Bổ sung — URL tải/xem 1 `knowledge_object_file` (`GetKnowledgeObjectFileDownloadURL`, D-SD03-017 (¶4.2)) |
| DELETE | `/knowledge/knowledge-objects/{id}/files/{file_id}` | `knowledge.deleteKnowledgeObjectFile` | admin, partner | Gỡ file Nội dung — cùng điều kiện khoá |
| POST | `/knowledge/knowledge-objects/{id}/claims` | `knowledge.createClaim` | admin, partner | Tạo Phát biểu — body `{text, content_file_id?, content_location?}` — cùng điều kiện khoá |
| PATCH | `/knowledge/knowledge-objects/{id}/claims/{claim_id}` | `knowledge.updateClaim` | admin, partner | Sửa `text`/`content_file_id`/`content_location` — chặn nếu đang khoá |
| DELETE | `/knowledge/knowledge-objects/{id}/claims/{claim_id}` | `knowledge.deleteClaim` | admin, partner | Xoá Phát biểu (kéo theo các Tham chiếu con) |
| POST | `/knowledge/knowledge-objects/{id}/claims/{claim_id}/references` | `knowledge.createClaimReference` | admin, partner | Thêm Tham chiếu tới Tư liệu gốc — body `{source_file_id, location}` (cấu trúc `location` theo `file_type`, D-SD03-009 (¶2.9)) |
| DELETE | `/knowledge/knowledge-objects/{id}/claims/{claim_id}/references/{reference_id}` | `knowledge.deleteClaimReference` | admin, partner | Gỡ Tham chiếu |

### 5.4. [D-SD03-024] Luồng xét duyệt, Người phụ trách & AI Verification

| Method | Path | operationId | Mount | Mô tả |
|---|---|---|---|---|
| POST | `/knowledge/knowledge-objects/{id}/submit-for-review` | `knowledge.submitKnowledgeObjectForReview` | admin, partner | `dang_nghien_cuu → cho_xet_duyet` (R-KB-076 (§2.2.6.4)) — nếu `ai_verification.trigger_mode = auto` thì kích hoạt AI Verification ngay sau đó trong cùng transaction (D-SD03-018 (¶4.3)); nếu `manual` thì dừng ở `cho_xet_duyet` |
| POST | `/knowledge/knowledge-objects/{id}/trigger-ai-verification` | `knowledge.triggerAiVerification` | admin, partner | Kích hoạt (chế độ `manual`) hoặc kích hoạt lại AI Verification thủ công (R-KB-077 (§2.2.6.5)) — chỉ Nhân viên giữ role trong `ai_verification.manual_trigger_roles` (`07-system-settings.md`); chỉ hợp lệ từ `cho_xet_duyet`, `dang_xet_duyet_ai`, `da_qua_xet_duyet_ai`, `khong_dat_xet_duyet` (D-SD03-012 (¶3.3) bước (3)). Response kèm `merged_into_running_job` (⚠ bổ sung — bool): `true` khi hạng mục đã có job `verification.run` đang chờ/đang chạy — lệnh gộp vào job đó, không tạo job mới, không đổi trạng thái, không ghi audit (D-SD01-002 (¶2)) |
| POST | `/knowledge/knowledge-objects/{id}/claim` | `knowledge.claimKnowledgeObject` | admin, partner | Người phụ trách "nhận xử lý" (R-KB-041 (§2.2.3.11)) — hợp lệ tại `dang_nghien_cuu` (chỉ gán `assignee_id`, không đổi `status`) hoặc `da_qua_xet_duyet_ai` (gán `assignee_id` **và** chuyển `status → dang_xet_duyet`, D-SD03-012 (¶3.3) bước (6)) |
| POST | `/knowledge/knowledge-objects/{id}/release` | `knowledge.releaseKnowledgeObject` | admin, partner | Người phụ trách hiện tại tự "nhả" — hợp lệ tại `dang_nghien_cuu` (chỉ xoá `assignee_id`) hoặc `dang_xet_duyet` (xoá `assignee_id` **và** lùi `status → da_qua_xet_duyet_ai`) |
| POST | `/knowledge/knowledge-objects/{id}/force-release` | `knowledge.forceReleaseKnowledgeObject` | admin | Quản trị hệ thống cưỡng chế nhả (R-KB-046 (§2.2.3.11.5)) — hợp lệ ở bất kỳ trạng thái nào đang có `assignee_id`, hành vi giống `release` nhưng không cần khớp người gọi |
| GET | `/knowledge/knowledge-objects/{id}/claims` | `knowledge.listClaims` | admin, partner | Danh sách Phát biểu kèm Tham chiếu + verdict `ai_*`/`expert_*`/`content_*` — màn hình xét duyệt (`ListClaimsForVersion`); mỗi Tham chiếu kèm `source_file.is_missing`/`missing_since` để hiển thị cảnh báo trực tiếp trên từng dòng (bổ sung cùng `has_missing_source_files`, D-SD03-023 (¶5.3)) |
| POST | `/knowledge/knowledge-objects/{id}/claims/{claim_id}/references/{reference_id}/review` | `knowledge.reviewClaimReference` | admin, partner | Chuyên gia ghi `expert_verdict`/`expert_note` cho Tham chiếu (R-KB-088 (§2.2.6.8.1)) — body `{verdict, note?}`; chỉ hợp lệ tại `dang_xet_duyet`, chỉ `assignee_id` hiện tại gọi được, không ghi đè `ai_*` |
| POST | `/knowledge/knowledge-objects/{id}/claims/{claim_id}/content-review` | `knowledge.reviewClaimContent` | admin, partner | Chuyên gia ghi `content_expert_verdict`/`content_expert_note` cho Vị trí trong Nội dung (R-KB-088 (§2.2.6.8.1)) — chỉ khi `claim.content_location` đã khai báo; chỉ `assignee_id` hiện tại gọi được |
| POST | `/knowledge/knowledge-objects/{id}/reject` | `knowledge.rejectKnowledgeObject` | admin, partner | `dang_xet_duyet → khong_dat_xet_duyet` sau bước 8.3 (R-KB-091 (§2.2.6.9)) |
| POST | `/knowledge/knowledge-objects/{id}/resume-research` | `knowledge.resumeKnowledgeObjectResearch` | admin, partner | ⚠ Bổ sung — vai trò Nghiên cứu xem ghi chú rồi nghiên cứu lại: `khong_dat_xet_duyet → dang_nghien_cuu` (R-KB-091 (§2.2.6.9), D-SD03-012 (¶3.3) bước (7)); chỉ hợp lệ từ `khong_dat_xet_duyet`; bất kỳ Nhân viên nào giữ vai trò Nghiên cứu của đề tài gọi được (không giới hạn theo `assignee_id`); dùng `TransitionDraftStatus` (D-SD03-017 (¶4.2)), `assignee_id` giữ nguyên, không tạo phiên bản mới |
| POST | `/knowledge/knowledge-objects/{id}/approve` | `knowledge.approveKnowledgeObject` | admin, partner | `dang_xet_duyet → dat_xet_duyet` sau bước 8.3 (R-KB-092 (§2.2.6.10)) |
| POST | `/knowledge/knowledge-objects/{id}/publish` | `knowledge.publishKnowledgeObject` | admin | Quyết định "Xuất bản" (`PublishVersion`) — chỉ vai trò Xuất bản |
| POST | `/knowledge/knowledge-objects/{id}/skip-publish` | `knowledge.skipKnowledgeObjectPublish` | admin | Quyết định "Không xuất bản" — body `{confirmed}` — chỉ vai trò Xuất bản |
| POST | `/knowledge/knowledge-objects/{id}/reopen` | `knowledge.reopenKnowledgeObject` | admin, partner | Mở lại từ `da_xuat_ban`/`khong_xuat_ban` — body `{target_status}` — chỉ vai trò Xét duyệt |
| POST | `/knowledge/knowledge-objects/{id}/set-used-version` | `knowledge.setKnowledgeObjectUsedVersion` | admin | Chọn/đổi `used_version_id` (D-SD03-013 (¶3.4) thao tác (b)) — body `{version_id}` — chỉ vai trò Xuất bản |

Vai trò Xuất bản là role theo chức năng (R-KB-072 (§2.2.5.4), không theo phạm vi đề tài) nhưng theo `business-requirements.md` R-PTN-003 (§2.7.2), Nhân viên Tổ chức khác **không có** vai trò Xuất bản — chỉ Nhân viên Tổ chức Văn Minh Việt mới được gán vai trò này. Vì vậy 3 endpoint `publish`/`skip-publish`/`set-used-version` **chỉ mount ở `admin`** — khác với các endpoint còn lại của D-SD03-024 (¶5.4) (mount cả `admin`, `partner`); `reopen` (vai trò Xét duyệt) vẫn mount ở cả hai vì vai trò Xét duyệt có ở `partner` (R-PTN-003 (§2.7.2)).

### 5.5. [D-SD03-025] Webhook nội bộ nhận tín hiệu đồng bộ MinIO/S3

⚠ Không mount dưới `/api/v1/{admin,partner,public}/...` — đây là endpoint nội bộ nhận sự kiện từ hạ tầng object storage (MinIO/S3 bucket notification), không phải Nhân viên/Người dùng gọi trực tiếp, nên đặt riêng theo đúng tinh thần `/internal/ingestion` đã nêu ở D-SD01-005 (¶5).

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| POST | `/internal/ingestion/source-webhook` | `internal.receiveSourceWebhook` | Nhận bucket notification — body tối thiểu `{source_id}` (đủ để tra `storage_prefix` từ DB, không cần payload nội dung file). ⚠ Xác thực bằng **shared secret** (header, hoặc HMAC ký trên body — cấu hình khi thiết lập bucket notification trên MinIO/S3), không dùng JWT Nhân viên vì bên gọi là hạ tầng, không phải người dùng. Gọi `/ingestion.HandleSourceReadyWebhook` (D-SD03-017 (¶4.2)) — debounce/coalesce trước khi thực sự chạy `SyncSourceFiles` |

### 5.6. [D-SD03-026] Tổng hợp mount theo nhóm route

| Nhóm resource | `admin` | `partner` | `public` |
|---|---|---|---|
| `research-topics` | Đầy đủ, **gồm xoá đề tài rỗng** (`knowledge.deleteResearchTopic`, D-SD03-001 (¶2.1)) | Thấy đề tài mình giữ **bất kỳ vai trò phạm vi nào** (`chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet`) và **xem tiến độ** đề tài đó (`progress`, D-SD03-015 (¶3.6)); quản lý nhân sự (Nghiên cứu/Xét duyệt) và tìm Nhân viên (`employee-search`) nếu là Chủ nhiệm đề tài của đề tài đó (R-KB-073 (§2.2.5.5)); không tạo đề tài, không xoá đề tài, không `set-chair` | Không mount |
| `sources` | Đầy đủ | Chỉ đọc 1 dòng, lồng theo `research-topics/{id}` (⚠ bổ sung, xem D-SD03-021 (¶5.1)) — không mount `/knowledge/sources` độc lập | Không mount |
| `knowledge-objects` (+ luồng xét duyệt, `claims`) | Đầy đủ, xem toàn bộ với `quan_tri_he_thong` (D-SD03-014 (¶3.5)) | Đầy đủ trừ `publish`/`skip-publish`/`set-used-version` (chỉ `admin`, vai trò Xuất bản, xem D-SD03-024 (¶5.4)), giới hạn theo đề tài được gán vai trò `nghien_cuu`/`xet_duyet` (không gồm `chu_nhiem_de_tai`, xem D-SD03-023 (¶5.3)); riêng `knowledge.deleteKnowledgeObject` mở thêm cho Chủ nhiệm đề tài của đề tài cha (D-SD03-005 (¶2.5)) | Không mount |
| `internal.receiveSourceWebhook` | *(ngoài 3 nhóm route chuẩn — xác thực riêng bằng shared secret, xem 5.5)* | | |

Mọi endpoint ghi ở 5.1–5.4 có audit log, cùng các sự kiện do hệ thống thực hiện (`source.sync` qua webhook, `knowledge_object.ai_verification_complete`) — `action_type` và `detail` theo danh mục sự kiện audit ở D-SD01-002 (¶2).

## 6. Vấn đề mở / giả định

> Các điểm dưới đây là đề xuất bổ sung thuần kỹ thuật/kiến trúc nội bộ của System Design (không đổi hành vi nghiệp vụ quan sát được từ bên ngoài), đã được người dùng duyệt trực tiếp, không cần gửi qua luồng Requirements để xác nhận. Giữ lại danh sách và dấu ⚠ chỉ để ghi nhận rõ đây là phần mở rộng ngoài đặc tả gốc, phục vụ tra cứu sau này.

- **Trạng thái `dang_xet_duyet_ai` và phạm vi kích hoạt lại AI Verification** (D-SD03-011 (¶3.2), D-SD03-012 (¶3.3) bước (3)) hiện thực R-KB-078 (§2.2.6.5.1)–R-KB-079 (§2.2.6.5.2); chế độ kích hoạt theo cấu hình R-CFG-006 (§2.8.4.1).
- **State machine cấp Đề tài nghiên cứu đặt ở `/knowledge`, không ở `/gate`** (D-SD03-010 (¶3.1), D-SD03-016 (¶4.1)) — ⚠ quyết định kiến trúc, không phải yêu cầu trực tiếp từ đặc tả; lý do: `/gate` giữ đúng phạm vi workflow xét duyệt Hạng mục tri thức, bản chất khác hẳn state machine 1-chiều của Đề tài.
- **`source_file.transcript_storage_key`** (D-SD03-004 (¶2.4)) — ⚠ đề xuất bổ sung, chưa gửi Requirements xác nhận riêng (khác với `knowledge_object_file.transcript_storage_key` ở D-SD03-007 (¶2.7) — phần phục vụ AI Verification kiểm Vị trí trong Nội dung đã được Requirements chấp thuận, R-KB-082 (§2.2.6.6.2)); cột này chỉ phục vụ mục đích kỹ thuật (UI nghiên cứu chọn đúng vị trí/thời điểm, AI Verification tra cứu nhanh).
- **`knowledge_object.created_by`/`created_at`** (D-SD03-005 (¶2.5)) — nay chính thức là R-KB-047 (§2.2.3.12) "Người tạo" và R-KB-048 (§2.2.3.13) "Ngày giờ tạo", Requirements đã chốt ngày 2026-09-23, không còn là đề xuất bổ sung thuần thiết kế.
- **Đường nhập Tư liệu gốc thủ công đặt ở `/knowledge`, không ở `/ingestion`** (D-SD03-020 (¶4.5)) — quyết định kiến trúc; đặc tả gốc chỉ nêu vai trò Nhập liệu thực hiện việc nhập tư liệu (R-KB-069 (§2.2.5.1)), không quy định package/kiến trúc kỹ thuật cụ thể.
- **Cơ chế debounce/coalesce cho webhook đồng bộ MinIO/S3** (D-SD03-017 (¶4.2), D-SD03-020 (¶4.5)) — ⚠ độ trễ debounce và thời gian hoãn job khi advisory lock đang bị giữ cùng dùng tham số cấu hình `operations.source_sync_debounce_seconds` (mặc định 45s, `07-system-settings.md`), không phải giá trị cố định từ đặc tả. Job nối tiếp (`follows_job_id`) là cách hiện thực kỹ thuật do river luôn tính job đang chạy là bản trùng.
- **Xác thực webhook `internal.receiveSourceWebhook` bằng shared secret/HMAC, không qua JWT Nhân viên** (D-SD03-025 (¶5.5)) — ⚠ quyết định kiến trúc thuần kỹ thuật: bên gọi là hạ tầng MinIO/S3, không phải người dùng, nên không dùng cùng cơ chế xác thực Nhân viên (D-SD01-007 (¶7)); cơ chế cụ thể (loại secret, vị trí header/HMAC) chốt khi triển khai.
- **Giao diện Nghiên cứu để tạo Nội dung là upload file trực tiếp, không phải Rich Text Editor** (D-SD03-007 (¶2.7)) — ⚠ quyết định người dùng: nhà nghiên cứu vốn không quen/không thích soạn thảo trên web, và Nội dung ở module này chỉ là tài liệu làm việc nội bộ (khác Mục từ, module 04, cần trình bày công khai nên dùng TipTap); hệ quả UI: cần bộ chọn vị trí trong file tĩnh đã upload (page/line, khung ảnh, timeline), không cần trình soạn thảo trực tuyến.
- **Endpoint `resume-research` cho transition `khong_dat_xet_duyet → dang_nghien_cuu`** (D-SD03-012 (¶3.3) bước (7), D-SD03-017 (¶4.2), D-SD03-024 (¶5.4)) — ⚠ bổ sung: hành vi nghiệp vụ có sẵn trong đặc tả gốc (R-KB-091 (§2.2.6.9)), thực thi bằng cách tái dùng hàm `TransitionDraftStatus` sẵn có (nhất quán với `reject`/`approve`); không giới hạn quyền gọi theo `assignee_id` — bất kỳ Nhân viên nào giữ vai trò Nghiên cứu của đề tài đều gọi được, nhất quán với `submit-for-review`.
- **Route mới `knowledge.getResearchTopicSource` — `GET /knowledge/research-topics/{id}/sources/{source_id}`** (D-SD03-021 (¶5.1), D-SD03-022 (¶5.2)) — ⚠ bổ sung: giải quyết khoảng trống route đọc file Tư liệu gốc ở `partner`, cần thiết cho màn hình Nghiên cứu khi tạo Tham chiếu (chọn file + vị trí). Phạm vi tự động giới hạn theo Đề tài được gán (đã kiểm quyền ở `research-topics/{id}`, D-SD03-021 (¶5.1)), không mở route đọc `sources` độc lập/không giới hạn ở `partner`.
- **Vai trò Chủ nhiệm đề tài (`chu_nhiem_de_tai`) và quyền quản lý nhân sự đề tài** (D-SD03-001 (¶2.1), D-SD03-017 (¶4.2), D-SD03-021 (¶5.1)) — role mới theo `requirements/business-requirements.md` R-KB-073 (§2.2.5.5) (bổ sung 2026-09-22): role theo phạm vi thứ 3 bên cạnh Nghiên cứu/Xét duyệt, tự sinh cùng lúc khi tạo đề tài, đúng 1 người giữ/đề tài, chỉ Quản trị hệ thống gán/đổi. ⚠ Các endpoint `set-chair`/`researchers`/`reviewers`/`members` (D-SD03-021 (¶5.1)), các hàm `SetTopicChair`/`AssignResearcher`/`RemoveResearcher`/`AssignReviewer`/`RemoveReviewer`/`ListTopicMembers` (D-SD03-017 (¶4.2)), và cơ chế `is_singular` phía `/identity` (D-SD02-001 (¶2), D-SD02-008 (¶4)) là thiết kế kỹ thuật để hiện thực quyền "Chủ nhiệm đề tài tự gán/gỡ Nghiên cứu, Xét duyệt cho đề tài mình phụ trách" (R-KB-073 (§2.2.5.5)) — chi tiết route/tên hàm không có trong đặc tả gốc.
- **Bộ lọc phạm vi ở `partner` gồm cả `chu_nhiem_de_tai` (D-SD03-021 (¶5.1)), nhưng route Hạng mục tri thức thì không (D-SD03-023 (¶5.3))** — bám đúng R-PTN-003 (§2.7.2)–R-PTN-004 (§2.7.3): Chủ nhiệm đề tài được giao đúng việc quản lý nhân sự (R-PTN-008 (§2.7.3.4)), không được giao việc nghiên cứu/xét duyệt. ⚠ **Hệ quả đã được xử lý (2026-09-23)**: Chủ nhiệm đề tài không kiêm vai trò Nghiên cứu/Xét duyệt nay **xem được tiến độ** đề tài mình phụ trách (D-SD03-015 (¶3.6), endpoint `progress`), nhưng vẫn **không xem được Nội dung/Phát biểu/kết quả xét duyệt** của Hạng mục tri thức — đúng phạm vi đã chốt, không còn là câu hỏi treo gửi Requirements.
- **`GetUsedVersionContent` và `GetUsedVersionIDs` (D-SD03-017 (¶4.2))** — ⚠ 2 interface đọc do `/knowledge` expose cho `/encyclopedia`. `GetUsedVersionContent` đã được D-SD04-012 (¶4.2) khai báo và sử dụng từ 2026-09-13 nhưng còn thiếu trong danh sách interface của tài liệu này (phát hiện khi rà soát chéo 2026-09-23). `GetUsedVersionIDs` là bản đọc nhẹ dạng batch, bổ sung cùng ngày để `/encyclopedia` tính cờ "nguồn đã lỗi thời" (`is_outdated`, D-SD04-015 (¶5.1)) mà không phải kéo toàn bộ nội dung. Thuần dọn/bổ sung tài liệu cho khớp, không đổi hành vi nghiệp vụ.
- **Quyền xem tiến độ của Chủ nhiệm đề tài** (D-SD03-015 (¶3.6), D-SD03-017 (¶4.2), D-SD03-021 (¶5.1)) — nay chính thức là R-KB-073 (§2.2.5.5) (đoạn tiến độ) và R-PTN-009 (§2.7.3.5), Requirements đã chốt ngày 2026-09-23 đúng theo đề nghị đã gửi. Phạm vi đã chốt là hẹp — thống kê theo trạng thái + danh sách Hạng mục tri thức ở mức tiến độ, không gồm nội dung/kết quả xét duyệt (khác với quyền chỉ-đọc toàn bộ của Quản trị hệ thống ở R-KB-007 (§2.2.1.5)).
- **Xoá Đề tài nghiên cứu rỗng và xoá Hạng mục tri thức** (D-SD03-001 (¶2.1), D-SD03-005 (¶2.5), D-SD03-017 (¶4.2), D-SD03-021 (¶5.1), D-SD03-023 (¶5.3)) — nay chính thức là R-KB-012 (§2.2.1.7) và R-KB-049 (§2.2.3.14), Requirements đã chốt ngày 2026-09-23; đồng thời đóng điểm lệch ghi nhận ở đợt rà soát chéo cùng ngày (D-SD03-001 (¶2.1) mô tả hành vi "khi xoá đề tài" nhưng D-SD03-021 (¶5.1) không có endpoint xoá). Các quyết định kỹ thuật đi kèm do người dùng chốt, nay khớp đúng đặc tả: **xoá cứng** (không dùng cột `deleted_at`, R-KB-016 (§2.2.1.7.4)/R-KB-055 (§2.2.3.14.6)); điều kiện "rỗng" **chỉ** tính số Hạng mục tri thức (Tư liệu gốc đã gán và trạng thái `tu_lieu_san_sang` không chặn); người xoá Hạng mục tri thức gồm cả Chủ nhiệm đề tài và Người phụ trách hiện tại, không chỉ Quản trị hệ thống. ⚠ Bất đối xứng có chủ đích: Chủ nhiệm đề tài xoá được một Hạng mục tri thức mà lại không đọc được nội dung của nó — chấp nhận vì Chủ nhiệm là người chịu trách nhiệm chính của đề tài (R-KB-073 (§2.2.5.5)), và điều kiện xoá đã giới hạn ở hạng mục chưa có phiên bản chốt, đang `dang_nghien_cuu`, chưa bị Mục từ tham chiếu. Cũng ⚠ khác D-SD02-010 (¶5.2) (không có xoá cứng Nhân viên/Tổ chức) — khác biệt có chủ đích: đề tài rỗng không để lại tham chiếu nghiệp vụ nào, vết xoá vẫn nằm ở `audit_log`.
- **`ON DELETE RESTRICT` cho `entry_knowledge_object.knowledge_object_id`** (D-SD03-017 (¶4.2)) — ⚠ quyết định kỹ thuật đi kèm cơ chế xoá ở trên: dùng ràng buộc CSDL thay vì gọi ngược sang `/encyclopedia` để kiểm, giữ đúng hướng phụ thuộc một chiều (04 → 03). Ghi kèm 1 câu tương ứng ở D-SD04-004 (¶2.4).
- **Upload/download presigned URL, tên hiển thị kèm ID, số đếm trong danh sách, tìm kiếm Nhân viên cho Chủ nhiệm đề tài, làm rõ quyền `sources`/`mark-ready`** (D-SD03-007 (¶2.7), D-SD03-017 (¶4.2), D-SD03-021 (¶5.1), D-SD03-022 (¶5.2), D-SD03-023 (¶5.3)) — ⚠ đợt bổ sung 2026-09-23, thuần hoàn thiện kỹ thuật, không đổi hành vi nghiệp vụ: (1) `RequestKnowledgeObjectFileUpload`/`GetKnowledgeObjectFileDownloadURL`/`GetSourceFileDownloadURL` hiện thực quy ước 2 bước đã chốt ở D-SD01-003 (¶3) — trước đó D-SD03-023 (¶5.3) có endpoint xác nhận file (`knowledge.createKnowledgeObjectFile`) nhưng chưa có endpoint xin URL lẫn endpoint tải file đã có; (2) `chair`/`assignee`/`created_by`/`frozen_by` đổi từ ID thuần sang object `{id, display_name}` ở các response danh sách/chi tiết — giải quyết khoảng trống FE (`admin-web`/`partner-web`) phải tự tra cứu tên hiển thị cho từng ID; (3) `source_count`/`knowledge_object_count` bổ sung vào response danh sách đề tài — khớp cột đã có sẵn ở D-ADM-008 (¶4.8)/D-PRT-004 (¶4.4); (4) `SearchEmployeesForTopic`/endpoint `employee-search` — Chủ nhiệm đề tài trước đó không có API nào để tìm Nhân viên khi thêm Nghiên cứu/Xét duyệt (D-PRT-009 (¶4.9)/D-PRT-010 (¶4.10) đã chốt phạm vi không giới hạn Tổ chức); (5) đoạn "Quyền" mới ở D-SD03-022 (¶5.2) — làm rõ tường minh `sources`/`mark-ready` yêu cầu role `nhap_lieu` hoặc `quan_tri_he_thong` ở tầng service (mount `admin` chỉ chặn Tổ chức khác, không thu hẹp role trong `admin`), để tránh lặp lại tình trạng code chỉ cho phép `quan_tri_he_thong` trong khi thiết kế đã luôn cho phép cả `nhap_lieu`.
