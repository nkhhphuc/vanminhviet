# Đặc Tả Giao Diện Cổng Nhân Viên Tổ Chức Khác — Văn Minh Việt

> Xem khung làm việc và nguyên tắc tại `partner-web/00-claude-instructions.md`. Lịch sử thay đổi tại `partner-web/changelog.md`.

## 1. Tổng quan

- **Mục đích cốt lõi:** hỗ trợ nghiên cứu văn hóa và lịch sử của dân tộc Việt Nam.
- Quasar (Vue 3) + Pinia, **app/deploy riêng** khỏi Admin nội bộ (R-GEN-010 (§1.2.3.2), R-PTN-001 (§2.7) đặc tả gốc; D-SD01-001 (¶1)) — dành cho Nhân viên thuộc Tổ chức khác (viện nghiên cứu ngoài). ⚠ Nhân viên Tổ chức Văn Minh Việt (Tổ chức nội bộ) cũng đăng nhập được Cổng này, với phiên đăng nhập riêng, tách khỏi Admin nội bộ (D-SD02-004 (¶3.2) bước 2b). Điều này vượt ngoài R-GEN-010 (§1.2.3.2).
- Thực hiện 3 vai trò theo phạm vi Đề tài nghiên cứu được gán: **vai trò Nghiên cứu** (`nghien_cuu`), **vai trò Xét duyệt** (`xet_duyet`) (R-PTN-003 (§2.7.2) đặc tả gốc), và **vai trò Chủ nhiệm đề tài** (`chu_nhiem_de_tai`, R-KB-073 (§2.2.5.5)/R-PTN-008 (§2.7.3.4)–R-PTN-009 (§2.7.3.5) — có thể thuộc Tổ chức khác, không chỉ Văn Minh Việt) — không có Nhập liệu, Xuất bản, Biên tập, Xét duyệt Mục từ, Quản trị hệ thống. Ở Cổng này chỉ role theo phạm vi Đề tài có hiệu lực. `roles` trong `auth.login`/`auth.getMe` chỉ gồm role theo phạm vi. Role chức năng mà Nhân viên nội bộ đang giữ (kể cả `quan_tri_he_thong`) không cho thêm quyền hay ngoại lệ nào (D-SD02-009 (¶5.1), D-SD03-021 (¶5.1)). Không có màn hình quản lý người dùng/phân quyền/Tổ chức dù giữ vai trò gì (R-PTN-010 (§2.7.4)); riêng việc Chủ nhiệm đề tài quản lý nhân sự Nghiên cứu/Xét duyệt **trong đúng đề tài mình phụ trách** không thuộc phạm vi cấm này (R-KB-073 (§2.2.5.5) — khác quản lý người dùng toàn hệ thống).
- **Phạm vi xem khác nhau theo vai trò**: Nghiên cứu/Xét duyệt xem được Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt (D-PRT-005 (¶4.5)–D-PRT-009 (¶4.9)). Chủ nhiệm đề tài — khi **không** đồng thời giữ Nghiên cứu/Xét duyệt của đề tài đó — chỉ xem được tiến độ (Tiêu đề/Trạng thái/Người phụ trách/Người tạo) và quản lý nhân sự đề tài, **không** xem được Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt (D-SD03-021 (¶5.1)) — xem màn hình riêng D-PRT-010 (¶4.10).
- Ranh giới route đã chốt ở D-SD01-002 (¶2): nhóm `/api/v1/partner/...` chỉ mount phần Nghiên cứu/Xét duyệt/quản lý nhân sự đề tài trong `knowledge`/`gate` (chi tiết endpoint ở `03` ¶5), cùng nhóm `auth/*` (mọi Nhân viên tự xác thực, D-SD02-009 (¶5.1)) — **không mount** `identity`, `ingestion`, `encyclopedia`. Phiên đăng nhập gắn với kênh `partner`: token cấp ở Cổng này không dùng được ở Admin nội bộ và ngược lại (D-SD02-004 (¶3.2)).
- Mức độ đặc tả: wireframe/mô tả bố cục đủ dùng cho dev, không mockup chi tiết layout/spacing như `public-web/` (theo `00-claude-instructions.md` mục 1) — cùng mức với `admin-web/`. Riêng bảng màu, font và bo góc (xem D-PRT-013 (¶3)) được định nghĩa để đảm bảo nhất quán nhận diện thương hiệu với `public-web/` và landing vanminhviet.org.
- Một Nhân viên có thể giữ role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` của **nhiều Đề tài nghiên cứu khác nhau** cùng lúc (R-KB-006 (§2.2.1.4), R-KB-070 (§2.2.5.2)–R-KB-071 (§2.2.5.3), R-KB-073 (§2.2.5.5)) → mọi danh sách/thao tác trong tài liệu này đều giới hạn theo đúng phạm vi đề tài mà Nhân viên đang đăng nhập được gán, không có khái niệm "xem toàn bộ" như Quản trị hệ thống ở Admin nội bộ (D-SD03-014 (¶3.5) nêu rõ ngoại lệ xem toàn bộ **không áp dụng** cho nhóm route `partner`).
- **Nguyên tắc giao diện**: giao diện cần giúp người dùng luôn thấy được bức tranh tổng thể (cấu trúc điều hướng/phân cấp dữ liệu của Cổng này) và vị trí chức năng hiện tại nằm ở đâu trong đó — thực hiện qua Breadcrumb, Stepper trạng thái, Sidebar/Topbar, và màn hình Dashboard (chi tiết ở D-PRT-013 (¶3) và D-PRT-011 (¶4.11); quyết định ở `00-claude-instructions.md` mục 6). Đáp ứng R-NFR-037 (§3.7): ngoài các cơ chế trên, nút thao tác đọc theo `actions`, lý do khi chưa thực hiện được, trạng thái kế tiếp và vai trò xử lý tiếp, tham số cấu hình tại nơi thao tác (D-PRT-013 (¶3)).

## 2. Danh sách màn hình

**Nhóm Tổng quan**
- 4.11. Tổng quan (Dashboard)

*(Ghi chú: số thứ tự tài liệu không phản ánh thứ tự điều hướng — mục "Tổng quan" hiện đầu tiên trong Sidebar dù được đánh số D-PRT-011 (¶4.11), đặt cuối để không xáo trộn tham chiếu các mục đã có; xem D-PRT-013 (¶3).)*

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
- 4.13. Chi tiết Tư liệu gốc (chỉ xem — vai trò Nghiên cứu/Xét duyệt)

## 3. [D-PRT-013] Quy ước chung — khung ứng dụng & điều hướng

- **Bố cục sau đăng nhập**: Sidebar cố định bên trái + Topbar trên cùng + khu vực nội dung chính — cùng khung với Admin nội bộ (D-ADM-029 (¶3)), khác app/deploy.
- **Không lập chỉ mục** (R-NFR-032 (§3.6.6), D-SD01-007 (¶7)): Cổng này phục vụ `robots.txt` chặn toàn bộ; reverse proxy gắn header `X-Robots-Tag: noindex, nofollow`.
- **Bố cục trước đăng nhập** (D-PRT-001 (¶4.1)–D-PRT-003 (¶4.3)): không có Sidebar, Topbar, Breadcrumb; form đặt giữa màn hình; chip "DEV" (bullet Topbar) ở góc trên phải màn hình.
- **Bảng màu (Color Palette)**: kế thừa bảng màu D-PUB-011 (¶2.1) (nhận diện dùng chung với landing vanminhviet.org), cùng logic với D-ADM-029 (¶3) (accent + chữ + viền dùng chung, vùng nội dung chính dùng nền trung tính) — riêng nền vùng nội dung ấm hơn Admin nội bộ một mức, vì Cổng này là giao diện Nhân viên Tổ chức khác nhìn thấy (đối tác bên ngoài), phạm vi/tần suất thao tác cũng hẹp hơn Admin:

  | Vai trò | Mã màu | Áp dụng |
  |---|---|---|
  | Nền vùng nội dung chính (bảng, form, khu làm việc) | `#FDFBF6` | Toàn bộ khu vực nội dung của các màn hình — kem rất nhạt, ấm hơn nền trắng/xám của `admin-web/` nhưng nhạt hơn nền chính `#F7F2EA` của `public-web/` |
  | Nền Sidebar / Topbar | `#F7F2EA` | Khung điều hướng (mục này) — trùng nền chính của D-PUB-011 (¶2.1) |
  | Accent (màu nhấn chính) | `#C4171D` | Nút hành động chính (CTA), trạng thái active trên Sidebar, logo, link văn bản (hyperlink) trong toàn ứng dụng (vd. breadcrumb, link "Đề tài nghiên cứu cha" ở D-PRT-006 (¶4.6)/D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9), link "Quên mật khẩu?" ở D-PRT-001 (¶4.1)) |
  | Accent đậm | `#9C2B2B` | Trạng thái hover/pressed của phần tử dùng Accent (nút CTA, link) |
  | Chữ trên nền Accent | `#FFFFFF` | Mọi chữ/icon đặt trên nền Accent hoặc Accent đậm |
  | Chữ chính | `#252421` | Toàn bộ văn bản chính |
  | Chữ phụ | `#6D6A64` | Văn bản phụ/mô tả |
  | Viền / divider | `#E6E0D7` | Toàn bộ khung ứng dụng |

  Hai màu phụ vàng đồng `#C8944A` và xanh rêu `#2F4B3F` của D-PUB-011 (¶2.1) không dùng ở Cổng này.

  **Quy tắc tương phản chữ/nền**: trên nền `#FDFBF6`/`#F7F2EA` chỉ dùng Chữ chính/Chữ phụ/Accent, **không dùng `#FFFFFF`**; trên nền Accent/Accent đậm chỉ dùng `#FFFFFF`. Các cặp màu phát sinh ngoài bảng trên đạt tối thiểu 4.5:1 (WCAG 2.1 AA) với chữ thường, 3:1 với chữ ≥ 18px hoặc đậm ≥ 14px và icon. Với component Quasar có sẵn cặp màu nền/chữ mặc định (`QHeader` mặc định `bg-primary text-white`…), khi đổi màu nền thì phải đặt lại cả màu chữ theo quy tắc này.

  Badge trạng thái (xem bullet "Thành phần dùng lại nhiều nơi" bên dưới) dùng bảng màu ngữ nghĩa chuẩn (xanh lá/vàng/đỏ/xanh dương theo convention Quasar) — không theo bảng màu thương hiệu ở trên, cùng nguyên tắc với `admin-web/`.
