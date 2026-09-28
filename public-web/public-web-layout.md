# TÀI LIỆU ĐẶC TẢ GIAO DIỆN — ỨNG DỤNG "VĂN MINH VIỆT"

> Tài liệu mô tả UI/UX từ bản thiết kế mockup, dùng để bàn giao cho đội phát triển web/app.

---

## 1. Tổng quan sản phẩm

- **Tên sản phẩm:** Văn Minh Việt
- **Slogan:** "Hệ sinh thái số toàn cầu về văn minh Việt" / "Kết nối quá khứ — Kiến tạo tương lai"
- **Loại hình:** Ứng dụng di động (thiết kế theo chuẩn iOS, status bar 9:41), tổng hợp nội dung văn hóa – lịch sử Việt Nam dưới nhiều hình thức: bách khoa tri thức, AI trợ lý, bảo tàng số 3D/VR/AR, game giáo dục, phim ảnh, bản đồ văn hóa và mạng xã hội cộng đồng.
- **Nền tảng đề xuất:** Responsive web app hoặc app di động (React Native / Flutter / PWA đều phù hợp với bố cục này).

---

## 2. Design System

### 2.1 Bảng màu (Color Palette)

| Vai trò | Mô tả | Gợi ý mã màu |
|---|---|---|
| Nền chính (Background) | Trắng ngà / kem sáng | `#FAF6EE` – `#F5EFE3` |
| Nền phụ / Card | Trắng, viền xám nhạt phân tách | `#FFFFFF` (viền `#E7DECD`) |
| Màu nhấn chính (Accent) | Đỏ / đỏ mận | `#A6192E` – `#8E1B2B` |
| Chữ chính | Đen / nâu đậm | `#241C15` |
| Chữ phụ | Xám nâu nhạt | `#7A7166` |
| Đường viền / Divider | Xám kem nhạt | `#E7DECD` |
| Icon active (tab bar) | Đỏ, trùng màu accent | Trùng màu accent |

**Nguyên tắc:** Nền sáng chủ đạo (light mode by default), điểm nhấn đỏ/đỏ mận cho logo, tiêu đề, icon, nút CTA, badge — vẫn giữ cảm giác cổ kính, trang trọng nhưng theo tông sáng, ấm áp thay vì tông tối như trước.

### 2.2 Typography

- **Heading/Logo:** Font serif hoặc có chân cách điệu, chữ hoa, letter-spacing rộng (dùng cho "VĂN MINH VIỆT", tiêu đề trang chủ) — màu đỏ.
- **Tiêu đề mục (H2/H3):** Sans-serif đậm (bold/semibold), màu đen/nâu đậm.
- **Body text:** Sans-serif thường, cỡ trung bình, màu xám nhạt cho mô tả phụ.
- **Nút bấm/label tab:** Sans-serif nhỏ, đều, dễ đọc ở kích thước icon 20–24px.

### 2.3 Thành phần dùng chung (Shared Components)

- **Status bar** giả lập iOS (giờ, sóng, wifi, pin) — không cần dựng thật nếu build web, chỉ dựng cho app.
- **Top App Bar:** gồm nút back/menu (trái), tiêu đề màn hình (giữa), icon action (phải: search/notification/share/QR...).
- **Bottom Tab Bar (5 tab cố định):** Trang chủ · Khám phá · [Nút trung tâm nổi bật, icon trống đồng, dùng để mở nhanh tính năng chính/AI] · Cộng đồng · Cá nhân. Nút trung tâm có style khác biệt: hình tròn, viền đỏ, nổi lên trên thanh tab. *Tab "Khám phá" dẫn tới màn hình Bách Khoa Toàn Thư (mục 4.3) — cùng đích đến với icon "Bách khoa" ở lưới chức năng Trang chủ.*
- **Card hình chữ nhật bo góc** (radius ~12–16px) dùng cho danh sách nội dung nổi bật, ảnh nền + gradient tối phía dưới để đè chữ.
- **Nút CTA chính:** nền đỏ, chữ trắng, bo góc, dùng cho hành động chính (vd: "Chơi ngay", "Tìm hiểu ngay").
- **Search bar:** bo tròn/bo góc lớn, nền sáng hơn/khác tông nhẹ so với nền chính (viền mảnh xám kem), icon kính lúp bên phải, placeholder dạng câu hỏi gợi ý.
- **Grid icon chức năng:** lưới 4 cột, mỗi ô gồm icon minh hoạ màu (illustrated), nền sáng, bo góc vuông + label bên dưới.

