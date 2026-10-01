# Thiết Kế Module: AI Văn Minh Việt (`/assistant`)

> Trạng thái: ¶1–6 đã chốt (lịch sử thay đổi ở `system-design/changelog.md`). Module cuối cùng theo thứ tự build (`00-claude-instructions.md` mục 4). Tên bảng/field/hàm nội bộ và path API dùng tiếng Anh (`00-claude-instructions.md` mục 6); giá trị nghiệp vụ (nếu có) dùng tiếng Việt không dấu.

## 1. Tổng quan module

- Module cuối trong chuỗi giá trị (R-KB-001 (§2.2) đặc tả gốc: `... → Trợ lý số → Sản phẩm → Đời sống`) — hiện thực AI Văn Minh Việt (R-AI-001 (§2.4)), self-host RAG dựa trên Bách Khoa Toàn Thư.
- Phụ thuộc vào module 04 (`/encyclopedia`): đọc nội dung phiên bản đang công khai, danh sách Cương vực của Mục từ, và danh sách Mục từ công khai theo Cương vực — qua 3 interface đã chốt ở D-SD04-013 (¶4.3) (`GetPublicVersion`, `ListPublicByScope`, `ListCulturalDomainsByEntry`) — chỉ đọc, không JOIN chéo. Chiều phụ thuộc một chiều (05 → 04) — `/encyclopedia` không import `/assistant`; việc kích hoạt re-index đi qua job queue, xem D-SD05-009 (¶4.3).
- Phụ thuộc vào AI Gateway (D-SD01-006 (¶6)) qua API nội bộ cho: sinh embedding, rewrite câu hỏi, LLM generate, self-audit pass.
- Đối tượng sử dụng: **tất cả người dùng** — cả Nhân viên và Người dùng công khai (R-AI-003 (§2.4.2)) — nên route chat mount ở cả `admin` và `public` (đã chốt ranh giới ở D-SD01-002 (¶2)). ⚠ **Không mount ở `partner`**: R-AI-003 (§2.4.2) đặc tả gốc chỉ nêu Nhân viên Văn Minh Việt và Người dùng công khai là đối tượng sử dụng, không nhắc Nhân viên Tổ chức khác; Nhân viên Tổ chức khác cần dùng AI Văn Minh Việt thì dùng chung route `public` như người dùng thường (ẩn danh, không gắn `asked_by_employee_id`) — đây là chủ đích, không phải khoảng trống thiết kế.
- Không có role riêng của module này (đặc tả R-AI-001 (§2.4) không giao vai trò nghiệp vụ nào cho AI Văn Minh Việt) — dùng lại `quan_tri_he_thong` cho việc rà soát log chất lượng.
- Hỗ trợ hội thoại nhiều lượt (multi-turn) — người dùng hỏi tiếp trong cùng một hội thoại, AI trả lời có ngữ cảnh các lượt trước đó ⚠ Đề xuất bổ sung (xem D-SD05-002 (¶2.2), D-SD05-005 (¶3.2), ¶6).

## 2. Mô hình dữ liệu

Tên bảng/field tiếng Anh, path API tiếng Anh (theo `00-claude-instructions.md` mục 6).

### 2.1. [D-SD05-001] `assistant_chunk` (đoạn nội dung đã đánh chỉ mục, phục vụ RAG)

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | |
| `entry_id` | UUID | FK → `entry.id` (module 04 — tham chiếu chéo module, khoá ngoại đơn thuần) |
| `entry_version_id` | UUID | FK → `entry_version.id` — gắn theo đúng phiên bản đã sinh ra đoạn này (R-ENC-010 (§2.3.2.4.1): một Mục từ có nhiều phiên bản, chỉ 1 là đang công khai tại một thời điểm) |
| `chunk_index` | int | Thứ tự đoạn trong phiên bản |
| `content_chunk` | text | Đoạn text đã cắt từ `content_plain_text` (D-SD04-002 (¶2.2)) |
| `embedding` | vector(N) | pgvector — N theo model embedding đã pin (`01` ¶9 ) |
| `cultural_domain_ids` | UUID[] | ⚠ Đề xuất bổ sung — bản sao (denormalize) Cương vực đang gán cho Mục từ tại thời điểm đánh chỉ mục, dùng lọc trực tiếp trong SQL khi truy hồi mà không JOIN chéo sang bảng `entry_cultural_domain` (module 04). Đồng bộ lại khi Cương vực của Mục từ thay đổi (D-SD05-009 (¶4.3)) |
| `is_active` | boolean | ⚠ Đề xuất bổ sung — chỉ `true` cho các đoạn thuộc phiên bản **đang công khai hiện tại** của Mục từ; khi phiên bản công khai đổi, đoạn của phiên bản cũ chuyển `false` (vô hiệu khỏi truy hồi) thay vì xoá — giữ lại phục vụ debug/audit |
| `token_count` | int (nullable) | ⚠ metadata, phục vụ theo dõi chi phí/hiệu năng |
| `created_at` | timestamptz | |

