# TÀI LIỆU ĐẶC TẢ GIAO DIỆN — WEB CÔNG KHAI "VĂN MINH VIỆT"

> Tài liệu mô tả UI/UX của website cho Người dùng công khai, dùng để bàn giao cho đội phát triển web. Ứng dụng di động (R-NFR-018 (§3.3.3)) không thuộc phạm vi tài liệu này.

---

## 1. Tổng quan sản phẩm

- **Tên sản phẩm:** Văn Minh Việt
- **Slogan:** "Hệ sinh thái số toàn cầu về văn minh Việt" / "Kết nối quá khứ — Kiến tạo tương lai"
- **Loại hình:** Website responsive cho Người dùng công khai (R-GEN-007 (§1.2.2), R-PUB-001 (§2.6)), một giao diện dùng cho cả màn hình hẹp (điện thoại) và màn hình rộng (máy tính) theo 2 mức bố cục (¶5); tổng hợp nội dung văn hóa – lịch sử Việt Nam dưới nhiều hình thức: bách khoa tri thức, AI trợ lý, bảo tàng số 3D/VR/AR, game giáo dục, phim ảnh, bản đồ văn hóa và mạng xã hội cộng đồng.
- **Nền tảng:** Next.js (SSR/SSG) theo D-SD01-001 (¶1); hỗ trợ trình duyệt theo R-NFR-019 (§3.3.4).

---

## 2. Design System

Nhận diện thương hiệu (màu, font, logo, phong cách ảnh) dùng chung với landing page giới thiệu dự án vanminhviet.org (`assets/css/main.css`). Bố cục và mật độ thông tin theo đặc tả riêng của tài liệu này.

### 2.1 [D-PUB-011] Bảng màu (Color Palette)

| Vai trò | Mô tả | Mã màu |
|---|---|---|
| Nền chính (Background) | Trắng ngà | `#F7F2EA` |
| Nền phụ / Card | Trắng, viền phân tách | `#FFFFFF` (viền `#E6E0D7`) |
| Màu nhấn chính (Accent) | Đỏ son — logo, nút CTA, icon active, link, badge | `#C4171D` |
| Accent đậm | Đỏ đậm — hover/pressed của phần tử dùng Accent | `#9C2B2B` |
| Chữ trên nền Accent | Trắng | `#FFFFFF` |
| Chữ chính | Đen nâu | `#252421` |
| Chữ phụ | Xám nâu | `#6D6A64` |
| Đường viền / Divider | Xám kem nhạt | `#E6E0D7` |
| Màu phụ — Vàng đồng | Hoạ tiết, đường kẻ trang trí, viền/biểu tượng badge | `#C8944A` |
| Màu phụ — Xanh rêu | Nền khối tối (footer, section nhấn mạnh); chữ trên nền này dùng `#F7F2EA` | `#2F4B3F` |
| Mục menu đang active | Chữ và gạch chân màu Accent | `#C4171D` |

**Nguyên tắc:** Nền sáng chủ đạo, đỏ son là màu nhấn duy nhất cho phần tử tương tác. Hai màu phụ chỉ dùng trang trí, không dùng cho nút/CTA/link. Vàng đồng không dùng làm màu chữ trên nền sáng (không đủ tương phản).

### 2.2 Typography

- **Font:** sans-serif **Be Vietnam Pro** (400/500/600/700), dự phòng `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`; serif **Lora** (500/600/700), dự phòng `Georgia, "Times New Roman", serif`. Nạp từ Google Fonts; với Next.js nạp qua `next/font`, subset `vietnamese`.
- **Logo / chữ "VĂN MINH VIỆT":** serif, chữ hoa, màu Accent.
- **H1 (tiêu đề trang), H2 (tiêu đề section):** Lora, màu Chữ chính.
- **H3 (tiêu đề card, khối con):** Be Vietnam Pro semibold, màu Chữ chính.
- **Nhãn section nhỏ** (vd. "KHÁM PHÁ NỔI BẬT", "HÔM NAY"): Be Vietnam Pro, chữ hoa, letter-spacing rộng, màu Accent.
- **Body text:** Be Vietnam Pro regular, màu Chữ chính; mô tả phụ màu Chữ phụ.
- **Nút bấm/label tab:** Be Vietnam Pro medium, cỡ nhỏ.

### 2.3 [D-PUB-012] Thành phần dùng chung (Shared Components)

