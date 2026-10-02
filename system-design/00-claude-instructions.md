# Thiết Kế Hệ Thống Văn Minh Việt — Khung & Nguyên Tắc

> Tài liệu điều phối cho toàn bộ quá trình thiết kế kỹ thuật. Đọc `common/00-claude-instructions.md` trước (nguyên tắc dùng chung cho mọi luồng), rồi đọc file này trước khi làm việc trên bất kỳ tài liệu module nào trong thư mục `system-design/`.

## 1. Mục tiêu

- Xây dựng bộ tài liệu thiết kế kỹ thuật (kiến trúc → mô hình dữ liệu → luồng nghiệp vụ → API) đủ chi tiết để dùng làm đầu vào **thực thi dự án (code) sau này**, kể cả bằng một phiên Claude Code khác.
- Người đọc tài liệu: kiến trúc sư hệ thống (chủ trì), đội dev, và có thể trình cấp trên — nên tài liệu cần đủ rõ ràng, trình bày được, không chỉ là ghi chú nháp cá nhân.
- Nguồn chính để bám theo: `requirements/business-requirements.md` (đặc tả gốc — vẫn đang tiếp tục hoàn thiện ở một session/luồng công việc riêng). Mọi entity/quyết định thiết kế phải trích số mục tương ứng trong đặc tả gốc khi có thể. Tài liệu kỹ thuật bên ngoài (ví dụ đề xuất kiến trúc từ bên tư vấn khác) có thể dùng làm **nguồn tham khảo bổ sung** cho phần kiến trúc/tech stack — nhưng không được dùng để mở rộng phạm vi module ngoài những gì đã có trong đặc tả gốc; mọi lần dùng nguồn ngoài phải ghi rõ nguồn và trạng thái "đã chốt" hay "chưa chốt".

## 2. Ranh giới thư mục

- `requirements/` — đặc tả yêu cầu phần mềm và khung làm việc riêng cho việc biên tập đặc tả. **Không thuộc phạm vi của luồng thiết kế này** — chỉ đọc để tham chiếu, không ghi vào đây.
- `system-design/` — toàn bộ kết quả làm việc của luồng thiết kế hệ thống này: tài liệu kiến trúc, tài liệu module, sơ đồ, ghi chú...

## 3. Cách làm việc

- Đặc tả gốc còn đang thay đổi nhiều → thiết kế **từng phần một** (kiến trúc chung trước, rồi từng module): đi hết mô hình dữ liệu → kiến trúc riêng → luồng nghiệp vụ → API cho **một phần**, chốt xong mới chuyển sang phần kế tiếp. Mục đích: giới hạn phạm vi phải sửa lại mỗi khi đặc tả đổi.
- Phần "nền tảng" dùng chung (mục 5, 6 bên dưới, và tài liệu kiến trúc `01`) được chốt trước tiên vì mọi phần khác phụ thuộc vào nó — nên hạn chế thay đổi phần này trừ khi đặc tả gốc đổi trực tiếp các mục liên quan.
- Khi `requirements/business-requirements.md` thay đổi: xử lý theo CR trong sổ theo dõi `common/requirements-change-tracker.md` (quy trình ở `common/requirements-design-sync.md`).
- Trong lúc thảo luận, giữ bản nháp gọn nhẹ để sửa nhanh. Khi một phần được xác nhận chốt, làm lại thành bản "sạch" hoàn chỉnh, sẵn sàng chia sẻ cho đội dev/cấp trên.

## 4. Thứ tự build

1. **Kiến trúc & Tech Stack** (`01`) — nền tảng dùng chung cho mọi module: tech stack, quy ước API, background job, bảo mật... Không theo cấu trúc chuẩn module ở mục 5 (vì không phải một module nghiệp vụ) mà có cấu trúc riêng phù hợp nội dung kiến trúc.
2. **Quản lý người dùng** (`02`) — nền tảng Role/User mà mọi module nghiệp vụ khác phụ thuộc vào.
3. **Cơ sở dữ liệu văn hóa** (`03`) — lõi nghiệp vụ (Đề tài nghiên cứu, Tư liệu gốc, Hạng mục tri thức).
4. **Bách khoa toàn thư** (`04`).
5. **AI Văn Minh Việt** (`05`).
6. **AI Gateway** (`06`) — service Python riêng phục vụ RAG (module 05) và AI Verification (module 03), hiện thực quyết định kiến trúc ở D-SD01-006 (¶6).
7. **Cấu hình hệ thống** (`07`) — tham số vận hành/nghiệp vụ dùng chung (package `/shared`), do Quản trị hệ thống điều chỉnh qua Admin nội bộ.

*Lịch & Sự Kiện hiện đang ngoài phạm vi đặc tả giai đoạn này (đặc tả gốc mục R-OOS-006 (§2.5.5)) — sẽ bổ sung khi được đặc tả chi tiết.*

## 5. Cấu trúc chuẩn cho tài liệu module (02–05, 07)

Áp dụng cho các module nghiệp vụ 02–05 và tài liệu 07. Tài liệu `01` và `06` không phải module nghiệp vụ ánh xạ 1-1 với đặc tả gốc nên có cấu trúc riêng phù hợp nội dung.

Mỗi file `system-design/0X-<tên module tiếng Anh>.md` nên theo cấu trúc (lịch sử thay đổi không nhúng ở đây nữa — ghi chung vào `system-design/changelog.md`, xem mục 3):