**Ràng buộc**: unique `(entry_version_id, chunk_index)`. Index HNSW/IVFFlat trên `embedding` (pgvector) + GIN trên `to_tsvector(content_chunk)` cho hybrid search (D-SD05-005 (¶3.2)).

### 2.2. [D-SD05-002] `assistant_conversation` (hội thoại nhiều lượt — multi-turn, ⚠ Đề xuất bổ sung, xem ¶6)

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | Do **client tự sinh** (không do server cấp phát) — client gửi kèm ngay từ lượt hỏi đầu tiên của một hội thoại mới; server upsert khi gặp `id` chưa tồn tại |
| `channel` | text | `admin` / `public`, phân biệt hội thoại của Nhân viên hay Người dùng công khai (R-AI-003 (§2.4.2): cùng 1 module phục vụ cả 2 kênh). Cố định từ lượt hỏi đầu tiên, áp dụng cho mọi lượt trong hội thoại |
| `asked_by_employee_id` | UUID (nullable) | FK → `employee.id`. Chỉ có giá trị khi hội thoại thuộc kênh `admin`. `NULL` với kênh `public` (ẩn danh, không có định danh — R-GEN-007 (§1.2.2)). Cố định từ lượt hỏi đầu tiên |
| `started_at` | timestamptz | |
| `last_message_at` | timestamptz | Cập nhật mỗi khi có lượt hỏi mới trong hội thoại |
| `turn_count` | int | ⚠ Đề xuất bổ sung — đếm số lượt hỏi-đáp, tiện hiển thị/rà soát ở `assistant/query-logs` |

**Index** (⚠ bổ sung, phục vụ filter ở D-SD05-013 (¶5.2)): index trên `channel` và trên `asked_by_employee_id`.

### 2.3. [D-SD05-003] `assistant_query_log` (R-AI-002 (§2.4.1), D-SD01-006 (¶6)  bước 5 "Log & feedback")

| Field | Kiểu | Ghi chú |
|---|---|---|
| `id` | UUID | |
| `conversation_id` | UUID | FK → `assistant_conversation.id`, `ON DELETE CASCADE` (dọn theo hội thoại, D-SD05-006 (¶3.3)) — mỗi lượt hỏi thuộc đúng 1 hội thoại (xem D-SD05-002 (¶2.2), ¶6) |
| `turn_index` | int | Thứ tự lượt trong hội thoại, bắt đầu từ 0 |
| `asked_at` | timestamptz | |
| `cultural_domain_id` | UUID (nullable) | Bộ lọc Cương vực dùng khi hỏi (R-AI-004 (§2.4.3)); `NULL` nếu không chọn (trả lời trên toàn bộ Bách khoa) |
| `question` | text | Câu hỏi gốc do người dùng nhập |
| `rewritten_question` | text (nullable) | ⚠ Đề xuất bổ sung — câu hỏi đã viết lại (self-contained) dùng cho bước Retrieve khi hội thoại đã có lượt trước đó (D-SD05-005 (¶3.2), ¶6); `NULL` ở lượt đầu tiên (không cần rewrite) |
| `answer` | text | |
| `cited_entry_ids` | UUID[] | R-AI-002 (§2.4.1)/R-PUB-010 (§2.6.4.2) — các Mục từ được trích dẫn kèm câu trả lời |
| `self_audit_flags` | JSONB (nullable) | Kết quả bước self-audit (D-SD01-006 (¶6)  bước 4) — danh sách phát biểu trong câu trả lời chưa được chứng thực bởi đoạn đã truy hồi |
| `created_at` | timestamptz | |

**Ràng buộc**: unique `(conversation_id, turn_index)`.

**Index** (⚠ bổ sung, phục vụ filter ở D-SD05-013 (¶5.2)): partial index `WHERE jsonb_array_length(self_audit_flags) > 0` cho filter `has_self_audit_flags`. Quy ước giá trị `self_audit_flags`: `NULL` = chưa kiểm được (bước self-audit lỗi/timeout, D-SD05-005 (¶3.2) bước 4), `[]` = đã kiểm, không có cờ.

- Không có bảng `assistant_feedback` riêng — đặc tả gốc chỉ nói "lưu câu hỏi/đáp/nguồn để chuyên gia rà soát chất lượng sau này" (D-SD01-006 (¶6)  bước 5), chưa mô tả cơ chế feedback tường minh (like/dislike...) — để ngỏ, xem ¶6.
- Hỗ trợ hội thoại nhiều lượt (multi-turn) qua `conversation_id`/`turn_index` — xem D-SD05-002 (¶2.2), D-SD05-005 (¶3.2), ¶6.
- Kênh hỏi (`channel`) và người hỏi (`asked_by_employee_id`) là thuộc tính của cả hội thoại, lưu ở `assistant_conversation` (D-SD05-002 (¶2.2)) và không lặp lại trên từng lượt. Khi cần lọc hoặc hiển thị theo kênh/người hỏi thì JOIN qua `conversation_id` (cùng package `/assistant`, không phải JOIN chéo module).
- Lưu có thời hạn (R-AI-014 (§2.4.9.4)): hội thoại có `last_message_at` quá `assistant.query_log_retention_days` (mặc định 180 ngày) bị xoá cùng toàn bộ lượt hỏi–đáp của nó — D-SD05-006 (¶3.3). Lượt hỏi kênh `public` không lưu định danh hay địa chỉ IP người hỏi (R-AI-011 (§2.4.9.1)).