---

## 3. Cấu trúc điều hướng (Navigation Map)

```
Bottom Tab Bar
├── Trang chủ (Home)
├── Khám phá (Explore) ──► Màn hình Bách Khoa Toàn Thư (mục 4.3)
├── [Trung tâm] — truy cập nhanh (AI / mở rộng)
├── Cộng đồng (Community)
└── Cá nhân (Profile)

Từ Trang chủ, lưới 8 chức năng dẫn tới các module con:
├── Bách khoa (Encyclopedia) ──► Màn hình Bách Khoa Toàn Thư (mục 4.3)
├── AI trợ lý (AI Chat) ──► Màn hình Chat AI Văn Minh Việt
├── Bảo tàng số (3D Museum) ──► Màn hình Bảo tàng số 3D
├── Bản đồ văn hóa (Culture Map) ──► Màn hình Bản đồ
├── Game lịch sử (History Game) ──► Màn hình Game
├── Phim & TV (Film & TV) ──► Màn hình Phim & Truyền hình
├── Giáo dục (Education)
└── Cộng đồng (Community) ──► Màn hình Cộng đồng

Thanh tìm kiếm Hero banner (mục 4.1, gõ câu hỏi rồi nhấn Enter/gửi) ──► Màn hình Chat AI (mục 4.2)

Mục từ Bách Khoa (từ carousel Trang chủ, trích dẫn Chat AI, hoặc mục 4.3) ──► Trang chi tiết Mục từ (mục 4.4)
```

---

## 4. Đặc tả chi tiết từng màn hình

### 4.1 Màn hình Trang chủ (Home)

**Top bar:** icon menu (trái) — logo/tên "VĂN MINH VIỆT" (giữa, chữ đỏ) — icon tìm kiếm + icon chuông thông báo (phải).

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: icon chuông thông báo hiện chưa có đặc tả nghiệp vụ tương ứng trong Business Requirements — tài liệu chưa có mục nào về tính năng thông báo cho web công khai (nguồn thông báo, loại thông báo, quy tắc hiển thị/đánh dấu đã đọc, v.v.). Đây là thiết kế UI tham khảo, cần đặc tả bổ sung ở luồng Requirements riêng nếu tính năng này được triển khai.

**Hero banner:** Ảnh nền phong cảnh văn hóa (đình làng, hoàng hôn) full-width, phía trên có gradient tối để nổi chữ. Nội dung overlay:
- Tiêu đề lớn 2 dòng: "Khám phá / Văn Minh Việt"
- Mô tả phụ 1 dòng: "Hành trình xuyên suốt lịch sử, văn hóa và con người Việt Nam"
- Thanh tìm kiếm: placeholder "Bạn muốn tìm gì?" — gõ câu hỏi và nhấn Enter/gửi sẽ mở màn hình Chat AI (mục 4.2) kèm câu hỏi vừa nhập, là lối vào chính cho Trợ lý AI Văn Minh Việt ngay từ Trang chủ. Khác với thanh tìm kiếm riêng ở màn hình Bách Khoa Toàn Thư (mục 4.3) — nơi tìm kiếm Mục từ theo từ khoá (Business Requirements §2.6.2.1).

