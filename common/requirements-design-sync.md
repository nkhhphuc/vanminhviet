# Quy Trình Đồng Bộ Requirements ↔ Thiết Kế ↔ Code

> Mô tả cách theo dõi thay đổi — của đặc tả (`requirements/business-requirements.md`) và của riêng tài liệu thiết kế — lan xuống các luồng thiết kế (`system-design/`, `admin-web/`, `partner-web/`, `public-web/`) và code. Dùng chung cho mọi luồng và team Code. Sổ theo dõi thực tế nằm ở `common/requirements-change-tracker.md`.

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
- Ký hiệu `§` chỉ dùng cho số mục của đặc tả. Số mục của tài liệu thiết kế dùng ký hiệu `¶`, trích theo mục 2.4.

### 2.4. ID và cách trích dẫn mục thiết kế

- **Tài liệu thiết kế** gồm: `system-design/01`–`07`, `admin-web/admin-web-design.md`, `partner-web/partner-web-design.md`, `public-web/public-web-layout.md`. Các file `00-claude-instructions.md`, `changelog.md` và file trong `common/` không thuộc nhóm này. Khi trích mục của các file đó, vẫn ghi "mục N".
- **Định dạng ID**: `D-<mã file>-<số thứ tự 3 chữ số>`. Mã file:

| Mã | File |
|---|---|
| SD01 … SD07 | `system-design/01-…` … `07-…` (theo số file) |
| ADM | `admin-web/admin-web-design.md` |
| PRT | `partner-web/partner-web-design.md` |
| PUB | `public-web/public-web-layout.md` |

- Khi thêm một tài liệu thiết kế mới, phải bổ sung mã file của nó vào bảng này trước khi cấp ID.
- **Mục được gắn ID** là các mục mà luồng khác hoặc team Code trỏ tới:
  - system-design: từng bảng dữ liệu (2.x), từng luồng nghiệp vụ (3.x), từng thành phần kiến trúc (4.x), từng nhóm API (5.x). Riêng `01` và `06`: mọi mục `##`/`###` có nội dung kỹ thuật, trừ các mục "Mục đích" và "Vấn đề mở".
  - Các luồng web: mục "Quy ước chung" (3), từng màn hình (4.x), và từng thành phần dùng chung có tiêu đề riêng.
  - Mọi mục khác: gắn ID vào lần đầu tiên mục đó được trích từ một file khác.
  - Không mang ID: mục tổng quan, mục đích, vấn đề mở, và các tiêu đề chỉ dùng để nhóm mục.
- **Vị trí đặt ID**: ngay sau số mục trong tiêu đề. Ví dụ ``### 2.1. [D-SD03-001] `research_topic` …``, `## 4.19. [D-ADM-019] Biên tập Mục từ`.
- **Cấp số**: số thứ tự tăng dần trong từng mã file, theo thứ tự thêm vào, không phản ánh vị trí trong file. ID lớn nhất đã cấp của từng mã được ghi ở đầu sổ theo dõi.
- **Quy tắc bất biến**: như mục 2.2 — ID không đổi, không dùng lại; khi tách mục, phần giữ ý chính giữ ID cũ; khi gộp, giữ một ID; khi bỏ mục, không cấp lại ID đó. Số mục vẫn được đánh lại khi cần.
- **Cách trích dẫn**:
  - Mục có ID: `D-ADM-019 (¶4.19)`, `D-SD03-001 (¶2.1)`. Không cần ghi tên file vì mã file đã nằm trong ID. Viết giống nhau dù trích từ file khác hay trong cùng file.
  - Khoảng mục: ghi ID cho cả hai đầu, `D-ADM-023 (¶4.23)–D-ADM-025 (¶4.25)`.
  - Mục không mang ID: `` `03` ¶6 ``, `admin-web ¶1`. Trong cùng file, chỉ ghi `¶6`.
  - Nếu cần trích từ file khác một mục chưa có ID: gắn ID cho mục đó trong cùng lần sửa. Nếu mục đó thuộc luồng khác thì ghi ⚠, chờ luồng sở hữu cấp ID.
  - Không dùng "mục N" để trích số mục của tài liệu thiết kế.
- **Cách gõ `¶`** (U+00B6): trên Windows dùng Alt+0182, tương tự Alt+0167 cho `§`.

### 2.5. operationId của endpoint API

