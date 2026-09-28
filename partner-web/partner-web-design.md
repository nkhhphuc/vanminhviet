# Đặc Tả Giao Diện Cổng Nhân Viên Tổ Chức Khác — Văn Minh Việt

> Xem khung làm việc và nguyên tắc tại `partner-web/00-claude-instructions.md`. Lịch sử thay đổi tại `partner-web/changelog.md`.

## 1. Tổng quan

- Quasar (Vue 3) + Pinia, **app/deploy riêng** khỏi Admin nội bộ (§1.2.3.2, module 2.7 đặc tả gốc; `system-design/01-architecture-and-tech-stack.md` mục 1) — dành cho Nhân viên thuộc Tổ chức khác (viện nghiên cứu ngoài).
- Thực hiện 3 vai trò theo phạm vi Đề tài nghiên cứu được gán: **vai trò Nghiên cứu** (`nghien_cuu`), **vai trò Xét duyệt** (`xet_duyet`) (§2.7.2 đặc tả gốc), và **vai trò Chủ nhiệm đề tài** (`chu_nhiem_de_tai`, §2.2.5.5/§2.7.3.4–5 — có thể thuộc Tổ chức khác, không chỉ Văn Minh Việt) — không có Nhập liệu, Xuất bản, Biên tập, Xét duyệt Mục từ, Quản trị hệ thống. Không có màn hình quản lý người dùng/phân quyền/Tổ chức dù giữ vai trò gì (§2.7.4); riêng việc Chủ nhiệm đề tài quản lý nhân sự Nghiên cứu/Xét duyệt **trong đúng đề tài mình phụ trách** không thuộc phạm vi cấm này (§2.2.5.5 — khác quản lý người dùng toàn hệ thống).
- **Phạm vi xem khác nhau theo vai trò**: Nghiên cứu/Xét duyệt xem được Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt (4.5–4.9). Chủ nhiệm đề tài — khi **không** đồng thời giữ Nghiên cứu/Xét duyệt của đề tài đó — chỉ xem được tiến độ (Tiêu đề/Trạng thái/Người phụ trách/Người tạo) và quản lý nhân sự đề tài, **không** xem được Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt (`system-design/03-cultural-knowledge-base.md` mục 5.1) — xem màn hình riêng 4.10.
- Ranh giới route đã chốt ở `system-design/01-architecture-and-tech-stack.md` mục 2: nhóm `/api/v1/partner/...` chỉ mount phần Nghiên cứu/Xét duyệt/quản lý nhân sự đề tài trong `knowledge`/`gate` (chi tiết endpoint ở `03-cultural-knowledge-base.md` mục 5), cùng nhóm `auth/*` (mọi Nhân viên tự xác thực, `02-identity.md` mục 5.1) — **không mount** `identity`, `ingestion`, `encyclopedia`.
- Mức độ đặc tả: wireframe/mô tả bố cục đủ dùng cho dev, không mockup chi tiết layout/spacing như `public-web/` (theo `00-claude-instructions.md` mục 1) — cùng mức với `admin-web/`. Riêng bảng màu (xem mục 3) được định nghĩa để đảm bảo nhất quán nhận diện thương hiệu với `public-web/`.
- Một Nhân viên có thể giữ role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` của **nhiều Đề tài nghiên cứu khác nhau** cùng lúc (§2.2.1.4, §2.2.5.2–5.3, §2.2.5.5) → mọi danh sách/thao tác trong tài liệu này đều giới hạn theo đúng phạm vi đề tài mà Nhân viên đang đăng nhập được gán, không có khái niệm "xem toàn bộ" như Quản trị hệ thống ở Admin nội bộ (`03-cultural-knowledge-base.md` mục 3.5 nêu rõ ngoại lệ xem toàn bộ **không áp dụng** cho nhóm route `partner`).
- **Nguyên tắc giao diện**: giao diện cần giúp người dùng luôn thấy được bức tranh tổng thể (cấu trúc điều hướng/phân cấp dữ liệu của Cổng này) và vị trí chức năng hiện tại nằm ở đâu trong đó — thực hiện qua Breadcrumb, Stepper trạng thái, Sidebar/Topbar, và màn hình Dashboard (chi tiết ở mục 3 và 4.11; quyết định ở `00-claude-instructions.md` mục 6).

## 2. Danh sách màn hình

**Nhóm Tổng quan**
- 4.11. Tổng quan (Dashboard)

*(Ghi chú: số thứ tự tài liệu không phản ánh thứ tự điều hướng — mục "Tổng quan" hiện đầu tiên trong Sidebar dù được đánh số 4.11, đặt cuối để không xáo trộn tham chiếu các mục đã có; xem mục 3.)*

**Nhóm Xác thực**
- 4.1. Đăng nhập
- 4.2. Quên mật khẩu / Đặt lại mật khẩu
- 4.3. Đặt mật khẩu lần đầu (từ lời mời)
- 4.12. Đổi mật khẩu (dialog, dành cho Nhân viên đã đăng nhập)

**Nhóm Nghiên cứu & Xét duyệt** (`/knowledge`, `/gate` — theo Đề tài nghiên cứu được gán)
- 4.4. Danh sách Đề tài nghiên cứu (được gán)
- 4.5. Chi tiết Đề tài nghiên cứu (chỉ xem — vai trò Nghiên cứu/Xét duyệt)
- 4.6. Danh sách Hạng mục tri thức
- 4.7. Màn hình Nghiên cứu (biên tập Hạng mục tri thức)
- 4.8. Màn hình Xét duyệt Hạng mục tri thức (chuyên gia)
- 4.9. Xem & Mở lại Hạng mục tri thức (Đạt xét duyệt / Đã xuất bản / Không xuất bản)
- 4.10. Quản lý & Tiến độ đề tài (vai trò Chủ nhiệm đề tài)

## 3. Quy ước chung — khung ứng dụng & điều hướng

- **Bố cục sau đăng nhập**: Sidebar cố định bên trái + Topbar trên cùng + khu vực nội dung chính — cùng khung với Admin nội bộ (`admin-web-design.md` mục 3), khác app/deploy.
- **Bảng màu (Color Palette)** (bổ sung 2026-09-24): kế thừa từ bảng màu `public-web/public-web-layout.md` mục 2.1, cùng logic với `admin-web-design.md` mục 3 (accent + chữ + viền dùng chung, vùng nội dung chính dùng nền trung tính) — nhưng ấm hơn Admin nội bộ một mức, vì Cổng này là giao diện Nhân viên Tổ chức khác nhìn thấy (đối tác bên ngoài), phạm vi/tần suất thao tác cũng hẹp hơn Admin:

  | Vai trò | Mã màu | Áp dụng |
  |---|---|---|
  | Nền vùng nội dung chính (bảng, form, khu làm việc) | `#FDFBF6` | Toàn bộ khu vực nội dung mục 4.x — kem rất nhạt, ấm hơn nền trắng/xám của `admin-web/` nhưng nhạt hơn nhiều so với `public-web/` |
  | Nền Sidebar / Topbar | `#FAF6EE` | Khung điều hướng (mục này) — giống `public-web/` và `admin-web/` |
  | Accent (màu nhấn chính) | `#A6192E` | Nút hành động chính (CTA), trạng thái active trên Sidebar, logo, link văn bản (hyperlink) trong toàn ứng dụng (vd. breadcrumb, link "Đề tài nghiên cứu cha" ở 4.6/4.7/4.8/4.9, link "Quên mật khẩu?" ở 4.1) |
  | Chữ chính | `#241C15` | Toàn bộ văn bản chính |
  | Chữ phụ | `#7A7166` | Văn bản phụ/mô tả |
  | Viền / divider | `#E7DECD` | Toàn bộ khung ứng dụng |

  Badge trạng thái (xem bullet "Thành phần dùng lại nhiều nơi" bên dưới) dùng bảng màu ngữ nghĩa chuẩn (xanh lá/vàng/đỏ/xanh dương theo convention Quasar) — không theo bảng màu thương hiệu ở trên, cùng nguyên tắc với `admin-web/`.