**Lưới chức năng chính (Grid 4x2, 8 icon):**
1. Bách khoa
2. AI trợ lý
3. Bảo tàng số
4. Bản đồ văn hóa
5. Game lịch sử
6. Phim & TV
7. Giáo dục *(⚠ thiết kế đi trước — chưa có module tương ứng nào trong Business Requirements, kể cả ở danh sách ngoài phạm vi §2.5; cần đề xuất bổ sung ở luồng Requirements riêng)*
8. Cộng đồng

Mỗi item: icon minh hoạ màu, nền sáng, bo góc vuông + nhãn text bên dưới, căn giữa.

**Section "Khám phá nổi bật":**
- Header có link "Xem tất cả >" bên phải.
- Danh sách carousel ngang gồm 3+ card, **mỗi card ứng với một Mục từ của Bách Khoa Toàn Thư** (Business Requirements §2.3.1–2.3.2): ảnh minh họa (từ file đính kèm của Mục từ), tiêu đề đậm (= tiêu đề Mục từ, §2.3.2.2), mô tả phụ 1 dòng (trích đoạn nội dung). Ví dụ tiêu đề minh hoạ: "Đình Làng Việt", "Trống Đồng", "Lễ Hội Truyền Thống" — đây là tên Mục từ tự do, không cần trùng tên cương vực (§2.3.7); một Mục từ có thể được gán một hoặc nhiều cương vực theo §2.3.6.

**Section "Hôm nay" (Card sự kiện nổi bật):**

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: nội dung sự kiện/ngày âm lịch ở đây thuộc phạm vi module Lịch & Sự Kiện (Business Requirements §2.5.5) — hiện ngoài phạm vi giai đoạn này, chưa có đặc tả về nguồn dữ liệu sự kiện, quy tắc chọn sự kiện nổi bật, v.v.

- Card lớn, ảnh nhân vật lịch sử làm nền, overlay gradient.
- Nội dung: nhãn "HÔM NAY", tiêu đề sự kiện (vd "Lễ Giỗ Tổ Hùng Vương"), ngày âm lịch, nút CTA "Tìm hiểu ngay".

**Bottom tab bar:** Trang chủ (active) · Khám phá · [nút tròn trung tâm] · Cộng đồng · Cá nhân.

---

### 4.2 Màn hình Chat AI (AI Văn Minh Việt)

> ⚠️ **Thiết kế đi trước / đơn giản hoá so với đặc tả nghiệp vụ**: Business Requirements §2.6.5 quy định Trợ lý AI cho phép chọn Cương vực để giới hạn phạm vi trả lời (§2.6.5.2), chọn ngôn ngữ trả lời theo §2.3.8 (§2.6.5.3). Ở giai đoạn thiết kế này, màn hình tạm **không có UI chọn Cương vực, chỉ hỗ trợ tiếng Việt** — đây là lựa chọn đơn giản hoá cho UI ở giai đoạn này, không phải đề xuất thay đổi Business Requirements. Riêng **quick-reply chips + nhập giọng nói** bên dưới (hai chi tiết chưa có cơ sở trong BR) tạm để xử lý sau.

**Top bar:** nút back — tiêu đề "AI VĂN MINH VIỆT" — icon mở rộng/full-screen.

**Khung chat:**
- Tin nhắn người dùng: bong bóng bo góc, căn phải, nền đỏ nhạt/hồng phấn.
- Tin nhắn AI: avatar icon tròn (logo trống đồng, nền đỏ) bên trái + bong bóng text căn trái, nền trắng, viền xám kem nhạt.
- AI có thể trả lời kèm **dải ảnh minh họa ngang** (3 ảnh nhỏ bo góc) ngay dưới câu trả lời text.
- Dưới mỗi câu trả lời của AI, hiển thị **danh sách trích dẫn Mục từ nguồn** đã dùng để trả lời (dạng chip nhỏ, ví dụ: "Nguồn: Đình Làng Việt · Trống Đồng Đông Sơn") — bấm vào một trích dẫn để mở Trang chi tiết Mục từ tương ứng (Business Requirements §2.6.3, §2.6.5.4).

