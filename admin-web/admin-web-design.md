# Đặc Tả Giao Diện Web Admin Nội Bộ — Văn Minh Việt

> Xem khung làm việc và nguyên tắc tại `admin-web/00-claude-instructions.md`. Lịch sử thay đổi tại `admin-web/changelog.md`.

## 1. Tổng quan

- Quasar (Vue 3) + Pinia, SPA riêng cho Nhân viên thuộc Tổ chức Văn Minh Việt (R-GEN-009 (§1.2.3.1) đặc tả gốc) — đầy đủ chức năng: quản lý người dùng/phân quyền/Tổ chức, nạp liệu, nghiên cứu/xét duyệt Hạng mục tri thức, biên tập/xét duyệt/xuất bản Mục từ, hỏi AI Văn Minh Việt và rà soát chất lượng hỏi–đáp AI, giám sát audit log và job nền, cấu hình tham số hệ thống; mọi Nhân viên tự đổi mật khẩu và đăng xuất qua menu tài khoản trên Topbar.
- Vì là công cụ nội bộ, mức độ đặc tả dừng ở wireframe/mô tả bố cục đủ dùng cho dev — không mockup chi tiết layout/spacing như `public-web/` (theo `00-claude-instructions.md` mục 1). Riêng bảng màu (xem D-ADM-029 (¶3)) được định nghĩa để đảm bảo nhất quán nhận diện thương hiệu với `public-web/`, không phải mockup hình ảnh chi tiết.
- Một Nhân viên có thể giữ nhiều role cùng lúc (R-ID-005 (§2.1.3.1) đặc tả gốc) → giao diện cần hiển thị/ẩn theo tập hợp role đang có, không phải theo một role duy nhất.
- **Định hướng tổng thể** (nguyên tắc bổ sung 2026-09-23, xem `00-claude-instructions.md` mục 6): giao diện phải giúp người dùng luôn thấy được bức tranh tổng thể và vị trí của màn hình hiện tại trong bức tranh đó — thực hiện qua Breadcrumb, Stepper trạng thái, Sidebar/Topbar, và màn hình Dashboard (D-ADM-022 (¶4.22)), tất cả định nghĩa ở D-ADM-029 (¶3) và áp dụng cho từng màn hình bên dưới.

## 2. Danh sách màn hình

**Nhóm Tổng quan**
- 4.22. Tổng quan (Dashboard) — trang mặc định sau đăng nhập, xem D-ADM-029 (¶3) về vị trí thực tế trên sidebar.

**Nhóm Xác thực**
- 4.1. Đăng nhập
- 4.2. Quên mật khẩu / Đặt lại mật khẩu
- 4.3. Đặt mật khẩu lần đầu (từ lời mời)
- 4.27. Đổi mật khẩu (dialog, mở từ menu tài khoản trên Topbar)

**Nhóm Quản lý người dùng & Tổ chức** (`/identity`, chỉ role `quan_tri_he_thong`)
- 4.4. Danh sách Nhân viên
- 4.5. Tạo/sửa Nhân viên — gán Tổ chức, gán role
- 4.6. Danh sách Tổ chức
- 4.7. Tạo/sửa Tổ chức

**Nhóm Cơ sở dữ liệu văn hóa** (`/knowledge`, `/gate`, `/verification`)
- 4.8. Danh sách Đề tài nghiên cứu
- 4.9. Chi tiết Đề tài nghiên cứu
- 4.10. Danh sách Tư liệu gốc
- 4.11. Chi tiết Tư liệu gốc
- 4.12. Danh sách Hạng mục tri thức
- 4.13. Màn hình Nghiên cứu (biên tập Hạng mục tri thức)
- 4.14. Màn hình Xét duyệt Hạng mục tri thức (chuyên gia)
- 4.15. Màn hình Xuất bản Hạng mục tri thức

**Nhóm Bách khoa toàn thư** (`/encyclopedia`)
- 4.16. Danh sách Mục từ
- 4.17. Soạn thảo Mục từ (TipTap)
- 4.18. Xét duyệt Mục từ
- 4.19. Xuất bản Mục từ
- 4.20. Quản lý Cương vực

**Nhóm Trợ lý AI** (`/assistant`)
- 4.23. Hỏi AI Văn Minh Việt — mọi Nhân viên
- 4.24. Danh sách hỏi–đáp AI — chỉ role `quan_tri_he_thong`
- 4.25. Chi tiết hội thoại AI — chỉ role `quan_tri_he_thong`

**Nhóm Giám sát** (`/shared`, chỉ role `quan_tri_he_thong`)
- 4.21. Nhật ký hoạt động (Audit Log)
- 4.26. Theo dõi job nền

**Nhóm Hệ thống** (`/shared`, chỉ role `quan_tri_he_thong`)
- 4.28. Cấu hình hệ thống

> Ghi chú đánh số: D-ADM-022 (¶4.22) (Dashboard) được đánh số cuối cùng để không xáo trộn tham chiếu các mục đã có (theo quy ước "giữ nguyên cách đánh số hiện có" ở `00-claude-instructions.md` mục 3), nhưng **vị trí thực tế trên Sidebar là mục đầu tiên** (D-ADM-029 (¶3)) — số thứ tự tài liệu không phản ánh thứ tự điều hướng. Tương tự, D-ADM-023 (¶4.23)–D-ADM-028 (¶4.28) đánh số nối tiếp sau D-ADM-022 (¶4.22); vị trí trên Sidebar theo nhóm (D-ADM-029 (¶3)). D-ADM-027 (¶4.27) không có mục trên Sidebar — mở từ menu tài khoản trên Topbar.

## 3. [D-ADM-029] Quy ước chung — khung ứng dụng & điều hướng

- **Bố cục sau đăng nhập**: Sidebar cố định bên trái + Topbar trên cùng + khu vực nội dung chính.
- **Bảng màu (Color Palette)** (bổ sung 2026-09-24): kế thừa vừa phải từ bảng màu D-PUB-011 (¶2.1) — dùng chung màu nhận diện thương hiệu, nhưng vùng nội dung/bảng dữ liệu chính dùng nền trung tính để ưu tiên tốc độ đọc/thao tác (đúng nguyên tắc ¶1):

  | Vai trò | Mã màu | Áp dụng |
  |---|---|---|
  | Nền vùng nội dung chính (bảng, form, khu làm việc) | `#FFFFFF` / `#FAFAFA` | Toàn bộ khu vực nội dung các màn hình |
  | Nền Sidebar / Topbar | `#FAF6EE` | Khung điều hướng (mục này) |
  | Accent (màu nhấn chính) | `#A6192E` | Nút hành động chính (CTA), trạng thái active trên Sidebar, logo, link văn bản (hyperlink) trong toàn ứng dụng (vd. "Quên mật khẩu?" ở D-ADM-001 (¶4.1)) |
  | Chữ chính | `#241C15` | Toàn bộ văn bản chính |
  | Chữ phụ | `#7A7166` | Văn bản phụ/mô tả |
  | Chữ trên nền Accent | `#FFFFFF` | Mọi chữ/icon đặt trên nền `#A6192E` (nút CTA, mục active trên Sidebar nếu dùng nền Accent, badge thương hiệu…) — không dùng Chữ chính/Chữ phụ trên nền Accent |
  | Viền / divider | `#E7DECD` (trên nền kem) hoặc xám nhạt trung tính (trên nền trắng) | Sidebar/Topbar vs. vùng nội dung |

  Badge trạng thái (xem bullet "Thành phần dùng lại nhiều nơi" bên dưới) dùng bảng màu ngữ nghĩa chuẩn (xanh lá/vàng/đỏ/xanh dương theo convention Quasar) — không theo bảng màu thương hiệu ở trên, để đảm bảo nhận diện mức độ trạng thái rõ ràng, nhất quán.

  **Quy tắc tương phản chữ/nền**: trên nền `#FAF6EE`/`#FFFFFF`/`#FAFAFA` chỉ dùng Chữ chính/Chữ phụ/Accent, **không dùng `#FFFFFF`**; trên nền `#A6192E` chỉ dùng `#FFFFFF`. Các cặp màu phát sinh ngoài bảng trên đạt tối thiểu 4.5:1 (WCAG 2.1 AA) với chữ thường, 3:1 với chữ ≥ 18px hoặc đậm ≥ 14px và icon. Với component Quasar có sẵn cặp màu nền/chữ mặc định (`QHeader`/`QToolbar` mặc định `bg-primary text-white`, `QBtn` unelevated…), khi đổi màu nền thì phải đặt lại cả màu chữ theo quy tắc này, không để giá trị mặc định.
- **Topbar**:
  - Màu: nền `#FAF6EE`, viền dưới `#E7DECD`. Tên nhóm/module hiện tại và tên Nhân viên dùng Chữ chính `#241C15`, tên Tổ chức dùng Chữ phụ, logo và icon dùng Accent. **Không dùng chữ/icon `#FFFFFF` trên Topbar**: phải đặt lại cả màu chữ mặc định `text-white` lẫn màu nền mặc định `bg-primary` của `QHeader` (quy tắc tương phản ở Bảng màu).
  - Bên trái: **tên nhóm/module hiện tại** (ví dụ "Cơ sở dữ liệu văn hóa", cập nhật theo màn hình đang xem, giúp biết đang ở module nào trong tổng thể hệ thống dù đã cuộn sâu vào một màn hình chi tiết).
  - Bên phải: **nút tài khoản** — avatar (chữ cái đầu của tên) + tên Nhân viên + tên Tổ chức trực thuộc, kèm icon mũi tên xuống. Bấm mở **menu tài khoản** gồm:
    - Phần đầu (không bấm được): tên Nhân viên, email, tên Tổ chức.
    - "Đổi mật khẩu" (icon khoá) → mở dialog D-ADM-027 (¶4.27).
    - Divider.
    - "Đăng xuất" (icon thoát) → hành vi theo bullet "Đăng xuất & phiên đăng nhập" bên dưới.
  - Menu tài khoản hiện cho mọi Nhân viên đã đăng nhập, không phụ thuộc role.
- **Đăng xuất & phiên đăng nhập**:
  - Bấm "Đăng xuất" trong menu tài khoản thực hiện ngay, không hộp thoại xác nhận (không mất dữ liệu đã lưu). Trình tự: gọi `POST /auth/logout` (thu hồi refresh token của phiên hiện tại — D-SD02-004 (¶3.2) bước 7) → xoá access/refresh token và store Pinia phía client → xoá hội thoại AI lưu tạm của Nhân viên này (D-ADM-023 (¶4.23)) → điều hướng về D-ADM-001 (¶4.1).
  - Nếu `POST /auth/logout` lỗi (mất mạng, token đã hết hạn…), client vẫn xoá dữ liệu phiên cục bộ và về D-ADM-001 (¶4.1) — người dùng không bị kẹt ở trạng thái đăng nhập.
  - Hết phiên ngoài ý muốn — client phân biệt 2 loại HTTP 401:
    - **401 do access token hết hạn**: gọi `POST /auth/refresh` một lần. Refresh thành công thì gửi lại request ban đầu. Refresh thất bại (refresh token hết hạn hoặc bị thu hồi, hoặc `/auth/refresh` trả `session_revoked`) thì xử lý như dòng dưới.
    - **401 `session_revoked`** (D-SD02-007 (¶3.5) — tài khoản bị vô hiệu hoá, mật khẩu vừa được đổi/đặt lại ở thiết bị khác, hoặc bị tạm khoá khi đổi mật khẩu): **không gọi `/auth/refresh`**. Xử lý ngay như Đăng xuất (bỏ qua bước gọi `POST /auth/logout`): xoá access/refresh token, store Pinia, hội thoại AI lưu tạm (D-ADM-023 (¶4.23)), rồi về D-ADM-001 (¶4.1).
    - Cả hai trường hợp: về D-ADM-001 (¶4.1) kèm thông báo "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Sau khi đăng nhập lại, điều hướng về đúng màn hình trước đó (nếu Nhân viên vẫn có quyền truy cập), không phải D-ADM-022 (¶4.22). Nhiều request cùng nhận 401 một lúc chỉ kích hoạt một lần làm mới phiên/một lần chuyển về D-ADM-001 (¶4.1).
    - Form đang chỉnh sửa dở không được giữ lại khi phiên kết thúc ngoài ý muốn (không hiện hộp thoại "Thay đổi chưa lưu").
  - Có form đang chỉnh sửa dở (ví dụ TipTap ở D-ADM-017 (¶4.17), form Phát biểu ở D-ADM-013 (¶4.13)) khi bấm Đăng xuất: hộp thoại "Thay đổi chưa lưu sẽ bị mất. Vẫn đăng xuất?" — theo cùng cơ chế cảnh báo rời trang của màn hình đó.
