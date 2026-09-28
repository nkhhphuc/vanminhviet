# Đặc Tả Giao Diện Web Admin Nội Bộ — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình thiết kế giao diện Admin nội bộ (Quasar SPA, dành cho Nhân viên thuộc Tổ chức Văn Minh Việt — §1.2.3.1 đặc tả gốc). Đọc `common/00-claude-common-instructions.md` trước, rồi đọc file này trước khi chỉnh sửa `admin-web-design.md`, kể cả ở một session khác.

## 1. Mục tiêu

- Thiết kế/biên tập `admin-web-design.md` thành một đặc tả giao diện đủ chi tiết để đội dev dùng làm đầu vào build giao diện Admin nội bộ.
- Đối tượng dùng: Nhân viên Tổ chức Văn Minh Việt — đầy đủ chức năng, gồm quản lý người dùng/phân quyền/Tổ chức, nạp liệu, nghiên cứu/xét duyệt Hạng mục tri thức, biên tập Mục từ... (theo ranh giới route `/api/v1/admin/...` đã chốt ở `system-design/01-architecture-and-tech-stack.md` mục 2).
- Vì là công cụ nội bộ, ưu tiên rõ ràng chức năng và tốc độ thao tác hơn là trải nghiệm hình ảnh — không cần mockup chi tiết như `public-web/`, wireframe/mô tả bố cục ở mức đủ dùng cho dev là được, trừ khi có yêu cầu khác.

## 2. File nguồn & ranh giới thư mục

- `admin-web/admin-web-design.md` là **nguồn chân lý duy nhất** cho đặc tả giao diện Admin nội bộ. Không tạo thêm bản sao/bản nháp song song trong project.
- `requirements/` (đặc tả nghiệp vụ gốc) và `system-design/` (thiết kế kỹ thuật, gồm mô hình dữ liệu/API mà giao diện này gọi vào) — **không thuộc phạm vi của luồng này**, chỉ đọc để đối chiếu, không ghi vào đó.
- `admin-web/changelog.md` là nhật ký các thay đổi đã ghi vào `admin-web-design.md` (xem quy tắc chung ở `common/00-claude-common-instructions.md` mục 2).
- Mọi file phát sinh từ luồng này chỉ lưu trong thư mục `admin-web/` — không rải rác sang thư mục khác.

## 3. Quy ước cấu trúc tài liệu

- Đánh số màn hình theo mục `4.x` (một màn hình/nhóm màn hình = một mục con), giữ nguyên cách đánh số hiện có khi thêm màn hình mới để không xáo trộn tham chiếu.
- Mỗi màn hình nên ghi rõ: vai trò/quyền nào được truy cập (đối chiếu `system-design/02-identity.md`), API/module backend liên quan (đối chiếu package trong `system-design/01-architecture-and-tech-stack.md` mục 2: `/identity`, `/knowledge`, `/gate`, `/encyclopedia`...).
- Phần nào là thiết kế UI đi trước đặc tả nghiệp vụ (chưa có cơ sở ở `business-requirements.md` hoặc `system-design/`) cần đánh dấu rõ ràng (ví dụ ghi chú ngay dưới tiêu đề màn hình).

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, và luôn `project_read` bản mới nhất trước khi ghi đè: theo nguyên tắc chung ở `common/00-claude-common-instructions.md` mục 3.
- Sau khi ghi xong một thay đổi vào `admin-web-design.md`, tóm tắt ngắn gọn cho người dùng xem, đồng thời ghi thêm một mục vào `admin-web/changelog.md`.
- Đồng bộ ra máy: theo nguyên tắc chung mục 1 (`admin-web/` ↔ `Z:\GoogleDrive\VanMinhViet\admin-web`).

## 5. Đối chiếu với Business Requirements / System Design — quy trình xử lý điểm lệch

Khi phát hiện một điểm trong `admin-web-design.md` không có cơ sở (hoặc lệch) so với `requirements/business-requirements.md` hoặc `system-design/`:

1. Nêu rõ điểm lệch (chức năng/thành phần nào, khớp hay không khớp mục nào).
2. Hỏi người dùng chọn hướng xử lý: (a) giữ trong `admin-web-design.md` kèm ghi chú rõ đây là thiết kế đi trước; (b) tạm gỡ khỏi tài liệu giao diện; (c) để lại xử lý sau; (d) gửi đề xuất bổ sung thiết kế sang `system-design/` (thuần kỹ thuật, không đổi hành vi nghiệp vụ) — nếu người dùng chọn hướng này, việc soạn/ghi đề xuất thực hiện trong đúng luồng `system-design` (đọc `system-design/00-claude-instructions.md` trước), không ghi trực tiếp từ luồng `admin-web`.
3. **Không tự sửa `business-requirements.md` hay tài liệu `system-design/` trong luồng này.**
4. Ghi nhận kết quả từng điểm vào mục 7 (Trạng thái hiện tại) của chính file này.

## 6. Quyết định đã chốt