- **Phạm vi**: mọi endpoint HTTP khai báo trong `system-design/`, gồm các nhóm route `admin`/`partner`/`public`, webhook nội bộ và endpoint của AI Gateway. Mỗi endpoint có đúng một operationId, ghi ở cột `operationId` (ngay sau cột Path) trong bảng endpoint của mục thiết kế chứa endpoint đó. Chỉ tài liệu system-design đặt operationId. Các luồng web chỉ trích dẫn; cần endpoint mới thì đề xuất sang system-design như các thay đổi thiết kế khác.
- **Định dạng**: `<tiền tố>.<tên>`, duy nhất trong toàn hệ thống.
  - Tiền tố là đoạn đầu của path sau nhóm route: `auth`, `identity`, `knowledge`, `encyclopedia`, `assistant`, `shared`, `public`. Đoạn có gạch ngang viết thành camelCase (`client-settings` → `clientSettings`). Webhook nội bộ dùng `internal`. Endpoint AI Gateway dùng `gateway`.
  - Tên viết camelCase tiếng Anh, dạng động từ + danh từ: `list…` (danh sách), `get…` (chi tiết), `create…`, `update…`, `delete…`. Endpoint hành động lấy động từ theo path, ví dụ `…/trigger-ai-verification` → `triggerAiVerification`.
  - Ví dụ: `auth.login`, `knowledge.getKnowledgeObject`, `knowledge.triggerAiVerification`, `shared.retryJob`, `public.getEntry`, `gateway.generate`.
- **Endpoint mount ở nhiều nhóm route** với cùng hành vi (ví dụ `auth/*` ở `admin` và `partner`) dùng chung một operationId.
- **Quy tắc bất biến**:
  - operationId không đổi khi đổi path, method hoặc mô tả.
  - Endpoint bị bỏ thì không dùng lại operationId của nó.
  - Khi đổi hành vi theo cách không tương thích với bên gọi, tạo endpoint mới với operationId mới và bỏ endpoint cũ.
  - Thêm endpoint thì đặt operationId trong cùng lượt ghi.
- **Cách trích dẫn**:
  - Dạng chuẩn: `` `knowledge.triggerAiVerification` ``, chỉ ghi operationId, không kèm ID mục thiết kế. operationId là duy nhất và chỉ khai báo ở một bảng endpoint, nên tìm theo tên là ra mục chứa endpoint.
  - Khi cần cho dễ đọc, thêm method + path sau dấu gạch ngang: `` `knowledge.triggerAiVerification` — `POST /knowledge/knowledge-objects/{id}/trigger-ai-verification` ``.
  - Không trích endpoint chỉ bằng method + path.
  - Cần dẫn tới mục thiết kế mô tả hành vi liên quan thì trích mục đó theo mục 2.4, ví dụ `` `auth.changePassword` (D-SD02-006 (¶3.4)) ``. Không ghi ID trần `(D-…)` ngay sau operationId.

## 3. Change Request (CR) và Design Change (DC)

- **CR**: mỗi lần ghi thay đổi vào `business-requirements.md` (một lượt preview được duyệt) tạo một CR, mã `CR-YYYYMMDD-NN`. Luồng requirements ghi CR vào sổ theo dõi ngay sau khi ghi đặc tả, cùng lúc với `requirements/changelog.md`. Mục changelog ghi kèm mã CR.
- **DC**: mỗi lần một luồng thiết kế ghi thay đổi vào file nguồn của mình mà không xuất phát từ một CR (ví dụ quyết định kỹ thuật ⚠, sửa sai sót thiết kế) tạo một DC, mã `DC-YYYYMMDD-NN`. Luồng đó ghi DC vào sổ theo dõi ngay sau khi ghi file nguồn, cùng lúc với changelog của luồng. Mục changelog ghi kèm mã DC. Sửa thuần câu chữ hoặc định dạng, không đổi nội dung cần hiện thực, thì không tạo DC.
- Việc gắn ID cho mục thiết kế, hoặc đổi trích dẫn sang dạng ở mục 2.4, không đổi nội dung cần hiện thực nhưng vẫn phải tạo DC, để team Code cập nhật tham chiếu trong kế hoạch.
- **Bộ đếm chung**: CR và DC dùng chung bộ đếm NN trong ngày (đánh từ 01). Mỗi cặp ngày + NN là duy nhất và xác định thứ tự các dòng trong sổ; tiền tố chỉ cho biết nguồn gốc thay đổi. Ví dụ: `CR-20261002-01`, `DC-20261002-02`, `CR-20261002-03`.
- Nội dung một dòng trong sổ: mã, ngày, tóm tắt, ID ảnh hưởng, và trạng thái xử lý ở từng luồng thiết kế kèm các mục đã sửa (mục 4). Trạng thái xử lý ở Code nằm ở file riêng (mục 4.1).
  - **CR**: cột "ID ảnh hưởng" liệt kê các ID kèm hành động (`thêm` / `sửa` / `bỏ` / `di chuyển`). Mọi cột luồng thiết kế mặc định ⏳.
  - **DC**: cột "ID ảnh hưởng" ghi `—`. Cột của luồng tạo DC ghi ✅ kèm các mục đã sửa ngay khi tạo. Cột của các luồng phía dưới luồng đó (mục 1) mặc định ⏳. Các cột còn lại ghi `—`.

