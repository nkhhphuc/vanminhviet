# Đặc Tả — Phần Mềm Văn Minh Việt

## 1. Tổng Quan

### 1.1. Dữ liệu đầu vào

- **1.1.1.** Tư Liệu Hán Nôm. Đây là kho tự liệu bằng ngôn ngữ Hán Nôm đã kiểm duyệt thông qua hệ thống OCR.
- **1.1.2.** Tư liệu của các đề tài nghiên cứu. Hiện có 210 đề tài nghiên cứu, trong tương lai sẽ có thêm nhiều đề tài nghiên cứu khác.

### 1.2. Đối tượng sử dụng

Chia làm 2 nhóm theo kênh truy cập:

- **1.2.1. Nhân viên** (truy cập hệ thống backend): gồm nhân viên vận hành hệ thống, nhân viên/chuyên gia của các viện nghiên cứu, chuyên gia xét duyệt, quản trị viên. Đây là một loại người dùng duy nhất, phân biệt nhau bằng **role** (vd: admin, vận hành, nghiên cứu, xét duyệt...).
- **1.2.2. Người dùng công khai** (truy cập frontend – website và ứng dụng di động): gồm công dân Việt Nam và các tổ chức do nhà nước quản lý. Đây là một loại người dùng duy nhất; ở giai đoạn hiện tại truy cập hoàn toàn ẩn danh, không có tài khoản/định danh nào, chỉ sử dụng các tính năng xem/tra cứu Bách Khoa Toàn Thư và trò chuyện với AI Văn Minh Việt (mục 2.6). Mô tả "đầy đủ quyền tương tác" ở mục 2.1.3.2 là định hướng đón đầu cho các module tương tác/tạo nội dung phát sinh sau này (ngoài phạm vi giai đoạn này, ví dụ Cộng Đồng Văn Hóa — mục 2.5.3), không áp dụng ngay ở giai đoạn hiện tại.
- **1.2.3. Giao diện truy cập theo Tổ chức** (áp dụng cho Nhân viên — mục 1.2.1): giao diện backend mà một Nhân viên sử dụng được xác định theo Tổ chức mà Nhân viên đó trực thuộc (xem mục 2.1.4):
  - **1.2.3.1.** Nhân viên thuộc Tổ chức Văn Minh Việt: dùng giao diện quản trị nội bộ đầy đủ như hiện tại, bao gồm quản lý người dùng/phân quyền — giới hạn theo vai trò Quản trị hệ thống (mục 2.1.3.1.1).
  - **1.2.3.2.** Nhân viên thuộc Tổ chức khác (viện nghiên cứu ngoài): dùng giao diện riêng phục vụ quản lý công việc nghiên cứu trong phạm vi được cấp — thực hiện vai trò Chủ nhiệm đề tài/Nghiên cứu/Xét duyệt (mục 2.2.5) theo đúng Đề tài nghiên cứu được gán (mục 2.1.3.1.2, 2.2.1.4). Giao diện này không có chức năng quản lý người dùng/phân quyền, không tạo/sửa Tổ chức, dù nhân viên đó giữ vai trò gì. Chi tiết ứng dụng này ở mục 2.7.
  - **1.2.3.3.** Quản lý tài khoản Nhân viên, phân quyền (bao gồm gán vai trò Nghiên cứu/Xét duyệt theo từng Đề tài — xem mục 2.2.1.4), và tạo/gán Tổ chức chỉ thực hiện được từ giao diện quản trị nội bộ (1.2.3.1), bởi Nhân viên giữ vai trò Quản trị hệ thống.

### 1.3. Hệ thống gồm các modules chính

- **1.3.1.** Quản lý người dùng.
- **1.3.2.** Cơ sở dữ liệu văn hóa - Dây chuyền chuyển hóa tri thức.
- **1.3.3.** Bách khoa toàn thư - Nền tảng dữ liệu dành cho cộng đồng.
- **1.3.4.** AI Văn Minh Việt.

**Ghi chú:** Văn minh đình làng việt, Văn minh gia lễ việt, Văn minh quân sự việt, Văn minh trống đồng **không phải là module riêng**, mà là các giá trị phân loại (cương vực/taxonomy) dùng chung trong Bách Khoa Toàn Thư và AI Văn Minh Việt.

Các module sau đã được đề cập nhưng **tạm để ngoài phạm vi đặc tả giai đoạn này**, sẽ làm rõ và đặc tả sau: Lịch & Sự Kiện, Trò Chơi Lịch Sử, Phim Lịch Sử, Cộng Đồng Văn Hóa, Hộ Chiếu Văn Hóa, Bảo tàng số 3D, Bản đồ văn hóa, Giáo dục (xem mục 2.5).

## 2. Modules

### 2.1. Quản Lý Người Dùng

- **2.1.1.** Nhân viên được định danh bằng một ID duy nhất do hệ thống tự sinh. Người dùng công khai không có tài khoản/định danh nào ở giai đoạn này — xem mục 2.1.3.2.
- **2.1.2.** Mỗi Nhân viên có các thông tin chính: 01 email, 01 số điện thoại và 01 tên gọi.
- **2.1.3.** Hai loại người dùng, phân theo kênh truy cập:
  - **2.1.3.1. Nhân viên**: là người dùng truy cập hệ thống backend, gồm quản trị viên, nhân viên vận hành hệ thống, nhân viên/chuyên gia các viện nghiên cứu. Mỗi Nhân viên thuộc về đúng một Tổ chức (xem mục 2.1.4). Được cấp một hoặc nhiều **role** để phân quyền theo từng nghiệp vụ — một Nhân viên có thể giữ nhiều role cùng lúc. Danh sách role dưới đây **chưa đầy đủ**, có thể bổ sung khi thiết kế chi tiết từng module. Có 2 loại role:
    - **2.1.3.1.1. Role theo chức năng** (phân loại theo chức năng/nghiệp vụ được phép thực hiện, không gắn với một phạm vi dữ liệu cụ thể — khác với Role theo phạm vi ở mục 2.1.3.1.2): ví dụ Nhập liệu, Xuất bản, Biên tập, Xét duyệt Mục từ, Vận hành, Quản trị hệ thống, v.v.
    - **2.1.3.1.2. Role theo phạm vi** (giới hạn quyền theo một phạm vi dữ liệu cụ thể, khác với Role theo chức năng ở mục 2.1.3.1.1): ví dụ theo Đề tài nghiên cứu (vai trò Chủ nhiệm đề tài, vai trò Nghiên cứu, vai trò Xét duyệt — chi tiết ở mục 2.2.5), theo Cương vực, v.v. Vai trò cụ thể theo từng phạm vi sẽ được đặc tả chi tiết ở module liên quan. Một Nhân viên có thể được gán nhiều role theo phạm vi khác nhau cùng lúc (ví dụ role của nhiều đề tài nghiên cứu khác nhau).

    Mô hình phân quyền chi tiết theo từng hành động/module (permission matrix) sẽ được xác định khi thiết kế chi tiết từng module.
  - **2.1.3.2. Người dùng**: là người dùng truy cập frontend (website, ứng dụng di động), gồm công dân Việt Nam và các tổ chức do nhà nước quản lý. Là một loại người dùng duy nhất; ở giai đoạn hiện tại truy cập hoàn toàn ẩn danh, chưa triển khai cơ chế tài khoản nào — chỉ sử dụng các tính năng xem/tra cứu và trò chuyện AI đã đặc tả ở mục 2.6 (nhất quán với mục 2.6.1). Câu "đầy đủ quyền tương tác (tạo/sửa/xoá, tương tác thay đổi dữ liệu)" là định hướng cho các module tương tác/tạo nội dung phát sinh sau này (ngoài phạm vi giai đoạn này, ví dụ Cộng Đồng Văn Hóa — mục 2.5.3); khi đặc tả các module đó sẽ làm rõ quyền cụ thể, kể cả khi đó có cần cơ chế tài khoản hay không.
- **2.1.4. Tổ chức (organization)**: entity quản lý các tổ chức mà Nhân viên trực thuộc. Gồm:
  - **2.1.4.1.** Định danh.
  - **2.1.4.2.** Tên tổ chức.
  - **2.1.4.3.** Địa chỉ.
  - **2.1.4.4.** Thông tin liên hệ: email, số điện thoại.
  - **2.1.4.5.** Mỗi Nhân viên (mục 2.1.3.1) thuộc về đúng một Tổ chức — bao gồm cả nhân viên nội bộ Văn Minh Việt (Văn Minh Việt là một Tổ chức bình thường trong mô hình này, không phải trường hợp đặc biệt) lẫn nhân viên các viện nghiên cứu khác.
  - **2.1.4.6.** Mục đích bổ sung entity này từ giai đoạn hiện tại: dự kiến cần tính chi phí sử dụng hệ thống theo từng Tổ chức trong tương lai — logic tính chi phí cụ thể (cách tính, đơn giá, xuất hoá đơn...) sẽ đặc tả sau, nhưng cần có sẵn Tổ chức để gắn dữ liệu sử dụng ngay từ đầu.
- **2.1.5. Xác thực Nhân viên**: cơ chế đăng nhập cho Nhân viên (mục 2.1.3.1).
  - **2.1.5.1.** Nhân viên đăng nhập bằng email (mục 2.1.2) và mật khẩu.
  - **2.1.5.2.** Nhân viên không tự đăng ký tài khoản — tài khoản chỉ được tạo bởi Nhân viên giữ vai trò Quản trị hệ thống (mục 2.1.3.1.1), từ giao diện quản trị nội bộ, nhất quán với quy định ở mục 1.2.3.3.
    - **2.1.5.2.1.** Ngoại lệ duy nhất: tài khoản Quản trị hệ thống **đầu tiên** của hệ thống (khi chưa có Nhân viên nào) được tạo trong quá trình triển khai hệ thống, thuộc Tổ chức Văn Minh Việt (mục 2.1.4.5), và dùng được ngay mà không qua email mời. Mọi tài khoản sau đó được tạo theo mục 2.1.5.2–2.1.5.3.
  - **2.1.5.3.** Khi tài khoản được tạo, hệ thống gửi một email mời tới địa chỉ email của Nhân viên, chứa đường dẫn để tự đặt mật khẩu lần đầu; tài khoản chỉ kích hoạt (dùng được) sau khi Nhân viên hoàn tất bước này.
  - **2.1.5.4.** Quên mật khẩu: Nhân viên tự yêu cầu đặt lại mật khẩu, nhận email chứa đường dẫn đặt lại — theo cùng cơ chế với mục 2.1.5.3.
  - **2.1.5.5.** Đường dẫn mời (2.1.5.3) và đường dẫn đặt lại mật khẩu (2.1.5.4) có thời hạn sử dụng và chỉ dùng được một lần; thời hạn do Quản trị hệ thống cấu hình (mục 2.8.4.2); giá trị mặc định do thiết kế kỹ thuật quyết định.
  - **2.1.5.6.** Không dùng cơ chế đăng nhập ngoài (SSO/OAuth của bên thứ ba) ở giai đoạn này — áp dụng cho mọi Nhân viên, kể cả Nhân viên thuộc Tổ chức khác (viện nghiên cứu ngoài, mục 2.7) — do chưa có yêu cầu tích hợp cụ thể và để tránh phụ thuộc ngoài không cần thiết.
  - **2.1.5.7. Vô hiệu hoá tài khoản**: Nhân viên giữ vai trò Quản trị hệ thống (mục 2.1.3.1.1) có thể **vô hiệu hoá** tài khoản của một Nhân viên (ví dụ khi Nhân viên nghỉ việc hoặc tạm ngừng tham gia), và **kích hoạt lại** tài khoản đã vô hiệu hoá khi cần. Thao tác thực hiện từ giao diện quản trị nội bộ (mục 1.2.3.3).
    - **2.1.5.7.1.** Khi bị vô hiệu hoá, mọi phiên đăng nhập đang mở của Nhân viên đó **bị đăng xuất ngay**. Nhân viên bị vô hiệu hoá không đăng nhập được; hệ thống thông báo tài khoản đã bị khoá và hướng dẫn liên hệ Quản trị hệ thống.
    - **2.1.5.7.2.** Vô hiệu hoá **không xoá** tài khoản, **không gỡ** các role đang giữ (mục 2.1.3.1), và không ảnh hưởng dữ liệu hay lịch sử do Nhân viên đó tạo ra. Kích hoạt lại thì Nhân viên dùng lại đúng tài khoản, mật khẩu và các role cũ.
    - **2.1.5.7.3.** Hạng mục tri thức hoặc Mục từ mà Nhân viên bị vô hiệu hoá đang phụ trách **không tự động được nhả**. Quản trị hệ thống dùng cơ chế cưỡng chế nhả (mục 2.2.3.11.5, 2.3.2.5.5) khi cần.
    - **2.1.5.7.4.** Ở giai đoạn này **không có chức năng xoá** tài khoản Nhân viên hay xoá Tổ chức (mục 2.1.4), và Tổ chức không có trạng thái ngừng hoạt động. Để ngừng quyền truy cập của Nhân viên một Tổ chức, Quản trị hệ thống vô hiệu hoá từng Nhân viên.
  - **2.1.5.8. Chính sách mật khẩu**: mật khẩu Nhân viên đặt lần đầu (mục 2.1.5.3), đặt lại (mục 2.1.5.4) hoặc đổi (mục 2.1.5.10) phải đáp ứng chính sách mật khẩu hiện hành: độ dài tối thiểu, có cả chữ và số, và có ký tự đặc biệt hay không. Chính sách do Quản trị hệ thống cấu hình (mục 2.8.4.2); giá trị mặc định do thiết kế kỹ thuật quyết định. Màn hình đặt mật khẩu hiển thị các yêu cầu này. Thay đổi chính sách chỉ áp dụng cho các lần đặt mật khẩu sau đó, không buộc Nhân viên đổi mật khẩu đang dùng.
  - **2.1.5.9. Tạm khoá đăng nhập**: nếu nhập sai mật khẩu liên tiếp, khi đăng nhập hoặc khi đổi mật khẩu (mục 2.1.5.10), đến số lần giới hạn, tài khoản bị **tạm khoá đăng nhập** trong một khoảng thời gian. Số lần và thời gian khoá do Quản trị hệ thống cấu hình (mục 2.8.4.2), và có thể tắt cơ chế này.
    - **2.1.5.9.1.** Trong thời gian tạm khoá, Nhân viên không đăng nhập được, kể cả khi nhập đúng mật khẩu. Hệ thống báo tài khoản đang tạm khoá và thời điểm được thử lại.
    - **2.1.5.9.2.** Tạm khoá tự hết khi hết thời gian. Tạm khoá cũng được gỡ khi Nhân viên đặt lại mật khẩu thành công (mục 2.1.5.4), hoặc khi Quản trị hệ thống chủ động **gỡ tạm khoá** trước thời hạn.
    - **2.1.5.9.3.** Tạm khoá đăng nhập khác với vô hiệu hoá tài khoản (mục 2.1.5.7): tạm khoá do hệ thống tự áp dụng và tự hết hạn; vô hiệu hoá do Quản trị hệ thống thực hiện và chỉ hết khi được kích hoạt lại.
    - **2.1.5.9.4.** Sau khi Nhân viên đặt lại mật khẩu thành công, mọi phiên đăng nhập đang mở của Nhân viên đó bị đăng xuất.
  - **2.1.5.10. Đổi mật khẩu**: Nhân viên đang đăng nhập được tự đổi mật khẩu của chính mình, ở cả giao diện quản trị nội bộ (mục 1.2.3.1) lẫn giao diện cho Nhân viên Tổ chức khác (mục 2.7). Không ai đổi được mật khẩu thay cho Nhân viên khác, kể cả Quản trị hệ thống.
    - **2.1.5.10.1.** Nhân viên phải nhập đúng **mật khẩu hiện tại**. Nhập sai được tính chung vào số lần sai của tạm khoá đăng nhập (mục 2.1.5.9). Nếu đạt ngưỡng, tài khoản bị tạm khoá và mọi phiên đăng nhập bị đăng xuất.
    - **2.1.5.10.2.** Mật khẩu mới phải đáp ứng chính sách mật khẩu (mục 2.1.5.8) và **không được trùng** mật khẩu hiện tại. Hệ thống không kiểm tra trùng với các mật khẩu cũ hơn.
    - **2.1.5.10.3.** Đổi thành công thì mọi phiên đăng nhập của Nhân viên, kể cả phiên đang dùng, bị đăng xuất; Nhân viên đăng nhập lại bằng mật khẩu mới.
    - **2.1.5.10.4.** Hệ thống không gửi email thông báo sau khi đổi mật khẩu.