- **Header (mọi màn hình, cả 2 mức):** dính ở đầu trang (sticky), nền trắng, viền dưới `#E6E0D7`.
  - **Màn hình rộng** (cao khoảng 72px):
    - Bên trái: logo và chữ "VĂN MINH VIỆT". Bấm vào thì về Trang chủ.
    - Ở giữa: menu chữ gồm Trang chủ · Bách khoa toàn thư · Trợ lý AI · Khám phá thêm ▾. Mục đang active có chữ đỏ và gạch chân đỏ.
    - Bên phải: icon tìm kiếm, icon chuông thông báo (⚠, xem D-PUB-001 (¶4.1)) và nút CTA "Hỏi Trợ lý AI" mở D-PUB-002 (¶4.2).
  - **"Khám phá thêm"** mở mega menu khi hover hoặc bấm, nhấn Esc để đóng. Mega menu có 3 cột:
    - "Cương vực": danh sách động lấy từ `public.listCulturalDomains`. Bấm một Cương vực thì mở D-PUB-003 (¶4.3) đã lọc sẵn Cương vực đó.
    - "Trải nghiệm": Bảo tàng số 3D, Bản đồ văn hóa, Game lịch sử, Phim & Truyền hình.
    - "Cộng đồng & Học tập": Cộng đồng, Giáo dục.
  - **Nhãn "Sắp ra mắt":** mỗi module ngoài phạm vi có nhãn dạng pill viền vàng đồng.
    - Module đã có màn hình thiết kế đi trước (D-PUB-005 (¶4.5)–D-PUB-009 (¶4.9)) là liên kết mở màn hình đó.
    - Giáo dục chưa có màn hình nên chỉ hiển thị chữ, không bấm được.
  - **Màn hình hẹp** (cao khoảng 60px): logo bên trái; icon tìm kiếm và nút menu ☰ bên phải.
    - Không có chuông thông báo, không có nút back riêng.
    - Nút menu mở menu toàn màn hình ngay dưới Header. Menu gồm các mục của menu chữ, sau đó là nhóm "Cương vực" và nhóm "Sắp ra mắt", cùng quy tắc liên kết như mega menu.
  - **Icon tìm kiếm** mở ô nhập từ khoá. Nhấn Enter thì mở D-PUB-003 (¶4.3) với từ khoá đó.
  - **Tiêu đề màn hình** là H1 ở đầu vùng nội dung (trừ Trang chủ). Icon action của màn hình (share…) đặt cạnh tiêu đề. Người dùng quay lại bằng nút back của trình duyệt.
- **Footer (mọi màn hình, trừ Chat AI D-PUB-002 (¶4.2)):** nền xanh rêu `#2F4B3F`, phía trên có dải hoạ tiết vàng đồng mảnh, chữ màu `#F7F2EA`. Nội dung lấy theo footer của landing vanminhviet.org:
  - Logo kèm dòng: "Văn Minh Việt – nền tảng được phát triển và vận hành bởi CÔNG TY CỔ PHẦN TẬP ĐOÀN VĂN MINH VIỆT. Mã số doanh nghiệp: 0111582233".
  - Cột "Khám phá": Bách khoa toàn thư, Trợ lý AI, Cương vực (mở D-PUB-003 (¶4.3)).
  - Cột "Về dự án": Giới thiệu, Hệ sinh thái, Dự án, Tầm nhìn. Bốn mục này liên kết tới `https://vanminhviet.org/#about`, `#ecosystem`, `#projects`, `#vision`.
  - Cột "Liên hệ": contact@vanminhviet.org (mailto), Facebook, Zalo. ⚠ Landing hiện chưa có địa chỉ Facebook và Zalo.
  - Dòng cuối: "© 2026 Văn Minh Việt. All rights reserved." · "Bản sắc – Tiếp nối – Khai mở".
  - Màn hình rộng chia 4 cột. Màn hình hẹp: khối logo chiếm một hàng, các cột còn lại chia 2 cột.
- **Card hình chữ nhật bo góc** (radius 16px, ¶5) dùng cho danh sách nội dung nổi bật, ảnh nền + gradient tối phía dưới để đè chữ.
- **Ảnh mặc định của Mục từ** ⚠: một minh hoạ thuỷ mặc tông sáng cố định (¶6). Dùng khi Mục từ không có ảnh bìa (`cover_image = null`) ở card Mục từ, đồng thời là hình chia sẻ mặc định của website (D-SD04-023 (¶3.7)).
- **Cương vực đầu tiên của Mục từ:** phần tử đầu của `cultural_domain_ids`, tức Cương vực được gán sớm nhất (D-SD04-018 (¶5.4)). Tên Cương vực lấy từ `public.listCulturalDomains`. Mục từ chưa gán Cương vực thì không hiện nhãn này.
- **Nút CTA chính:** nền đỏ, chữ trắng, bo góc, dùng cho hành động chính (vd: "Chơi ngay", "Tìm hiểu ngay").
- **Search bar:** bo tròn/bo góc lớn, nền sáng hơn/khác tông nhẹ so với nền chính (viền mảnh xám kem), icon kính lúp bên phải, placeholder dạng câu hỏi gợi ý.
- **Chia sẻ:** nếu trình duyệt hỗ trợ thì mở hộp chia sẻ của hệ thống (Web Share API). Nếu không, sao chép URL của màn hình vào clipboard và hiện thông báo ngắn "Đã sao chép liên kết".
- **Trạng thái tương tác:**
  - Mọi phần tử bấm được đều có trạng thái hover (chữ hoặc viền chuyển đỏ, hoặc nền đậm nhẹ).
  - Mọi phần tử bấm được đều có focus ring nhìn rõ (viền accent 2px) khi điều hướng bằng bàn phím.
  - Mọi thao tác đều làm được bằng bàn phím (Tab, Enter, Esc).

