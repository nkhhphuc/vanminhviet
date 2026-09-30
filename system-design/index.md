# Mục Lục Tài Liệu Thiết Kế Hệ Thống — Văn Minh Việt

> Bản đồ bộ tài liệu thiết kế: mỗi file tương ứng package/route nào, phụ thuộc vào đâu, và cần đọc những file nào cho từng phần việc. Đặc tả gốc: `requirements/business-requirements.md`.

## 1. Danh sách tài liệu

| File | Nội dung | Package Go / route | Phụ thuộc vào | Trạng thái |
|---|---|---|---|---|
| `01-architecture-and-tech-stack.md` | Tech stack, kiến trúc modular monolith, quy ước API chung, background job, tiếp nhận Tư liệu gốc, kiến trúc AI, bảo mật, NFR | Toàn hệ thống; `/shared` (audit log, usage event) | — | Đã chốt |
| `02-identity.md` | Quản lý người dùng: Nhân viên, Tổ chức, role theo chức năng / theo phạm vi, xác thực | `/identity` (`auth/*`, `identity/*`) | 01, 07 | Đã chốt `02` ¶1–5 |
| `03-cultural-knowledge-base.md` | Cơ sở dữ liệu văn hóa: Đề tài nghiên cứu, Tư liệu gốc, Hạng mục tri thức, workflow xét duyệt, AI Verification | `/ingestion`, `/knowledge`, `/provenance`, `/gate`, `/verification` | 01, 02, 06, 07 | Đã chốt `03` ¶1–6 |
| `04-encyclopedia.md` | Bách khoa toàn thư: Mục từ, phiên bản, Cương vực, workflow xét duyệt Mục từ | `/encyclopedia`; route `public` | 01, 02, 03 | Đã chốt `04` ¶1–6, trừ R-ENC-038 (§2.3.8) |
| `05-ai-assistant.md` | AI Văn Minh Việt: RAG, hội thoại nhiều lượt, log chất lượng | `/assistant` (route `admin`, `public`) | 01, 04, 06, 07 | Đã chốt `05` ¶1–6 |
| `06-ai-gateway.md` | AI Gateway: endpoint embed/generate/rewrite/self-audit/transcribe/verify, model, prompt, vận hành | Service Python riêng (mạng nội bộ) | 01 | Đã chốt |
| `07-system-settings.md` | Cấu hình hệ thống: registry tham số, giá trị đã chỉnh, API cấu hình | `/shared` (system settings) | 01 | Đã chốt |

## 2. Chiều phụ thuộc giữa các module

`07 settings` ← `02 identity` ← `03 knowledge…` ← `04 encyclopedia` ← `05 assistant`

- `01` là nền cho mọi tài liệu. `07` (cấu hình, thuộc package `/shared`) chỉ phụ thuộc `01`; 02, 03, 05 đọc cấu hình qua getter `shared.Settings` (D-SD07-007 (¶4.1)).
- API `/shared/settings` dùng xác thực và role `quan_tri_he_thong` của 02, và ghép `updated_by` bằng `identity.GetEmployeeSummaries` ở tầng handler `/cmd/api` — cùng cách `shared.listAuditLogs` — `GET /shared/audit-logs`. Đây là ghép nối ở tầng entrypoint, không phải phụ thuộc giữa package: `/shared` không import `/identity`.
- `06` (AI Gateway) được gọi bởi 03 (`/verification`, transcript) và 05 (`/assistant`).
- Không có phụ thuộc ngược chiều mũi tên; giao tiếp giữa module qua interface nội bộ, không JOIN chéo bảng (D-SD01-002 (¶2)).

## 3. Đọc gì khi làm gì

| Phần việc | File cần đọc |
|---|---|
| Hạ tầng, khung dự án, quy ước API chung | 01 |
| Đăng nhập, Nhân viên, role, Tổ chức | 01, 02, 07 |
| Đề tài nghiên cứu, Tư liệu gốc, Hạng mục tri thức, xét duyệt | 01, 02, 03, 07 (+ 06 cho AI Verification) |
| Mục từ, Cương vực, Web công khai | 01, 02, 04 (+ 03 cho phần tham chiếu Hạng mục tri thức) |
| AI Văn Minh Việt | 01, 04, 05, 06, 07 |
| Service AI Gateway | 01, 06 |
| Màn hình cấu hình hệ thống | 01, 07 |