- **Typography**: sans-serif **Be Vietnam Pro** (400/500/600/700) cho toàn bộ giao diện (Sidebar, Topbar, Breadcrumb, bảng, form, nút, nội dung), dự phòng `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`; serif **Lora** (600) chỉ cho logo/chữ "VĂN MINH VIỆT" và tiêu đề màn hình (H1), dự phòng `Georgia, "Times New Roman", serif`. Nạp kèm subset `vietnamese`. Cùng bộ font với `public-web/`.
- **Bo góc & hình ảnh**: card, dialog, ô nhập liệu, nút bo góc 8px; chip và badge trạng thái dạng pill. Không dùng ảnh minh hoạ trang trí. Logo dùng logo của landing vanminhviet.org.
- **Topbar**: tên Nhân viên, tên Tổ chức trực thuộc (`organization_name`; với Nhân viên nội bộ là Văn Minh Việt — để phân biệt khi một Đề tài có Nhân viên từ nhiều Tổ chức cùng tham gia, R-KB-006 (§2.2.1.4)), **tên nhóm/màn hình hiện tại** (ví dụ "Nghiên cứu & Xét duyệt" hoặc "Tổng quan" — đồng bộ với mục đang highlight ở Sidebar), avatar/dropdown mở **menu tài khoản** gồm: "Đổi mật khẩu" → dialog D-PRT-012 (¶4.12); "Đăng xuất" (`auth.logout`). Menu tài khoản hiện cho mọi Nhân viên đã đăng nhập, không phụ thuộc role.
  - **Chip "DEV"** (D-SD01-009 (¶9)), cùng cách hiển thị với D-ADM-029 (¶3):
    - Khi tải app (kể cả trước đăng nhập), client gọi `auth.getEnvironment` một lần.
    - Chip hiện khi ít nhất một trong `dev_mailbox_url`, `dev_db_console_url`, `dev_storage_console_url` khác `null`. Nếu gọi lỗi thì ẩn chip, không báo lỗi.
    - Vị trí: bên phải Topbar, ngay trước avatar. Ở D-PRT-001 (¶4.1)–D-PRT-003 (¶4.3) đặt ở góc trên phải màn hình. Hiện cho mọi Nhân viên, kể cả khi chưa đăng nhập.
    - Màu: nền vàng cảnh báo (`warning` của Quasar); chữ, icon và mũi tên dùng Chữ chính `#252421`.
    - Bấm chip mở menu. Mỗi mục chỉ hiện khi URL tương ứng khác `null`, và mở ở tab mới:
      - "Hộp thư DEV" (icon thư) → `dev_mailbox_url`.
      - "Cơ sở dữ liệu DEV" (icon cơ sở dữ liệu) → `dev_db_console_url`, kèm dòng phụ "Toàn quyền dữ liệu, không qua kiểm tra nghiệp vụ".
      - "Lưu trữ DEV" (icon thư mục) → `dev_storage_console_url`, kèm dòng phụ "Toàn quyền dữ liệu, không qua kiểm tra nghiệp vụ".
- **Phiên đăng nhập** (D-SD02-004 (¶3.2) bước 6, D-SD02-007 (¶3.5), D-SD02-009 (¶5.1)):
  - Access token hết hạn (HTTP 401 thông thường): client tự gọi `auth.refresh`, rồi gửi lại request ban đầu. Người dùng không thấy gián đoạn.
  - HTTP 401 `session_revoked`, trả về từ bất kỳ API nào (kể cả `auth.refresh`): phiên đã bị vô hiệu hoá phía máy chủ. Nguyên nhân có thể là một trong các trường hợp sau: tài khoản bị Quản trị hệ thống vô hiệu hoá; Nhân viên vừa đổi/đặt lại mật khẩu ở nơi khác; Nhân viên bị chuyển sang Tổ chức khác (D-SD02-007 (¶3.5)); hoặc token không thuộc kênh `partner` (D-SD02-004 (¶3.2)). Client **không** gọi `auth.refresh` và không gọi `auth.logout`. Client xoá access/refresh token và store Pinia, rồi chuyển thẳng về D-PRT-001 (¶4.1) kèm thông báo "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Mã lỗi không cho biết nguyên nhân cụ thể, nên mọi trường hợp dùng chung một thông báo.
  - Không hiện hộp thoại "Thay đổi chưa lưu" khi bị chuyển về do `session_revoked` (ví dụ đang biên tập ở D-PRT-007 (¶4.7)). Lúc này mọi request lưu đều bị từ chối, nên không còn cách nào giữ lại thay đổi.
  - Sau khi đăng nhập lại, client đưa Nhân viên về đúng màn hình trước đó nếu họ vẫn còn quyền truy cập. Nếu không còn quyền thì về D-PRT-011 (¶4.11) (Tổng quan).
- **Sidebar**: mục **"Tổng quan"** luôn hiện đầu tiên (mọi Nhân viên đã đăng nhập, dẫn tới D-PRT-011 (¶4.11)), tiếp theo là nhóm **"Nghiên cứu & Xét duyệt"**: Đề tài nghiên cứu, Hạng mục tri thức. Mục đang được chọn luôn được highlight rõ ràng (kể cả khi đang ở màn hình con không có mục Sidebar riêng, ví dụ D-PRT-005 (¶4.5)/D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9)/D-PRT-010 (¶4.10)/D-PRT-014 (¶4.13) — Sidebar highlight mục cha gần nhất, ở đây là "Đề tài nghiên cứu" hoặc "Hạng mục tri thức" tuỳ đường vào). Mục "Đề tài nghiên cứu" luôn hiện cho mọi Nhân viên đã đăng nhập (việc lọc theo đúng đề tài/role đã xử lý ở tầng dữ liệu, gồm cả role Chủ nhiệm đề tài — D-PRT-004 (¶4.4)). Mục "Hạng mục tri thức" **ẩn** nếu Nhân viên không giữ role `nghien_cuu`/`xet_duyet` ở **bất kỳ** đề tài nào (chỉ giữ `chu_nhiem_de_tai` đơn thuần) — vì không có quyền vào D-PRT-006 (¶4.6)/D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9) (D-SD03-021 (¶5.1)); trường hợp này truy cập tiến độ/quản lý nhân sự qua D-PRT-010 (¶4.10) (mở từ D-PRT-004 (¶4.4)).
- **Breadcrumb**: mỗi màn hình con (trừ nhóm Xác thực D-PRT-001 (¶4.1)–D-PRT-003 (¶4.3), không thuộc cây phân cấp dữ liệu) hiển thị đường dẫn phân cấp đầy đủ từ nhóm chức năng đến màn hình hiện tại, đặt ngay dưới Topbar, phía trên tiêu đề màn hình — ví dụ "Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}". Mỗi mắt xích (trừ mắt xích cuối, chính là màn hình đang xem) là link điều hướng ngược lại đúng màn hình tương ứng. Breadcrumb là thành phần bắt buộc cho mọi màn hình con, thay cho các link cha rời rạc kiểu cũ.
- **Stepper trạng thái**: áp dụng cho các màn hình thuộc vòng đời Hạng mục tri thức (D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9) — Cổng này không có Mục từ nên chỉ có 1 Stepper duy nhất, khác Admin nội bộ). Đặt ngay dưới Breadcrumb, trên phần nội dung màn hình, gộp 9 mã trạng thái thành **5 cụm** hiển thị theo thứ tự trước sau — cùng cách gộp với D-ADM-029 (¶3):
  1. **Nghiên cứu** (`dang_nghien_cuu`)
  2. **Chờ & Xác minh AI** (`cho_xet_duyet`, `dang_xet_duyet_ai`)
  3. **Xét duyệt chuyên gia** (`da_qua_xet_duyet_ai`, `dang_xet_duyet`)
  4. **Đạt xét duyệt** (`dat_xet_duyet`)
  5. **Xuất bản** (`da_xuat_ban`/`khong_xuat_ban`)

  "Không đạt xét duyệt" (`khong_dat_xet_duyet`) và "Mở lại" (`reopen`) thể hiện bằng mũi tên cong quay về cụm trước đó, không phải một bước riêng trong Stepper. ⚠ Cụm "Xuất bản" vẫn hiển thị đầy đủ trên Stepper ở cả 3 màn hình D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9) dù Nhân viên Tổ chức khác không tự thực hiện được thao tác Xuất bản/Không xuất bản (thuộc vai trò Xuất bản, ngoài phạm vi Cổng này — ¶6) — Stepper cho biết Hạng mục tri thức đang ở đâu trong toàn bộ vòng đời, kể cả các bước Nhân viên xem không có quyền thao tác. Stepper chỉ hiển thị, không thay thế các nút hành động sẵn có.