---

## 3. [D-PUB-010] Cấu trúc điều hướng (Navigation Map)

```
Header (D-PUB-012 (¶2.3)) — mọi màn hình
├── Logo / Trang chủ ──► D-PUB-001 (¶4.1)
├── Bách khoa toàn thư ──► D-PUB-003 (¶4.3)
├── Trợ lý AI, nút "Hỏi Trợ lý AI" ──► D-PUB-002 (¶4.2)
├── Khám phá thêm (mega menu / menu màn hình hẹp)
│   ├── Cương vực (danh sách động) ──► D-PUB-003 (¶4.3), lọc sẵn Cương vực
│   ├── Bảo tàng số 3D · Sắp ra mắt ──► D-PUB-006 (¶4.6)
│   ├── Bản đồ văn hóa · Sắp ra mắt ──► D-PUB-005 (¶4.5)
│   ├── Game lịch sử · Sắp ra mắt ──► D-PUB-007 (¶4.7)
│   ├── Phim & Truyền hình · Sắp ra mắt ──► D-PUB-008 (¶4.8)
│   ├── Cộng đồng · Sắp ra mắt ──► D-PUB-009 (¶4.9)
│   └── Giáo dục · Sắp ra mắt (không có liên kết)
└── Icon tìm kiếm (từ khoá) ──► D-PUB-003 (¶4.3)

Trang chủ D-PUB-001 (¶4.1):
├── Ô hỏi AI ở hero / câu hỏi gợi ý ──► D-PUB-002 (¶4.2), kèm câu hỏi
├── Card Cương vực ──► D-PUB-003 (¶4.3), lọc sẵn Cương vực
└── Dải "Sắp ra mắt" ──► như nhóm Sắp ra mắt ở trên

Mục từ (card Trang chủ, trích dẫn Chat AI, hoặc D-PUB-003 (¶4.3)) ──► Trang chi tiết Mục từ (D-PUB-004 (¶4.4))

Footer "Về dự án" ──► landing vanminhviet.org
```

**Đường dẫn (URL):** mỗi màn hình có URL riêng, mở trực tiếp và chia sẻ được. Nút back và forward của trình duyệt phải hoạt động đúng. Từ khoá tìm kiếm và bộ lọc Cương vực ở D-PUB-003 (¶4.3) được phản ánh lên query của URL.

⚠ Đề xuất bảng đường dẫn:

| Màn hình | Đường dẫn |
|---|---|
| Trang chủ D-PUB-001 (¶4.1) | `/` |
| Chat AI D-PUB-002 (¶4.2) | `/tro-ly-ai` |
| Bách Khoa Toàn Thư D-PUB-003 (¶4.3) | `/bach-khoa` |
| Trang chi tiết Mục từ D-PUB-004 (¶4.4) | `/muc-tu/{id}` |
| Bản đồ văn hóa D-PUB-005 (¶4.5) | `/ban-do` |
| Bảo tàng số 3D D-PUB-006 (¶4.6) | `/bao-tang` |
| Game lịch sử D-PUB-007 (¶4.7) | `/game` |
| Phim & TV D-PUB-008 (¶4.8) | `/phim` |
| Cộng đồng D-PUB-009 (¶4.9) | `/cong-dong` |

---

## 4. Đặc tả chi tiết từng màn hình

### 4.1 [D-PUB-001] Màn hình Trang chủ (Home)

Header và Footer theo D-PUB-012 (¶2.3), mục "Trang chủ" ở trạng thái active. Các section xếp từ trên xuống theo thứ tự: Hero → Hôm nay → Khám phá theo Cương vực → Mục từ nổi bật → Trợ lý AI → Sắp ra mắt.

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: icon chuông thông báo ở Header (màn hình rộng) hiện chưa có đặc tả nghiệp vụ tương ứng trong Business Requirements. Tài liệu đó chưa có mục nào về tính năng thông báo cho web công khai (nguồn thông báo, loại thông báo, quy tắc hiển thị/đánh dấu đã đọc, v.v.). Đây là thiết kế UI tham khảo, cần đặc tả bổ sung ở luồng Requirements riêng nếu tính năng này được triển khai.