## 3. Luồng nghiệp vụ

### 3.1. [D-SD05-004] Đánh chỉ mục (Indexing) — job nền

Kích hoạt bởi sự kiện từ `/encyclopedia` (module 04), qua hàng đợi job (river, enqueue cùng transaction — D-SD01-001 (¶1), D-SD01-004 (¶4)) — **không** gọi hàm trực tiếp giữa 2 package theo chiều 04→05 (module 05 chỉ được phép phụ thuộc *vào* module 04, không ngược lại, theo thứ tự build `00-claude-instructions.md` mục 4). Cụ thể:

1. `/encyclopedia.SetPublicVersion` (đã chốt ở D-SD04-014 (¶4.4)), sau khi cập nhật `entry.current_public_version_id` thành công trong cùng transaction, enqueue job `assistant.reindex_entry` với payload `{entry_id}` — enqueue chỉ cần biết tên job + payload, không import package `/assistant` (cùng nguyên tắc `/gate` enqueue job cho `/verification` ở module 03).
2. `/encyclopedia.AssignCulturalDomain`/`UnassignCulturalDomain` (đã chốt ở D-SD04-014 (¶4.4)) enqueue job `assistant.refresh_domain_tags` với payload `{entry_id}` — chỉ cập nhật `cultural_domain_ids` trên các `assistant_chunk` đang `is_active = true` của Mục từ đó, không tính lại embedding.
3. Job `assistant.reindex_entry` (worker trong `/assistant`, `/cmd/worker`):
   - Đọc phiên bản đang công khai qua `encyclopedia.GetPublicVersion(entryID)`.
   - Nếu không còn phiên bản công khai (`current_public_version_id = NULL`, ví dụ vừa bị mở lại): đặt `is_active = false` cho mọi `assistant_chunk` của `entry_id`, dừng.
   - Nếu đã có `assistant_chunk` cho đúng `entry_version_id` này: chỉ cần đặt `is_active = true` cho các dòng đó, `is_active = false` cho các dòng thuộc `entry_version_id` khác cùng `entry_id` (⚠ hệ quả kỹ thuật đã nêu ở D-SD01-006 (¶6) — "re-index khi con trỏ đổi, kể cả quay lại phiên bản cũ hơn": ở đây tái sử dụng chunk cũ nếu đã có sẵn, không sinh lại embedding).
   - Nếu chưa có: cắt đoạn (`content_plain_text` của `entry_version`) thành các `content_chunk`, gọi AI Gateway (D-SD01-006 (¶6) ) sinh `embedding` cho từng đoạn, insert `assistant_chunk` mới với `is_active = true`, đồng thời set `is_active = false` cho các dòng của `entry_version_id` khác.
4. Job `assistant.refresh_domain_tags`: đọc lại danh sách Cương vực hiện tại của Mục từ qua `encyclopedia.ListCulturalDomainsByEntry(entryID)` (D-SD04-013 (¶4.3)), cập nhật `cultural_domain_ids` trên mọi `assistant_chunk` đang `is_active = true` của `entry_id`.

### 3.2. [D-SD05-005] Trả lời câu hỏi (Chat) — hội thoại nhiều lượt (multi-turn), theo D-SD01-006 (¶6)

