# Đặc Tả Giao Diện Web Admin Nội Bộ — Khung & Nguyên Tắc

> Tài liệu điều phối cho quá trình thiết kế giao diện Admin nội bộ (Quasar SPA, dành cho Nhân viên thuộc Tổ chức Văn Minh Việt — R-GEN-009 (§1.2.3.1) đặc tả gốc). Đọc `common/00-claude-instructions.md` trước, rồi đọc file này trước khi chỉnh sửa `admin-web-design.md`, kể cả ở một session khác.

## 1. Mục tiêu

- Thiết kế/biên tập `admin-web-design.md` thành một đặc tả giao diện đủ chi tiết để đội dev dùng làm đầu vào build giao diện Admin nội bộ.
- Đối tượng dùng: Nhân viên Tổ chức Văn Minh Việt — đầy đủ chức năng, gồm quản lý người dùng/phân quyền/Tổ chức, nạp liệu, nghiên cứu/xét duyệt Hạng mục tri thức, biên tập Mục từ... (theo ranh giới route `/api/v1/admin/...` đã chốt ở D-SD01-002 (¶2)).
- Vì là công cụ nội bộ, ưu tiên rõ ràng chức năng và tốc độ thao tác hơn là trải nghiệm hình ảnh — không cần mockup chi tiết như `public-web/`, wireframe/mô tả bố cục ở mức đủ dùng cho dev là được, trừ khi có yêu cầu khác.

## 2. File nguồn & ranh giới thư mục

- `admin-web/admin-web-design.md` là **nguồn chân lý duy nhất** cho đặc tả giao diện Admin nội bộ. Không tạo thêm bản sao/bản nháp song song trong project.
- `requirements/` (đặc tả nghiệp vụ gốc) và `system-design/` (thiết kế kỹ thuật, gồm mô hình dữ liệu/API mà giao diện này gọi vào) — **không thuộc phạm vi của luồng này**, chỉ đọc để đối chiếu, không ghi vào đó.
- `admin-web/changelog.md` là nhật ký các thay đổi đã ghi vào `admin-web-design.md` (xem quy tắc chung ở `common/00-claude-instructions.md` mục 2).
- Mọi file phát sinh từ luồng này chỉ lưu trong thư mục `admin-web/` — không rải rác sang thư mục khác.

## 3. Quy ước cấu trúc tài liệu

- Đánh số màn hình theo mục `4.x` (một màn hình/nhóm màn hình = một mục con), giữ nguyên cách đánh số hiện có khi thêm màn hình mới để không xáo trộn tham chiếu.
- ID thiết kế: mục 3 (Quy ước chung) và từng màn hình 4.x mang ID `D-ADM-NNN` đặt ngay sau số mục trong tiêu đề, theo `common/requirements-design-sync.md` mục 2.4. Màn hình mới nhận ID kế tiếp theo bảng "ID thiết kế lớn nhất đã cấp" trong `common/requirements-change-tracker.md`; ID không đổi khi đánh số lại mục. Trong `admin-web-design.md`, trích mục có ID dùng dạng `D-ADM-019 (¶4.19)` (kể cả khi nhắc số màn hình), mục không có ID dùng `¶N`; trích system-design dùng `D-SD0X-NNN (¶N)`.
- Mỗi màn hình nên ghi rõ: vai trò/quyền nào được truy cập (đối chiếu `system-design/02-identity.md`), API/module backend liên quan (đối chiếu package trong D-SD01-002 (¶2): `/identity`, `/knowledge`, `/gate`, `/encyclopedia`...); endpoint trích bằng operationId `` `op` `` (không kèm ID mục; theo `common/requirements-design-sync.md` mục 2.5).
- Phần nào là thiết kế UI đi trước đặc tả nghiệp vụ (chưa có cơ sở ở `business-requirements.md` hoặc `system-design/`) cần đánh dấu rõ ràng (ví dụ ghi chú ngay dưới tiêu đề màn hình).

## 4. Quy trình chỉnh sửa