**Hero:**
- Nền trắng ngà, minh hoạ thuỷ mặc tông sáng (trống đồng, núi, hạc, mặt trời; ¶6). Ở màn hình rộng, minh hoạ nằm ở nửa phải. Ở màn hình hẹp, minh hoạ hiện mờ phía sau chữ. Không dùng ảnh chụp, không dùng gradient tối.
- Nhãn nhỏ "BÁCH KHOA TRI THỨC VĂN HOÁ – LỊCH SỬ VIỆT".
- H1 "Khám phá Văn Minh Việt", trong đó cụm "Văn Minh Việt" màu Accent.
- Mô tả: "Tra cứu Mục từ đã được thẩm định, hoặc hỏi Trợ lý AI và nhận câu trả lời kèm nguồn trích dẫn."
- **Ô hỏi AI** dạng pill, placeholder "Hỏi về lịch sử, văn hoá Việt Nam…", nút "Hỏi AI" nền đỏ ở cuối ô.
  - Gửi bằng Enter hoặc bấm nút thì mở Chat AI (D-PUB-002 (¶4.2)) kèm câu hỏi vừa nhập. Đây là lối vào chính tới Trợ lý AI từ Trang chủ.
  - Ô này khác ô tìm kiếm Mục từ theo từ khoá ở D-PUB-003 (¶4.3) (R-PUB-004 (§2.6.2.1)).
- **Câu hỏi gợi ý:** 3 chip đặt dưới ô hỏi, ví dụ "Đình làng có vai trò gì?", "Trống đồng Ngọc Lũ có gì đặc biệt?", "Nghi lễ cúng giỗ gồm những gì?". Bấm một chip thì mở Chat AI kèm câu hỏi đó. Ở màn hình hẹp, các chip cuộn ngang. ⚠ Danh sách cố định trong code, chưa có cơ sở ở BR.
- Link "Hoặc duyệt Bách khoa toàn thư →" mở D-PUB-003 (¶4.3).

**Section "Hôm nay":**

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: nội dung sự kiện/ngày âm lịch ở đây thuộc phạm vi module Lịch & Sự Kiện (Business Requirements R-OOS-006 (§2.5.5)). Module này hiện ngoài phạm vi giai đoạn này, chưa có đặc tả về nguồn dữ liệu sự kiện, quy tắc chọn sự kiện nổi bật, v.v.

- Card ngang đặt ngay dưới hero, đè nhẹ lên mép dưới của hero. Chữ bên trái, minh hoạ bên phải. Ở màn hình hẹp, minh hoạ ở trên, chữ ở dưới.
- Nội dung: nhãn "HÔM NAY", tên sự kiện dạng H2 (vd. "Giỗ Tổ Hùng Vương"), ngày âm lịch, 1 dòng mô tả, nút viền đỏ "Tìm hiểu ngay".

**Section "Khám phá theo Cương vực":**
- Nhãn "CƯƠNG VỰC", H2 "Khám phá theo Cương vực", 1 dòng mô tả, link "Tất cả Mục từ →" mở D-PUB-003 (¶4.3).
- Mỗi Cương vực trong `public.listCulturalDomains` là một card (R-PUB-005 (§2.6.2.2), R-ENC-032 (§2.3.7)).
  - Card có nền trắng ngà và viền. Góc trên-phải có hoạ tiết trang trí vàng đồng nét mảnh.
  - Nội dung card: nhãn nhỏ "CƯƠNG VỰC", tên Cương vực (Lora), link "Xem Mục từ →".
  - Bấm card thì mở D-PUB-003 (¶4.3) đã lọc sẵn Cương vực đó.
- Hoạ tiết lấy luân phiên từ một bộ cố định theo mô-típ văn hoá (mái đình, trống đồng, đồ thờ, binh khí…). Hoạ tiết không gắn với Cương vực cụ thể, vì Cương vực không có ảnh hay mô tả.
- Lưới 4 cột ở màn hình rộng, 2 cột ở màn hình hẹp.

**Section "Mục từ nổi bật":**
- Nhãn "BÁCH KHOA TOÀN THƯ", H2 "Mục từ nổi bật", link "Xem tất cả →" mở D-PUB-003 (¶4.3).
- Section hiển thị 4 Mục từ được công khai lần đầu gần nhất, lấy bằng `public.listEntries` với `sort=latest&limit=4` (D-SD04-018 (¶5.4)). Đổi phiên bản công khai không làm Mục từ đổi vị trí. Chưa có Mục từ công khai nào thì ẩn section. ⚠
- Mỗi card ứng với một Mục từ của Bách Khoa Toàn Thư (Business Requirements R-ENC-002 (§2.3.1)–R-ENC-003 (§2.3.2)). Card gồm:
  - Ảnh bìa tỉ lệ 4:3 (`cover_image`). Không có ảnh bìa thì dùng Ảnh mặc định của Mục từ (D-PUB-012 (¶2.3)).
  - Cương vực đầu tiên (D-PUB-012 (¶2.3)), chữ nhỏ màu Accent.
  - Tiêu đề Mục từ dạng H3 (R-ENC-005 (§2.3.2.2)).
  - Trích đoạn `excerpt`, tối đa 2 dòng. `excerpt = null` thì bỏ dòng này.
- Bấm card thì mở D-PUB-004 (¶4.4).
- Màn hình rộng dùng lưới 4 cột. Màn hình hẹp dùng carousel vuốt ngang (¶5).

