# Đặc Tả Giao Diện Cổng Nhân Viên Tổ Chức Khác — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình thiết kế giao diện Cổng Nhân viên Tổ chức khác (Quasar SPA, app/deploy riêng khỏi Admin nội bộ — dành cho Nhân viên thuộc Tổ chức khác, R-GEN-010 (§1.2.3.2)/R-PTN-001 (§2.7) đặc tả gốc). Đọc `common/00-claude-instructions.md` trước, rồi đọc file này trước khi chỉnh sửa `partner-web-design.md`, kể cả ở một session khác.

## 1. Mục tiêu

- Thiết kế/biên tập `partner-web-design.md` thành một đặc tả giao diện đủ chi tiết để đội dev dùng làm đầu vào build giao diện Cổng Nhân viên Tổ chức khác.
- Đối tượng dùng: Nhân viên Tổ chức khác — 3 vai trò theo phạm vi Đề tài được gán: Nghiên cứu, Xét duyệt (R-PTN-003 (§2.7.2)–R-PTN-004 (§2.7.3) đặc tả gốc) và Chủ nhiệm đề tài (R-KB-073 (§2.2.5.5)) — **không có** màn hình quản lý người dùng/Tổ chức (ranh giới route `/api/v1/partner/...` đã chốt ở D-SD01-002 (¶2) — chỉ mount `knowledge` và `gate`, không mount `identity`, `ingestion`, `encyclopedia`).
- Ưu tiên rõ ràng chức năng, phạm vi thao tác hẹp và đúng theo Đề tài được gán — không cần mockup chi tiết như `public-web/`.

## 2. File nguồn & ranh giới thư mục

- `partner-web/partner-web-design.md` là **nguồn chân lý duy nhất** cho đặc tả giao diện Cổng Nhân viên Tổ chức khác. Không tạo thêm bản sao/bản nháp song song trong project.
- `requirements/` và `system-design/` — **không thuộc phạm vi của luồng này**, chỉ đọc để đối chiếu, không ghi vào đó.
- `partner-web/changelog.md` là nhật ký các thay đổi đã ghi vào `partner-web-design.md`.
- Mọi file phát sinh từ luồng này chỉ lưu trong thư mục `partner-web/`.

## 3. Quy ước cấu trúc tài liệu

- Đánh số màn hình theo mục `4.x`, giữ nguyên cách đánh số hiện có khi thêm màn hình mới.
- ID thiết kế: mục 3 (Quy ước chung) và từng màn hình 4.x mang ID `D-PRT-NNN` đặt ngay sau số mục trong tiêu đề, theo `common/requirements-design-sync.md` mục 2.4. Màn hình mới nhận ID kế tiếp theo bảng "ID thiết kế lớn nhất đã cấp" trong `common/requirements-change-tracker.md`; ID không đổi khi đánh số lại mục. Trong `partner-web-design.md`, trích mục có ID dùng dạng `D-PRT-010 (¶4.10)` (kể cả khi nhắc số màn hình), mục không có ID dùng `¶N`; trích system-design dùng `D-SD0X-NNN (¶N)`, trích admin-web dùng `D-ADM-NNN (¶N)`.
- Mỗi màn hình cần ghi rõ ranh giới quyền theo Đề tài được gán (không được vượt phạm vi R-PTN-010 (§2.7.4) đặc tả gốc — "không có chức năng quản lý người dùng/Tổ chức dù giữ vai trò gì").
- Phần nào là thiết kế UI đi trước đặc tả nghiệp vụ cần đánh dấu rõ ràng.

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, luôn đọc lại bản mới nhất từ máy trước khi ghi.
- Sau khi ghi xong, tóm tắt cho người dùng và ghi vào `partner-web/changelog.md`.

## 5. Đối chiếu với Business Requirements / System Design — quy trình xử lý điểm lệch

Khi phát hiện một điểm trong `partner-web-design.md` không có cơ sở (hoặc lệch) so với `requirements/business-requirements.md` hoặc `system-design/`:

1. Nêu rõ điểm lệch (chức năng/thành phần nào, khớp hay không khớp mục nào).
2. Hỏi người dùng chọn hướng xử lý: (a) giữ trong `partner-web-design.md` kèm ghi chú rõ đây là thiết kế đi trước; (b) tạm gỡ khỏi tài liệu giao diện; (c) để lại xử lý sau; (d) gửi đề xuất bổ sung thiết kế sang `system-design/` (thuần kỹ thuật, không đổi hành vi nghiệp vụ) — nếu người dùng chọn hướng này, việc soạn/ghi đề xuất thực hiện trong đúng luồng `system-design` (đọc `system-design/00-claude-instructions.md` trước), không ghi trực tiếp từ luồng `partner-web`.
3. **Không tự sửa `business-requirements.md` hay tài liệu `system-design/` trong luồng này.**
4. Ghi nhận kết quả từng điểm vào mục 7 (Trạng thái hiện tại) của chính file này.

## 6. Quyết định đã chốt

- **Vai trò Xuất bản không thuộc phạm vi Cổng này** (`business-requirements.md` R-PTN-003 (§2.7.2)) — khớp `system-design/03-cultural-knowledge-base.md` (`/publish`, `/skip-publish`, `/set-used-version` chỉ mount `admin`).
- **Route đọc file Tư liệu gốc ở `partner`**: `GET /knowledge/research-topics/{id}/sources/{source_id}` (mount `admin`, `partner`).
- **Vai trò Chủ nhiệm đề tài** (R-KB-073 (§2.2.5.5)/R-PTN-008 (§2.7.3.4)–R-PTN-009 (§2.7.3.5)): màn hình riêng 4.10 "Quản lý & Tiến độ đề tài" (tách khỏi 4.5 vì phạm vi xem khác — không xem được Nội dung/Hạng mục tri thức chi tiết); nút "Xoá" Hạng mục tri thức (R-KB-049 (§2.2.3.14)) ở 4.6, 4.7, 4.10 — chỉ Chủ nhiệm đề tài của đề tài cha hoặc `assignee_id` hiện tại (không có `quan_tri_he_thong` ở Cổng này); không có nút đổi Chủ nhiệm đề tài ở Cổng này (`set-chair` chỉ mount `admin`).
- **Nguyên tắc "bức tranh tổng thể"**: giao diện luôn thể hiện cấu trúc điều hướng/phân cấp dữ liệu của Cổng này và vị trí màn hình hiện tại, áp dụng cho toàn bộ 12 màn hình, qua 4 cơ chế: Breadcrumb (đầu mỗi màn hình con, trừ nhóm Xác thực), Stepper trạng thái (4.7/4.8/4.9 — chỉ 1 Stepper vì Cổng này không có Mục từ, 5 cụm giống Admin nội bộ; cụm "Xuất bản" vẫn hiển thị đầy đủ dù Nhân viên không tự thao tác được, để phản ánh đúng vị trí thực tế trong vòng đời), Sidebar mục "Tổng quan" luôn đứng đầu + highlight mục đang chọn, Topbar hiển thị tên nhóm/màn hình hiện tại.
- **Dashboard (4.11)**: nội dung hoàn toàn tĩnh — sơ đồ phạm vi công việc (Khối 1) + mô tả ngắn theo từng role (Khối 2), không có chip đếm số liệu, không phụ thuộc API `stats`.

## 7. Trạng thái hiện tại

- 12 màn hình (4.1–4.12) đã thiết kế xong, khớp `business-requirements.md` R-GEN-010 (§1.2.3.2), R-PTN-001 (§2.7), R-KB-073 (§2.2.5.5), R-KB-012 (§2.2.1.7), R-KB-049 (§2.2.3.14), R-ID-035 (§2.1.5.10) và `system-design/01, 02, 03`: Nhóm Tổng quan (4.11), Nhóm Xác thực (4.1–4.3), Nhóm Nghiên cứu & Xét duyệt (4.4–4.10, gồm màn hình dành riêng cho Chủ nhiệm đề tài 4.10), dialog Đổi mật khẩu (4.12).
- Không còn điểm lệch nào đang mở. Tài liệu sẵn sàng làm đầu vào build.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-instructions.md` mục 4.
