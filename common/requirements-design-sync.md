# Quy Trình Đồng Bộ Requirements ↔ Thiết Kế ↔ Code

> Mô tả cách theo dõi thay đổi của đặc tả (`requirements/business-requirements.md`) lan xuống các luồng thiết kế (`system-design/`, `admin-web/`, `partner-web/`, `public-web/`) và code. Dùng chung cho mọi luồng và team Code. Sổ theo dõi thực tế nằm ở `common/requirements-change-tracker.md`.

## 1. Chuỗi phụ thuộc

requirements → system-design → admin-web / partner-web / public-web → code

- Thay đổi ở tầng trên có thể ảnh hưởng tất cả các tầng dưới.
- Đề xuất từ tầng dưới (ví dụ ⚠ ở system-design, admin-web) chỉ trở thành yêu cầu chính thức khi được ghi vào `business-requirements.md` — lúc đó cũng sinh một CR như mọi thay đổi khác (mục 3).

## 2. ID yêu cầu ổn định

### 2.1. Định dạng

- Mỗi mục đánh số trong `business-requirements.md` (kể cả tiêu đề mục) mang một ID cố định, đặt ngay sau số mục:
  `- **2.2.3.12.** [R-KB-014] Nội dung...`
- Cấu trúc: `R-<mã module>-<số thứ tự 3 chữ số>`. Mã module:

| Mã | Phần đặc tả |
|---|---|
| GEN | 1. Tổng quan |
| ID | 2.1. Quản lý người dùng |
| KB | 2.2. Cơ sở dữ liệu văn hoá |
| ENC | 2.3. Bách khoa toàn thư |
| AI | 2.4. AI Văn Minh Việt |
| OOS | 2.5. Module ngoài phạm vi |
| PUB | 2.6. Web công khai |
| PTN | 2.7. Ứng dụng Tổ chức khác |
| CFG | 2.8. Cấu hình hệ thống |
| NFR | 3. Yêu cầu phi chức năng |

- Số thứ tự tăng dần trong từng mã module, cấp theo thứ tự thêm vào — không phản ánh vị trí trong tài liệu.

### 2.2. Quy tắc bất biến

- ID **không bao giờ đổi và không bao giờ dùng lại**, kể cả khi mục bị di chuyển, đánh số lại hoặc bị bỏ.
- Số mục (§) vẫn được đánh số lại khi cần (theo `requirements/00-claude-instructions.md` mục 3) — số mục chỉ để đọc, ID mới là khoá tham chiếu.
- **Bỏ một mục**: xoá khỏi đặc tả; ghi ID đó vào CR với hành động `bỏ`. ID không được cấp lại.
- **Tách một mục**: phần giữ ý chính giữ ID cũ; phần tách ra nhận ID mới.
- **Gộp nhiều mục**: giữ ID của một mục; các ID còn lại ghi `bỏ — gộp vào R-...` trong CR.
- ID mới lớn nhất đang dùng của từng mã module ghi ở đầu sổ theo dõi, để cấp ID tiếp theo không trùng.

### 2.3. Cách trích dẫn trong tài liệu các luồng thiết kế

- Phạm vi: các file trong `system-design/`, `admin-web/`, `partner-web/`, `public-web/`. Trích dẫn trong code/test theo mục 7.
- Dạng chuẩn: `R-KB-014 (§2.2.3.12)` — ID là bắt buộc, số mục đi kèm để dễ đọc.
- Khoảng mục: ghi ID cho cả hai đầu mút, dạng `R-ID-002 (§2.1.1)–R-ID-005 (§2.1.3.1)`.
- Khi số mục thay đổi mà ID không đổi, trích dẫn vẫn đúng; số mục đi kèm được cập nhật ở lần rà soát kế tiếp (mục 5).
- Ký hiệu `§` chỉ dùng cho mục của đặc tả. Mục nội bộ trong tài liệu thiết kế ghi dạng "`03` mục 4.2".

## 3. Change Request (CR)

- Mỗi lần ghi thay đổi vào `business-requirements.md` (một lượt preview được duyệt) tạo **một CR**, mã `CR-YYYYMMDD-NN` (NN đánh từ 01 trong ngày).
- Luồng requirements ghi CR vào sổ theo dõi ngay sau khi ghi đặc tả, cùng lúc với `requirements/changelog.md`. Mục changelog ghi kèm mã CR.
- Nội dung một CR trong sổ: mã, ngày, tóm tắt, danh sách ID bị ảnh hưởng kèm hành động (`thêm` / `sửa` / `bỏ` / `di chuyển`), và trạng thái xử lý ở từng luồng thiết kế. Trạng thái xử lý ở Code nằm ở file riêng (mục 4.1).

## 4. Trạng thái xử lý ở từng luồng

| Ký hiệu | Nghĩa |
|---|---|
| ⏳ | Chưa xử lý |
| 🔄 | Đang xử lý |
| ✅ | Đã xử lý xong |
| — | Không ảnh hưởng luồng này (đã đối chiếu) |