- Preview trước khi ghi, và luôn đọc lại bản mới nhất từ máy trước khi ghi: theo nguyên tắc chung ở `common/00-claude-instructions.md` mục 3.
- Sau khi ghi xong một thay đổi vào `admin-web-design.md`, tóm tắt ngắn gọn cho người dùng xem, đồng thời ghi thêm một mục vào `admin-web/changelog.md`.

## 5. Đối chiếu với Business Requirements / System Design — quy trình xử lý điểm lệch

Khi phát hiện một điểm trong `admin-web-design.md` không có cơ sở (hoặc lệch) so với `requirements/business-requirements.md` hoặc `system-design/`:

1. Nêu rõ điểm lệch (chức năng/thành phần nào, khớp hay không khớp mục nào).
2. Hỏi người dùng chọn hướng xử lý: (a) giữ trong `admin-web-design.md` kèm ghi chú rõ đây là thiết kế đi trước; (b) tạm gỡ khỏi tài liệu giao diện; (c) để lại xử lý sau; (d) gửi đề xuất bổ sung thiết kế sang `system-design/` (thuần kỹ thuật, không đổi hành vi nghiệp vụ) — nếu người dùng chọn hướng này, việc soạn/ghi đề xuất thực hiện trong đúng luồng `system-design` (đọc `system-design/00-claude-instructions.md` trước), không ghi trực tiếp từ luồng `admin-web`.
3. **Không tự sửa `business-requirements.md` hay tài liệu `system-design/` trong luồng này.**
4. Ghi nhận kết quả từng điểm vào mục 7 (Trạng thái hiện tại) của chính file này.

## 6. Quyết định đã chốt

