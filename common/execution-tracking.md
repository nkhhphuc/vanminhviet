# Execution Tracking — Ghi chú về theo dõi tiến độ code

> Tài liệu nội bộ (framework), không phải nguồn chân lý về nghiệp vụ/kỹ thuật. Mục đích: ghi lại quyết định về cách theo dõi tiến độ code hoá dự án Van Minh Viet, để các phiên Claude sau (trong Project này) biết bối cảnh mà không cần hỏi lại.

## 1. Bối cảnh

- Đội ngũ: chỉ có Phuc (solo developer) + Claude Code. Không có thành viên nào khác.
- Nhịp làm việc: sprint theo tuần.
- Việc code hoá thực hiện bằng Claude Code, dựa trên các tài liệu `requirements/` và `system-design/` đã export sang repo code (qua skill "Đồng bộ sang Code").
- Thứ tự build cố định theo `system-design/00-claude-instructions.md` mục 4: 01 (Kiến trúc) → 02 (Định danh) → 03 (Cơ sở tri thức văn hoá) → 04 (Bách khoa toàn thư) → 05 (Trợ lý AI) → 06 (AI Gateway, song song khi cần).

## 2. Hai file theo dõi tiến độ — sống trong repo code, KHÔNG trong Project này

Theo yêu cầu của Phuc (2026-09-15), việc theo dõi milestones/sprints/tasks được tách thành 2 file, do **Claude Code tạo và duy trì trực tiếp trong repo code** (`Z:\VanMinhSo\vanminhviet\docs\`), không phải tài liệu của Project "Van Minh Viet" trên Claude:

- **`docs/VanMinhViet_Conventions.md`** — file tĩnh, hiếm khi đổi. Gồm: vai trò của bộ đôi tài liệu, bối cảnh nhóm, thứ tự build cố định, task-ID scheme theo package, status legend, Definition of Done, Definition of Ready.
- **`docs/VanMinhViet_Execution_Plan.md`** — file sống, cập nhật sau mỗi vòng code. Gồm: milestone map, bảng task theo từng sprint (task | mô tả | tham chiếu design | trạng thái), checklist nghiệm thu từng milestone, bảng risk (rút ra từ các ghi chú ⚠ trong system-design — không bịa risk/evidence từ dự án khác), bảng progress-log.

Lý do tách: quy ước gần như không đổi, còn kế hoạch/task thay đổi liên tục — gộp chung một file khiến mỗi lần cập nhật trạng thái task có nguy cơ động vào phần quy ước.

## 3. Vị trí của 2 file này so với Project

- `requirements/` và `system-design/` (trong Project) là **nguồn chân lý** về nghiệp vụ và thiết kế.
- `VanMinhViet_Conventions.md` và `VanMinhViet_Execution_Plan.md` (trong repo code) là **execution layer** — chỉ phản ánh tiến độ thực thi, không định nghĩa lại nghiệp vụ/thiết kế. Nếu có mâu thuẫn, `requirements/`/`system-design/` trong Project luôn thắng.
- Khi cần đối chiếu tiến độ code hoá, hỏi Phuc lấy nội dung 2 file này từ repo (Claude trên Project không tự truy cập được repo code).

## 4. Lịch sử quyết định liên quan

- 2026-09-24: chạy skill "Đồng bộ sang Code" cho cả 5 luồng (`requirements`, `system-design`, `admin-web`, `partner-web`, `public-web`). Theo yêu cầu của Phuc, `changelog.md` của cả 5 luồng được xoá trắng hoàn toàn ngay sau đồng bộ — mỗi file chỉ còn lại dòng tiêu đề, không giữ dòng ghi chú về việc lược bỏ như khuôn mẫu đã dùng đợt 2026-09-23. Nội dung lịch sử vẫn còn nguyên trong các file nguồn/thiết kế và mục 6–7 của từng `00-claude-instructions.md` (đối với các luồng web).