0. **Xác định hội thoại** — request kèm `conversation_id` (do client tự sinh, xem D-SD05-012 (¶5.1), ¶6). Nếu `conversation_id` chưa tồn tại trong `assistant_conversation`: insert mới (`channel` và `asked_by_employee_id` theo nhóm route gọi vào, `started_at = now()`, `turn_count = 0`). Nếu đã tồn tại: ⚠ kiểm tra `channel` và `asked_by_employee_id` của hội thoại phải khớp với request hiện tại (cùng kênh; với kênh `admin` thì phải cùng Nhân viên). Nếu không khớp, trả sự kiện `error` với `error_code = conversation_mismatch` rồi dừng: không đọc lịch sử, không ghi log. Client sinh `conversation_id` mới để bắt đầu hội thoại mới. Sau đó đọc N lượt gần nhất (N = `assistant.history_turns`, mặc định 6 — `07-system-settings.md`; N = 0 thì không đọc lịch sử, mỗi lượt hỏi xử lý như lượt đầu tiên) từ `assistant_query_log` theo `conversation_id`, sắp theo `turn_index` giảm dần, làm lịch sử hội thoại cho các bước dưới. Lượt hỏi đầu tiên của một hội thoại mới không có lịch sử.
1. **Rewrite query** ⚠ Đề xuất bổ sung — nếu `assistant.rewrite_query_enabled = true` và hội thoại đã có lịch sử (không phải lượt đầu tiên): gọi AI Gateway `gateway.rewriteQuery` — `POST /v1/rewrite-query` (D-SD06-005 (¶3.3)), truyền câu hỏi hiện tại + N lượt gần nhất, nhận về câu hỏi độc lập (self-contained), lưu vào `rewritten_question`. Lượt đầu tiên: bỏ qua bước này, dùng thẳng `question` gốc cho bước Retrieve. Tắt Rewrite → dùng thẳng `question` gốc cho Retrieve ở mọi lượt.
2. **Retrieve** — hybrid search trên `assistant_chunk` (chỉ `is_active = true`): kết hợp vector similarity (`embedding`) + full-text (`content_chunk`) trên câu hỏi đã rewrite ở bước 1 (hoặc câu hỏi gốc nếu là lượt đầu tiên); lọc `cultural_domain_id = ANY(cultural_domain_ids)` nếu người dùng chọn Cương vực (R-AI-004 (§2.4.3)), bỏ lọc nếu không chọn (R-AI-004 (§2.4.3): "trả lời trên toàn bộ Bách khoa"). Lấy top-K đoạn liên quan nhất (K = `assistant.retrieve_top_k`, mặc định 8 — `07-system-settings.md`). Nếu không truy hồi được đoạn nào (ví dụ Cương vực đã chọn chưa có Mục từ nào được đánh chỉ mục): bỏ qua bước 3–4, stream nguyên văn `assistant.no_context_answer` qua sự kiện `token`, `citations` rỗng, `self_audit` là `[]`, rồi tiếp tục bước 6 (vẫn ghi log). Sau khi có top-K, gọi `encyclopedia.GetEntryTitles` (D-SD04-013 (¶4.3)) cho các `entry_id` riêng biệt để gắn `title` vào `context_chunks` gửi AI Gateway (D-SD06-004 (¶3.2)).
3. **Generate** — gọi AI Gateway (LLM), dựa trên các đoạn đã truy hồi ở bước 2 **và lịch sử hội thoại** (bước 0) làm ngữ cảnh, sinh câu trả lời kèm danh sách Mục từ nguồn (`cited_entry_ids`) — đúng R-AI-002 (§2.4.1), R-AI-005 (§2.4.4) (giới hạn trong phạm vi tri thức Bách khoa, không trả lời ngoài phạm vi). Truyền kèm `no_answer_text = assistant.no_context_answer` để LLM dùng đúng câu này khi các đoạn truy hồi không đủ thông tin trả lời (D-SD06-004 (¶3.2)).
4. **Self-audit pass** — gọi AI Gateway lần nữa (model khác hoặc cùng model, vai trò kiểm tra), rà lại câu trả lời so với các đoạn đã truy hồi, gắn cờ phát biểu chưa được chứng thực (`self_audit_flags`) — không chặn trả lời, chỉ gắn cờ để hiển thị cảnh báo hoặc phục vụ rà soát sau. Chạy **sau khi** phần Generate đã stream xong cho người dùng. Lỗi/timeout ở bước này không làm hỏng lượt hỏi: ghi `self_audit_flags = NULL` (chưa kiểm được), vẫn tiếp tục bước 5–6.
5. **Trả lời cho người dùng** — trả dạng streaming SSE (đã chốt ở D-SD01-003 (¶3), đáp ứng NFR token đầu ≤3s — D-SD01-008 (¶8)/R-NFR-011 (§3.2.2), xem rủi ro độ trễ do bước Rewrite ở ¶6), kèm trích dẫn Mục từ nguồn để người dùng bấm xem (R-PUB-010 (§2.6.4.2)). Thứ tự sự kiện: `token` trong lúc Generate → `citations` khi Generate xong (tiêu đề đã có từ bước 2) → `self_audit` sau bước 4 → `done` sau bước 6 — hợp đồng chi tiết ở D-SD05-012 (¶5.1).
6. **Log & feedback** — sau khi trả lời xong: ghi 1 dòng `assistant_query_log` (D-SD05-003 (¶2.3)) với `conversation_id`/`turn_index` đúng hội thoại; cập nhật `last_message_at = now()`, `turn_count += 1` trên `assistant_conversation` (D-SD05-002 (¶2.2)). Nếu lỗi xảy ra trước khi Generate hoàn tất (gửi sự kiện `error`), lượt hỏi không được ghi log và `turn_count` không tăng.

### 3.3. [D-SD05-006] Dọn nhật ký hỏi đáp quá hạn — job nền