**Gợi ý câu hỏi nhanh (Quick reply chips):** dạng nút bo tròn nhỏ, xếp dạng wrap, ví dụ: "Nguồn gốc đình làng", "Kiến trúc đình làng", "Vai trò đình làng".

**Thanh nhập liệu (input bar) dưới cùng:** ô nhập text bo tròn lớn, placeholder "Bạn muốn hỏi thêm gì?", icon microphone bên phải để nhập giọng nói.

---

### 4.3 Màn hình Bách Khoa Toàn Thư (Danh sách Mục từ)

**Top bar:** back/menu (trái) — tiêu đề "BÁCH KHOA TOÀN THƯ" (giữa).

**Thanh tìm kiếm:** placeholder "Tìm mục từ theo tên hoặc nội dung...", tìm theo tiêu đề, nội dung (Business Requirements §2.6.2.1).

**Bộ lọc Cương vực** (filter chips, đa chọn, cuộn ngang): "Văn minh đình làng việt", "Văn minh gia lễ việt", "Văn minh quân sự việt", "Văn minh trống đồng" (§2.6.2.2, §2.3.7 — danh sách "dự kiến", có thể mở rộng khi Nhân viên tạo thêm Cương vực).

**Danh sách Mục từ — lưới 2 cột:** mỗi ô là một card dọc gồm:
- Ảnh minh hoạ tỉ lệ vuông (1:1), bo góc, lấy từ file đính kèm của Mục từ.
- Nhãn Cương vực đầu tiên (nếu có), dạng chip nhỏ đặt đè góc trên-trái của ảnh.
- Tiêu đề Mục từ bên dưới ảnh, đậm, tối đa 2 dòng (không hiện mô tả phụ do khổ card hẹp).
- Gap ngang/dọc giữa các card ~12–16px, container padding 16–20px hai bên (nhất quán mục 5).

Empty state khi tìm kiếm/lọc không có kết quả: minh hoạ + text "Không tìm thấy mục từ phù hợp".

> Ghi chú: chỉ hiển thị Mục từ đang có phiên bản công khai (§2.6.2.3) — quy tắc dữ liệu, không cần UI riêng.

**Bottom tab bar:** Khám phá (active) · các tab còn lại như mục 2.3.

---

### 4.4 Trang chi tiết Mục từ

**Top bar:** back — icon share (phải).

**Header:** Tiêu đề Mục từ (lớn, đậm), chip Cương vực ngay dưới tiêu đề (có thể nhiều).

**Nội dung:** render tuần tự theo danh sách block đã đặc tả (§2.3.2.3.1) — kiểu trang wiki:
- Block đoạn văn/tiêu đề phụ/chú thích: typography Body/H2-H3 (mục 2.2).
- Block nhúng ảnh: full-width, bo góc.
- Block nhúng âm thanh: thanh audio player ngang.
- Block nhúng phim: video player/thumbnail có nút play.

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: section "Mục từ liên quan" (gợi ý các Mục từ khác cùng Cương vực) bên dưới nội dung — chưa có cơ sở trong Business Requirements, là đề xuất UI thêm để tăng khả năng khám phá nội dung.

Là màn hình đích khi: bấm card ở "Khám phá nổi bật" (mục 4.1), bấm trích dẫn Mục từ nguồn ở Chat AI (mục 4.2, §2.6.3), hoặc bấm một Mục từ ở màn hình Bách Khoa (mục 4.3).

---

### 4.5 Màn hình Bản đồ văn hóa (Culture Map)

**Top bar:** back — tiêu đề "BẢN ĐỒ VĂN HÓA" — icon share/export.

**Tab switch (segmented control):** "Bản đồ Việt Nam" / "Bản đồ thế giới".