- **Sidebar**: mục **"Tổng quan"** (→ D-ADM-022 (¶4.22)) luôn ở đầu danh sách, hiện cho mọi Nhân viên đã đăng nhập, là trang mặc định điều hướng tới ngay sau khi đăng nhập thành công (bổ sung 2026-09-23). Mục đang chọn (khớp route hiện tại) được **highlight rõ** (nền/màu chữ khác — bổ sung 2026-09-23), kể cả khi đang ở màn hình chi tiết lồng sâu (vd D-ADM-013 (¶4.13)) thì mục cha tương ứng ở Sidebar (Hạng mục tri thức) vẫn được highlight. Các nhóm còn lại ẩn/hiện theo role hiện có của Nhân viên đăng nhập (không chỉ chặn API, ẩn cả trên menu):
  - Nhóm **"Người dùng & Tổ chức"** — chỉ hiện nếu có role `quan_tri_he_thong`: Nhân viên, Tổ chức.
  - Nhóm **"Cơ sở dữ liệu văn hóa"** — hiện nếu có bất kỳ role nào trong `nhap_lieu`/`nghien_cuu`/`xet_duyet`/`xuat_ban`/`chu_nhiem_de_tai`/`quan_tri_he_thong`: Đề tài nghiên cứu, Tư liệu gốc (mục Tư liệu gốc chỉ hiện với `nhap_lieu`/`quan_tri_he_thong`), Hạng mục tri thức (mục Hạng mục tri thức chỉ hiện với `nghien_cuu`/`xet_duyet`/`quan_tri_he_thong` — Chủ nhiệm đề tài đơn thuần xem tiến độ qua khối riêng ở D-ADM-009 (¶4.9), không có quyền vào danh sách/chi tiết Hạng mục tri thức).
  - Nhóm **"Bách khoa toàn thư"** — hiện nếu có role `bien_tap`/`xet_duyet_muc_tu`/`xuat_ban_muc_tu`: Mục từ, Cương vực.
  - Nhóm **"Trợ lý AI"** — hiện cho mọi Nhân viên đã đăng nhập: Hỏi AI Văn Minh Việt (mọi Nhân viên), Hỏi–đáp AI (chỉ hiện với `quan_tri_he_thong`).
  - Nhóm **"Giám sát"** — chỉ hiện nếu có role `quan_tri_he_thong`: Nhật ký hoạt động, Job nền.
  - Nhóm **"Hệ thống"** — chỉ hiện nếu có role `quan_tri_he_thong`: Cấu hình hệ thống.
  - Thứ tự nhóm trên Sidebar: Tổng quan → Người dùng & Tổ chức → Cơ sở dữ liệu văn hóa → Bách khoa toàn thư → Trợ lý AI → Giám sát → Hệ thống.
  - `quan_tri_he_thong` luôn thấy toàn bộ Đề tài nghiên cứu/Hạng mục tri thức (chỉ xem, R-KB-007 (§2.2.1.5)) dù không có role Nghiên cứu/Xét duyệt.
- **Breadcrumb** (bổ sung 2026-09-23): mọi màn hình con (trừ Đăng nhập/Quên mật khẩu/Đặt mật khẩu lần đầu và Dashboard) hiển thị chuỗi breadcrumb đầy đủ theo cây phân cấp ở đầu trang, ngay dưới Topbar — mỗi cấp là link về màn hình tương ứng, trừ cấp cuối (trang hiện tại, không phải link). Breadcrumb cụ thể cho từng màn hình ghi ở từng màn hình tương ứng.
- **Stepper trạng thái** (bổ sung 2026-09-23): áp dụng cho 2 entity có luồng trạng thái nhiều bước — Hạng mục tri thức (D-ADM-013 (¶4.13)/D-ADM-014 (¶4.14)/D-ADM-015 (¶4.15)) và Mục từ (D-ADM-017 (¶4.17)/D-ADM-018 (¶4.18)/D-ADM-019 (¶4.19)). Hiển thị ngay dưới Breadcrumb, dạng thanh ngang gồm các **cụm giai đoạn** (gộp nhóm các mã trạng thái con cùng bản chất, không liệt kê từng mã), điểm đang active tương ứng trạng thái hiện tại của bản soạn thảo:
  - Hạng mục tri thức (5 cụm): Nghiên cứu (`dang_nghien_cuu`) → Chờ & Xác minh AI (`cho_xet_duyet`, `dang_xet_duyet_ai`) → Xét duyệt chuyên gia (`da_qua_xet_duyet_ai`, `dang_xet_duyet`) → Đạt xét duyệt (`dat_xet_duyet`) → Xuất bản (`da_xuat_ban`/`khong_xuat_ban`, thể hiện 2 nhánh kết quả bằng 1 điểm chung có nhãn phụ theo giá trị thực tế).
  - Mục từ (4 cụm): Soạn thảo (`soan_thao`) → Chờ & Xét duyệt (`cho_xet_duyet`, `dang_xet_duyet`) → Đạt xét duyệt (`dat_xet_duyet`) → Xuất bản (`da_xuat_ban`/`khong_xuat_ban`).
  - Nhánh "Không đạt xét duyệt" (`khong_dat_xet_duyet`) thể hiện bằng một mũi tên cong nối từ cụm "Xét duyệt"/"Chờ & Xét duyệt" quay lại cụm đầu tiên, kèm nhãn — **không** phải một điểm riêng trên trục chính, vì đây là luồng có thể lặp lại nhiều vòng, không tuyến tính tuyệt đối. Tương tự, việc "Mở lại" từ `da_xuat_ban`/`khong_xuat_ban` về một trạng thái trước đó cũng thể hiện bằng mũi tên quay lại, không vẽ lại toàn bộ trục.
  - Stepper chỉ mang tính hiển thị định hướng, không thay thế các nút hành động đã có ở màn hình tương ứng.
- **Thành phần dùng lại nhiều nơi**: badge trạng thái (màu theo `status`), bảng danh sách có cursor-pagination + filter, khối "Người phụ trách" (hiện tên người đang giữ + nút Nhận xử lý/Nhả tuỳ quyền, cùng nút Cưỡng chế nhả riêng cho `quan_tri_he_thong` khi đang có người phụ trách), bộ chọn vị trí trong file tuỳ theo `file_type` (page/line cho văn bản, vẽ khung cho ảnh, kéo mốc thời gian cho âm thanh/phim — dùng chung cho Tham chiếu tới Tư liệu gốc và Vị trí trong Nội dung, cả ở chế độ chọn và chế độ chỉ xem/highlight).
- **Mức độ đặc tả hành vi cho từng thao tác**: chỉ mô tả rõ nội dung hộp thoại xác nhận/cảnh báo cho các hành động (a) đặc tả gốc yêu cầu cảnh báo rõ (ví dụ "Không xuất bản"), (b) không thể hoàn tác hoặc ảnh hưởng người khác (Cưỡng chế nhả, Xuất bản, Xoá, Khoá/Disable Nhân viên), (c) trạng thái khoá nội dung — cần thể hiện rõ lý do khoá trên UI (banner/tooltip), không chỉ ẩn/mờ nút, (d) cảnh báo dữ liệu bất thường (file `is_missing`, nội dung Mục từ đã lỗi thời so với Hạng mục tri thức nguồn). Các hành vi UI thông thường khác (validate trường bắt buộc, trạng thái loading, toast thành công...) theo convention chuẩn của Quasar, không đặc tả riêng cho từng màn hình.

## 4.1. [D-ADM-001] Đăng nhập

- Form giữa màn hình: input Email, input Mật khẩu, nút "Đăng nhập", link "Quên mật khẩu?".
- Không có lựa chọn "Đăng ký" — Nhân viên không tự tạo tài khoản (R-ID-018 (§2.1.5.2) đặc tả gốc).
- Lỗi hiển thị dùng chung một thông báo ("Email hoặc mật khẩu không đúng") dù sai lý do gì (email không tồn tại/sai mật khẩu/tài khoản `invited`/`disabled` xử lý riêng theo thông báo tương ứng — xem D-SD02-004 (¶3.2)).
- Đăng nhập thành công điều hướng tới D-ADM-022 (¶4.22) (Tổng quan) — không có Breadcrumb (nhóm Xác thực).
- Thông báo dạng banner thông tin phía trên form khi được điều hướng về từ: hết phiên hoặc phiên bị thu hồi (D-ADM-029 (¶3) — "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại"), đổi mật khẩu thành công (D-ADM-027 (¶4.27) — "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới"), bị tạm khoá khi đổi mật khẩu (D-ADM-027 (¶4.27) — "Tài khoản đang tạm khoá do nhập sai mật khẩu nhiều lần. Thử lại sau {locked_until}."). Đăng xuất chủ động không hiện thông báo.
- Vai trò truy cập: không cần đăng nhập. API: `POST /auth/login`.

## 4.2. [D-ADM-002] Quên mật khẩu / Đặt lại mật khẩu

- **Bước 1 — Quên mật khẩu**: input Email, nút gửi. Sau khi gửi luôn hiện cùng một thông báo ("Nếu email tồn tại, một link đặt lại mật khẩu đã được gửi") bất kể email có tồn tại hay không (D-SD02-005 (¶3.3)).
- **Bước 2 — Đặt lại mật khẩu** (mở từ link trong email): input Mật khẩu mới + Xác nhận mật khẩu, nút "Đặt lại mật khẩu". Token sai/hết hạn/đã dùng → báo lỗi, hướng dẫn liên hệ Quản trị hệ thống.
- API: `POST /auth/forgot-password`, `POST /auth/reset-password`.

## 4.3. [D-ADM-003] Đặt mật khẩu lần đầu (từ lời mời)

- Mở từ link mời trong email → gọi `GET /auth/invite/{token}` để xác thực trước, hiện email (readonly) nếu hợp lệ.
- Input Mật khẩu mới + Xác nhận, nút "Kích hoạt tài khoản". Token sai/hết hạn/đã dùng → báo lỗi tương tự D-ADM-002 (¶4.2).
- API: `GET /auth/invite/{token}`, `POST /auth/accept-invite`.

## 4.4. [D-ADM-004] Danh sách Nhân viên

- Breadcrumb: Người dùng & Tổ chức > Nhân viên.
- Bảng: Tên, Email, Tổ chức, Trạng thái (badge `invited`/`active`/`disabled`; khi `locked_until` > hiện tại, hiện thêm badge cam "Tạm khoá đến {locked_until}" — R-ID-030 (§2.1.5.9)), Role đang giữ (dạng chip, có thể nhiều).
- Filter: theo Tổ chức, theo Trạng thái; tìm theo tên/email.
- Nút "+ Tạo Nhân viên" → mở màn hình D-ADM-005 (¶4.5).
- Action inline theo dòng: "Gửi lại lời mời" (chỉ hiện khi `status = invited`), "Vô hiệu hoá" (khi `active`) / "Kích hoạt lại" (khi `disabled`) (R-ID-024 (§2.1.5.7)). Cả hai cần hộp thoại xác nhận vì ảnh hưởng trực tiếp quyền truy cập của Nhân viên đó (quy ước (b) D-ADM-029 (¶3)):
  - Vô hiệu hoá: "Vô hiệu hoá tài khoản {Tên}? Nhân viên này sẽ **bị đăng xuất ngay khỏi mọi thiết bị** và không đăng nhập được cho tới khi được kích hoạt lại. Role và các Hạng mục tri thức/Mục từ đang phụ trách được giữ nguyên — dùng Cưỡng chế nhả nếu cần giao lại cho người khác. Tiếp tục?" (R-ID-025 (§2.1.5.7.1)–R-ID-027 (§2.1.5.7.3)).
  - Kích hoạt lại: "Kích hoạt lại tài khoản {Tên}? Nhân viên đăng nhập lại bằng mật khẩu và các role cũ. Tiếp tục?" (R-ID-026 (§2.1.5.7.2)).
- Action "Gỡ tạm khoá" — chỉ hiện khi `locked_until` > hiện tại (R-ID-032 (§2.1.5.9.2)): xác nhận ngắn "Gỡ tạm khoá đăng nhập cho {Tên}? Nhân viên đăng nhập lại được ngay." → `POST /identity/employees/{id}/clear-login-lock`; thành công thì tải lại dòng.
- Nhãn badge Trạng thái: `invited` "Đã mời", `active` "Đang hoạt động", `disabled` "Đã vô hiệu hoá" — "Vô hiệu hoá" (R-ID-024 (§2.1.5.7)) khác "tạm khoá đăng nhập" (R-ID-033 (§2.1.5.9.3)).
- API: `GET /identity/employees`, `POST .../resend-invite`, `POST .../disable`, `POST .../enable`, `POST .../clear-login-lock`.
- Quyền truy cập: chỉ role `quan_tri_he_thong`.

## 4.5. [D-ADM-005] Tạo/sửa Nhân viên

- Breadcrumb: Người dùng & Tổ chức > Nhân viên > {Tên Nhân viên} (hoặc "Tạo mới" khi chưa có tên).
- Form: Tên gọi, Email, Số điện thoại, chọn Tổ chức (dropdown).
- **Email không sửa được sau khi tạo** — vì là định danh đăng nhập, và API `PATCH /identity/employees/{id}` chỉ nhận `display_name`/`phone`/`organization_id` (D-SD02-010 (¶5.2)). Ở màn hình sửa, field Email hiển thị readonly.
- Khối gán **Role theo chức năng**: multi-select trong danh sách role cố định (`nhap_lieu`, `xuat_ban`, `xuat_ban_muc_tu`, `bien_tap`, `xet_duyet_muc_tu`, `van_hanh`, `quan_tri_he_thong`).
- Role theo phạm vi Đề tài nghiên cứu (Chủ nhiệm đề tài, Nghiên cứu, Xét duyệt — R-KB-073 (§2.2.5.5)/R-KB-070 (§2.2.5.2)/R-KB-071 (§2.2.5.3)) được gán tại màn hình D-ADM-009 (¶4.9) (Chi tiết Đề tài nghiên cứu), qua các endpoint `research-topics/{id}/set-chair`, `.../researchers`, `.../reviewers`. Màn hình này chỉ gán role theo chức năng.
- Submit khi tạo mới: tạo Nhân viên trạng thái `invited`, gửi email mời — toast "Đã tạo Nhân viên và gửi email mời".
- API: `POST /identity/employees`, `PATCH /identity/employees/{id}`, `POST/DELETE /identity/employees/{id}/roles` (nay chỉ dùng cho role theo chức năng).