## 4. Trạng thái xử lý ở từng luồng

| Ký hiệu | Nghĩa |
|---|---|
| ⏳ | Chưa xử lý |
| 🔄 | Đang xử lý |
| ✅ | Đã xử lý xong |
| — | Không ảnh hưởng luồng này (đã đối chiếu) |

- Ngoài lúc tạo dòng (mục 3), chỉ luồng tương ứng mới đổi trạng thái của cột mình, sau khi đã đối chiếu.
- Một luồng chỉ xử lý một dòng khi luồng ngay trên nó đã ✅ hoặc — (ví dụ admin-web chờ system-design).
- **Ghi mục đã sửa**: khi đổi cột của mình sang ✅, luồng ghi kèm các mục trong file nguồn đã sửa do dòng đó:
  - system-design ghi theo file, dạng `` ✅ `04`: 2.2, 3.1 · `05`: 3.1 ``.
  - Luồng web ghi số mục, dạng `✅ 4.19, 4.29`.
  - Mục mới thêm ghi `(mới)`, mục bị bỏ ghi `(bỏ)`. Mục bị đánh số lại ghi cả số cũ và số mới, dạng `3.3 → 3.4`, để team Code cập nhật tham chiếu trong kế hoạch.
- Khi luồng thiết kế sửa file nguồn do một CR hoặc DC, mục changelog của luồng đó ghi kèm mã CR/DC.
- **Mốc đồng bộ** của một luồng là mã (CR hoặc DC) mới nhất mà mọi dòng trước đó ở cột luồng đó đều là ✅ hoặc —. Mốc này ghi ở đầu sổ theo dõi.
- **Đóng dòng**: khi mọi cột luồng của một dòng là ✅ hoặc — **và** mã đó có trạng thái ✅ hoặc — trong `planning/cr-status.md` (mục 4.1), thì cập nhật mốc đồng bộ nếu cần rồi xoá dòng khỏi sổ. Commit git với message ghi mã (ví dụ `CR-20260928-01: đóng`, `DC-20261002-02: đóng`) để còn tra được trong git history.
  - Trước khi đóng, luôn tự đọc `planning/cr-status.md` trong repo `vanminhviet` và đối chiếu các commit ghi ở đó trong git log của repo — không đóng dòng chỉ dựa trên thông báo trạng thái từ bên ngoài.

### 4.1. Trạng thái xử lý ở Code

- Trạng thái xử lý CR/DC ở Code ghi trong `planning/cr-status.md` ở gốc repo `vanminhviet` (trên máy: `Z:\VanMinhSo\vanminhviet\planning\cr-status.md`). File này do team Code sở hữu: chỉ team Code ghi/sửa/xoá; các luồng thiết kế chỉ đọc, không bao giờ ghi vào.
- Định dạng — một bảng, mỗi mã (CR hoặc DC) một dòng:

| Mã | Trạng thái | Commit/PR | Ngày | Ghi chú |
|---|---|---|---|---|
| CR-20260928-01 | ✅ | `a1b2c3d` / #12 | 2026-10-02 | |

- Trạng thái dùng ký hiệu 🔄 / ✅ / — như mục 4. Mã chưa có dòng trong file được hiểu là ⏳.
- Code chỉ xử lý một CR/DC khi cột system-design và cột web liên quan trong sổ theo dõi đều là ✅ hoặc —.
- **Dọn dẹp**: sau mỗi lần đồng bộ sang Code, mã nào không còn trong sổ theo dõi (bản `docs/common/requirements-change-tracker.md` trong repo) là đã đóng — team Code xoá dòng đó khỏi `cr-status.md`, commit với message ghi mã. Không xoá dòng của mã còn trong sổ theo dõi.

