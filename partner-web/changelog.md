# Changelog — Partner Web

## 2026-09-24
- Thêm Bảng màu (Color Palette) vào mục 3 (Quy ước chung) và cập nhật mục 1 (Tổng quan) của `partner-web-design.md`: kế thừa từ bảng màu `public-web/public-web-layout.md` mục 2.1, cùng logic với `admin-web-design.md` mục 3 (accent đỏ mận `#A6192E` + chữ/viền dùng chung, vùng nội dung chính dùng nền trung tính) nhưng ấm hơn Admin nội bộ một mức — nền vùng nội dung chính `#FDFBF6` (kem rất nhạt) thay vì trắng/xám như admin-web, vì đây là giao diện Nhân viên Tổ chức khác (đối tác bên ngoài) nhìn thấy. Sidebar/Topbar dùng tông kem `#FAF6EE` giống public-web/admin-web. Badge trạng thái tiếp tục dùng bảng màu ngữ nghĩa chuẩn, không theo bảng màu thương hiệu này.
- Bổ sung "link văn bản (hyperlink) trong toàn ứng dụng" vào cột Áp dụng của dòng Accent (`#A6192E`) trong bảng màu mục 3 của `partner-web-design.md` — link thay màu xanh mặc định thành màu accent, cùng logic tái dùng accent cho hyperlink đã có ở `admin-web-design.md` mục 3.

## 2026-09-26
- Đồng bộ theo `system-design/02-identity.md` mục 3.5, 5.1 (HTTP 401 `session_revoked`), file `partner-web-design.md`:
  - Mục 3: thêm bullet "Phiên đăng nhập". Access token hết hạn thì tự gọi `POST /auth/refresh`. Nhận `session_revoked` (từ bất kỳ API nào, kể cả refresh) thì không refresh, không gọi logout; xoá token và store, về 4.1 kèm thông báo "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Không hiện hộp thoại "Thay đổi chưa lưu". Đăng nhập lại thì về màn hình trước đó nếu còn quyền, không thì về 4.11.
  - Mục 4.1: thêm banner thông báo khi bị chuyển về do `session_revoked`.
- Thêm màn hình 4.12 Đổi mật khẩu (§2.1.5.10, `system-design/02-identity.md` mục 3.4, 5.1), file `partner-web-design.md`: dialog mở từ menu tài khoản trên Topbar, cho mọi Nhân viên đã đăng nhập; cảnh báo thay đổi chưa lưu trước khi mở; hiển thị chính sách mật khẩu qua `GET /auth/password-policy`; xử lý lỗi `invalid_current_password`, `password_unchanged`, `password_policy_violation`, `login_locked` (gọi `GET /auth/me` để phân biệt vừa bị tạm khoá trong dialog, phiên đã bị vô hiệu hoá, với đang tạm khoá từ trước, phiên còn hợp lệ); thành công thì xoá phiên và về 4.1 kèm banner. Cập nhật mục 2 (danh sách màn hình), mục 3 (Topbar có menu tài khoản), mục 4.1 (banner đổi mật khẩu thành công/tạm khoá), mục 7 (12 màn hình).
- `00-claude-instructions.md` mục 6, 7: cập nhật số màn hình thành 12, thêm 4.12 và §2.1.5.10 vào trạng thái hiện tại.
- Mục 4.2 bước 2 và 4.3 của `partner-web-design.md` (`system-design/02-identity.md` mục 3.1 bước 4, 3.3 bước 5): hiển thị và kiểm tra chính sách mật khẩu qua `GET /auth/password-policy`, xử lý lỗi `password_policy_violation`. Khi thành công, thay form bằng thông báo tại chỗ ("Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại bằng mật khẩu mới." / "Kích hoạt tài khoản thành công. Vui lòng đăng nhập.") kèm nút "Quay lại đăng nhập" dẫn tới 4.1, không tự chuyển trang.

## 2026-09-28

- CR-20260928-01: đổi toàn bộ trích dẫn mục đặc tả `§...` sang dạng chuẩn `R-XXX-NNN (§...)`; khoảng mục ghi ID cho hai đầu mút; "module 2.7" ghi thành `R-PTN-001 (§2.7)`. Không đổi nội dung thiết kế. File: **partner-web-design.md** (47), **00-claude-instructions.md** (16).

## 2026-09-29

