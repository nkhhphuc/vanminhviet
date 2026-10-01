# Kiến Trúc & Tech Stack — Văn Minh Việt

> Lịch sử thay đổi của tài liệu này được ghi tại `system-design/changelog.md`.

## 0. Mục đích tài liệu này

Ghi lại các quyết định kiến trúc/tech stack dùng chung cho cả 4 module nghiệp vụ (Quản lý người dùng, Cơ sở dữ liệu văn hóa, Bách khoa toàn thư, AI Văn Minh Việt). Không mô tả mô hình dữ liệu nghiệp vụ chi tiết — phần đó thuộc từng tài liệu module (`02`–`05`).

## 1. [D-SD01-001] Tech stack — đã chốt

| Lớp | Công nghệ | Ghi chú |
|---|---|---|
| Backend API | Go | Modular monolith — xem D-SD01-002 (¶2) |
| Database | PostgreSQL 16+ | + `pgvector` (vector search cho RAG), + `pg_trgm`/`unaccent`/`tsvector` (full-text tiếng Việt) + JSONB (trường linh hoạt). Bắt đầu chỉ với Postgres (chưa cần search engine riêng như Meilisearch/Elasticsearch) — tải công khai hiện tại (R-NFR-010 (§3.2.1): 50–100 rps, burst 200–300) chưa đủ lớn để cần thêm; theo dõi hiệu năng thực tế sau khi vận hành, chỉ thêm nếu số liệu thật cho thấy không đủ. Hạ tầng/nhà cung cấp phải đặt trong lãnh thổ Việt Nam (data residency, R-NFR-005 (§3.1.3) đặc tả gốc) |
| Database (mở rộng sau) | + PostGIS | Chỉ cần nếu làm Bản đồ văn hóa — hiện ngoài phạm vi đặc tả, tạm chưa cần |
| Object storage | S3-compatible / MinIO | Lưu file tư liệu gốc (văn bản, ảnh, âm thanh, phim). **Không xoá phiên bản cũ** (yêu cầu truy vết, R-KB-029 (§2.2.3.4) đặc tả gốc) — dùng storage-class tiering (hot/cold) để tối ưu chi phí khi kho phình to; ngưỡng cụ thể (bao lâu chuyển cold) chốt sau khi có số liệu tăng trưởng thực tế, chưa chốt ngay bây giờ. Hạ tầng/nhà cung cấp phải đặt trong lãnh thổ Việt Nam (data residency, R-NFR-005 (§3.1.3) đặc tả gốc). ⚠ Việc nạp file cho Tư liệu gốc (`source`/`source_file`, module 03) vào bucket nằm **ngoài hệ thống** — nền tảng chỉ tự quản lý upload (presigned URL, D-SD01-003 (¶3)) cho các loại file khác, ví dụ `knowledge_object_file` — xem D-SD01-005 (¶5) |
| Hàng đợi job | river (thư viện Go, lưu job trong chính PostgreSQL) | Chạy nền: xử lý dữ liệu nạp vào, embedding, AI Verification… (danh sách ở D-SD01-004 (¶4)). Có sẵn retry/dead-letter (trạng thái `discarded`), unique job, lịch chạy trễ và hoãn job (snooze) — dùng cho cơ chế gộp (coalesce) webhook đồng bộ MinIO/S3 (D-SD01-005 (¶5); chi tiết D-SD03-017 (¶4.2)). Job nằm cùng CSDL nghiệp vụ nên **enqueue/chạy lại/huỷ job thực hiện được trong cùng transaction** với thao tác nghiệp vụ (`InsertTx`, `JobRetryTx`, `JobCancelTx`) — cùng nguyên tắc chống dual-write đã áp dụng cho `audit_log` (D-SD01-002 (¶2)). Trạng thái job truy vấn trực tiếp bằng SQL (D-SD01-004 (¶4)) |
| Cache | Redis — không bắt buộc ở giai đoạn ra mắt | Chỉ bổ sung khi phát sinh nhu cầu cache cụ thể; hàng đợi job không phụ thuộc Redis |
| CDN | Chưa dùng — phục vụ trực tiếp (local/origin) | Để chọn công nghệ cụ thể (Cloudflare/CloudFront...) ở giai đoạn sau khi lưu lượng thực tế yêu cầu; hiện tại phục vụ trực tiếp từ Object storage/Next.js là đủ cho quy mô ra mắt (R-NFR-010 (§3.2.1)) |
| Containerization & Orchestration | Docker (đóng gói); orchestration để mở | Mọi service (Go monolith, 2 app Nhân viên, Next.js, AI service) đóng gói bằng Docker. Công cụ orchestration (Kubernetes/Nomad/docker-compose cho production...) chưa chốt — do đội triển khai (deployer) quyết định theo hạ tầng thực tế lúc đó |
| Reverse proxy / Routing | Dev: Docker Compose · Production: Traefik | Định tuyến giữa các app (Admin nội bộ, Cổng Tổ chức khác, Web công khai, API) theo domain/path — khớp ranh giới route/API đã chốt ở D-SD01-002 (¶2) |
| Email / SMTP | Dev: Mailpit (container) · Production: Amazon SES (giao thức SMTP) | Phục vụ gửi email dùng chung cho nhiều module (mời/tạo tài khoản, đặt lại mật khẩu ở module 02; thông báo trạng thái xét duyệt ở module 03...) — xem `/shared` ở D-SD01-002 (¶2). ⚠ **Email không thuộc phạm vi R-NFR-005 (§3.1.3)** (data residency) — đặc tả gốc liệt kê rõ phạm vi là dữ liệu lưu trữ lâu dài (dữ liệu cá nhân Nhân viên, Tư liệu gốc, nội dung Hạng mục tri thức và Mục từ trong DB/Object storage), không bao gồm hạ tầng truyền tải/chuyển tiếp như SMTP relay — giữ nguyên Amazon SES, không cần đổi nhà cung cấp |
| Admin nội bộ (backend UI) | Quasar (Vue 3) + Pinia | Cho Nhân viên thuộc Tổ chức Văn Minh Việt (R-GEN-009 (§1.2.3.1) đặc tả gốc) — đầy đủ chức năng, gồm quản lý người dùng/phân quyền/Tổ chức |
| Trình soạn thảo nội dung Mục từ | TipTap (Vue 3) | Dùng trong Admin nội bộ cho vai trò Biên tập (R-ENC-019 (§2.3.4) đặc tả gốc) soạn nội dung Mục từ dạng JSON block (R-ENC-007 (§2.3.2.3.1) đặc tả gốc). Core mã nguồn mở (MIT), tự host, không dùng gói Cloud trả phí của TipTap. Dựng trên ProseMirror nên định nghĩa được các loại khối (Node) tuỳ biến cho từng loại nhúng file (ảnh/audio/phim) đúng vị trí, khớp mô hình block đã chốt |
| Cổng Nhân viên Tổ chức khác | Quasar (Vue 3) + Pinia, **app/deploy riêng** khỏi Admin nội bộ | Cho Nhân viên thuộc Tổ chức khác (R-GEN-010 (§1.2.3.2), module 2.7 đặc tả gốc) — chỉ vai trò Nghiên cứu/Xét duyệt theo Đề tài được gán, không có màn hình quản lý người dùng/Tổ chức. Tách app riêng (không chỉ ẩn UI trong cùng app Admin) để ranh giới bảo mật rõ ràng ở cả tầng route/API — xem D-SD01-002 (¶2) |
| Hạ tầng AI | GPU on-prem + service Python riêng | Self-host, tách khỏi Go monolith — xem D-SD01-006 (¶6) (gồm cả chế độ chạy không cần GPU cho môi trường phát triển local). Serving: **vLLM** cho LLM/embedding/VLM (một framework, nhiều model tương thích); **ASR riêng** (faster-whisper/PhoWhisper) vì ASR không serve tốt qua vLLM — 2 service nhỏ, không ép chung 1 framework |
| Web công khai | Next.js (SSR/SSG) | Cho Người dùng công khai (R-GEN-007 (§1.2.2), R-PUB-001 (§2.6) đặc tả gốc) — truy cập ẩn danh, không cần đa ngôn ngữ (đặc tả đã bỏ hỗ trợ đa ngôn ngữ) |
| Mobile app | Flutter | Giai đoạn sau — khi triển khai sẽ gọi vào nhóm route `/api/v1/public/...` (D-SD01-002 (¶2)), cùng nhóm với Web công khai, vì cũng phục vụ Người dùng công khai. ⚠ R-NFR-018 (§3.3.3) đặc tả gốc ghi "ngay từ giai đoạn ra mắt" — tài liệu này giữ định hướng "giai đoạn sau"; cần làm rõ lại với luồng Requirements nếu cần đối chiếu ý định thật sự của R-NFR-018 (§3.3.3) |

## 2. [D-SD01-002] Kiến trúc Backend — Modular Monolith

Đề xuất một service Go duy nhất, chia module theo domain, biên giới rõ để có thể tách ra sau nếu cần.

**Nguyên tắc giữ khả năng tách thành service độc lập sau này**: mỗi package trong `/internal` chỉ được thao tác trực tiếp lên các bảng do chính nó sở hữu; giao tiếp cross-domain thực hiện qua hàm/interface nội bộ (Go function call), không JOIN chéo sang bảng do package khác sở hữu. Đây là điều kiện để sau này, khi cần, có thể tách một package thành service riêng (đóng gói container riêng, route riêng qua reverse proxy — D-SD01-001 (¶1)) mà không phải viết lại toàn bộ tầng truy cập dữ liệu. Việc `/assistant` và `/verification` (bên dưới) đã gọi ra AI service qua API nội bộ ngay từ giai đoạn monolith là một ví dụ đã áp dụng đúng nguyên tắc này.

Thứ tự các package dưới đây theo đúng luồng giá trị đã mô tả ở R-KB-001 (§2.2) đặc tả gốc: `Tư liệu Hán Nôm → Nghiên cứu → Dữ liệu chuẩn → Bách khoa → Trợ lý số` (cũng trùng với thứ tự module 02→03→04→05):

