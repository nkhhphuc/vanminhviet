# Đặc Tả Yêu Cầu Văn Minh Việt — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình biên tập, hoàn thiện đặc tả yêu cầu phần mềm. Đọc `common/00-claude-common-instructions.md` trước (nguyên tắc dùng chung cho mọi luồng), rồi đọc file này trước khi chỉnh sửa `requirements/business-requirements.md`, kể cả ở một session khác.

## 1. Mục tiêu

- Biên tập, hoàn thiện `business-requirements.md` thành một đặc tả đủ chi tiết, rõ ràng, không mơ hồ — để **bất kỳ ai** (không giới hạn người biên soạn) có thể dùng làm đầu vào cho Claude Code (hoặc AI/đội dev khác) thiết kế và build phần mềm.
- Đây không phải tài liệu giữ kín riêng cho một người — mục tiêu chính là chất lượng & độ đầy đủ của đặc tả, không phải kiểm soát ai được dùng nó.
- (Việc phụ, on-demand, không ảnh hưởng mục tiêu chính): từng thử tạo một skill tóm tắt điều hành (rút gọn, ẩn chi tiết) để trình cấp trên/ban lãnh đạo, nhưng bản thử không đủ chi tiết theo đánh giá thực tế nên đã huỷ. Đã tạo lại theo hướng khác — xem skill `van-minh-viet-bao-cao-cong-viec` ở mục 7.

## 2. File nguồn duy nhất

- `requirements/business-requirements.md` là **nguồn chân lý duy nhất** cho đặc tả yêu cầu. Không tạo thêm bản sao/bản nháp song song trong project.
- Tài liệu thiết kế kỹ thuật (`system-design/`) tham chiếu ngược lại tài liệu này theo ID (kèm số mục), xem `common/requirements-design-sync.md` mục 2.3 — không tự ý suy diễn khi đặc tả gốc chưa có.
- Các bản xuất khác (Word, PDF...) là bản phái sinh phục vụ mục đích cụ thể (đọc offline, gửi máy tính người dùng...), không phải nguồn chân lý — khi có thay đổi, `business-requirements.md` trong project luôn được cập nhật trước.
- `requirements/changelog.md` là nhật ký các thay đổi đã ghi vào `business-requirements.md` (xem quy tắc chung ở `common/00-claude-common-instructions.md` mục 2).
- Mọi file là kết quả làm việc của giai đoạn đặc tả này (đặc tả, khung nguyên tắc, và các tài liệu liên quan khác nếu phát sinh) **chỉ lưu trong project, dưới thư mục `requirements/`** — không tạo rải rác ở các đường dẫn khác trong project.

## 3. Quy ước đánh số & cấu trúc

- Đánh số nhiều cấp thủ công ngay trong text (`**1.1.1.**`, `**2.2.3.7.**`...) — không dùng danh sách tự đánh số của Markdown — để người dùng có thể tham chiếu chính xác một mục/câu khi trao đổi. Về mặt cú pháp, mỗi mục vẫn là một list item Markdown (`- **1.1.1.** ...`) để có thụt lề phân cấp; đây là quy ước cố ý giữ nguyên (xem mục 7 về cách xử lý khi xuất Word).
- Khi thêm/xoá/tách một mục làm lệch số các mục con phía sau, phải đánh số lại toàn bộ và rà soát mọi tham chiếu chéo tới số mục đó ở nơi khác trong tài liệu (ví dụ "xem mục 2.2.5.11") để tránh trỏ sai sau khi đánh số lại. Đánh số lại chỉ đổi số mục, không đổi ID (xem bên dưới).
- **ID yêu cầu ổn định**: mỗi mục đánh số (kể cả tiêu đề mục) mang một ID `R-<mã module>-<3 chữ số>` theo `common/requirements-design-sync.md` mục 2. Vị trí đặt ID:
  - Mục thường: `- **2.2.3.5.** [R-KB-031] Nội dung...`
  - Mục có tiêu đề in đậm: `- **2.1.5.7.** [R-ID-024] **Vô hiệu hoá tài khoản**: nội dung...`
  - Tiêu đề Markdown: `### 2.2. [R-KB-001] Cơ Sở Dữ Liệu Văn Hóa`
  - Không mang ID: tiêu đề khung `## 2. Modules`; các dòng không đánh số (gạch đầu dòng con, đoạn văn, ghi chú, khối code) — thuộc về ID của mục đánh số gần nhất phía trên. Khi cần trích dẫn riêng một dòng như vậy, nâng nó thành mục đánh số và cấp ID mới.