### 2.2. Cơ Sở Dữ Liệu Văn Hóa

Cơ sở dữ liệu văn hóa là nền tảng lưu trữ và quản lý tri thức văn hóa. Định hướng tổng thể (không phải một quy trình xử lý cứng, tuần tự bắt buộc theo đúng nghĩa đen) của giá trị mà cơ sở dữ liệu này tạo ra là:
`Tư liệu Hán Nôm → Nghiên cứu → Dữ liệu chuẩn → Bách khoa → Trợ lý số → Sản phẩm → Đời sống`
— tức là từ tư liệu gốc, qua nghiên cứu, tạo ra dữ liệu tri thức chuẩn hóa, từ đó phục vụ Bách Khoa Toàn Thư, các trợ lý số (AI), các sản phẩm ứng dụng, và cuối cùng đi vào đời sống cộng đồng. Quy trình nghiệp vụ cụ thể (trạng thái, các bước xét duyệt...) được đặc tả riêng ở mục 2.2.6.

Cấu trúc phân cấp tổ chức: Đề tài nghiên cứu (2.2.1) → sử dụng nhiều Tư liệu gốc (2.2.2) và tạo ra nhiều Hạng mục tri thức (2.2.3) → mỗi Hạng mục tri thức có Phát biểu, mỗi Phát biểu có Tham chiếu (2.2.4) trỏ về một file cụ thể của Tư liệu gốc.

#### 2.2.1. Đề tài nghiên cứu (research_topic)

Là đơn vị tổ chức nghiên cứu (hiện có 210 đề tài, xem mục 1.1.2). Mỗi đề tài nghiên cứu cần có:

- **2.2.1.1.** Định danh.
- **2.2.1.2.** Tên đề tài.
- **2.2.1.3.** Danh sách Tư liệu gốc được sử dụng — quan hệ **nhiều – nhiều** với Tư liệu gốc (mục 2.2.2): một đề tài sử dụng nhiều tư liệu gốc, một tư liệu gốc cũng có thể được nhiều đề tài cùng sử dụng. Việc nhập Tư liệu gốc vào hệ thống và gán Tư liệu gốc cho đề tài do **vai trò Nhập liệu** thực hiện (mục 2.2.5.1), theo trạng thái của đề tài ở mục 2.2.1.6.
- **2.2.1.4.** Đề tài nghiên cứu chỉ do Nhân viên giữ vai trò Quản trị hệ thống tạo mới (mục 2.1.3.1.1). Khi Đề tài nghiên cứu được tạo, hệ thống tự động tạo **vai trò Chủ nhiệm đề tài**, **vai trò Nghiên cứu** và **vai trò Xét duyệt** theo phạm vi của đề tài đó (xem mục 2.1.3.1.2 và chi tiết vai trò ở mục 2.2.5).
  - Chỉ Quản trị hệ thống mới gán hoặc thay đổi Nhân viên giữ vai trò Chủ nhiệm đề tài (mục 2.2.5.5) — không phân biệt thuộc Tổ chức nào; mỗi đề tài có đúng một Chủ nhiệm đề tài tại một thời điểm.
  - Việc gán Nhân viên (không phân biệt thuộc Tổ chức nào — một Đề tài có thể có Nhân viên từ nhiều Tổ chức khác nhau cùng tham gia) vào vai trò Nghiên cứu và vai trò Xét duyệt của đề tài, để có quyền truy cập Tư liệu gốc (2.2.1.3) và quyền xét duyệt các Hạng mục tri thức (2.2.6) thuộc đề tài, do Quản trị hệ thống **hoặc** Chủ nhiệm đề tài (mục 2.2.5.5) của chính đề tài đó thực hiện; có thể gán nhiều Nhân viên vào cùng một role, và một Nhân viên có thể giữ role của nhiều đề tài khác nhau.
- **2.2.1.5.** Nhân viên giữ vai trò Quản trị hệ thống (mục 2.1.3.1.1) có quyền **xem** (không cần thực hiện) tiến độ, nội dung Hạng mục tri thức, và kết quả xét duyệt của **mọi** Đề tài nghiên cứu — không phân biệt có được gán vai trò Nghiên cứu/Xét duyệt (mục 2.2.1.4) của đề tài đó hay không. Quản trị hệ thống không có quyền thực hiện Nghiên cứu (2.2.6.3–2.2.6.4) hay Xét duyệt (2.2.6.8–2.2.6.10) trừ khi được gán thêm vai trò tương ứng.
  - **2.2.1.5.1.** Cơ chế gỡ nghẽn vai trò Xuất bản: vai trò Xuất bản (mục 2.2.5.4) là role theo chức năng, không tự sinh theo Đề tài như vai trò Nghiên cứu/Xét duyệt (mục 2.2.1.4). Nếu không còn Nhân viên nào giữ vai trò Xuất bản (ví dụ do nghỉ việc, bị thu hồi quyền...), khiến các Hạng mục tri thức đang ở "Đạt xét duyệt" (mục 2.2.6.10) không thể được xử lý tiếp, Quản trị hệ thống có thể tự gán vai trò Xuất bản cho chính mình hoặc cho Nhân viên khác, dùng đúng cơ chế gán role sẵn có (mục 2.1.3.1.1) — không cần một quy trình/route đặc biệt riêng cho việc gỡ nghẽn này.
- **2.2.1.6. Trạng thái**: Đề tài nghiên cứu có trạng thái riêng, phản ánh tiến độ chuẩn bị tư liệu cho đề tài — tách biệt với trạng thái của từng Hạng mục tri thức (mục 2.2.3.3, 2.2.6). Luồng trạng thái:

  ```
  Chuẩn bị tư liệu → Tư liệu sẵn sàng
  ```

  - **2.2.1.6.1. Chuẩn bị tư liệu**: Đề tài nghiên cứu được khởi tạo ở trạng thái này khi Quản trị hệ thống tạo đề tài (mục 2.2.1.4). **Vai trò Nhập liệu** (mục 2.2.5.1) nhập Tư liệu gốc vào hệ thống và gán vào danh sách Tư liệu gốc của đề tài (mục 2.2.1.3). Việc chuẩn bị tư liệu có thể kéo dài và thực hiện nhiều lần.
  - **2.2.1.6.2. Tư liệu sẵn sàng**: Vai trò Nhập liệu tự bật cờ sẵn sàng khi hoàn tất, bàn giao cho vai trò Nghiên cứu. Cờ này **mở khoá** việc tạo Hạng mục tri thức cho đề tài (mục 2.2.3.10) — khi đề tài còn ở "Chuẩn bị tư liệu", vai trò Nghiên cứu **không tạo được** Hạng mục tri thức nào. Sau khi đã bật cờ, vẫn **tiếp tục bổ sung Tư liệu gốc cho đề tài bất kỳ lúc nào**, không làm đề tài quay lại "Chuẩn bị tư liệu" và không chặn việc nghiên cứu đang diễn ra.
- **2.2.1.7. Xoá Đề tài nghiên cứu**: Nhân viên giữ vai trò Quản trị hệ thống (mục 2.1.3.1.1) xoá được Đề tài nghiên cứu khi đề tài đang **rỗng** — chưa có Hạng mục tri thức nào được tạo (mục 2.2.3.10), hoặc các Hạng mục tri thức đã bị xoá hết (mục 2.2.3.14). Nếu đề tài còn ít nhất một Hạng mục tri thức, hệ thống **chặn** thao tác xoá.
  - **2.2.1.7.1.** Xoá được ở cả hai trạng thái của đề tài (mục 2.2.1.6) — "Chuẩn bị tư liệu" và "Tư liệu sẵn sàng".
  - **2.2.1.7.2.** Việc xoá đề tài **gỡ luôn các vai trò theo phạm vi** của đề tài đó (vai trò Chủ nhiệm đề tài — mục 2.2.5.5, vai trò Nghiên cứu — mục 2.2.5.2, vai trò Xét duyệt — mục 2.2.5.3), bao gồm cả việc gỡ các Nhân viên đang được gán vào các vai trò này. Vai trò theo phạm vi của các đề tài khác, và các role theo chức năng (mục 2.1.3.1.1) của cùng Nhân viên, không bị ảnh hưởng.
  - **2.2.1.7.3.** Tư liệu gốc (mục 2.2.2) đã gán cho đề tài **không bị xoá** — chỉ gỡ khỏi danh sách Tư liệu gốc của đề tài (mục 2.2.1.3). Tư liệu gốc vẫn còn trong hệ thống và vẫn thuộc các đề tài khác đang sử dụng nó, nếu có.
  - **2.2.1.7.4.** Hệ thống **cảnh báo rõ** trước khi xoá, chỉ thực hiện khi Quản trị hệ thống xác nhận. Cách lưu trữ bản ghi sau khi xoá (xoá vĩnh viễn hay đánh dấu đã xoá để truy vết) để thiết kế kỹ thuật quyết định; dù theo cách nào, đề tài đã xoá không còn xuất hiện ở bất kỳ danh sách/giao diện nghiệp vụ nào.

Quan hệ với Hạng mục tri thức (mục 2.2.3): **một – nhiều** — mỗi Đề tài nghiên cứu tạo ra nhiều Hạng mục tri thức, mỗi Hạng mục tri thức thuộc về đúng một Đề tài nghiên cứu.

#### 2.2.2. Tư liệu gốc (source)

Gồm các trường:

- **2.2.2.1.** Định danh.
- **2.2.2.2.** Tên/tiêu đề tư liệu.
- **2.2.2.3.** Loại tư liệu: mộc bản Hán Nôm, sách, hiện vật, điền dã, phỏng vấn nghệ nhân…
- **2.2.2.4.** Một Tư liệu gốc gồm **nhiều file**, các file **không cần thứ tự**, và có thể gồm **nhiều loại file khác nhau** (văn bản, hình ảnh, âm thanh, phim) trong cùng một Tư liệu gốc. Mỗi file cần có:
  - **2.2.2.4.1.** Định danh file.
  - **2.2.2.4.2.** Loại file: văn bản / hình ảnh / âm thanh / phim *(có thể xác định trực tiếp hoặc suy ra từ định dạng/phần mở rộng file — chi tiết triển khai để thiết kế kỹ thuật quyết định)*.
  - **2.2.2.4.3.** Nội dung file.

#### 2.2.3. Hạng mục tri thức (knowledge_object)

Mỗi hạng mục tri thức cần có:

- **2.2.3.1.** Định danh.
- **2.2.3.2.** Tiêu đề.
- **2.2.3.3.** Trạng thái.
- **2.2.3.4.** Phiên bản: mỗi Hạng mục tri thức có thể có nhiều phiên bản theo thời gian. Phiên bản **do vai trò Xuất bản tạo** (mục 2.2.5.4) khi thực hiện quyết định xuất bản trên một Hạng mục tri thức đang ở trạng thái **"Đạt xét duyệt"** (mục 2.2.6.10) — hệ thống **không tự động** tạo phiên bản khi chuyển trạng thái. Phiên bản chốt lại nội dung tại thời điểm tạo và **bất biến** sau đó.
  - Khi hạng mục ở "Đạt xét duyệt", vai trò Xuất bản chọn **một trong hai**: **"Xuất bản"** — tạo phiên bản và chuyển hạng mục sang "Đã xuất bản" (mục 2.2.6.11); hoặc **"Không xuất bản"** — không tạo phiên bản và chuyển hạng mục sang "Không xuất bản" (mục 2.2.6.12).
  - Vì vậy mỗi vòng xét duyệt thành công tạo ra **tối đa 1 phiên bản**, tuỳ quyết định của vai trò Xuất bản.
  - Khi chọn "Không xuất bản", vòng xét duyệt đó **không để lại bản chốt nào** — nội dung đã qua xét duyệt sẽ bị ghi đè nếu hạng mục được mở lại để sửa tiếp. Hệ thống **không chặn** nhưng phải **cảnh báo rõ**, chỉ tiếp tục khi vai trò Xuất bản xác nhận.
  - Bị "Không đạt xét duyệt" (bởi AI — mục 2.2.6.6, hoặc bởi chuyên gia) và quay lại "Đang nghiên cứu" để sửa tiếp không tạo phiên bản — các chỉnh sửa đó vẫn thuộc bản đang soạn thảo.
  - Các phiên bản đã tạo được **giữ lại đầy đủ, không ghi đè**, phục vụ truy vết lịch sử.
  - **2.2.3.4.1.** Phiên bản đang được sử dụng: ghi nhận phiên bản nào (trong số các phiên bản đã tạo ở mục 2.2.3.4) hiện đang được chọn để đưa vào sử dụng cho Bách Khoa Toàn Thư (mục 2.3) và AI Văn Minh Việt (mục 2.4). Do **vai trò Xuất bản** chọn, và có thể đổi sang phiên bản khác bất kỳ lúc nào (mục 2.2.5.4) — không bắt buộc là phiên bản mới nhất, có thể chọn lại một phiên bản cũ hơn. **Tạo phiên bản (mục 2.2.3.4) và chọn phiên bản đang được sử dụng là hai thao tác tách rời**: tạo một phiên bản mới không tự động đưa phiên bản đó vào sử dụng. Mặc định chưa có phiên bản nào được chọn cho tới lần chọn đầu tiên của vai trò Xuất bản. Đây **không phải một trạng thái** của Hạng mục tri thức (xem mục 2.2.6) — việc nghiên cứu/xét duyệt tiếp tục (kể cả khi hạng mục được mở lại để làm tiếp sau khi đã xuất bản) diễn ra độc lập, không bị chặn bởi và không ảnh hưởng tới phiên bản đang được chọn để sử dụng, cho tới khi vai trò Xuất bản chủ động chọn phiên bản khác.
- **2.2.3.5.** Ngày giờ tạo phiên bản này.
- **2.2.3.6.** Nội dung: một Hạng mục tri thức gồm **nhiều file**, các file **không cần thứ tự**, và có thể gồm **nhiều loại file khác nhau** (văn bản, hình ảnh, âm thanh, phim) — cấu trúc giống Tư liệu gốc (2.2.2.4). Nội dung này là **sản phẩm biên tập của vai trò Nghiên cứu** (mục 2.2.6.3), **không phải tư liệu thô đầu vào** — Tư liệu gốc (mục 2.2.2) được quản lý ở cấp Đề tài nghiên cứu (mục 2.2.1.3). Mỗi file cần có:
  - **2.2.3.6.1.** Định danh file.
  - **2.2.3.6.2.** Loại file: văn bản / hình ảnh / âm thanh / phim *(có thể xác định trực tiếp hoặc suy ra từ định dạng/phần mở rộng file — chi tiết triển khai để thiết kế kỹ thuật quyết định)*.
  - **2.2.3.6.3.** Nội dung file.
- **2.2.3.7.** Các phát biểu (claims): là các tên gọi, thuật ngữ, định nghĩa, v.v. dùng trong Hạng mục tri thức mà các nhà nghiên cứu đã biên tập ra từ việc nghiên cứu các Tư liệu gốc. Mỗi phát biểu có thể khai báo thêm:
  - **2.2.3.7.1.** Vị trí trong Nội dung (mục 2.2.3.6, không bắt buộc) — khác với Tham chiếu ở mục 2.2.3.8 (trỏ ra Tư liệu gốc để làm chứng): định danh file cụ thể trong Nội dung của Hạng mục tri thức chứa phát biểu này, và vị trí trong file đó — dùng chung cấu trúc vị trí đã định nghĩa ở mục 2.2.4.2 (trang/dòng với văn bản, khung ảnh với hình ảnh, khoảng thời gian với âm thanh/phim). Mục đích: nếu có khai báo, khi xét duyệt (mục 2.2.6.6, 2.2.6.8), chuyên gia/AI biết chính xác phát biểu này xuất hiện ở đâu trong nội dung đã biên tập.
- **2.2.3.8.** Các tham chiếu (claim-mappings) đến tư liệu gốc.
- **2.2.3.9.** Đề tài nghiên cứu liên quan (Đề tài nghiên cứu cha, mục 2.2.1) — mỗi Hạng mục tri thức thuộc về đúng một Đề tài nghiên cứu.
- **2.2.3.10.** Hạng mục tri thức do **vai trò Nghiên cứu** của đề tài tạo (mục 2.2.5.2) trong quá trình nghiên cứu, bao gồm việc đặt Tiêu đề (mục 2.2.3.2) — Hạng mục tri thức là **đầu ra** của nghiên cứu, số lượng và tên gọi chỉ xác định được sau khi đã đọc tư liệu, nên không được tạo sẵn từ trước. **Chỉ tạo được khi Đề tài nghiên cứu cha đang ở trạng thái "Tư liệu sẵn sàng"** (mục 2.2.1.6.2). Hạng mục tri thức khởi tạo ở trạng thái "Đang nghiên cứu" (mục 2.2.6.3).
- **2.2.3.11. Người phụ trách**: ghi nhận đúng một Nhân viên đang chịu trách nhiệm chính tại thời điểm hiện tại, xuyên suốt vòng đời Hạng mục tri thức (mọi trạng thái ở mục 2.2.6). Cơ chế **"nhận xử lý"/"nhả"** tường minh, khoá độc quyền — tại một thời điểm chỉ có đúng một người phụ trách; người khác (kể cả cùng vai trò) không nhận được cho tới khi được nhả ra.
  - **2.2.3.11.1.** Khi Hạng mục tri thức được tạo (mục 2.2.3.10), người tạo tự động trở thành người phụ trách đầu tiên — không cần thao tác "nhận xử lý" riêng.
  - **2.2.3.11.2.** Trong "Đang nghiên cứu" (mục 2.2.6.3): chỉ Người phụ trách hiện tại được sửa Nội dung (2.2.3.6), Phát biểu (2.2.3.7), Tham chiếu (2.2.3.8). Một Nhân viên khác giữ vai trò Nghiên cứu của đề tài có thể "nhận xử lý" khi hạng mục hiện chưa có người phụ trách (đã được nhả).
  - **2.2.3.11.3.** Trong "Đang xét duyệt" (mục 2.2.6.8): áp dụng cơ chế nhận/nhả riêng cho vai trò Xét duyệt, đã đặc tả ở mục 2.2.6.8 — độc lập với người phụ trách của giai đoạn nghiên cứu (khác vai trò, khác lần "nhận xử lý").
  - **2.2.3.11.4.** Ở các trạng thái không yêu cầu người xử lý cụ thể tại thời điểm đó ("Chờ xét duyệt", "Đang xét duyệt AI", "Đã qua xét duyệt AI", "Đạt xét duyệt", "Đã xuất bản", "Không xuất bản") — trường Người phụ trách **giữ nguyên giá trị của lần nhận gần nhất**, mang tính hiển thị/tham khảo, không phát sinh khoá mới, không yêu cầu thao tác nhận việc.
  - **2.2.3.11.5.** Người đang nhận có thể **tự nhả** bất kỳ lúc nào. Nếu không tự nhả (ví dụ nghỉ việc, bị thu hồi quyền), **Quản trị hệ thống có thể cưỡng chế nhả** để người khác nhận được — cùng tinh thần cơ chế gỡ nghẽn đã áp dụng cho vai trò Xuất bản (mục 2.2.1.5.1).
- **2.2.3.12. Người tạo**: ghi nhận Nhân viên đã tạo Hạng mục tri thức (mục 2.2.3.10). **Bất biến** sau khi tạo — không thay đổi khi Người phụ trách (mục 2.2.3.11) được nhả/nhận lại bởi người khác.
- **2.2.3.13. Ngày giờ tạo**: thời điểm Hạng mục tri thức được tạo (mục 2.2.3.10), bất biến — khác với Ngày giờ tạo phiên bản (mục 2.2.3.5), vốn gắn với từng phiên bản đã chốt.
- **2.2.3.14. Xoá Hạng mục tri thức**: Hạng mục tri thức xoá được khi thoả **đồng thời** cả ba điều kiện sau:
  - **2.2.3.14.1.** Chưa có phiên bản nào được chốt (mục 2.2.3.4) — kể cả phiên bản hiện không được chọn để sử dụng (mục 2.2.3.4.1).
  - **2.2.3.14.2.** Đang ở trạng thái "Đang nghiên cứu" (mục 2.2.6.3).
  - **2.2.3.14.3.** Chưa được Mục từ nào tham chiếu (quan hệ ở mục 2.3.3).
  - **2.2.3.14.4. Người xoá**: Quản trị hệ thống (mục 2.1.3.1.1); Chủ nhiệm đề tài (mục 2.2.5.5) của Đề tài nghiên cứu cha (mục 2.2.3.9); hoặc Người phụ trách hiện tại (mục 2.2.3.11). Khi hạng mục đang **không có** Người phụ trách (đã nhả — mục 2.2.3.11.5), chỉ Quản trị hệ thống và Chủ nhiệm đề tài xoá được; Nhân viên giữ vai trò Nghiên cứu muốn xoá phải "nhận xử lý" để trở thành Người phụ trách trước.
  - **2.2.3.14.5.** Xoá Hạng mục tri thức xoá luôn Nội dung (mục 2.2.3.6), Phát biểu (mục 2.2.3.7) và Tham chiếu (mục 2.2.3.8) thuộc hạng mục đó. Tư liệu gốc (mục 2.2.2) mà các Tham chiếu trỏ tới **không bị ảnh hưởng**.
  - **2.2.3.14.6.** Hệ thống **cảnh báo rõ** trước khi xoá, chỉ thực hiện khi người xoá xác nhận. Cách lưu trữ bản ghi sau khi xoá để thiết kế kỹ thuật quyết định — cùng nguyên tắc ở mục 2.2.1.7.4.

#### 2.2.4. Truy vết dữ liệu gốc

Việc tổ chức/gán Tư liệu gốc cho từng Đề tài nghiên cứu được quản lý ở mục 2.2.1; mục này chỉ mô tả tham chiếu chi tiết ở cấp Phát biểu.

Mỗi phát biểu trong Hạng mục tri thức phải tham chiếu đến các Tư liệu gốc liên quan. Vì một Tư liệu gốc có thể gồm nhiều file (mục 2.2.2.4), mỗi tham chiếu phải trỏ đến một file cụ thể. Mỗi tham chiếu cần có:

- **2.2.4.1.** Định danh file cụ thể (thuộc một Tư liệu gốc, xem mục 2.2.2.4) mà tham chiếu này trỏ đến.
- **2.2.4.2.** Vị trí thông tin trong file:
  - **2.2.4.2.1.** Số trang, số dòng đối với văn bản.
  - **2.2.4.2.2.** Vị trí khung thông tin (top, left, right, bottom) đối với hình ảnh.
  - **2.2.4.2.3.** Khoảng thời gian (giờ, phút, giây) đối với âm thanh: gồm thời điểm bắt đầu (bắt buộc) và thời điểm kết thúc (không bắt buộc).
  - **2.2.4.2.4.** Khoảng thời gian (bắt đầu bắt buộc / kết thúc không bắt buộc) và vị trí khung (top, left, right, bottom, không bắt buộc) đối với phim.
- **2.2.4.3.** Ví dụ minh hoạ: Hạng mục tri thức "Trống đồng Đông Sơn" có Phát biểu "Trống đồng Đông Sơn thường có hoa văn hình chim Lạc ở vành ngoài mặt trống", với các tham chiếu:
  - **2.2.4.3.1.** File văn bản (một cuốn sách nghiên cứu đã số hoá): tham chiếu tới trang 42, dòng 5–8.
  - **2.2.4.3.2.** File hình ảnh (ảnh chụp cận cảnh mặt trống đồng): tham chiếu tới khung toạ độ top=120, left=300, right=480, bottom=460 — đúng vùng chứa hoa văn chim Lạc.
  - **2.2.4.3.3.** File âm thanh (ghi âm phỏng vấn nghệ nhân đúc đồng): tham chiếu tới khoảng thời gian từ 00:03:15 đến 00:03:42.
  - **2.2.4.3.4.** File phim (phim tư liệu điền dã): tham chiếu tới khoảng thời gian từ 00:12:03 đến 00:12:20, khung toạ độ top=80, left=200, right=520, bottom=400.

  Một phát biểu có thể có nhiều tham chiếu như vậy cùng lúc (ví dụ vừa trích từ sách, vừa từ ảnh); mỗi tham chiếu là một bản ghi độc lập trỏ về đúng một file.

#### 2.2.5. Vai trò trong module

Module Cơ Sở Dữ Liệu Văn Hóa sử dụng các vai trò (role) sau — xem phân loại Role theo chức năng / Role theo phạm vi ở mục 2.1.3.1:

- **2.2.5.1. Vai trò Nhập liệu** (role theo chức năng): nhập Tư liệu gốc (mục 2.2.2) vào hệ thống, gán Tư liệu gốc cho Đề tài nghiên cứu (mục 2.2.1.3), và bật cờ "Tư liệu sẵn sàng" cho đề tài (mục 2.2.1.6.2). Đây là role theo chức năng dùng chung, **không giới hạn theo phạm vi Đề tài** — vì một Tư liệu gốc có thể được nhiều đề tài cùng sử dụng (mục 2.2.1.3). Vai trò này **không tham gia** quy trình trạng thái của Hạng mục tri thức (mục 2.2.6).
- **2.2.5.2. Vai trò Nghiên cứu** (role theo phạm vi Đề tài nghiên cứu — xem mục 2.1.3.1.2): được hệ thống **tự động tạo cho từng Đề tài nghiên cứu** ngay khi đề tài đó được tạo (xem mục 2.2.1.4). Có quyền truy cập Tư liệu gốc thuộc đề tài (2.2.1.3), **tạo Hạng mục tri thức** (mục 2.2.3.10), thực hiện nghiên cứu và biên tập Hạng mục tri thức (mục 2.2.6.3–2.2.6.4, kể cả nghiên cứu lại sau khi "Không đạt xét duyệt") — chỉ giới hạn trong phạm vi đề tài tương ứng. Một Nhân viên có thể được gán vai trò Nghiên cứu của nhiều đề tài khác nhau.
- **2.2.5.3. Vai trò Xét duyệt** (chuyên gia; role theo phạm vi Đề tài nghiên cứu — xem mục 2.1.3.1.2): được hệ thống **tự động tạo cho từng Đề tài nghiên cứu**, cùng lúc với vai trò Nghiên cứu (xem mục 2.2.1.4). Có quyền xét duyệt Hạng mục tri thức thuộc đề tài (mục 2.2.6.8–2.2.6.10), và **mở lại** hạng mục đang ở "Đã xuất bản"/"Không xuất bản" về một trạng thái trước đó (mục 2.2.6.11–2.2.6.12) — chỉ giới hạn trong phạm vi đề tài tương ứng. Một Nhân viên có thể được gán vai trò Xét duyệt của nhiều đề tài khác nhau; có thể gán nhiều Nhân viên vào cùng một vai trò Xét duyệt của một đề tài.
- **2.2.5.4. Vai trò Xuất bản** (role theo chức năng, tách biệt với vai trò Xét duyệt): thực hiện hai thao tác tách rời trên Hạng mục tri thức — (a) **quyết định xuất bản** cho hạng mục đang ở "Đạt xét duyệt": "Xuất bản" (tạo phiên bản — mục 2.2.3.4 — và chuyển sang "Đã xuất bản") hoặc "Không xuất bản" (không tạo phiên bản, chuyển sang "Không xuất bản"); đây là cách duy nhất để một hạng mục rời khỏi "Đạt xét duyệt"; và (b) **chọn/thay đổi phiên bản đang được sử dụng** (mục 2.2.3.4.1), độc lập với (a).
- **2.2.5.5. Vai trò Chủ nhiệm đề tài** (role theo phạm vi Đề tài nghiên cứu — xem mục 2.1.3.1.2): được hệ thống **tự động tạo cho từng Đề tài nghiên cứu**, cùng lúc với vai trò Nghiên cứu và vai trò Xét duyệt (xem mục 2.2.1.4). Là người chịu trách nhiệm chính, đứng đầu đề tài. Mỗi Đề tài nghiên cứu có **đúng một** Chủ nhiệm đề tài tại một thời điểm; chỉ Quản trị hệ thống mới gán hoặc thay đổi Nhân viên giữ vai trò này (mục 2.2.1.4) — Chủ nhiệm đề tài không tự chuyển giao vai trò cho người khác. Có quyền **gán/gỡ** Nhân viên vào vai trò Nghiên cứu và vai trò Xét duyệt của đề tài mình phụ trách (mục 2.2.5.2, 2.2.5.3), không cần qua Quản trị hệ thống. Để gán, Chủ nhiệm đề tài được **tìm kiếm Nhân viên theo từ khoá** trong toàn bộ Nhân viên của hệ thống, **không giới hạn Tổ chức** (nhất quán với mục 2.2.1.4: một đề tài có thể có Nhân viên từ nhiều Tổ chức). Kết quả tìm kiếm chỉ hiển thị thông tin định danh tối thiểu (tên gọi, email) đủ để chọn đúng người. Vai trò Chủ nhiệm đề tài **không tự động** có quyền thực hiện Nghiên cứu (2.2.6.3–2.2.6.4) hay Xét duyệt (2.2.6.8–2.2.6.10) — muốn tự mình thực hiện, phải tự gán thêm vai trò Nghiên cứu/Xét duyệt tương ứng cho chính mình. Một Nhân viên có thể đồng thời giữ vai trò Chủ nhiệm đề tài của nhiều đề tài khác nhau. Chủ nhiệm đề tài **xem được tiến độ** của Đề tài mình phụ trách: thống kê số Hạng mục tri thức theo từng trạng thái (mục 2.2.6), và danh sách Hạng mục tri thức kèm Tiêu đề (mục 2.2.3.2), trạng thái (mục 2.2.3.3), Người phụ trách hiện tại (mục 2.2.3.11) và Người tạo (mục 2.2.3.12). Quyền xem này **không bao gồm** xem Nội dung (mục 2.2.3.6), Phát biểu (mục 2.2.3.7), Tham chiếu (mục 2.2.3.8) hay kết quả xét duyệt (mục 2.2.6.6, 2.2.6.8), và **không kèm** quyền thực hiện Nghiên cứu (mục 2.2.6.3–2.2.6.4) hay Xét duyệt (mục 2.2.6.8–2.2.6.10). Ngoài ra, Chủ nhiệm đề tài **xoá được Hạng mục tri thức** đủ điều kiện thuộc đề tài mình phụ trách (mục 2.2.3.14).

Phân quyền chi tiết theo từng hành động sẽ được thiết kế cụ thể khi triển khai (xem mục 2.1.3.1).

#### 2.2.6. Quy trình & trạng thái Hạng mục tri thức

Quy trình: `Nghiên Cứu → Xét Duyệt`

Trạng thái:

```
Đang nghiên cứu → Chờ xét duyệt
  → (kích hoạt AI Verification) → Đang xét duyệt AI
      → Đã qua xét duyệt AI → (nhận xử lý) → Đang xét duyệt (chuyên gia)
          → Không đạt xét duyệt → Đang nghiên cứu
          → Đạt xét duyệt → (chỉ vai trò Xuất bản) Đã xuất bản | Không xuất bản
      → Không đạt xét duyệt (bởi AI) → Đang nghiên cứu

Kích hoạt lại AI Verification (→ Đang xét duyệt AI) từ:
    Chờ xét duyệt | Đang xét duyệt AI | Đã qua xét duyệt AI | Không đạt xét duyệt

Đã xuất bản | Không xuất bản → (chỉ vai trò Xét duyệt) một trạng thái trước đó bất kỳ:
    Đang nghiên cứu | Chờ xét duyệt | Đã qua xét duyệt AI | Đang xét duyệt
```

Các bước trong quy trình được thực hiện bởi các vai trò đã mô tả ở mục 2.2.5: **vai trò Nghiên cứu** (2.2.6.3–2.2.6.4, và nghiên cứu lại sau "Không đạt xét duyệt"), **vai trò Xét duyệt** (chuyên gia, 2.2.6.8–2.2.6.10, và mở lại hạng mục đã xuất bản — 2.2.6.11–2.2.6.12), **vai trò Xuất bản** (quyết định xuất bản tại "Đạt xét duyệt" — 2.2.6.10). Thao tác chọn phiên bản đang được sử dụng của vai trò Xuất bản (mục 2.2.3.4.1) diễn ra độc lập, không thuộc quy trình trạng thái này.

- **2.2.6.3. Đang nghiên cứu**: Hạng mục tri thức được **khởi tạo** ở trạng thái này, do vai trò Nghiên cứu tạo (mục 2.2.3.10). Đang trong quá trình nghiên cứu để biên tập nội dung Hạng mục tri thức (mục 2.2.3.6), cùng với việc tạo các tham chiếu đến tư liệu gốc. Chỉ **Người phụ trách** hiện tại (mục 2.2.3.11) được thực hiện các thao tác này.
- **2.2.6.4. Chờ xét duyệt**: Bật cờ sẵn sàng cho việc xét duyệt.
- **2.2.6.5. Kích hoạt AI Verification**: được kích hoạt **tự động** (ngay khi vào trạng thái "Chờ xét duyệt") hoặc **thủ công**, tùy theo cấu hình hệ thống (mục 2.8.4.1). Khi cấu hình thủ công, người nghiên cứu, chuyên gia xét duyệt, hoặc các role khác được cấp quyền đều có thể kích hoạt, và có thể kích hoạt lại nhiều lần. Quyền kích hoạt được quản lý theo role.
  - **2.2.6.5.1. Đang xét duyệt AI**: sau khi được kích hoạt, Hạng mục tri thức ở trạng thái "Đang xét duyệt AI" trong lúc AI Verification (mục 2.2.6.6) xử lý theo hàng đợi (mục 3.2.2). Khi có kết quả, hạng mục chuyển sang "Đã qua xét duyệt AI" (mục 2.2.6.7) hoặc "Không đạt xét duyệt" (mục 2.2.6.9) theo mục 2.2.6.6.4. Trong trạng thái này **nội dung bị khoá**: vai trò Nghiên cứu không sửa được Nội dung (mục 2.2.3.6), Phát biểu (2.2.3.7) hay Tham chiếu (2.2.3.8). Giao diện hiển thị rõ hạng mục đang được AI xử lý.
  - **2.2.6.5.2. Kích hoạt lại**: AI Verification được kích hoạt lại khi hạng mục đang ở "Chờ xét duyệt", "Đang xét duyệt AI", "Đã qua xét duyệt AI" hoặc "Không đạt xét duyệt". Mỗi lần kích hoạt lại, hạng mục quay về "Đang xét duyệt AI" và kết quả mới thay thế kết quả cũ. Nếu AI Verification của hạng mục đang chờ hoặc đang chạy, hệ thống không chạy thêm một lượt trùng. Nếu lượt AI Verification trước bị lỗi hoặc bị huỷ, kích hoạt lại là cách tiếp tục xử lý hạng mục. Khi vai trò Xét duyệt mở lại hạng mục đã "Đã xuất bản"/"Không xuất bản" (mục 2.2.6.11–2.2.6.12), trạng thái đích không gồm "Đang xét duyệt AI"; muốn chạy lại AI Verification thì mở về "Chờ xét duyệt" rồi kích hoạt.