```
/cmd/api          # entrypoint HTTP
/cmd/worker       # entrypoint worker — xử lý job nền qua river (D-SD01-001 (¶1), D-SD01-004 (¶4)), đóng gói/deploy độc lập với /cmd/api
/internal
  /identity       # module 02 — user, role, Tổ chức (R-ID-009 (§2.1.4) đặc tả gốc), phiên đăng nhập, RBAC — nền tảng, mọi package khác đều phụ thuộc
  /ingestion      # module 03 — nhận tín hiệu đồng bộ (webhook debounce từ MinIO/S3) và gọi /knowledge.SyncSourceFiles — xem D-SD01-005 (¶5)
  /knowledge      # module 03 — Đề tài nghiên cứu, Tư liệu gốc, Hạng mục tri thức (→ Nghiên cứu)
  /provenance     # module 03 — claim, claim_reference, truy vết — tạo cùng lúc với việc nghiên cứu ở /knowledge
  /gate           # module 03 — workflow trạng thái Hạng mục tri thức (R-KB-074 (§2.2.6), → Dữ liệu chuẩn) + các bước xét duyệt chuyên gia thủ công; kích hoạt AI Verification theo trạng thái (R-KB-077 (§2.2.6.5)), giao cho /verification xử lý — không liên quan workflow Mục từ (xem /encyclopedia)
  /verification   # module 03 — AI Verification, Trợ lý Tư liệu gốc (R-KB-080 (§2.2.6.6)); nhận kích hoạt từ /gate, gọi năng lực Verification của AI service (D-SD01-006 (¶6)) qua API nội bộ, ghi kết quả vào Tham chiếu
  /encyclopedia   # module 04 (→ Bách khoa) — Mục từ, Cương vực; quan hệ nhiều-nhiều gộp/tách với Hạng mục tri thức gọi qua interface nội bộ tới /knowledge (không JOIN chéo); vai trò Biên tập soạn nội dung JSON block (D-SD01-001 (¶1) — TipTap) và tự quản lý workflow trạng thái Mục từ (R-ENC-022 (§2.3.5), đồ thị đối xứng với Hạng mục tri thức R-KB-074 (§2.2.6) — kết thúc bằng quyết định Xuất bản/Không xuất bản của vai trò Xuất bản Mục từ; Mục từ đang hiển thị công khai xác định qua con trỏ **phiên bản đang công khai** (R-ENC-010 (§2.3.2.4.1)), cùng cơ chế `used_version_id` đã dùng ở module 03; chi tiết chốt ở `04-encyclopedia.md`); vai trò Xét duyệt Mục từ xét duyệt riêng, khác vai trò Xét duyệt Hạng mục tri thức ở /gate
  /assistant      # module 05 (→ Trợ lý số) — RAG orchestration cho AI Văn Minh Việt, dẫn nguồn; đọc nội dung **phiên bản đang công khai** của Mục từ (con trỏ, R-ENC-010 (§2.3.2.4.1), xem /encyclopedia) + Cương vực qua interface nội bộ tới /encyclopedia — Cương vực dùng để giới hạn phạm vi truy hồi khi người dùng chọn lọc (R-AI-004 (§2.4.3) đặc tả gốc); sinh embedding qua job nền (D-SD01-004 (¶4)), gắn theo đúng phiên bản, re-index khi con trỏ đổi — xem D-SD01-006 (¶6); chỉ gọi năng lực RAG của AI service (D-SD01-006 (¶6)) qua API nội bộ, không tự host model
  /shared         # dùng chung nhiều module, không thuộc riêng module nghiệp vụ nào — db, logger, config, errors, i18n, gửi email/thông báo dùng chung (SMTP — D-SD01-001 (¶1)), audit_log + usage_event (xem đoạn dưới), API theo dõi job nền (D-SD01-004 (¶4)), cấu hình hệ thống runtime do Quản trị hệ thống chỉnh (bảng system_setting — 07-system-settings.md); ví dụ: mời/reset tài khoản ở module 02, thông báo trạng thái xét duyệt ở module 03
```

**Triển khai workflow xét duyệt (`/gate`, `/encyclopedia`)**: cả 2 workflow (Hạng mục tri thức R-KB-074 (§2.2.6), Mục từ R-ENC-022 (§2.3.5)) đã được đặc tả gốc mô tả cố định — **không xây engine cấu hình workflow qua UI kiểu Jira/Atlassian**. Chi phí xây một engine đủ tổng quát (schema định nghĩa trạng thái/transition động, UI cấu hình cho admin, versioning workflow khi có bản ghi đang giữa chừng, cơ chế hook/side-effect gắn động cho bước như kích hoạt AI Verification) không tương xứng với quy mô hệ thống (D-SD01-008 (¶8)), và không có yêu cầu nào cần người vận hành tự đổi quy trình mà không cần lập trình viên.

Thay vào đó, `/gate` và `/encyclopedia` mỗi package tự khai báo state machine riêng bằng một thư viện state-machine nhỏ dùng chung (đặt trong `/shared`) — cung cấp kiểu dữ liệu chung cho trạng thái, transition hợp lệ, guard theo quyền (role), và hook khi vào/rời trạng thái (ví dụ `/gate` dùng hook để kích hoạt AI Verification, R-KB-077 (§2.2.6.5)). Đồ thị trạng thái định nghĩa **bằng code Go, không cấu hình runtime** — mỗi package vẫn tự sở hữu bảng trạng thái của mình, đúng nguyên tắc biên giới package ở trên.

Cột lưu trạng thái trong DB dùng kiểu **text/varchar thường + validate ở tầng ứng dụng**, không dùng kiểu ENUM riêng của Postgres — vì Postgres cho thêm giá trị ENUM dễ nhưng xoá/đổi tên giá trị ENUM rất phiền (không xoá trực tiếp được, phải tạo type mới rồi migrate cột). Khi quy trình xét duyệt cần đổi:

- **Thêm transition hoặc trạng thái mới chen vào luồng**: chỉ là thay đổi code (thêm hằng số trạng thái, cập nhật bảng transition hợp lệ, guard/hook nếu cần) + deploy — không cần migrate dữ liệu cũ, vì bản ghi hiện có giữ nguyên trạng thái hiện tại, chỉ áp dụng luồng mới cho lần chuyển trạng thái tiếp theo. Audit log (D-SD01-003 (¶3)) của các bản ghi cũ vẫn phản ánh đúng luồng tại thời điểm đó, không cần viết lại.
- **Bỏ một trạng thái đang được dùng**: không xoá khỏi code (để đọc lịch sử cũ vẫn đúng), chỉ chặn transition mới đi vào trạng thái đó, và chạy thao tác thủ công một lần để chuyển các bản ghi đang mắc kẹt sang trạng thái tương đương mới.

**Audit log & usage tracking (`/shared`)**: hai bảng `audit_log` (ghi ai/khi nào/đổi gì cho mọi thao tác ghi — D-SD01-003 (¶3), bắt buộc cho luồng xét duyệt) và `usage_event` (đo lường mức sử dụng theo Tổ chức, chuẩn bị cho việc tính chi phí trong tương lai — R-ID-015 (§2.1.4.6) đặc tả gốc) đều đặt trong `/shared`, không thuộc riêng module nghiệp vụ nào — cùng nguyên tắc đã áp dụng cho việc gửi email dùng chung (D-SD01-001 (¶1)). Các package khác (`/gate`, `/knowledge`, `/encyclopedia`, `/verification`...) gọi hàm nội bộ (`shared.RecordAudit(...)`, `shared.RecordUsage(...)`) tại điểm phát sinh, không tự chạm 2 bảng này — đúng nguyên tắc biên giới package ở trên.

**Phạm vi audit log (R-NFR-004 (§3.1.2) đặc tả gốc, đã mở rộng)**: R-NFR-004 (§3.1.2) yêu cầu tối thiểu: đăng nhập/đăng xuất Nhân viên, tạm khoá đăng nhập và gỡ tạm khoá (R-ID-030 (§2.1.5.9)), đổi mật khẩu (R-ID-035 (§2.1.5.10)), nhập/gán Tư liệu gốc, thay đổi trạng thái Đề tài nghiên cứu, xoá Đề tài nghiên cứu (R-KB-012 (§2.2.1.7)), nghiên cứu/xét duyệt/đổi trạng thái Hạng mục tri thức, xoá Hạng mục tri thức (R-KB-049 (§2.2.3.14)), soạn thảo/xét duyệt/xuất bản Mục từ, tạo/sửa/xoá Cương vực (R-ENC-037 (§2.3.7.5)), thay đổi phân quyền/role của Nhân viên (gồm cả việc Chủ nhiệm đề tài gán/gỡ vai trò Nghiên cứu/Xét duyệt — R-KB-073 (§2.2.5.5)), vô hiệu hoá/kích hoạt lại tài khoản (R-ID-024 (§2.1.5.7)), tạo/sửa Tổ chức, thay đổi cấu hình hệ thống (R-CFG-004 (§2.8.3)). ⚠ Thiết kế mở rộng thành: **mọi thao tác ghi thành công** của Nhân viên, cộng các thay đổi do hệ thống tự thực hiện trên dữ liệu nghiệp vụ. Danh sách đầy đủ ở "Danh mục sự kiện audit" bên dưới — đây là nguồn duy nhất; tài liệu module không liệt kê lại. Thao tác bị từ chối (lỗi validate, sai quyền, sai trạng thái) không ghi, trừ `auth.login_locked`. **Thời hạn lưu**: theo tham số `operations.audit_log_retention_months` (mặc định 24 tháng, không dưới 12 — R-NFR-004 (§3.1.2), R-CFG-010 (§2.8.4.5)); bản ghi quá hạn được xoá định kỳ bởi job `shared.audit_log_cleanup` (D-SD01-004 (¶4), D-SD07-009 (¶4.3)).

Thời điểm ghi: cùng transaction với thao tác nghiệp vụ (xem đoạn "Ghi đồng bộ" bên dưới). Ngoại lệ: `auth.login`/`auth.logout` ghi ngay sau khi xử lý xong, vì không có bản ghi nghiệp vụ đi kèm; `auth.login_locked` ghi trong transaction cập nhật bộ đếm đăng nhập sai (transaction này commit dù request trả lỗi). Sự kiện do hệ thống thực hiện ghi cùng transaction của job tạo ra thay đổi đó.

**⚠ Đề xuất bổ sung — Schema `audit_log` và API đọc lại**: phần trên mới chỉ mô tả bằng lời việc *ghi* audit log; phần này bổ sung schema cụ thể và một API *đọc lại*, phục vụ nhu cầu giám sát hoạt động Nhân viên qua Admin nội bộ (D-ADM-021 (¶4.21) — Nhật ký hoạt động). Đây là hoàn thiện kỹ thuật cho yêu cầu đã duyệt ở R-NFR-004 (§3.1.2) (phải ghi audit log) — không thay đổi hành vi nghiệp vụ nào của Nhân viên khác, không phát sinh mô hình phân quyền mới (quyền xem giới hạn `quan_tri_he_thong`, nhất quán với quyền xem toàn bộ đã có ở R-KB-007 (§2.2.1.5)).

Schema `audit_log`:

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Khoá chính |
| `employee_id` | UUID (nullable) | Nhân viên thực hiện hành động; `NULL` khi `actor_type = system`. Tham chiếu `employee.id` — **Không đặt ràng buộc FK ở tầng CSDL** (khác các cột tham chiếu `employee.id` thông thường ở nơi khác trong hệ thống) — vì audit log phải giữ đủ lịch sử bất biến (R-NFR-004 (§3.1.2), tối thiểu 12 tháng) độc lập với vòng đời `employee`; một FK cứng sẽ chặn xoá `employee` (nếu sau này triển khai "quyền xoá" theo Nghị định 13/2023/NĐ-CP, D-SD01-007 (¶7)) hoặc mất dấu vết nếu dùng CASCADE/SET NULL. Cùng tinh thần không-FK với `entity_id`/`entity_type` bên dưới (ở đó là do đa hình, ở đây là do yêu cầu bất biến) |
| `actor_type` | text | ⚠ Bổ sung — `employee` (Nhân viên thực hiện qua API) hoặc `system` (hệ thống tự thực hiện: job nền, webhook, tạm khoá tự động). Tập giá trị mở, không ENUM. Ràng buộc: `actor_type = employee` ⇔ `employee_id IS NOT NULL` |
| `action_type` | text | Tập giá trị mở, không ENUM (`00-claude-instructions.md` mục 6). Dạng `<nhóm>.<hành động>`, danh sách đầy đủ ở "Danh mục sự kiện audit" bên dưới |
| `entity_type` | text (nullable) | Loại **đối tượng nghiệp vụ gốc** bị tác động (`employee`, `organization`, `research_topic`, `source`, `knowledge_object`, `entry`, `cultural_domain`, `job`, `system_setting`). Thao tác trên thành phần con (Phát biểu, Tham chiếu, file, ánh xạ…) ghi theo đối tượng gốc chứa nó; id thành phần con nằm trong `detail` — để lọc theo một đối tượng là thấy toàn bộ lịch sử của nó |
| `entity_id` | UUID (nullable) | Id đối tượng gốc; `NULL` khi id không phải UUID (`job`, `system_setting`) |
| `detail` | JSONB (nullable) | Ngữ cảnh bổ sung tuỳ `action_type` (ví dụ trạng thái trước/sau khi đổi status) — không ép chung 1 schema |
| `created_at` | timestamptz | Thời điểm |