## 4.6. [D-ADM-006] Danh sách Tổ chức

- Breadcrumb: Người dùng & Tổ chức > Tổ chức.
- Bảng: Tên, Địa chỉ, Email liên hệ, SĐT liên hệ, số Nhân viên trực thuộc.
- Nút "+ Tạo Tổ chức" → mở D-ADM-007 (¶4.7). Click dòng → mở D-ADM-007 (¶4.7) ở chế độ sửa.
- Không có chức năng xoá Tổ chức (không có endpoint xoá cứng — D-SD02-010 (¶5.2)).
- API: `GET /identity/organizations`. Quyền: chỉ `quan_tri_he_thong`.

## 4.7. [D-ADM-007] Tạo/sửa Tổ chức

- Breadcrumb: Người dùng & Tổ chức > Tổ chức > {Tên Tổ chức} (hoặc "Tạo mới").
- Form: Tên tổ chức, Địa chỉ, Email liên hệ, Số điện thoại liên hệ.
- API: `POST /identity/organizations`, `PATCH /identity/organizations/{id}`.

## 4.8. [D-ADM-008] Danh sách Đề tài nghiên cứu

- Breadcrumb: Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu.
- Bảng: Tên, Trạng thái (badge `chuan_bi_tu_lieu`/`tu_lieu_san_sang`), Chủ nhiệm đề tài (tên hoặc "Chưa gán"), Số Tư liệu gốc đã gán, Số Hạng mục tri thức (tổng), Ngày tạo.
- Filter: theo Trạng thái; tìm theo tên.
- Nút "+ Tạo Đề tài nghiên cứu" — chỉ hiện với role `quan_tri_he_thong` (R-KB-006 (§2.2.1.4)) — mở dialog đơn giản (chỉ nhập Tên), submit xong điều hướng sang D-ADM-009 (¶4.9) để tiếp tục gán Tư liệu gốc.
- Action inline theo dòng: "Xoá" (R-KB-012 (§2.2.1.7)) — chỉ role `quan_tri_he_thong`; disable kèm tooltip "Đề tài còn Hạng mục tri thức, không xoá được" khi Số Hạng mục tri thức > 0 (điều kiện rỗng); khi đủ điều kiện, hộp thoại xác nhận (không hoàn tác, ảnh hưởng vai trò đã gán — quy ước (b) D-ADM-029 (¶3)): "Xoá Đề tài nghiên cứu này sẽ gỡ luôn các vai trò Chủ nhiệm đề tài/Nghiên cứu/Xét duyệt đã gán. Tư liệu gốc đã gán không bị xoá, chỉ gỡ khỏi danh sách của đề tài. Không thể hoàn tác. Tiếp tục?" (R-KB-013 (§2.2.1.7.1)–R-KB-016 (§2.2.1.7.4)).
- Click dòng → mở D-ADM-009 (¶4.9).
- Phạm vi hiển thị: `quan_tri_he_thong` thấy toàn bộ (D-SD03-014 (¶3.5)); Nhân viên khác chỉ thấy đề tài mình được gán **ít nhất một trong** role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` (D-SD03-021 (¶5.1)).
- API: `GET /knowledge/research-topics`, `POST /knowledge/research-topics`, `DELETE /knowledge/research-topics/{id}`.
- Quyền truy cập: role `nhap_lieu`/`nghien_cuu`/`xet_duyet`/`xuat_ban`/`chu_nhiem_de_tai`/`quan_tri_he_thong`.

## 4.9. [D-ADM-009] Chi tiết Đề tài nghiên cứu

- Breadcrumb: Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu > {Tên đề tài}.
- Header: Tên, badge Trạng thái, nút "Xoá" (chỉ `quan_tri_he_thong`; disable kèm tooltip khi còn Hạng mục tri thức — cùng điều kiện/cảnh báo như action "Xoá" ở D-ADM-008 (¶4.8), R-KB-012 (§2.2.1.7)).
- Nút "Đánh dấu Tư liệu sẵn sàng" — chỉ hiện khi `status = chuan_bi_tu_lieu`, chỉ role `nhap_lieu`/`quan_tri_he_thong`; hộp thoại xác nhận vì đây là chuyển tiếp một chiều, không quay lại được (R-KB-011 (§2.2.1.6.2)): "Sau khi xác nhận, đề tài sẽ mở khoá tạo Hạng mục tri thức cho vai trò Nghiên cứu và không thể quay lại trạng thái Chuẩn bị tư liệu. Tiếp tục?".
- Khối "Chủ nhiệm đề tài" (R-KB-073 (§2.2.5.5)): hiện tên Nhân viên đang giữ (hoặc "Chưa gán"), nút "Đổi Chủ nhiệm" — chỉ `quan_tri_he_thong` — mở dialog tìm/chọn 1 Nhân viên (không giới hạn Tổ chức, R-KB-073 (§2.2.5.5) — có thể thuộc bất kỳ Tổ chức nào), xác nhận vì thay thế người cũ (nếu có): "Đổi Chủ nhiệm đề tài sẽ thay thế người đang giữ hiện tại (nếu có). Tiếp tục?" → `POST .../set-chair`.
- Khối "Quản lý nhân sự đề tài" (Nghiên cứu/Xét duyệt, R-KB-006 (§2.2.1.4)): 2 bảng con "Nghiên cứu" và "Xét duyệt", mỗi bảng liệt kê Nhân viên đang giữ role tương ứng của đề tài này + nút "Gỡ" từng dòng, cùng ô tìm/thêm Nhân viên (không giới hạn Tổ chức). Quyền thao tác: `quan_tri_he_thong` **hoặc** Nhân viên đang giữ Chủ nhiệm đề tài của chính đề tài này (R-KB-006 (§2.2.1.4)) — người xem khác chỉ đọc. API: `GET .../members`, `POST/DELETE .../researchers`, `POST/DELETE .../reviewers`.
- Khối "Tư liệu gốc đã gán": bảng (Tên, Loại, cảnh báo nếu có file `is_missing`), nút "Gỡ" từng dòng (`DELETE .../sources/{source_id}`), ô tìm/gán thêm Tư liệu gốc có sẵn (`POST .../sources`) — gán được bất kỳ lúc nào, kể cả sau `tu_lieu_san_sang` (R-KB-005 (§2.2.1.3)). Chỉ role `nhap_lieu`/`quan_tri_he_thong` thao tác được, các role khác chỉ xem.
- Khối "Hạng mục tri thức":
  - Nếu người xem có role `nghien_cuu`/`xet_duyet` của đề tài này, hoặc là `quan_tri_he_thong`: hiển thị đầy đủ — thống kê số lượng theo từng trạng thái (chip đếm), link mở D-ADM-012 (¶4.12) đã lọc sẵn theo đề tài này.
  - Nếu người xem **chỉ** giữ Chủ nhiệm đề tài (không có Nghiên cứu/Xét duyệt của đề tài này): hiển thị bản rút gọn qua `GET .../progress` (R-KB-073 (§2.2.5.5)/R-PTN-009 (§2.7.3.5)) — thống kê theo trạng thái + bảng danh sách chỉ gồm Tiêu đề/Trạng thái/Người phụ trách/Người tạo, **không** link mở D-ADM-012 (¶4.12)/D-ADM-013 (¶4.13) (không có quyền xem Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt).
- API: `GET /knowledge/research-topics/{id}`, `POST/DELETE /knowledge/research-topics/{id}/sources`, `POST /knowledge/research-topics/{id}/mark-ready`, `DELETE /knowledge/research-topics/{id}`, `POST .../set-chair`, `GET .../members`, `POST/DELETE .../researchers`, `POST/DELETE .../reviewers`, `GET .../progress`.

## 4.10. [D-ADM-010] Danh sách Tư liệu gốc

- Breadcrumb: Cơ sở dữ liệu văn hóa > Tư liệu gốc.
- Chỉ mount `admin` (D-SD03-022 (¶5.2)) — vai trò Nhập liệu là Nhân viên Tổ chức Văn Minh Việt, không tồn tại ở `partner`.
- Bảng: Tên, Loại (`type`), đường dẫn thư mục (`storage_prefix`), Lần đồng bộ gần nhất (`last_synced_at`), cảnh báo nếu có `source_file.is_missing = true` trong tư liệu (badge đỏ).
- Filter: theo Loại; tìm theo tên.
- Nút "+ Tạo Tư liệu gốc" → dialog: Tên, Loại, đường dẫn thư mục (`storage_prefix`, đã có sẵn file trong MinIO/S3 — việc nạp file nằm ngoài hệ thống, R-KB-017 (§2.2.2)/D-SD03-020 (¶4.5)).
- Click dòng → mở D-ADM-011 (¶4.11).
- API: `GET /knowledge/sources`, `POST /knowledge/sources`.
- Quyền truy cập: role `nhap_lieu`/`quan_tri_he_thong`.

## 4.11. [D-ADM-011] Chi tiết Tư liệu gốc

- Breadcrumb: Cơ sở dữ liệu văn hóa > Tư liệu gốc > {Tên tư liệu}.
- Header: Tên, Loại, đường dẫn thư mục, Lần đồng bộ gần nhất.
- Nút "Đồng bộ lại" (`POST .../sync`) — chạy đồng bộ thủ công không qua debounce (D-SD03-020 (¶4.5)); nếu đang có lần đồng bộ khác chạy (advisory lock), hiện thông báo "Đang có lượt đồng bộ khác đang chạy, thử lại sau" thay vì chờ.
- Bảng file (`source_file`): Loại file, đường dẫn lưu trữ, Trạng thái (badge "Còn file" / cảnh báo đỏ "Không tìm thấy file" kèm tooltip thời điểm phát hiện mất — `missing_since`, theo quy ước (c) D-ADM-029 (¶3)), Metadata (số trang/kích thước/độ dài tuỳ loại, hiển thị gọn), có transcript hay không (icon).
- Không có thao tác thêm/sửa/xoá file thủ công trên màn hình này — file chỉ đến từ đồng bộ MinIO/S3 (D-SD03-020 (¶4.5)); chỉ đọc, trừ nút "Đồng bộ lại" ở trên.
- API: `GET /knowledge/sources/{id}`, `POST /knowledge/sources/{id}/sync`.

## 4.12. [D-ADM-012] Danh sách Hạng mục tri thức

- Breadcrumb: nếu vào từ Sidebar (không lọc theo đề tài): Cơ sở dữ liệu văn hóa > Hạng mục tri thức. Nếu vào từ link ở D-ADM-009 (¶4.9) (đã lọc theo 1 đề tài): Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức.
- Bảng: Tiêu đề, Đề tài nghiên cứu, Trạng thái (badge, 9 mã, gồm cả `dang_xet_duyet_ai` — D-SD03-011 (¶3.2)), Người phụ trách (`assignee_id` — tên hoặc "Chưa có"), **Người tạo** (`created_by`, R-KB-047 (§2.2.3.12)), cảnh báo nếu `has_missing_source_files = true`, Ngày tạo (R-KB-048 (§2.2.3.13)).
- Filter: theo Đề tài nghiên cứu, theo Trạng thái.
- Nút "+ Tạo Hạng mục tri thức" — chỉ hiện khi Nhân viên đang giữ role `nghien_cuu` của ít nhất một Đề tài nghiên cứu đang `tu_lieu_san_sang`; dialog chọn Đề tài nghiên cứu (chỉ liệt kê đề tài thoả điều kiện trên) + nhập Tiêu đề. Submit xong điều hướng sang D-ADM-013 (¶4.13).
- Action inline theo dòng: "Xoá" (R-KB-049 (§2.2.3.14)) — chỉ enable khi `status = dang_nghien_cuu`, disable kèm tooltip "Chỉ xoá được khi đang ở trạng thái Đang nghiên cứu" ở trạng thái khác; hiện với `quan_tri_he_thong`, Chủ nhiệm đề tài của đề tài cha, hoặc `assignee_id` hiện tại (R-KB-053 (§2.2.3.14.4) — khi chưa có Người phụ trách, chỉ 2 vai trò đầu thấy nút này). Hộp thoại xác nhận (không hoàn tác — quy ước (b) D-ADM-029 (¶3)): "Xoá sẽ xoá vĩnh viễn Nội dung/Phát biểu/Tham chiếu của Hạng mục tri thức này. Tư liệu gốc không bị ảnh hưởng. Tiếp tục?"; nếu backend từ chối (đã có phiên bản chốt hoặc đã bị Mục từ tham chiếu), hiện thông báo lỗi tương ứng.
- Click dòng → điều hướng theo `status`: `dang_nghien_cuu`/`cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet` → D-ADM-013 (¶4.13); `da_qua_xet_duyet_ai`/`dang_xet_duyet` → D-ADM-014 (¶4.14); `dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban` → D-ADM-015 (¶4.15).
- API: `GET /knowledge/knowledge-objects`, `POST /knowledge/knowledge-objects`, `DELETE /knowledge/knowledge-objects/{id}`.
- Quyền truy cập: `admin`+`partner` (theo phạm vi đề tài được gán); `quan_tri_he_thong` xem toàn bộ không lọc (D-SD03-014 (¶3.5)), chỉ đọc trừ khi được gán thêm role.

## 4.13. [D-ADM-013] Màn hình Nghiên cứu (biên tập Hạng mục tri thức)

- Breadcrumb: Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3), 5 cụm): active tại cụm "Nghiên cứu" (khi `dang_nghien_cuu`) hoặc "Chờ & Xác minh AI" (khi `cho_xet_duyet`/`dang_xet_duyet_ai`); nếu `khong_dat_xet_duyet`, active vẫn ở cụm "Nghiên cứu" kèm mũi tên quay lại từ cụm "Xét duyệt chuyên gia".
- Áp dụng khi Hạng mục tri thức đang ở `dang_nghien_cuu`, `cho_xet_duyet`, `dang_xet_duyet_ai`, hoặc `khong_dat_xet_duyet` (D-SD03-012 (¶3.3) bước (1)(2)(3)(7)).
- Header: Tiêu đề, badge Trạng thái.
- Khối "Người phụ trách" (component dùng chung, D-ADM-029 (¶3)): tên đang giữ (nếu có) + nút "Nhận xử lý" (`Claim`, hiện khi `assignee_id` đang trống và người xem giữ role `nghien_cuu` của đề tài) / "Nhả" (`Release`, hiện khi `assignee_id` = người xem) / "Cưỡng chế nhả" (`ForceRelease`, chỉ role `quan_tri_he_thong`, hiện khi `assignee_id` đang có giá trị — hộp thoại xác nhận vì ảnh hưởng người khác, quy ước (b) D-ADM-029 (¶3): "Cưỡng chế nhả sẽ gỡ Người phụ trách hiện tại khỏi Hạng mục tri thức này. Tiếp tục?", R-KB-046 (§2.2.3.11.5)).
- Khối Nội dung (`knowledge_object_file`, R-KB-032 (§2.2.3.6) — sản phẩm biên tập của vai trò Nghiên cứu, khác Tư liệu gốc): danh sách file đã tải lên (tên, loại, kích thước, nút xem/tải), nút "+ Tải file lên" (upload trực tiếp qua presigned URL, không phải trình soạn thảo trực tuyến — D-SD03-007 (¶2.7)).
  - Chỉnh sửa (tải lên/gỡ file, thêm/sửa/xoá Phát biểu & Tham chiếu) chỉ mở khi `status = dang_nghien_cuu` **và** người xem là `assignee_id` hiện tại — các trạng thái/người xem khác chỉ đọc, kèm banner nêu rõ lý do khoá (quy ước (c) D-ADM-029 (¶3): ví dụ "Đang chờ xét duyệt — chỉ Người phụ trách mới chỉnh sửa được" hoặc "Đang chạy AI Verification"). ⚠ Ghi chú thiết kế đi trước: theo `03-cultural-knowledge-base.md` mục "Ghi chú chung cho 2.7–2.9", tầng backend hiện chỉ khoá cứng ghi dữ liệu ở 4 trạng thái (`dang_xet_duyet`/`dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban`) và theo `assignee_id` khi `dang_nghien_cuu` — chưa khoá cứng ở `cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet`; việc ẩn nút chỉnh sửa ở các trạng thái này tại đây là lựa chọn UI, không phải do backend chặn.
- Khối Phát biểu (`claim`): bảng liệt kê nội dung, danh sách Tham chiếu (chip: Tư liệu gốc + vị trí) kèm cảnh báo nếu `source_file.is_missing = true`, Vị trí trong Nội dung (nếu có khai báo). Nút "+ Thêm Phát biểu" mở form: nội dung, chọn file Nội dung + bộ chọn vị trí (không bắt buộc), thêm một hoặc nhiều Tham chiếu (chọn Tư liệu gốc đã gán cho đề tài → chọn file → bộ chọn vị trí theo `file_type`: page/line cho văn bản, vẽ khung cho ảnh, kéo mốc thời gian cho âm thanh/phim — component dùng chung cho cả Tham chiếu và Vị trí trong Nội dung, D-SD03-007 (¶2.7)).
- Khối "Gợi ý AI" (`ai_missed_claims_suggestions`, R-KB-085 (§2.2.6.6.5)): chỉ đọc, hiện khi có dữ liệu — danh sách gợi ý phát biểu có thể bị bỏ sót, chỉ mang tính tham khảo.
- Vùng trạng thái/hành động cuối trang theo `status`:
  - `dang_nghien_cuu`: nút "Gửi xét duyệt" (`submit-for-review`, chỉ `assignee_id` hiện tại) — hạng mục có tự chạy AI Verification hay không tuỳ cấu hình `ai_verification.trigger_mode` (D-SD07-004 (¶3.1)); giao diện không đọc cấu hình này mà dựa vào `status` trả về: `dang_xet_duyet_ai` → toast "Đã gửi xét duyệt — AI Verification đang chạy"; `cho_xet_duyet` → toast "Đã gửi xét duyệt — chờ kích hoạt AI Verification"; nút "Xoá Hạng mục tri thức" (R-KB-049 (§2.2.3.14) — hiện với `quan_tri_he_thong`, Chủ nhiệm đề tài của đề tài cha, hoặc `assignee_id` hiện tại; khi chưa có Người phụ trách, chỉ 2 vai trò đầu thấy nút này, R-KB-053 (§2.2.3.14.4); hộp thoại xác nhận: "Xoá sẽ xoá vĩnh viễn Nội dung/Phát biểu/Tham chiếu của Hạng mục tri thức này. Tư liệu gốc không bị ảnh hưởng. Không thể hoàn tác. Tiếp tục?"; nếu backend từ chối do đã có phiên bản chốt hoặc đã bị Mục từ tham chiếu, hiện thông báo lỗi tương ứng).
  - `cho_xet_duyet`: hiện "Đang chờ kích hoạt AI Verification" (hạng mục dừng ở đây khi `trigger_mode = manual`, hoặc khi đã vào trạng thái này trước lúc chuyển `manual → auto` — D-SD07-004 (¶3.1)).
  - `dang_xet_duyet_ai`: hiện "Đang chạy AI Verification..." — chờ job nền `verification.run` (D-SD03-018 (¶4.3); theo dõi job ở D-ADM-026 (¶4.26)).
  - Cả `cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet`: nút kích hoạt AI Verification (`trigger-ai-verification`) — chỉ hiện khi `can_trigger_ai_verification = true` trong chi tiết Hạng mục tri thức (D-SD03-023 (¶5.3); backend tính theo `ai_verification.manual_trigger_roles` — role theo phạm vi chỉ tính với đúng Đề tài nghiên cứu cha — và trạng thái hiện tại, D-SD07-004 (¶3.1), D-SD03-012 (¶3.3) bước (3)); giao diện không tự kiểm role. Nhãn: "Kích hoạt AI Verification" tại `cho_xet_duyet`; "Kích hoạt lại AI Verification" tại `dang_xet_duyet_ai`/`khong_dat_xet_duyet`. Tại `dang_xet_duyet_ai`, nút này là đường khôi phục khi job AI Verification đã bị huỷ hoặc thất bại hẳn; nếu job của hạng mục vẫn đang chờ/đang chạy, backend không tạo job trùng — giao diện hiện thông báo "AI Verification đang chạy cho Hạng mục tri thức này".
  - `khong_dat_xet_duyet`: hiện ghi chú không đạt (`ai_note`/`expert_note` của các Tham chiếu/Vị trí liên quan, gộp lại một danh sách). Nút "Quay lại nghiên cứu" (`resume-research`, role `nghien_cuu` của đề tài — không giới hạn theo `assignee_id`, nhất quán với `submit-for-review`).
- API: `GET /knowledge/knowledge-objects/{id}`, `POST/DELETE .../files`, `POST/PATCH/DELETE .../claims`, `POST/DELETE .../claims/{claim_id}/references`, `POST .../submit-for-review`, `POST .../trigger-ai-verification`, `POST .../claim`, `POST .../release`, `POST .../force-release`, `POST .../resume-research`, `DELETE /knowledge/knowledge-objects/{id}`.

## 4.14. [D-ADM-014] Màn hình Xét duyệt Hạng mục tri thức (chuyên gia)

- Breadcrumb: Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3)): active tại cụm "Xét duyệt chuyên gia" (`da_qua_xet_duyet_ai`/`dang_xet_duyet`).
- Áp dụng khi Hạng mục tri thức đang ở `da_qua_xet_duyet_ai` (chưa ai nhận xử lý) hoặc `dang_xet_duyet` (chuyên gia đang xử lý — R-KB-087 (§2.2.6.8)).
- Header: Tiêu đề, badge Trạng thái. Banner "Nội dung bị khoá" khi `dang_xet_duyet` (quy ước (c) D-ADM-029 (¶3)).
- Khối "Người phụ trách": nút "Nhận xử lý" (`Claim`, hiện tại `da_qua_xet_duyet_ai`, role `xet_duyet` của đề tài — nhận xử lý là một lần "nhận" độc lập, ghi đè `assignee_id` không cần trống trước, đồng thời chuyển `status → dang_xet_duyet`) / "Nhả" (`Release`, chỉ `assignee_id` hiện tại, hiện tại `dang_xet_duyet`, lùi về `da_qua_xet_duyet_ai`) / "Cưỡng chế nhả" (`ForceRelease`, chỉ role `quan_tri_he_thong`, hiện tại `dang_xet_duyet` khi đang có `assignee_id` — hộp thoại xác nhận, cùng quy ước (b) D-ADM-029 (¶3), R-KB-046 (§2.2.3.11.5)).
- Khối Nội dung: xem file đã upload (đọc, không sửa).
- Khối Phát biểu — với mỗi Phát biểu, hiện từng Tham chiếu và Vị trí trong Nội dung (nếu có) kèm:
  - Vị trí trong Tư liệu gốc/Nội dung (mở file kèm highlight đúng vị trí — dùng lại bộ chọn vị trí ở chế độ chỉ xem).
  - Kết quả AI (`ai_verdict`/`ai_note` hoặc `content_ai_verdict`/`content_ai_note`) — chỉ đọc.
  - Cảnh báo nếu `source_file.is_missing = true` (banner đỏ ngay trên dòng Tham chiếu, quy ước (c) D-ADM-029 (¶3)).
  - Form ghi kết luận chuyên gia (`expert_verdict`/`expert_note` hoặc `content_expert_verdict`/`content_expert_note`) — chỉ hiện/enable khi `status = dang_xet_duyet` và người xem là `assignee_id` hiện tại.
- Khối "Gợi ý AI" — tham khảo, cùng cơ chế D-ADM-013 (¶4.13).
- Nút cuối trang (chỉ `assignee_id` hiện tại, tại `dang_xet_duyet`, sau khi đã thẩm định tổng thể — R-KB-090 (§2.2.6.8.3)): "Không đạt xét duyệt" (`reject` → `khong_dat_xet_duyet`) và "Đạt xét duyệt" (`approve` → `dat_xet_duyet`) — cả hai không có ràng buộc kỹ thuật bắt buộc phải đánh giá hết từng Tham chiếu trước khi bấm (đặc tả không yêu cầu), nhưng giao diện cảnh báo mềm (không chặn) nếu còn Tham chiếu/Vị trí chưa có `expert_verdict`.
- Nút "Kích hoạt lại AI Verification" — chỉ hiện tại `da_qua_xet_duyet_ai` (chưa `Claim`) khi `can_trigger_ai_verification = true` (cùng cơ chế D-ADM-013 (¶4.13)), không hiện tại `dang_xet_duyet` (D-SD03-012 (¶3.3) bước (3) không liệt kê `dang_xet_duyet` trong danh sách trạng thái được kích hoạt lại).
- API: `GET /knowledge/knowledge-objects/{id}`, `GET /knowledge/knowledge-objects/{id}/claims`, `POST .../claim`, `POST .../release`, `POST .../force-release`, `POST .../claims/{claim_id}/references/{reference_id}/review`, `POST .../claims/{claim_id}/content-review`, `POST .../reject`, `POST .../approve`, `POST .../trigger-ai-verification`.

## 4.15. [D-ADM-015] Màn hình Xuất bản Hạng mục tri thức

- Breadcrumb: Cơ sở dữ liệu văn hóa > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3)): active tại cụm "Đạt xét duyệt" (`dat_xet_duyet`) hoặc "Xuất bản" (`da_xuat_ban`/`khong_xuat_ban`, kèm nhãn phụ theo giá trị thực tế).
- Áp dụng khi Hạng mục tri thức đang ở `dat_xet_duyet`, `da_xuat_ban`, hoặc `khong_xuat_ban` (D-SD03-012 (¶3.3) bước (8)(9)(10)) — cả 3 trạng thái đều "Nội dung bị khoá" (banner, quy ước (c) D-ADM-029 (¶3)).
- Header: Tiêu đề, badge Trạng thái, Người phụ trách (chỉ hiển thị, không còn thao tác Nhận/Nhả ở nhóm trạng thái này).
- Khối Nội dung/Phát biểu: xem lại toàn bộ (đọc, tái dùng view của D-ADM-014 (¶4.14)) kèm kết quả xét duyệt AI + chuyên gia cuối cùng.
- Tại `dat_xet_duyet` — 2 quyết định bắt buộc, đúng một trong hai, chỉ role `xuat_ban` (R-KB-092 (§2.2.6.10)):
  - Nút "Xuất bản" (`publish`) — hộp thoại xác nhận (không hoàn tác, tạo phiên bản mới, ảnh hưởng người khác — quy ước (b) D-ADM-029 (¶3)): "Xuất bản sẽ tạo một phiên bản mới, chốt lại toàn bộ Nội dung/Phát biểu hiện tại. Tiếp tục?".
  - Nút "Không xuất bản" (`skip-publish`, body `{confirmed: true}`) — hộp thoại xác nhận bắt buộc (đặc tả yêu cầu cảnh báo rõ, R-KB-094 (§2.2.6.12)): "Không xuất bản: vòng xét duyệt này sẽ không tạo phiên bản nào để lưu lại. Tiếp tục?".
- Tại `da_xuat_ban`: hiện "Đã xuất bản lúc {frozen_at} bởi {frozen_by}", số phiên bản (`version_number`) vừa tạo.
- Tại `khong_xuat_ban`: hiện thời điểm chuyển trạng thái.
- Cả `da_xuat_ban`/`khong_xuat_ban`: nút "Mở lại" — **chỉ role `xet_duyet` của đề tài** (không phải role `xuat_ban` — R-KB-093 (§2.2.6.11)–R-KB-094 (§2.2.6.12)), mở dialog chọn trạng thái đích trong 4 lựa chọn (`dang_nghien_cuu`/`cho_xet_duyet`/`da_qua_xet_duyet_ai`/`dang_xet_duyet`) kèm cảnh báo không hoàn tác/ảnh hưởng người khác (quy ước (b) D-ADM-029 (¶3)): "Mở lại sẽ đưa Hạng mục tri thức quay lại quy trình xét duyệt, Người phụ trách hiện tại (nếu có) được giữ nguyên. Tiếp tục?" (`reopen`, body `{target_status}`).
- Khối "Lịch sử phiên bản" (độc lập với `status`, luôn hiện nếu đã có ít nhất 1 phiên bản chốt): bảng các phiên bản đã chốt (Số phiên bản, Thời điểm chốt, Người chốt), click 1 dòng → xem snapshot chỉ đọc (`GET .../versions/{version_id}`).
- Khối "Phiên bản đang được sử dụng" (D-SD03-013 (¶3.4) thao tác (b) — thao tác độc lập với `status`, luôn hiện nếu đã có ít nhất 1 phiên bản chốt, chỉ role `xuat_ban` thao tác): hiện phiên bản hiện đang dùng (`used_version_id`, hoặc "Chưa chọn"), nút "Chọn/Đổi phiên bản đang dùng" mở dialog chọn từ danh sách phiên bản đã chốt (không nhất thiết mới nhất) → `set-used-version`.
- API: `GET /knowledge/knowledge-objects/{id}`, `GET .../versions/{version_id}`, `POST .../publish`, `POST .../skip-publish`, `POST .../reopen`, `POST .../set-used-version`.

## 4.16. [D-ADM-016] Danh sách Mục từ

- Breadcrumb: Bách khoa toàn thư > Mục từ.
- Bảng: Tiêu đề, Trạng thái (badge, 7 mã — D-SD04-007 (¶3.1)), Người phụ trách, Cương vực (chip, có thể nhiều), Ngày tạo.
- Filter: theo Trạng thái, theo Cương vực; tìm theo tiêu đề.
- Nút "+ Tạo Mục từ" — chỉ role `bien_tap` — dialog: Tiêu đề + chọn một hoặc nhiều Hạng mục tri thức nguồn (ô tìm kiếm, gộp/tách theo R-ENC-017 (§2.3.3)). Submit xong điều hướng sang D-ADM-017 (¶4.17).
- Click dòng → điều hướng theo `status`: `soan_thao`/`cho_xet_duyet` → D-ADM-017 (¶4.17); `dang_xet_duyet` → D-ADM-018 (¶4.18); `dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban` → D-ADM-019 (¶4.19).
- API: `GET /encyclopedia/entries`, `POST /encyclopedia/entries`.
- Quyền truy cập: role `bien_tap`/`xet_duyet_muc_tu`/`xuat_ban_muc_tu`.

## 4.17. [D-ADM-017] Soạn thảo Mục từ (TipTap)

- Breadcrumb: Bách khoa toàn thư > Mục từ > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3), 4 cụm): active tại cụm "Soạn thảo" (`soan_thao`) hoặc "Chờ & Xét duyệt" (`cho_xet_duyet`); nếu `khong_dat_xet_duyet`, active vẫn ở cụm "Soạn thảo" kèm mũi tên quay lại từ cụm "Chờ & Xét duyệt".
- Áp dụng khi `status ∈ {soan_thao, cho_xet_duyet, khong_dat_xet_duyet}`.
- Header: Tiêu đề, badge Trạng thái.
- Khối "Người phụ trách": "Nhận xử lý"/"Nhả" (`Claim`/`Release`), cùng cơ chế D-ADM-013 (¶4.13); thêm "Cưỡng chế nhả" (`ForceRelease`, chỉ role `quan_tri_he_thong`, hiện tại `soan_thao` khi đang có `assignee_id` — hộp thoại xác nhận, quy ước (b) D-ADM-029 (¶3), R-ENC-016 (§2.3.2.5.5)).
- Khối "Hạng mục tri thức nguồn": danh sách Hạng mục tri thức đã gộp/tách vào Mục từ này, nút "Xem nội dung nguồn" (đọc `used_version` — tiêu đề, file, Phát biểu — chỉ tham khảo, qua `GetUsedVersionContent`), cảnh báo "Nội dung nguồn đã có phiên bản mới hơn" khi `used_version_id` khác `last_synced_version_id` (quy ước (d) D-ADM-029 (¶3)), nút "Đánh dấu đã đồng bộ" (`mark-synced`) để tắt cảnh báo sau khi đã cập nhật nội dung. Nút "+ Thêm"/"Gỡ" Hạng mục tri thức nguồn.
- Khối Nội dung: trình soạn thảo TipTap cho `content_blocks` (đoạn văn, tiêu đề phụ, chú thích, khối nhúng ảnh/âm thanh/phim — nhúng từ file đã tải lên ở khối Tệp đính kèm bên dưới).
- Khối "Tệp đính kèm" (`entry_file`): danh sách file đã tải lên, nút "+ Tải file lên" (presigned URL) — dùng để nhúng vào Nội dung.
- Khối "Cương vực": multi-select gán/gỡ (`AssignCulturalDomain`/`UnassignCulturalDomain`).
- Chỉnh sửa (Nội dung/Tệp đính kèm/Cương vực/Hạng mục tri thức nguồn) chỉ mở khi `status = soan_thao` **và** người xem là `assignee_id` hiện tại — trạng thái/người xem khác chỉ đọc kèm banner lý do khoá. ⚠ Ghi chú thiết kế đi trước (cùng cách xử lý đã áp dụng ở D-ADM-013 (¶4.13)): backend hiện chỉ khoá cứng ở 4 trạng thái (`dang_xet_duyet`/`dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban`) + theo `assignee_id` khi `soan_thao` — chưa khoá cứng ở `cho_xet_duyet`/`khong_dat_xet_duyet`; ẩn nút chỉnh sửa ở các trạng thái này tại đây là lựa chọn UI.
- Hành động cuối trang theo `status`:
  - `soan_thao` (chỉ `assignee_id` hiện tại): nút "Gửi xét duyệt" (`submit-for-review`).
  - `cho_xet_duyet`: hiện "Đang chờ nhận xét duyệt".
  - Ghi chú không đạt (`review_note`) hiện ở đây khi Mục từ vừa bị trả về (đọc lại từ lần `khong_dat_xet_duyet` gần nhất). Nút "Quay lại soạn thảo" (`resume-editing`, role `bien_tap` — không giới hạn theo `assignee_id`, nhất quán với `submit-for-review`).
- API: `GET /encyclopedia/entries/{id}`, `PATCH .../content`, `POST/DELETE .../knowledge-objects`, `POST .../knowledge-objects/{knowledge_object_id}/mark-synced`, `POST/DELETE .../files`, `POST/DELETE .../cultural-domains`, `POST .../submit-for-review`, `POST .../claim`, `POST .../release`, `POST .../force-release`, `POST .../resume-editing`.

## 4.18. [D-ADM-018] Xét duyệt Mục từ

- Breadcrumb: Bách khoa toàn thư > Mục từ > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3)): active tại cụm "Chờ & Xét duyệt" (`cho_xet_duyet`/`dang_xet_duyet`).
- Áp dụng khi `status ∈ {cho_xet_duyet, dang_xet_duyet}` (vai trò Xét duyệt Mục từ — khác vai trò Xét duyệt Hạng mục tri thức ở module 03).
- Header, banner "Nội dung bị khoá" khi `dang_xet_duyet`.
- Khối "Người phụ trách": "Nhận xử lý" (`Claim`, tại `cho_xet_duyet`, role `xet_duyet_muc_tu`, đồng thời chuyển `status → dang_xet_duyet`) / "Nhả" (`Release`, chỉ `assignee_id` hiện tại, lùi về `cho_xet_duyet`) / "Cưỡng chế nhả" (`ForceRelease`, chỉ role `quan_tri_he_thong`, tại `dang_xet_duyet` khi đang có `assignee_id` — hộp thoại xác nhận, quy ước (b) D-ADM-029 (¶3), R-ENC-016 (§2.3.2.5.5)).
- Nội dung: xem lại Mục từ đã render (đọc, tái dùng view TipTap ở chế độ chỉ đọc) + Tệp đính kèm + Cương vực đã gán + danh sách Hạng mục tri thức nguồn (tham khảo).
- Không có cấu trúc Phát biểu/Tham chiếu như module 03 — chỉ có 1 ô "Nhận xét xét duyệt" (`review_note`, textarea) cho nhận xét tổng thể (R-ENC-025 (§2.3.5.3)). Ô chỉ nhập được khi `status = dang_xet_duyet`.
- Nút cuối trang (tại `dang_xet_duyet`, bất kỳ Nhân viên nào giữ role `xet_duyet_muc_tu`, không giới hạn theo `assignee_id` — D-SD04-014 (¶4.4)):
  - "Không đạt xét duyệt" (`reject`, body `{note}`): **nhận xét bắt buộc** (R-ENC-025 (§2.3.5.3)). Nhãn ô nhận xét có dấu `*` kèm chú thích "Bắt buộc khi Không đạt xét duyệt". Nếu ô trống hoặc chỉ có khoảng trắng: không gọi API, báo lỗi ngay dưới ô "Vui lòng nhập nhận xét để vai trò Biên tập biết cần sửa gì" và focus vào ô. Nếu API vẫn trả HTTP 422 `review_note_required`, hiện cùng thông báo lỗi đó dưới ô.
  - "Đạt xét duyệt" (`approve`, body `{note?}`): nhận xét tuỳ chọn; ô trống thì gửi không kèm `note`.
- API: `GET /encyclopedia/entries/{id}`, `POST .../claim`, `POST .../release`, `POST .../force-release`, `POST .../reject`, `POST .../approve`.

## 4.19. [D-ADM-019] Xuất bản Mục từ

- Breadcrumb: Bách khoa toàn thư > Mục từ > {Tiêu đề}.
- Stepper trạng thái (D-ADM-029 (¶3)): active tại cụm "Đạt xét duyệt" (`dat_xet_duyet`) hoặc "Xuất bản" (`da_xuat_ban`/`khong_xuat_ban`, kèm nhãn phụ theo giá trị thực tế).
- Áp dụng khi `status ∈ {dat_xet_duyet, da_xuat_ban, khong_xuat_ban}` — cả 3 đều "Nội dung bị khoá".
- Header + xem lại toàn bộ Nội dung/Tệp đính kèm (đọc, tái dùng view D-ADM-018 (¶4.18)) kèm `review_note` cuối cùng.
- Tại `dat_xet_duyet` — 2 quyết định bắt buộc, chỉ role `xuat_ban_muc_tu` (R-ENC-021 (§2.3.4.2)):
  - Nút "Xuất bản" (`publish`) — xác nhận: "Xuất bản sẽ tạo một phiên bản mới, chốt lại toàn bộ Nội dung hiện tại. Tiếp tục?".
  - Nút "Không xuất bản" (`skip-publish`, body `{confirmed: true}`) — xác nhận bắt buộc (R-ENC-009 (§2.3.2.4) đặc tả gốc yêu cầu cảnh báo): "Không xuất bản: vòng xét duyệt này sẽ không tạo phiên bản nào để lưu lại. Tiếp tục?".
- Tại `da_xuat_ban`/`khong_xuat_ban`: hiện thời điểm chuyển trạng thái tương ứng. Nút "Mở lại" — **chỉ role `xet_duyet_muc_tu`** (không phải `xuat_ban_muc_tu`) — dialog chọn 1 trong 3 trạng thái đích (`soan_thao`/`cho_xet_duyet`/`dang_xet_duyet`), xác nhận không hoàn tác/ảnh hưởng người khác (`reopen`, body `{target_status}`).
- Khối "Lịch sử phiên bản" (luôn hiện nếu đã có ≥1 phiên bản chốt): bảng phiên bản, click → xem snapshot chỉ đọc.
- Khối "Phiên bản đang công khai" (`current_public_version_id`, độc lập với `status`, chỉ role `xuat_ban_muc_tu`): hiện phiên bản đang công khai (hoặc "Chưa chọn"), nút "Chọn/Đổi" (`set-public-version`).
- Khối "Chỉ mục AI" (chỉ role `quan_tri_he_thong`, chỉ hiện khi Mục từ đang có phiên bản công khai): nút "Đánh chỉ mục lại cho AI" (`POST /assistant/reindex/{entry_id}`) — dùng khi khắc phục sự cố chỉ mục AI; không cần hộp thoại xác nhận (không làm mất dữ liệu). Thành công → toast "Đã đưa vào hàng đợi" kèm link "Xem job nền" mở D-ADM-026 (¶4.26) lọc theo loại `assistant.reindex_entry`.
- API: `GET /encyclopedia/entries/{id}`, `POST .../publish`, `POST .../skip-publish`, `POST .../reopen`, `POST .../set-public-version`, `POST /assistant/reindex/{entry_id}`.

## 4.20. [D-ADM-020] Quản lý Cương vực

- Breadcrumb: Bách khoa toàn thư > Cương vực.
- Bảng: Mã (`code`), Tên (`name`), số Mục từ đang gán.
- Nút "+ Thêm Cương vực" — chỉ role `bien_tap` — dialog: Mã, Tên.
- Click dòng (chỉ role `bien_tap`) → dialog sửa Tên/Mã.
- Action inline theo dòng: "Xoá" — chỉ role `bien_tap` (R-ENC-037 (§2.3.7.5)). Hộp thoại xác nhận (không hoàn tác — quy ước (b) D-ADM-029 (¶3)): "Xoá Cương vực "{Tên}" khỏi danh mục? Cương vực sẽ không còn trong bộ lọc của Bách khoa toàn thư và AI Văn Minh Việt. Không thể hoàn tác. Tiếp tục?" → `DELETE /encyclopedia/cultural-domains/{id}`.
- Nếu API trả HTTP 409 `cultural_domain_in_use`: đóng hộp thoại xác nhận, hiện thông báo lỗi "Không xoá được: Cương vực "{Tên}" đang được gán cho {`entry_count`} Mục từ. Hãy gỡ Cương vực này khỏi các Mục từ đó trước (ở màn hình Soạn thảo Mục từ, D-ADM-017 (¶4.17))." kèm link "Xem các Mục từ" mở D-ADM-016 (¶4.16) đã lọc sẵn theo Cương vực này. Số liệu lấy từ `entry_count` trong response lỗi, không lấy từ cột trên bảng (có thể đã cũ). Sau khi báo lỗi, tải lại bảng.
- Quyền tạo/sửa/xoá giới hạn role `bien_tap` — theo D-SD04-017 (¶5.3).
- API: `GET /encyclopedia/cultural-domains`, `POST /encyclopedia/cultural-domains`, `PATCH /encyclopedia/cultural-domains/{id}`, `DELETE /encyclopedia/cultural-domains/{id}`.
- Quyền truy cập: màn hình này — role `bien_tap`/`xet_duyet_muc_tu`/`xuat_ban_muc_tu`; tạo/sửa/xoá — chỉ role `bien_tap`. (API đọc `GET /encyclopedia/cultural-domains` mở cho mọi Nhân viên kênh admin — dùng cho bộ lọc Cương vực ở D-ADM-023 (¶4.23)/D-ADM-024 (¶4.24), không mở thêm màn hình này cho role khác.)

## 4.21. [D-ADM-021] Nhật ký hoạt động (Audit Log)

- Breadcrumb: Giám sát > Nhật ký hoạt động.
- Bảng: Thời điểm, Nhân viên (tên + email), Loại hành động (`action_type`, hiển thị nhãn tiếng Việt dịch từ mã, ví dụ "Đăng nhập", "Tạo Nhân viên", "Xuất bản Mục từ", "Xoá Đề tài nghiên cứu", "Xoá Hạng mục tri thức", "Gán Chủ nhiệm đề tài", "Chạy lại job nền" (`job.retry`), "Huỷ job nền" (`job.cancel`), "Xoá Cương vực" (`cultural_domain.delete`), "Sửa cấu hình hệ thống" (`system_setting.update`), "Khôi phục mặc định cấu hình" (`system_setting.reset`)), Đối tượng liên quan (`entity_type` + `entity_id`, link tới màn hình chi tiết tương ứng nếu có), Chi tiết thay đổi (nút "Xem" mở popup hiển thị `detail` dạng key-value).
- Với `entity_type = job` (`entity_id` rỗng vì id job là bigint — D-SD01-004 (¶4)): cột Đối tượng liên quan hiển thị "Job #{`detail.job_id`}", link mở chi tiết job ở D-ADM-026 (¶4.26); nếu job đã bị dọn khỏi lịch sử (retention), D-ADM-026 (¶4.26) báo "Job không còn trong lịch sử lưu giữ".
- Với `entity_type = system_setting` (`entity_id` rỗng): cột Đối tượng liên quan hiển thị nhãn tham số theo `detail.key`, link mở D-ADM-028 (¶4.28) tại đúng nhóm; popup "Xem" hiển thị Giá trị trước (`detail.old_value`) → Giá trị sau (`detail.new_value`).
- Filter: theo Nhân viên, theo Loại hành động, theo khoảng thời gian (từ ngày – đến ngày).
- Tự động tải lại định kỳ (chu kỳ theo `operations.admin_polling_interval_seconds`, mặc định 30 giây, đọc từ `GET /client-settings`; có toggle bật/tắt) + nút "Tải lại" thủ công — chỉ làm mới danh sách theo bộ lọc hiện tại.
- Phân trang kiểu cursor, cùng convention với các bảng danh sách khác trong hệ thống.
- Chỉ đọc — không có thao tác sửa/xoá trên màn hình này.
- Dòng chú thích dưới bảng: "Nhật ký được lưu theo thời hạn cấu hình (mặc định 24 tháng). Bản ghi quá thời hạn được hệ thống tự động xoá mỗi ngày." — kèm link "Cấu hình thời hạn lưu" mở D-ADM-028 (¶4.28), nhóm Vận hành (`operations.audit_log_retention_months`, D-SD07-009 (¶4.3)).
- Quyền truy cập: chỉ role `quan_tri_he_thong`, xem toàn bộ, không giới hạn theo phạm vi/Tổ chức.
- API: `GET /shared/audit-logs` (D-SD01-002 (¶2)), `GET /client-settings`.

## 4.22. [D-ADM-022] Tổng quan (Dashboard)

- Không có Breadcrumb (trang gốc). Là trang mặc định điều hướng tới ngay sau khi đăng nhập thành công; trên Sidebar đặt ở vị trí đầu tiên (D-ADM-029 (¶3)), bất kể số thứ tự tài liệu.
- **Mục tiêu chính**: giúp người dùng, đặc biệt Nhân viên mới, hiểu được **bức tranh tổng thể của hệ nghiệp vụ** — toàn bộ pipeline dữ liệu văn hóa vận hành ra sao, các nhóm chức năng liên hệ với nhau thế nào, vai trò nào phụ trách bước nào — hơn là cung cấp số liệu thống kê. Toàn bộ nội dung màn hình là **nội dung tĩnh**, không có chip đếm số liệu và không phụ thuộc API mới nào.
- **Khối 1 — Sơ đồ pipeline nghiệp vụ tổng thể** (thành phần chính, đặt đầu trang, ngay dưới tiêu đề): sơ đồ tĩnh dạng luồng nối tiếp, mỗi khối bấm được (link) dẫn tới màn hình danh sách tương ứng:
  1. **Đề tài nghiên cứu** (2 trạng thái: Chuẩn bị tư liệu → Tư liệu sẵn sàng) — vai trò: Quản trị hệ thống (tạo/xoá), Chủ nhiệm đề tài (điều phối nhân sự). Click → mở D-ADM-008 (¶4.8).
  2. **Tư liệu gốc** (đồng bộ tự động từ MinIO/S3, không upload thủ công) — vai trò: Nhập liệu. Click → mở D-ADM-010 (¶4.10).
  3. **Hạng mục tri thức** — 5 cụm trạng thái nối tiếp (cùng cách gộp cụm với Stepper ở D-ADM-029 (¶3)): Nghiên cứu (vai trò Nghiên cứu) → Chờ & Xác minh AI (tự động hoặc kích hoạt thủ công theo cấu hình) → Xét duyệt chuyên gia (vai trò Xét duyệt) → Đạt xét duyệt → Xuất bản (vai trò Xuất bản). Click → mở D-ADM-012 (¶4.12).
  4. **Mục từ** (rẽ nhánh từ cụm "Xuất bản" của Hạng mục tri thức, thể hiện quan hệ nhiều-nhiều `entry_knowledge_object`) — 4 cụm trạng thái: Soạn thảo (vai trò Biên tập) → Chờ & Xét duyệt (vai trò Xét duyệt Mục từ) → Đạt xét duyệt → Xuất bản (vai trò Xuất bản Mục từ). Click → mở D-ADM-016 (¶4.16).
  5. **Trợ lý AI Văn Minh Việt** (rẽ từ cụm "Xuất bản" của Mục từ: phiên bản đang công khai được tự động đánh chỉ mục bằng job nền) — trả lời câu hỏi dựa trên Bách khoa toàn thư, kèm trích dẫn Mục từ nguồn và cảnh báo phát biểu chưa được chứng thực. Vai trò: mọi Nhân viên (hỏi), Quản trị hệ thống (rà soát chất lượng). Click → mở D-ADM-023 (¶4.23). Khối này không highlight theo role (mọi Nhân viên đều dùng).

  Cụm/khối tương ứng với (các) role theo chức năng mà Nhân viên đang đăng nhập đang giữ được làm nổi bật trực quan (viền đậm/nền khác màu) trên sơ đồ, để người dùng thấy ngay mình "đứng ở đâu" trong toàn bộ pipeline — đúng tinh thần nguyên tắc ở ¶1. Sơ đồ không hiển thị bất kỳ số liệu/số đếm nào, chỉ thể hiện cấu trúc luồng nghiệp vụ.
- **Khối 2 — Mô tả từng nhóm chức năng** (đặt dưới sơ đồ, văn bản ngắn 1–2 câu mỗi nhóm kèm link "Xem thêm" dẫn tới màn hình đầu tiên của nhóm — chỉ hiện nhóm mà người dùng có quyền truy cập, theo đúng điều kiện ẩn/hiện ở Sidebar D-ADM-029 (¶3)):
  - **Người dùng & Tổ chức**: quản lý Nhân viên, phân quyền theo chức năng và theo phạm vi Đề tài nghiên cứu, quản lý các Tổ chức khác tham gia hợp tác nghiên cứu. → D-ADM-004 (¶4.4).
  - **Cơ sở dữ liệu văn hóa**: khởi tạo Đề tài nghiên cứu, đồng bộ Tư liệu gốc, và đội ngũ Nghiên cứu/Xét duyệt cùng biến Tư liệu gốc thành Hạng mục tri thức đã qua kiểm chứng (AI + chuyên gia). → D-ADM-008 (¶4.8).
  - **Bách khoa toàn thư**: đội ngũ Biên tập tổng hợp các Hạng mục tri thức đã xuất bản thành Mục từ — nội dung công khai cuối cùng phục vụ độc giả. → D-ADM-016 (¶4.16).
  - **Trợ lý AI**: hỏi AI Văn Minh Việt trên nội dung Bách khoa toàn thư đã xuất bản, có trích dẫn nguồn; Quản trị hệ thống rà soát chất lượng các lượt hỏi–đáp. → D-ADM-023 (¶4.23).
  - **Giám sát**: theo dõi lịch sử hoạt động (audit log) của toàn bộ Nhân viên và trạng thái các job nền (đồng bộ tư liệu, AI Verification, đánh chỉ mục AI...). → D-ADM-021 (¶4.21).
  - **Hệ thống**: điều chỉnh tham số vận hành (AI Verification, tài khoản & bảo mật, email hệ thống, AI Văn Minh Việt, vận hành) mà không cần triển khai lại phần mềm. → D-ADM-028 (¶4.28).
- Quyền truy cập: mọi Nhân viên đã đăng nhập (Khối 1 hiển thị đầy đủ cho mọi người xem, có highlight riêng theo role; Khối 2 tự ẩn/hiện từng nhóm theo role như trên).
- API: không có — toàn bộ nội dung tĩnh, không gọi API đếm số liệu nào.

## 4.23. [D-ADM-023] Hỏi AI Văn Minh Việt

- Breadcrumb: Trợ lý AI > Hỏi AI Văn Minh Việt.
- Quyền truy cập: mọi Nhân viên đã đăng nhập (R-AI-003 (§2.4.2)).
- Bố cục: khung chat một cột, ô nhập câu hỏi cố định ở đáy; header có nút "Hội thoại mới".
- Bộ lọc Cương vực (R-AI-004 (§2.4.3)): select một Cương vực đặt ngay trên ô nhập, mặc định "Toàn bộ Bách khoa"; danh sách lấy từ `GET /encyclopedia/cultural-domains`; áp dụng cho từng lượt hỏi (gửi `cultural_domain_id` theo lượt).
- Hội thoại: chỉ giữ một hội thoại hiện tại, không có danh sách hội thoại cũ. Client tự sinh `conversation_id` (UUID) khi bắt đầu hội thoại mới (lần đầu vào màn hình, bấm "Hội thoại mới", hoặc hội thoại đã lưu hết hạn).
- Lưu tạm hội thoại hiện tại trong localStorage của trình duyệt để tải lại trang/quay lại màn hình vẫn chat tiếp được:
  - Khoá lưu gắn theo id Nhân viên đăng nhập (nhiều tài khoản trên cùng trình duyệt không thấy hội thoại của nhau).
  - Nội dung lưu: `conversation_id`, Cương vực đang chọn, các lượt đã hoàn tất (câu hỏi, câu trả lời, trích dẫn, cờ self-audit), thời điểm lượt hỏi cuối.
  - Chỉ lưu lượt sau khi nhận `done`; lượt đang stream dở hoặc lỗi không được lưu.
  - Hết hạn sau `assistant.conversation_ttl_hours` giờ (mặc định 6, đọc từ `GET /client-settings` — D-SD07-013 (¶5.2)) tính từ lượt hỏi cuối — khi vào màn hình mà hội thoại đã lưu quá hạn thì xoá và bắt đầu hội thoại mới.
  - Xoá khi bấm "Hội thoại mới" và khi Đăng xuất.
  - Tiếp tục chat sau khi tải lại: gửi cùng `conversation_id` — backend tự đọc lịch sử N lượt gần nhất theo `conversation_id` (D-SD05-005 (¶3.2) bước 0), không cần API đọc lại hội thoại cho Nhân viên.
- Trạng thái trống: đoạn giới thiệu ngắn — AI chỉ trả lời trong phạm vi Bách khoa toàn thư đã xuất bản (R-AI-005 (§2.4.4)).
- Câu miễn trừ trách nhiệm (R-AI-009 (§2.4.8)): `assistant.disclaimer_text` từ `GET /client-settings`, hiện dạng chú thích Chữ phụ cố định ngay dưới ô nhập; chuỗi rỗng thì không hiện.
- Hiển thị một lượt hỏi theo hợp đồng SSE (D-SD05-012 (¶5.1)):
  - `token`: bong bóng trả lời hiện chữ dần; trong lúc stream khoá ô nhập/nút gửi (một lượt hỏi tại một thời điểm).
  - `citations`: dải chip "Nguồn: …" dưới câu trả lời; mỗi chip mở Trang chi tiết Mục từ của Web công khai (D-PUB-004 (¶4.4)) trong tab mới — không mở màn hình biên tập D-ADM-017 (¶4.17)–D-ADM-019 (¶4.19).
  - `self_audit`: `flags` có phần tử → banner cảnh báo màu vàng dưới câu trả lời: "Một số phát biểu trong câu trả lời chưa được chứng thực bởi nguồn trích dẫn", mở rộng để xem từng `claim_text` kèm `reason`; `flags = null` → dòng chú thích xám "Chưa kiểm tra được độ tin cậy của câu trả lời này"; `[]` → không hiện gì.
  - `done`: mở lại ô nhập.
  - `error`: giữ nguyên phần câu trả lời đã hiện (nếu có), hiện thông báo lỗi kèm `trace_id` và nút "Hỏi lại" (gửi lại cùng câu hỏi, cùng `conversation_id`).
- API: `POST /assistant/chat` (SSE), `GET /encyclopedia/cultural-domains`, `GET /client-settings`.

## 4.24. [D-ADM-024] Danh sách hỏi–đáp AI

- Breadcrumb: Trợ lý AI > Hỏi–đáp AI.
- Quyền truy cập: chỉ role `quan_tri_he_thong` (rà soát chất lượng — D-SD05-013 (¶5.2)).
- Bảng (mỗi dòng = một lượt hỏi–đáp): Thời điểm, Kênh (badge "Admin"/"Công khai"), Người hỏi (`asked_by` — tên + email; "Ẩn danh" với kênh công khai), Câu hỏi (cắt 2 dòng), Cương vực (tên, hoặc "Toàn bộ"), Số Mục từ trích dẫn, Cờ self-audit (`self_audit_flag_count`: > 0 → badge vàng kèm số; 0 → "—"; `null` → badge xám "Chưa kiểm"), Lượt thứ (`turn_index + 1`).
- Filter: Kênh, Cương vực, Nhân viên hỏi (ô tìm theo tên/email, `GET /identity/employees`), toggle "Chỉ lượt có cờ self-audit" (`has_self_audit_flags = true`), khoảng thời gian.
- Phân trang cursor; nút "Tải lại" thủ công (không tự tải lại định kỳ).
- Click dòng → D-ADM-025 (¶4.25) mở hội thoại chứa lượt đó, cuộn tới và highlight lượt được chọn.
- Chỉ đọc.
- Dòng chú thích dưới bảng: "Hội thoại không có lượt hỏi mới trong thời hạn lưu (mặc định 180 ngày) được hệ thống tự động xoá mỗi ngày, cùng toàn bộ lượt hỏi–đáp của hội thoại đó." — kèm link "Cấu hình thời hạn lưu" mở D-ADM-028 (¶4.28), nhóm AI Văn Minh Việt (`assistant.query_log_retention_days`, D-SD05-006 (¶3.3)).
- API: `GET /assistant/query-logs`, `GET /encyclopedia/cultural-domains`, `GET /identity/employees`.

## 4.25. [D-ADM-025] Chi tiết hội thoại AI

- Breadcrumb: Trợ lý AI > Hỏi–đáp AI > Hội thoại {thời điểm bắt đầu}.
- Quyền truy cập: chỉ role `quan_tri_he_thong`.
- Header: Kênh, Người hỏi (`asked_by` cấp hội thoại; "Ẩn danh" với kênh công khai), thời điểm bắt đầu/lượt cuối, số lượt.
- Danh sách các lượt theo `turn_index`, mỗi lượt gồm:
  - Câu hỏi gốc; nếu có `rewritten_question`, hiện dòng chữ phụ "Câu hỏi đã viết lại: …".
  - Cương vực đã chọn (hoặc "Toàn bộ").
  - Câu trả lời.
  - Trích dẫn (`cited_entries`): chip tiêu đề Mục từ, click mở màn hình Mục từ tương ứng trong Admin (điều hướng theo `status` như D-ADM-016 (¶4.16)); `is_public = false` → chip xám kèm tooltip "Mục từ hiện không còn phiên bản công khai — tiêu đề lấy theo phiên bản đã chốt mới nhất".
  - Cờ self-audit: danh sách `claim_text` + `reason` (nền vàng); `null` → "Chưa kiểm được"; `[]` → "Không có cờ".
- Hội thoại đã bị dọn theo thời hạn lưu (mở từ link cũ/bookmark, API trả 404): hiện "Hội thoại không còn trong thời hạn lưu giữ" kèm link quay lại D-ADM-024 (¶4.24).
- Chỉ đọc.
- API: `GET /assistant/conversations/{id}`.

## 4.26. [D-ADM-026] Theo dõi job nền

- Breadcrumb: Giám sát > Job nền.
- Quyền truy cập: chỉ role `quan_tri_he_thong` (D-SD01-004 (¶4)).
- Bảng: ID (`#` + id), Loại job (nhãn tiếng Việt kèm mã — bảng nhãn bên dưới), Trạng thái (badge), Số lần thử (`attempts`/`max_attempts`), Đối tượng liên quan, Tạo lúc, Bắt đầu, Kết thúc, Lỗi gần nhất (cắt 1 dòng).
- Nhãn loại job: `ingestion.sync_source` "Đồng bộ Tư liệu gốc"; `knowledge.extract_file_metadata` "Trích metadata file"; `knowledge.generate_transcript` "Sinh bản chép lời"; `verification.run` "AI Verification"; `assistant.reindex_entry` "Đánh chỉ mục Mục từ cho AI"; `assistant.refresh_domain_tags` "Cập nhật Cương vực trong chỉ mục AI"; `search.rebuild_fulltext` "Tái lập chỉ mục toàn văn"; `shared.usage_snapshot` "Snapshot usage theo Tổ chức"; `shared.job_cleanup` "Dọn lịch sử job nền"; `shared.audit_log_cleanup` "Dọn audit log quá hạn"; `assistant.query_log_cleanup` "Dọn nhật ký hỏi đáp AI quá hạn"; `shared.apply_storage_lifecycle` "Áp quy tắc lưu trữ lạnh".
- Badge trạng thái: `pending` "Đang chờ"; `running` "Đang chạy"; `failed` + `exhausted = false` "Lỗi — sẽ thử lại"; `failed` + `exhausted = true` "Lỗi — hết lượt thử"; `completed` "Hoàn thành"; `cancelled` "Đã huỷ".
- Đối tượng liên quan (`related_entity`): `source` → D-ADM-011 (¶4.11); `knowledge_object` → điều hướng theo `status` như D-ADM-012 (¶4.12); `entry` → điều hướng theo `status` như D-ADM-016 (¶4.16); `null` → "—".
- Filter: Loại job, Trạng thái, khoảng thời gian.
- Tự động tải lại định kỳ (cùng chu kỳ cấu hình và toggle như D-ADM-021 (¶4.21)) + nút "Tải lại".
- Click dòng → panel chi tiết (`GET /shared/jobs/{id}`): payload (key-value), lỗi gần nhất, lịch sử các lần thử (thời điểm + lỗi từng lần).
  - Job `ingestion.sync_source` có `follows_job_id` trong payload (job nối tiếp, D-SD03-017 (¶4.2)): hiện dòng "Nối tiếp job #{follows_job_id}", click mở panel chi tiết của job đó; nếu job đó đã bị dọn (API trả 404) → thông báo "Job #{follows_job_id} không còn trong thời gian lưu giữ".