- **2.2.6.6. AI Verification** (thực hiện bởi "Trợ lý Tư liệu gốc" — self-host AI huấn luyện bằng tư liệu gốc):
  - **2.2.6.6.1.** Duyệt từng Tham chiếu đến Tư liệu gốc dựa trên **2 tiêu chí**: (a) vị trí tham chiếu có tồn tại hợp lệ trong file tư liệu gốc (đúng số trang/dòng, khung ảnh, khoảng thời gian...), và (b) nội dung Phát biểu có khớp ngữ nghĩa với nội dung tại đúng vị trí đó trong tư liệu gốc. Tham chiếu chỉ **đạt** khi thỏa cả hai tiêu chí.
  - **2.2.6.6.2.** Nếu phát biểu có khai báo Vị trí trong Nội dung (mục 2.2.3.7.1), kiểm tra vị trí đó theo đúng 2 tiêu chí trên, áp dụng cho Nội dung (2.2.3.6) của Hạng mục tri thức thay vì Tư liệu gốc: (a) vị trí đó có tồn tại hợp lệ trong file Nội dung, và (b) nội dung phát biểu có khớp ngữ nghĩa với nội dung tại đúng vị trí đó — tức đối chiếu chính phát biểu với đúng vị trí nó tự khai.
  - **2.2.6.6.3.** Ghi nhận thời điểm xét duyệt và ghi chú của AI cho mỗi Tham chiếu và mỗi Vị trí trong Nội dung đã khai báo.
  - **2.2.6.6.4.** Nếu **tất cả** Tham chiếu và (các) Vị trí trong Nội dung đã khai báo đều đạt → chuyển "Đã qua xét duyệt AI". Nếu có Tham chiếu hoặc Vị trí trong Nội dung không đạt → chuyển thẳng "Không đạt xét duyệt" (không cần chuyên gia duyệt tiếp).
  - **2.2.6.6.5.** Rà soát Nội dung (mục 2.2.3.6) của Hạng mục tri thức để phát hiện các phát biểu tiềm năng xuất hiện trong nội dung nhưng chưa được liệt kê thành Phát biểu (mục 2.2.3.7); ghi nhận danh sách gợi ý này kèm theo kết quả AI Verification, để chuyên gia xét duyệt (mục 2.2.6.8.2) rà soát và xác nhận. Bước này chỉ mang tính gợi ý — không tự động khiến hạng mục "Không đạt xét duyệt".
- **2.2.6.7. Đã qua xét duyệt AI**: đã vượt qua bước AI Verification, sẵn sàng cho chuyên gia xét duyệt. Hạng mục tri thức ở trạng thái này **chưa có ai phụ trách xét duyệt** — để chuyển sang "Đang xét duyệt" (mục 2.2.6.8), một Nhân viên giữ vai trò Xét duyệt của đề tài phải chủ động **"nhận xử lý"** hạng mục này (xem mục 2.2.6.8).
- **2.2.6.8. Đang xét duyệt**: Nhân viên giữ vai trò Xét duyệt **"nhận xử lý"** một Hạng mục tri thức đang ở "Đã qua xét duyệt AI" (mục 2.2.6.7) để chuyển sang trạng thái này — thao tác **khoá độc quyền**: tại một thời điểm, mỗi hạng mục chỉ có đúng một chuyên gia đang xử lý; chuyên gia khác không nhận hay ghi nhận kết quả xét duyệt được cho tới khi được nhả ra. Chuyên gia đã nhận có thể **tự nhả** bất kỳ lúc nào, đưa hạng mục quay lại "Đã qua xét duyệt AI" để người khác nhận. Nếu không tự nhả, Quản trị hệ thống có thể **cưỡng chế nhả** (xem mục 2.2.3.11.5). Trong khi đang xét duyệt, **nội dung bị khoá**: vai trò Nghiên cứu không sửa được Nội dung (mục 2.2.3.6), Phát biểu (2.2.3.7) hay Tham chiếu (2.2.3.8) — phải chờ chuyên gia chuyển sang "Không đạt xét duyệt" (2.2.6.9) mới sửa tiếp được.
  - **2.2.6.8.1.** Xét duyệt tất cả các Phát biểu. Với mỗi Tham chiếu tư liệu gốc của phát biểu, và Vị trí trong Nội dung (2.2.3.7.1) nếu có khai báo, chuyên gia cần ghi nhận một kết luận **đạt/không đạt riêng cho từng Tham chiếu/Vị trí** — tương tự cách AI Verification ghi nhận ở mục 2.2.6.6.1 — kèm thời điểm xét duyệt và ghi chú của chuyên gia. Kết luận tổng thể ở bước thẩm định (mục 2.2.6.8.3) dựa trên các kết luận đạt/không đạt riêng lẻ này.
  - **2.2.6.8.2.** Rà soát các Phát biểu bị bỏ sót, tham khảo danh sách gợi ý từ AI Verification (mục 2.2.6.6) nếu có.
  - **2.2.6.8.3.** Thẩm định, đánh giá tổng thể nội dung Hạng mục tri thức.
- **2.2.6.9. Không đạt xét duyệt**: Bị từ chối bởi AI (xem mục 2.2.6.6) hoặc bởi chuyên gia. Xem xét các ghi chú trong quá trình duyệt để nghiên cứu lại (quay về "Đang nghiên cứu"; không tạo phiên bản mới ở bước này — xem mục 2.2.3.4).
- **2.2.6.10. Đạt xét duyệt**: Chuyên gia xác nhận đã đạt xét duyệt. **Nội dung bị khoá**: vai trò Nghiên cứu không sửa được Nội dung (2.2.3.6), Phát biểu (2.2.3.7) hay Tham chiếu (2.2.3.8). **Chỉ vai trò Xuất bản** được đưa hạng mục rời khỏi trạng thái này, bằng đúng một trong hai quyết định: **"Xuất bản"** → tạo phiên bản (mục 2.2.3.4) và chuyển sang "Đã xuất bản" (2.2.6.11); hoặc **"Không xuất bản"** → không tạo phiên bản và chuyển sang "Không xuất bản" (2.2.6.12), kèm cảnh báo rằng vòng xét duyệt này sẽ không để lại bản chốt nào. Vai trò Nghiên cứu và vai trò Xét duyệt **không tự** đưa hạng mục rời khỏi trạng thái này.
- **2.2.6.11. Đã xuất bản**: vai trò Xuất bản đã chốt phiên bản cho vòng xét duyệt vừa rồi (mục 2.2.3.4). Nội dung bị khoá — vai trò Nghiên cứu không sửa được. Trạng thái này **không đồng nghĩa** với việc phiên bản vừa tạo đang được sử dụng: việc chọn phiên bản đang được sử dụng là thao tác riêng của vai trò Xuất bản (mục 2.2.3.4.1). **Chỉ vai trò Xét duyệt** được đưa hạng mục rời khỏi trạng thái này, chuyển về **bất kỳ trạng thái nào trước đó** trong quy trình — "Đang nghiên cứu" (2.2.6.3), "Chờ xét duyệt" (2.2.6.4), "Đã qua xét duyệt AI" (2.2.6.7) hoặc "Đang xét duyệt" (2.2.6.8) — tuỳ mức độ cần làm lại. Các phiên bản đã tạo trước đó vẫn được giữ nguyên, không bị ảnh hưởng.
- **2.2.6.12. Không xuất bản**: vai trò Xuất bản quyết định không chốt phiên bản cho vòng xét duyệt vừa rồi — vòng đó không để lại bản chốt nào. Nội dung bị khoá, giống "Đã xuất bản". **Chỉ vai trò Xét duyệt** được đưa hạng mục rời khỏi trạng thái này, chuyển về bất kỳ trạng thái nào trước đó, cùng danh sách như ở mục 2.2.6.11.

### 2.3. Bách Khoa Toàn Thư

- **2.3.1.** Bách khoa toàn thư là một tập gồm các mục từ, được tạo ra từ các Hạng mục tri thức đang có phiên bản được chọn để sử dụng (mục 2.2.3.4.1) của Cơ Sở Dữ Liệu Văn Hóa.
- **2.3.2.** Mỗi Mục từ cần có:
  - **2.3.2.1.** Định danh.
  - **2.3.2.2.** Tiêu đề.
  - **2.3.2.3.** Nội dung: mỗi Mục từ có cấu trúc kiểu **trang wiki**, gồm:
    - **2.3.2.3.1.** Một nội dung chính dạng **JSON có cấu trúc block**: một danh sách các khối nội dung (block) có thứ tự, mỗi khối có một loại (type) và dữ liệu tương ứng — ví dụ: tiêu đề, đoạn văn, chú thích, khối nhúng hình ảnh, khối nhúng âm thanh, khối nhúng phim.
    - **2.3.2.3.2.** Các file đính kèm (hình ảnh, âm thanh, phim...) được nhúng vào đúng vị trí cụ thể trong nội dung — thể hiện bằng một khối (block) loại nhúng file được chèn đúng thứ tự trong danh sách các khối.

    Khác với Tư liệu gốc (2.2.2.4) — nơi các file đứng ngang hàng, không phân biệt file chính/phụ — Mục từ có **một file nội dung chính giữ vai trò trung tâm**, các file khác chỉ là tài nguyên đính kèm.
  - **2.3.2.4.** Phiên bản: mỗi Mục từ có thể có nhiều phiên bản theo thời gian, tương tự Hạng mục tri thức (mục 2.2.3.4). Phiên bản **do vai trò Xuất bản Mục từ tạo** (mục 2.3.4.2) khi thực hiện quyết định xuất bản trên một Mục từ đang ở trạng thái **"Đạt xét duyệt"** (mục 2.3.5.5) — hệ thống **không tự động** tạo phiên bản khi chuyển trạng thái. Phiên bản chốt lại nội dung tại thời điểm tạo và **bất biến** sau đó.
    - Khi Mục từ ở "Đạt xét duyệt", vai trò Xuất bản Mục từ chọn **một trong hai**: **"Xuất bản"** — tạo phiên bản và chuyển Mục từ sang "Đã xuất bản" (mục 2.3.5.7); hoặc **"Không xuất bản"** — không tạo phiên bản và chuyển Mục từ sang "Không xuất bản" (mục 2.3.5.8).
    - Vì vậy mỗi vòng xét duyệt thành công tạo ra **tối đa 1 phiên bản**, tuỳ quyết định của vai trò Xuất bản Mục từ.
    - Khi chọn "Không xuất bản", vòng xét duyệt đó **không để lại bản chốt nào** — nội dung đã qua xét duyệt sẽ bị ghi đè nếu Mục từ được mở lại để sửa tiếp. Hệ thống **không chặn** nhưng phải **cảnh báo rõ**, chỉ tiếp tục khi vai trò Xuất bản Mục từ xác nhận.
    - Bị "Không đạt xét duyệt" (mục 2.3.5.4) và quay lại "Soạn thảo" để sửa tiếp không tạo phiên bản — các chỉnh sửa đó vẫn thuộc bản đang soạn thảo.
    - Các phiên bản đã tạo được **giữ lại đầy đủ, không ghi đè**, phục vụ truy vết lịch sử.
    - **2.3.2.4.1.** Phiên bản đang công khai: ghi nhận phiên bản nào (trong số các phiên bản đã tạo ở mục 2.3.2.4) hiện đang được chọn để hiển thị công khai trên Bách Khoa Toàn Thư (mục 2.6). Do **vai trò Xuất bản Mục từ** chọn (mục 2.3.4.2), có thể đổi sang phiên bản khác bất kỳ lúc nào — không bắt buộc là phiên bản mới nhất. **Tạo phiên bản (mục 2.3.2.4) và chọn phiên bản đang công khai là hai thao tác tách rời**: tạo một phiên bản mới không tự động đưa phiên bản đó ra công khai. Mặc định chưa có phiên bản nào được chọn (Mục từ chưa công khai) cho tới lần chọn đầu tiên. Đây **không phải một trạng thái** của Mục từ (xem mục 2.3.5) — việc soạn thảo/xét duyệt tiếp theo diễn ra độc lập (kể cả khi Mục từ được mở lại để làm tiếp sau khi đã xuất bản), không ảnh hưởng tới phiên bản đang công khai, cho tới khi vai trò Xuất bản Mục từ chủ động chọn phiên bản khác.
  - **2.3.2.5. Người phụ trách**: ghi nhận đúng một Nhân viên đang chịu trách nhiệm chính tại thời điểm hiện tại, xuyên suốt vòng đời Mục từ (mọi trạng thái ở mục 2.3.5). Cơ chế **"nhận xử lý"/"nhả"** tường minh, khoá độc quyền — cùng quy tắc như mục 2.2.3.11 của Hạng mục tri thức.
    - **2.3.2.5.1.** Khi Mục từ được tạo (gộp/tách từ Hạng mục tri thức, mục 2.3.3), người tạo (vai trò Biên tập) tự động trở thành người phụ trách đầu tiên.
    - **2.3.2.5.2.** Trong "Soạn thảo" (mục 2.3.5.1): chỉ Người phụ trách hiện tại được sửa nội dung Mục từ (2.3.2.3). Một Nhân viên khác giữ vai trò Biên tập có thể "nhận xử lý" khi Mục từ hiện chưa có người phụ trách.
    - **2.3.2.5.3.** Trong "Đang xét duyệt" (mục 2.3.5.3): áp dụng cơ chế nhận/nhả riêng cho vai trò Xét duyệt Mục từ, đã đặc tả ở mục 2.3.5.3 — độc lập với người phụ trách của giai đoạn soạn thảo.
    - **2.3.2.5.4.** Ở các trạng thái chờ khác ("Chờ xét duyệt", "Đạt xét duyệt", "Đã xuất bản", "Không xuất bản") — giữ nguyên giá trị lần nhận gần nhất, mang tính hiển thị.
    - **2.3.2.5.5.** Người đang nhận có thể **tự nhả**; nếu không, Quản trị hệ thống có thể **cưỡng chế nhả** — cùng cơ chế như mục 2.2.3.11.5.