- **Topbar**: tên Nhân viên, tên Tổ chức trực thuộc (Tổ chức khác — để phân biệt khi một Đề tài có Nhân viên từ nhiều Tổ chức cùng tham gia, §2.2.1.4), **tên nhóm/màn hình hiện tại** (ví dụ "Nghiên cứu & Xét duyệt" hoặc "Tổng quan" — đồng bộ với mục đang highlight ở Sidebar), avatar/dropdown mở **menu tài khoản** gồm: "Đổi mật khẩu" → dialog 4.12; "Đăng xuất" (`POST /auth/logout`). Menu tài khoản hiện cho mọi Nhân viên đã đăng nhập, không phụ thuộc role.
- **Phiên đăng nhập** (`system-design/02-identity.md` mục 3.2 bước 6, 3.5, 5.1):
  - Access token hết hạn (HTTP 401 thông thường): client tự gọi `POST /auth/refresh`, rồi gửi lại request ban đầu. Người dùng không thấy gián đoạn.
  - HTTP 401 `session_revoked`, trả về từ bất kỳ API nào (kể cả `POST /auth/refresh`): phiên đã bị vô hiệu hoá phía máy chủ. Nguyên nhân là tài khoản bị Quản trị hệ thống vô hiệu hoá, hoặc Nhân viên vừa đổi/đặt lại mật khẩu ở nơi khác. Client **không** gọi `POST /auth/refresh` và không gọi `POST /auth/logout`. Client xoá access/refresh token và store Pinia, rồi chuyển thẳng về 4.1 kèm thông báo "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Mã lỗi không cho biết nguyên nhân cụ thể, nên mọi trường hợp dùng chung một thông báo.
  - Không hiện hộp thoại "Thay đổi chưa lưu" khi bị chuyển về do `session_revoked` (ví dụ đang biên tập ở 4.7). Lúc này mọi request lưu đều bị từ chối, nên không còn cách nào giữ lại thay đổi.
  - Sau khi đăng nhập lại, client đưa Nhân viên về đúng màn hình trước đó nếu họ vẫn còn quyền truy cập. Nếu không còn quyền thì về 4.11 (Tổng quan).
- **Sidebar**: mục **"Tổng quan"** luôn hiện đầu tiên (mọi Nhân viên đã đăng nhập, dẫn tới 4.11), tiếp theo là nhóm **"Nghiên cứu & Xét duyệt"**: Đề tài nghiên cứu, Hạng mục tri thức. Mục đang được chọn luôn được highlight rõ ràng (kể cả khi đang ở màn hình con không có mục Sidebar riêng, ví dụ 4.5/4.7/4.8/4.9/4.10 — Sidebar highlight mục cha gần nhất, ở đây là "Đề tài nghiên cứu" hoặc "Hạng mục tri thức" tuỳ đường vào). Mục "Đề tài nghiên cứu" luôn hiện cho mọi Nhân viên đã đăng nhập (việc lọc theo đúng đề tài/role đã xử lý ở tầng dữ liệu, gồm cả role Chủ nhiệm đề tài — mục 4.4). Mục "Hạng mục tri thức" **ẩn** nếu Nhân viên không giữ role `nghien_cuu`/`xet_duyet` ở **bất kỳ** đề tài nào (chỉ giữ `chu_nhiem_de_tai` đơn thuần) — vì không có quyền vào 4.6/4.7/4.8/4.9 (`system-design/03-cultural-knowledge-base.md` mục 5.1); trường hợp này truy cập tiến độ/quản lý nhân sự qua 4.10 (mở từ 4.4).
- **Breadcrumb**: mỗi màn hình con (trừ nhóm Xác thực 4.1–4.3, không thuộc cây phân cấp dữ liệu) hiển thị đường dẫn phân cấp đầy đủ từ nhóm chức năng đến màn hình hiện tại, đặt ngay dưới Topbar, phía trên tiêu đề màn hình — ví dụ "Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}". Mỗi mắt xích (trừ mắt xích cuối, chính là màn hình đang xem) là link điều hướng ngược lại đúng màn hình tương ứng. Breadcrumb là thành phần bắt buộc cho mọi màn hình con, thay cho các link cha rời rạc kiểu cũ.
- **Stepper trạng thái**: áp dụng cho các màn hình thuộc vòng đời Hạng mục tri thức (4.7/4.8/4.9 — Cổng này không có Mục từ nên chỉ có 1 Stepper duy nhất, khác Admin nội bộ). Đặt ngay dưới Breadcrumb, trên phần nội dung màn hình, gộp 9 mã trạng thái thành **5 cụm** hiển thị theo thứ tự trước sau — cùng cách gộp với `admin-web-design.md` mục 3:
  1. **Nghiên cứu** (`dang_nghien_cuu`)
  2. **Chờ & Xác minh AI** (`cho_xet_duyet`, `dang_xet_duyet_ai`)
  3. **Xét duyệt chuyên gia** (`da_qua_xet_duyet_ai`, `dang_xet_duyet`)
  4. **Đạt xét duyệt** (`dat_xet_duyet`)
  5. **Xuất bản** (`da_xuat_ban`/`khong_xuat_ban`)

  "Không đạt xét duyệt" (`khong_dat_xet_duyet`) và "Mở lại" (`reopen`) thể hiện bằng mũi tên cong quay về cụm trước đó, không phải một bước riêng trong Stepper. ⚠ Cụm "Xuất bản" vẫn hiển thị đầy đủ trên Stepper ở cả 3 màn hình 4.7/4.8/4.9 dù Nhân viên Tổ chức khác không tự thực hiện được thao tác Xuất bản/Không xuất bản (thuộc vai trò Xuất bản, ngoài phạm vi Cổng này — mục 6) — Stepper cho biết Hạng mục tri thức đang ở đâu trong toàn bộ vòng đời, kể cả các bước Nhân viên xem không có quyền thao tác. Stepper chỉ hiển thị, không thay thế các nút hành động sẵn có.
