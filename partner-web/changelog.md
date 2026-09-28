# Changelog — Partner Web

## 2026-09-28

- CR-20260928-01: đổi toàn bộ trích dẫn mục đặc tả `§...` sang dạng chuẩn `R-XXX-NNN (§...)`; khoảng mục ghi ID cho hai đầu mút; "module 2.7" ghi thành `R-PTN-001 (§2.7)`. Không đổi nội dung thiết kế. File: **partner-web-design.md** (47), **00-claude-instructions.md** (16).

## 2026-09-26
- Đồng bộ theo `system-design/02-identity.md` mục 3.5, 5.1 (HTTP 401 `session_revoked`), file `partner-web-design.md`:
  - Mục 3: thêm bullet "Phiên đăng nhập". Access token hết hạn thì tự gọi `POST /auth/refresh`. Nhận `session_revoked` (từ bất kỳ API nào, kể cả refresh) thì không refresh, không gọi logout; xoá token và store, về 4.1 kèm thông báo "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Không hiện hộp thoại "Thay đổi chưa lưu". Đăng nhập lại thì về màn hình trước đó nếu còn quyền, không thì về 4.11.
  - Mục 4.1: thêm banner thông báo khi bị chuyển về do `session_revoked`.
- Thêm màn hình 4.12 Đổi mật khẩu (§2.1.5.10, `system-design/02-identity.md` mục 3.4, 5.1), file `partner-web-design.md`: dialog mở từ menu tài khoản trên Topbar, cho mọi Nhân viên đã đăng nhập; cảnh báo thay đổi chưa lưu trước khi mở; hiển thị chính sách mật khẩu qua `GET /auth/password-policy`; xử lý lỗi `invalid_current_password`, `password_unchanged`, `password_policy_violation`, `login_locked` (gọi `GET /auth/me` để phân biệt vừa bị tạm khoá trong dialog, phiên đã bị vô hiệu hoá, với đang tạm khoá từ trước, phiên còn hợp lệ); thành công thì xoá phiên và về 4.1 kèm banner. Cập nhật mục 2 (danh sách màn hình), mục 3 (Topbar có menu tài khoản), mục 4.1 (banner đổi mật khẩu thành công/tạm khoá), mục 7 (12 màn hình).
- `00-claude-instructions.md` mục 6, 7: cập nhật số màn hình thành 12, thêm 4.12 và §2.1.5.10 vào trạng thái hiện tại.
- Mục 4.2 bước 2 và 4.3 của `partner-web-design.md` (`system-design/02-identity.md` mục 3.1 bước 4, 3.3 bước 5): hiển thị và kiểm tra chính sách mật khẩu qua `GET /auth/password-policy`, xử lý lỗi `password_policy_violation`. Khi thành công, thay form bằng thông báo tại chỗ ("Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại bằng mật khẩu mới." / "Kích hoạt tài khoản thành công. Vui lòng đăng nhập.") kèm nút "Quay lại đăng nhập" dẫn tới 4.1, không tự chuyển trang.

## 2026-09-24
- Thêm Bảng màu (Color Palette) vào mục 3 (Quy ước chung) và cập nhật mục 1 (Tổng quan) của `partner-web-design.md`: kế thừa từ bảng màu `public-web/public-web-layout.md` mục 2.1, cùng logic với `admin-web-design.md` mục 3 (accent đỏ mận `#A6192E` + chữ/viền dùng chung, vùng nội dung chính dùng nền trung tính) nhưng ấm hơn Admin nội bộ một mức — nền vùng nội dung chính `#FDFBF6` (kem rất nhạt) thay vì trắng/xám như admin-web, vì đây là giao diện Nhân viên Tổ chức khác (đối tác bên ngoài) nhìn thấy. Sidebar/Topbar dùng tông kem `#FAF6EE` giống public-web/admin-web. Badge trạng thái tiếp tục dùng bảng màu ngữ nghĩa chuẩn, không theo bảng màu thương hiệu này.
- Bổ sung "link văn bản (hyperlink) trong toàn ứng dụng" vào cột Áp dụng của dòng Accent (`#A6192E`) trong bảng màu mục 3 của `partner-web-design.md` — link thay màu xanh mặc định thành màu accent, cùng logic tái dùng accent cho hyperlink đã có ở `admin-web-design.md` mục 3.
