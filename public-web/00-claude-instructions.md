# Đặc Tả Giao Diện Web Công Khai — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình biên tập, hoàn thiện đặc tả giao diện web công khai. Đọc `common/00-claude-common-instructions.md` trước (nguyên tắc dùng chung cho mọi luồng), rồi đọc file này trước khi chỉnh sửa `public-web/public-web-layout.md`, kể cả ở một session khác.

## 1. Mục tiêu

- Biên tập, hoàn thiện `public-web-layout.md` thành một đặc tả giao diện đủ chi tiết để đội dev/thiết kế dùng làm đầu vào build giao diện web công khai cho "Văn Minh Việt".
- Tài liệu bắt nguồn từ một bản mô tả lại mockup ứng dụng di động (do người dùng cung cấp) — phạm vi ban đầu rộng hơn nhiều so với những gì `requirements/business-requirements.md` đã đặc tả cho web công khai (mục 2.6 ở đó). Một phần công việc của luồng này là **đối chiếu từng điểm** giữa hai tài liệu để cả hai bên hiểu giống nhau, và quyết định mỗi điểm lệch nên xử lý thế nào (xem mục 5).

## 2. File nguồn & ranh giới thư mục

- `public-web/public-web-layout.md` là **nguồn chân lý duy nhất** cho đặc tả giao diện web công khai. Không tạo thêm bản sao/bản nháp song song trong project.
- `requirements/` (đặc tả nghiệp vụ gốc) và `system-design/` (thiết kế kỹ thuật) — **không thuộc phạm vi của luồng biên tập giao diện này**, chỉ đọc để đối chiếu, không ghi vào đó. Việc sửa `business-requirements.md` (nếu cần) thuộc về luồng Requirements riêng.
- `public-web/changelog.md` là nhật ký các thay đổi đã ghi vào `public-web-layout.md` (xem quy tắc chung ở `common/00-claude-common-instructions.md` mục 2) — khác với mục 7 bên dưới, vốn là bảng theo dõi trạng thái đối chiếu, không phải nhật ký theo ngày.
- Mọi file phát sinh từ luồng biên tập giao diện này chỉ lưu trong project, dưới thư mục `public-web/` — không rải rác ở thư mục khác.

## 3. Quy ước cấu trúc tài liệu

- Giữ nguyên phong cách trình bày mobile-first đã có trong bản mockup gốc (status bar, bottom tab bar...) trừ khi có quyết định khác — xem quyết định đã chốt ở mục 6.
- Đánh số màn hình theo mục `4.x` (một màn hình = một mục con), giữ nguyên cách đánh số hiện có khi thêm màn hình mới để không xáo trộn tham chiếu — trừ khi người dùng chủ động yêu cầu sắp xếp lại thứ tự (xem ví dụ ở mục 6), trường hợp đó cần rà soát và cập nhật toàn bộ tham chiếu chéo trong `public-web-layout.md` và file này.
- Phần nào là thiết kế UI đi trước đặc tả nghiệp vụ (chưa có cơ sở ở `business-requirements.md`) cần được đánh dấu rõ ràng trong tài liệu (ví dụ ghi chú ngay dưới tiêu đề màn hình) để người đọc không nhầm là đã chốt nghiệp vụ.

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, và luôn `project_read` bản mới nhất trước khi ghi đè: theo nguyên tắc chung ở `common/00-claude-common-instructions.md` mục 3 — áp dụng nguyên vẹn cho luồng này.
- Sau khi ghi xong một thay đổi vào `public-web-layout.md`, tóm tắt ngắn gọn cho người dùng xem, đồng thời ghi thêm một mục vào `public-web/changelog.md` theo nguyên tắc ở `common/00-claude-common-instructions.md` mục 2.
- Đồng bộ ra máy: theo nguyên tắc chung mục 1 (`public-web/` ↔ `Z:\GoogleDrive\VanMinhViet\public-web`).

## 5. Đối chiếu với Business Requirements — quy trình xử lý điểm lệch

Khi phát hiện một điểm trong `public-web-layout.md` không có cơ sở (hoặc lệch) so với `requirements/business-requirements.md`:

1. Nêu rõ điểm lệch (chức năng/thành phần nào, khớp hay không khớp mục nào trong BR).
2. Hỏi người dùng chọn hướng xử lý cho phần UI: (a) giữ trong `public-web-layout.md` kèm ghi chú rõ đây là thiết kế đi trước, chưa có cơ sở nghiệp vụ; (b) tạm gỡ khỏi tài liệu giao diện; (c) để lại xử lý sau.
3. **Không tự sửa `business-requirements.md` trong luồng này.** Nếu người dùng muốn cập nhật BR, việc đó được thực hiện ở một luồng/session Requirements riêng, theo đúng quy trình ở `requirements/00-claude-instructions.md`.
4. Ghi nhận kết quả từng điểm (đã xử lý UI thế nào, có cần đề xuất cập nhật BR hay không) vào mục 7 (Trạng thái hiện tại) của chính file này.

## 6. Quyết định đã chốt

- **UI-first cho các module ngoài phạm vi**: các màn hình mô tả module chưa có đặc tả nghiệp vụ (Bảo tàng số 3D, Bản đồ văn hóa, Game lịch sử, Phim & TV, Cộng đồng...) vẫn giữ trong `public-web-layout.md` như thiết kế đi trước, không xoá.
- **Giữ phong cách mobile**: không chuyển đổi bố cục sang dạng web desktop (top nav, nhiều cột...); giữ nguyên bottom tab bar, status bar như mockup gốc.
- **Mục 4.9 (Cộng đồng)**: tạm gác lại, chưa biên tập chi tiết — chờ quay lại sau.
- **Theme**: sáng (light mode), nền trắng ngà/kem, màu nhấn đỏ/đỏ mận, icon set minh hoạ màu (illustrated). Áp dụng cho toàn bộ `public-web-layout.md` (mục 2 Design System, mô tả màu sắc ở mục 4, ghi chú theme ở mục 7).
- **Thứ tự màn hình 4.x**: Bách Khoa Toàn Thư (Danh sách Mục từ, Trang chi tiết Mục từ) đặt ngay sau mục 4.2 (Chat AI); các màn hình còn lại theo sau: 4.5 Bản đồ văn hóa, 4.6 Bảo tàng số 3D, 4.7 Game lịch sử, 4.8 Phim & TV, 4.9 Cộng đồng.

## 7. Trạng thái hiện tại — đối chiếu phạm vi (10 điểm)

Danh sách điểm đối chiếu giữa `public-web-layout.md` và `business-requirements.md`, cùng trạng thái xử lý hiện tại (lịch sử xử lý xem `public-web/changelog.md`):

1. ✅ Bảo tàng số 3D — module ngoài phạm vi (BR §2.5.6), đã ghi chú trong `public-web-layout.md`.
2. ✅ Bản đồ văn hóa — module ngoài phạm vi (BR §2.5.7), đã ghi chú.
3. ✅ Game lịch sử (mục 4.7) — module ngoài phạm vi (BR §2.5.1), đã ghi chú "thiết kế đi trước".
4. ✅ Phim & TV (mục 4.8) — module ngoài phạm vi (BR §2.5.2), đã ghi chú "thiết kế đi trước".
5. ✅ Giáo dục (lưới chức năng mục 4.1) — module mới, chưa có cơ sở trong BR, đã ghi chú "thiết kế đi trước, chưa có cơ sở".
6. ✅ Cộng đồng (mục 4.9) — module ngoài phạm vi (BR §2.5.3, §3.5.1), đã ghi chú "thiết kế đi trước"; nội dung chi tiết màn hình tạm gác lại.
7. ✅ Section "Hôm nay" (mục 4.1) — khớp BR §2.5.5 (ngoài phạm vi), đã ghi chú "thiết kế đi trước".
8. ✅ "Lễ Hội Truyền Thống" trong carousel "Khám phá nổi bật" (mục 4.1) — không lệch: mỗi card là một Mục từ (BR §2.3.1–2.3.2, §2.3.7), tài liệu đã làm rõ cấu trúc này.
9. ✅ Icon thông báo ở top bar Trang chủ (mục 4.1) — chưa có đặc tả nghiệp vụ, đã ghi chú "thiết kế đi trước".
10. ⏳ Màn hình Chat AI (mục 4.2): (a) ✅ chỉ hỗ trợ tiếng Việt, không có UI chọn Cương vực/ngôn ngữ; (b) ✅ trích dẫn Mục từ nguồn dạng chip, bấm mở Trang chi tiết Mục từ (khớp BR §2.6.3, §2.6.5.4); (c) ⏳ quick-reply chips + nhập giọng nói — chưa có cơ sở trong BR, để xử lý sau.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-common-instructions.md` mục 4.