- **Màn hình Nhật ký hoạt động (4.21)**: phạm vi chỉ lịch sử audit log (không theo dõi "đang online"); cập nhật bằng polling định kỳ phía client (không WebSocket/SSE); quyền xem giới hạn role `quan_tri_he_thong`, xem toàn bộ không giới hạn phạm vi/Tổ chức.
- **Nhóm Cơ sở dữ liệu văn hóa (4.8–4.15)**: theo đúng mô hình dữ liệu/state machine ở `system-design/03-cultural-knowledge-base.md` — Tư liệu gốc đồng bộ từ MinIO/S3 (không upload thủ công qua UI), Hạng mục tri thức dùng cơ chế "Người phụ trách" (`assignee_id`) xuyên suốt vòng đời.
- **Nhóm Bách khoa toàn thư (4.16–4.20)**: theo đúng mô hình dữ liệu/state machine ở `system-design/04-encyclopedia.md`. Quản lý danh mục Cương vực (4.20 — tạo/sửa/xoá; xoá bị chặn khi còn Mục từ đang gán, 409 `cultural_domain_in_use`) giới hạn cho role `bien_tap`.
- **Nút "Cưỡng chế nhả" (Force Release)**: hiện ở cả 4 màn hình có khối "Người phụ trách" — 4.13, 4.14, 4.17, 4.18 — chỉ cho role `quan_tri_he_thong`, chỉ khi đang có người phụ trách.
- **Xét duyệt Mục từ (4.18)**: nút Đạt/Không đạt xét duyệt không giới hạn theo `assignee_id` — khác Hạng mục tri thức (module 03), là chủ ý.
- **Nguyên tắc "bức tranh tổng thể"**: giao diện luôn thể hiện cấu trúc điều hướng/phân cấp dữ liệu toàn hệ thống và vị trí màn hình hiện tại, áp dụng cho toàn bộ 28 màn hình, qua 4 cơ chế: Breadcrumb (đầu mỗi màn hình con, trừ nhóm Xác thực và Dashboard), Stepper trạng thái theo cụm (4.13/4.14/4.15 và 4.17/4.18/4.19 — "Không đạt xét duyệt"/"Mở lại" thể hiện bằng mũi tên cong, không phải bước riêng), Sidebar luôn highlight mục đang chọn + mục "Tổng quan" đứng đầu, Topbar hiển thị tên nhóm/module hiện tại.
- **Nhật ký hoạt động — lọc & hiển thị (4.21)**: cột Người thực hiện theo `actor_type`; nhãn hành động theo Danh mục sự kiện audit ở D-SD01-002 (¶2); lọc theo đối tượng cụ thể chỉ qua icon trên dòng hoặc nút "Lịch sử hoạt động" (chỉ `quan_tri_he_thong`) ở các màn chi tiết 4.5, 4.7, 4.9, 4.11, 4.13–4.15, 4.17–4.19 và "Lịch sử thay đổi cấu hình" ở 4.28; popup `detail` theo quy ước `detail` của SD01.
- **Dashboard (4.22)**: nội dung hoàn toàn tĩnh — sơ đồ pipeline nghiệp vụ tổng thể (Khối 1) + mô tả ngắn từng nhóm chức năng (Khối 2), không có chip đếm số liệu, không phụ thuộc API `stats`.
- **Nhóm Trợ lý AI (4.23–4.25)**: theo `system-design/05-ai-assistant.md` (hợp đồng SSE D-SD05-012 (¶5.1), API rà soát D-SD05-013 (¶5.2)). 4.23 cho mọi Nhân viên, chỉ giữ một hội thoại hiện tại (không danh sách hội thoại cũ), lưu tạm trong localStorage theo Nhân viên trong `assistant.conversation_ttl_hours` (mặc định 6 giờ, qua `clientSettings.getSettings`) tính từ lượt hỏi cuối để chat tiếp khi tải lại trang (xoá khi "Hội thoại mới"/Đăng xuất), trích dẫn mở Trang chi tiết Mục từ của Web công khai, cảnh báo cờ self-audit dưới câu trả lời. 4.24–4.25 chỉ `quan_tri_he_thong`, chỉ đọc. 4.23 hiện dải ảnh minh hoạ (tối đa 3 ảnh từ `cover_image` của `citations`) như Web công khai; khi khôi phục từ localStorage, ảnh có `url_expires_at` đã qua bị ẩn.
- **Theo dõi job nền (4.26)**: theo D-SD01-004 (¶4) (API `shared.listJobs`, `shared.getJob`, `shared.retryJob`, `shared.cancelJob`). Chỉ `quan_tri_he_thong`; Chạy lại job lỗi, Huỷ job đang chờ (có cảnh báo hệ quả theo loại job); polling như 4.21 (chu kỳ theo `operations.admin_polling_interval_seconds`).
- **Kích hoạt AI Verification (4.13/4.14)**: nút hiện theo `can_trigger_ai_verification` (D-SD03-023 (¶5.3)), giao diện không tự kiểm role; tách 2 nhãn "Kích hoạt AI Verification" (`cho_xet_duyet`) / "Kích hoạt lại AI Verification" (các trạng thái còn lại); kết quả "Gửi xét duyệt" (có chạy AI ngay hay chờ kích hoạt) dựa vào `status` trả về; tại `dang_xet_duyet_ai` (4.13), dòng trạng thái theo `ai_verification_running` (đang chạy / đã dừng cần kích hoạt lại), nút Kích hoạt lại luôn hiện; kết quả kích hoạt (4.13/4.14) theo `merged_into_running_job` (gộp vào job đang chạy → thông báo "AI Verification đang chạy…").
- **Đánh chỉ mục lại cho AI (4.19)**: nút chỉ cho `quan_tri_he_thong`, khi Mục từ có phiên bản công khai.
- **Menu tài khoản & Đăng xuất (D-ADM-029 (¶3))**: Topbar nền kem `#F7F2EA`, chữ `#252421`/Chữ phụ, không dùng chữ trắng; chữ trắng `#FFFFFF` chỉ dùng trên nền Accent. Menu tài khoản gồm "Đổi mật khẩu" và "Đăng xuất"; Đăng xuất không hỏi xác nhận (trừ khi có form chỉnh sửa dở), luôn xoá phiên cục bộ kể cả khi API lỗi; hết phiên ngoài ý muốn xử lý như Đăng xuất kèm thông báo và quay lại màn hình trước sau khi đăng nhập lại; 401 `session_revoked` → không làm mới phiên, về thẳng 4.1.
- **Bảng màu & font (D-ADM-029 (¶3))**: mã màu theo D-PUB-011 (¶2.1) — Accent `#C4171D`, Accent đậm `#9C2B2B`, nền kem `#F7F2EA`, chữ `#252421`/`#6D6A64`, viền `#E6E0D7`; font Be Vietnam Pro toàn ứng dụng. Không dùng Lora, màu phụ trang trí, ảnh thuỷ mặc, thang bo góc của Web công khai. Vùng nội dung giữ nền trắng/xám trung tính, badge trạng thái giữ màu ngữ nghĩa.
- **Đổi mật khẩu (4.27)**: dialog từ menu tài khoản, mọi Nhân viên; theo D-SD02-006 (¶3.4) (`auth.changePassword`); kiểm tra chính sách mật khẩu theo `auth.getPasswordPolicy`; `login_locked` → xử lý như phiên bị thu hồi; đổi thành công → đăng xuất mọi thiết bị (kể cả thiết bị đang dùng), về 4.1.
- **Cấu hình hệ thống (4.28)**: theo `system-design/07-system-settings.md`; nhóm Sidebar riêng "Hệ thống", chỉ `quan_tri_he_thong`; lưu theo từng nhóm (nguyên khối), khôi phục mặc định từng tham số; xác nhận khi giảm thời hạn lưu.
- **Khởi tạo nội dung Mục từ bằng AI (4.17)**: theo D-SD04-019 (¶3.5). Nút ở đầu khối Nội dung, chỉ Người phụ trách khi `soan_thao`; cảnh báo ghi đè gộp cảnh báo thay đổi chưa lưu trong một hộp thoại; polling `encyclopedia.getEntry` cố định 5 giây khi đang xử lý; khi `content_generation` về `null`, UI tự suy ra thành công hay bị bỏ theo trạng thái, Người phụ trách và danh sách nguồn (không đổi API); lỗi `source_content_too_long` hiện thông báo gợi ý gỡ bớt nguồn.
- **Tài khoản gốc & Hộp thư DEV (DC-20261001-05)**: 4.4/4.5 chip "Tài khoản gốc" theo `is_root_admin`; thao tác bị chặn (Vô hiệu hoá, gỡ role `quan_tri_he_thong`, đổi Tổ chức) vẫn hiện nhưng vô hiệu kèm tooltip. Topbar: chip vàng "DEV · Hộp thư" khi `dev_mailbox_url` khác `null`, mọi Nhân viên, mở tab mới.