1. **Tổng quan module** — vai trò của module trong hệ thống, phụ thuộc vào module nào.
2. **Mô hình dữ liệu** — entity, field, kiểu dữ liệu, quan hệ, trích số mục đặc tả gốc.
3. **Luồng trạng thái / nghiệp vụ** (nếu có) — state machine, vai trò/role thực hiện từng bước.
4. **Kiến trúc riêng của module** (nếu có điểm đặc thù kỹ thuật, ngoài phần đã ghi ở `01-architecture-and-tech-stack.md`).
5. **Thiết kế API**.
6. **Vấn đề mở / giả định** — đánh dấu **⚠ Đề xuất bổ sung** cho phần không có trong đặc tả gốc mà do người thiết kế đề xuất thêm để hệ thống vận hành được; cần xác nhận riêng.

## 6. Nguyên tắc mô hình hoá dữ liệu chung

- Khoá chính: UUID.
- Tên bảng/field: `snake_case`, dùng **tiếng Anh** (kể cả khi entity/khái niệm nghiệp vụ có tên tiếng Việt — dịch sang tiếng Anh cho tên bảng/field, tương tự nguyên tắc path API ở dưới).
- Vị trí tham chiếu (trang/dòng văn bản, khung ảnh, mốc thời gian âm thanh/phim...): lưu dạng JSONB, cấu trúc tuỳ theo loại file — không ép chung một schema cứng.
- Thực thể có vòng đời versioned theo đặc tả (ví dụ Hạng mục tri thức): tách bảng "phiên bản" riêng khỏi bảng định danh cha; bảng cha chỉ giữ ID + con trỏ phiên bản hiện hành. Phiên bản cũ giữ nguyên, không ghi đè.
- Role có 2 loại theo đặc tả (R-ID-005 (§2.1.3.1)): **role theo chức năng** và **role theo phạm vi** — phạm vi không giới hạn ở Đề tài nghiên cứu (ví dụ Nghiên cứu, Xét duyệt — tự sinh khi tạo đề tài) mà là cơ chế chung, có thể mở rộng theo phạm vi khác (đặc tả nêu thêm ví dụ: theo Cương vực). Mô hình hoá trong cùng một bảng `roles`, dùng cột phân loại phạm vi (`scope_type`) + tham chiếu phạm vi (`scope_id`) linh hoạt theo loại, không hard-code riêng cho Đề tài nghiên cứu.
- Thông tin mang tính tập hợp (set) — trạng thái, phân loại, hoặc bất kỳ trường nào nhận giá trị từ một tập hữu hạn — nếu tập giá trị đó có tính chất mở hoặc có thể thay đổi theo thời gian: dùng kiểu `text`/`varchar` + validate ở tầng ứng dụng, **không** dùng kiểu ENUM của database (dù là Postgres hay hệ quản trị khác) — vì thêm giá trị vào tập thì dễ, nhưng xoá/đổi tên giá trị đã có trong kiểu ENUM thường rất phiền (không sửa trực tiếp được, phải tạo type mới rồi migrate cột).
- **Path API dùng tiếng Anh** (route path, tên resource trong URL — ví dụ `/encyclopedia/entries`, `/encyclopedia/entries/{id}/cultural-domains`), kể cả khi entity/khái niệm nghiệp vụ có tên tiếng Việt (ví dụ Mục từ → `entries`, Cương vực → `cultural-domains`). Ngược lại, **giá trị dữ liệu mang tính nghiệp vụ** (mã trạng thái, tên role...) vẫn dùng tiếng Việt không dấu theo đúng thuật ngữ đặc tả gốc (ví dụ `dang_nghien_cuu`, `nhap_lieu`) — không dịch sang tiếng Anh, để giữ đối chiếu trực tiếp với đặc tả.
- **operationId**: mỗi endpoint trong mục "Thiết kế API" có một operationId, ghi ở cột `operationId` ngay sau cột Path trong bảng endpoint. Cách đặt tên, quy tắc bất biến và cách trích dẫn theo `common/requirements-design-sync.md` mục 2.5.
- Luôn phân biệt rõ: phần bám sát đặc tả gốc (trích số mục) vs. phần do người thiết kế đề xuất thêm (đánh dấu ⚠, cần xác nhận).

## 7. Nơi lưu trữ & quy ước đặt tên

- Quy ước đặt tên file: `system-design/0X-<tên phần theo thứ tự build ở mục 4, tiếng Anh, gạch ngang>.md`. File này là `00-claude-instructions.md`; lịch sử thay đổi chung của cả thư mục nằm ở `system-design/changelog.md`.
- `system-design/index.md` — mục lục bộ tài liệu thiết kế (file ↔ package/route ↔ phụ thuộc ↔ trạng thái), dành cho người đọc và Team Code. Khi thêm file mới, đổi tên file, hoặc trạng thái/phụ thuộc của một tài liệu thay đổi: cập nhật `index.md` trong cùng lần ghi.
- Nguyên tắc lưu trữ và preview trước khi ghi: xem `common/00-claude-instructions.md` mục 1 và 3.

## 8. Việc tồn đọng

Việc thiết kế đã biết nhưng chưa làm. Khi làm xong một việc, xoá dòng đó và ghi DC tương ứng vào sổ theo dõi.

- **Phần quản lý section "Hôm nay"** (CR-20261002-01, R-PUB-013 (§2.6.6)–R-PUB-018 (§2.6.6.5), R-CFG-010 (§2.8.4.5)). Đã có hợp đồng `public.listTodayItems` (D-SD04-018 (¶5.4)). Còn: nơi đặt module (tài liệu riêng hay trong `04`), dữ liệu nguồn tin và tin, đọc tin định kỳ, agent AI gợi ý Mục từ (hướng đang cân nhắc: agent ở AI Gateway, dữ liệu và duyệt ở Go), duyệt và gỡ tin, tham số cấu hình, audit, thời hạn tin theo R-NFR-042 (§3.7.5), `actions` cho tin. Khi thiết kế xong, tạo DC; `public.listTodayItems` thôi trả rỗng.
