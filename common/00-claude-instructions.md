# Nguyên Tắc Chung — Dự Án Văn Minh Việt

> Áp dụng cho mọi luồng làm việc (conversation) trong project này. Mỗi luồng có file điều phối riêng `00-claude-instructions.md` trong thư mục của mình, chứa phần đặc thù và tham chiếu ngược lại file này cho phần dùng chung. Khi bắt đầu một luồng, đọc file này trước, rồi đọc file "00" của đúng luồng đang làm việc.

## 1. Mỗi luồng = Một thư mục trên máy

- Toàn bộ tài liệu của project nằm trên máy người dùng, trong thư mục gốc `Z:\VanMinhSo\docs`. Đây là nơi lưu trữ duy nhất và là nguồn chân lý; Claude đọc và ghi trực tiếp vào đây. Project trên claude.ai không chứa bản sao tài liệu.
- Mỗi luồng làm việc (requirements, system-design, public-web, admin-web, partner-web, và các luồng phát sinh sau này) có một thư mục con cùng tên: `Z:\VanMinhSo\docs\<tên luồng>` (ví dụ `Z:\VanMinhSo\docs\requirements`). Tài liệu dùng chung cho mọi luồng nằm ở `Z:\VanMinhSo\docs\common`.
- Mọi file phát sinh từ một luồng chỉ lưu trong thư mục của luồng đó — không rải rác sang thư mục khác.
- **Thư mục `outputs`** (`Z:\VanMinhSo\docs\outputs`) là nơi duy nhất chứa các file xuất/phái sinh: bản preview soạn ra file, báo cáo công việc, báo cáo tiến độ, bản xuất Word/PDF/HTML/sơ đồ… — ngoại lệ của quy tắc trên, kể cả khi file đó xuất từ một luồng cụ thể. File trong `outputs` không phải nguồn chân lý, không đồng bộ sang Code và có thể bị xoá bất cứ lúc nào. Không tạo thêm thư mục output nào khác ở gốc `docs` hay trong thư mục luồng. Tên file trong `outputs` vẫn theo quy ước đặt tên bên dưới, nên bắt đầu bằng tên luồng hoặc loại file và kèm ngày, ví dụ `requirements-export-2026-09-28.docx`, `bao-cao-tien-do-2026-09-28.html`.
- Luôn hỏi/xác nhận trước khi lưu vào thư mục.
- **Quy ước đặt tên thư mục & file**: tên thư mục và tên file trong project này dùng tiếng Anh, chữ thường (lowercase), không dấu, cách nhau bằng gạch ngang (`-`), không dùng khoảng trắng hay ký tự đặc biệt — để tránh lỗi khi đồng bộ/di chuyển file giữa các hệ điều hành. Nội dung bên trong file (tiêu đề, văn bản) vẫn viết bằng tiếng Việt như bình thường; chỉ tên thư mục/tên file/đường dẫn theo quy ước này.

## 2. Mỗi luồng theo dõi thay đổi bằng file Changelog riêng