- **ID bất biến**: ID không đổi khi mục được đánh số lại, di chuyển sang vị trí khác hay sang phần của module khác (tiền tố giữ nguyên), và không bao giờ được cấp lại cho mục khác.
- **Mục mới**: ID = số lớn nhất đã cấp của mã module đó (bảng "ID lớn nhất đã cấp" trong `common/requirements-change-tracker.md`) + 1, bất kể vị trí chèn. Cập nhật bảng đó cùng lúc với ghi CR.
- **Tách mục**: phần giữ ý chính giữ ID cũ (CR ghi `sửa`); phần tách ra nhận ID mới (CR ghi `thêm`).
- **Gộp mục**: giữ ID của mục giữ ý chính; các ID còn lại biến mất khỏi đặc tả, CR ghi `bỏ — gộp vào R-...`.
- **Bỏ mục**: xoá mục cùng ID khỏi đặc tả; CR ghi `bỏ`. ID đó không được cấp lại.
- **Module mới** (một phần cấp 2 mới): cần bổ sung mã module vào bảng ở `common/requirements-design-sync.md` mục 2.1 trước khi cấp ID.
- Module/nội dung ngoài phạm vi giai đoạn hiện tại được liệt kê gọn trong một mục riêng (hiện tại: mục 2.5 "Module ngoài phạm vi giai đoạn này"), không mô tả chi tiết.

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, và luôn `project_read` bản mới nhất trước khi ghi đè: theo nguyên tắc chung ở `common/00-claude-common-instructions.md` mục 3 — áp dụng nguyên vẹn cho luồng này.
- Sau khi ghi xong một thay đổi vào `business-requirements.md`, tóm tắt ngắn gọn đã thay đổi những gì cho người dùng xem (không dán lại toàn bộ nội dung file), đồng thời ghi thêm một mục vào `requirements/changelog.md` theo nguyên tắc ở `common/00-claude-common-instructions.md` mục 2.
- Đồng bộ ra máy: theo nguyên tắc chung mục 1 (`requirements/` ↔ `Z:\GoogleDrive\VanMinhViet\requirements`).

## 5. Đồng bộ với các session khác

- Xem `common/00-claude-common-instructions.md` mục 4. Lưu ý riêng cho luồng này: session thiết kế hệ thống ở `system-design/` cũng cần được báo khi `business-requirements.md` đổi, vì system-design tham chiếu ngược lại tài liệu này.

## 6. Trạng thái hiện tại (cập nhật lần cuối: xem ngày sửa file business-requirements.md)

- Đã rà soát chi tiết, đóng các gap chính: mục 2.1 (Quản Lý Người Dùng, gồm cả RBAC ở 2.1.3.1), 2.2 (Cơ Sở Dữ Liệu Văn Hóa), 2.3 (Bách Khoa Toàn Thư), 2.4 (AI Văn Minh Việt).
- Mục 2.5 ("Module ngoài phạm vi giai đoạn này") gồm Lịch & Sự Kiện, chưa cần đặc tả chi tiết.
- Mục 3 (Yêu Cầu Phi Chức Năng) đã chốt: bảo mật/quyền riêng tư (data residency Việt Nam, mã hoá truyền tải, audit log mở rộng + retention 12 tháng, MFA chưa bắt buộc, rate limiting AI công khai), hiệu năng (ước tính dung lượng lưu trữ để lại cho thiết kế kỹ thuật), nền tảng đa kênh (di động cả iOS/Android, trình duyệt hiện đại, chỉ tiếng Việt giai đoạn này, accessibility chưa yêu cầu), sao lưu (RPO/RTO 24 giờ, sao lưu hàng ngày).
- Có tài liệu thiết kế kỹ thuật riêng tại `system-design/00-claude-instructions.md`, bám theo đặc tả này.

## 7. Skill hỗ trợ đã lưu

- **`xuat-ra-docx`** (đã lưu, đang dùng được): xuất toàn bộ, đầy đủ chi tiết một tài liệu trong project này (mặc định `business-requirements.md`) ra file Word (.docx). Vì tài liệu nguồn dùng cú pháp list Markdown cho số mục thủ công (xem mục 3), khi convert bằng pandoc sẽ phát sinh dấu đầu dòng dư — skill này tự động sửa (xoá glyph bullet trong `word/numbering.xml`, giữ nguyên thụt lề) trước khi giao file.
- **`van-minh-viet-bao-cao-cong-viec`** (đã lưu, đang dùng được): tạo báo cáo công việc ngắn gọn (file Word) tóm tắt các thay đổi đã ghi vào `business-requirements.md` trong một phiên hoặc khoảng thời gian làm việc — mỗi mục nêu đã đổi gì kèm lý do ngắn gọn. Với phiên hiện tại, dựa vào chính hội thoại; với khoảng thời gian khác/nhiều session trước đó, đọc `requirements/changelog.md` (xem mục 2) để lấy đúng phạm vi thay vì phải hỏi người dùng kể lại thủ công.