- Periodic job `assistant.query_log_cleanup` (river, chạy mỗi ngày — D-SD01-004 (¶4)) đọc `assistant.query_log_retention_days` (`07-system-settings.md`) tại thời điểm chạy.
- Xoá theo lô các `assistant_conversation` có `last_message_at < now() - N ngày`, cùng các dòng `assistant_query_log` thuộc hội thoại đó (FK `ON DELETE CASCADE` từ `assistant_query_log.conversation_id`).
- Dọn theo cả hội thoại, không theo từng lượt, để không để lại hội thoại bị mất lượt giữa chừng.
- Không ghi audit log (D-SD01-002 (¶2), "Không ghi audit").
- Client đang giữ `conversation_id` của hội thoại đã bị xoá: thời hạn lưu (≥ 30 ngày) luôn dài hơn thời hạn giữ hội thoại phía client (`assistant.conversation_ttl_hours`, tối đa 168 giờ), nên trường hợp này thực tế không xảy ra. Nếu xảy ra, `GetOrCreateConversation` tạo hội thoại mới với đúng `id` đó.

## 4. Kiến trúc riêng của module

### 4.1. [D-SD05-007] Sở hữu bảng

| Package | Bảng sở hữu |
|---|---|
| `/assistant` | `assistant_chunk`, `assistant_conversation`, `assistant_query_log` |

### 4.2. [D-SD05-008] Interface gọi sang `/encyclopedia` (đã chốt ở D-SD04-013 (¶4.3))

```go
package encyclopedia
func GetPublicVersion(ctx context.Context, entryID uuid.UUID) (*EntryVersion, error)
func ListPublicByScope(ctx context.Context, culturalDomainID *uuid.UUID, cursor string) ([]EntrySummary, string, error)
func ListCulturalDomainsByEntry(ctx context.Context, entryID uuid.UUID) ([]CulturalDomain, error)
func GetEntryTitles(ctx context.Context, entryIDs []uuid.UUID) (map[uuid.UUID]EntryTitle, error)
```

`ListPublicByScope` dùng cho job quét toàn bộ Mục từ đang công khai khi cần tái đánh chỉ mục hàng loạt (ví dụ đổi model embedding — ¶6). `ListCulturalDomainsByEntry` dùng cho job `refresh_domain_tags` (D-SD05-004 (¶3.1) bước 4) — ⚠ bổ sung 2026-09-23, trước đó D-SD05-004 (¶3.1) đã mô tả job này "đọc lại Cương vực qua interface đọc của `/encyclopedia`" nhưng D-SD04-013 (¶4.3) chưa có hàm tương ứng. `GetEntryTitles` dùng ở bước Retrieve (D-SD05-005 (¶3.2) bước 2) và khi ghép `cited_entries` cho API rà soát (D-SD05-013 (¶5.2)).

### 4.3. [D-SD05-009] Cơ chế kích hoạt re-index — qua job queue, không phụ thuộc ngược

- D-SD04-014 (¶4.4) enqueue 2 job: `SetPublicVersion` enqueue `assistant.reindex_entry`; `AssignCulturalDomain`/`UnassignCulturalDomain` enqueue `assistant.refresh_domain_tags`.
- Lý do dùng job queue thay vì gọi hàm trực tiếp: giữ đúng chiều phụ thuộc một chiều 05 → 04 đã chốt ở thứ tự build (`00-claude-instructions.md` mục 4) — `/encyclopedia` không được import `/assistant`.

### 4.4. [D-SD05-010] Các hàm chính trong `/assistant`

```go
package assistant

// Job handlers (đăng ký ở /cmd/worker)
func ReindexEntry(ctx context.Context, entryID uuid.UUID) error
func RefreshDomainTags(ctx context.Context, entryID uuid.UUID) error
func CleanupExpiredQueryLogs(ctx context.Context) error // periodic, D-SD05-006 (¶3.3)

// Orchestration cho endpoint chat (D-SD05-005 (¶3.2))
func GetOrCreateConversation(ctx context.Context, tx pgx.Tx, conversationID uuid.UUID, channel string, employeeID *uuid.UUID) (*Conversation, error)
func GetRecentHistory(ctx context.Context, conversationID uuid.UUID, limitTurns int) ([]Turn, error)
func RewriteQuery(ctx context.Context, question string, history []Turn) (rewritten string, err error)
func Retrieve(ctx context.Context, question string, culturalDomainID *uuid.UUID, topK int) ([]ChunkResult, error)
func GenerateAnswer(ctx context.Context, question string, chunks []ChunkResult, history []Turn) (answer string, citedEntryIDs []uuid.UUID, err error)
func SelfAudit(ctx context.Context, answer string, chunks []ChunkResult) ([]UnverifiedClaim, error)
func LogQuery(ctx context.Context, tx pgx.Tx, log AssistantQueryLog) error
```

`Turn` = 1 cặp câu hỏi-trả lời trong lịch sử hội thoại (đọc từ `assistant_query_log`, sắp theo `turn_index`).

`GetOrCreateConversation` thực hiện cả việc kiểm tra `channel`/`employeeID` khớp với hội thoại đã có (D-SD05-005 (¶3.2) bước 0). Nếu không khớp thì trả lỗi `conversation_mismatch`.

### 4.5. [D-SD05-011] AI Gateway — 4 điểm gọi

Theo D-SD01-006 (¶6) và hợp đồng cụ thể ở `06-ai-gateway.md`:

- sinh `embedding` (bước indexing) — `gateway.embed` — `POST /v1/embed`;
- **Rewrite query** (bước mới cho multi-turn, D-SD05-005 (¶3.2) bước 1) — **endpoint riêng `gateway.rewriteQuery` — `POST /v1/rewrite-query`** (D-SD06-005 (¶3.3)): dùng chung LLM với Generate nhưng khác prompt và khác kiểu trả (JSON một lần, không streaming), nên tách endpoint riêng cho đúng hợp đồng — cùng lý do `gateway.selfAudit` được tách khỏi `gateway.generate`;
- `Generate` (LLM trả lời) — `gateway.generate` — `POST /v1/generate`, streaming SSE;
- `Self-audit` (LLM kiểm tra lại) — `gateway.selfAudit` — `POST /v1/self-audit`.

Cả 4 qua cùng AI Gateway (API nội bộ REST, D-SD06-001 (¶1)), hỗ trợ 3 chế độ backend (`mock`/`cpu-small`/`gpu-onprem`) để phát triển local không cần GPU.

## 5. Thiết kế API

### 5.1. [D-SD05-012] Chat — mount ở cả `admin` và `public` (R-AI-003 (§2.4.2): phục vụ cả Nhân viên lẫn Người dùng công khai)

| Method | Path | operationId | Mô tả | Xác thực |
|---|---|---|---|---|
| POST | `/assistant/chat` | `assistant.chat` | Đặt câu hỏi — body `{question, conversation_id, cultural_domain_id?}`. Response: SSE gồm các sự kiện có tên (bảng dưới) — chốt ở D-SD01-003 (¶3) | Admin: JWT (ghi `asked_by_employee_id`). Public: không |

**Hợp đồng sự kiện SSE** (⚠ Bổ sung — dùng chung cho kênh `admin` và `public`):

| `event` | `data` | Thời điểm |
|---|---|---|
| `token` | `{text}` | Lặp lại trong lúc Generate stream (relay từ `delta` của `gateway.generate`) |
| `citations` | `{items: [{entry_id, title, cover_image}]}` | Một lần, khi Generate xong. `title` là tiêu đề phiên bản đang công khai (`GetEntryTitles`). ⚠ `cover_image` — `{file_id, url, url_expires_at}` ảnh đại diện phiên bản công khai (`GetPublicCoverImages`, D-SD04-013 (¶4.3)) hoặc `null`; dùng cho dải ảnh minh hoạ dưới câu trả lời ở Web công khai. Cùng dữ liệu ở cả 2 kênh |
| `self_audit` | `{flags: [{claim_text, reason}] \| null}` | Một lần, sau bước Self-audit. Cùng schema `flags` của `gateway.selfAudit` (D-SD06-006 (¶3.4)). `[]` = không có cờ; `null` = không kiểm được (lỗi/timeout) |
| `done` | `{query_log_id, turn_index}` | Một lần, sau khi ghi `assistant_query_log` (D-SD05-005 (¶3.2) bước 6) — sự kiện cuối của lượt hỏi thành công |
| `error` | `{error_code, message, trace_id}` | Bất kỳ lúc nào; stream kết thúc ngay sau sự kiện này. Định dạng theo quy ước lỗi chung (D-SD01-003 (¶3), D-SD06-012 (¶6)) |

Nếu lỗi xảy ra sau khi đã gửi `citations`, client giữ nguyên phần câu trả lời đã hiển thị và thông báo lỗi.

- **Rate limit kênh `public`** (R-NFR-008 (§3.1.6)): khi bật (`assistant.public_rate_limit_enabled`), request vượt ngưỡng bị từ chối **trước khi** mở stream SSE — HTTP 429, body lỗi JSON theo quy ước chung (`error_code = rate_limited`), header `Retry-After`; không tạo/ghi hội thoại. Cơ chế ở D-SD07-009 (¶4.3). Kênh `admin` không áp dụng.
- **Câu miễn trừ trách nhiệm và thời hạn hội thoại phía client**: frontend đọc `assistant.disclaimer_text` và `assistant.conversation_ttl_hours` qua `clientSettings.getSettings` — `GET /client-settings`.

- Cùng 1 path `/assistant/chat`, mount riêng dưới `/api/v1/admin/...` và `/api/v1/public/...` — handler dùng chung logic (D-SD05-005 (¶3.2)), chỉ khác `channel`/`asked_by_employee_id` gắn theo nhóm route gọi vào.
- **Không mount ở `/api/v1/partner/...`**: Nhân viên Tổ chức khác dùng AI Văn Minh Việt qua route `public` như người dùng thường, không có trải nghiệm chat xác thực riêng theo tổ chức.
- Danh sách Cương vực để hiển thị bộ lọc: dùng lại `encyclopedia.listCulturalDomains` — `GET /encyclopedia/cultural-domains` (admin — mở cho mọi Nhân viên đã đăng nhập, D-SD04-017 (¶5.3)) / `public.listCulturalDomains` (public) đã có ở D-SD04-017 (¶5.3)/D-SD04-018 (¶5.4) — không tạo endpoint trùng.
- **`conversation_id`** (UUID) do client tự sinh và tự quản lý (không do server cấp phát) — bắt buộc trong body ở mọi request, kể cả lượt hỏi đầu tiên của một hội thoại mới (client tự sinh UUID mới cho hội thoại mới). Server dùng để nhóm các lượt hỏi thành 1 hội thoại (D-SD05-002 (¶2.2)), đọc lịch sử N lượt gần nhất phục vụ bước Rewrite/Generate (D-SD05-005 (¶3.2)). Hỗ trợ hội thoại nhiều lượt (multi-turn) — xem ¶6. Một `conversation_id` gắn cố định với kênh và người hỏi của lượt đầu tiên. Nếu dùng lại ở kênh khác, hoặc bởi Nhân viên khác, server trả `error` `conversation_mismatch` (D-SD05-005 (¶3.2) bước 0).