- **2.3.3.** Quan hệ giữa Hạng mục tri thức và Mục từ là **nhiều – nhiều**: vai trò Biên tập (2.3.4.1) có thể gộp nhiều Hạng mục tri thức thành một Mục từ, hoặc tách một Hạng mục tri thức thành nhiều Mục từ. Khi Hạng mục tri thức nguồn đổi phiên bản đang được sử dụng (mục 2.2.3.4.1), Mục từ liên quan **không tự động cập nhật** — vai trò Biên tập phải chủ động đồng bộ lại nội dung.
  - **2.3.3.1.** Với mỗi Hạng mục tri thức đã gán cho Mục từ, hệ thống ghi nhận phiên bản mà vai trò Biên tập đã dùng làm nguồn lần đồng bộ gần nhất. Khi **phiên bản đang được sử dụng** (mục 2.2.3.4.1) của Hạng mục tri thức đó khác với phiên bản đã đồng bộ, màn hình Mục từ **cảnh báo** nguồn đã lỗi thời. Sau khi cập nhật nội dung, vai trò Biên tập xác nhận đã đồng bộ để tắt cảnh báo. Cảnh báo chỉ mang tính nhắc việc: không chặn thao tác nào và không tự sửa nội dung Mục từ.
- **2.3.4. Vai trò trong module** (khác các vai trò ở mục 2.2.5: Nhập liệu/Nghiên cứu/Xét duyệt/Xuất bản — module Bách Khoa Toàn Thư có vai trò riêng):
  - **2.3.4.1. Vai trò Biên tập**: soạn thảo Mục từ (gộp/tách Hạng mục tri thức, biên soạn nội dung — các khối block theo mục 2.3.2.3), đồng bộ lại nội dung khi Hạng mục tri thức nguồn đổi phiên bản đang được sử dụng (mục 2.2.3.4.1, 2.3.3.1), và gán Cương vực (2.3.6). Có thể dùng AI để hỗ trợ khởi tạo/tạo lại nội dung ban đầu (mục 2.3.8).
  - **2.3.4.2. Vai trò Xuất bản Mục từ** (vai trò riêng, khác với **vai trò Xuất bản** ở mục 2.2.5.4 — vốn làm việc trên Hạng mục tri thức): thực hiện hai thao tác tách rời trên Mục từ — (a) **quyết định xuất bản** cho Mục từ đang ở "Đạt xét duyệt": "Xuất bản" (tạo phiên bản — mục 2.3.2.4 — và chuyển sang "Đã xuất bản") hoặc "Không xuất bản" (không tạo phiên bản, chuyển sang "Không xuất bản"); đây là cách duy nhất để một Mục từ rời khỏi "Đạt xét duyệt"; và (b) **chọn/thay đổi phiên bản đang công khai** (mục 2.3.2.4.1), độc lập với (a).
- **2.3.5. Quy trình & trạng thái Mục từ**:

  ```
  Soạn thảo → Chờ xét duyệt → (nhận xử lý) → Đang xét duyệt → Đạt xét duyệt
                                             → Không đạt xét duyệt → Soạn thảo

  Đạt xét duyệt → (chỉ vai trò Xuất bản Mục từ) Đã xuất bản | Không xuất bản

  Đã xuất bản | Không xuất bản → (chỉ vai trò Xét duyệt Mục từ) một trạng thái trước đó bất kỳ:
      Soạn thảo | Chờ xét duyệt | Đang xét duyệt
  ```

  **Vai trò Xuất bản Mục từ** tham gia quy trình trạng thái ở đúng một điểm: quyết định xuất bản tại "Đạt xét duyệt" (mục 2.3.5.5). Thao tác chọn phiên bản đang công khai (mục 2.3.2.4.1) diễn ra độc lập, không thuộc quy trình trạng thái này.

  - **2.3.5.1. Soạn thảo**: vai trò Biên tập tạo/sửa nội dung Mục từ. Chỉ **Người phụ trách** hiện tại (mục 2.3.2.5) được thực hiện thao tác này.
  - **2.3.5.2. Chờ xét duyệt**: vai trò Biên tập bật cờ sẵn sàng cho xét duyệt. Mục từ ở trạng thái này **chưa có ai phụ trách xét duyệt** — để chuyển sang "Đang xét duyệt" (mục 2.3.5.3), một Nhân viên giữ vai trò Xét duyệt Mục từ phải chủ động **"nhận xử lý"** mục từ này (xem mục 2.3.5.3).
  - **2.3.5.3. Đang xét duyệt**: một Nhân viên giữ **vai trò Xét duyệt Mục từ** — nhóm chuyên gia riêng, khác với vai trò Xét duyệt ở mục 2.2.5 (xét duyệt Hạng mục tri thức) — **"nhận xử lý"** Mục từ đang ở "Chờ xét duyệt" (mục 2.3.5.2) để chuyển sang trạng thái này. Thao tác **khoá độc quyền**: tại một thời điểm, mỗi Mục từ chỉ có đúng một chuyên gia đang xử lý; chuyên gia khác không nhận được cho tới khi được nhả ra. Chuyên gia đã nhận có thể **tự nhả** bất kỳ lúc nào, đưa Mục từ quay lại "Chờ xét duyệt" để người khác nhận. Nếu không tự nhả, Quản trị hệ thống có thể **cưỡng chế nhả** (xem mục 2.3.2.5.5). Vai trò này cũng **mở lại** Mục từ đang ở "Đã xuất bản"/"Không xuất bản" về một trạng thái trước đó (mục 2.3.5.7–2.3.5.8). **Nội dung bị khoá**: vai trò Biên tập không sửa được nội dung Mục từ (mục 2.3.2.3) trong khi Mục từ đang ở trạng thái này — phải chờ vai trò Xét duyệt Mục từ chuyển sang "Không đạt xét duyệt" (2.3.5.4) mới sửa tiếp được. Khi kết luận "Đạt xét duyệt" hoặc "Không đạt xét duyệt", vai trò Xét duyệt Mục từ ghi **nhận xét tổng thể** cho Mục từ; nhận xét là **bắt buộc** khi kết luận "Không đạt xét duyệt", không bắt buộc khi "Đạt xét duyệt". Mục từ không có cấu trúc Phát biểu/Tham chiếu như Hạng mục tri thức, nên việc xét duyệt thực hiện ở cấp toàn Mục từ.
  - **2.3.5.4. Không đạt xét duyệt**: vai trò Biên tập xem nhận xét của vai trò Xét duyệt Mục từ (mục 2.3.5.3), rồi đưa Mục từ quay lại "Soạn thảo" để chỉnh sửa theo góp ý.
  - **2.3.5.5. Đạt xét duyệt**: **vai trò Xét duyệt Mục từ** xác nhận đạt xét duyệt. **Nội dung bị khoá**: vai trò Biên tập không sửa được nội dung Mục từ (mục 2.3.2.3). **Chỉ vai trò Xuất bản Mục từ** được đưa Mục từ rời khỏi trạng thái này, bằng đúng một trong hai quyết định: **"Xuất bản"** → tạo phiên bản (mục 2.3.2.4) và chuyển sang "Đã xuất bản" (2.3.5.7); hoặc **"Không xuất bản"** → không tạo phiên bản và chuyển sang "Không xuất bản" (2.3.5.8), kèm cảnh báo rằng vòng xét duyệt này sẽ không để lại bản chốt nào. Vai trò Biên tập và vai trò Xét duyệt Mục từ **không tự** đưa Mục từ rời khỏi trạng thái này.
  - **2.3.5.6.** Việc sửa tiếp một Mục từ (sau khi vai trò Xét duyệt Mục từ mở lại về "Soạn thảo") không bị chặn bởi và không ảnh hưởng tới phiên bản đang công khai (mục 2.3.2.4.1) — nội dung công khai chỉ thay đổi khi **vai trò Xuất bản Mục từ** chủ động chọn một phiên bản khác.
  - **2.3.5.7. Đã xuất bản**: vai trò Xuất bản Mục từ đã chốt phiên bản cho vòng xét duyệt vừa rồi (mục 2.3.2.4). Nội dung bị khoá — vai trò Biên tập không sửa được. Trạng thái này **không đồng nghĩa** với việc phiên bản vừa tạo đang công khai: việc chọn phiên bản đang công khai là thao tác riêng của vai trò Xuất bản Mục từ (mục 2.3.2.4.1). **Chỉ vai trò Xét duyệt Mục từ** được đưa Mục từ rời khỏi trạng thái này, chuyển về **bất kỳ trạng thái nào trước đó** trong quy trình — "Soạn thảo" (2.3.5.1), "Chờ xét duyệt" (2.3.5.2) hoặc "Đang xét duyệt" (2.3.5.3) — tuỳ mức độ cần làm lại. Các phiên bản đã tạo trước đó vẫn được giữ nguyên, không bị ảnh hưởng.
  - **2.3.5.8. Không xuất bản**: vai trò Xuất bản Mục từ quyết định không chốt phiên bản cho vòng xét duyệt vừa rồi — vòng đó không để lại bản chốt nào. Nội dung bị khoá, giống "Đã xuất bản". **Chỉ vai trò Xét duyệt Mục từ** được đưa Mục từ rời khỏi trạng thái này, chuyển về bất kỳ trạng thái nào trước đó, cùng danh sách như ở mục 2.3.5.7.
- **2.3.6. Cương vực**: là một phạm vi (taxonomy) dùng để phân loại các mục từ. Mỗi mục từ có thể thuộc về nhiều cương vực, ví dụ: gia lễ, đình làng, trống đồng, v.v. Do **vai trò Biên tập gán thủ công** (có thể tự động hoá/gợi ý trong tương lai).
- **2.3.7.** Các cương vực dự kiến:
  - **2.3.7.1.** Văn minh đình làng việt.
  - **2.3.7.2.** Văn minh gia lễ việt.
  - **2.3.7.3.** Văn minh quân sự việt.
  - **2.3.7.4.** Văn minh trống đồng.
  - **2.3.7.5.** Danh sách cương vực ở trên là danh sách khởi đầu và **có thể thay đổi**. **Vai trò Biên tập** (mục 2.3.4.1) được thêm cương vực mới, sửa tên cương vực đã có, và **xoá** cương vực. Chỉ xoá được cương vực **chưa được gán cho Mục từ nào** (mục 2.3.6); nếu còn Mục từ đang gán, hệ thống chặn thao tác xoá và vai trò Biên tập phải gỡ cương vực khỏi các Mục từ đó trước. Hệ thống cảnh báo rõ trước khi xoá, chỉ thực hiện khi vai trò Biên tập xác nhận. Mọi Nhân viên đều xem được danh sách cương vực (để lọc khi trò chuyện với AI — mục 2.4.3). Người dùng công khai xem được qua Ứng dụng Web (mục 2.6.2.2).
- **2.3.8. Khởi tạo nội dung Mục từ bằng AI**: vai trò Biên tập có thể yêu cầu hệ thống dùng AI tự động sinh nội dung (mục 2.3.2.3) cho Mục từ, dựa trên nội dung của (các) Hạng mục tri thức đã gán cho Mục từ đó (mục 2.3.3) — hỗ trợ thay vì bắt buộc phải tự soạn thảo từ đầu.
  - **2.3.8.1.** Là một **thao tác thủ công riêng**, do vai trò Biên tập chủ động kích hoạt — không tự động chạy khi tạo Mục từ. Chỉ thực hiện được khi Mục từ đang ở "Soạn thảo" (mục 2.3.5.1) và bởi Người phụ trách hiện tại (mục 2.3.2.5), cùng điều kiện với việc sửa nội dung thủ công.
  - **2.3.8.2.** Có thể kích hoạt lại nhiều lần — ví dụ để tạo lại bản nháp sau khi gộp/tách thêm Hạng mục tri thức (mục 2.3.3), hoặc khi cần đồng bộ lại theo phiên bản đang được sử dụng mới của Hạng mục tri thức nguồn (mục 2.2.3.4.1, 2.3.3.1).
  - **2.3.8.3.** Nội dung do AI sinh ra sẽ **ghi đè** nội dung hiện tại của Mục từ (mục 2.3.2.3). Hệ thống **không chặn** nhưng phải **cảnh báo rõ** trước khi ghi đè, chỉ tiếp tục khi vai trò Biên tập xác nhận — cùng nguyên tắc cảnh báo đã áp dụng ở mục 2.3.5.8.
  - **2.3.8.4.** Việc sinh nội dung có thể mất thời gian xử lý — hệ thống cần cho vai trò Biên tập biết Mục từ đang trong quá trình xử lý (chi tiết cơ chế để thiết kế kỹ thuật quyết định).
  - **2.3.8.5.** Nội dung do AI sinh ra trở thành nội dung Mục từ bình thường ngay khi sinh xong — không đánh dấu/phân biệt với nội dung do vai trò Biên tập tự viết. Vai trò Biên tập chịu trách nhiệm rà soát, chỉnh sửa trước khi bật cờ "Chờ xét duyệt" (mục 2.3.5.2) — không có bước xét duyệt tự động riêng cho phần nội dung do AI sinh (khác Hạng mục tri thức, Mục từ không có AI Verification, xem mục 2.3.5).

