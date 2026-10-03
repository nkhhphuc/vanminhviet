# Đặc Tả Giao Diện Web Công Khai — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình biên tập, hoàn thiện đặc tả giao diện web công khai. Đọc `common/00-claude-instructions.md` trước (nguyên tắc dùng chung cho mọi luồng), rồi đọc file này trước khi chỉnh sửa `public-web/public-web-design.md`, kể cả ở một session khác.

## 1. Mục tiêu

- **Mục đích cốt lõi của web công khai:** truyền bá văn hóa và lịch sử của dân tộc Việt Nam trong cộng đồng. Mọi quyết định thiết kế giao diện (bố cục, ưu tiên nội dung, điều hướng) được cân nhắc theo mục đích này; khi có nhiều lựa chọn, ưu tiên phương án giúp người dùng tiếp cận và đọc nội dung văn hoá – lịch sử tốt hơn.
- Biên tập, hoàn thiện `public-web-design.md` thành một đặc tả giao diện đủ chi tiết để đội dev/thiết kế dùng làm đầu vào build giao diện web công khai cho "Văn Minh Việt".
- Tài liệu bắt nguồn từ một bản mô tả lại mockup ứng dụng di động (do người dùng cung cấp) — phạm vi ban đầu rộng hơn nhiều so với những gì `requirements/business-requirements.md` đã đặc tả cho web công khai (R-PUB-001 (§2.6) ở đó). Một phần công việc của luồng này là **đối chiếu từng điểm** giữa hai tài liệu để cả hai bên hiểu giống nhau, và quyết định mỗi điểm lệch nên xử lý thế nào (xem mục 5).

## 2. File nguồn & ranh giới thư mục

- `public-web/public-web-design.md` là **nguồn chân lý duy nhất** cho đặc tả giao diện web công khai. Không tạo thêm bản sao/bản nháp song song trong project.
- `requirements/` (đặc tả nghiệp vụ gốc) và `system-design/` (thiết kế kỹ thuật) — **không thuộc phạm vi của luồng biên tập giao diện này**, chỉ đọc để đối chiếu, không ghi vào đó. Việc sửa `business-requirements.md` (nếu cần) thuộc về luồng Requirements riêng.
- `public-web/changelog.md` là nhật ký các thay đổi đã ghi vào `public-web-design.md` (xem quy tắc chung ở `common/00-claude-instructions.md` mục 2) — khác với mục 7 bên dưới, vốn là bảng theo dõi trạng thái đối chiếu, không phải nhật ký theo ngày.
- Mọi file phát sinh từ luồng biên tập giao diện này chỉ lưu trong thư mục `public-web/` — không rải rác ở thư mục khác.

## 3. Quy ước cấu trúc tài liệu

- Mô tả mỗi màn hình theo màn hình hẹp; khác biệt ở màn hình rộng viết thành quy tắc chung ở `public-web` ¶5, chỉ ghi riêng trong màn hình khi là ngoại lệ — xem quyết định ở mục 6.
- Đánh số màn hình theo mục `4.x` (một màn hình = một mục con), giữ nguyên cách đánh số hiện có khi thêm màn hình mới để không xáo trộn tham chiếu — trừ khi người dùng chủ động yêu cầu sắp xếp lại thứ tự (xem ví dụ ở mục 6), trường hợp đó cần rà soát và cập nhật toàn bộ tham chiếu chéo trong `public-web-design.md` và file này.
- ID thiết kế: Bảng màu D-PUB-011 (¶2.1), Thành phần dùng chung D-PUB-012 (¶2.3), Cấu trúc điều hướng D-PUB-010 (¶3) và từng màn hình 4.x mang ID `D-PUB-NNN` đặt ngay sau số mục trong tiêu đề, theo `common/requirements-design-sync.md` mục 2.4. Màn hình mới nhận ID kế tiếp theo bảng "ID thiết kế lớn nhất đã cấp" trong `common/requirements-change-tracker.md`; ID không đổi khi đánh số lại mục. Trong `public-web-design.md`, trích mục có ID dùng dạng `D-PUB-003 (¶4.3)` (kể cả khi nhắc số màn hình), mục không có ID dùng `¶N`.
- Phần nào là thiết kế UI đi trước đặc tả nghiệp vụ (chưa có cơ sở ở `business-requirements.md`) cần được đánh dấu rõ ràng trong tài liệu (ví dụ ghi chú ngay dưới tiêu đề màn hình) để người đọc không nhầm là đã chốt nghiệp vụ.

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, và luôn đọc lại bản mới nhất từ máy trước khi ghi: theo nguyên tắc chung ở `common/00-claude-instructions.md` mục 3 — áp dụng nguyên vẹn cho luồng này.
- Sau khi ghi xong một thay đổi vào `public-web-design.md`, tóm tắt ngắn gọn cho người dùng xem, đồng thời ghi thêm một mục vào `public-web/changelog.md` theo nguyên tắc ở `common/00-claude-instructions.md` mục 2.