## 7. Trạng thái hiện tại

- 28 màn hình (4.1–4.28) đã thiết kế xong: Nhóm Tổng quan (4.22), Nhóm Xác thực (4.1–4.3, 4.27), Nhóm Quản lý người dùng & Tổ chức (4.4–4.7), Nhóm Cơ sở dữ liệu văn hóa (4.8–4.15), Nhóm Bách khoa toàn thư (4.16–4.20), Nhóm Trợ lý AI (4.23–4.25), Nhóm Giám sát (4.21, 4.26), Nhóm Hệ thống (4.28).
- Điểm lệch đang mở: **Hộp thư DEV trước đăng nhập (4.1–4.3)** — `dev_mailbox_url` hiện chỉ có sau đăng nhập; đã chọn hướng (d): đề xuất system-design trả trường này qua một endpoint không cần xác thực (soạn đề xuất ở luồng system-design). **Thời gian lưu hội thoại AI (4.23)** — đã gửi đề xuất sang system-design đổi mặc định `assistant.conversation_ttl_hours` xuống 60 phút cho cả 2 kênh (bằng thời hạn URL ảnh ký sẵn); 4.23 giữ ghi mặc định 6 giờ theo system-design hiện hành cho tới khi chốt. Các màn hình còn lại khớp `business-requirements.md`/`system-design/01–05, 07`.

## 8. Đồng bộ với session khác

- Xem `common/00-claude-instructions.md` mục 4.