- Hành động (trên dòng và trong panel chi tiết):
  - "Chạy lại" — chỉ khi `status = failed` (cả `exhausted` true/false); xác nhận ngắn "Chạy lại job #{id} ngay?" (`retry`).
  - "Huỷ" — chỉ khi `status = pending` (không huỷ job đang chạy); hộp thoại xác nhận (quy ước (b) D-ADM-029 (¶3)) nêu hệ quả theo loại job:
    - `verification.run`: "Hạng mục tri thức sẽ ở lại trạng thái 'Đang chạy AI Verification' cho tới khi kích hoạt lại AI Verification (D-ADM-013 (¶4.13)/D-ADM-014 (¶4.14))."
    - `assistant.reindex_entry`: "Chỉ mục AI của Mục từ sẽ không được cập nhật cho tới khi bấm 'Đánh chỉ mục lại cho AI' (D-ADM-019 (¶4.19))."
    - `ingestion.sync_source`: "Tư liệu gốc sẽ không được đồng bộ cho tới khi bấm 'Đồng bộ lại' (D-ADM-011 (¶4.11))."
    - Loại khác: "Huỷ job #{id}? Không thể hoàn tác."
  - Cả hai thao tác được ghi audit log (`job.retry`/`job.cancel`, xem D-ADM-021 (¶4.21)).