### 2.4. AI Văn Minh Việt

- **2.4.1.** Là self-host AI theo kiến trúc **RAG** (Retrieval-Augmented Generation): khi trả lời, truy xuất nội dung liên quan từ **Bách Khoa Toàn Thư** (các Mục từ, mục 2.3) và trích dẫn Mục từ nguồn kèm theo câu trả lời.
- **2.4.2.** Đối tượng sử dụng: tất cả người dùng — cả Nhân viên (mục 2.1.3.1) và Người dùng công khai (mục 2.1.3.2).
- **2.4.3.** Cho phép lựa chọn cương vực, để giới hạn phạm vi trả lời trong các Mục từ tương ứng, ví dụ: gia lễ, đình làng, trống đồng, v.v. Nếu không chọn cương vực, AI trả lời trên **toàn bộ** Bách Khoa Toàn Thư.
- **2.4.4.** Phạm vi trả lời: **giới hạn** trong phạm vi tri thức của Bách Khoa Toàn Thư; không trả lời các câu hỏi ngoài phạm vi văn hóa/kiến thức chung không liên quan.
- **2.4.5.** Các cương vực dự kiến: giống danh sách cương vực ở mục 2.3.7.
- **2.4.6. Hội thoại nhiều lượt**: người dùng hỏi tiếp nối trong cùng một hội thoại. AI hiểu câu hỏi dựa trên một số lượt hỏi–đáp gần nhất của hội thoại đó, ví dụ câu "còn về X thì sao?" sau một câu hỏi trước. Số lượt dùng làm ngữ cảnh và thời hạn giữ hội thoại do Quản trị hệ thống cấu hình (mục 2.8.4.4). Người dùng có thể bắt đầu hội thoại mới bất kỳ lúc nào. Hội thoại của kênh công khai và của Nhân viên tách biệt nhau. Nhân viên không xem được hội thoại của Nhân viên khác trong giao diện trò chuyện.
- **2.4.7.** Khi Bách Khoa Toàn Thư không có nội dung phù hợp để trả lời (mục 2.4.4), AI trả lời bằng một câu thông báo mặc định do Quản trị hệ thống cấu hình (mục 2.8.4.4), không tự suy diễn ngoài phạm vi.
- **2.4.8.** Giao diện trò chuyện hiển thị **câu miễn trừ trách nhiệm**: câu trả lời do AI tạo ra và có thể chưa chính xác, người dùng nên đối chiếu với các Mục từ nguồn. Nội dung câu do Quản trị hệ thống cấu hình (mục 2.8.4.4); để trống thì không hiển thị.
- **2.4.9. Nhật ký hỏi đáp và rà soát chất lượng**: hệ thống lưu mỗi lượt hỏi–đáp ở cả hai kênh, gồm câu hỏi, câu trả lời, các Mục từ được trích dẫn, cương vực đã chọn (nếu có), và kết quả **tự kiểm** của AI. Tự kiểm là bước AI đối chiếu câu trả lời với nội dung đã truy xuất để đánh dấu các ý chưa có căn cứ. Mục đích lưu là phục vụ rà soát chất lượng câu trả lời.
  - **2.4.9.1.** Lượt hỏi của kênh công khai **không gắn** với định danh hay địa chỉ IP của người hỏi. Lượt hỏi của Nhân viên gắn với Nhân viên đã hỏi.
  - **2.4.9.2.** Việc rà soát do Nhân viên giữ vai trò **Quản trị hệ thống** thực hiện từ giao diện quản trị nội bộ. Người rà soát xem lại toàn bộ hội thoại và lọc theo kênh, người hỏi, cương vực, thời gian, và theo lượt có ý bị AI tự kiểm đánh dấu.
  - **2.4.9.3.** Giai đoạn này **chưa có** chức năng để người dùng đánh giá câu trả lời (thích/không thích, báo sai).
  - **2.4.9.4.** Nhật ký hỏi đáp được lưu **có thời hạn**. Thời hạn do Quản trị hệ thống cấu hình (mục 2.8.4.4); giá trị mặc định do thiết kế kỹ thuật quyết định. Lượt hỏi–đáp quá thời hạn được hệ thống tự động xoá. Lý do: câu hỏi của người dùng có thể vô tình chứa thông tin cá nhân (mục 3.1.1).

### 2.5. Module ngoài phạm vi giai đoạn này (chưa đặc tả chi tiết)

- **2.5.1.** Trò Chơi Lịch Sử.
- **2.5.2.** Phim Lịch Sử.
- **2.5.3.** Cộng Đồng Văn Hóa.
- **2.5.4.** Hộ Chiếu Văn Hóa.
- **2.5.5.** Lịch & Sự Kiện.
- **2.5.6.** Bảo tàng số 3D.
- **2.5.7.** Bản đồ văn hóa.
- **2.5.8.** Giáo dục.

**Ghi chú:** Mockup ở `public-web/public-web-layout.md` còn có tính năng chuông thông báo (notification bell) chưa được đặc tả nghiệp vụ ở tài liệu này — nội dung thông báo cụ thể sẽ phụ thuộc vào các module tương tác/phát sinh sự kiện phát triển sau này (ví dụ Cộng Đồng Văn Hóa — 2.5.3, Lịch & Sự Kiện — 2.5.5). Sẽ làm rõ khi đặc tả các module đó.

### 2.6. Ứng dụng Web cho Người dùng công khai

- **2.6.1.** Là lớp giao diện frontend (website) phục vụ Người dùng công khai (mục 1.2.2, 2.1.3.2), sử dụng dữ liệu và tính năng đã có ở Bách Khoa Toàn Thư (mục 2.3) và AI Văn Minh Việt (mục 2.4) — không phải một module dữ liệu mới, không có thực thể/quy trình trạng thái riêng. Chỉ phục vụ xem/tra cứu và trò chuyện với AI; Người dùng công khai không có quyền tạo/sửa/xoá Mục từ hay bất kỳ dữ liệu nào của Cơ Sở Dữ Liệu Văn Hóa/Bách Khoa Toàn Thư (các thao tác đó thuộc về Nhân viên qua các vai trò ở mục 2.2.5 và 2.3.4, thực hiện ở backend). **Không bắt buộc đăng ký/đăng nhập tài khoản** để sử dụng — truy cập và dùng đầy đủ các tính năng ở mục 2.6.2–2.6.4 ngay, không cần tạo tài khoản.
- **2.6.2.** Duyệt & tìm kiếm Mục từ:
  - **2.6.2.1.** Tìm kiếm Mục từ theo từ khoá (tiêu đề, nội dung).
  - **2.6.2.2.** Duyệt/lọc Mục từ theo Cương vực (mục 2.3.6, danh sách cương vực ở mục 2.3.7).
  - **2.6.2.3.** Chỉ hiển thị các Mục từ đang có phiên bản được chọn để công khai (mục 2.3.2.4.1); Mục từ chưa từng được chọn phiên bản công khai thì không hiển thị.
- **2.6.3.** Trang chi tiết Mục từ: hiển thị nội dung theo cấu trúc trang wiki đã đặc tả ở mục 2.3.2.3 (dựng từ nội dung JSON dạng block, gồm các file đính kèm hình ảnh/âm thanh/phim nhúng trong nội dung).
- **2.6.4.** Trợ lý AI Văn Minh Việt:
  - **2.6.4.1.** Cho phép chọn Cương vực để giới hạn phạm vi trả lời (mục 2.4.3); nếu không chọn, AI trả lời trên toàn bộ Bách Khoa Toàn Thư.
  - **2.6.4.2.** Mỗi câu trả lời hiển thị kèm trích dẫn (các) Mục từ nguồn đã dùng để trả lời (mục 2.4.1); cho phép bấm vào trích dẫn để xem Mục từ gốc (mở màn hình ở mục 2.6.3).
  - **2.6.4.3.** Hội thoại của Người dùng công khai được lưu trên thiết bị của người dùng trong thời hạn giữ hội thoại (mục 2.4.6), không gắn với tài khoản hay định danh nào (nhất quán với mục 2.1.3.2). Hết thời hạn, hoặc khi dùng thiết bị hay trình duyệt khác, người dùng bắt đầu hội thoại mới.
- **2.6.5.** Đối tượng sử dụng: mọi Người dùng công khai theo mục 1.2.2, không phân theo tầng quyền nào khác, không cần tài khoản (mục 2.6.1) — nhất quán với mục 2.1.3.2 (một loại người dùng duy nhất) và mục 2.4.2.

### 2.7. Ứng dụng cho Nhân viên Tổ chức khác

- **2.7.1.** Là lớp giao diện backend dành riêng cho Nhân viên thuộc Tổ chức khác (viện nghiên cứu ngoài, mục 1.2.3.2) — khác với giao diện quản trị nội bộ đầy đủ dành cho Nhân viên thuộc Tổ chức Văn Minh Việt (mục 1.2.3.1). Không phải một module dữ liệu mới, không có thực thể/quy trình trạng thái riêng — sử dụng lại dữ liệu và nghiệp vụ đã có ở Cơ Sở Dữ Liệu Văn Hóa (mục 2.2).
- **2.7.2.** Phạm vi: chỉ cho phép thực hiện **vai trò Chủ nhiệm đề tài**, **vai trò Nghiên cứu** và **vai trò Xét duyệt** (mục 2.2.5.5, 2.2.5.2, 2.2.5.3) theo đúng Đề tài nghiên cứu được gán (mục 2.1.3.1.2, 2.2.1.4) — không có các vai trò theo chức năng khác (Nhập liệu, Xuất bản, Biên tập, Xét duyệt Mục từ, Quản trị hệ thống — mục 2.1.3.1.1). Riêng việc gán/thay đổi Nhân viên giữ vai trò Chủ nhiệm đề tài vẫn chỉ do Quản trị hệ thống thực hiện (mục 2.2.5.5), dù Chủ nhiệm đề tài đó thuộc Tổ chức nào.
- **2.7.3.** Các chức năng chính (theo vai trò được gán, giới hạn trong Đề tài của mình):
  - **2.7.3.1.** Truy cập Tư liệu gốc thuộc Đề tài (mục 2.2.1.3).
  - **2.7.3.2.** Nghiên cứu, biên tập Hạng mục tri thức và tạo tham chiếu tới Tư liệu gốc (mục 2.2.6.3–2.2.6.4), kể cả nghiên cứu lại sau khi "Không đạt xét duyệt".
  - **2.7.3.3.** Xét duyệt Hạng mục tri thức (mục 2.2.6.8–2.2.6.10).
  - **2.7.3.4.** Chủ nhiệm đề tài: gán/gỡ Nhân viên vào vai trò Nghiên cứu và vai trò Xét duyệt của Đề tài mình phụ trách (mục 2.2.5.5).
  - **2.7.3.5.** Chủ nhiệm đề tài: xem tiến độ Đề tài mình phụ trách — thống kê số Hạng mục tri thức theo trạng thái và danh sách Hạng mục tri thức kèm Tiêu đề, trạng thái, Người phụ trách hiện tại, Người tạo (mục 2.2.5.5); xoá Hạng mục tri thức đủ điều kiện của đề tài đó (mục 2.2.3.14).
- **2.7.4.** Không có chức năng quản lý người dùng/phân quyền, không tạo/sửa Tổ chức — các thao tác này chỉ thực hiện được từ giao diện quản trị nội bộ (mục 1.2.3.1, 1.2.3.3), dù Nhân viên đó giữ vai trò gì.
- **2.7.5.** Đối tượng sử dụng: Nhân viên thuộc Tổ chức khác Văn Minh Việt (mục 1.2.3.2), đã được gán vai trò Chủ nhiệm đề tài, Nghiên cứu và/hoặc Xét duyệt của (các) Đề tài cụ thể — nhất quán với mục 2.1.3.1 và 2.2.5.

### 2.8. Cấu hình hệ thống