**Section "Trợ lý AI":** chia 2 cột ở màn hình rộng, xếp dọc ở màn hình hẹp.
- **Cột trái:**
  - Nhãn "TRỢ LÝ AI VĂN MINH VIỆT" và H2 "Hỏi bất cứ điều gì về văn hoá Việt".
  - 3 ý giới thiệu:
    - Trợ lý trả lời dựa trên các Mục từ của Bách khoa toàn thư.
    - Mỗi câu trả lời kèm trích dẫn Mục từ nguồn, bấm vào để đọc tiếp (R-PUB-010 (§2.6.4.2)).
    - Không cần tài khoản, hội thoại lưu trên thiết bị (R-PUB-011 (§2.6.4.3)).
  - Nút CTA "Bắt đầu trò chuyện" mở D-PUB-002 (¶4.2).
- **Cột phải:** khung hội thoại mẫu tĩnh gồm 1 câu hỏi và 1 câu trả lời kèm chip trích dẫn. Khung này không gọi API.

**Section "Sắp ra mắt":**

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: các module dưới đây nằm ngoài phạm vi giai đoạn này (Business Requirements R-OOS-001 (§2.5)).

- Nhãn "SẮP RA MẮT", H2 "Những trải nghiệm đang được xây dựng".
- Gồm 6 ô:
  - Bảo tàng số 3D (R-OOS-007 (§2.5.6), D-PUB-006 (¶4.6))
  - Bản đồ văn hóa (R-OOS-008 (§2.5.7), D-PUB-005 (¶4.5))
  - Game lịch sử (R-OOS-002 (§2.5.1), D-PUB-007 (¶4.7))
  - Phim & TV (R-OOS-003 (§2.5.2), D-PUB-008 (¶4.8))
  - Giáo dục (R-OOS-009 (§2.5.8))
  - Cộng đồng (R-OOS-004 (§2.5.3), D-PUB-009 (¶4.9))
- Mỗi ô gồm icon minh hoạ (¶6), tên module và nhãn "Sắp ra mắt".
- Ô của module đã có màn hình thiết kế đi trước là liên kết mở màn hình đó. Giáo dục chưa có màn hình nên chỉ hiển thị, không bấm được.
- Lưới 6 cột ở màn hình rộng, 2 cột ở màn hình hẹp.

---

### 4.2 [D-PUB-002] Màn hình Chat AI (AI Văn Minh Việt)

> ⚠️ **Thiết kế đi trước / đơn giản hoá so với đặc tả nghiệp vụ**: Business Requirements R-PUB-008 (§2.6.4) quy định Trợ lý AI cho phép chọn Cương vực để giới hạn phạm vi trả lời (R-PUB-009 (§2.6.4.1)); hệ thống chỉ hỗ trợ tiếng Việt (R-NFR-020 (§3.3.5)). Ở giai đoạn thiết kế này, màn hình tạm **không có UI chọn Cương vực, chỉ hỗ trợ tiếng Việt** — đây là lựa chọn đơn giản hoá cho UI ở giai đoạn này, không phải đề xuất thay đổi Business Requirements. Riêng **quick-reply chips + nhập giọng nói** bên dưới (hai chi tiết chưa có cơ sở trong BR) tạm để xử lý sau.

**Vùng tiêu đề:** H1 "AI Văn Minh Việt". Màn hình này không có Footer; thanh nhập liệu dính ở đáy màn hình.

**Khung chat:**
- Tin nhắn người dùng: bong bóng bo góc, căn phải, nền đỏ nhạt/hồng phấn.
- Tin nhắn AI: avatar icon tròn (logo trống đồng, nền đỏ) bên trái + bong bóng text căn trái, nền trắng, viền xám kem nhạt.
- **Dải ảnh minh hoạ ngang** ngay dưới câu trả lời text: tối đa 3 ảnh nhỏ bo góc, lấy `cover_image` của các Mục từ trong sự kiện `citations` theo thứ tự trích dẫn.
  - Mục từ không có ảnh bìa thì bỏ qua, không dùng Ảnh mặc định.
  - Không có ảnh nào thì ẩn dải.
  - Bấm một ảnh thì mở Trang chi tiết Mục từ tương ứng. ⚠
- Dưới mỗi câu trả lời của AI, hiển thị **danh sách trích dẫn Mục từ nguồn** đã dùng để trả lời (dạng chip nhỏ, ví dụ: "Nguồn: Đình Làng Việt · Trống Đồng Đông Sơn") — bấm vào một trích dẫn để mở Trang chi tiết Mục từ tương ứng (Business Requirements R-PUB-007 (§2.6.3), R-PUB-010 (§2.6.4.2)). Nhãn chip là `title` trong sự kiện `citations`.

**Dữ liệu câu trả lời:** `assistant.chat` trả về các sự kiện SSE (D-SD05-012 (¶5.1)):
- `token`: nối dần vào bong bóng câu trả lời.
- `citations`: hiện chip trích dẫn và dải ảnh minh hoạ.
- `done`: kết thúc lượt hỏi.
- `error`: hiện thông báo lỗi ngắn dưới câu trả lời, phần câu trả lời đã hiển thị giữ nguyên.
- Kênh `public` không có sự kiện `self_audit`, và `done` chỉ có `turn_index`. Vì vậy màn hình không hiển thị cảnh báo kiểm tra câu trả lời.