- Dòng chú thích dưới bảng: chỉ hiển thị job trong thời gian lưu giữ của hệ thống; job cũ hơn đã được dọn tự động.
- API: `GET /shared/jobs`, `GET /shared/jobs/{id}`, `POST /shared/jobs/{id}/retry`, `POST /shared/jobs/{id}/cancel`.

## 4.27. [D-ADM-027] Đổi mật khẩu

> Cơ sở: R-ID-035 (§2.1.5.10); D-SD02-006 (¶3.4), D-SD02-009 (¶5.1).

- Dạng dialog (không có route/Breadcrumb riêng), mở từ "Đổi mật khẩu" trong menu tài khoản trên Topbar (D-ADM-029 (¶3)), từ bất kỳ màn hình nào.
- Quyền truy cập: mọi Nhân viên đã đăng nhập, chỉ đổi mật khẩu của chính mình.
- Form:
  - Mật khẩu hiện tại.
  - Mật khẩu mới — bên dưới hiện danh sách yêu cầu theo chính sách mật khẩu đang cấu hình (`GET /auth/password-policy`: độ dài tối thiểu, có cả chữ và số, có ký tự đặc biệt), mỗi dòng tick xanh khi đã đạt, kiểm tra ngay khi gõ.
  - Xác nhận mật khẩu mới.
  - Cả 3 ô có nút hiện/ẩn mật khẩu.
  - Nút "Huỷ" và "Đổi mật khẩu" (disable cho tới khi đủ 3 ô, mật khẩu mới đạt chính sách, khớp ô xác nhận và khác mật khẩu hiện tại).