- **Thành phần dùng lại nhiều nơi** (cùng khái niệm với `admin-web-design.md` mục 3, tái dùng ở Cổng này):
  - Badge trạng thái (màu theo `status`, cùng 9 mã Hạng mục tri thức).
  - Bảng danh sách có cursor-pagination + filter.
  - Khối "Người phụ trách": hiện tên người đang giữ + nút **Nhận xử lý**/**Nhả** tuỳ quyền. ⚠ Khác Admin nội bộ: Cổng này **không có** nút "Cưỡng chế nhả" — `ForceRelease` chỉ gọi được bởi role `quan_tri_he_thong`, không tồn tại ở giao diện này (`03-cultural-knowledge-base.md` mục 4.2); khi người phụ trách không tự nhả (nghỉ việc, thu hồi quyền...), Nhân viên Tổ chức khác phải liên hệ Quản trị hệ thống xử lý qua Admin nội bộ — ngoài phạm vi thao tác của Cổng này.
  - Bộ chọn vị trí trong file tuỳ theo `file_type` (page/line cho văn bản, vẽ khung cho ảnh, kéo mốc thời gian cho âm thanh/phim) — dùng chung cho Tham chiếu tới Tư liệu gốc và Vị trí trong Nội dung, cả ở chế độ chọn và chế độ chỉ xem/highlight.
- **Mức độ đặc tả hành vi cho từng thao tác**: chỉ mô tả rõ nội dung hộp thoại xác nhận/cảnh báo cho (a) đặc tả gốc yêu cầu cảnh báo rõ, (b) không thể hoàn tác hoặc ảnh hưởng người khác (Mở lại, Xoá), (c) trạng thái khoá nội dung — banner/tooltip nêu rõ lý do khoá, không chỉ ẩn/mờ nút, (d) cảnh báo dữ liệu bất thường (file `is_missing`). Các hành vi UI thông thường khác theo convention chuẩn của Quasar, không đặc tả riêng từng màn hình.
- Mọi endpoint dùng trong tài liệu này thuộc nhóm mount `partner` theo `03-cultural-knowledge-base.md` mục 5.6, trừ `auth/*` mount ở cả `admin` và `partner` (`02-identity.md` mục 5.1).

## 4.1. Đăng nhập

- Form giữa màn hình: input Email, input Mật khẩu, nút "Đăng nhập", link "Quên mật khẩu?".
- Không có lựa chọn "Đăng ký" — Nhân viên không tự tạo tài khoản (§2.1.5.2), kể cả Nhân viên Tổ chức khác (chỉ Quản trị hệ thống ở Admin nội bộ tạo — §1.2.3.3).
- Lỗi hiển thị dùng chung một thông báo ("Email hoặc mật khẩu không đúng") dù sai lý do gì — xem `02-identity.md` mục 3.2.
- Khi bị chuyển về do `session_revoked` (mục 3, bullet "Phiên đăng nhập"): hiện banner thông tin phía trên form, nội dung "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Nếu người dùng mở trang trực tiếp hoặc tự đăng xuất thì không hiện banner.
- Banner thông tin khi bị chuyển về từ 4.12:
  - Đổi mật khẩu thành công: "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới".
  - Bị tạm khoá do nhập sai mật khẩu hiện tại (`login_locked`): "Bạn đã nhập sai mật khẩu hiện tại quá số lần cho phép. Tài khoản tạm khoá đến {locked_until}."
- Vai trò truy cập: không cần đăng nhập. API: `POST /auth/login`.

## 4.2. Quên mật khẩu / Đặt lại mật khẩu

- **Bước 1 — Quên mật khẩu**: input Email, nút gửi. Luôn hiện cùng một thông báo ("Nếu email tồn tại, một link đặt lại mật khẩu đã được gửi") — `02-identity.md` mục 3.3.
- **Bước 2 — Đặt lại mật khẩu** (mở từ link trong email): input Mật khẩu mới + Xác nhận mật khẩu, nút "Đặt lại mật khẩu".
  - Dưới ô Mật khẩu mới hiện danh sách yêu cầu theo chính sách mật khẩu (`GET /auth/password-policy`), kiểm tra ngay khi gõ, cùng cách hiển thị với 4.12. Hai ô đều có nút hiện/ẩn mật khẩu. Nút "Đặt lại mật khẩu" chỉ bật khi mật khẩu mới đạt chính sách và khớp ô xác nhận.
  - `password_policy_violation`: hiện đúng các điều kiện chưa đạt mà backend trả về.
  - Token sai/hết hạn/đã dùng → báo lỗi, hướng dẫn liên hệ Quản trị hệ thống (Tổ chức Văn Minh Việt — không có Quản trị hệ thống ở Cổng này).
  - Thành công: form được thay bằng thông báo ngay tại màn hình này, nội dung "Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại bằng mật khẩu mới.", kèm nút "Quay lại đăng nhập" dẫn tới 4.1. Không tự chuyển trang.
- API: `POST /auth/forgot-password`, `GET /auth/password-policy`, `POST /auth/reset-password`.

## 4.3. Đặt mật khẩu lần đầu (từ lời mời)

- Mở từ link mời trong email → gọi `GET /auth/invite/{token}` để xác thực trước, hiện email (readonly) nếu hợp lệ.
- Input Mật khẩu mới + Xác nhận, nút "Kích hoạt tài khoản". Hiển thị và kiểm tra chính sách mật khẩu cùng cách với 4.2 bước 2. Khi gặp `password_policy_violation`, hiện các điều kiện chưa đạt. Token sai/hết hạn/đã dùng → báo lỗi tương tự mục 4.2.
- Thành công: form được thay bằng thông báo ngay tại màn hình này, nội dung "Kích hoạt tài khoản thành công. Vui lòng đăng nhập.", kèm nút "Quay lại đăng nhập" dẫn tới 4.1. Không tự chuyển trang.
- API: `GET /auth/invite/{token}`, `GET /auth/password-policy`, `POST /auth/accept-invite`.

## 4.4. Danh sách Đề tài nghiên cứu (được gán)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu
- Bảng: Tên, Trạng thái (badge `chuan_bi_tu_lieu`/`tu_lieu_san_sang`), Vai trò của bạn ở đề tài này (chip: "Chủ nhiệm"/"Nghiên cứu"/"Xét duyệt", có thể nhiều), Số Tư liệu gốc đã gán, Số Hạng mục tri thức (tổng), Ngày tạo.
- Filter: theo Trạng thái; tìm theo tên.
- Chỉ liệt kê đề tài mà Nhân viên đang đăng nhập được gán **ít nhất một trong** role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` (lọc theo `employee_role`, `03-cultural-knowledge-base.md` mục 5.1) — không có ngoại lệ "xem toàn bộ" như Quản trị hệ thống ở Admin nội bộ.
- **Không có** nút "+ Tạo Đề tài nghiên cứu" — chỉ Quản trị hệ thống tạo được, ở Admin nội bộ (§2.2.1.4).
- Click dòng → điều hướng theo vai trò tại đề tài đó: có `nghien_cuu` hoặc `xet_duyet` → mở 4.5 (Chi tiết, xem đầy đủ); **chỉ** có `chu_nhiem_de_tai` (không có 2 role kia ở đề tài này) → mở thẳng 4.10 (Quản lý & Tiến độ). Có cả Chủ nhiệm đề tài lẫn Nghiên cứu/Xét duyệt → mở 4.5, kèm nút/link sang 4.10 (xem mục 4.5).
- API: `GET /knowledge/research-topics`.
- Quyền truy cập: role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` (của ít nhất một đề tài).

## 4.5. Chi tiết Đề tài nghiên cứu (chỉ xem — vai trò Nghiên cứu/Xét duyệt)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài}
- Áp dụng khi Nhân viên đang xem giữ role `nghien_cuu` hoặc `xet_duyet` của đề tài này (xem điều hướng ở 4.4). Nếu **đồng thời** giữ `chu_nhiem_de_tai` của đề tài này, hiện thêm link/nút "Quản lý & Tiến độ đề tài (Chủ nhiệm)" → mở 4.10.
- Header: Tên, badge Trạng thái.
- **Không có** nút "Đánh dấu Tư liệu sẵn sàng" — chỉ vai trò Nhập liệu/Quản trị hệ thống, không tồn tại ở Cổng này (§2.2.1.6.2, §2.2.5.1).
- Khối "Tư liệu gốc đã gán": bảng chỉ đọc (Tên, Loại, cảnh báo nếu có file `is_missing`) — **không có** nút "Gỡ" hay ô gán thêm Tư liệu gốc (chỉ vai trò Nhập liệu/Quản trị hệ thống thao tác được, ở Admin nội bộ).
- Khối "Hạng mục tri thức": thống kê số lượng theo từng trạng thái (chip đếm), link mở 4.6 đã lọc sẵn theo đề tài này.
- API: `GET /knowledge/research-topics/{id}`.

## 4.6. Danh sách Hạng mục tri thức

- Breadcrumb: khi vào không lọc theo đề tài — Nghiên cứu & Xét duyệt > Hạng mục tri thức; khi vào từ link lọc sẵn ở 4.5 — Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức.
- Chỉ truy cập được khi Nhân viên giữ role `nghien_cuu`/`xet_duyet` của ít nhất một đề tài — Chủ nhiệm đề tài đơn thuần (không có 2 role này ở đề tài nào) không vào được màn hình này (xem tiến độ qua 4.10 thay thế, `system-design/03-cultural-knowledge-base.md` mục 5.1).
- Bảng: Tiêu đề, Đề tài nghiên cứu (ẩn cột này khi đã vào từ link lọc sẵn theo 1 đề tài ở mục 4.5), Trạng thái (badge, 9 mã — `03-cultural-knowledge-base.md` mục 3.2), Người phụ trách (tên hoặc "Chưa có"), **Người tạo** (`created_by`, §2.2.3.12), cảnh báo nếu `has_missing_source_files = true`, Ngày tạo (§2.2.3.13).
- Filter: theo Đề tài nghiên cứu (chỉ liệt kê đề tài được gán `nghien_cuu`/`xet_duyet`), theo Trạng thái.
- Nút "+ Tạo Hạng mục tri thức" — chỉ hiện khi Nhân viên đang giữ role `nghien_cuu` của ít nhất một đề tài (trong số đề tài được gán) đang `tu_lieu_san_sang`; dialog chọn Đề tài nghiên cứu (chỉ liệt kê đề tài thoả điều kiện trên) + nhập Tiêu đề. Submit xong điều hướng sang 4.7.
- Action inline theo dòng: "Xoá" (§2.2.3.14) — chỉ enable khi `status = dang_nghien_cuu`, disable kèm tooltip "Chỉ xoá được khi đang ở trạng thái Đang nghiên cứu" ở trạng thái khác; hiện với Chủ nhiệm đề tài của đề tài cha hoặc `assignee_id` hiện tại (§2.2.3.14.4 — khi chưa có Người phụ trách, chỉ Chủ nhiệm đề tài thấy nút này ở Cổng này, vì không có `quan_tri_he_thong`). Hộp thoại xác nhận (không hoàn tác — quy ước (b) mục 3): "Xoá sẽ xoá vĩnh viễn Nội dung/Phát biểu/Tham chiếu của Hạng mục tri thức này. Tư liệu gốc không bị ảnh hưởng. Tiếp tục?"; nếu backend từ chối (đã có phiên bản chốt hoặc đã bị Mục từ tham chiếu), hiện thông báo lỗi tương ứng.
- Click dòng → điều hướng theo `status`: `dang_nghien_cuu`/`cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet` → 4.7; `da_qua_xet_duyet_ai`/`dang_xet_duyet` → 4.8; `dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban` → 4.9.
- API: `GET /knowledge/knowledge-objects`, `POST /knowledge/knowledge-objects`, `DELETE /knowledge/knowledge-objects/{id}`.
- Quyền truy cập: giới hạn theo đề tài được gán role `nghien_cuu`/`xet_duyet` — **không** có ngoại lệ xem toàn bộ (khác Admin nội bộ, `03-cultural-knowledge-base.md` mục 3.5).

## 4.7. Màn hình Nghiên cứu (biên tập Hạng mục tri thức)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (mục 3): active tại cụm "Nghiên cứu" khi `status = dang_nghien_cuu` hoặc `khong_dat_xet_duyet` (trường hợp `khong_dat_xet_duyet` thể hiện thêm mũi tên cong quay lại từ cụm "Xét duyệt chuyên gia"); active tại cụm "Chờ & Xác minh AI" khi `status = cho_xet_duyet`/`dang_xet_duyet_ai`.
- Áp dụng khi Hạng mục tri thức đang ở `dang_nghien_cuu`, `cho_xet_duyet`, `dang_xet_duyet_ai`, hoặc `khong_dat_xet_duyet`.
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha (→ 4.5).
- Khối "Người phụ trách": tên đang giữ (nếu có) + nút "Nhận xử lý" (`Claim`, hiện khi `assignee_id` đang trống và người xem giữ role `nghien_cuu` của đề tài) / "Nhả" (`Release`, hiện khi `assignee_id` = người xem).
- Khối Nội dung (`knowledge_object_file`, §2.2.3.6 — sản phẩm biên tập của vai trò Nghiên cứu): danh sách file đã tải lên (tên, loại, kích thước, nút xem/tải), nút "+ Tải file lên" (upload trực tiếp qua presigned URL, không phải trình soạn thảo trực tuyến — `03-cultural-knowledge-base.md` mục 2.7).
  - Chỉnh sửa (tải lên/gỡ file, thêm/sửa/xoá Phát biểu & Tham chiếu) chỉ mở khi `status = dang_nghien_cuu` **và** người xem là `assignee_id` hiện tại — các trạng thái/người xem khác chỉ đọc, kèm banner nêu rõ lý do khoá.
- Khối Phát biểu (`claim`): bảng liệt kê nội dung, danh sách Tham chiếu (chip: Tư liệu gốc + vị trí) kèm cảnh báo nếu `source_file.is_missing = true`, Vị trí trong Nội dung (nếu có khai báo). Nút "+ Thêm Phát biểu" mở form: nội dung, chọn file Nội dung + bộ chọn vị trí (không bắt buộc), thêm một hoặc nhiều Tham chiếu (chọn Tư liệu gốc đã gán cho đề tài → chọn file → bộ chọn vị trí theo `file_type`) — bước "chọn Tư liệu gốc → chọn file" gọi `GET /knowledge/research-topics/{id}/sources/{source_id}` (mount `admin`, `partner` — `system-design/03-cultural-knowledge-base.md` mục 5.1).
- Khối "Gợi ý AI" (`ai_missed_claims_suggestions`, §2.2.6.6.5): chỉ đọc, hiện khi có dữ liệu.
- Vùng trạng thái/hành động cuối trang theo `status`:
  - `dang_nghien_cuu`: nút "Gửi xét duyệt" (`submit-for-review`, chỉ `assignee_id` hiện tại, tự động kích hoạt AI Verification); nút "Xoá Hạng mục tri thức" (§2.2.3.14, cùng điều kiện/hộp thoại như action "Xoá" ở 4.6 — hiện với Chủ nhiệm đề tài của đề tài cha hoặc `assignee_id` hiện tại).
  - `cho_xet_duyet`: hiện "Đang chờ kích hoạt AI Verification".
  - `dang_xet_duyet_ai`: hiện "Đang chạy AI Verification..." (không có hành động, chỉ chờ job nền).
  - Cả `cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet`: nút "Kích hoạt lại AI Verification" (`trigger-ai-verification`, role `nghien_cuu`/`xet_duyet` của đề tài).
  - `khong_dat_xet_duyet`: hiện ghi chú không đạt (`ai_note`/`expert_note` gộp lại). Nút "Quay lại nghiên cứu" (`resume-research`, role `nghien_cuu` của đề tài — không giới hạn theo `assignee_id`).
- API: `GET /knowledge/knowledge-objects/{id}`, `GET /knowledge/research-topics/{id}/sources/{source_id}`, `POST/DELETE .../files`, `POST/PATCH/DELETE .../claims`, `POST/DELETE .../claims/{claim_id}/references`, `POST .../submit-for-review`, `POST .../trigger-ai-verification`, `POST .../claim`, `POST .../release`, `POST .../resume-research`, `DELETE /knowledge/knowledge-objects/{id}`.

## 4.8. Màn hình Xét duyệt Hạng mục tri thức (chuyên gia)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (mục 3): active tại cụm "Xét duyệt chuyên gia" (`da_qua_xet_duyet_ai`/`dang_xet_duyet`).
- Áp dụng khi Hạng mục tri thức đang ở `da_qua_xet_duyet_ai` (chưa ai nhận xử lý) hoặc `dang_xet_duyet` (chuyên gia đang xử lý).
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha. Banner "Nội dung bị khoá" khi `dang_xet_duyet`.
- Khối "Người phụ trách": nút "Nhận xử lý" (`Claim`, hiện tại `da_qua_xet_duyet_ai`, role `xet_duyet` của đề tài — ghi đè `assignee_id`, đồng thời chuyển `status → dang_xet_duyet`) / "Nhả" (`Release`, chỉ `assignee_id` hiện tại, lùi về `da_qua_xet_duyet_ai`).
- Khối Nội dung: xem file đã upload (đọc, không sửa).
- Khối Phát biểu — với mỗi Phát biểu, hiện từng Tham chiếu và Vị trí trong Nội dung (nếu có) kèm: vị trí (mở file kèm highlight), kết quả AI (`ai_verdict`/`ai_note` hoặc `content_ai_verdict`/`content_ai_note` — chỉ đọc), cảnh báo nếu `source_file.is_missing = true`, form ghi kết luận chuyên gia (`expert_verdict`/`expert_note` hoặc `content_expert_verdict`/`content_expert_note`) — chỉ hiện/enable khi `status = dang_xet_duyet` và người xem là `assignee_id` hiện tại.
- Khối "Gợi ý AI" — tham khảo, cùng cơ chế 4.7.
- Nút cuối trang (chỉ `assignee_id` hiện tại, tại `dang_xet_duyet`): "Không đạt xét duyệt" (`reject` → `khong_dat_xet_duyet`) và "Đạt xét duyệt" (`approve` → `dat_xet_duyet`) — giao diện cảnh báo mềm (không chặn) nếu còn Tham chiếu/Vị trí chưa có `expert_verdict`.
- Nút "Kích hoạt lại AI Verification" — chỉ hiện tại `da_qua_xet_duyet_ai` (chưa `Claim`).
- API: `GET /knowledge/knowledge-objects/{id}/claims`, `POST .../claim`, `POST .../release`, `POST .../claims/{claim_id}/references/{reference_id}/review`, `POST .../claims/{claim_id}/content-review`, `POST .../reject`, `POST .../approve`, `POST .../trigger-ai-verification`.

## 4.9. Xem & Mở lại Hạng mục tri thức (Đạt xét duyệt / Đã xuất bản / Không xuất bản)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (mục 3): active tại cụm "Đạt xét duyệt" khi `status = dat_xet_duyet`; active tại cụm "Xuất bản" khi `status = da_xuat_ban`/`khong_xuat_ban`.
- Áp dụng khi Hạng mục tri thức đang ở `dat_xet_duyet`, `da_xuat_ban`, hoặc `khong_xuat_ban` — cả 3 trạng thái đều "Nội dung bị khoá" (banner).
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha, Người phụ trách (chỉ hiển thị).
- Khối Nội dung/Phát biểu: xem lại toàn bộ (đọc, tái dùng view của 4.8) kèm kết quả xét duyệt AI + chuyên gia cuối cùng.
- Tại `dat_xet_duyet`: hiện ghi chú "Đang chờ vai trò Xuất bản quyết định Xuất bản/Không xuất bản — thao tác này không thuộc phạm vi Cổng Nhân viên Tổ chức khác (§2.7.2 đặc tả gốc)". **Không có** nút hành động nào cho vai trò Xuất bản ở màn hình này (xem mục 6) — chỉ xem.
- Tại `da_xuat_ban`: hiện "Đã xuất bản lúc {frozen_at} bởi {frozen_by}", số phiên bản (`version_number`) vừa tạo.
- Tại `khong_xuat_ban`: hiện thời điểm chuyển trạng thái.
- Cả `da_xuat_ban`/`khong_xuat_ban`: nút "Mở lại" — **chỉ role `xet_duyet` của đề tài**, mở dialog chọn trạng thái đích trong 4 lựa chọn (`dang_nghien_cuu`/`cho_xet_duyet`/`da_qua_xet_duyet_ai`/`dang_xet_duyet`) kèm cảnh báo không hoàn tác/ảnh hưởng người khác: "Mở lại sẽ đưa Hạng mục tri thức quay lại quy trình xét duyệt, Người phụ trách hiện tại (nếu có) được giữ nguyên. Tiếp tục?" (`reopen`, body `{target_status}`).
- Khối "Lịch sử phiên bản" (luôn hiện nếu đã có ≥1 phiên bản chốt): bảng các phiên bản đã chốt (Số phiên bản, Thời điểm chốt, Người chốt), click 1 dòng → xem snapshot chỉ đọc (`GET .../versions/{version_id}`).
- **Không có** khối "Phiên bản đang được sử dụng" / nút "Chọn/Đổi phiên bản đang dùng" — thuộc thao tác riêng của vai trò Xuất bản (§2.2.3.4.1, §2.2.5.4), ngoài phạm vi Cổng này (xem mục 6).
- API: `GET /knowledge/knowledge-objects/{id}`, `GET .../versions/{version_id}`, `POST .../reopen`.

## 4.10. Quản lý & Tiến độ đề tài (vai trò Chủ nhiệm đề tài)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Quản lý & Tiến độ đề tài
- Áp dụng cho Nhân viên giữ role `chu_nhiem_de_tai` của đề tài đang xem (§2.2.5.5) — mở từ 4.4 (điều hướng thẳng nếu chỉ giữ Chủ nhiệm đề tài ở đề tài này) hoặc từ link trong 4.5 (nếu đồng thời giữ Nghiên cứu/Xét duyệt).
- Header: Tên đề tài, badge Trạng thái.
- Khối "Chủ nhiệm đề tài": hiện tên Nhân viên đang giữ (chính người xem) — **không có** nút đổi Chủ nhiệm ở Cổng này (§2.2.1.4 — chỉ Quản trị hệ thống đổi được, thực hiện ở Admin nội bộ).
- Khối "Quản lý nhân sự đề tài" (§2.2.1.4): 2 bảng con "Nghiên cứu" và "Xét duyệt", mỗi bảng liệt kê Nhân viên đang giữ role tương ứng của đề tài này + nút "Gỡ" từng dòng, cùng ô tìm/thêm Nhân viên (không giới hạn Tổ chức — một Đề tài có thể có Nhân viên từ nhiều Tổ chức khác nhau, §2.2.1.4). API: `GET .../members`, `POST/DELETE .../researchers`, `POST/DELETE .../reviewers`.
- Khối "Tiến độ" (§2.2.5.5/§2.7.3.5): thống kê số Hạng mục tri thức theo từng trạng thái (chip đếm) + bảng danh sách rút gọn (Tiêu đề, Trạng thái, Người phụ trách, Người tạo) — **không** có link mở chi tiết (không có quyền xem Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt, §2.2.5.5). Action inline "Xoá" (§2.2.3.14) trên mỗi dòng — cùng điều kiện/hộp thoại như 4.6 (chỉ enable khi `status = dang_nghien_cuu`; quyền ở đây luôn hợp lệ vì người xem là Chủ nhiệm đề tài của đề tài cha).
- **Không có** khối Tư liệu gốc — ngoài phạm vi vai trò Chủ nhiệm đề tài (§2.7.3.4–5 chỉ liệt kê quản lý nhân sự + xem tiến độ + xoá Hạng mục tri thức).
- API: `GET /knowledge/research-topics/{id}/progress`, `GET .../members`, `POST/DELETE .../researchers`, `POST/DELETE .../reviewers`, `DELETE /knowledge/knowledge-objects/{id}`.

## 4.11. Tổng quan (Dashboard)

- Không có Breadcrumb (màn hình gốc, luôn là mục đầu tiên trong Sidebar).
- **Mục tiêu chính**: giúp Nhân viên Tổ chức khác hiểu được vị trí công việc của mình trong toàn bộ pipeline nghiệp vụ Văn Minh Việt (dù phạm vi thao tác chỉ gói gọn trong giai đoạn Nghiên cứu & Xét duyệt của Hạng mục tri thức) — hơn là cung cấp số liệu thống kê. Toàn bộ nội dung màn hình là **nội dung tĩnh**, không có chip đếm và không phụ thuộc API mới nào.
- **Khối 1 — Sơ đồ phạm vi công việc** (thành phần chính, đặt đầu trang): sơ đồ tĩnh thể hiện vị trí của Cổng này trong toàn bộ pipeline nghiệp vụ (đối chiếu `admin-web-design.md` mục 4.22 — sơ đồ đầy đủ ở Admin nội bộ), làm rõ đâu là phần Nhân viên Tổ chức khác tham gia được và đâu không:
  1. **Đề tài nghiên cứu** (2 trạng thái: Chuẩn bị tư liệu → Tư liệu sẵn sàng, do Quản trị hệ thống khởi tạo ở Admin nội bộ) — vai trò của bạn ở bước này: Chủ nhiệm đề tài (nếu được gán) điều phối nhân sự Nghiên cứu/Xét duyệt trong đề tài. Click → mở 4.4.
  2. **Tư liệu gốc** (đồng bộ từ MinIO/S3, do vai trò Nhập liệu ở Admin nội bộ quản lý) — hiển thị mờ, không click được: chỉ để biết đây là bước trước, **ngoài phạm vi Cổng này**.
  3. **Hạng mục tri thức** — 5 cụm trạng thái, cùng cách gộp với Stepper ở mục 3: Nghiên cứu (vai trò Nghiên cứu — **thuộc phạm vi Cổng này**) → Chờ & Xác minh AI (tự động) → Xét duyệt chuyên gia (vai trò Xét duyệt — **thuộc phạm vi Cổng này**) → Đạt xét duyệt → Xuất bản (vai trò Xuất bản — **ngoài phạm vi Cổng này**, thực hiện ở Admin nội bộ). Click → mở 4.6 (nếu Nhân viên có role Nghiên cứu/Xét duyệt ở ít nhất 1 đề tài).
  4. **Mục từ** (rẽ nhánh từ cụm "Xuất bản" của Hạng mục tri thức) — hiển thị mờ, không click được: **hoàn toàn ngoài phạm vi Cổng này**, do đội ngũ Biên tập/Xét duyệt Mục từ/Xuất bản Mục từ của Văn Minh Việt thực hiện ở Admin nội bộ.

  2 cụm "Nghiên cứu" và "Xét duyệt chuyên gia" (thuộc phạm vi Cổng này) được làm nổi bật trực quan trên sơ đồ ứng với (các) role mà Nhân viên đang đăng nhập đang giữ ở ít nhất một đề tài, để thấy ngay công việc của mình nằm ở đâu trong toàn bộ pipeline — kể cả các bước ngoài phạm vi thao tác của mình. Sơ đồ không hiển thị số liệu/số đếm.
- **Khối 2 — Mô tả vai trò của bạn** (đặt dưới sơ đồ, văn bản ngắn, chỉ hiện đoạn tương ứng (các) role Nhân viên đang giữ ở ít nhất 1 đề tài):
  - **Nghiên cứu**: biên tập Nội dung/Phát biểu/Tham chiếu cho Hạng mục tri thức thuộc đề tài được gán, gửi đi xét duyệt. → 4.6.
  - **Xét duyệt**: thẩm định Hạng mục tri thức đã qua AI Verification, ghi kết luận chuyên gia, quyết định Đạt/Không đạt xét duyệt; có thể Mở lại Hạng mục tri thức đã xuất bản/không xuất bản. → 4.6.
  - **Chủ nhiệm đề tài**: quản lý nhân sự Nghiên cứu/Xét duyệt và theo dõi tiến độ của (các) đề tài mình phụ trách, không xem được Nội dung/Phát biểu/Tham chiếu chi tiết. → 4.4 (từ đó điều hướng tới 4.10 của từng đề tài).
- Quyền truy cập: mọi Nhân viên đã đăng nhập (nội dung Khối 1/Khối 2 tự điều chỉnh theo (các) role đang giữ như trên).
- API: không có — toàn bộ nội dung tĩnh, không gọi API đếm số liệu nào.

## 4.12. Đổi mật khẩu

- Dạng dialog, không có route và không có Breadcrumb riêng. Mở từ "Đổi mật khẩu" trong menu tài khoản trên Topbar (mục 3), ở bất kỳ màn hình nào.
- Quyền truy cập: mọi Nhân viên đã đăng nhập, không phụ thuộc role. Nhân viên chỉ đổi được mật khẩu của chính mình (backend xác định theo access token, request không gửi `employee_id`). Đây là thao tác trên tài khoản của chính mình, không thuộc phạm vi cấm quản lý người dùng ở §2.7.4.
- Nếu màn hình đang mở có thay đổi chưa lưu (ví dụ 4.7), bấm "Đổi mật khẩu" sẽ hiện hộp thoại "Thay đổi chưa lưu sẽ bị mất khi đổi mật khẩu. Tiếp tục?" trước khi mở dialog, vì đổi mật khẩu thành công sẽ đăng xuất ngay.
- Form:
  - Mật khẩu hiện tại.
  - Mật khẩu mới. Bên dưới hiện danh sách yêu cầu theo chính sách mật khẩu đang cấu hình (`GET /auth/password-policy`: độ dài tối thiểu, có cả chữ và số, có ký tự đặc biệt). Hệ thống kiểm tra ngay khi gõ, dòng nào đạt thì hiện tick xanh.
  - Xác nhận mật khẩu mới.
  - Cả 3 ô đều có nút hiện/ẩn mật khẩu.
  - Nút "Huỷ" và "Đổi mật khẩu". Nút "Đổi mật khẩu" chỉ bật khi đủ 3 ô, mật khẩu mới đạt chính sách, khớp ô xác nhận và khác mật khẩu hiện tại.
- Dòng lưu ý ngay trên các nút: "Sau khi đổi mật khẩu, bạn sẽ bị đăng xuất khỏi mọi thiết bị và cần đăng nhập lại."
- Lỗi từ backend (`system-design/02-identity.md` mục 3.4, 5.1):
  - `invalid_current_password` (422): báo lỗi dưới ô "Mật khẩu hiện tại" là "Mật khẩu hiện tại không đúng". Dialog vẫn mở.
  - `password_unchanged` (422): báo lỗi dưới ô "Mật khẩu mới" là "Mật khẩu mới phải khác mật khẩu hiện tại".
  - `password_policy_violation` (422): hiện đúng các điều kiện chưa đạt mà backend trả về (trường hợp chính sách vừa đổi sau lúc mở dialog).
  - `login_locked` (423, kèm `locked_until`): client gọi `GET /auth/me` để kiểm tra phiên.
    - Nếu nhận 401 `session_revoked` (vừa bị tạm khoá do nhập sai mật khẩu hiện tại ngay trong dialog, phiên đã bị vô hiệu hoá): xoá token và store, không gọi `POST /auth/logout`, rồi về 4.1 kèm banner tạm khoá (mục 4.1).
    - Nếu phiên vẫn hợp lệ (tài khoản đang bị tạm khoá từ trước, do đăng nhập sai ở nơi khác): giữ nguyên phiên, dialog hiện lỗi "Tài khoản đang tạm khoá do đăng nhập sai nhiều lần. Bạn có thể đổi mật khẩu sau {locked_until}." Nút "Đổi mật khẩu" bị tắt cho tới thời điểm đó.
  - 401 `session_revoked`: xử lý theo mục 3, bullet "Phiên đăng nhập".
- Thành công (204): backend thu hồi toàn bộ refresh token và vô hiệu hoá mọi phiên (`02-identity.md` mục 3.4 bước 6, 3.5). Client xoá token và store, không gọi `POST /auth/logout`, rồi về 4.1 kèm banner "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới". Sau khi đăng nhập lại, client đưa Nhân viên về màn hình trước đó theo cùng quy tắc ở mục 3, bullet "Phiên đăng nhập".
- Không có email thông báo sau khi đổi mật khẩu (§2.1.5.10.4).
- API: `GET /auth/password-policy`, `GET /auth/me`, `POST /auth/change-password` (body `{current_password, new_password}`).

## 5. Đối chiếu với Business Requirements / System Design — quy trình xử lý điểm lệch

*(xem `partner-web/00-claude-instructions.md` mục 5)*

## 6. Quyết định đã chốt

- **Vai trò Xuất bản không thuộc phạm vi Cổng này** (`business-requirements.md` §2.7.2) — khớp `system-design/03-cultural-knowledge-base.md` (`/publish`, `/skip-publish`, `/set-used-version` chỉ mount `admin`).
- **Route đọc file Tư liệu gốc ở `partner`**: `GET /knowledge/research-topics/{id}/sources/{source_id}` (mount `admin`, `partner`).
- **Chủ nhiệm đề tài** (§2.2.5.5/§2.7.3.4–5): màn hình riêng 4.10 (tách khỏi 4.5 vì phạm vi xem khác — không xem được Nội dung/Hạng mục tri thức chi tiết); nút "Xoá" Hạng mục tri thức (§2.2.3.14) ở 4.6/4.7/4.10 — chỉ Chủ nhiệm đề tài của đề tài cha hoặc `assignee_id` hiện tại (không có `quan_tri_he_thong` ở Cổng này); không có nút đổi Chủ nhiệm đề tài ở Cổng này (`set-chair` chỉ mount `admin`).
- **Stepper trạng thái (4.7/4.8/4.9)**: hiển thị đầy đủ cụm "Xuất bản" dù Nhân viên không tự thao tác được — mục đích là cho biết vị trí trong toàn bộ vòng đời, không chỉ liệt kê bước tự làm được.
- **Dashboard (4.11)**: nội dung tĩnh — sơ đồ phạm vi công việc + mô tả theo role, không có chip đếm, không phụ thuộc API `stats`.

## 7. Trạng thái hiện tại

- Đã thiết kế đủ 12 màn hình (4.1–4.12), khớp `business-requirements.md` §1.2.3.2, §2.7, §2.2.5.5, §2.2.1.7, §2.2.3.14, §2.1.5.10 và `system-design/01, 02, 03`.
- Không còn điểm lệch nào đang mở. Tài liệu sẵn sàng làm đầu vào build.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-common-instructions.md` mục 4.