- **Màn hình Nhật ký hoạt động (4.21)**: phạm vi chỉ lịch sử audit log (không theo dõi "đang online"); cập nhật bằng polling định kỳ phía client (không WebSocket/SSE); quyền xem giới hạn role `quan_tri_he_thong`, xem toàn bộ không giới hạn phạm vi/Tổ chức.
- **Nhóm Cơ sở dữ liệu văn hóa (4.8–4.15)**: theo đúng mô hình dữ liệu/state machine ở `system-design/03-cultural-knowledge-base.md` — Tư liệu gốc đồng bộ từ MinIO/S3 (không upload thủ công qua UI), Hạng mục tri thức dùng cơ chế "Người phụ trách" (`assignee_id`) xuyên suốt vòng đời.
- **Nhóm Bách khoa toàn thư (4.16–4.20)**: theo đúng mô hình dữ liệu/state machine ở `system-design/04-encyclopedia.md`. Quản lý danh mục Cương vực (4.20 — tạo/sửa/xoá; xoá bị chặn khi còn Mục từ đang gán, 409 `cultural_domain_in_use`) giới hạn cho role `bien_tap`.
- **Nút "Cưỡng chế nhả" (Force Release)**: hiện ở cả 4 màn hình có khối "Người phụ trách" — 4.13, 4.14, 4.17, 4.18 — chỉ cho role `quan_tri_he_thong`, chỉ khi đang có người phụ trách.
- **Xét duyệt Mục từ (4.18)**: nút Đạt/Không đạt xét duyệt không giới hạn theo `assignee_id` — khác Hạng mục tri thức (module 03), là chủ ý.
- **Nguyên tắc "bức tranh tổng thể"**: giao diện luôn thể hiện cấu trúc điều hướng/phân cấp dữ liệu toàn hệ thống và vị trí màn hình hiện tại, áp dụng cho toàn bộ 28 màn hình, qua 4 cơ chế: Breadcrumb (đầu mỗi màn hình con, trừ nhóm Xác thực và Dashboard), Stepper trạng thái theo cụm (4.13/4.14/4.15 và 4.17/4.18/4.19 — "Không đạt xét duyệt"/"Mở lại" thể hiện bằng mũi tên cong, không phải bước riêng), Sidebar luôn highlight mục đang chọn + mục "Tổng quan" đứng đầu, Topbar hiển thị tên nhóm/module hiện tại.
- **Dashboard (4.22)**: nội dung hoàn toàn tĩnh — sơ đồ pipeline nghiệp vụ tổng thể (Khối 1) + mô tả ngắn từng nhóm chức năng (Khối 2), không có chip đếm số liệu, không phụ thuộc API `stats`.
- **Nhóm Trợ lý AI (4.23–4.25)**: theo `system-design/05-ai-assistant.md` (hợp đồng SSE mục 5.1, API rà soát mục 5.2). 4.23 cho mọi Nhân viên, chỉ giữ một hội thoại hiện tại (không danh sách hội thoại cũ), lưu tạm trong localStorage theo Nhân viên trong `assistant.conversation_ttl_hours` (mặc định 6 giờ, qua `GET /client-settings`) tính từ lượt hỏi cuối để chat tiếp khi tải lại trang (xoá khi "Hội thoại mới"/Đăng xuất), trích dẫn mở Trang chi tiết Mục từ của Web công khai, cảnh báo cờ self-audit dưới câu trả lời. 4.24–4.25 chỉ `quan_tri_he_thong`, chỉ đọc.
- **Theo dõi job nền (4.26)**: theo `system-design/01-architecture-and-tech-stack.md` mục 4 (API `/shared/jobs`). Chỉ `quan_tri_he_thong`; Chạy lại job lỗi, Huỷ job đang chờ (có cảnh báo hệ quả theo loại job); polling như 4.21 (chu kỳ theo `operations.admin_polling_interval_seconds`).
- **Đánh chỉ mục lại cho AI (4.19)**: nút chỉ cho `quan_tri_he_thong`, khi Mục từ có phiên bản công khai.
- **Menu tài khoản & Đăng xuất (mục 3)**: Topbar nền kem `#FAF6EE`, chữ `#241C15`/Chữ phụ, không dùng chữ trắng; chữ trắng `#FFFFFF` chỉ dùng trên nền Accent; giữ nguyên bảng màu hiện hành. Menu tài khoản gồm "Đổi mật khẩu" và "Đăng xuất"; Đăng xuất không hỏi xác nhận (trừ khi có form chỉnh sửa dở), luôn xoá phiên cục bộ kể cả khi API lỗi; hết phiên ngoài ý muốn xử lý như Đăng xuất kèm thông báo và quay lại màn hình trước sau khi đăng nhập lại; 401 `session_revoked` → không làm mới phiên, về thẳng 4.1.
- **Đổi mật khẩu (4.27)**: dialog từ menu tài khoản, mọi Nhân viên; theo `02-identity.md` mục 3.4 (`POST /auth/change-password`); kiểm tra chính sách mật khẩu theo `GET /auth/password-policy`; `login_locked` → xử lý như phiên bị thu hồi; đổi thành công → đăng xuất mọi thiết bị (kể cả thiết bị đang dùng), về 4.1.
- **Cấu hình hệ thống (4.28)**: theo `system-design/07-system-settings.md`; nhóm Sidebar riêng "Hệ thống", chỉ `quan_tri_he_thong`; lưu theo từng nhóm (nguyên khối), khôi phục mặc định từng tham số; xác nhận khi giảm thời hạn lưu.

## 7. Trạng thái hiện tại

- 28 màn hình (4.1–4.28) đã thiết kế xong: Nhóm Tổng quan (4.22), Nhóm Xác thực (4.1–4.3, 4.27), Nhóm Quản lý người dùng & Tổ chức (4.4–4.7), Nhóm Cơ sở dữ liệu văn hóa (4.8–4.15), Nhóm Bách khoa toàn thư (4.16–4.20), Nhóm Trợ lý AI (4.23–4.25), Nhóm Giám sát (4.21, 4.26), Nhóm Hệ thống (4.28).
- Điểm lệch đang mở: không còn. Toàn bộ màn hình khớp `business-requirements.md`/`system-design/01–05, 07`.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-common-instructions.md` mục 4.