### 5.2. [D-SD05-013] Nhóm `assistant/*` — chỉ mount `admin` (rà soát chất lượng, role `quan_tri_he_thong`)

| Method | Path | operationId | Mô tả |
|---|---|---|---|
| GET | `/assistant/query-logs` | `assistant.listQueryLogs` | Danh sách log hỏi–đáp (filter `channel`, `cultural_domain_id`, `conversation_id`, `asked_by_employee_id`, `has_self_audit_flags`, khoảng thời gian) — cursor pagination |
| GET | `/assistant/query-logs/{id}` | `assistant.getQueryLog` | Chi tiết 1 lượt hỏi–đáp (câu hỏi/trả lời/trích dẫn/cờ self-audit) |
| GET | `/assistant/conversations/{id}` | `assistant.getConversation` | ⚠ Đề xuất bổ sung — xem toàn bộ các lượt hỏi–đáp trong 1 hội thoại, sắp theo `turn_index`, phục vụ rà soát ngữ cảnh multi-turn |
| POST | `/assistant/reindex/{entry_id}` | `assistant.reindexEntry` | ⚠ Đề xuất bổ sung — kích hoạt lại thủ công job `reindex_entry` cho 1 Mục từ (khắc phục sự cố/đổi model embedding) |

**Response bổ sung** (⚠ Bổ sung — hoàn thiện kỹ thuật cho màn hình rà soát D-ADM-024 (¶4.24)–D-ADM-025 (¶4.25)):

- Mỗi lượt hỏi–đáp (ở cả 3 endpoint `GET`) trả thêm `asked_by: {id, display_name, email} | null` (`null` với kênh `public`) và `cited_entries: [{entry_id, title, is_public}]` (qua `GetEntryTitles`; `is_public = false` khi Mục từ không còn công khai — `title` khi đó là tiêu đề phiên bản đã chốt mới nhất).
- Filter `channel` và `asked_by_employee_id` ở `assistant.listQueryLogs` — `GET /assistant/query-logs` lọc qua JOIN `assistant_query_log.conversation_id → assistant_conversation` (D-SD05-003 (¶2.3)). `asked_by` của mỗi lượt lấy theo hội thoại chứa lượt đó.
- Riêng `assistant.listQueryLogs` — `GET /assistant/query-logs` (danh sách) trả thêm `self_audit_flag_count` (int, `null` nếu `self_audit_flags` là `NULL`).
- `assistant.getConversation` — `GET /assistant/conversations/{id}`: `asked_by` trả một lần ở cấp hội thoại.
- Tên/email Nhân viên ghép ở **tầng handler HTTP** (`/cmd/api`) bằng `identity.GetEmployeeSummaries` (D-SD02-008 (¶4)), tiêu đề Mục từ bằng `encyclopedia.GetEntryTitles` — cùng cách đã áp dụng cho `shared.listAuditLogs` — `GET /shared/audit-logs`. Không đổi schema `assistant_query_log`, không JOIN chéo, không phát sinh import cycle.

## 6. Vấn đề mở / giả định