**Bản đồ tương tác:** hình bản đồ Việt Nam cách điệu (dạng đồ họa tông be/xanh nhạt trên nền sáng, marker đỏ), có các điểm đánh dấu (marker) sáng rải theo vị trí địa lý; một số điểm mở rộng thành **ảnh tròn thumbnail nổi bên cạnh bản đồ** (di tích/lễ hội) nối bằng đường kẻ mảnh tới marker tương ứng.

**Bộ lọc (filter chips) phía dưới bản đồ:** "Di tích lịch sử", "Lễ hội", "Làng nghề", "Danh nhân" — dạng pill button, có thể chọn nhiều.

---

### 4.6 Màn hình Bảo tàng số 3D

**Top bar:** back — tiêu đề "BẢO TÀNG SỐ 3D" — icon share.

**Khu vực hiển thị hiện vật 3D:** ảnh/model lớn full-width phía trên (hiện vật đặt trong không gian trưng bày mô phỏng ánh sáng bảo tàng).

**Thông tin hiện vật:**
- Tên hiện vật (đậm, lớn): vd "Trống Đồng Ngọc Lũ"
- Mô tả phụ: "Văn hóa Đông Sơn"
- Hàng nút chế độ xem: "360°", "VR", "AR" (dạng pill button, có thể toggle) + nút "Chi tiết".

**Section "Hiện vật liên quan":** danh sách ảnh thumbnail vuông bo góc, cuộn ngang.

**Bottom tab bar riêng cho module này** (Trang chủ, Khám phá, [nút trung tâm active], Cộng đồng, Cá nhân) — cho thấy đây vẫn nằm trong flow chính của app, không phải màn hình cô lập.

---

### 4.7 Màn hình Game lịch sử

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Game lịch sử hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements §2.5.1) — chưa có đặc tả chi tiết về luồng chơi, cách tính điểm, lưu tiến độ, v.v. Màn hình dưới đây là thiết kế UI tham khảo, cần đối chiếu lại khi module được đặc tả chính thức.

**Top bar:** back — tiêu đề "GAME LỊCH SỬ" — icon share.

**Banner game nổi bật:** ảnh minh họa nhân vật lịch sử full-width, overlay gradient, nội dung:
- Tên game: "Thời đại Hùng Vương"
- Mô tả ngắn: "Xây dựng và phát triển văn minh Việt cổ"
- Nút CTA nền đỏ: "Chơi ngay"

**Section "Danh sách game":** list dạng hàng ngang, mỗi hàng gồm thumbnail vuông nhỏ bên trái + tên game bên phải, ví dụ: "Thời đại Hùng Vương", "Bách Việt Tranh Hùng", "Lý – Trần – Lê Sơ", "Hải Trình Mở Cõi".

---

### 4.8 Màn hình Phim & Truyền hình

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Phim & Truyền hình hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements §2.5.2, "Phim Lịch Sử") — chưa có đặc tả chi tiết về bản quyền nội dung, nguồn phim, cơ chế lưu tiến độ xem, v.v. Màn hình dưới đây là thiết kế UI tham khảo, cần đối chiếu lại khi module được đặc tả chính thức.

**Top bar:** tiêu đề "PHIM & TRUYỀN HÌNH" — icon search.

**Tab switch ngang:** "Phim" / "Series" / "Tài liệu" / "Hoạt hình".

**Banner phim nổi bật:** ảnh nền lớn (cảnh phim lịch sử), tiêu đề phim lớn (vd "Hùng Vương"), mô tả phụ ("Bộ phim lịch sử đặc sắc").

**Section "Phim nổi bật":** header + link "Xem tất cả >", carousel ngang các poster phim dọc (tỉ lệ ~2:3), tên phim bên dưới mỗi poster.

**Section "Series đang xem":** header + link "Xem tất cả >", list dạng hàng ngang gồm thumbnail + tên series + tập hiện tại + **thanh progress bar %** hiển thị tiến độ xem.

---