**Gợi ý câu hỏi nhanh (Quick reply chips):** dạng nút bo tròn nhỏ, xếp dạng wrap, ví dụ: "Nguồn gốc đình làng", "Kiến trúc đình làng", "Vai trò đình làng".

**Thanh nhập liệu (input bar) dưới cùng:** ô nhập text bo tròn lớn, placeholder "Bạn muốn hỏi thêm gì?", icon microphone bên phải để nhập giọng nói — chỉ hiển thị khi trình duyệt hỗ trợ nhận dạng giọng nói.

**Màn hình rộng:** khung chat và thanh nhập liệu có độ rộng tối đa của nội dung đọc (¶5), căn giữa; thanh nhập liệu dính ở đáy vùng nội dung.

---

### 4.3 [D-PUB-003] Màn hình Bách Khoa Toàn Thư (Danh sách Mục từ)

**Vùng tiêu đề:** H1 "Bách khoa toàn thư".

**Thanh tìm kiếm:** placeholder "Tìm mục từ theo tên hoặc nội dung...", tìm theo tiêu đề, nội dung (Business Requirements R-PUB-004 (§2.6.2.1)).

**Bộ lọc Cương vực** (filter chips, đa chọn; cuộn ngang ở màn hình hẹp, xuống dòng ở màn hình rộng): mỗi Cương vực trong `public.listCulturalDomains` là một chip (R-PUB-005 (§2.6.2.2), R-ENC-032 (§2.3.7)).
- Chọn nhiều Cương vực thì hiện các Mục từ thuộc ít nhất một Cương vực đã chọn. Không chọn Cương vực nào thì không lọc.
- Các Cương vực đã chọn gửi lên `public.listEntries` bằng tham số `cultural_domain_id` lặp lại (D-SD04-018 (¶5.4)).

**Danh sách Mục từ — lưới 2 cột (màn hình hẹp), 4 cột (màn hình rộng):** mỗi ô là một card dọc gồm:
- Ảnh tỉ lệ vuông (1:1), bo góc, lấy từ `cover_image`. Không có ảnh bìa thì dùng Ảnh mặc định của Mục từ (D-PUB-012 (¶2.3)).
- Nhãn Cương vực đầu tiên (D-PUB-012 (¶2.3)), dạng chip nhỏ đặt đè góc trên-trái của ảnh.
- Tiêu đề Mục từ bên dưới ảnh, đậm, tối đa 2 dòng (không hiện mô tả phụ do khổ card hẹp).
- Gap ngang/dọc giữa các card ~12–16px, container padding 16–20px hai bên (nhất quán ¶5).

Empty state khi tìm kiếm/lọc không có kết quả: minh hoạ + text "Không tìm thấy mục từ phù hợp".

> Ghi chú: chỉ hiển thị Mục từ đang có phiên bản công khai (R-PUB-006 (§2.6.2.3)) — quy tắc dữ liệu, không cần UI riêng.

Mở từ một Cương vực (card ở Trang chủ, menu Header) thì bộ lọc chọn sẵn Cương vực đó.

---

### 4.4 [D-PUB-004] Trang chi tiết Mục từ

**Icon share** đặt cạnh tiêu đề Mục từ.

**Header:** Tiêu đề Mục từ (lớn, đậm), chip Cương vực ngay dưới tiêu đề (có thể nhiều), theo thứ tự `cultural_domain_ids`.

**Nội dung:** render tuần tự theo danh sách block đã đặc tả (R-ENC-007 (§2.3.2.3.1)) — kiểu trang wiki:
- Block đoạn văn/tiêu đề phụ/chú thích: typography Body/H2-H3 (¶2.2).
- Block nhúng ảnh: full-width, bo góc.
- Block nhúng âm thanh: thanh audio player ngang.
- Block nhúng phim: video player/thumbnail có nút play.

**Màn hình rộng:** phần nội dung có độ rộng tối đa của nội dung đọc (¶5), căn giữa; section "Mục từ liên quan" dạng lưới 4 cột.

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: section "Mục từ liên quan" (gợi ý các Mục từ khác cùng Cương vực) bên dưới nội dung — chưa có cơ sở trong Business Requirements, là đề xuất UI thêm để tăng khả năng khám phá nội dung.

Là màn hình đích khi: bấm card ở "Mục từ nổi bật" (D-PUB-001 (¶4.1)), bấm trích dẫn Mục từ nguồn ở Chat AI (D-PUB-002 (¶4.2), R-PUB-007 (§2.6.3)), hoặc bấm một Mục từ ở màn hình Bách Khoa (D-PUB-003 (¶4.3)).

---

### 4.5 [D-PUB-005] Màn hình Bản đồ văn hóa (Culture Map)

**Vùng tiêu đề:** H1 "Bản đồ văn hóa" — icon share/export cạnh tiêu đề.