## 5. Kiểm tra tham chiếu

- Script `common/tools/check-requirement-refs.py` (Python 3, không cần thư viện ngoài) đọc `requirements/business-requirements.md` và quét các file `.md` ở `system-design/`, `admin-web/`, `partner-web/`, `public-web/` (trừ `changelog.md`), báo:
  - ID được trích dẫn nhưng không còn trong đặc tả (mục đã bỏ hoặc gõ sai).
  - Số § đi kèm không khớp với số mục hiện tại của ID đó.
  - Trích dẫn `§` không kèm ID.
  - ID bị trùng trong đặc tả, hoặc bảng "ID lớn nhất đã cấp" trong sổ theo dõi thấp hơn ID thực có trong đặc tả.
  - ID thiết kế được trích nhưng không có trong file tương ứng, hoặc số `¶` đi kèm không khớp với số mục hiện tại.
  - ID thiết kế bị trùng, hoặc bảng "ID thiết kế lớn nhất đã cấp" thấp hơn ID thực có.
  - Trích dẫn `¶` tới một mục đang mang ID nhưng không ghi ID.
  - Trích số mục thiết kế theo dạng cũ: "`0X` mục N", "`0X-….md` mục N", "admin-web N"/"admin-web mục N" (và tương tự cho partner-web, public-web), hoặc "mục N" trong chính tài liệu thiết kế.
  - Bảng endpoint thiếu operationId, operationId bị trùng hoặc sai định dạng (mục 2.5).
  - operationId được trích nhưng không có trong bảng endpoint nào, hoặc có ID mục trần `(D-…)` ghi ngay sau operationId (mục 2.5).
  - Trích endpoint chỉ bằng method + path, không kèm operationId (mục 2.5). Path viết tắt (`…/x`) chỉ bị báo khi khớp đúng một endpoint; khớp nhiều endpoint được coi là mô tả mẫu chung.
  - Trích đặc tả bằng "mục X.Y" (không có `§`, không có ID) khi đứng cạnh "đặc tả", "BR", `business-requirements`.
- Cách chạy: `python common/tools/check-requirement-refs.py` (chạy được từ bất kỳ thư mục nào); thêm `--luong <tên luồng>` để chỉ báo lỗi trong file của một luồng. Mỗi lỗi in kèm `file:dòng`; mã thoát 0 = không có lỗi, 1 = có lỗi.
- Chạy: sau mỗi CR/DC, và bắt buộc trước khi chạy "Đồng bộ sang Code".

## 6. Changelog và Git

- Sổ theo dõi (`requirements-change-tracker.md`) chỉ giữ các dòng CR/DC đang mở. Dòng đã đóng tra lại qua changelog của từng luồng và `git log --grep <mã>`. Vì vậy mọi commit liên quan tới một CR/DC đều ghi mã đó trong message.

## 7. Dành cho team Code

- Sổ theo dõi trong repo (`docs/common/requirements-change-tracker.md`) là bản chỉ đọc, bị ghi đè mỗi lần đồng bộ — không sửa file này.
- CR/DC đã xong ở thiết kế (✅ hoặc — ở cột system-design và web liên quan) mà chưa có ✅ hoặc — trong `planning/cr-status.md` là phần cần cập nhật code. Ghi trạng thái và dọn dẹp theo mục 4.1.
- Khi lập kế hoạch (milestone, sprint, task), trích tài liệu thiết kế bằng ID kèm `¶` (`D-SD04-012 (¶2.2)`, `D-ADM-019 (¶4.19)`), kèm R-ID liên quan nếu có. Ô trạng thái của các luồng trong sổ theo dõi cho biết mỗi CR/DC đã sửa mục thiết kế nào, kể cả mục bị đánh số lại. Dùng thông tin này để xác định task nào cần cập nhật.
- Trong code/test (comment, tên/mô tả test), chỉ ghi ID (`R-KB-014`, `D-SD03-001`), không kèm `§`/`¶`, vì code nằm ngoài phạm vi kiểm tra của mục 5 nên số mục đi kèm sẽ không được cập nhật.
- Hợp đồng OpenAPI dùng đúng operationId của thiết kế (mục 2.5, D-SD01-003 (¶3)). Trong kế hoạch, code và test, trích endpoint chỉ bằng operationId (`knowledge.triggerAiVerification`), không kèm ID mục thiết kế.
- Nếu `requirements/`, `system-design/` mâu thuẫn với code, tài liệu thiết kế luôn thắng.