### 4.9 Màn hình Cộng đồng (Community)

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Cộng Đồng Văn Hóa hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements §2.5.3) — chưa có đặc tả chi tiết về entity, quy trình kiểm duyệt nội dung (xem thêm BR §3.5.1), v.v. Nội dung chi tiết màn hình dưới đây tạm để nguyên như hiện tại, chưa biên tập sâu thêm — sẽ quay lại sau.

**Top bar:** icon menu (trái) — tiêu đề "CỘNG ĐỒNG" — icon search (phải).

**Tab switch:** "Khám phá" / "Đang theo dõi" / "Nhóm" (có thể nhiều hơn, cuộn ngang được).

**Feed dạng mạng xã hội**, mỗi post gồm:
- Header: avatar tròn + tên người dùng + thời gian đăng ("2 giờ trước") + icon menu "..." (phải).
- Nội dung text bài viết.
- Ảnh minh họa (nếu có), full-width bo góc.
- Thanh action dưới cùng: icon tim + số lượt thích, icon bình luận + số lượng, icon share + nhãn "Chia sẻ".

**Nút nổi (Floating Action Button):** hình tròn đỏ, icon dấu "+", góc dưới phải, dùng để tạo bài viết mới.

---

## 5. Hệ thống lưới & Spacing (đề xuất cho dev)

- **Container padding:** 16–20px hai bên.
- **Bo góc chuẩn:** card lớn 16px, button/pill 20–24px (bo tròn hoàn toàn với nút nhỏ), thumbnail vuông 8–12px.
- **Khoảng cách giữa các section:** 24–32px.
- **Grid icon chức năng:** 4 cột đều nhau, gap ngang/dọc ~16px.
- **Carousel ngang:** card rộng ~65–75% màn hình, hiển thị hé card tiếp theo để gợi ý vuốt.

## 6. Icon & Hình ảnh

- Icon set dùng dạng **minh hoạ màu (illustrated), phong cách thân thiện, đồng bộ 1 style** (gợi ý: bộ icon custom theo mô-típ hoa văn Đông Sơn, tông màu đỏ/be/nâu đất).
- Ảnh minh họa mang phong cách **tranh vẽ/render 3D chất lượng cao**, tông màu ấm (vàng, nâu, cam) trên nền tối — nên thống nhất bằng một bộ ảnh AI-generated hoặc minh họa custom theo đúng phong cách "cổ trang – huyền sử".
- Logo: biểu tượng trống đồng/hoa văn cách điệu, màu đỏ, đặt trong vòng tròn viền mảnh — dùng làm avatar AI, icon nút trung tâm tab bar, watermark.

## 7. Ghi chú kỹ thuật cho dev

- Toàn bộ app mặc định **light theme (nền sáng/kem)**; nếu cần dark mode, cần thiết kế bổ sung (không có trong mockup mới).
- Các màn hình con (Bảo tàng, Game, Phim, Cộng đồng...) đều giữ **bottom tab bar** để đảm bảo điều hướng nhất quán trong toàn app — trừ Chat AI và Bản đồ (dùng top bar back thay vì tab bar, có thể coi là màn hình dạng "full flow" mở từ trang chủ).
- Cần chuẩn bị hệ thống **component tái sử dụng**: Card ảnh + tiêu đề, Pill/Chip button, Progress bar, Segmented control (tab switch), Post card (cộng đồng), Bottom tab bar, Top app bar biến thể (menu/back).
- Nội dung media (ảnh 360°, VR/AR cho bảo tàng số) cần xác định rõ công nghệ triển khai (WebXR, model-viewer, hoặc SDK riêng) — phần này nên trao đổi thêm với dev trước khi implement để chọn giải pháp phù hợp nền tảng.

---

*Tài liệu này mô tả lại giao diện dựa trên bản mockup hình ảnh do người dùng cung cấp, dùng làm cơ sở tham khảo khi triển khai — các thông số màu sắc/spacing là gợi ý ước lượng, cần đối chiếu lại với file thiết kế gốc (Figma/XD) nếu có để lấy giá trị chính xác.*