Interface đọc bổ sung (song song `RecordAudit` đã có):

```go
package shared

type AuditLogFilter struct {
    EmployeeID *uuid.UUID
    ActorType  *string   // ⚠ bổ sung: employee | system
    ActionType *string
    EntityType *string
    EntityID   *uuid.UUID
    From, To   *time.Time
}

func ListAuditLogs(ctx context.Context, filter AuditLogFilter, cursor string) ([]AuditLog, string, error)
```

API mới — chỉ mount ở nhóm `admin`, yêu cầu role `quan_tri_he_thong` (tầng service, D-SD01-007 (¶7)):

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/shared/audit-logs` | `shared.listAuditLogs` | Danh sách audit log — filter `employee_id`, `actor_type`, `action_type`, `entity_type`, `entity_id`, `from`, `to`; cursor pagination (D-SD01-003 (¶3)) |

Đây là endpoint HTTP đầu tiên do `/shared` tự expose trực tiếp (khác các hàm nội bộ `RecordAudit`/`RecordUsage` vốn chỉ gọi qua function call nội bộ) — vẫn hợp lệ vì `/shared` là package sở hữu đúng bảng `audit_log`, đúng nguyên tắc biên giới package ở trên.

Response `shared.listAuditLogs` — `GET /shared/audit-logs` — `shared.ListAuditLogs` (và bảng `audit_log`) chỉ trả nguyên `employee_id`, **không JOIN sang `/identity`** trong package `/shared` (đúng nguyên tắc biên giới package ở trên). Tên/email Nhân viên hiển thị ở màn hình Nhật ký hoạt động (D-ADM-021 (¶4.21)) được ghép ở **tầng handler HTTP** (`/cmd/api`, ngoài cả `/shared` lẫn `/identity`): sau khi gọi `shared.ListAuditLogs` lấy 1 trang audit log, handler gọi tiếp `identity.GetEmployeeSummaries` (D-SD02-008 (¶4)) với danh sách `employee_id` duy nhất trong trang đó, rồi ghép vào response cuối cùng:

```json
{
  "id": "uuid",
  "actor_type": "employee" | "system",
  "employee": { "id": "uuid", "display_name": "string", "email": "string" } | null,
  "action_type": "string", "entity_type": "string" | null, "entity_id": "uuid" | null,
  "detail": {}, "created_at": "timestamptz"
}
```

`employee` trả `null` khi `actor_type = system`, hoặc khi `employee_id` không khớp Nhân viên nào (hiếm — hiện chưa có xoá cứng Nhân viên, D-SD02-010 (¶5.2) — nhưng vẫn xử lý an toàn vì `audit_log.employee_id` cố ý không có FK, xem phần schema phía trên). Ghép ở tầng handler (thay vì trong `/shared` hay `/identity`) giữ đúng 2 nguyên tắc cùng lúc: `/shared` không JOIN chéo bảng `employee`, và không phát sinh import cycle Go giữa `/shared`/`/identity` (`/identity` đã gọi `shared.RecordAudit` — nếu `/shared` gọi ngược lại `/identity` sẽ thành vòng). Cách ghép này chỉ áp dụng cho đúng endpoint này, không phải nguyên tắc chung mới cho mọi API liệt kê.

**⚠ Danh mục sự kiện audit** — nguồn duy nhất cho mọi `action_type`. Thêm endpoint ghi mới thì phải thêm dòng vào đây. Nhãn tiếng Việt dùng cho màn hình Nhật ký hoạt động (D-ADM-021 (¶4.21)).

Quy ước `detail` chung:
- Không bao giờ chứa mật khẩu, token, hash, nội dung file.
- Đổi trạng thái: `{from_status, to_status}`.
- Sửa trường thông tin quản trị (Nhân viên, Tổ chức, Cương vực, cấu hình): `{changes: {<field>: {old, new}}}`, chỉ các trường thực sự đổi.
- Sửa nội dung soạn thảo (nội dung Mục từ, Phát biểu): chỉ id + tên trường đã đổi (`fields: [...]`), không chép nội dung — nội dung đã có ở bản soạn thảo/phiên bản.
- Sự kiện `system` từ job: có `job_id`.

**1. Xác thực (`/identity`, nhóm `auth/*`)**

| `action_type` | Nhãn | Actor | Endpoint / nguồn | entity | `detail` |
|---|---|---|---|---|---|
| `auth.login` | Đăng nhập | employee | `auth.login` | `employee` | `{channel: admin\|partner}` |
| `auth.logout` | Đăng xuất | employee | `auth.logout` | `employee` | `{channel}` |
| `auth.login_locked` | Tạm khoá đăng nhập | system | Đạt ngưỡng sai mật khẩu ở `auth.login` hoặc `auth.changePassword` (D-SD02-004 (¶3.2), D-SD02-006 (¶3.4)) | `employee` | `{trigger: login\|change_password, locked_until}` |
| `auth.accept_invite` | Kích hoạt tài khoản | employee | `auth.acceptInvite` | `employee` | `{}` |
| `auth.password_reset` | Đặt lại mật khẩu qua email | employee | `auth.resetPassword` | `employee` | `{}` |
| `auth.password_change` | Đổi mật khẩu | employee | `auth.changePassword` | `employee` | `{}` |

**2. Nhân viên, role, Tổ chức (`/identity`, nhóm `identity/*`)**

| `action_type` | Nhãn | Actor | Endpoint | entity | `detail` |
|---|---|---|---|---|---|
| `employee.create` | Tạo Nhân viên | employee | `identity.createEmployee` | `employee` (mới) | `{email, organization_id, role_ids}` |
| `employee.update` | Sửa thông tin Nhân viên | employee | `identity.updateEmployee` | `employee` | `{changes}` |
| `employee.disable` | Khoá tài khoản | employee | `identity.disableEmployee` | `employee` | `{from_status, to_status}` |
| `employee.enable` | Mở khoá tài khoản | employee | `identity.enableEmployee` | `employee` | `{from_status, to_status}` |
| `employee.clear_login_lock` | Gỡ tạm khoá đăng nhập | employee | `identity.clearEmployeeLoginLock` | `employee` | `{locked_until}` (giá trị trước khi gỡ) |
| `employee.resend_invite` | Gửi lại lời mời | employee | `identity.resendEmployeeInvite` | `employee` | `{}` |
| `employee.assign_role` | Gán role | employee | `identity.addEmployeeRole` | `employee` | `{role_id, role_name, scope_type, scope_id}` |
| `employee.remove_role` | Gỡ role | employee | `identity.removeEmployeeRole` | `employee` | như trên |
| `organization.create` | Tạo Tổ chức | employee | `identity.createOrganization` | `organization` (mới) | `{name}` |
| `organization.update` | Sửa Tổ chức | employee | `identity.updateOrganization` | `organization` | `{changes}` |

**3. Đề tài nghiên cứu, Tư liệu gốc (`/knowledge`)**

| `action_type` | Nhãn | Actor | Endpoint / nguồn | entity | `detail` |
|---|---|---|---|---|---|
| `research_topic.create` | Tạo Đề tài nghiên cứu | employee | `knowledge.createResearchTopic` (gồm cả tự sinh 3 role theo phạm vi — không ghi riêng) | `research_topic` (mới) | `{name}` |
| `research_topic.delete` | Xoá Đề tài nghiên cứu | employee | `knowledge.deleteResearchTopic` | `research_topic` | `{name, removed_source_ids}` |
| `research_topic.add_source` | Gán Tư liệu gốc vào đề tài | employee | `knowledge.addResearchTopicSource` | `research_topic` | `{source_id}` |
| `research_topic.remove_source` | Gỡ Tư liệu gốc khỏi đề tài | employee | `knowledge.removeResearchTopicSource` | `research_topic` | `{source_id}` |
| `research_topic.mark_ready` | Đánh dấu tư liệu sẵn sàng | employee | `knowledge.markResearchTopicReady` | `research_topic` | `{from_status, to_status}` |
| `research_topic.set_chair` | Gán/đổi Chủ nhiệm đề tài | employee | `knowledge.setResearchTopicChair` | `research_topic` | `{employee_id, previous_employee_id}` |
| `research_topic.assign_researcher` | Gán vai trò Nghiên cứu | employee | `knowledge.addResearchTopicResearcher` | `research_topic` | `{employee_id}` |
| `research_topic.remove_researcher` | Gỡ vai trò Nghiên cứu | employee | `knowledge.removeResearchTopicResearcher` | `research_topic` | `{employee_id}` |
| `research_topic.assign_reviewer` | Gán vai trò Xét duyệt | employee | `knowledge.addResearchTopicReviewer` | `research_topic` | `{employee_id}` |
| `research_topic.remove_reviewer` | Gỡ vai trò Xét duyệt | employee | `knowledge.removeResearchTopicReviewer` | `research_topic` | `{employee_id}` |
| `source.create` | Tạo Tư liệu gốc | employee | `knowledge.createSource` | `source` (mới) | `{name, type, storage_prefix}` |
| `source.sync` | Đồng bộ Tư liệu gốc | employee | `knowledge.syncSource` — luôn ghi, kể cả khi không có thay đổi | `source` | `{added_count, missing_count, restored_count, unchanged_count, added_file_ids, missing_file_ids, restored_file_ids}` |
| `source.sync` | Đồng bộ Tư liệu gốc | system | Job `ingestion.sync_source` (webhook) — **chỉ ghi khi có file mới/mất/xuất hiện lại** | `source` | như trên + `job_id` |

**4. Hạng mục tri thức (`/knowledge`, `/gate`)**

| `action_type` | Nhãn | Actor | Endpoint / nguồn | entity | `detail` |
|---|---|---|---|---|---|
| `knowledge_object.create` | Tạo Hạng mục tri thức | employee | `knowledge.createKnowledgeObject` | `knowledge_object` (mới) | `{research_topic_id, title}` |
| `knowledge_object.delete` | Xoá Hạng mục tri thức | employee | `knowledge.deleteKnowledgeObject` | `knowledge_object` | `{research_topic_id, title}` |
| `knowledge_object.file_add` | Thêm file Nội dung | employee | `knowledge.createKnowledgeObjectFile` | `knowledge_object` | `{file_id, file_name, file_type}` |
| `knowledge_object.file_remove` | Gỡ file Nội dung | employee | `knowledge.deleteKnowledgeObjectFile` | `knowledge_object` | `{file_id, file_name}` |
| `knowledge_object.claim_create` | Thêm Phát biểu | employee | `knowledge.createClaim` | `knowledge_object` | `{claim_id}` |
| `knowledge_object.claim_update` | Sửa Phát biểu | employee | `knowledge.updateClaim` | `knowledge_object` | `{claim_id, fields}` |
| `knowledge_object.claim_delete` | Xoá Phát biểu | employee | `knowledge.deleteClaim` | `knowledge_object` | `{claim_id, removed_reference_ids}` |
| `knowledge_object.reference_add` | Thêm Tham chiếu | employee | `knowledge.createClaimReference` | `knowledge_object` | `{claim_id, reference_id, source_file_id}` |
| `knowledge_object.reference_remove` | Gỡ Tham chiếu | employee | `knowledge.deleteClaimReference` | `knowledge_object` | `{claim_id, reference_id}` |
| `knowledge_object.submit_for_review` | Gửi xét duyệt | employee | `knowledge.submitKnowledgeObjectForReview` | `knowledge_object` | `{from_status, to_status, ai_verification_triggered}` |
| `knowledge_object.trigger_ai_verification` | Kích hoạt AI Verification | employee | `knowledge.triggerAiVerification` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.ai_verification_complete` | Hoàn tất AI Verification | system | Job `verification.run`, khi ghi kết quả + chuyển trạng thái (D-SD03-018 (¶4.3)) | `knowledge_object` | `{from_status, to_status, job_id, dat_count, khong_dat_count}` |
| `knowledge_object.assignment_claim` | Nhận xử lý | employee | `knowledge.claimKnowledgeObject` | `knowledge_object` | `{from_status, to_status}` (bằng nhau nếu chỉ gán người) |
| `knowledge_object.assignment_release` | Nhả xử lý | employee | `knowledge.releaseKnowledgeObject` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.assignment_force_release` | Cưỡng chế nhả xử lý | employee | `knowledge.forceReleaseKnowledgeObject` | `knowledge_object` | `{from_status, to_status, previous_assignee_id}` |
| `knowledge_object.reference_review` | Chuyên gia đánh giá Tham chiếu | employee | `knowledge.reviewClaimReference` | `knowledge_object` | `{claim_id, reference_id, verdict}` |
| `knowledge_object.content_review` | Chuyên gia đánh giá vị trí Nội dung | employee | `knowledge.reviewClaimContent` | `knowledge_object` | `{claim_id, verdict}` |
| `knowledge_object.reject` | Không đạt xét duyệt | employee | `knowledge.rejectKnowledgeObject` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.resume_research` | Nghiên cứu lại | employee | `knowledge.resumeKnowledgeObjectResearch` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.approve` | Đạt xét duyệt | employee | `knowledge.approveKnowledgeObject` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.publish` | Xuất bản Hạng mục tri thức | employee | `knowledge.publishKnowledgeObject` | `knowledge_object` | `{from_status, to_status, version_id}` |
| `knowledge_object.skip_publish` | Không xuất bản Hạng mục tri thức | employee | `knowledge.skipKnowledgeObjectPublish` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.reopen` | Mở lại Hạng mục tri thức | employee | `knowledge.reopenKnowledgeObject` | `knowledge_object` | `{from_status, to_status}` |
| `knowledge_object.set_used_version` | Chọn phiên bản đang dùng | employee | `knowledge.setKnowledgeObjectUsedVersion` | `knowledge_object` | `{old_version_id, new_version_id}` |

**5. Mục từ, Cương vực (`/encyclopedia`)**

| `action_type` | Nhãn | Actor | Endpoint | entity | `detail` |
|---|---|---|---|---|---|
| `entry.create` | Tạo Mục từ | employee | `encyclopedia.createEntry` | `entry` (mới) | `{title, knowledge_object_ids}` |
| `entry.content_update` | Sửa nội dung Mục từ | employee | `encyclopedia.updateEntryContent` | `entry` | `{fields: ["content_blocks"]}` |
| `entry.knowledge_object_add` | Thêm ánh xạ Hạng mục tri thức | employee | `encyclopedia.addEntryKnowledgeObject` | `entry` | `{knowledge_object_id}` |
| `entry.knowledge_object_remove` | Gỡ ánh xạ Hạng mục tri thức | employee | `encyclopedia.removeEntryKnowledgeObject` | `entry` | `{knowledge_object_id}` |
| `entry.knowledge_object_mark_synced` | Đánh dấu đã đồng bộ Hạng mục tri thức | employee | `encyclopedia.markEntryKnowledgeObjectSynced` | `entry` | `{knowledge_object_id, used_version_id}` |
| `entry.file_add` | Thêm file đính kèm | employee | `encyclopedia.createEntryFile` | `entry` | `{file_id, file_name, file_type}` |
| `entry.file_remove` | Gỡ file đính kèm | employee | `encyclopedia.deleteEntryFile` | `entry` | `{file_id, file_name}` |
| `entry.cultural_domain_add` | Gán Cương vực | employee | `encyclopedia.addEntryCulturalDomain` | `entry` | `{cultural_domain_id}` |
| `entry.cultural_domain_remove` | Gỡ Cương vực | employee | `encyclopedia.removeEntryCulturalDomain` | `entry` | `{cultural_domain_id}` |
| `entry.submit_for_review` | Gửi xét duyệt Mục từ | employee | `encyclopedia.submitEntryForReview` | `entry` | `{from_status, to_status}` |
| `entry.assignment_claim` | Nhận xử lý Mục từ | employee | `encyclopedia.claimEntry` | `entry` | `{from_status, to_status}` |
| `entry.assignment_release` | Nhả xử lý Mục từ | employee | `encyclopedia.releaseEntry` | `entry` | `{from_status, to_status}` |
| `entry.assignment_force_release` | Cưỡng chế nhả xử lý Mục từ | employee | `encyclopedia.forceReleaseEntry` | `entry` | `{from_status, to_status, previous_assignee_id}` |
| `entry.reject` | Mục từ không đạt xét duyệt | employee | `encyclopedia.rejectEntry` | `entry` | `{from_status, to_status}` (không chép `note`) |
| `entry.resume_editing` | Soạn thảo lại Mục từ | employee | `encyclopedia.resumeEntryEditing` | `entry` | `{from_status, to_status}` |
| `entry.approve` | Mục từ đạt xét duyệt | employee | `encyclopedia.approveEntry` | `entry` | `{from_status, to_status}` |
| `entry.publish` | Xuất bản Mục từ | employee | `encyclopedia.publishEntry` | `entry` | `{from_status, to_status, version_id}` |
| `entry.skip_publish` | Không xuất bản Mục từ | employee | `encyclopedia.skipEntryPublish` | `entry` | `{from_status, to_status}` |
| `entry.reopen` | Mở lại Mục từ | employee | `encyclopedia.reopenEntry` | `entry` | `{from_status, to_status}` |
| `entry.set_public_version` | Chọn phiên bản công khai | employee | `encyclopedia.setEntryPublicVersion` | `entry` | `{old_version_id, new_version_id}` |
| `entry.content_generation_request` | Yêu cầu sinh nội dung bằng AI | employee | `encyclopedia.generateEntryContent` | `entry` | `{job_id}` |
| `entry.content_generation_complete` | Hoàn tất sinh nội dung bằng AI | system | Job `encyclopedia.generate_content`, khi ghi kết quả (D-SD04-019 (¶3.5)) | `entry` | `{job_id, block_count, file_ids, synced: [{knowledge_object_id, used_version_id}]}` |
| `entry.content_generation_discard` | Bỏ kết quả sinh nội dung | system | Job `encyclopedia.generate_content` (D-SD04-019 (¶3.5)) | `entry` | `{job_id, reason}` |
| `cultural_domain.create` | Tạo Cương vực | employee | `encyclopedia.createCulturalDomain` | `cultural_domain` (mới) | `{name, code}` |
| `cultural_domain.update` | Sửa Cương vực | employee | `encyclopedia.updateCulturalDomain` | `cultural_domain` | `{changes}` |
| `cultural_domain.delete` | Xoá Cương vực | employee | `encyclopedia.deleteCulturalDomain` | `cultural_domain` | `{name, code}` |

**6. AI Văn Minh Việt, vận hành, cấu hình (`/assistant`, `/shared`)**

| `action_type` | Nhãn | Actor | Endpoint | entity | `detail` |
|---|---|---|---|---|---|
| `assistant.reindex_entry` | Yêu cầu lập chỉ mục lại Mục từ | employee | `assistant.reindexEntry` | `entry` | `{job_id}` |
| `job.retry` | Chạy lại job nền | employee | `shared.retryJob` | `job` (`entity_id = NULL`) | `{job_id, job_type, previous_status, related_entity}` |
| `job.cancel` | Huỷ job nền | employee | `shared.cancelJob` | `job` (`entity_id = NULL`) | như trên |
| `system_setting.update` | Sửa cấu hình hệ thống | employee | `shared.updateSettings` — một dòng cho mỗi key đổi | `system_setting` (`entity_id = NULL`) | `{key, old_value, new_value}` |
| `system_setting.reset` | Khôi phục cấu hình mặc định | employee | `shared.resetSetting` | `system_setting` (`entity_id = NULL`) | như trên |

**Không ghi audit** (có chủ đích):
- Mọi request đọc (`GET`), kể cả xin URL tải file (`download-url`).
- `auth.refresh` — `POST /auth/refresh`, `auth.forgotPassword` — `POST /auth/forgot-password` (không đổi dữ liệu nghiệp vụ; tránh log rác khi bị gọi dồn dập).
- Bước 1 upload (`…/files/upload-url`) — chưa tạo dòng DB; audit ghi ở bước xác nhận `…/files`.
- `shared.previewEmailTemplate` — `POST /shared/settings/email-templates/{template}/preview` và `/test`.
- `assistant.chat` — `POST /assistant/chat` — đã có `assistant_conversation`/`assistant_query_log` (`05` ¶2) làm nhật ký riêng.
- `internal.receiveSourceWebhook` — `POST /internal/ingestion/source-webhook` (chỉ nhận tín hiệu) — kết quả đồng bộ ghi bằng `source.sync` actor `system`.
- `knowledge.triggerAiVerification` khi lệnh gộp vào job `verification.run` đang chờ/đang chạy (`merged_into_running_job = true`, D-SD03-012 (¶3.3) bước (3), D-SD03-024 (¶5.4)) — không tạo job, không đổi trạng thái.
- Job nền tạo dữ liệu dẫn xuất/kỹ thuật hoặc dọn dữ liệu theo thời hạn lưu: `knowledge.extract_file_metadata`, `knowledge.generate_transcript`, `assistant.reindex_entry` (lúc chạy), `assistant.refresh_domain_tags`, `assistant.query_log_cleanup`, `search.rebuild_fulltext`, `shared.usage_snapshot`, `shared.job_cleanup`, `shared.audit_log_cleanup`, `shared.apply_storage_lifecycle` — theo dõi qua màn hình job nền (D-SD01-004 (¶4)).
- Tạo tài khoản Quản trị hệ thống đầu tiên qua seed (D-SD02-002 (¶3.0)), tự sinh/xoá role theo phạm vi (nằm trong `research_topic.create`/`research_topic.delete`).
- Lần đăng nhập sai chưa tới ngưỡng tạm khoá, lần nhập sai mật khẩu hiện tại khi đổi mật khẩu.

- **Ghi đồng bộ, cùng transaction DB** với thao tác nghiệp vụ đang ghi nhận — không qua message queue/container riêng: audit log cần đảm bảo tính atomic với thao tác nó ghi lại (tách ra ghi bất đồng bộ dễ phát sinh "dual-write" — nghiệp vụ commit thành công nhưng bản ghi audit bị mất nếu bước publish message thất bại giữa chừng), và tải hệ thống (D-SD01-008 (¶8) — vài chục đến ~200 Nhân viên đồng thời) không đủ lớn để cần tách riêng thêm hạ tầng. Hàm `shared.RecordAudit`/`shared.RecordUsage` nhận transaction hiện tại của package gọi làm tham số (không tự mở transaction riêng), để đảm bảo insert này thật sự nằm cùng transaction với thao tác nghiệp vụ.
- Riêng phần usage phát sinh từ job nền có sẵn (AI Verification, sinh embedding — D-SD01-004 (¶4)) thì tự nhiên đã bất đồng bộ qua `/cmd/worker`, không cần thêm cơ chế nào khác.
- **Thiết kế append-only** cho cả 2 bảng — chỉ INSERT dòng mới, không UPDATE dòng đã có (kể cả không dùng một dòng đếm/tổng dùng chung cho mỗi Tổ chức) — để nhiều package ghi đồng thời vào cùng bảng không tranh chấp row lock với nhau: Postgres (MVCC) không khoá chặn giữa các INSERT độc lập của các transaction khác nhau, nên giữ nguyên tắc "chỉ insert" là đủ để tránh phát sinh lock contention giữa các package cùng gọi vào `/shared`.
- `usage_event` chưa cố định trước danh sách loại sự kiện/đơn vị tính — gồm `organization_id`, loại sự kiện dạng chuỗi mở (ví dụ `ai_verification_run`, `assistant_chat_message`, `storage_snapshot`...), số lượng, thời điểm, tham chiếu bản ghi liên quan (tuỳ chọn) — vì logic tính chi phí cụ thể (cách tính, đơn giá, xuất hoá đơn) chưa đặc tả (R-ID-015 (§2.1.4.6) đặc tả gốc), chỉ cần có sẵn chỗ gắn dữ liệu sử dụng từ đầu. Phân biệt 2 kiểu ghi: **đếm sự kiện** (ghi ngay lúc xảy ra, ví dụ một lượt AI Verification, một tin nhắn chat) và **đo trạng thái tại một thời điểm** (snapshot định kỳ qua job nền, ví dụ dung lượng storage đang chiếm theo Tổ chức — lấy mẫu định kỳ thay vì ghi mỗi lần đổi, tránh phình bảng vô ích).

**Cả 3 lớp giao diện (Admin nội bộ, Cổng Tổ chức khác — D-SD01-001 (¶1); và Web công khai, R-PUB-001 (§2.6) đặc tả gốc) đều gọi vào cùng một Go monolith này**, mount thành 3 nhóm route riêng dưới `/api/v1/`, được reverse proxy (D-SD01-001 (¶1)) định tuyến theo domain/path tới đúng frontend:

- `/api/v1/admin/...` — cho Admin nội bộ: mount đầy đủ mọi package, gồm cả nhóm quản lý người dùng/phân quyền/Tổ chức (`identity`) và nạp liệu Hán Nôm (`ingestion`); yêu cầu JWT Nhân viên thuộc Tổ chức Văn Minh Việt (D-SD01-007 (¶7)).
- `/api/v1/partner/...` — cho Cổng Nhân viên Tổ chức khác: chỉ mount route Nghiên cứu/Xét duyệt trong `knowledge` và `gate`, **cùng nhóm route quản lý nhân sự đề tài dành cho vai trò Chủ nhiệm đề tài** (`research-topics/{id}/members`, `researchers`, `reviewers` — R-PTN-003 (§2.7.2), R-PTN-008 (§2.7.3.4) đặc tả gốc; chi tiết D-SD03-021 (¶5.1)), tất cả giới hạn theo Đề tài nghiên cứu được gán (R-PTN-003 (§2.7.2)–R-PTN-004 (§2.7.3) đặc tả gốc); **không mount** bất kỳ route nào của `identity`, `ingestion`, hay `encyclopedia` — đây chính là cách thực thi ranh giới R-PTN-010 (§2.7.4) đặc tả gốc ("không có chức năng quản lý người dùng/Tổ chức dù giữ vai trò gì") ở tầng route/API, không dựa vào ẩn UI phía frontend; yêu cầu JWT Nhân viên thuộc Tổ chức khác.

  ⚠ **Lưu ý không mâu thuẫn với R-PTN-010 (§2.7.4)**: việc Chủ nhiệm đề tài gán/gỡ vai trò Nghiên cứu/Xét duyệt **trong đúng đề tài mình phụ trách** đi qua route của `/knowledge`, không phải `identity/*` — R-PTN-010 (§2.7.4) cấm chức năng quản lý người dùng/Tổ chức (tạo/sửa Nhân viên, tạo/sửa Tổ chức, gán role tuỳ ý toàn hệ thống), không cấm việc phân công nhân sự trong phạm vi một Đề tài. Việc gán/đổi chính vai trò **Chủ nhiệm đề tài** vẫn chỉ Quản trị hệ thống làm được, endpoint `set-chair` chỉ mount ở `admin` (R-KB-073 (§2.2.5.5), R-PTN-003 (§2.7.2)).

- `/api/v1/public/...` — cho Web công khai: chỉ mount route đọc Mục từ theo **phiên bản đang công khai** (`encyclopedia`, read-only — con trỏ R-ENC-010 (§2.3.2.4.1)) và route chat AI Văn Minh Việt (`assistant`); không yêu cầu xác thực (R-GEN-007 (§1.2.2)/R-PUB-002 (§2.6.1) đặc tả gốc).

**Ngoại lệ trong `/identity`**: bản thân `/identity` (module 02) tách thành 2 nhóm route con theo đúng ranh giới trên — nhóm `identity/*` (quản lý Nhân viên/Tổ chức/Role, R-ID-002 (§2.1.1)–R-ID-009 (§2.1.4)) chỉ mount ở `/api/v1/admin/identity/...`, đúng ranh giới R-PTN-010 (§2.7.4); nhưng nhóm `auth/*` (đăng nhập, làm mới phiên, đăng xuất, quên/đặt lại mật khẩu, nhận lời mời — R-ID-016 (§2.1.5); ⚠ đổi mật khẩu khi đang đăng nhập — D-SD02-006 (¶3.4)) mount ở **cả hai** `/api/v1/admin/auth/...` và `/api/v1/partner/auth/...`, vì Nhân viên Tổ chức khác cũng cần tự xác thực (R-ID-023 (§2.1.5.6) đặc tả gốc: cơ chế email + mật khẩu áp dụng cho mọi Nhân viên, kể cả Tổ chức khác) dù không được vào các route quản lý người dùng/Tổ chức. Chi tiết endpoint `auth`/`identity` ở `02` ¶5.

Danh sách endpoint cụ thể trong từng nhóm route sẽ chốt ở phần "Thiết kế API" của từng tài liệu module (02–05) — mục này chỉ chốt ranh giới mount giữa 3 giao diện, cũng là cách thực thi phân quyền ở **cả 2 tầng** route/API và service/role (D-SD01-007 (¶7)) theo đúng yêu cầu R-PTN-010 (§2.7.4) đặc tả gốc.

**Lưu ý: `/api/v1/...` chỉ là API trả JSON, không phải nơi phục vụ trang HTML.** Go monolith không tự phục vụ HTML cho bất kỳ giao diện nào — phần phục vụ HTML nằm ở 3 tiến trình/container hoàn toàn tách biệt, đóng gói Docker riêng (D-SD01-001 (¶1)):

- Web công khai (Next.js SSR/SSG): chạy một tiến trình Node.js riêng, vì SSR cần render theo từng request.
- Admin nội bộ và Cổng Nhân viên Tổ chức khác (Quasar SPA): build ra file tĩnh (HTML/CSS/JS) một lần lúc build, phục vụ qua static file server nhẹ (ví dụ nginx) — không cần chạy Node lúc request.

Sau khi trình duyệt tải xong trang từ 1 trong 3 tiến trình trên, JavaScript trong trang mới gọi AJAX/fetch sang `/api/v1/{admin,partner,public}/...` trên Go monolith để lấy dữ liệu. Reverse proxy (D-SD01-001 (¶1)) định tuyến 2 loại traffic này — phục vụ HTML (tới container web tương ứng) và gọi API JSON (tới Go monolith) — theo domain/path.

**Dựng nội dung Mục từ (JSON block, R-ENC-007 (§2.3.2.3.1) đặc tả gốc)**: vai trò Biên tập soạn nội dung qua trình soạn thảo TipTap (D-SD01-001 (¶1)) ngay trong Admin nội bộ, lưu thành JSON có cấu trúc block (danh sách khối có thứ tự, kể cả khối nhúng file đính kèm đúng vị trí — R-ENC-008 (§2.3.2.3.2)) qua `/encyclopedia`. Web công khai (Next.js) lấy JSON này qua `/api/v1/public/...` và tự render bằng component React ánh xạ theo từng loại khối (đoạn văn, chú thích, nhúng ảnh/audio/phim...) — không cần bước dựng phía server, không phụ thuộc XSLT.

## 3. [D-SD01-003] Quy ước API chung — áp dụng cho mọi module

- REST/JSON, versioned: `/api/v1/...`, mount thành 3 nhóm route theo giao diện (`admin`, `partner`, `public`) — xem ranh giới mount ở D-SD01-002 (¶2).
- Chuẩn hoá response lỗi: mã lỗi + message + `trace_id`.
- Phân trang cursor-based cho mọi danh sách lớn (Bách khoa, tư liệu gốc...).
- Mọi thao tác ghi có **audit log** (ai, khi nào, đổi gì) — bắt buộc cho luồng xét duyệt (R-NFR-004 (§3.1.2) đặc tả gốc); bảng dùng chung `audit_log`, sở hữu bởi `/shared`, ghi đồng bộ cùng transaction với thao tác nghiệp vụ — xem D-SD01-002 (¶2).
- Idempotency key cho job nặng (xử lý dữ liệu nạp vào, embedding) để tránh chạy trùng.
- **Service tự phát triển nhưng tách deploy riêng khỏi Go monolith (ví dụ AI Gateway) giữ đúng kiểu đồng bộ/bất đồng bộ của tầng gọi nó, không tự thêm một tầng async/job-polling riêng bên trong interface của chính nó**: nói rộng hơn, giữa các service/component phụ thuộc nhau trong hệ thống, không chồng nhiều tầng bất đồng bộ lên nhau cho cùng một lệnh gọi — nếu lệnh gọi đó đã nằm trong một ngữ cảnh bất đồng bộ sẵn có ở tầng trên (ví dụ job nền qua hàng đợi river, D-SD01-004 (¶4) — đã có sẵn theo dõi trạng thái + retry/dead-letter), thì interface của service được gọi ở tầng dưới nên giữ dạng đồng bộ (request-response bình thường, dù xử lý lâu) thay vì tự thêm một tầng async/job-polling riêng của chính nó — tránh 2 tầng bất đồng bộ lồng nhau, trùng lặp cơ chế theo dõi trạng thái, khó debug. Ngược lại, nếu lệnh gọi phục vụ trực tiếp một request tương tác của người dùng cần phản hồi thời gian thực, dùng streaming (SSE/chunked) ở đúng tầng đó thay vì bất đồng bộ kiểu job. Nguyên tắc áp dụng cho service do chính hệ thống tự thiết kế interface (không áp dụng cho dịch vụ bên thứ ba như SMTP/SES, MinIO/S3 — interface của họ đã cố định sẵn, không do mình quyết định). Ví dụ áp dụng cụ thể: AI Gateway (D-SD06-001 (¶1)).
- **CORS**: cả 3 web app (D-SD01-002 (¶2)) chạy trên domain/path riêng và gọi API bằng JavaScript phía trình duyệt (cross-origin) — cần cấu hình CORS policy cụ thể (origin nào được gọi nhóm route nào: `admin`, `partner`, hay `public`); chi tiết allowlist domain chốt khi triển khai thật (phụ thuộc domain production).
- **Upload file lớn cho nội dung do nền tảng tự quản lý** (ví dụ `knowledge_object_file` — file biên tập Nội dung, D-SD03-007 (¶2.7)): không proxy file qua REST/JSON như request thông thường — dùng **presigned URL** lên thẳng Object storage (D-SD01-001 (¶1)): API chỉ cấp URL có thời hạn và xác nhận/ghi metadata bản ghi sau khi client upload xong trực tiếp lên S3-compatible/MinIO. ⚠ Riêng **Tư liệu gốc** (`source`/`source_file`) **không** dùng đường này — file được nạp vào MinIO/S3 từ bên ngoài hệ thống, nền tảng chỉ đồng bộ lại qua liệt kê thư mục (xem D-SD01-005 (¶5); chi tiết D-SD03-017 (¶4.2), D-SD03-020 (¶4.5)).
- ⚠ **Đề xuất bổ sung — quy ước cụ thể 2 bước cho upload qua presigned URL** (hoàn thiện kỹ thuật cho gạch đầu dòng trên, áp dụng cho `knowledge_object_file` module 03 và `entry_file` module 04): (1) client gọi `POST .../upload-url` (body tối thiểu `{file_type, file_name}`) → server sinh `storage_key`, ký presigned PUT URL có thời hạn ngắn (vài phút), trả `{upload_url, storage_key, expires_at}` — **chưa tạo dòng DB**; (2) client PUT thẳng file lên `upload_url`; (3) client gọi endpoint xác nhận đã có sẵn (`POST .../files`, body gồm `storage_key` vừa nhận) để tạo dòng bản ghi. **Xem/tải file đã có** dùng cơ chế ngược chiều: `GET .../{file_id}/download-url` ký presigned GET URL ngắn hạn, gọi **theo yêu cầu** (khi người dùng bấm xem/tải) — không trả sẵn URL này trong response danh sách/chi tiết, tránh URL hết hạn nằm sẵn trong dữ liệu cache. Cơ chế này áp dụng cả cho `source_file` (Tư liệu gốc) — dù không upload qua app, vẫn cần `download-url` để xem/chọn vị trí tham chiếu (D-SD03-007 (¶2.7)); chi tiết endpoint từng loại file ở `03`/`04` mục "Thiết kế API". Ngoại lệ: nhóm route `public` trả sẵn presigned GET URL (kèm `url_expires_at`) trong response cho file của phiên bản Mục từ đang công khai — chi tiết D-SD04-018 (¶5.4).
- **Streaming cho AI Văn Minh Việt**: là ngoại lệ của quy ước REST/JSON ở trên — endpoint chat trả lời dạng **SSE (Server-Sent Events)** hoặc chunked transfer để đạt yêu cầu token đầu ≤3 giây (R-NFR-011 (§3.2.2), D-SD01-008 (¶8)), không phải JSON trả về một lần như các endpoint khác.
- **Hợp đồng OpenAPI**: mỗi nhóm route `admin`, `partner`, `public` có một file hợp đồng OpenAPI 3 riêng. Đây là bản máy đọc được của phần "Thiết kế API" trong các tài liệu module. Hành vi do tài liệu thiết kế quyết định; hợp đồng mâu thuẫn với thiết kế thì thiết kế thắng.
  - Mỗi operation mang đúng operationId của endpoint trong tài liệu thiết kế (`common/requirements-design-sync.md` mục 2.5). Endpoint mount ở nhiều nhóm route có mặt trong từng file hợp đồng tương ứng, với cùng operationId.
  - Hợp đồng phải khớp code backend cả về route (method, path, operationId, nhóm route mount) lẫn schema request/response. Sự khớp này được kiểm tra tự động trong CI; lệch thì CI báo lỗi. Cách bảo đảm do team Code chọn và ghi trong tài liệu của repo: sinh hợp đồng từ code, sinh code từ hợp đồng, hoặc viết tay hợp đồng kèm kiểm tra route và kiểm response theo hợp đồng trong test tích hợp.
  - admin-web, partner-web, public-web sinh API client (types và hàm gọi) từ file hợp đồng của nhóm route mình dùng, không viết tay lời gọi API. Hợp đồng thay đổi thì sinh lại client trước khi làm tiếp phần giao diện phụ thuộc.
  - Endpoint chat của AI Văn Minh Việt khai báo response với content type `text/event-stream`. Định dạng sự kiện theo D-SD05-012 (¶5.1).
  - Webhook nội bộ (D-SD03-025 (¶5.5)) không thuộc 3 file hợp đồng trên. AI Gateway công bố OpenAPI riêng của service, với operationId theo đúng `06`.

## 4. [D-SD01-004] Xử lý nền (background jobs)

Các tác vụ sau chạy **bất đồng bộ** qua hàng đợi, có trạng thái theo dõi được trên Admin (đang chờ / đang chạy / lỗi / xong), không được chặn API đồng bộ:

- Trích metadata file khi nhận tư liệu (số trang văn bản, kích thước ảnh, độ dài audio/video) — phục vụ AI Verification kiểm tra vị trí tham chiếu hợp lệ (R-KB-081 (§2.2.6.6.1) đặc tả gốc).
- Sinh embedding cho nội dung đủ điều kiện (phục vụ AI Văn Minh Việt), gắn theo đúng `version_id` của Mục từ — xem D-SD01-006 (¶6).
- **Re-index embedding khi phiên bản đang công khai của Mục từ đổi** (⚠ đề xuất bổ sung — hệ quả kỹ thuật của con trỏ phiên bản đang công khai, R-ENC-010 (§2.3.2.4.1), chưa nêu trong đặc tả gốc): kích hoạt mỗi khi vai trò Xuất bản Mục từ đổi con trỏ (kể cả quay về phiên bản cũ hơn) — vô hiệu embedding của phiên bản không còn công khai khỏi tập truy hồi RAG, sinh embedding cho phiên bản mới nếu chưa có sẵn.
- AI Verification (Trợ lý Tư liệu gốc — R-KB-080 (§2.2.6.6) đặc tả gốc).
- Tái lập chỉ mục tìm kiếm toàn văn.
- Snapshot định kỳ usage theo Tổ chức (ví dụ dung lượng storage đang chiếm) ghi vào `usage_event` — D-SD01-002 (¶2).
- **Đồng bộ thư mục Tư liệu gốc trong MinIO/S3** (⚠ bổ sung — xem D-SD01-005 (¶5)): `SyncSourceFiles`, kích hoạt qua webhook đã debounce/coalesce theo `source_id` hoặc thủ công.

**Tên loại job & đối tượng liên quan** (⚠ Đề xuất bổ sung — đặt tên thống nhất để lọc/hiển thị ở API theo dõi bên dưới):

| Loại job (`type`) | Package xử lý | Payload | `related_entity` |
|---|---|---|---|
| `ingestion.sync_source` | `/ingestion` → `/knowledge.SyncSourceFiles` | `{source_id}` hoặc `{source_id, follows_job_id}` — `follows_job_id` (bigint) là `id` của job `ingestion.sync_source` đang chạy mà job này nối tiếp (D-SD03-017 (¶4.2)) | `source` |
| `knowledge.extract_file_metadata` | `/knowledge` | `{file_kind, file_id, source_id \| knowledge_object_id}` — `file_kind ∈ {source_file, knowledge_object_file}` | `source` hoặc `knowledge_object`, theo `file_kind` |
| `knowledge.generate_transcript` | `/knowledge` | như trên | như trên |
| `verification.run` | `/verification` | `{knowledge_object_id}` | `knowledge_object` |
| `encyclopedia.generate_content` | `/encyclopedia` | `{entry_id, requested_by}` | `entry` |
| `assistant.reindex_entry` | `/assistant` | `{entry_id}` | `entry` |
| `assistant.refresh_domain_tags` | `/assistant` | `{entry_id}` | `entry` |
| `search.rebuild_fulltext` | *(package sở hữu chỉ mục)* | `{}` hoặc phạm vi cần dựng lại | `null` |
| `shared.usage_snapshot` | `/shared` | `{}` | `null` |
| `shared.job_cleanup` | `/shared` (periodic, mỗi giờ) | `{}` | `null` |
| `shared.audit_log_cleanup` | `/shared` (periodic, mỗi ngày) | `{}` | `null` |
| `assistant.query_log_cleanup` | `/assistant` (periodic, mỗi ngày) | `{}` | `null` |
| `shared.apply_storage_lifecycle` | `/shared` | `{}` | `null` |

Mỗi loại job tự khai báo (trong code, cùng chỗ đăng ký worker) cách suy ra `related_entity` từ payload — `/shared` chỉ gọi hàm suy ra này, không tự biết ngữ nghĩa từng loại job.

**Theo dõi job nền trên Admin** (⚠ Đề xuất bổ sung — hiện thực yêu cầu "trạng thái theo dõi được trên Admin" ở đầu mục này):

- Package `/shared` sở hữu phần đọc/điều khiển job: truy vấn bảng job của river (`river_job`, do thư viện river tự tạo/migrate) bằng SQL. Các package nghiệp vụ chỉ enqueue qua `InsertTx`, không đọc bảng này.
- Ánh xạ trạng thái gốc của river sang trạng thái hiển thị:

| Trạng thái river | `status` hiển thị | `exhausted` |
|---|---|---|
| `scheduled`, `available`, `pending` | `pending` | `false` |
| `running` | `running` | `false` |
| `retryable` (lỗi, còn lượt thử lại) | `failed` | `false` |
| `discarded` (hết lượt thử lại) | `failed` | `true` |
| `completed` | `completed` | `false` |
| `cancelled` | `cancelled` | `false` |

API — chỉ mount ở nhóm `admin`, yêu cầu role `quan_tri_he_thong` (tầng service, D-SD01-007 (¶7)):

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/shared/jobs` | `shared.listJobs` | Danh sách job — filter `type`, `status`, `from`, `to`; cursor pagination (D-SD01-003 (¶3)) |
| GET | `/shared/jobs/{id}` | `shared.getJob` | Chi tiết: payload, lỗi lần gần nhất, lịch sử các lần thử (`errors` của river) |
| POST | `/shared/jobs/{id}/retry` | `shared.retryJob` | Chạy lại ngay — chỉ hợp lệ khi `status = failed` (cả `exhausted` true lẫn false) |
| POST | `/shared/jobs/{id}/cancel` | `shared.cancelJob` | Huỷ — chỉ hợp lệ khi `status = pending`; không huỷ job đang chạy |

Mỗi dòng trả: `id` (bigint — định danh job của river, không phải UUID), `type`, `status`, `exhausted`, `attempts`, `max_attempts`, `created_at`, `started_at`, `finished_at`, `last_error`, `payload`, `related_entity: {entity_type, entity_id} | null`.

- `retry`/`cancel` là thao tác ghi nên có audit log theo quy ước chung (D-SD01-003 (¶3)), ghi **cùng transaction** với `JobRetryTx`/`JobCancelTx`: `action_type` = `job.retry`/`job.cancel`, `entity_type = job`, `entity_id = NULL` (id job là bigint), `detail = {job_id, job_type, previous_status, related_entity}`.
- Hệ quả khi huỷ một số loại job — UI hiển thị cảnh báo xác nhận trước khi huỷ, không cần cơ chế khôi phục mới:
  - `verification.run`: Hạng mục tri thức ở lại `dang_xet_duyet_ai` — khôi phục bằng cách kích hoạt lại AI Verification (D-SD03-012 (¶3.3) bước (3)).
  - `assistant.reindex_entry`: chỉ mục RAG của Mục từ không được cập nhật — khôi phục bằng `assistant.reindexEntry` — `POST /assistant/reindex/{entry_id}`.
  - `ingestion.sync_source`: khôi phục bằng nút "Đồng bộ lại" (D-SD03-020 (¶4.5)).
- Job đã xong/đã huỷ/hết lượt thử lại được xoá sau một thời gian giữ lại do Quản trị hệ thống cấu hình (`operations.job_retention_*`), bằng periodic job `shared.job_cleanup` thay cho bộ dọn dẹp mặc định của river. Màn hình theo dõi chỉ xem được lịch sử trong khoảng này. Audit log (`shared.audit_log_cleanup`) và nhật ký hỏi đáp AI (`assistant.query_log_cleanup`) được dọn theo thời hạn lưu cấu hình tương ứng — D-SD07-009 (¶4.3).

## 5. [D-SD01-005] Ranh giới tiếp nhận Tư liệu gốc (source) — cơ chế nạp đã chốt: đồng bộ thư mục MinIO/S3

Nền tảng dùng mô hình **đồng bộ thư mục MinIO/S3**, áp dụng chung cho mọi nguồn tư liệu — không riêng tư liệu Hán Nôm.

**Việc số hoá/OCR/phiên âm/dịch Hán Nôm (R-GEN-003 (§1.1.1) đặc tả gốc — hệ thống thượng nguồn có sẵn), cũng như việc thu thập các loại tư liệu khác (sách, hiện vật, điền dã, phỏng vấn nghệ nhân — R-KB-020 (§2.2.2.3)), đều nằm ngoài phạm vi build của nền tảng này.** Nền tảng **không nhận file/payload qua API/webhook** — việc nạp file vật lý vào MinIO/S3 nằm hoàn toàn bên ngoài hệ thống, dù nguồn là hệ thống OCR thượng nguồn tự ghi vào bucket, hay Nhân viên Nhập liệu copy file thủ công. Nền tảng chỉ quản lý metadata trỏ tới thư mục và tự đồng bộ lại nội dung:

- Mỗi `source` giữ một `storage_prefix` — đường dẫn thư mục gốc trong MinIO/S3. Ai/hệ thống nào ghi file vào thư mục đó là việc bên ngoài, nền tảng không cần biết.
- **Cơ chế đồng bộ**: nền tảng đọc lại nội dung thư mục qua hàm `SyncSourceFiles` (chi tiết D-SD03-017 (¶4.2), D-SD03-020 (¶4.5)) — liệt kê object dưới `storage_prefix`, so khớp với `source_file` đã có, tạo dòng mới cho file chưa thấy, đánh dấu `is_missing` cho file không còn tồn tại (không xoá dòng, giữ nguyên vẹn truy vết từ `claim_reference`).
- **Kích hoạt đồng bộ**: (a) tự động — MinIO/S3 bucket notification gửi webhook báo "thư mục có thay đổi" tới `/internal/ingestion`, xử lý debounce/coalesce theo `source_id` (độ trễ theo tham số cấu hình `operations.source_sync_debounce_seconds`, mặc định 45s — `07-system-settings.md`; hàng đợi bền river — D-SD01-001 (¶1), D-SD01-004 (¶4)) trước khi gọi `SyncSourceFiles`, tránh chạy dồn dập khi có nhiều file được ghi liên tục vào bucket; (b) thủ công — nút "Đồng bộ lại" ở Admin nội bộ, gọi thẳng không qua debounce.
- Sau khi đồng bộ: file mới đưa vào luồng nghiên cứu/xét duyệt bình thường (R-KB-074 (§2.2.6) đặc tả gốc), sinh chỉ mục + embedding + transcript như trước (D-SD01-004 (¶4)).
- Không có màn hình OCR/review OCR trong Admin của nền tảng này — chỉ có màn hình cấu trúc hoá & thẩm định tri thức trên dữ liệu đã có trong MinIO/S3.

## 6. [D-SD01-006] Kiến trúc AI — RAG cho AI Văn Minh Việt + AI Verification

**AI Gateway — đã chốt: self-host ngay từ đầu, chạy trên GPU on-prem, là một service Python độc lập** (không chỉ là interface trừu tượng), đứng sau ba điểm gọi trong Go monolith: `/internal/assistant` (năng lực RAG, module 05), `/internal/verification` (năng lực AI Verification, module 03) và `/internal/encyclopedia` (sinh nội dung Mục từ, module 04) — cả hai gọi qua API nội bộ gRPC/REST tới cùng một AI service (xem D-SD01-002 (¶2)). Phục vụ 3 năng lực (đặc tả đã bỏ đa ngôn ngữ nên không còn cần năng lực dịch thuật như dự kiến trước):

1. **RAG cho AI Văn Minh Việt** (module 05) — 5 bước, chi tiết hoá thêm khi viết tài liệu module đó:
   1. **Ingest/embedding** — nội dung đủ điều kiện (nội dung của **phiên bản đang công khai** từng Mục từ — con trỏ R-ENC-010 (§2.3.2.4.1), quản lý ở `/encyclopedia`) được chia đoạn, sinh embedding qua job nền, lưu vào `pgvector`, **gắn theo đúng `version_id` đã sinh nội dung đó** (không chỉ theo `entry_id`) — vì một Mục từ có thể có nhiều phiên bản đã chốt, chỉ một phiên bản là phiên bản đang công khai tại một thời điểm. ⚠ Hệ quả kỹ thuật (đề xuất bổ sung, chưa nêu trong đặc tả gốc): mỗi khi vai trò Xuất bản Mục từ đổi con trỏ phiên bản đang công khai — kể cả quay lại một phiên bản cũ hơn — phải **re-index**: vô hiệu embedding phiên bản không còn công khai khỏi tập truy hồi, sinh embedding cho phiên bản mới nếu chưa có; job nền tương ứng xem D-SD01-004 (¶4).
   2. **Retrieve** — kết hợp vector search + full-text (hybrid) để lấy đoạn liên quan.
   3. **Generate** — LLM sinh câu trả lời chỉ dựa trên đoạn đã truy hồi, kèm citation về Mục từ nguồn — khớp R-AI-002 (§2.4.1) đặc tả gốc.
   4. **Self-audit pass** — một lượt gọi LLM ở vai trò kiểm tra (model khác hoặc cùng model, khác prompt — D-SD06-006 (¶3.4)) rà lại câu trả lời **sau khi phần Generate đã stream xong**, gắn cờ phát biểu chưa được chứng thực; cờ gửi tới người dùng bằng một sự kiện SSE riêng ngay sau câu trả lời để hiển thị cảnh báo — không chặn, không trì hoãn việc stream câu trả lời (chi tiết D-SD05-005 (¶3.2), D-SD05-012 (¶5.1)).
   5. **Log & feedback** — lưu câu hỏi/đáp/nguồn để chuyên gia rà soát chất lượng sau này.
2. **AI Verification đa phương thức** (Trợ lý Tư liệu gốc, R-KB-080 (§2.2.6.6) đặc tả gốc) — so khớp Phát biểu với vị trí tham chiếu trong 4 loại tư liệu. **Đã chốt hướng phân rã** (không cần một "model đa phương thức" duy nhất):
   - **Văn bản**: so khớp ngữ nghĩa text-vs-text — dùng chung embedding/LLM judge với RAG, không cần gì đặc biệt.
   - **Âm thanh, và phần audio của phim**: chạy ASR self-host (Whisper hoặc PhoWhisper — bản tinh chỉnh tiếng Việt) lấy transcript đúng đoạn thời gian, rồi so khớp text như trên.
   - **Hình ảnh, và phần khung ảnh của phim**: dùng một Vision-Language Model (VLM) self-host để "đọc" nội dung trong khung toạ độ (ví dụ họ Qwen2-VL/InternVL — model mở, chạy được on-prem qua vLLM).
   - Phiên bản model cụ thể (ASR/VLM) cần **benchmark trên dữ liệu tư liệu gốc thật** (đặc biệt audio phỏng vấn nghệ nhân, ảnh hiện vật) trước khi pin — xem ¶9.
3. **Sinh bản nháp nội dung Mục từ** (module 04, R-ENC-038 (§2.3.8)) — job nền đọc Hạng mục tri thức đã gán, gọi LLM (và VLM cho ảnh) sinh nội dung theo khối; chi tiết D-SD04-019 (¶3.5), D-SD06-014 (¶3.8).

Tổ chức 3 năng lực trong cùng một service Python (theo capability bên trong), có thể tách tiếp thành nhiều service nếu tải lệch nhau nhiều về sau. Vẫn giữ AI Gateway như một lớp trừu tượng hoá phía gọi (Go monolith) để đổi/nâng cấp model self-host sau này mà không viết lại tầng gọi.

**Môi trường phát triển local (không có GPU)**: AI Gateway cần hỗ trợ nhiều chế độ backend, chọn qua cấu hình (ví dụ biến `AI_GATEWAY_MODE`), để Go monolith không cần đổi code khi đổi backend:

- `mock` — trả response giả cố định (text mẫu, embedding vector giả), không cần model nào; dùng khi phát triển/test luồng nghiệp vụ (RAG orchestration, AI Verification workflow, lưu kết quả...), không cần chất lượng AI thật.
- `cpu-small` — model nhỏ chạy CPU (ví dụ embedding nhỏ qua sentence-transformers, LLM quantize nhỏ qua llama.cpp); chậm hơn GPU nhiều nhưng cho kết quả thật, dùng khi cần test chất lượng RAG/citation hoặc AI Verification thực sự.
- `gpu-onprem` — vLLM + GPU on-prem như đã chốt ở trên; mặc định cho production.

Đây là hệ quả trực tiếp của việc giữ AI Gateway như một lớp trừu tượng hoá (đã nêu ở trên) — chỉ cần đổi implementation phía sau, không viết lại tầng gọi ở Go monolith. Đây là một yêu cầu kỹ thuật cụ thể khi build AI service (không chỉ là gợi ý tiện dụng), để khi triển khai không mặc định luôn có sẵn GPU.

## 7. [D-SD01-007] Bảo mật & tuân thủ

- Xác thực: token JWT + refresh token — áp dụng cho Nhân viên (cả 2 giao diện — D-SD01-001 (¶1), D-SD01-002 (¶2)). Middleware xác thực kiểm tra thêm trạng thái tài khoản và mốc vô hiệu hoá phiên ở mỗi request, để đăng xuất ngay khi vô hiệu hoá tài khoản hoặc đổi/đặt lại mật khẩu (R-ID-025 (§2.1.5.7.1), R-ID-034 (§2.1.5.9.4), R-ID-038 (§2.1.5.10.3) — D-SD02-007 (¶3.5)). Người dùng công khai không cần xác thực (truy cập ẩn danh, R-GEN-007 (§1.2.2)/R-PUB-002 (§2.6.1) đặc tả gốc).
- Phân quyền ở tầng service (dựa trên `roles` — xem `00-claude-instructions.md` mục 6) **và** ở tầng route/API cho ranh giới giữa cả 3 nhóm route — Admin nội bộ, Cổng Tổ chức khác, và Web công khai (không yêu cầu xác thực) — xem D-SD01-002 (¶2).
- Audit log bất biến (append-only — ứng dụng chỉ INSERT, không UPDATE/DELETE) cho luồng xét duyệt (R-NFR-004 (§3.1.2) đặc tả gốc) — bảng `audit_log` sở hữu bởi `/shared`, xem cơ chế và phạm vi sự kiện cụ thể ở D-SD01-002 (¶2). Ngoại lệ duy nhất: job `shared.audit_log_cleanup` xoá các bản ghi quá thời hạn lưu (D-SD01-002 (¶2), D-SD01-004 (¶4)).
- Mã hoá dữ liệu nhạy cảm at-rest: email, số điện thoại (R-NFR-003 (§3.1.1), R-ID-003 (§2.1.2) đặc tả gốc — hiện là thông tin định danh của **Nhân viên**, vì Người dùng công khai không còn tài khoản/dữ liệu cá nhân nào ở giai đoạn này).
- Mã hoá truyền tải: TLS/HTTPS bắt buộc trên mọi kênh (website, ứng dụng di động, backend) — R-NFR-006 (§3.1.4) đặc tả gốc.
- Xác thực đa yếu tố (MFA): chưa bắt buộc ở giai đoạn này cho bất kỳ vai trò nào, kể cả Quản trị hệ thống — R-NFR-007 (§3.1.5) đặc tả gốc; có thể xem xét bổ sung cho các vai trò nhạy cảm ở giai đoạn sau.
- Rate limit theo IP cho Trợ lý AI Văn Minh Việt trên Web công khai (R-NFR-008 (§3.1.6) đặc tả gốc — truy cập ẩn danh, không tài khoản; hệ thống có sẵn cơ chế, khi mới triển khai ở trạng thái tắt); áp dụng cho `assistant.chat` — `POST /api/v1/public/assistant/chat` (D-SD01-002 (¶2)) bằng **middleware Go**, bật/tắt và ngưỡng do Quản trị hệ thống cấu hình (`assistant.public_rate_limit_*`, mặc định tắt) — chi tiết D-SD07-009 (¶4.3), D-SD05-012 (¶5.1).
- Chính sách mật khẩu, tạm khoá đăng nhập sau nhiều lần sai và đổi mật khẩu khi đang đăng nhập (R-ID-029 (§2.1.5.8)–R-ID-035 (§2.1.5.10)), tham số do Quản trị hệ thống cấu hình (R-CFG-007 (§2.8.4.2)) — D-SD02-004 (¶3.2)–D-SD02-006 (¶3.4), `07-system-settings.md`.
- **Data residency (R-NFR-005 (§3.1.3) đặc tả gốc)**: toàn bộ dữ liệu hệ thống — dữ liệu cá nhân Nhân viên, Tư liệu gốc, nội dung Hạng mục tri thức và Mục từ — bắt buộc lưu trữ trong lãnh thổ Việt Nam; ràng buộc việc chọn nhà cung cấp hạ tầng Database/Object storage ở D-SD01-001 (¶1). **Phạm vi không bao gồm Email/SMTP** (xem D-SD01-001 (¶1)): email là hạ tầng truyền tải/chuyển tiếp, không phải nơi lưu trữ lâu dài dữ liệu cá nhân, nên giữ nguyên Amazon SES.
- **Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân** — được `business-requirements.md` R-NFR-003 (§3.1.1) chính thức tham chiếu. Áp dụng trực tiếp cho việc mã hoá dữ liệu định danh cá nhân Nhân viên (email, số điện thoại) ở trên. Các khía cạnh vận hành cụ thể hơn (cơ chế đồng ý, quyền xoá, giới hạn mục đích sử dụng...) vẫn để lại cho giai đoạn triển khai thực tế — đặc tả gốc chưa yêu cầu chi tiết hơn.

## 8. [D-SD01-008] NFR — theo số liệu chính thức đã chốt ở đặc tả gốc (R-NFR-009 (§3.2))

| Nhóm | Số liệu chính thức (đặc tả gốc) | Ý nghĩa kiến trúc |
|---|---|---|
| Tải Ứng dụng Web công khai | 50–100 request/giây ổn định, chịu burst 200–300 request/giây (R-NFR-010 (§3.2.1)) | Quy mô khiêm tốn cho giai đoạn ra mắt — Next.js SSR/SSG + cache/CDN là đủ, chưa cần hạ tầng scale ngang lớn ngay; kiến trúc cần cho phép mở rộng ngang dần theo thời gian (R-NFR-010 (§3.2.1)) |
| Phản hồi AI Văn Minh Việt | Token đầu ≤3 giây, hoàn tất ≤15 giây (p95) (R-NFR-011 (§3.2.2)) | AI service (D-SD01-006 (¶6)) cần trả lời dạng streaming; GPU on-prem phải đủ throughput cho mức độ trễ này |
| Trợ lý Tư liệu gốc (AI Verification) | Không cần real-time, vài phút/hạng mục là chấp nhận được (R-NFR-011 (§3.2.2)) | Xử lý qua hàng đợi nền (D-SD01-004 (¶4)), không cần ưu tiên GPU như AI Văn Minh Việt |
| Uptime | 99.5% cho Web công khai & AI Văn Minh Việt (R-NFR-012 (§3.2.3)); backend Nhân viên chấp nhận downtime cao hơn | Cần giám sát/cảnh báo cơ bản (D-SD01-004 (¶4), logging/tracing); chưa cần multi-region/HA phức tạp ở giai đoạn này |
| Nhân viên đồng thời | Vài chục đến ~200 người (R-NFR-013 (§3.2.4)) | Xác nhận modular monolith (D-SD01-002 (¶2)) đủ đáp ứng — chưa có áp lực tách service theo tải ở phần nghiệp vụ lõi; cũng đủ nhỏ để ghi `audit_log`/`usage_event` đồng bộ cùng transaction (D-SD01-002 (¶2)) mà không cần tách hạ tầng riêng |
| Sao lưu & khôi phục | Sao lưu hàng ngày, RPO 24 giờ / RTO 24 giờ (R-NFR-023 (§3.4.1)) | Backup job chạy hàng ngày cho DB + Object storage tư liệu gốc; cần runbook khôi phục và test định kỳ để đảm bảo đạt RTO 24h khi có sự cố |
| Trình duyệt hỗ trợ | Chrome/Safari/Firefox/Edge — 2 phiên bản gần nhất (R-NFR-019 (§3.3.4)) | Web công khai (Next.js) không cần polyfill/hỗ trợ trình duyệt cũ |
| Accessibility | Chưa yêu cầu WCAG cụ thể ở giai đoạn này (R-NFR-021 (§3.3.6)) | Không cần đầu tư audit/test accessibility riêng cho giai đoạn ra mắt |

Các mục kỹ thuật bổ sung (không phải chỉ số chính thức của đặc tả, do kiến trúc đề xuất thêm để vận hành được):

| Nhóm | Gợi ý |
|---|---|
| Sẵn sàng | Runbook khôi phục cụ thể + lịch test định kỳ để đảm bảo đạt RPO/RTO đã chốt chính thức (R-NFR-023 (§3.4.1), xem bảng phía trên) |
| Quan sát | Logging, tracing (`trace_id`), dashboard trạng thái job nền |
| Tài liệu kỹ thuật | Hợp đồng OpenAPI theo từng nhóm route — D-SD01-003 (¶3) |
| Kiểm thử | Bộ test tự động cho state machine xét duyệt và tính "có dẫn nguồn" của AI |

## 9. Vấn đề mở

- Benchmark thực tế trên dữ liệu tư liệu gốc thật trước khi pin phiên bản cụ thể của model ASR/VLM dùng cho AI Verification — hướng phân rã đã chốt ở D-SD01-006 (¶6), chỉ còn version/model cụ thể.
- Ngưỡng chuyển phiên bản cũ của Tư liệu gốc sang cold storage là tham số cấu hình `operations.source_cold_storage_after_days` (mặc định không chuyển) — Quản trị hệ thống đặt khi có số liệu tăng trưởng thực tế (R-NFR-014 (§3.2.5) đặc tả gốc); cơ chế áp dụng ở D-SD07-009 (¶4.3).
- Domain allowlist cụ thể cho CORS (D-SD01-003 (¶3)) — chốt khi có domain production thật.
- Danh sách cụ thể các loại sự kiện `usage_event` (D-SD01-002 (¶2)) và logic tính chi phí (cách tính, đơn giá, xuất hoá đơn) — chờ đặc tả nghiệp vụ billing cụ thể sau này (R-ID-015 (§2.1.4.6) đặc tả gốc), hiện chỉ chốt cơ chế ghi nhận.
- Model CPU nhỏ cụ thể dùng cho chế độ `cpu-small` (D-SD01-006 (¶6), dev không GPU) — chọn model/version cụ thể khi bắt đầu code AI service, không chốt trước ở tài liệu này.
- **Ghép tên/email Nhân viên vào `shared.listAuditLogs` — `GET /shared/audit-logs`** (D-SD01-002 (¶2)) — ⚠ bổ sung 2026-09-23: hoàn thiện kỹ thuật cho màn hình Nhật ký hoạt động (D-ADM-021 (¶4.21), trước đó chỉ có `employee_id` thô). Chọn ghép ở tầng handler (`/cmd/api`, gọi `identity.GetEmployeeSummaries` sau khi có `shared.ListAuditLogs`) thay vì lưu snapshot tên/email vào `audit_log` lúc ghi, để tránh import cycle Go giữa `/shared` và `/identity`. Không đổi schema `audit_log`.
- **Hàng đợi job dùng river, Redis không bắt buộc** (D-SD01-001 (¶1)) — ⚠ quyết định kỹ thuật: các điểm enqueue đã chốt ở `03`/`04` (`TriggerAIVerification`, `SetPublicVersion`, `AssignCulturalDomain`…) đều enqueue cùng transaction với thao tác nghiệp vụ, điều mà hàng đợi trên Redis không đảm bảo được.
- **Tên loại job, ánh xạ trạng thái và API `shared.listJobs`** (D-SD01-004 (¶4)) — ⚠ đề xuất bổ sung, hoàn thiện kỹ thuật cho màn hình theo dõi job nền của Admin nội bộ (D-ADM-026 (¶4.26)). Không đổi hành vi nghiệp vụ.
- **Danh mục sự kiện audit, cột `actor_type`** (D-SD01-002 (¶2)) — ⚠ đề xuất bổ sung: mở rộng R-NFR-004 (§3.1.2) thành mọi thao tác ghi thành công của Nhân viên, cộng thay đổi do hệ thống tự thực hiện trên dữ liệu nghiệp vụ (`source.sync` qua webhook, `knowledge_object.ai_verification_complete`, `auth.login_locked`). `audit_log.employee_id` thành nullable, thêm `actor_type`. Thao tác soạn thảo chi tiết vẫn ghi mọi lần, `detail` chỉ chứa id/tên trường. Đăng nhập sai chỉ ghi khi tạm khoá.