- Dòng lưu ý ngay trên nút: "Sau khi đổi mật khẩu, bạn sẽ bị đăng xuất khỏi mọi thiết bị và cần đăng nhập lại."
- Lỗi từ backend (D-SD02-009 (¶5.1)):
  - HTTP 422 `invalid_current_password` → báo lỗi dưới ô "Mật khẩu hiện tại": "Mật khẩu hiện tại không đúng".
  - HTTP 422 `password_unchanged` → báo lỗi dưới ô "Mật khẩu mới": "Mật khẩu mới phải khác mật khẩu hiện tại".
  - HTTP 422 `password_policy_violation` → hiện đúng các điều kiện chưa đạt trả về (trường hợp chính sách vừa đổi sau khi mở dialog).
  - HTTP 423 `login_locked` (nhập sai mật khẩu hiện tại quá số lần cho phép — mọi phiên đã bị thu hồi, R-ID-036 (§2.1.5.10.1)) → đóng dialog, xử lý như phiên bị thu hồi (D-ADM-029 (¶3)), về D-ADM-001 (¶4.1) với thông báo "Tài khoản đang tạm khoá do nhập sai mật khẩu nhiều lần. Thử lại sau {locked_until}."
- Thành công (204) → backend thu hồi toàn bộ phiên của Nhân viên (D-SD02-006 (¶3.4) bước 6, D-SD02-007 (¶3.5)) → client xử lý như Đăng xuất (D-ADM-029 (¶3), bỏ qua bước gọi `POST /auth/logout`) → về D-ADM-001 (¶4.1) kèm thông báo "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới".
- API: `GET /auth/password-policy`, `POST /auth/change-password` (body `{current_password, new_password}`).