## 5. Đối chiếu với Business Requirements — quy trình xử lý điểm lệch

Khi phát hiện một điểm trong `public-web-design.md` không có cơ sở (hoặc lệch) so với `requirements/business-requirements.md`:

1. Nêu rõ điểm lệch (chức năng/thành phần nào, khớp hay không khớp mục nào trong BR).
2. Hỏi người dùng chọn hướng xử lý cho phần UI: (a) giữ trong `public-web-design.md` kèm ghi chú rõ đây là thiết kế đi trước, chưa có cơ sở nghiệp vụ; (b) tạm gỡ khỏi tài liệu giao diện; (c) để lại xử lý sau.
3. **Không tự sửa `business-requirements.md` trong luồng này.** Nếu người dùng muốn cập nhật BR, việc đó được thực hiện ở một luồng/session Requirements riêng, theo đúng quy trình ở `requirements/00-claude-instructions.md`.
4. Ghi nhận kết quả từng điểm (đã xử lý UI thế nào, có cần đề xuất cập nhật BR hay không) vào mục 7 (Trạng thái hiện tại) của chính file này.

## 6. Quyết định đã chốt

- **UI-first cho các module ngoài phạm vi**: các màn hình mô tả module chưa có đặc tả nghiệp vụ (Bảo tàng số 3D, Bản đồ văn hóa, Game lịch sử, Phim & TV, Cộng đồng...) vẫn giữ trong `public-web-design.md` như thiết kế đi trước, không xoá.
- **Chỉ website, responsive 2 mức**: `public-web-design.md` chỉ đặc tả website (Next.js), ứng dụng di động không thuộc phạm vi. Bố cục 2 mức, dùng chung Header (menu chữ ở màn hình rộng, nút menu ở màn hình hẹp) và Footer; không dùng Bottom Tab Bar. Khác biệt giữa hai mức viết thành quy tắc chung, chỉ ghi riêng các ngoại lệ.
- **Mục 4.9 (Cộng đồng)**: tạm gác lại, chưa biên tập chi tiết — chờ quay lại sau.
- **Theme**: sáng (light mode), nền trắng ngà, màu nhấn đỏ son, icon set minh hoạ màu (illustrated); nhận diện (màu, font, logo, phong cách ảnh) dùng chung với landing vanminhviet.org. Áp dụng cho toàn bộ `public-web-design.md` (`public-web` ¶2 Design System, mô tả màu sắc ở `public-web` ¶4, ghi chú theme ở `public-web` ¶7).
- **Thứ tự màn hình 4.x**: Bách Khoa Toàn Thư (Danh sách Mục từ, Trang chi tiết Mục từ) đặt ngay sau D-PUB-002 (¶4.2) (Chat AI); các màn hình còn lại theo sau: 4.5 Bản đồ văn hóa, 4.6 Bảo tàng số 3D, 4.7 Game lịch sử, 4.8 Phim & TV, 4.9 Cộng đồng; 4.10 Trang Cương vực (D-PUB-013) đặt cuối theo quy tắc giữ số mục.
- **Trang chủ kiểu website**: module ngoài phạm vi gom vào dải "Sắp ra mắt" và menu "Khám phá thêm"; module đã có màn hình thiết kế đi trước thì liên kết tới màn hình đó, chưa có thì chỉ hiển thị. Footer lấy nội dung từ landing vanminhviet.org.