- **Rate limiting cho `assistant.chat` (kênh `public`)** hiện thực R-NFR-008 (§3.1.6): theo IP, Quản trị hệ thống bật/tắt và đặt hạn mức, mặc định tắt. ⚠ Cách làm — middleware Go, bộ đếm trong bộ nhớ tiến trình — là quyết định kỹ thuật (D-SD07-009 (¶4.3)).
- **Rà soát nhật ký hỏi đáp** (D-SD05-013 (¶5.2)) do role `quan_tri_he_thong` thực hiện (R-AI-012 (§2.4.9.2)).
- **`is_active`/`cultural_domain_ids` denormalize trên `assistant_chunk`** (D-SD05-001 (¶2.1)) — ⚠ giải pháp kỹ thuật để tránh JOIN chéo sang `/encyclopedia` khi truy hồi, đổi lại phải đồng bộ qua job mỗi khi phiên bản công khai/Cương vực thay đổi (D-SD05-004 (¶3.1), D-SD05-009 (¶4.3)).
- **Hội thoại nhiều lượt** hiện thực R-AI-007 (§2.4.6), R-PUB-011 (§2.6.4.3). Các quyết định kỹ thuật đi kèm:
  - `conversation_id` do client tự sinh (UUID) và tự quản lý (ví dụ lưu `localStorage` phía public-web/app) — server không cấp phát, không cần thêm cơ chế session/cookie hay định danh thiết bị ẩn danh riêng ở tầng ứng dụng (nhất quán với quyết định ở bullet rate limiting phía trên).
  - Lịch sử hội thoại giới hạn N lượt gần nhất, dùng cho cả bước Rewrite query và Generate (D-SD05-005 (¶3.2)) — N là tham số cấu hình `assistant.history_turns` (`07-system-settings.md`).
  - Có bước Rewrite query (gọi AI Gateway `gateway.rewriteQuery` — `POST /v1/rewrite-query`, D-SD06-005 (¶3.3)) trước Retrieve khi hội thoại đã có lượt trước đó, để xử lý câu hỏi nối tiếp phụ thuộc ngữ cảnh (ví dụ "còn về X thì sao?"). ⚠ Cập nhật 2026-09-23: trước đó tài liệu ghi "dùng chung endpoint Generate, đổi prompt", nhưng schema của `gateway.generate` (`{question, context_chunks}`) không có chỗ truyền lịch sử hội thoại — nay tách thành endpoint riêng, cùng khuôn với `gateway.selfAudit` (cũng dùng chung LLM nhưng là endpoint riêng).
  - Mô hình dữ liệu: bảng `assistant_conversation` riêng (D-SD05-002 (¶2.2)) lưu metadata hội thoại, gồm cả `channel` và `asked_by_employee_id`. `assistant_query_log` (D-SD05-003 (¶2.3)) lưu từng lượt với `conversation_id`, `turn_index`, `rewritten_question`.
- **Ràng buộc hội thoại theo kênh/người hỏi** ⚠ Đề xuất bổ sung — vì `conversation_id` do client tự sinh, server kiểm tra hội thoại đã có phải khớp kênh và Nhân viên với request (D-SD05-005 (¶3.2) bước 0). Việc này ngăn dùng `conversation_id` của hội thoại `admin` để đọc lịch sử qua kênh `public`, hoặc đọc hội thoại của Nhân viên khác. Riêng giữa các người dùng ẩn danh ở kênh `public` thì không phân biệt được. Ở đây chỉ dựa vào việc UUID khó đoán, nhất quán với quyết định không có định danh thiết bị ẩn danh (bullet rate limiting ở trên).
- **Rủi ro độ trễ do bước Rewrite query** ⚠ — bước Rewrite (D-SD05-005 (¶3.2) bước 1) thêm 1 lời gọi AI Gateway tuần tự trước Retrieve khi hội thoại đã có lịch sử, có thể ảnh hưởng NFR token đầu ≤3 giây (đặc tả gốc R-NFR-011 (§3.2.2), D-SD01-008 (¶8)) — cần đo đạc thực tế lúc code; có thể cân nhắc rút gọn prompt rewrite hoặc dùng model nhỏ/nhanh hơn cho riêng bước này nếu cần (timeout đề xuất cho endpoint này là 5s, D-SD06-012 (¶6)). Quản trị hệ thống có thể tắt bước này (`assistant.rewrite_query_enabled`) nếu đo thực tế không đạt NFR.
- **Không có chức năng đánh giá câu trả lời** (thích/không thích, báo sai) ở giai đoạn này (R-AI-013 (§2.4.9.3)).
- **Chunking strategy cụ thể** (kích thước đoạn, overlap, chiến lược cắt theo block JSON hay theo `content_plain_text`) — chi tiết kỹ thuật, chưa chốt số liệu cụ thể, để lại cho lúc code (tương tự các mục "chốt sau khi có số liệu thực tế" ở tài liệu 01).
- **Hợp đồng sự kiện SSE của `assistant.chat`** (D-SD05-005 (¶3.2), D-SD05-012 (¶5.1)) — ⚠ bổ sung: thứ tự `token` → `citations` → `self_audit` → `done`, cùng `error`; self-audit chạy sau khi đã stream câu trả lời; lỗi self-audit không làm hỏng lượt hỏi (`NULL` = chưa kiểm được); lỗi trước khi Generate xong thì không ghi log.
- **`asked_by`, `cited_entries`, `self_audit_flag_count` và 2 filter mới ở API rà soát** (D-SD05-003 (¶2.3), D-SD05-013 (¶5.2)) — ⚠ bổ sung: hoàn thiện kỹ thuật cho màn hình rà soát của Admin nội bộ; ghép dữ liệu ở tầng handler. Không đổi schema, không đổi hành vi nghiệp vụ.
- **Thời hạn lưu nhật ký hỏi đáp** (D-SD05-003 (¶2.3), D-SD05-006 (¶3.3)) hiện thực R-AI-014 (§2.4.9.4). ⚠ Mặc định 180 ngày và cách dọn theo cả hội thoại (không theo từng lượt) là quyết định của thiết kế.