## 4.28. [D-ADM-028] Cấu hình hệ thống

- Breadcrumb: Hệ thống > Cấu hình hệ thống.
- Quyền truy cập: chỉ role `quan_tri_he_thong` (R-CFG-002 (§2.8.1)).
- Cơ sở: `system-design/07-system-settings.md` (registry tham số D-SD07-003 (¶2.3), luồng sửa D-SD07-005 (¶3.2), API D-SD07-012 (¶5.1)).
- **Bố cục**: tab dọc bên trái gồm 5 nhóm theo `group` — AI Verification (`ai_verification`), Tài khoản & bảo mật (`identity`), Email hệ thống (`email`), AI Văn Minh Việt (`assistant`), Vận hành (`operations`). Tab nhóm nào có tham số đang khác mặc định hiện chấm nhỏ màu Accent. Tab đang chọn phản ánh trên URL (query `group`) để link từ màn hình khác (D-ADM-021 (¶4.21), D-ADM-024 (¶4.24)) mở đúng nhóm.
- Dữ liệu: `GET /shared/settings` một lần khi vào màn hình. Nhãn tiếng Việt, mô tả và đơn vị của từng tham số do frontend quản lý theo `key` (D-SD07-012 (¶5.1)) — bảng nhãn bên dưới.
- **Mỗi tham số là một dòng**:
  - Nhãn + mô tả ngắn (1 dòng, Chữ phụ).
  - Ô nhập theo `type`/`constraints`: `int` → ô số kèm đơn vị và gợi ý "Từ {min} đến {max}"; `bool` → toggle; `text` có `allowed_values` → radio; `text[]` → nhóm checkbox; `text` → input/textarea kèm đếm ký tự; `int` nullable → toggle bật/tắt + ô số (tắt = `null`).
  - Dòng phụ: "Mặc định: {default_value}" và `apply_note` ("Áp dụng: …").
  - Khi `is_default = false`: badge "Đã chỉnh", tooltip "Sửa lần cuối bởi {updated_by.display_name} lúc {updated_at}", và nút "Khôi phục mặc định".
  - Kiểm tra phía client theo `constraints` ngay khi nhập (ngoài giới hạn → viền đỏ + thông báo dưới ô).