**Tab switch (segmented control):** "Bản đồ Việt Nam" / "Bản đồ thế giới".

**Bản đồ tương tác:** hình bản đồ Việt Nam cách điệu (dạng đồ họa tông be/xanh nhạt trên nền sáng, marker đỏ), có các điểm đánh dấu (marker) sáng rải theo vị trí địa lý; một số điểm mở rộng thành **ảnh tròn thumbnail nổi bên cạnh bản đồ** (di tích/lễ hội) nối bằng đường kẻ mảnh tới marker tương ứng.

**Bộ lọc (filter chips) phía dưới bản đồ:** "Di tích lịch sử", "Lễ hội", "Làng nghề", "Danh nhân" — dạng pill button, có thể chọn nhiều.

---

### 4.6 [D-PUB-006] Màn hình Bảo tàng số 3D

**Vùng tiêu đề:** H1 "Bảo tàng số 3D" — icon share cạnh tiêu đề.

**Khu vực hiển thị hiện vật 3D:** ảnh/model lớn full-width phía trên (hiện vật đặt trong không gian trưng bày mô phỏng ánh sáng bảo tàng).

**Thông tin hiện vật:**
- Tên hiện vật (đậm, lớn): vd "Trống Đồng Ngọc Lũ"
- Mô tả phụ: "Văn hóa Đông Sơn"
- Hàng nút chế độ xem: "360°", "VR", "AR" (dạng pill button, có thể toggle) + nút "Chi tiết".

**Section "Hiện vật liên quan":** danh sách ảnh thumbnail vuông bo góc, cuộn ngang.

---

### 4.7 [D-PUB-007] Màn hình Game lịch sử

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Game lịch sử hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements R-OOS-002 (§2.5.1)) — chưa có đặc tả chi tiết về luồng chơi, cách tính điểm, lưu tiến độ, v.v. Màn hình dưới đây là thiết kế UI tham khảo, cần đối chiếu lại khi module được đặc tả chính thức.

**Vùng tiêu đề:** H1 "Game lịch sử" — icon share cạnh tiêu đề.

**Banner game nổi bật:** ảnh minh họa nhân vật lịch sử full-width, overlay gradient, nội dung:
- Tên game: "Thời đại Hùng Vương"
- Mô tả ngắn: "Xây dựng và phát triển văn minh Việt cổ"
- Nút CTA nền đỏ: "Chơi ngay"

**Section "Danh sách game":** list dạng hàng ngang, mỗi hàng gồm thumbnail vuông nhỏ bên trái + tên game bên phải, ví dụ: "Thời đại Hùng Vương", "Bách Việt Tranh Hùng", "Lý – Trần – Lê Sơ", "Hải Trình Mở Cõi".

---

### 4.8 [D-PUB-008] Màn hình Phim & Truyền hình

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Phim & Truyền hình hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements R-OOS-003 (§2.5.2), "Phim Lịch Sử") — chưa có đặc tả chi tiết về bản quyền nội dung, nguồn phim, cơ chế lưu tiến độ xem, v.v. Màn hình dưới đây là thiết kế UI tham khảo, cần đối chiếu lại khi module được đặc tả chính thức.

**Vùng tiêu đề:** H1 "Phim & Truyền hình" — icon search cạnh tiêu đề.

**Tab switch ngang:** "Phim" / "Series" / "Tài liệu" / "Hoạt hình".

**Banner phim nổi bật:** ảnh nền lớn (cảnh phim lịch sử), tiêu đề phim lớn (vd "Hùng Vương"), mô tả phụ ("Bộ phim lịch sử đặc sắc").

**Section "Phim nổi bật":** header + link "Xem tất cả >", carousel ngang các poster phim dọc (tỉ lệ ~2:3), tên phim bên dưới mỗi poster.

**Section "Series đang xem":** header + link "Xem tất cả >", list dạng hàng ngang gồm thumbnail + tên series + tập hiện tại + **thanh progress bar %** hiển thị tiến độ xem.

---

### 4.9 [D-PUB-009] Màn hình Cộng đồng (Community)

> ⚠️ **Thiết kế đi trước đặc tả nghiệp vụ**: module Cộng Đồng Văn Hóa hiện nằm trong danh sách module ngoài phạm vi giai đoạn này (Business Requirements R-OOS-004 (§2.5.3)) — chưa có đặc tả chi tiết về entity, quy trình kiểm duyệt nội dung (xem thêm BR R-NFR-025 (§3.5.1)), v.v. Nội dung chi tiết màn hình dưới đây tạm để nguyên như hiện tại, chưa biên tập sâu thêm — sẽ quay lại sau.

**Vùng tiêu đề:** H1 "Cộng đồng" — icon search cạnh tiêu đề.

**Tab switch:** "Khám phá" / "Đang theo dõi" / "Nhóm" (có thể nhiều hơn, cuộn ngang được).

