# Changelog — Business Requirements

## 2026-09-26

- Bổ sung từ các vấn đề mở của System Design: vô hiệu hoá/kích hoạt lại tài khoản Nhân viên, buộc đăng xuất khi vô hiệu hoá (2.1.5.7); chính sách mật khẩu (2.1.5.8); tạm khoá đăng nhập (2.1.5.9); tài khoản Quản trị hệ thống đầu tiên (2.1.5.2.1); thời hạn đường dẫn mời/đặt lại mật khẩu do Quản trị hệ thống cấu hình (2.1.5.5); Chủ nhiệm đề tài tìm Nhân viên mọi Tổ chức (2.2.5.5); trạng thái "Đang xét duyệt AI" và phạm vi kích hoạt lại AI Verification (sơ đồ 2.2.6, 2.2.6.5.1–2.2.6.5.2, 2.2.3.11.4); cảnh báo nguồn lỗi thời, thống nhất cách gọi "phiên bản đang được sử dụng" khi đồng bộ Mục từ (2.3.3, 2.3.3.1, 2.3.4.1, 2.3.8.2); nhận xét xét duyệt Mục từ, bắt buộc khi không đạt (2.3.5.3–2.3.5.4); quản lý và xoá Cương vực (2.3.7.5); hội thoại nhiều lượt, câu trả lời khi không có thông tin, câu miễn trừ (2.4.6–2.4.8, 2.6.4.3); nhật ký hỏi đáp và rà soát chất lượng, lưu có thời hạn (2.4.9); mục mới Cấu hình hệ thống (2.8, sửa tham chiếu ở 2.2.6.5); rate limiting AI công khai theo IP, mặc định tắt (3.1.6); bổ sung hành động audit và dọn audit log định kỳ theo cấu hình, tối thiểu 12 tháng (3.1.2).
- Bổ sung chức năng Nhân viên tự đổi mật khẩu khi đang đăng nhập (2.1.5.10): cần mật khẩu hiện tại, nhập sai tính vào tạm khoá đăng nhập; mật khẩu mới theo chính sách và không trùng mật khẩu hiện tại; đổi xong thì đăng xuất mọi phiên; không gửi email thông báo. Sửa tham chiếu ở 2.1.5.8, 2.1.5.9; thêm hành động đổi mật khẩu vào audit log (3.1.2).

## 2026-09-28

- CR-20260928-01: gắn ID ổn định `R-<mã module>-<số>` cho toàn bộ 274 mục đánh số trong `business-requirements.md` (GEN 001–016, ID 001–039, KB 001–094, ENC 001–043, AI 001–014, OOS 001–009, PUB 001–012, PTN 001–011, CFG 001–011, NFR 001–025); `## 2. Modules` và các dòng không đánh số không mang ID. Không đổi nội dung, số mục hay thứ tự. Cập nhật `00-claude-instructions.md`: mục 2 (tham chiếu theo ID), mục 3 (quy tắc ID bất biến, cấp ID cho mục mới/tách/gộp/bỏ, module mới).