- DC-20260929-01: đổi trích dẫn mục system-design sang dạng `D-SD0X-NNN (¶N)` (mục không có ID ghi `` `03` ¶5 ``); trích public-web ghi `public-web ¶2.1` kèm ⚠ chờ public-web cấp ID. Không đổi nội dung thiết kế. File: **partner-web-design.md** (mục 1, 3, 4.1, 4.2, 4.4, 4.6, 4.7, 4.12), **00-claude-instructions.md** (mục 1).
- DC-20260929-02: đổi trích dẫn admin-web sang `D-ADM-029 (¶3)`, `D-ADM-022 (¶4.22)`. Không đổi nội dung thiết kế. File: **partner-web-design.md** (mục 3, 4.11).
- DC-20260929-03: gắn ID `D-PRT-001`–`D-PRT-012` cho màn hình 4.1–4.12 và `D-PRT-013` cho mục 3 (Quy ước chung); đổi trích dẫn mục trong cùng file (kể cả số màn hình viết trần) sang `D-PRT-… (¶…)` / `¶N`. Không đổi nội dung thiết kế. File: **partner-web-design.md**, **00-claude-instructions.md** (mục 3 thêm quy ước ID).
- DC-20260929-04: đổi trích dẫn bảng màu public-web sang D-PUB-011 (¶2.1), gỡ ⚠ chờ public-web cấp ID. Không đổi nội dung thiết kế. File: **partner-web-design.md** (mục 3).

## 2026-09-30

- DC-20260930-01: căn theo cơ chế kích hoạt AI Verification theo cấu hình (D-SD07-004 (¶3.1), D-SD03-023 (¶5.3)). File **partner-web-design.md**:
  - Mục 4.7: "Gửi xét duyệt" không mặc định tự chạy AI Verification — hiện toast theo `status` trả về (`dang_xet_duyet_ai` / `cho_xet_duyet`); `cho_xet_duyet` ghi rõ khi nào hạng mục dừng ở đây; nút kích hoạt hiện theo `can_trigger_ai_verification` thay cho role cố định, tách nhãn "Kích hoạt AI Verification" (`cho_xet_duyet`) / "Kích hoạt lại AI Verification" (`dang_xet_duyet_ai`, `khong_dat_xet_duyet`).
  - Mục 4.8: nút "Kích hoạt lại AI Verification" tại `da_qua_xet_duyet_ai` hiện theo `can_trigger_ai_verification`; API thêm `GET /knowledge/knowledge-objects/{id}`.
  - Mục 4.11: cụm "Chờ & Xác minh AI" ghi "tự động hoặc kích hoạt thủ công theo cấu hình".
- DC-20260930-03: mục 4.7 — tại `dang_xet_duyet_ai` hiển thị theo `ai_verification_running` (`true`: "Đang chạy AI Verification..."; `false`: banner vàng báo AI Verification đã dừng, cần kích hoạt lại, thêm vế "liên hệ Nhân viên được phép kích hoạt AI Verification của đề tài" khi người xem không có nút kích hoạt); kết quả kích hoạt theo `merged_into_running_job` (`true`: thông báo AI Verification đang chạy, không tạo job mới; `false`: toast "Đã kích hoạt AI Verification"), dùng chung cho 4.8. File: **partner-web-design.md**.
- `00-claude-instructions.md` mục 7: ghi nhận lỗi ghi nhầm cột ở dòng DC-20260930-03 của sổ theo dõi, để xử lý sau.
- DC-20260930-04: đổi toàn bộ trích dẫn endpoint sang operationId, dạng `` `op` `` (giữ ` — METHOD /path` ở route đọc file Tư liệu gốc vì đang nói về nhóm mount), không kèm ID mục. Không đổi nội dung thiết kế. File: **partner-web-design.md** (mục 3, 4.1–4.10, 4.12, 6), **00-claude-instructions.md** (mục 6).
- DC-20260930-06: bổ sung vào danh sách API các endpoint đã có ở system-design, mount `partner`: 4.7 thêm `knowledge.createKnowledgeObjectFileUploadUrl`, `knowledge.getKnowledgeObjectFileDownloadUrl`, `knowledge.getResearchTopicSourceFileDownloadUrl`; 4.8 thêm 2 op download-url; 4.9 thêm `knowledge.listClaims` và 2 op download-url; 4.10 thêm `knowledge.searchResearchTopicEmployees`. File: **partner-web-design.md**.
- `00-claude-instructions.md` mục 7: gỡ ghi chú về lỗi ghi nhầm cột ở dòng DC-20260930-03, vì luồng admin-web đã sửa sổ theo dõi. Mốc đồng bộ partner-web: DC-20260930-06.

## 2026-10-01

- DC-20261001-04: căn nhận diện theo D-PUB-011 (¶2.1). File **partner-web-design.md**:
  - Mục 3: bảng màu mới — Accent `#C4171D`, Accent đậm `#9C2B2B` (hover/pressed), Chữ trên nền Accent `#FFFFFF`, chữ `#252421`/`#6D6A64`, viền `#E6E0D7`, Sidebar/Topbar `#F7F2EA`, nền nội dung giữ `#FDFBF6`; không dùng 2 màu phụ vàng đồng/xanh rêu; thêm quy tắc tương phản chữ/nền. Thêm bullet Typography (Be Vietnam Pro; Lora cho logo/H1, subset `vietnamese`) và bullet Bo góc & hình ảnh (8px, chip/badge pill, không ảnh trang trí, logo của landing vanminhviet.org).
  - Mục 1: bullet "Mức độ đặc tả" nhắc thêm font, bo góc và landing vanminhviet.org.