- **Lưu theo nhóm**: thanh hành động cố định ở cuối tab — "Huỷ thay đổi" và "Lưu thay đổi" (enable khi tab có thay đổi và không có lỗi phía client), kèm đếm "{n} tham số đã sửa". Lưu → `PATCH /shared/settings` chỉ gửi các key đã sửa trong tab.
  - Thành công → toast "Đã lưu. Thay đổi có hiệu lực trong vòng khoảng 1 phút" (D-SD07-008 (¶4.2)), tải lại dữ liệu.
  - HTTP 422 `invalid_settings` → không tham số nào được lưu (R-CFG-003 (§2.8.2)): banner đỏ đầu tab "Chưa lưu thay đổi nào — có tham số không hợp lệ", và `reason` hiện dưới đúng ô theo `details[].key`.
  - Rời tab/màn hình khi còn thay đổi chưa lưu → hộp thoại "Thay đổi chưa lưu sẽ bị mất. Tiếp tục?" (cùng cơ chế cảnh báo rời trang ở D-ADM-029 (¶3)).
- **Khôi phục mặc định** một tham số → xác nhận ngắn "Khôi phục "{Nhãn}" về giá trị mặc định ({default_value})?" → `DELETE /shared/settings/{key}`; lỗi 422 hiện như trên. Nếu dòng đó đang có thay đổi chưa lưu thì bỏ thay đổi đó.
- **Xác nhận khi giảm thời hạn lưu** (quy ước (b) D-ADM-029 (¶3) — dữ liệu bị xoá vĩnh viễn): khi Lưu mà giá trị mới **nhỏ hơn** giá trị hiện hành của `operations.audit_log_retention_months`, `assistant.query_log_retention_days` hoặc `operations.job_retention_*`, hộp thoại: "Giảm thời hạn lưu "{Nhãn}" từ {cũ} xuống {mới} {đơn vị}: dữ liệu cũ hơn thời hạn mới sẽ bị xoá vĩnh viễn ở lần dọn kế tiếp. Không thể hoàn tác. Tiếp tục?". Áp dụng cả cho "Khôi phục mặc định" khi mặc định nhỏ hơn giá trị hiện hành.
- Mọi lần lưu/khôi phục được ghi audit log (`system_setting.update`/`system_setting.reset`, R-CFG-004 (§2.8.3)) — xem ở D-ADM-021 (¶4.21). Không có lịch sử giá trị riêng trên màn hình này (R-CFG-003 (§2.8.2)).

**Nhóm AI Verification** (R-CFG-006 (§2.8.4.1))

| Key | Nhãn | Ô nhập |
|---|---|---|
| `ai_verification.trigger_mode` | Chế độ kích hoạt AI Verification | Radio "Tự động khi gửi xét duyệt" (`auto`) / "Thủ công" (`manual`) |
| `ai_verification.manual_trigger_roles` | Vai trò được kích hoạt thủ công | Checkbox: Nghiên cứu, Xét duyệt, Chủ nhiệm đề tài (theo đúng đề tài của hạng mục), Quản trị hệ thống |

- Khi đổi chế độ (chưa lưu): banner vàng ngay dưới radio — "Đổi chế độ không tự xử lý lại các Hạng mục tri thức đang chờ. Hạng mục đang ở 'Chờ xét duyệt' vẫn phải kích hoạt AI Verification thủ công (D-ADM-013 (¶4.13))." (R-CFG-006 (§2.8.4.1)).
- Chế độ Thủ công mà không tick vai trò nào → lỗi phía client "Chọn ít nhất một vai trò khi dùng chế độ Thủ công", không cho Lưu (backend cũng kiểm — D-SD07-005 (¶3.2)).

**Nhóm Tài khoản & bảo mật** (R-CFG-007 (§2.8.4.2))

| Key | Nhãn | Đơn vị |
|---|---|---|
| `identity.invite_token_ttl_hours` | Thời hạn đường dẫn mời | giờ |
| `identity.password_reset_token_ttl_minutes` | Thời hạn đường dẫn đặt lại mật khẩu | phút |
| `identity.access_token_ttl_minutes` | Thời hạn access token | phút |
| `identity.refresh_token_ttl_days` | Thời hạn phiên đăng nhập (refresh token) | ngày |
| `identity.password_min_length` | Độ dài mật khẩu tối thiểu | ký tự |
| `identity.password_require_letter_and_digit` | Mật khẩu phải có cả chữ và số | toggle |
| `identity.password_require_special_char` | Mật khẩu phải có ký tự đặc biệt | toggle |
| `identity.login_max_failed_attempts` | Số lần sai mật khẩu trước khi tạm khoá | lần (0 = tắt tạm khoá) |
| `identity.login_lockout_minutes` | Thời gian tạm khoá | phút |

- Chú thích cho nhóm chính sách mật khẩu: "Chỉ áp dụng khi đặt mật khẩu mới; không buộc Nhân viên đổi mật khẩu hiện có."

**Nhóm Email hệ thống** (R-CFG-008 (§2.8.4.3))

- `email.sender_name` "Tên người gửi"; `email.sender_address` "Địa chỉ người gửi" — lỗi tên miền không được phép hiện theo `reason` từ backend (tên miền phải thuộc danh sách đã xác minh, D-SD07-003 (¶2.3)).
- Hai khối mẫu: "Email mời" (`email.template.invite`) và "Email đặt lại mật khẩu" (`email.template.password_reset`), mỗi khối gồm:
  - "Tiêu đề" (1 dòng, tối đa 200 ký tự) và "Nội dung HTML" (ô soạn mã HTML dạng monospace, tối đa 50.000 ký tự, đếm ký tự).
  - Hàng chip "Chèn biến" — bấm để chèn tại con trỏ: `{{display_name}}` Tên Nhân viên, `{{link}}` Đường dẫn, `{{expires_at}}` Thời hạn đường dẫn, `{{organization_name}}` Tên Tổ chức (D-SD07-010 (¶4.4)).
  - Kiểm tra phía client: nội dung phải chứa `{{link}}` — thiếu thì báo "Mẫu bắt buộc phải chứa đường dẫn {{link}}" và không cho Lưu. Các lỗi khác (cú pháp, biến lạ, thẻ/thuộc tính HTML bị cấm) theo `reason` từ backend.
  - Nút "Xem trước" → `POST /shared/settings/email-templates/{template}/preview` với bản đang soạn (chưa lưu) → dialog hiện tiêu đề đã render và 2 tab: "HTML" (hiển thị trong iframe sandbox, không chạy script) / "Văn bản thuần" (`body_text`). Lỗi validate hiện trong dialog.
  - Nút "Gửi thử" → `POST .../test` với bản đang soạn → toast "Đã gửi email thử tới {email của Nhân viên đang đăng nhập}. Đường dẫn trong email thử không dùng được."
  - "Khôi phục mặc định" áp dụng cho cả mẫu (tiêu đề + nội dung).

**Nhóm AI Văn Minh Việt** (R-CFG-009 (§2.8.4.4))

| Key | Nhãn | Ô nhập / đơn vị |
|---|---|---|
| `assistant.retrieve_top_k` | Số đoạn nội dung truy xuất mỗi lượt hỏi | đoạn |
| `assistant.history_turns` | Số lượt hỏi trước dùng làm ngữ cảnh | lượt (0 = mỗi lượt hỏi độc lập) |
| `assistant.rewrite_query_enabled` | Viết lại câu hỏi nối tiếp theo ngữ cảnh | toggle |
| `assistant.conversation_ttl_hours` | Thời hạn giữ hội thoại phía người dùng | giờ |
| `assistant.no_context_answer` | Câu trả lời khi không có thông tin | textarea, 1–500 ký tự |
| `assistant.disclaimer_text` | Câu miễn trừ trách nhiệm | textarea, 0–500 ký tự (để trống = không hiển thị) |
| `assistant.query_log_retention_days` | **Thời hạn lưu nhật ký hỏi đáp** | ngày (30–3650, mặc định 180) |
| `assistant.public_rate_limit_enabled` | Bật giới hạn lượt hỏi kênh công khai | toggle |
| `assistant.public_rate_limit_max_requests` | Số lượt hỏi tối đa mỗi địa chỉ IP | lượt |
| `assistant.public_rate_limit_window_seconds` | Trong khoảng thời gian | giây |

- `assistant.query_log_retention_days` — mô tả: "Hội thoại không có lượt hỏi mới quá số ngày này bị xoá cùng toàn bộ lượt hỏi–đáp. Hệ thống dọn mỗi ngày." (R-AI-014 (§2.4.9.4), D-SD05-006 (¶3.3)).
- Hai ô hạn mức kênh công khai hiện mờ (vẫn sửa được) khi toggle giới hạn đang tắt.

**Nhóm Vận hành** (R-CFG-010 (§2.8.4.5))

| Key | Nhãn | Ô nhập / đơn vị |
|---|---|---|
| `operations.source_sync_debounce_seconds` | Thời gian gom sự kiện đồng bộ Tư liệu gốc | giây |
| `operations.job_retention_completed_hours` | Giữ job đã hoàn thành | giờ |
| `operations.job_retention_cancelled_hours` | Giữ job đã huỷ | giờ |
| `operations.job_retention_discarded_hours` | Giữ job lỗi hết lượt thử | giờ |
| `operations.audit_log_retention_months` | **Thời hạn lưu audit log** | tháng (12–120, mặc định 24) |
| `operations.source_cold_storage_after_days` | Chuyển phiên bản Tư liệu gốc cũ sang lưu trữ lạnh | toggle + ngày (tắt = không chuyển) |
| `operations.admin_polling_interval_seconds` | Chu kỳ tự tải lại (Nhật ký hoạt động, Job nền) | giây |

- `operations.source_sync_debounce_seconds` — mô tả: "Khi thư mục Tư liệu gốc có thay đổi, hệ thống chờ số giây này để gom các thay đổi liên tiếp rồi đồng bộ một lần. Nếu lúc đó đang có lượt đồng bộ khác chạy, hệ thống chờ thêm đúng khoảng này rồi thử lại." (D-SD03-017 (¶4.2), D-SD07-003 (¶2.3)).
- `operations.audit_log_retention_months` — mô tả: "Không được đặt dưới 12 tháng (R-NFR-004 (§3.1.2)). Bản ghi quá thời hạn được xoá mỗi ngày." (D-SD07-009 (¶4.3)).
- `operations.source_cold_storage_after_days` — sau khi lưu, toast kèm link "Xem job nền" mở D-ADM-026 (¶4.26) lọc theo loại `shared.apply_storage_lifecycle`.
- API: `GET /shared/settings`, `PATCH /shared/settings`, `DELETE /shared/settings/{key}`, `POST /shared/settings/email-templates/{template}/preview`, `POST /shared/settings/email-templates/{template}/test`.