- Khi tạo CR, mọi cột luồng dưới mặc định ⏳. Chỉ luồng tương ứng mới đổi trạng thái của cột mình, sau khi đã đối chiếu.
- Một luồng chỉ xử lý CR khi luồng ngay trên nó đã ✅ hoặc — (ví dụ admin-web chờ system-design).
- Khi luồng thiết kế sửa file nguồn do một CR, mục changelog của luồng đó ghi kèm mã CR.
- **Mốc đồng bộ** của một luồng = CR mới nhất mà mọi CR trước đó ở cột luồng đó đều là ✅ hoặc —. Mốc này ghi ở đầu sổ theo dõi.
- **Đóng CR**: khi mọi cột luồng của một CR là ✅ hoặc — **và** CR đó có trạng thái ✅ hoặc — trong `planning/cr-status.md` (mục 4.1), cập nhật mốc đồng bộ nếu cần, rồi xoá dòng CR đó khỏi sổ. Commit git với message ghi mã CR (ví dụ `CR-20260928-01: đóng`) để CR vẫn tra được trong git history.
  - Trước khi đóng, luôn tự đọc `planning/cr-status.md` trong repo `vanminhviet` và đối chiếu các commit ghi ở đó trong git log của repo — không đóng CR chỉ dựa trên thông báo trạng thái từ bên ngoài.

### 4.1. Trạng thái xử lý ở Code

- Trạng thái xử lý CR ở Code ghi trong `planning/cr-status.md` ở gốc repo `vanminhviet` (trên máy: `Z:\VanMinhSo\vanminhviet\planning\cr-status.md`). File này do team Code sở hữu: chỉ team Code ghi/sửa/xoá; các luồng thiết kế chỉ đọc, không bao giờ ghi vào.
- Định dạng — một bảng, mỗi CR một dòng:

| CR | Trạng thái | Commit/PR | Ngày | Ghi chú |
|---|---|---|---|---|
| CR-20260928-01 | ✅ | `a1b2c3d` / #12 | 2026-10-02 | |

- Trạng thái dùng ký hiệu 🔄 / ✅ / — như mục 4. CR chưa có dòng trong file được hiểu là ⏳.
- Code chỉ xử lý một CR khi cột system-design và cột web liên quan trong sổ theo dõi đều là ✅ hoặc —.
- **Dọn dẹp**: sau mỗi lần đồng bộ sang Code, CR nào không còn trong sổ theo dõi (bản `docs/common/requirements-change-tracker.md` trong repo) là đã đóng — team Code xoá dòng CR đó khỏi `cr-status.md`, commit với message ghi mã CR. Không xoá dòng của CR còn trong sổ theo dõi.

## 5. Kiểm tra tham chiếu

- Script `common/tools/check-requirement-refs.py` (Python 3, không cần thư viện ngoài) đọc `requirements/business-requirements.md` và quét các file `.md` ở `system-design/`, `admin-web/`, `partner-web/`, `public-web/` (trừ `changelog.md`), báo:
  - ID được trích dẫn nhưng không còn trong đặc tả (mục đã bỏ hoặc gõ sai).
  - Số § đi kèm không khớp với số mục hiện tại của ID đó.
  - Trích dẫn `§` không kèm ID.
  - ID bị trùng trong đặc tả, hoặc bảng "ID lớn nhất đã cấp" trong sổ theo dõi thấp hơn ID thực có trong đặc tả.
- Cách chạy: `python common/tools/check-requirement-refs.py` (chạy được từ bất kỳ thư mục nào). Mỗi lỗi in kèm `file:dòng`; mã thoát 0 = không có lỗi, 1 = có lỗi.
- Chạy: sau mỗi CR, và bắt buộc trước khi chạy "Đồng bộ sang Code".

## 6. Changelog và Git

- Changelog của mỗi luồng vẫn được xoá trắng sau khi đồng bộ sang Code, nhưng **bắt buộc commit git trước khi xoá**, để lịch sử còn trong repo.
- Sổ theo dõi (`requirements-change-tracker.md`) chỉ giữ các CR đang mở; CR đã đóng tra lại qua changelog của từng luồng và `git log --grep <mã CR>`. Vì vậy mọi commit liên quan tới một CR đều ghi mã CR trong message.

## 7. Dành cho team Code

- Sổ theo dõi trong repo (`docs/common/requirements-change-tracker.md`) là bản chỉ đọc, bị ghi đè mỗi lần đồng bộ — không sửa file này.
- CR đã xong ở thiết kế (✅ hoặc — ở cột system-design và web liên quan) mà chưa có ✅ hoặc — trong `planning/cr-status.md` là phần cần cập nhật code. Ghi trạng thái và dọn dẹp theo mục 4.1.
- Trong code/test (comment, tên/mô tả test), khi cần trích yêu cầu, chỉ ghi ID (`R-KB-014`), không kèm số mục — code nằm ngoài phạm vi kiểm tra của mục 5 nên số mục đi kèm không được cập nhật.
- Nếu `requirements/`, `system-design/` mâu thuẫn với code, tài liệu thiết kế luôn thắng.
