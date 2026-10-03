# Changelog — PublicWeb

## 2026-09-28

- CR-20260928-01: đổi toàn bộ trích dẫn mục đặc tả `§...` sang dạng chuẩn `R-XXX-NNN (§...)`. Không đổi nội dung thiết kế. File: **public-web-layout.md** (21), **00-claude-instructions.md** (11).
- **public-web-layout.md**: ghi chú ⚠ đầu màn hình Chat AI (mục 4.2) trỏ về mục đặc tả hiện hành R-PUB-008/009; ngôn ngữ trả lời trỏ về R-NFR-020 thay cho mục chọn ngôn ngữ không còn trong đặc tả.

## 2026-09-29

- DC-20260929-04: gắn ID `D-PUB-001`–`D-PUB-009` cho màn hình 4.1–4.9, `D-PUB-010` cho mục 3 (Cấu trúc điều hướng), `D-PUB-011` cho 2.1 (Bảng màu), `D-PUB-012` cho 2.3 (Thành phần dùng chung); đổi trích dẫn mục trong cùng file sang `D-PUB-… (¶…)` / `¶N`. Không đổi nội dung thiết kế. File: **public-web-layout.md**, **00-claude-instructions.md** (mục 3 thêm quy ước ID; mục 1 sửa trích đặc tả thành R-PUB-001 (§2.6)).

## 2026-09-30

- DC-20260930-08: đổi tên `public-web-layout.md` → `public-web-design.md`. Không đổi nội dung. File: **00-claude-instructions.md** (cập nhật tên file); ngoài luồng: `common/requirements-design-sync.md`, `common/tools/check-requirement-refs.py`.
- DC-20260930-10: chuyển đặc tả sang website responsive 2 mức (hẹp < 1024px / rộng ≥ 1024px), chỉ website. Top Nav ngang cho màn hình rộng, bỏ status bar, quy tắc responsive chung ở ¶5, ngoại lệ ở 4.2–4.4, bảng đường dẫn URL, chia sẻ, hover/focus. File: **public-web-design.md** (1, 2.3, 3, 4.2, 4.3, 4.4, 5, 7), **00-claude-instructions.md** (3, 6).

## 2026-10-01

- DC-20261001-04: áp nhận diện của landing vanminhviet.org — bảng màu theo `main.css` (Accent `#C4171D`, thêm Accent đậm, vàng đồng, xanh rêu), font Be Vietnam Pro + Lora (H1/H2 Lora), thang bo góc 8/16/24/pill, ảnh minh hoạ thuỷ mặc tông sáng, logo theo landing. File: **public-web-design.md** (2, 2.1, 2.2, 2.3, 5, 6, ghi chú cuối), **00-claude-instructions.md** (6).
- DC-20261001-06: Trang chủ và điều hướng kiểu website.
  - Bỏ Bottom Tab Bar, Top App Bar và tab Cá nhân. Thay bằng Header 2 mức (menu chữ + mega menu "Khám phá thêm" ở màn hình rộng, nút menu ở màn hình hẹp) và Footer lấy từ landing.
  - Trang chủ gồm: Hero thuỷ mặc kèm ô hỏi AI và 3 câu hỏi gợi ý cố định, Hôm nay, Khám phá theo Cương vực, Mục từ nổi bật (4 Mục từ mới công khai gần nhất), Trợ lý AI, Sắp ra mắt.
  - "Top bar" ở 4.2–4.9 đổi thành "Vùng tiêu đề".
  - File: **public-web-design.md** (2.1, 2.3, 3, 4.1–4.9, 5, 6, 7), **00-claude-instructions.md** (6, 7).

## 2026-10-03

- DC-20261001-01, DC-20261001-03, DC-20261002-03: căn theo API nhóm `public`.
  - Card Mục từ dùng `cover_image`; không có ảnh bìa thì dùng Ảnh mặc định của Mục từ (thành phần mới ở 2.3, cũng là hình chia sẻ mặc định); `excerpt` null thì bỏ dòng trích đoạn.
  - Cương vực đầu tiên theo thứ tự gán (`cultural_domain_ids`), quy tắc chung ở 2.3.
  - Bộ lọc Cương vực ở 4.3 lấy động từ `public.listCulturalDomains`, chọn nhiều theo ngữ nghĩa OR.
  - Chat AI: dải ảnh minh hoạ lấy `cover_image` trong `citations` (tối đa 3, bấm mở Mục từ); thêm khối "Dữ liệu câu trả lời" theo sự kiện SSE kênh `public`, không có `self_audit`.
  - "Mục từ nổi bật" dùng `sort=latest&limit=4`, ẩn section khi chưa có Mục từ công khai.
  - File: **public-web-design.md** (2.3, 4.1, 4.2, 4.3, 4.4).