## 7. Trạng thái hiện tại — đối chiếu phạm vi (10 điểm)

Danh sách điểm đối chiếu giữa `public-web-design.md` và `business-requirements.md`, cùng trạng thái xử lý hiện tại (lịch sử xử lý xem `public-web/changelog.md`):

1. ✅ Bảo tàng số 3D — module ngoài phạm vi (BR R-OOS-007 (§2.5.6)), đã ghi chú trong `public-web-design.md`.
2. ✅ Bản đồ văn hóa — module ngoài phạm vi (BR R-OOS-008 (§2.5.7)), đã ghi chú.
3. ✅ Game lịch sử (D-PUB-007 (¶4.7)) — module ngoài phạm vi (BR R-OOS-002 (§2.5.1)), đã ghi chú "thiết kế đi trước".
4. ✅ Phim & TV (D-PUB-008 (¶4.8)) — module ngoài phạm vi (BR R-OOS-003 (§2.5.2)), đã ghi chú "thiết kế đi trước".
5. ✅ Giáo dục — module ngoài phạm vi (BR R-OOS-009 (§2.5.8)), chưa có màn hình; hiện ở dải "Sắp ra mắt" (D-PUB-001 (¶4.1)) và menu Header, không có liên kết.
6. ✅ Cộng đồng (D-PUB-009 (¶4.9)) — module ngoài phạm vi (BR R-OOS-004 (§2.5.3), R-NFR-025 (§3.5.1)), đã ghi chú "thiết kế đi trước"; nội dung chi tiết màn hình tạm gác lại.
7. ✅ Section "Hôm nay" (D-PUB-001 (¶4.1)) — khớp BR R-OOS-006 (§2.5.5) (ngoài phạm vi), đã ghi chú "thiết kế đi trước".
8. ✅ Card trong section "Mục từ nổi bật" (D-PUB-001 (¶4.1)) — không lệch: mỗi card là một Mục từ (BR R-ENC-002 (§2.3.1)–R-ENC-003 (§2.3.2), R-ENC-032 (§2.3.7)), tài liệu đã làm rõ cấu trúc này.
9. ✅ Icon thông báo ở Header (màn hình rộng) (D-PUB-001 (¶4.1)) — chưa có đặc tả nghiệp vụ, đã ghi chú "thiết kế đi trước".
10. ⏳ Màn hình Chat AI (D-PUB-002 (¶4.2)): (a) ⚠ lệch đặc tả — không có UI chọn Cương vực (R-PUB-009 (§2.6.4.1)), giữ đơn giản hoá; cần đề xuất sửa đặc tả ở luồng Requirements; chỉ hỗ trợ tiếng Việt khớp R-NFR-020 (§3.3.5); (b) ✅ trích dẫn Mục từ nguồn dạng chip, bấm mở Trang chi tiết Mục từ (khớp BR R-PUB-007 (§2.6.3), R-PUB-010 (§2.6.4.2)); (c) ⏳ quick-reply chips + nhập giọng nói — chưa có cơ sở trong BR, để xử lý sau; (d) ✅ câu miễn trừ trách nhiệm, hội thoại mới, lưu hội thoại trên trình duyệt (R-AI-009 (§2.4.8), R-AI-007 (§2.4.6), R-PUB-011 (§2.6.4.3)).

## 8. Đồng bộ với session khác

- Xem `common/00-claude-instructions.md` mục 4.