**Feed dạng mạng xã hội**, mỗi post gồm:
- Header: avatar tròn + tên người dùng + thời gian đăng ("2 giờ trước") + icon menu "..." (phải).
- Nội dung text bài viết.
- Ảnh minh họa (nếu có), full-width bo góc.
- Thanh action dưới cùng: icon tim + số lượt thích, icon bình luận + số lượng, icon share + nhãn "Chia sẻ".

**Nút nổi (Floating Action Button):** hình tròn đỏ, icon dấu "+", góc dưới phải, dùng để tạo bài viết mới.

---

## 5. Hệ thống lưới, Spacing & Responsive (đề xuất cho dev)

- **Container padding:** 16–20px hai bên.
- **Bo góc chuẩn** (thang 8 / 16 / 24px và pill): thumbnail 8px; card 16px; khối lớn (hero banner, card "Hôm nay", banner nổi bật) 24px; nút, chip, search bar, input bar dạng pill (bo tròn hoàn toàn).
- **Khoảng cách giữa các section:** màn hình hẹp 48px, màn hình rộng 72px.

**Responsive 2 mức:**

- **Màn hình hẹp** (< 1024px ⚠) và **màn hình rộng** (≥ 1024px ⚠).
- Header và Footer (D-PUB-012 (¶2.3)) dùng cho mọi màn hình ở cả 2 mức. Khác biệt giữa 2 mức của Header ghi ở D-PUB-012 (¶2.3). "Vùng tiêu đề" ở từng màn hình ¶4 là phần đầu vùng nội dung, giống nhau ở 2 mức.
- **Container ở màn hình rộng:** vùng nội dung rộng tối đa 1200px ⚠, căn giữa, padding hai bên 24–32px.
- **Nội dung đọc** (khung Chat AI, nội dung Mục từ): rộng tối đa 760px ⚠, căn giữa.
- **Lưới card ở Trang chủ:** Cương vực 2 cột (hẹp) / 4 cột (rộng); Sắp ra mắt 2 cột (hẹp) / 6 cột (rộng); gap 12–20px.
- **Carousel ngang:**
  - Màn hình hẹp: card rộng khoảng 65–75% màn hình, hé một phần card tiếp theo để gợi ý vuốt.
  - Màn hình rộng: hiện 3–4 card mỗi lượt, có nút mũi tên trái/phải ở hai bên, vẫn cuộn được bằng trackpad.
- **Filter chips / tab switch:** màn hình hẹp cuộn ngang; màn hình rộng xuống dòng nếu không đủ chỗ.
- **Hero** (D-PUB-001 (¶4.1)) ở màn hình rộng: khối chữ căn trái, rộng tối đa khoảng 640px, minh hoạ ở nửa phải.

## 6. Icon & Hình ảnh

- Icon set dùng dạng **minh hoạ màu (illustrated), phong cách thân thiện, đồng bộ 1 style** (gợi ý: bộ icon custom theo mô-típ hoa văn Đông Sơn, tông màu đỏ/be/nâu đất).
- Ảnh minh hoạ theo phong cách **thuỷ mặc, tông sáng**: nền giấy ngà, nét mực nhạt, điểm xuyết đỏ son/vàng đồng, mô-típ trống đồng, hạc, núi, mái đình — thống nhất với landing vanminhviet.org. Ảnh thật của Mục từ hiển thị nguyên trạng, không áp phong cách này.
- Logo: dùng logo của landing vanminhviet.org ở Header và Footer. Biểu tượng trống đồng cách điệu màu đỏ trong vòng tròn viền mảnh dùng làm avatar AI, watermark.

## 7. Ghi chú kỹ thuật cho dev

- Toàn bộ website mặc định **light theme (nền sáng/kem)**; nếu cần dark mode, cần thiết kế bổ sung (không có trong mockup mới).
- Mọi màn hình dùng chung Header và Footer (D-PUB-012 (¶2.3)); riêng Chat AI không có Footer.
- Cần chuẩn bị hệ thống **component tái sử dụng**: Card ảnh + tiêu đề, Pill/Chip button, Progress bar, Segmented control (tab switch), Post card (cộng đồng), Header (2 mức, mega menu, menu màn hình hẹp), Footer, Card Cương vực, Nhãn "Sắp ra mắt".
- Nội dung media (ảnh 360°, VR/AR cho bảo tàng số) cần xác định rõ công nghệ triển khai (WebXR, model-viewer) — mức hỗ trợ WebXR/AR khác nhau giữa các trình duyệt trong R-NFR-019 (§3.3.4), cần có cách xem thay thế (360°/ảnh) khi trình duyệt không hỗ trợ; phần này nên trao đổi thêm với dev trước khi implement để chọn giải pháp phù hợp nền tảng.

---

*Tài liệu này mô tả lại giao diện dựa trên bản mockup hình ảnh do người dùng cung cấp. Màu, font và bo góc theo bộ nhận diện của landing vanminhviet.org; các thông số spacing là gợi ý ước lượng, cần đối chiếu lại với file thiết kế gốc (Figma/XD) nếu có.*