- Mỗi thư mục luồng có một file `changelog.md` riêng, là nhật ký các thay đổi đã ghi vào (các) file nguồn của luồng đó — không phải nguồn chân lý, chỉ phục vụ tra cứu lịch sử và tạo báo cáo công việc.
- Sau khi ghi một thay đổi vào file nguồn, thêm ngay một mục vào Changelog tương ứng (ngày + tóm tắt ngắn gọn, đúng nội dung đã tóm tắt cho người dùng, nêu rõ file nào bị ảnh hưởng nếu thư mục có nhiều file) — không cần preview riêng cho bước ghi Changelog.
- Danh sách hiện có: `requirements/changelog.md`, `system-design/changelog.md`, `public-web/changelog.md`, `admin-web/changelog.md`, `partner-web/changelog.md`.
- **Đồng bộ thay đổi đặc tả giữa các luồng**: mỗi thay đổi ghi vào `requirements/business-requirements.md` là một CR, được theo dõi chéo giữa các luồng theo quy trình ở `common/requirements-design-sync.md`. Sổ theo dõi các CR chưa đồng bộ xong: `common/requirements-change-tracker.md`. Khi bắt đầu làm việc ở một luồng thiết kế, kiểm tra sổ này xem còn CR nào đang chờ luồng đó xử lý.
- **Văn phong trong file nguồn**: file nguồn chỉ mô tả đúng trạng thái/thiết kế **hiện hành** — không diễn giải lại lý do thay đổi, không so sánh với phiên bản trước ("so với bản trước...", "thay thế cơ chế X cũ...", "bản 2026-09-XX từng..."), không kể lại quá trình trao đổi dẫn tới quyết định. Toàn bộ lịch sử đó đã có trong Changelog (mục trên) — không lặp lại trong file nguồn. Dấu **⚠** vẫn giữ để đánh dấu phần vượt ngoài đặc tả gốc/do người thiết kế tự đề xuất, cần lưu ý hoặc chờ xác nhận riêng — nhưng chỉ nêu đúng phần đó đang là gì, không kể vì sao/khi nào nó đổi.

## 3. Quy trình chỉnh sửa — luôn preview trước khi ghi

- Nguyên tắc bắt buộc, áp dụng cho mọi luồng: trước khi ghi bất kỳ thay đổi nào vào file nguồn của một luồng, luôn trình bày bản preview đầy đủ nội dung sẽ thay đổi, chỉ ghi vào file sau khi người dùng xác nhận (ví dụ gõ "duyệt").
- Với các mục còn mơ hồ, thiếu quan hệ/quy tắc nghiệp vụ, hoặc là quyết định thiết kế có nhiều lựa chọn: đặt câu hỏi làm rõ trước (có thể qua nhiều vòng hỏi–đáp), không tự suy đoán rồi ghi thẳng.
- Ngay trước khi soạn preview và ngay trước khi ghi, luôn đọc lại bản mới nhất của file từ thư mục trên máy — tránh ghi đè thay đổi mà session khác hoặc người dùng vừa thêm vào. Nếu file đã đổi so với lúc soạn preview, báo người dùng và soạn lại preview. Khi ghi, sửa tại chỗ đúng phần đã duyệt (bằng lệnh/script đọc chính file đó), không gõ lại toàn bộ nội dung file.

## 4. Đồng bộ nhận biết giữa các session

- Mọi session dùng chung một thư mục trên máy, nên không cần báo nhau khi file thay đổi — mỗi session tự đọc lại file từ máy trước khi dùng (mục 3). Nội dung đã đọc từ trước trong một session có thể đã cũ: khi quay lại một session đang chờ, đọc lại các file liên quan trước khi làm tiếp.
- Nếu một session làm việc bị mất hoặc cần chuyển sang session mới: mở session mới, yêu cầu đọc file `00-claude-instructions.md` của đúng luồng cùng file này là đủ để tiếp tục đúng mạch, không cần chép lại lịch sử hội thoại cũ.

## 5. Làm việc với Git/GitHub

- Nguyên tắc chung: mọi thao tác liên quan đến Git/GitHub (commit, push, pull, checkout, tạo branch, clone, tạo pull request/issue qua `gh`, v.v.) — dù thực hiện trên máy người dùng hay trong session cloud — luôn dùng tài khoản GitHub của chính người dùng (git identity/credentials, hoặc phiên đăng nhập `gh`/token đã cấu hình sẵn cho người dùng), không dùng tài khoản, identity hay token mặc định nào khác (kể cả tài khoản/identity gắn với Claude).
- Dùng đúng git identity/credentials đã cấu hình sẵn trên máy. Không tự thêm, sửa hay ghi đè cấu hình git (`user.name`, `user.email`, credential helper, remote, v.v.) trừ khi được yêu cầu rõ ràng.
- Commit message và mô tả pull request **không bao giờ** được chứa dòng ghi công cho Claude/AI (ví dụ `Co-Authored-By: Claude...`, link phiên Claude, "Generated with Claude Code"). Chỉ ghi nội dung thay đổi.