- **2.8.1.** Là chức năng của giao diện quản trị nội bộ (mục 1.2.3.1), **chỉ dành cho** Nhân viên giữ vai trò Quản trị hệ thống (mục 2.1.3.1.1). Chức năng này cho phép xem và điều chỉnh các tham số vận hành của hệ thống mà **không cần triển khai lại** phần mềm. Thay đổi có hiệu lực ngay cho các thao tác phát sinh sau khi lưu.
- **2.8.2.** Mỗi tham số có một giá trị mặc định. Quản trị hệ thống có thể sửa, hoặc **khôi phục về mặc định** từng tham số. Không có chức năng xem lịch sử hay quay về một giá trị trước đó khác giá trị mặc định; giá trị cũ tra cứu qua audit log (mục 2.8.3). Hệ thống kiểm tra tính hợp lệ trước khi lưu (giới hạn giá trị, ràng buộc giữa các tham số). Nếu có tham số không hợp lệ thì không lưu thay đổi nào của lần lưu đó.
- **2.8.3.** Mọi thay đổi cấu hình được ghi audit log (mục 3.1.2) kèm giá trị trước và sau khi đổi.
- **2.8.4.** Các nhóm tham số:
  - **2.8.4.1. AI Verification** (mục 2.2.6.5): chế độ kích hoạt **tự động** hoặc **thủ công**; danh sách role được kích hoạt thủ công, chọn trong vai trò Nghiên cứu, Xét duyệt, Chủ nhiệm đề tài (theo đúng đề tài của hạng mục) và Quản trị hệ thống. Ở chế độ thủ công, danh sách này không được rỗng. Đổi chế độ không tự xử lý lại các Hạng mục tri thức đang chờ: hạng mục đang ở "Chờ xét duyệt" khi chuyển từ thủ công sang tự động vẫn phải kích hoạt thủ công. Màn hình cấu hình cảnh báo điều này khi đổi chế độ.
  - **2.8.4.2. Tài khoản & bảo mật**: thời hạn đường dẫn mời và đường dẫn đặt lại mật khẩu (mục 2.1.5.5); thời hạn phiên đăng nhập; chính sách mật khẩu (mục 2.1.5.8); tạm khoá đăng nhập (mục 2.1.5.9).
  - **2.8.4.3. Email hệ thống**: tên và địa chỉ người gửi; **mẫu nội dung** email mời (mục 2.1.5.3) và email đặt lại mật khẩu (mục 2.1.5.4). Quản trị hệ thống được sửa **toàn bộ** tiêu đề và nội dung mẫu, có chèn các thông tin tự động (tên Nhân viên, đường dẫn, thời hạn đường dẫn, tên Tổ chức). Mẫu bắt buộc phải chứa đường dẫn. Có chức năng **xem trước** và **gửi thử** trước khi lưu.
  - **2.8.4.4. AI Văn Minh Việt** (mục 2.4): số lượt hỏi trước đó được dùng làm ngữ cảnh và thời hạn giữ hội thoại (mục 2.4.6); câu trả lời mặc định khi không có thông tin (mục 2.4.7); câu miễn trừ trách nhiệm (mục 2.4.8); thời hạn lưu nhật ký hỏi đáp (mục 2.4.9.4); bật/tắt và hạn mức chống lạm dụng cho kênh công khai (mục 3.1.6).
  - **2.8.4.5. Vận hành**: thời hạn lưu audit log (mục 3.1.2); ngưỡng chuyển tư liệu cũ sang lưu trữ lạnh; thời gian lưu thông tin tác vụ nền; và các tham số vận hành kỹ thuật khác do thiết kế kỹ thuật xác định.
- **2.8.5.** Danh sách tham số cụ thể, giá trị mặc định và giới hạn của từng tham số do thiết kế kỹ thuật quyết định. Danh sách có thể mở rộng khi phát sinh nhu cầu vận hành mới.

## 3. Yêu Cầu Phi Chức Năng

_Phần này đã được rà soát và chốt các quyết định nghiệp vụ chính cho giai đoạn đầu; một số thông số kỹ thuật rất chi tiết (ví dụ dung lượng lưu trữ hạ tầng cụ thể) vẫn để lại cho giai đoạn thiết kế kỹ thuật quyết định._

### 3.1. Bảo mật & quyền riêng tư dữ liệu

- **3.1.1.** Dữ liệu định danh cá nhân của công dân và Nhân viên (email, số điện thoại) cần được mã hoá lưu trữ, tuân thủ quy định pháp luật Việt Nam về bảo vệ dữ liệu cá nhân (hiện hành: Nghị định 13/2023/NĐ-CP và các văn bản thay thế/bổ sung sau này).
- **3.1.2.** Phân quyền truy cập dữ liệu backend theo role. Ghi log (audit trail) tối thiểu cho các hành động: đăng nhập/đăng xuất Nhân viên, tạm khoá đăng nhập do nhập sai mật khẩu và gỡ tạm khoá (mục 2.1.5.9), đổi mật khẩu (mục 2.1.5.10), nhập/gán Tư liệu gốc, thay đổi trạng thái Đề tài nghiên cứu, xoá Đề tài nghiên cứu, nghiên cứu, xét duyệt và thay đổi trạng thái Hạng mục tri thức, xoá Hạng mục tri thức, soạn thảo/xét duyệt/xuất bản Mục từ, tạo/sửa/xoá Cương vực (mục 2.3.7.5), thay đổi phân quyền/role của Nhân viên, vô hiệu hoá/kích hoạt lại tài khoản Nhân viên (mục 2.1.5.7), tạo/sửa Tổ chức, thay đổi cấu hình hệ thống (mục 2.8.3). Audit log lưu trữ tối thiểu **12 tháng**. Bản ghi quá thời hạn lưu được hệ thống **dọn định kỳ**. Thời hạn lưu do Quản trị hệ thống cấu hình (mục 2.8.4.5) và không được đặt dưới 12 tháng.
- **3.1.3.** Dữ liệu hệ thống — bao gồm dữ liệu cá nhân Nhân viên, Tư liệu gốc, nội dung Hạng mục tri thức và Mục từ — **bắt buộc lưu trữ trong lãnh thổ Việt Nam** (data residency). Hạ tầng/nhà cung cấp dịch vụ được chọn khi thiết kế kỹ thuật phải đáp ứng yêu cầu này.
- **3.1.4.** Dữ liệu truyền tải giữa client và hệ thống phải được mã hoá (TLS/HTTPS) trên mọi kênh (website, ứng dụng di động, backend).
- **3.1.5.** Xác thực đa yếu tố (MFA) **chưa bắt buộc** ở giai đoạn này cho bất kỳ vai trò nào, kể cả Quản trị hệ thống — Nhân viên đăng nhập bằng email/mật khẩu theo mục 2.1.5. Có thể xem xét bổ sung MFA cho các vai trò nhạy cảm ở giai đoạn sau.
- **3.1.6.** Trợ lý AI Văn Minh Việt trên Ứng dụng Web cho Người dùng công khai (mục 2.6.4) được truy cập ẩn danh, không cần tài khoản. Vì vậy hệ thống có sẵn cơ chế chống lạm dụng (rate limiting) nhằm hạn chế spam và lạm dụng chi phí vận hành AI. Giới hạn tính theo **địa chỉ IP**: số câu hỏi tối đa trong một khoảng thời gian. Quản trị hệ thống bật/tắt cơ chế và đặt hạn mức (mục 2.8.4.4). Khi mới triển khai, cơ chế ở trạng thái **tắt**. Khi cơ chế đang bật mà vượt hạn mức, hệ thống từ chối câu hỏi và báo người dùng thử lại sau. Người dùng truy cập chung một mạng (ví dụ trường học, cơ quan) dùng chung một hạn mức; điều này được chấp nhận ở giai đoạn này. Không định danh thiết bị ẩn danh.

### 3.2. Hiệu năng & khả năng mở rộng

- **3.2.1.** Hệ thống cần đáp ứng việc mở rộng số lượng đề tài nghiên cứu (hiện 210, tăng dần theo thời gian) và khối lượng tư liệu gốc (văn bản, hình ảnh, âm thanh, phim) ngày càng lớn. Giai đoạn đầu (ra mắt): tải đỉnh khoảng **50–100 request/giây** cho Ứng dụng Web cho Người dùng công khai (mục 2.6), có khả năng chịu burst ngắn hạn lên **200–300 request/giây** (ví dụ khi có sự kiện truyền thông/báo chí đưa tin) — tương ứng khoảng vài trăm nghìn lượt truy cập/tháng. Kiến trúc cần cho phép mở rộng theo chiều ngang (horizontal scaling) cho các giai đoạn sau khi lượng người dùng tăng dần theo thời gian; không cần đáp ứng ngay quy mô toàn dân (~100 triệu người) từ giai đoạn ra mắt.
- **3.2.2.** AI Văn Minh Việt và Trợ lý Tư liệu gốc (self-host AI) cần đáp ứng thời gian phản hồi phù hợp cho tương tác thời gian thực với người dùng. Mục tiêu giai đoạn đầu: AI Văn Minh Việt (mục 2.4) trả token đầu tiên trong **≤3 giây**, hoàn tất câu trả lời trong **≤15 giây** đối với câu hỏi thông thường (mốc 95th percentile). Trợ lý Tư liệu gốc (AI Verification nội bộ, mục 2.2.6.6) không yêu cầu thời gian thực nghiêm ngặt — xử lý theo hàng đợi, mục tiêu hoàn tất trong vài phút cho mỗi Hạng mục tri thức là chấp nhận được.
- **3.2.3.** Uptime mục tiêu giai đoạn đầu: **99.5%** (tối đa ~3,6 giờ downtime/tháng) cho Ứng dụng Web cho Người dùng công khai (mục 2.6) và AI Văn Minh Việt (mục 2.4). Hệ thống backend (Nhân viên) có thể chấp nhận mức downtime cao hơn, kể cả bảo trì ngoài giờ hành chính, do không phục vụ trực tiếp người dân.
- **3.2.4.** Số lượng Nhân viên sử dụng đồng thời (mục 1.2.1): dự kiến vài chục đến khoảng **200 người dùng đồng thời** ở giai đoạn đầu, tương ứng quy mô 210 đề tài nghiên cứu hiện có (mục 1.1.2).
- **3.2.5.** Dung lượng lưu trữ cụ thể cho khối lượng file media (văn bản, hình ảnh, âm thanh, phim) của Tư liệu gốc và Hạng mục tri thức chưa được ước tính ở giai đoạn đặc tả này — sẽ ước lượng khi thiết kế kỹ thuật hạ tầng lưu trữ, dựa trên khối lượng thực tế của 210 đề tài nghiên cứu hiện có (mục 1.1.2) và tốc độ bổ sung tư liệu theo thời gian.

### 3.3. Nền tảng đa kênh

- **3.3.1.** Website và ứng dụng di động (công dân) cần đồng bộ dữ liệu và trải nghiệm nhất quán.
- **3.3.2.** Hệ thống backend (nhân viên) là nền tảng riêng, không bắt buộc tối ưu cho thiết bị di động trừ khi có yêu cầu bổ sung.
- **3.3.3.** Ứng dụng di động cho công dân phát triển cho cả hai nền tảng **iOS và Android** ngay từ giai đoạn ra mắt (native hay cross-platform do thiết kế kỹ thuật quyết định công nghệ cụ thể).
- **3.3.4.** Website hỗ trợ các trình duyệt phổ biến hiện đại (Chrome, Safari, Firefox, Edge — 2 phiên bản gần nhất của mỗi trình duyệt); không cần hỗ trợ trình duyệt cũ đã ngừng được nhà sản xuất hỗ trợ.
- **3.3.5.** Ngôn ngữ: hệ thống (Bách Khoa Toàn Thư, AI Văn Minh Việt, giao diện) chỉ hỗ trợ **tiếng Việt** ở giai đoạn này. Hỗ trợ đa ngôn ngữ (ví dụ tiếng Anh, phục vụ mục tiêu quảng bá văn hóa ra thế giới) để lại xem xét ở giai đoạn sau — không thiết kế cấu trúc dữ liệu đa ngôn ngữ ngay từ đầu.
- **3.3.6.** Khả năng tiếp cận (accessibility/WCAG) cho website công khai **chưa đặt ra yêu cầu cụ thể** ở giai đoạn này.

### 3.4. Độ tin cậy & sao lưu

- **3.4.1.** Tư liệu gốc và nội dung Hạng mục tri thức là tài sản quan trọng, cần có cơ chế sao lưu và khôi phục dữ liệu. Giai đoạn đầu: **sao lưu hàng ngày**, mục tiêu **RPO 24 giờ / RTO 24 giờ** (tối đa mất dữ liệu 24 giờ, khôi phục xong trong tối đa 24 giờ khi có sự cố).

### 3.5. Kiểm duyệt nội dung

- **3.5.1.** Tạm chưa áp dụng do module Cộng Đồng Văn Hóa (nơi phát sinh nội dung do người dùng tạo, mục 2.5.3) đang ngoài phạm vi giai đoạn này. Sẽ bổ sung khi đặc tả module đó.