- **Thành phần dùng lại nhiều nơi** (cùng khái niệm với D-ADM-029 (¶3), tái dùng ở Cổng này):
  - Badge trạng thái (màu theo `status`, cùng 9 mã Hạng mục tri thức).
  - Bảng danh sách có cursor-pagination + filter.
  - Khối "Người phụ trách": hiện tên người đang giữ + nút **Nhận xử lý**/**Nhả** theo phần tử `claim`/`release` của `actions` (bullet "Thao tác theo `actions`"). ⚠ Khác Admin nội bộ: Cổng này **không có** nút "Cưỡng chế nhả" — `ForceRelease` chỉ gọi được bởi role `quan_tri_he_thong`, và role này không có hiệu lực ở Cổng này, kể cả khi Nhân viên nội bộ đang giữ (D-SD03-017 (¶4.2)); khi người phụ trách không tự nhả (nghỉ việc, thu hồi quyền...), Nhân viên Tổ chức khác phải liên hệ Quản trị hệ thống xử lý qua Admin nội bộ — ngoài phạm vi thao tác của Cổng này.
  - Bộ chọn vị trí trong file tuỳ theo `file_type` (page/line cho văn bản, vẽ khung cho ảnh, kéo mốc thời gian cho âm thanh/phim) — dùng chung cho Tham chiếu tới Tư liệu gốc và Vị trí trong Nội dung, cả ở chế độ chọn và chế độ chỉ xem/highlight. Chế độ chỉ xem không highlight dùng để đọc file Tư liệu gốc ở D-PRT-014 (¶4.13).
- **Thao tác theo `actions`** (R-NFR-039 (§3.7.2), R-NFR-040 (§3.7.3); quy ước D-SD01-003 (¶3), bảng thao tác D-SD03-027 (¶3.7)), cùng cách hiển thị với D-ADM-029 (¶3): ở D-PRT-005 (¶4.5) (`actions` của `knowledge.getResearchTopic`), D-PRT-007 (¶4.7)–D-PRT-009 (¶4.9) (`actions` của `knowledge.getKnowledgeObject`) và D-PRT-010 (¶4.10) (`actions` của từng dòng `knowledge.getResearchTopicProgress`, chỉ gồm `delete`), nút thao tác và quyền chỉnh sửa lấy từ `actions` trong response chi tiết. Giao diện không tự suy quy tắc từ `status`, Người phụ trách hay role. Ở kênh `partner`, `actions` chỉ xét role theo phạm vi Đề tài.
  - Thao tác có trong `actions` thì hiện nút; không có thì không hiện.
  - `enabled = false`: nút vô hiệu, kèm dòng chữ phụ ngay dưới nút nêu lý do theo `reason_code` (không chỉ làm mờ nút). Với `edit_content` và `review_claims`, lý do hiện thành banner khoá trên khối nội dung (quy ước (c) bên dưới).
  - Nhãn `reason_code`: `invalid_status` "Không thực hiện được ở trạng thái {nhãn trạng thái hiện tại}"; `assigned_to_other` "{Tên Người phụ trách} đang phụ trách"; `not_assigned` "Cần Nhận xử lý trước"; `no_assignee` "Chưa có Người phụ trách"; `job_running` "Đang có xử lý nền trên đối tượng này"; `topic_not_ready` "Đề tài nghiên cứu chưa ở trạng thái Tư liệu sẵn sàng"; `has_frozen_version` "Đã có phiên bản chốt"; `referenced_by_entry` "Đang được Mục từ tham chiếu"; mã lạ → "Hiện chưa thực hiện được thao tác này".
  - Thao tác có `transitions`: dòng chữ phụ dưới nút "→ {nhãn trạng thái đích} · Xử lý tiếp: {vai trò}"; hộp thoại xác nhận (nếu có) lặp lại thông tin này. Nhãn vai trò: `nghien_cuu` Nghiên cứu, `xet_duyet` Xét duyệt, `chu_nhiem_de_tai` Chủ nhiệm đề tài, `xuat_ban` "Xuất bản (Văn Minh Việt)", `quan_tri_he_thong` Quản trị hệ thống; `he_thong` → "Hệ thống tự xử lý"; mảng rỗng → "Kết thúc vòng xử lý". Thao tác có nhiều phần tử `transitions` (Mở lại): dialog liệt kê từng trạng thái đích kèm vai trò xử lý tiếp.
  - Sau mỗi thao tác (thành công hoặc lỗi), tải lại chi tiết để cập nhật `actions`. Endpoint vẫn có thể từ chối (dữ liệu vừa đổi): hiện thông báo lỗi rồi tải lại.
  - Màn hình danh sách (D-PRT-004 (¶4.4), D-PRT-006 (¶4.6)) không có `actions`, nên không có thao tác chuyển trạng thái/xoá trên dòng.
- **Tham số cấu hình tại nơi thao tác** (R-NFR-041 (§3.7.4)): giá trị hiện hành lấy từ `clientSettings.getSettings` ở kênh `partner` (D-SD07-013 (¶5.2) — mỗi key `{value, label, description, applies_to}`), gọi sau khi đăng nhập/khôi phục phiên, dùng chung toàn app. Hiện thành dòng chữ phụ kèm icon ⓘ ngay cạnh nút/khối liên quan, bằng lời của từng màn hình; di chuột vào ⓘ hiện `description`. Không có link sang màn hình Cấu hình (Cổng này không có). Gọi lỗi thì ẩn dòng. Tham số theo màn hình: D-PRT-007 (¶4.7) (`ai_verification.trigger_mode`, `ai_verification.manual_trigger_roles`), D-PRT-012 (¶4.12) (`identity.login_max_failed_attempts`, `identity.login_lockout_minutes`).
- **Thời hạn tự xử lý** (R-NFR-042 (§3.7.5)): Cổng này hiện không có đối tượng nào hệ thống tự xử lý khi đến hạn (lời mời, tạm khoá đăng nhập, log hỏi–đáp AI chỉ hiển thị ở Admin nội bộ). Khi thêm đối tượng loại này, hiển thị theo cùng cách D-ADM-029 (¶3).
- **Mức độ đặc tả hành vi cho từng thao tác**: chỉ mô tả rõ nội dung hộp thoại xác nhận/cảnh báo cho (a) đặc tả gốc yêu cầu cảnh báo rõ, (b) không thể hoàn tác hoặc ảnh hưởng người khác (Mở lại, Xoá, Gỡ Nhân viên khỏi đề tài), (c) trạng thái khoá nội dung — banner/tooltip nêu rõ lý do khoá, không chỉ ẩn/mờ nút, theo `reason_code` khi có `actions`, (d) cảnh báo dữ liệu bất thường (file `is_missing`). Các hành vi UI thông thường khác theo convention chuẩn của Quasar, không đặc tả riêng từng màn hình.
- Mọi endpoint dùng trong tài liệu này thuộc nhóm mount `partner` theo D-SD03-026 (¶5.6), trừ `auth/*` mount ở cả `admin` và `partner` (D-SD02-009 (¶5.1)).

## 4.1. [D-PRT-001] Đăng nhập

- Form giữa màn hình: input Email, input Mật khẩu, nút "Đăng nhập", link "Quên mật khẩu?".
- Không có lựa chọn "Đăng ký" — Nhân viên không tự tạo tài khoản (R-ID-018 (§2.1.5.2)), kể cả Nhân viên Tổ chức khác (chỉ Quản trị hệ thống ở Admin nội bộ tạo — R-GEN-011 (§1.2.3.3)).
- Nhận mọi Nhân viên đang hoạt động, kể cả Nhân viên Tổ chức nội bộ (D-SD02-004 (¶3.2) bước 2b).
- Lỗi hiển thị dùng chung một thông báo ("Email hoặc mật khẩu không đúng") dù sai lý do gì — xem D-SD02-004 (¶3.2).
- Khi bị chuyển về do `session_revoked` (D-PRT-013 (¶3), bullet "Phiên đăng nhập"): hiện banner thông tin phía trên form, nội dung "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Nếu người dùng mở trang trực tiếp hoặc tự đăng xuất thì không hiện banner.
- Banner thông tin khi bị chuyển về từ D-PRT-012 (¶4.12):
  - Đổi mật khẩu thành công: "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới".
  - Bị tạm khoá do nhập sai mật khẩu hiện tại (`login_locked`): "Bạn đã nhập sai mật khẩu hiện tại quá số lần cho phép. Tài khoản tạm khoá đến {locked_until}."
- Vai trò truy cập: không cần đăng nhập. API: `auth.login`, `auth.getEnvironment` (chip "DEV", D-PRT-013 (¶3)).

## 4.2. [D-PRT-002] Quên mật khẩu / Đặt lại mật khẩu

- **Bước 1 — Quên mật khẩu**: input Email, nút gửi. Luôn hiện cùng một thông báo ("Nếu email tồn tại, một link đặt lại mật khẩu đã được gửi") — D-SD02-005 (¶3.3).
- **Bước 2 — Đặt lại mật khẩu** (mở từ link trong email): input Mật khẩu mới + Xác nhận mật khẩu, nút "Đặt lại mật khẩu".
  - Dưới ô Mật khẩu mới hiện danh sách yêu cầu theo chính sách mật khẩu (`auth.getPasswordPolicy`), kiểm tra ngay khi gõ, cùng cách hiển thị với D-PRT-012 (¶4.12). Hai ô đều có nút hiện/ẩn mật khẩu. Nút "Đặt lại mật khẩu" chỉ bật khi mật khẩu mới đạt chính sách và khớp ô xác nhận.
  - `password_policy_violation`: hiện đúng các điều kiện chưa đạt mà backend trả về.
  - Token sai/hết hạn/đã dùng → báo lỗi, hướng dẫn liên hệ Quản trị hệ thống (Tổ chức Văn Minh Việt — thao tác quản trị chỉ thực hiện ở Admin nội bộ).
  - Thành công: form được thay bằng thông báo ngay tại màn hình này, nội dung "Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại bằng mật khẩu mới.", kèm nút "Quay lại đăng nhập" dẫn tới D-PRT-001 (¶4.1). Không tự chuyển trang.
- API: `auth.forgotPassword`, `auth.getPasswordPolicy`, `auth.resetPassword`, `auth.getEnvironment` (chip "DEV", D-PRT-013 (¶3)).

## 4.3. [D-PRT-003] Đặt mật khẩu lần đầu (từ lời mời)

- Mở từ link mời trong email → gọi `auth.getInvite` để xác thực trước, hiện email (readonly) nếu hợp lệ.
- Input Mật khẩu mới + Xác nhận, nút "Kích hoạt tài khoản". Hiển thị và kiểm tra chính sách mật khẩu cùng cách với D-PRT-002 (¶4.2) bước 2. Khi gặp `password_policy_violation`, hiện các điều kiện chưa đạt. Token sai/hết hạn/đã dùng → báo lỗi tương tự mục D-PRT-002 (¶4.2).
- Thành công: form được thay bằng thông báo ngay tại màn hình này, nội dung "Kích hoạt tài khoản thành công. Vui lòng đăng nhập.", kèm nút "Quay lại đăng nhập" dẫn tới D-PRT-001 (¶4.1). Không tự chuyển trang.
- API: `auth.getInvite`, `auth.getPasswordPolicy`, `auth.acceptInvite`, `auth.getEnvironment` (chip "DEV", D-PRT-013 (¶3)).

## 4.4. [D-PRT-004] Danh sách Đề tài nghiên cứu (được gán)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu
- Bảng: Tên, Trạng thái (badge `chuan_bi_tu_lieu`/`tu_lieu_san_sang`), Vai trò của bạn ở đề tài này (chip: "Chủ nhiệm"/"Nghiên cứu"/"Xét duyệt", có thể nhiều), Số Tư liệu gốc đã gán, Số Hạng mục tri thức (tổng), Ngày tạo.
- Filter: theo Trạng thái; tìm theo tên.
- Chỉ liệt kê đề tài mà Nhân viên đang đăng nhập được gán **ít nhất một trong** role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` (lọc theo `employee_role`, D-SD03-021 (¶5.1)) — không có ngoại lệ "xem toàn bộ" như Quản trị hệ thống ở Admin nội bộ.
- **Không có** nút "+ Tạo Đề tài nghiên cứu" — chỉ Quản trị hệ thống tạo được, ở Admin nội bộ (R-KB-006 (§2.2.1.4)).
- Click dòng → điều hướng theo vai trò tại đề tài đó: có `nghien_cuu` hoặc `xet_duyet` → mở D-PRT-005 (¶4.5) (Chi tiết, xem đầy đủ); **chỉ** có `chu_nhiem_de_tai` (không có 2 role kia ở đề tài này) → mở thẳng D-PRT-010 (¶4.10) (Quản lý & Tiến độ). Có cả Chủ nhiệm đề tài lẫn Nghiên cứu/Xét duyệt → mở D-PRT-005 (¶4.5), kèm nút/link sang D-PRT-010 (¶4.10) (xem D-PRT-005 (¶4.5)).
- ⚠ Danh sách rỗng (ví dụ Nhân viên nội bộ chưa được gán role theo phạm vi Đề tài nào): hiện "Bạn chưa được gán vào Đề tài nghiên cứu nào. Liên hệ Chủ nhiệm đề tài hoặc Quản trị hệ thống để được gán."
- API: `knowledge.listResearchTopics`.
- Quyền truy cập: role `chu_nhiem_de_tai`/`nghien_cuu`/`xet_duyet` (của ít nhất một đề tài).

## 4.5. [D-PRT-005] Chi tiết Đề tài nghiên cứu (chỉ xem — vai trò Nghiên cứu/Xét duyệt)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài}
- Áp dụng khi Nhân viên đang xem giữ role `nghien_cuu` hoặc `xet_duyet` của đề tài này (xem điều hướng ở D-PRT-004 (¶4.4)). Nếu **đồng thời** giữ `chu_nhiem_de_tai` của đề tài này, hiện thêm link/nút "Quản lý & Tiến độ đề tài (Chủ nhiệm)" → mở D-PRT-010 (¶4.10).
- Header: Tên, badge Trạng thái. ⚠ Dưới badge hiện dòng quy trình "Chuẩn bị tư liệu → Tư liệu sẵn sàng", in đậm bước hiện tại (R-NFR-039 (§3.7.2)).
- Nút thao tác theo `actions` của `knowledge.getResearchTopic` (D-PRT-013 (¶3), D-SD03-027 (¶3.7)).
- **Không có** nút "Đánh dấu Tư liệu sẵn sàng" — chỉ vai trò Nhập liệu/Quản trị hệ thống, không tồn tại ở Cổng này (R-KB-011 (§2.2.1.6.2), R-KB-069 (§2.2.5.1)).
- Khối "Tư liệu gốc đã gán": bảng chỉ đọc (Tên, Loại, cảnh báo khi `has_missing_files = true`). Bấm một dòng sẽ mở D-PRT-014 (¶4.13) (Chi tiết Tư liệu gốc). Bảng **không có** nút "Gỡ" hay ô gán thêm Tư liệu gốc (chỉ vai trò Nhập liệu/Quản trị hệ thống thao tác được, ở Admin nội bộ).
- Khối "Hạng mục tri thức": thống kê số lượng theo từng trạng thái (chip đếm), link mở D-PRT-006 (¶4.6) đã lọc sẵn theo đề tài này. Nút "+ Tạo Hạng mục tri thức" theo phần tử `create_knowledge_object` — dialog nhập Tiêu đề, đề tài này chọn sẵn; khi vô hiệu, lý do theo `reason_code` (`topic_not_ready`).
- API: `knowledge.getResearchTopic`.

## 4.6. [D-PRT-006] Danh sách Hạng mục tri thức

- Breadcrumb: khi vào không lọc theo đề tài — Nghiên cứu & Xét duyệt > Hạng mục tri thức; khi vào từ link lọc sẵn ở D-PRT-005 (¶4.5) — Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức.
- Chỉ truy cập được khi Nhân viên giữ role `nghien_cuu`/`xet_duyet` của ít nhất một đề tài — Chủ nhiệm đề tài đơn thuần (không có 2 role này ở đề tài nào) không vào được màn hình này (xem tiến độ qua D-PRT-010 (¶4.10) thay thế, D-SD03-021 (¶5.1)).
- Bảng: Tiêu đề, Đề tài nghiên cứu (ẩn cột này khi đã vào từ link lọc sẵn theo 1 đề tài ở D-PRT-005 (¶4.5)), Trạng thái (badge, 9 mã — D-SD03-011 (¶3.2)), Người phụ trách (tên hoặc "Chưa có"), **Người tạo** (`created_by`, R-KB-047 (§2.2.3.12)), cảnh báo nếu `has_missing_source_files = true`, Ngày tạo (R-KB-048 (§2.2.3.13)).
- Filter: theo Đề tài nghiên cứu (chỉ liệt kê đề tài được gán `nghien_cuu`/`xet_duyet`), theo Trạng thái.
- Nút "+ Tạo Hạng mục tri thức" — chỉ hiện khi Nhân viên đang giữ role `nghien_cuu` của ít nhất một đề tài (trong số đề tài được gán) đang `tu_lieu_san_sang`; dialog chọn Đề tài nghiên cứu (chỉ liệt kê đề tài thoả điều kiện trên) + nhập Tiêu đề. Submit xong điều hướng sang D-PRT-007 (¶4.7).
- Không có thao tác trên dòng; xoá Hạng mục tri thức ở D-PRT-007 (¶4.7) (Chủ nhiệm đề tài không giữ Nghiên cứu/Xét duyệt: ở D-PRT-010 (¶4.10)).
- Click dòng → điều hướng theo `status`: `dang_nghien_cuu`/`cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet` → D-PRT-007 (¶4.7); `da_qua_xet_duyet_ai`/`dang_xet_duyet` → D-PRT-008 (¶4.8); `dat_xet_duyet`/`da_xuat_ban`/`khong_xuat_ban` → D-PRT-009 (¶4.9).
- API: `knowledge.listKnowledgeObjects`, `knowledge.createKnowledgeObject`.
- Quyền truy cập: giới hạn theo đề tài được gán role `nghien_cuu`/`xet_duyet` — **không** có ngoại lệ xem toàn bộ (khác Admin nội bộ, D-SD03-014 (¶3.5)).

## 4.7. [D-PRT-007] Màn hình Nghiên cứu (biên tập Hạng mục tri thức)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (D-PRT-013 (¶3)): active tại cụm "Nghiên cứu" khi `status = dang_nghien_cuu` hoặc `khong_dat_xet_duyet` (trường hợp `khong_dat_xet_duyet` thể hiện thêm mũi tên cong quay lại từ cụm "Xét duyệt chuyên gia"); active tại cụm "Chờ & Xác minh AI" khi `status = cho_xet_duyet`/`dang_xet_duyet_ai`.
- Áp dụng khi Hạng mục tri thức đang ở `dang_nghien_cuu`, `cho_xet_duyet`, `dang_xet_duyet_ai`, hoặc `khong_dat_xet_duyet`.
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha (→ D-PRT-005 (¶4.5)).
- Nút thao tác theo `actions` của `knowledge.getKnowledgeObject` (D-PRT-013 (¶3), D-SD03-027 (¶3.7)).
- Khối "Người phụ trách": tên đang giữ (nếu có) + nút "Nhận xử lý" (`claim`) / "Nhả" (`release`).
- Khối Nội dung (`knowledge_object_file`, R-KB-032 (§2.2.3.6) — sản phẩm biên tập của vai trò Nghiên cứu): danh sách file đã tải lên (tên, loại, kích thước, nút xem/tải), nút "+ Tải file lên" (upload trực tiếp qua presigned URL, không phải trình soạn thảo trực tuyến — D-SD03-007 (¶2.7)).
  - Chỉnh sửa (tải lên/gỡ file, thêm/sửa/xoá Phát biểu & Tham chiếu) theo phần tử `edit_content`: `enabled = true` thì mở chỉnh sửa; `enabled = false` thì chỉ đọc kèm banner lý do theo `reason_code` (quy ước (c) D-PRT-013 (¶3)), riêng tại `dang_xet_duyet_ai` banner theo dòng trạng thái AI Verification bên dưới; không có phần tử này thì chỉ đọc.
- Khối Phát biểu (`claim`): bảng liệt kê nội dung, danh sách Tham chiếu (chip: Tư liệu gốc + file theo `relative_path` + vị trí) kèm cảnh báo nếu `source_file.is_missing = true`, Vị trí trong Nội dung (nếu có khai báo). Nút "+ Thêm Phát biểu" mở form: nội dung, chọn file Nội dung + bộ chọn vị trí (không bắt buộc), thêm một hoặc nhiều Tham chiếu (chọn Tư liệu gốc đã gán cho đề tài → chọn file (liệt kê theo `relative_path`) → bộ chọn vị trí theo `file_type`) — bước "chọn Tư liệu gốc → chọn file" gọi `knowledge.getResearchTopicSource` — `GET /knowledge/research-topics/{id}/sources/{source_id}` (mount `admin`, `partner` — D-SD03-021 (¶5.1)).
- Khối "Gợi ý AI" (`ai_missed_claims_suggestions`, R-KB-085 (§2.2.6.6.5)): chỉ đọc, hiện khi có dữ liệu.
- Vùng trạng thái/hành động cuối trang theo `status`:
  - `dang_nghien_cuu`: nút "Gửi xét duyệt" (`submit_for_review`), dòng chữ phụ theo `transitions` (D-PRT-013 (¶3)) và dòng tham số "AI Verification: tự động chạy khi gửi xét duyệt" / "AI Verification: kích hoạt thủ công bởi {nhãn các vai trò trong `ai_verification.manual_trigger_roles`}" theo `ai_verification.trigger_mode` (D-SD07-004 (¶3.1)). Sau khi gửi, toast theo `status` trả về: `dang_xet_duyet_ai` → "Đã gửi xét duyệt — AI Verification đang chạy"; `cho_xet_duyet` → "Đã gửi xét duyệt — chờ kích hoạt AI Verification". Nút "Xoá Hạng mục tri thức" (`delete`, R-KB-049 (§2.2.3.14)); hộp thoại xác nhận (không hoàn tác — quy ước (b) D-PRT-013 (¶3)): "Xoá sẽ xoá vĩnh viễn Nội dung/Phát biểu/Tham chiếu của Hạng mục tri thức này. Tư liệu gốc không bị ảnh hưởng. Không thể hoàn tác. Tiếp tục?"; khi vô hiệu, lý do theo `reason_code` (`has_frozen_version`, `invalid_status`, `referenced_by_entry`).
  - `cho_xet_duyet`: hiện "Đang chờ kích hoạt AI Verification" (hạng mục dừng ở đây khi `trigger_mode = manual`, hoặc khi đã vào trạng thái này trước lúc chuyển `manual → auto` — D-SD07-004 (¶3.1)), kèm dòng tham số "Kích hoạt thủ công bởi: {nhãn các vai trò trong `ai_verification.manual_trigger_roles`}".
  - `dang_xet_duyet_ai`: dòng trạng thái theo `ai_verification_running` trong chi tiết Hạng mục tri thức (D-SD03-023 (¶5.3)):
    - `true` → "Đang chạy AI Verification..." — chờ job nền.
    - `false` → banner vàng "AI Verification đã dừng (job bị huỷ hoặc thất bại) — cần kích hoạt lại AI Verification" (quy ước (c) D-PRT-013 (¶3)); khi `actions` không có `trigger_ai_verification` (người xem không có nút kích hoạt), banner thêm vế "— liên hệ Nhân viên được phép kích hoạt AI Verification của đề tài" (Cổng này không có màn hình theo dõi job nền).
  - Cả `cho_xet_duyet`/`dang_xet_duyet_ai`/`khong_dat_xet_duyet`: nút kích hoạt AI Verification theo phần tử `trigger_ai_verification` (D-SD03-027 (¶3.7); backend tính theo `ai_verification.manual_trigger_roles` — role theo phạm vi chỉ tính với đúng Đề tài nghiên cứu cha — và trạng thái hiện tại, D-SD07-004 (¶3.1)). Nhãn: "Kích hoạt AI Verification" tại `cho_xet_duyet`; "Kích hoạt lại AI Verification" tại `dang_xet_duyet_ai`/`khong_dat_xet_duyet`. Tại `dang_xet_duyet_ai`, nút hiện bất kể giá trị `ai_verification_running`; đây là đường khôi phục khi job đã bị huỷ hoặc thất bại hẳn.
    - Kết quả kích hoạt (dùng chung cho D-PRT-008 (¶4.8)), theo `merged_into_running_job` trong response (D-SD03-024 (¶5.4)):
      - `true` → thông báo "AI Verification đang chạy cho Hạng mục tri thức này" (không tạo job mới, trạng thái giữ nguyên).
      - `false` → toast "Đã kích hoạt AI Verification".
      - Cả hai trường hợp: tải lại chi tiết Hạng mục tri thức; nếu `status` mới thuộc màn hình khác thì điều hướng theo `status` như D-PRT-006 (¶4.6).
  - `khong_dat_xet_duyet`: hiện ghi chú không đạt (`ai_note`/`expert_note` gộp lại). Nút "Quay lại nghiên cứu" (`resume_research`).
- API: `knowledge.getKnowledgeObject`, `knowledge.getResearchTopicSource`, `knowledge.getResearchTopicSourceFileDownloadUrl`, `knowledge.createKnowledgeObjectFileUploadUrl`, `knowledge.createKnowledgeObjectFile`, `knowledge.getKnowledgeObjectFileDownloadUrl`, `knowledge.deleteKnowledgeObjectFile`, `knowledge.createClaim`, `knowledge.updateClaim`, `knowledge.deleteClaim`, `knowledge.createClaimReference`, `knowledge.deleteClaimReference`, `knowledge.submitKnowledgeObjectForReview`, `knowledge.triggerAiVerification`, `knowledge.claimKnowledgeObject`, `knowledge.releaseKnowledgeObject`, `knowledge.resumeKnowledgeObjectResearch`, `knowledge.deleteKnowledgeObject`, `clientSettings.getSettings`.

## 4.8. [D-PRT-008] Màn hình Xét duyệt Hạng mục tri thức (chuyên gia)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (D-PRT-013 (¶3)): active tại cụm "Xét duyệt chuyên gia" (`da_qua_xet_duyet_ai`/`dang_xet_duyet`).
- Áp dụng khi Hạng mục tri thức đang ở `da_qua_xet_duyet_ai` (chưa ai nhận xử lý) hoặc `dang_xet_duyet` (chuyên gia đang xử lý).
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha. Banner "Nội dung bị khoá" khi `dang_xet_duyet`.
- Nút thao tác theo `actions` của `knowledge.getKnowledgeObject` (D-PRT-013 (¶3), D-SD03-027 (¶3.7)).
- Khối "Người phụ trách": nút "Nhận xử lý" (`claim`) / "Nhả" (`release`), mỗi nút kèm dòng chữ phụ theo `transitions` (D-PRT-013 (¶3)).
- Khối Nội dung: xem file đã upload (đọc, không sửa).
- Khối Phát biểu — với mỗi Phát biểu, hiện từng Tham chiếu và Vị trí trong Nội dung (nếu có) kèm: vị trí (mở file kèm highlight), kết quả AI (`ai_verdict`/`ai_note` hoặc `content_ai_verdict`/`content_ai_note` — chỉ đọc), cảnh báo nếu `source_file.is_missing = true`, form ghi kết luận chuyên gia (`expert_verdict`/`expert_note` hoặc `content_expert_verdict`/`content_expert_note`) — theo phần tử `review_claims`: `enabled = true` thì nhập được; ngược lại chỉ đọc kèm lý do theo `reason_code`.
- Khối "Gợi ý AI" — tham khảo, cùng cơ chế D-PRT-007 (¶4.7).
- Nút cuối trang: "Không đạt xét duyệt" (`reject`) và "Đạt xét duyệt" (`approve`), mỗi nút kèm dòng chữ phụ theo `transitions` (D-PRT-013 (¶3)) — giao diện cảnh báo mềm (không chặn) nếu còn Tham chiếu/Vị trí chưa có `expert_verdict`.
- Nút "Kích hoạt lại AI Verification" — theo phần tử `trigger_ai_verification` (cùng cơ chế D-PRT-007 (¶4.7)); tại `dang_xet_duyet` nút vô hiệu kèm lý do `invalid_status`; kết quả kích hoạt xử lý theo `merged_into_running_job` như D-PRT-007 (¶4.7).
- API: `knowledge.getKnowledgeObject`, `knowledge.listClaims`, `knowledge.getKnowledgeObjectFileDownloadUrl`, `knowledge.getResearchTopicSourceFileDownloadUrl`, `knowledge.claimKnowledgeObject`, `knowledge.releaseKnowledgeObject`, `knowledge.reviewClaimReference`, `knowledge.reviewClaimContent`, `knowledge.rejectKnowledgeObject`, `knowledge.approveKnowledgeObject`, `knowledge.triggerAiVerification`.

## 4.9. [D-PRT-009] Xem & Mở lại Hạng mục tri thức (Đạt xét duyệt / Đã xuất bản / Không xuất bản)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Hạng mục tri thức > {Tiêu đề}
- Stepper trạng thái (D-PRT-013 (¶3)): active tại cụm "Đạt xét duyệt" khi `status = dat_xet_duyet`; active tại cụm "Xuất bản" khi `status = da_xuat_ban`/`khong_xuat_ban`.
- Áp dụng khi Hạng mục tri thức đang ở `dat_xet_duyet`, `da_xuat_ban`, hoặc `khong_xuat_ban` — cả 3 trạng thái đều "Nội dung bị khoá" (banner).
- Header: Tiêu đề, badge Trạng thái, link Đề tài nghiên cứu cha, Người phụ trách (chỉ hiển thị).
- Nút thao tác theo `actions` của `knowledge.getKnowledgeObject` (D-PRT-013 (¶3), D-SD03-027 (¶3.7)).
- Khối Nội dung/Phát biểu: xem lại toàn bộ (đọc, tái dùng view của D-PRT-008 (¶4.8)) kèm kết quả xét duyệt AI + chuyên gia cuối cùng.
- Tại `dat_xet_duyet`: hiện ghi chú "Đang chờ vai trò Xuất bản quyết định Xuất bản/Không xuất bản — thao tác này không thuộc phạm vi Cổng Nhân viên Tổ chức khác (R-PTN-003 (§2.7.2) đặc tả gốc)". **Không có** nút hành động nào cho vai trò Xuất bản ở màn hình này (xem ¶6) — chỉ xem.
- Tại `da_xuat_ban`: hiện "Đã xuất bản lúc {frozen_at} bởi {frozen_by}", số phiên bản (`version_number`) vừa tạo.
- Tại `khong_xuat_ban`: hiện thời điểm chuyển trạng thái.
- Cả `da_xuat_ban`/`khong_xuat_ban`: nút "Mở lại" theo phần tử `reopen`, mở dialog chọn trạng thái đích theo `transitions` (4 lựa chọn: `dang_nghien_cuu`/`cho_xet_duyet`/`da_qua_xet_duyet_ai`/`dang_xet_duyet`, mỗi lựa chọn kèm vai trò xử lý tiếp) kèm cảnh báo không hoàn tác/ảnh hưởng người khác: "Mở lại sẽ đưa Hạng mục tri thức quay lại quy trình xét duyệt, Người phụ trách hiện tại (nếu có) được giữ nguyên. Tiếp tục?" (`knowledge.reopenKnowledgeObject`, body `{target_status}`).
- Khối "Lịch sử phiên bản" (luôn hiện nếu đã có ≥1 phiên bản chốt): bảng các phiên bản đã chốt (Số phiên bản, Thời điểm chốt, Người chốt), click 1 dòng → xem snapshot chỉ đọc (`knowledge.getKnowledgeObjectVersion`).
- **Không có** khối "Phiên bản đang được sử dụng" / nút "Chọn/Đổi phiên bản đang dùng" — thuộc thao tác riêng của vai trò Xuất bản (R-KB-030 (§2.2.3.4.1), R-KB-072 (§2.2.5.4)), ngoài phạm vi Cổng này (xem ¶6).
- API: `knowledge.getKnowledgeObject`, `knowledge.listClaims`, `knowledge.getKnowledgeObjectFileDownloadUrl`, `knowledge.getResearchTopicSourceFileDownloadUrl`, `knowledge.getKnowledgeObjectVersion`, `knowledge.reopenKnowledgeObject`.

## 4.10. [D-PRT-010] Quản lý & Tiến độ đề tài (vai trò Chủ nhiệm đề tài)

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > Quản lý & Tiến độ đề tài
- Áp dụng cho Nhân viên giữ role `chu_nhiem_de_tai` của đề tài đang xem (R-KB-073 (§2.2.5.5)) — mở từ D-PRT-004 (¶4.4) (điều hướng thẳng nếu chỉ giữ Chủ nhiệm đề tài ở đề tài này) hoặc từ link trong D-PRT-005 (¶4.5) (nếu đồng thời giữ Nghiên cứu/Xét duyệt).
- Header: Tên đề tài, badge Trạng thái. ⚠ Dưới badge hiện dòng quy trình "Chuẩn bị tư liệu → Tư liệu sẵn sàng", in đậm bước hiện tại (R-NFR-039 (§3.7.2)).
- Khối "Chủ nhiệm đề tài": hiện tên Nhân viên đang giữ (chính người xem) — **không có** nút đổi Chủ nhiệm ở Cổng này (R-KB-006 (§2.2.1.4) — chỉ Quản trị hệ thống đổi được, thực hiện ở Admin nội bộ).
- Khối "Quản lý nhân sự đề tài" (R-KB-006 (§2.2.1.4)): 2 bảng con "Nghiên cứu" và "Xét duyệt", mỗi bảng liệt kê Nhân viên đang giữ role tương ứng của đề tài này + nút "Gỡ" từng dòng, cùng ô tìm/thêm Nhân viên (không giới hạn Tổ chức — một Đề tài có thể có Nhân viên từ nhiều Tổ chức khác nhau, R-KB-006 (§2.2.1.4)). Thêm/gỡ theo phần tử `manage_members` trong `actions` của `knowledge.getResearchTopic`; không có phần tử này thì chỉ đọc. ⚠ Nút "Gỡ" có hộp thoại xác nhận (ảnh hưởng người khác — quy ước (b) D-PRT-013 (¶3)): "Gỡ {Tên} khỏi vai trò {Nghiên cứu/Xét duyệt} của đề tài này? Người này sẽ mất quyền thao tác với vai trò đó trong đề tài. Nếu người này đang là Người phụ trách của Hạng mục tri thức nào, hạng mục đó vẫn giữ người này làm Người phụ trách cho tới khi Quản trị hệ thống cưỡng chế nhả ở Admin nội bộ." API: `knowledge.listResearchTopicMembers`, `knowledge.searchResearchTopicEmployees`, `knowledge.addResearchTopicResearcher`, `knowledge.removeResearchTopicResearcher`, `knowledge.addResearchTopicReviewer`, `knowledge.removeResearchTopicReviewer`.
- Khối "Tiến độ" (R-KB-073 (§2.2.5.5)/R-PTN-009 (§2.7.3.5)): thống kê số Hạng mục tri thức theo từng trạng thái (chip đếm) + bảng danh sách rút gọn (Tiêu đề, Trạng thái, Người phụ trách, Người tạo) — **không** có link mở chi tiết (không có quyền xem Nội dung/Phát biểu/Tham chiếu/kết quả xét duyệt, R-KB-073 (§2.2.5.5)). Nút "Xoá" (R-KB-049 (§2.2.3.14)) trên mỗi dòng theo phần tử `delete` trong `actions` của dòng (D-SD03-027 (¶3.7)); khi vô hiệu, lý do theo `reason_code`; hộp thoại xác nhận như D-PRT-007 (¶4.7).
- **Không có** khối Tư liệu gốc — ngoài phạm vi vai trò Chủ nhiệm đề tài (R-PTN-008 (§2.7.3.4)–R-PTN-009 (§2.7.3.5) chỉ liệt kê quản lý nhân sự + xem tiến độ + xoá Hạng mục tri thức).
- API: `knowledge.getResearchTopic`, `knowledge.getResearchTopicProgress`, `knowledge.listResearchTopicMembers`, `knowledge.searchResearchTopicEmployees`, `knowledge.addResearchTopicResearcher`, `knowledge.removeResearchTopicResearcher`, `knowledge.addResearchTopicReviewer`, `knowledge.removeResearchTopicReviewer`, `knowledge.deleteKnowledgeObject`.

## 4.11. [D-PRT-011] Tổng quan (Dashboard)

- Không có Breadcrumb (màn hình gốc, luôn là mục đầu tiên trong Sidebar).
- **Mục tiêu chính**: giúp Nhân viên Tổ chức khác hiểu được vị trí công việc của mình trong toàn bộ pipeline nghiệp vụ Văn Minh Việt (dù phạm vi thao tác chỉ gói gọn trong giai đoạn Nghiên cứu & Xét duyệt của Hạng mục tri thức) — hơn là cung cấp số liệu thống kê. Toàn bộ nội dung màn hình là **nội dung tĩnh**, không có chip đếm và không phụ thuộc API mới nào.
- **Khối 1 — Sơ đồ phạm vi công việc** (thành phần chính, đặt đầu trang): sơ đồ tĩnh thể hiện vị trí của Cổng này trong toàn bộ pipeline nghiệp vụ (đối chiếu D-ADM-022 (¶4.22) — sơ đồ đầy đủ ở Admin nội bộ), làm rõ đâu là phần Nhân viên Tổ chức khác tham gia được và đâu không:
  1. **Đề tài nghiên cứu** (2 trạng thái: Chuẩn bị tư liệu → Tư liệu sẵn sàng, do Quản trị hệ thống khởi tạo ở Admin nội bộ) — vai trò của bạn ở bước này: Chủ nhiệm đề tài (nếu được gán) điều phối nhân sự Nghiên cứu/Xét duyệt trong đề tài. Click → mở D-PRT-004 (¶4.4).
  2. **Tư liệu gốc** (đồng bộ từ MinIO/S3, do vai trò Nhập liệu ở Admin nội bộ quản lý) — hiển thị mờ, không click được: chỉ để biết đây là bước trước, **ngoài phạm vi Cổng này**.
  3. **Hạng mục tri thức** — 5 cụm trạng thái, cùng cách gộp với Stepper ở D-PRT-013 (¶3): Nghiên cứu (vai trò Nghiên cứu — **thuộc phạm vi Cổng này**) → Chờ & Xác minh AI (tự động hoặc kích hoạt thủ công theo cấu hình) → Xét duyệt chuyên gia (vai trò Xét duyệt — **thuộc phạm vi Cổng này**) → Đạt xét duyệt → Xuất bản (vai trò Xuất bản — **ngoài phạm vi Cổng này**, thực hiện ở Admin nội bộ). Click → mở D-PRT-006 (¶4.6) (nếu Nhân viên có role Nghiên cứu/Xét duyệt ở ít nhất 1 đề tài).
  4. **Mục từ** (rẽ nhánh từ cụm "Xuất bản" của Hạng mục tri thức) — hiển thị mờ, không click được: **hoàn toàn ngoài phạm vi Cổng này**, do đội ngũ Biên tập/Xét duyệt Mục từ/Xuất bản Mục từ của Văn Minh Việt thực hiện ở Admin nội bộ.

  2 cụm "Nghiên cứu" và "Xét duyệt chuyên gia" (thuộc phạm vi Cổng này) được làm nổi bật trực quan trên sơ đồ ứng với (các) role mà Nhân viên đang đăng nhập đang giữ ở ít nhất một đề tài, để thấy ngay công việc của mình nằm ở đâu trong toàn bộ pipeline — kể cả các bước ngoài phạm vi thao tác của mình. Sơ đồ không hiển thị số liệu/số đếm.
- **Khối 2 — Mô tả vai trò của bạn** (đặt dưới sơ đồ, văn bản ngắn, chỉ hiện đoạn tương ứng (các) role Nhân viên đang giữ ở ít nhất 1 đề tài):
  - **Nghiên cứu**: đọc Tư liệu gốc của đề tài được gán (D-PRT-014 (¶4.13)), biên tập Nội dung/Phát biểu/Tham chiếu cho Hạng mục tri thức thuộc đề tài được gán, gửi đi xét duyệt. → D-PRT-006 (¶4.6).
  - **Xét duyệt**: thẩm định Hạng mục tri thức đã qua AI Verification, ghi kết luận chuyên gia, quyết định Đạt/Không đạt xét duyệt; có thể Mở lại Hạng mục tri thức đã xuất bản/không xuất bản. → D-PRT-006 (¶4.6).
  - **Chủ nhiệm đề tài**: quản lý nhân sự Nghiên cứu/Xét duyệt và theo dõi tiến độ của (các) đề tài mình phụ trách, không xem được Nội dung/Phát biểu/Tham chiếu chi tiết. → D-PRT-004 (¶4.4) (từ đó điều hướng tới D-PRT-010 (¶4.10) của từng đề tài).
- Quyền truy cập: mọi Nhân viên đã đăng nhập (nội dung Khối 1/Khối 2 tự điều chỉnh theo (các) role đang giữ như trên).
- API: không có — toàn bộ nội dung tĩnh, không gọi API đếm số liệu nào.

## 4.12. [D-PRT-012] Đổi mật khẩu

- Dạng dialog, không có route và không có Breadcrumb riêng. Mở từ "Đổi mật khẩu" trong menu tài khoản trên Topbar (D-PRT-013 (¶3)), ở bất kỳ màn hình nào.
- Quyền truy cập: mọi Nhân viên đã đăng nhập, không phụ thuộc role. Nhân viên chỉ đổi được mật khẩu của chính mình (backend xác định theo access token, request không gửi `employee_id`). Đây là thao tác trên tài khoản của chính mình, không thuộc phạm vi cấm quản lý người dùng ở R-PTN-010 (§2.7.4).
- Nếu màn hình đang mở có thay đổi chưa lưu (ví dụ D-PRT-007 (¶4.7)), bấm "Đổi mật khẩu" sẽ hiện hộp thoại "Thay đổi chưa lưu sẽ bị mất khi đổi mật khẩu. Tiếp tục?" trước khi mở dialog, vì đổi mật khẩu thành công sẽ đăng xuất ngay.
- Form:
  - Mật khẩu hiện tại — dòng tham số bên dưới (D-PRT-013 (¶3)): "Nhập sai mật khẩu {identity.login_max_failed_attempts} lần liên tiếp sẽ bị tạm khoá {identity.login_lockout_minutes} phút" (không hiện khi `identity.login_max_failed_attempts = 0`).
  - Mật khẩu mới. Bên dưới hiện danh sách yêu cầu theo chính sách mật khẩu đang cấu hình (`auth.getPasswordPolicy`: độ dài tối thiểu, có cả chữ và số, có ký tự đặc biệt). Hệ thống kiểm tra ngay khi gõ, dòng nào đạt thì hiện tick xanh.
  - Xác nhận mật khẩu mới.
  - Cả 3 ô đều có nút hiện/ẩn mật khẩu.
  - Nút "Huỷ" và "Đổi mật khẩu". Nút "Đổi mật khẩu" chỉ bật khi đủ 3 ô, mật khẩu mới đạt chính sách, khớp ô xác nhận và khác mật khẩu hiện tại.
- Dòng lưu ý ngay trên các nút: "Sau khi đổi mật khẩu, bạn sẽ bị đăng xuất khỏi mọi thiết bị và cần đăng nhập lại."
- Lỗi từ backend (D-SD02-006 (¶3.4), D-SD02-009 (¶5.1)):
  - `invalid_current_password` (422): báo lỗi dưới ô "Mật khẩu hiện tại" là "Mật khẩu hiện tại không đúng". Dialog vẫn mở.
  - `password_unchanged` (422): báo lỗi dưới ô "Mật khẩu mới" là "Mật khẩu mới phải khác mật khẩu hiện tại".
  - `password_policy_violation` (422): hiện đúng các điều kiện chưa đạt mà backend trả về (trường hợp chính sách vừa đổi sau lúc mở dialog).
  - `login_locked` (423, kèm `locked_until`): client gọi `auth.getMe` để kiểm tra phiên.
    - Nếu nhận 401 `session_revoked` (vừa bị tạm khoá do nhập sai mật khẩu hiện tại ngay trong dialog, phiên đã bị vô hiệu hoá): xoá token và store, không gọi `auth.logout`, rồi về D-PRT-001 (¶4.1) kèm banner tạm khoá (D-PRT-001 (¶4.1)).
    - Nếu phiên vẫn hợp lệ (tài khoản đang bị tạm khoá từ trước, do đăng nhập sai ở nơi khác): giữ nguyên phiên, dialog hiện lỗi "Tài khoản đang tạm khoá do đăng nhập sai nhiều lần. Bạn có thể đổi mật khẩu sau {locked_until}." Nút "Đổi mật khẩu" bị tắt cho tới thời điểm đó.
  - 401 `session_revoked`: xử lý theo D-PRT-013 (¶3), bullet "Phiên đăng nhập".
- Thành công (204): backend thu hồi toàn bộ refresh token và vô hiệu hoá mọi phiên (D-SD02-006 (¶3.4) bước 6, D-SD02-007 (¶3.5)). Client xoá token và store, không gọi `auth.logout`, rồi về D-PRT-001 (¶4.1) kèm banner "Đổi mật khẩu thành công, vui lòng đăng nhập lại bằng mật khẩu mới". Sau khi đăng nhập lại, client đưa Nhân viên về màn hình trước đó theo cùng quy tắc ở D-PRT-013 (¶3), bullet "Phiên đăng nhập".
- Không có email thông báo sau khi đổi mật khẩu (R-ID-039 (§2.1.5.10.4)).
- API: `auth.getPasswordPolicy`, `auth.getMe`, `auth.changePassword` (body `{current_password, new_password}`), `clientSettings.getSettings`.

## 4.13. [D-PRT-014] Chi tiết Tư liệu gốc

- Breadcrumb: Nghiên cứu & Xét duyệt > Đề tài nghiên cứu > {Tên đề tài} > {Tên Tư liệu gốc}
- Mở từ dòng Tư liệu gốc ở D-PRT-005 (¶4.5) (R-PTN-005 (§2.7.3.1), R-KB-070 (§2.2.5.2)). Route gồm ID đề tài và ID Tư liệu gốc, theo `knowledge.getResearchTopicSource`.
- Quyền truy cập: Nhân viên giữ role `nghien_cuu` hoặc `xet_duyet` của đề tài này. Chủ nhiệm đề tài đơn thuần không đọc được Tư liệu gốc (D-SD03-021 (¶5.1)). Nếu mở trực tiếp bằng URL mà không có quyền, hoặc Tư liệu gốc không còn được gán cho đề tài, backend trả lỗi. Khi đó màn hình hiện "Bạn không có quyền xem Tư liệu gốc này, hoặc Tư liệu gốc không còn thuộc đề tài", kèm link về D-PRT-004 (¶4.4).
- Header: Tên, Loại, link Đề tài nghiên cứu cha (→ D-PRT-005 (¶4.5)), cảnh báo khi `has_missing_files = true`.
- Bố cục 2 cột:
  - **Cột trái — danh sách file** (`source_file`):
    - Mỗi dòng có Đường dẫn (`relative_path`) và icon theo `file_type`.
    - Ô lọc theo đường dẫn, lọc tại client.
    - File có `is_missing = true` vẫn hiện trong danh sách, kèm cảnh báo "File không còn trong kho lưu trữ từ {missing_since}", nhưng không chọn để xem được (quy ước (d) D-PRT-013 (¶3)).
    - File đang chọn được highlight.
  - **Cột phải — trình xem**:
    - Hiển thị file đang chọn bằng bộ chọn vị trí ở chế độ chỉ xem, không highlight (D-PRT-013 (¶3)), kèm nút "Tải xuống".
    - URL xem/tải lấy qua `knowledge.getResearchTopicSourceFileDownloadUrl` mỗi khi chọn file. URL có thời hạn: nếu trình xem báo lỗi tải, client lấy lại URL một lần rồi mới hiện lỗi.
    - Khi chưa chọn file: hiện "Chọn một file ở danh sách bên trái để xem".
  - Màn hình hẹp (dưới breakpoint `md` của Quasar): hai cột xếp chồng, danh sách file ở trên.
  - ⚠ File đang chọn được ghi vào URL (`?file={file_id}`). Mở trang với tham số này thì file đó được chọn sẵn. `file_id` không thuộc Tư liệu gốc này hoặc là file `is_missing` thì bỏ qua tham số.
- Màn hình chỉ đọc: **không có** gỡ/gán Tư liệu gốc (Admin nội bộ) và không tạo Tham chiếu tại đây. Tham chiếu được tạo ở D-PRT-007 (¶4.7).
- API: `knowledge.getResearchTopicSource`, `knowledge.getResearchTopicSourceFileDownloadUrl`.

## 5. Đối chiếu với Business Requirements / System Design — quy trình xử lý điểm lệch

*(xem `partner-web/00-claude-instructions.md` mục 5)*

## 6. Quyết định đã chốt

- **Vai trò Xuất bản không thuộc phạm vi Cổng này** (`business-requirements.md` R-PTN-003 (§2.7.2)) — khớp `system-design/03-cultural-knowledge-base.md` (`knowledge.publishKnowledgeObject`, `knowledge.skipKnowledgeObjectPublish`, `knowledge.setKnowledgeObjectUsedVersion` chỉ mount `admin`).
- **Route đọc file Tư liệu gốc ở `partner`**: `knowledge.getResearchTopicSource` — `GET /knowledge/research-topics/{id}/sources/{source_id}` (mount `admin`, `partner`). Dùng ở D-PRT-014 (¶4.13) để đọc Tư liệu gốc (R-PTN-005 (§2.7.3.1)) và ở D-PRT-007 (¶4.7) để chọn file khi tạo Tham chiếu.
- **Truy cập Tư liệu gốc** (R-PTN-005 (§2.7.3.1)): màn hình riêng D-PRT-014 (¶4.13), mở từ D-PRT-005 (¶4.5), bố cục 2 cột (danh sách file + trình xem).
- **Chủ nhiệm đề tài** (R-KB-073 (§2.2.5.5)/R-PTN-008 (§2.7.3.4)–R-PTN-009 (§2.7.3.5)): màn hình riêng D-PRT-010 (¶4.10) (tách khỏi D-PRT-005 (¶4.5) vì phạm vi xem khác — không xem được Nội dung/Hạng mục tri thức chi tiết); nút "Xoá" Hạng mục tri thức (R-KB-049 (§2.2.3.14)) ở D-PRT-007 (¶4.7)/D-PRT-010 (¶4.10), theo phần tử `delete` của `actions` (Chủ nhiệm đề tài của đề tài cha hoặc Người phụ trách; role `quan_tri_he_thong` không có hiệu lực ở Cổng này); không có nút đổi Chủ nhiệm đề tài ở Cổng này (`knowledge.setResearchTopicChair` chỉ mount `admin`).
- **Stepper trạng thái (D-PRT-007 (¶4.7)/D-PRT-008 (¶4.8)/D-PRT-009 (¶4.9))**: hiển thị đầy đủ cụm "Xuất bản" dù Nhân viên không tự thao tác được — mục đích là cho biết vị trí trong toàn bộ vòng đời, không chỉ liệt kê bước tự làm được.
- **Dashboard (D-PRT-011 (¶4.11))**: nội dung tĩnh — sơ đồ phạm vi công việc + mô tả theo role, không có chip đếm, không phụ thuộc API `stats`.

## 7. Trạng thái hiện tại

- Đã thiết kế đủ 13 màn hình (D-PRT-001 (¶4.1)–D-PRT-012 (¶4.12), D-PRT-014 (¶4.13)), khớp `business-requirements.md` R-GEN-010 (§1.2.3.2), R-PTN-001 (§2.7), R-KB-073 (§2.2.5.5), R-KB-012 (§2.2.1.7), R-KB-049 (§2.2.3.14), R-ID-035 (§2.1.5.10) và `system-design/01, 02, 03`.
- Không còn điểm lệch nào đang mở. Tài liệu sẵn sàng làm đầu vào build.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-instructions.md` mục 4.
