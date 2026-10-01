# Thiết Kế: AI Gateway (service Python riêng)

> Trạng thái: đã chốt — đang được `03-cultural-knowledge-base.md` (D-SD03-017 (¶4.2)–D-SD03-019 (¶4.4)) `05-ai-assistant.md` (D-SD05-011 (¶4.5)) và `04-encyclopedia.md` (D-SD04-020 (¶4.5)) tham chiếu tới các endpoint cụ thể.
>
> Tài liệu này **không theo cấu trúc chuẩn module 02–05** (`00-claude-instructions.md` mục 5), vì AI Gateway không phải một module nghiệp vụ ánh xạ 1-1 với đặc tả gốc — nó là service hạ tầng đã được quyết định kiến trúc ở D-SD01-006 (¶6) (self-host, GPU on-prem, vLLM + ASR riêng, 3 chế độ backend). Tài liệu này bổ sung phần D-SD01-006 (¶6) còn để ngỏ: **hợp đồng API cụ thể** giữa Go monolith (`/assistant` — tài liệu 05, `/verification` — tài liệu 03) và AI Gateway, cùng **kiến trúc nội bộ** của chính service Python này — đủ chi tiết để tự implement (không chỉ để Go gọi vào).

## 1. [D-SD06-001] Phạm vi & nguyên tắc

- AI Gateway phục vụ đúng 3 năng lực nghiệp vụ đã chốt ở D-SD01-006 (¶6): **RAG cho AI Văn Minh Việt** (module 05), **AI Verification đa phương thức** (module 03, R-KB-080 (§2.2.6.6)) và **sinh bản nháp nội dung Mục từ** (module 04, R-ENC-038 (§2.3.8)) — không phục vụ mục đích nào khác.
- **Không tự quyết định nghiệp vụ** (verdict cuối cùng ghi vào `claim_reference`/`claim`, quyết định trạng thái workflow...) — AI Gateway chỉ trả kết quả thô (verdict/note/embedding/answer) cho Go monolith; Go monolith (`/verification`, `/assistant`, `/encyclopedia`) chịu trách nhiệm ghi dữ liệu, validate quyền, quản lý transaction. Đúng nguyên tắc "AI Gateway chỉ là lớp trừu tượng hoá phía gọi" đã nêu ở D-SD01-006 (¶6).
- **Không gọi trực tiếp tới CSDL Postgres của Go monolith** — nhận input qua request (text, URL file trong MinIO/S3 nếu cần đọc file), trả output qua response. Việc đọc file (Tư liệu gốc/Nội dung) từ MinIO/S3 do chính AI Gateway thực hiện khi cần (ví dụ ASR, VLM) — MinIO/S3 credentials cấp riêng cho AI Gateway (chỉ quyền đọc), không đi qua Go monolith để tránh proxy file nặng qua REST/JSON (nhất quán với nguyên tắc "không proxy file lớn" ở D-SD01-003 (¶3)).
- Giao thức: **REST/JSON**, không dùng gRPC — dù D-SD01-006 (¶6) để ngỏ "gRPC/REST", chọn REST cho nhất quán với toàn bộ hệ thống (đã dùng REST/JSON cho mọi API khác — D-SD01-003 (¶3)), dễ debug/log, không cần thêm tooling codegen protobuf. ⚠ Quyết định bổ sung của tài liệu này — có thể đổi sang gRPC sau nếu đo được overhead JSON đáng kể ở tải cao.
- Mạng nội bộ (internal network), **không** đi qua reverse proxy/route `/api/v1/...` công khai (D-SD01-001 (¶1), D-SD01-002 (¶2)) — chỉ Go monolith (`/cmd/api`, `/cmd/worker`) gọi được. Xác thực bằng shared secret header (`X-Internal-Secret`), cùng kiểu cơ chế đã dùng cho webhook nội bộ ở D-SD03-025 (¶5.5) — không cần JWT/OAuth vì không phải endpoint người dùng gọi.
- Mỗi năng lực con có **endpoint riêng** ngay cả khi dùng chung model phía sau — ví dụ `gateway.generate`, `gateway.rewriteQuery` và `gateway.selfAudit` đều chạy trên cùng LLM nhưng khác prompt, khác schema input/output và khác kiểu trả (streaming vs. JSON một lần), nên không gộp thành một endpoint có cờ chế độ.

## 2. [D-SD06-002] Danh sách năng lực & endpoint

| # | Năng lực | Endpoint | operationId | Gọi bởi | Đồng bộ/bất đồng bộ |
|---|---|---|---|---|---|
| 1 | Sinh embedding | `POST /v1/embed` | `gateway.embed` | `/assistant` (indexing, D-SD05-004 (¶3.1) ) | Đồng bộ, trong job nền |
| 2 | Sinh câu trả lời (RAG) | `POST /v1/generate` | `gateway.generate` | `/assistant` (chat, D-SD05-005 (¶3.2) ) | Đồng bộ, streaming SSE — nằm trong request đồng bộ của người dùng |
| 3 | Viết lại câu hỏi theo ngữ cảnh hội thoại | `POST /v1/rewrite-query` | `gateway.rewriteQuery` | `/assistant` (chat multi-turn, bước 1 D-SD05-005 (¶3.2) ) | Đồng bộ, JSON một lần — nằm trong request đồng bộ của người dùng |
| 4 | Self-audit câu trả lời | `POST /v1/self-audit` | `gateway.selfAudit` | `/assistant` (chat, D-SD05-005 (¶3.2) ) | Đồng bộ, sau bước Generate |
| 5 | Trích transcript ASR | `POST /v1/transcribe` | `gateway.transcribe` | `/knowledge`/`/shared` (job nền sinh `transcript_storage_key` cho audio/video — D-SD03-019 (¶4.4) ) | Đồng bộ, trong job nền |
| 6 | So khớp ngữ nghĩa văn bản | `POST /v1/verify/text-match` | `gateway.verifyTextMatch` | `/verification` (AI Verification — văn bản, và âm thanh/phim sau khi có transcript, R-KB-081 (§2.2.6.6.1)) | Đồng bộ, trong job nền |
| 7 | So khớp nội dung vùng ảnh | `POST /v1/verify/image-region` | `gateway.verifyImageRegion` | `/verification` (AI Verification — hình ảnh, và khung hình phim, R-KB-081 (§2.2.6.6.1)) | Đồng bộ, trong job nền |
| 8 | Sinh bản nháp nội dung Mục từ | `POST /v1/generate-entry-draft` | `gateway.generateEntryDraft` | `/encyclopedia` (job `encyclopedia.generate_content`, D-SD04-019 (¶3.5)) | Đồng bộ, JSON một lần, trong job nền |

**Không có endpoint riêng cho việc trích metadata file** (số trang, kích thước ảnh, độ dài audio/video — D-SD01-004 (¶4)) — đây là xử lý kỹ thuật thuần tuý (đọc header file), không cần model AI, thực hiện trực tiếp trong `/cmd/worker` bằng thư viện thông thường (ví dụ `ffprobe` cho audio/video, đọc thuộc tính ảnh, đếm trang PDF) — **không gọi AI Gateway**.

**Không có endpoint trích transcript cho file văn bản** (`source_file.transcript_storage_key`/`knowledge_object_file.transcript_storage_key` khi `file_type = text`, cấu trúc `[{page, line, text}]` — D-SD03-004 (¶2.4) ) — tư liệu Hán Nôm đã được số hoá/OCR ở hệ thống thượng nguồn trước khi vào MinIO/S3 (R-GEN-003 (§1.1.1) đặc tả gốc), nên đây là **trích xuất text đã có sẵn trong file** (PDF text layer/OCR layer), không phải nhận dạng lại — thực hiện bằng thư viện parsing thông thường (`pdfplumber`/tương tự) trong `/cmd/worker`, **không gọi AI Gateway**. Việc tách 2 đường sinh transcript được ghi ở D-SD03-019 (¶4.4): **ASR (audio/video) → AI Gateway `gateway.transcribe`**; **text → parsing thuần tuý, không qua AI Gateway**.

## 3. Chi tiết từng endpoint

### 3.1. [D-SD06-003] `POST /v1/embed`

Request:
```json
{ "texts": ["đoạn văn bản 1", "đoạn văn bản 2"] }
```

Response:
```json
{
  "model": "qwen3-embedding-0.6b",
  "dim": 1024,
  "embeddings": [[0.012, -0.034, ...], [0.045, 0.001, ...]]
}
```

- Batch nhiều đoạn trong 1 request để giảm round-trip khi đánh chỉ mục hàng loạt (job `assistant.reindex_entry`, D-SD05-004 (¶3.1) ).
- `dim` phải khớp `vector(N)` đã khai báo cho cột `assistant_chunk.embedding` (D-SD05-001 (¶2.1) ) — đổi model embedding (khác `dim`) là thay đổi lớn, cần migration cột + re-index toàn bộ (đã nêu ở `01` ¶9 "chốt version model khi benchmark xong").
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem ¶8)**: **Qwen3-Embedding (bản 0.6B)** làm ứng viên chính — hỗ trợ hơn 100 ngôn ngữ (gồm tiếng Việt), instruction-aware, footprint nhỏ; **BGE-M3** làm ứng viên phụ vì có sẵn cơ chế hybrid (dense + sparse + multi-vector) trong cùng 1 model, khớp trực tiếp thiết kế retrieval hybrid đã chốt ở D-SD01-001 (¶1). `model` trong response ở trên chỉ là ví dụ minh hoạ theo ứng viên chính, chưa phải quyết định cuối.

### 3.2. [D-SD06-004] `POST /v1/generate`

Request:
```json
{
  "question": "Trống đồng Đông Sơn có hoa văn gì đặc trưng?",
  "context_chunks": [
    { "entry_id": "uuid", "title": "Trống đồng Đông Sơn", "text": "đoạn nội dung đã truy hồi..." }
  ],
  "no_answer_text": "Xin lỗi, Bách khoa Văn Minh Việt hiện chưa có thông tin về nội dung này."
}
```

- `no_answer_text` (tuỳ chọn): câu LLM phải dùng nguyên văn khi `context_chunks` không đủ thông tin trả lời; Go truyền giá trị cấu hình `assistant.no_context_answer` (D-SD05-005 (¶3.2), `07-system-settings.md`). Không truyền → dùng câu mặc định trong prompt.

Response — **streaming SSE** (đáp ứng NFR token đầu ≤3s, D-SD01-008 (¶8)/R-NFR-011 (§3.2.2)):
```
data: {"delta": "Trống đồng Đông Sơn "}

data: {"delta": "thường có hoa văn hình chim Lạc..."}

data: {"done": true, "cited_entry_ids": ["uuid1", "uuid2"]}
```

- Go (`/assistant.GenerateAnswer`, D-SD05-010 (¶4.4) ) đọc stream này và relay tiếp thành SSE cho client cuối (`assistant.chat` — `POST /assistant/chat` ) — 2 tầng SSE nối tiếp nhau, không buffer toàn bộ câu trả lời rồi mới gửi (giữ đúng mục tiêu token đầu ≤3s xuyên suốt cả 2 tầng).
- Prompt hệ thống (system prompt) ép LLM **chỉ trả lời dựa trên `context_chunks`**, không dùng kiến thức ngoài (R-AI-002 (§2.4.1), R-AI-005 (§2.4.4) đặc tả gốc) — chi tiết nội dung prompt ở D-SD06-011 (¶5).
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem ¶8)**: **Qwen3-30B-A3B-Instruct-2507** — kiến trúc MoE (30B tổng tham số, ~3.3B active mỗi token), context dài (262K token, dư sức chứa nhiều `context_chunks`), năng lực instruction-following mạnh — phù hợp trực tiếp yêu cầu bám sát context ở trên; tốc độ suy luận gần model 3B dù năng lực gần 30B, hỗ trợ đạt NFR token đầu ≤3s dễ hơn model dense cùng cỡ.

### 3.3. [D-SD06-005] `POST /v1/rewrite-query`

Request:
```json
{
  "question": "còn về hoa văn thì sao?",
  "history": [
    { "question": "Trống đồng Đông Sơn có niên đại nào?", "answer": "Khoảng thế kỷ..." }
  ]
}
```

Response:
```json
{ "rewritten_question": "Trống đồng Đông Sơn có hoa văn gì đặc trưng?" }
```

- Chỉ được gọi khi hội thoại **đã có lượt trước đó**; lượt đầu tiên Go bỏ qua bước này và dùng thẳng câu hỏi gốc (D-SD05-005 (¶3.2) bước 1 ).
- `history` là N lượt gần nhất do Go cắt sẵn (số N chốt lúc code — `05` ¶6); AI Gateway không tự đọc DB.
- **JSON một lần, không streaming** — kết quả là một câu ngắn, dùng ngay cho bước Retrieve ở Go, người dùng không nhìn thấy trực tiếp.
- ⚠ Nằm **trên đường tương tác** của người dùng (trước Retrieve/Generate), nên độ trễ endpoint này cộng thẳng vào NFR token đầu ≤3s (R-NFR-011 (§3.2.2)) — xem rủi ro đã ghi ở `05` ¶6; cân nhắc model nhỏ/nhanh hơn riêng cho endpoint này khi benchmark.
- Dùng chung LLM với `gateway.generate`, prompt khác (D-SD06-011 (¶5)).

### 3.4. [D-SD06-006] `POST /v1/self-audit`

Request:
```json
{
  "answer": "câu trả lời vừa sinh...",
  "context_chunks": [ { "entry_id": "uuid", "text": "..." } ]
}
```

Response:
```json
{
  "flags": [
    { "claim_text": "câu/đoạn trong answer chưa được chứng thực", "reason": "khong_tim_thay_trong_ngu_canh" }
  ]
}
```

- `flags` rỗng nếu không phát hiện gì bất thường — ghi thẳng vào `assistant_query_log.self_audit_flags` (D-SD05-003 (¶2.3) ), không chặn việc trả lời (đã chốt ở D-SD01-006 (¶6) bước 4).
- Go gọi endpoint này **sau khi** đã relay xong stream của `gateway.generate` cho người dùng (D-SD05-005 (¶3.2) bước 4). Lỗi/timeout ở đây không làm hỏng lượt hỏi — Go gửi sự kiện `self_audit` với `flags: null` và ghi `self_audit_flags = NULL` (D-SD05-012 (¶5.1)).

### 3.5. [D-SD06-007] `POST /v1/transcribe`

Request:
```json
{
  "storage_key": "sources/abc/interview_2024.mp3",
  "media_type": "audio",
  "language": "vi"
}
```

Response:
```json
{
  "segments": [
    { "start_time": 12.5, "end_time": 18.2, "text": "đoạn lời thoại được ASR..." },
    { "start_time": 18.2, "end_time": 25.0, "text": "..." }
  ]
}
```

- `storage_key` là đường dẫn MinIO/S3 (từ `source_file.storage_key`/`knowledge_object_file.storage_key`) — AI Gateway tự đọc file bằng credentials riêng (D-SD06-001 (¶1)), Go không upload/proxy file audio/video qua request này.
- `media_type = "video"`: AI Gateway tự tách audio track trước khi chạy ASR (dùng `ffmpeg` nội bộ) — Go không cần tách trước.
- Response ghi thẳng vào `transcript_storage_key` (JSON file mới trong Object storage, do Go/`worker` ghi lại sau khi nhận response — AI Gateway không tự ghi vào Object storage của hệ thống, tránh 2 phía cùng ghi 1 kho).
- Cấu trúc `segments` khớp trực tiếp định dạng `transcript_storage_key` cho audio/video đã chốt ở D-SD03-004 (¶2.4)  (`[{start_time, end_time, text}]`) — không cần transform thêm.
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem ¶8)**: **EraX-WoW-Turbo** (fine-tune tiếng Việt trên nền Whisper-turbo — nhẹ, nhanh) làm ứng viên chính; **PhoWhisper** (fine-tune tiếng Việt trên nền Whisper large-v3) làm ứng viên dự phòng (runner-up) nếu EraX-WoW-Turbo không đạt đủ chất lượng trên dữ liệu âm thanh phỏng vấn nghệ nhân thật.

### 3.6. [D-SD06-008] `POST /v1/verify/text-match`

Request:
```json
{
  "claim_text": "Trống đồng Đông Sơn thường có hoa văn hình chim Lạc ở vành ngoài mặt trống",
  "source_text": "đoạn văn bản trích đúng vị trí location đã khai báo, hoặc đúng segment transcript"
}
```

Response:
```json
{ "verdict": "dat", "note": "Nội dung trích dẫn khớp với phát biểu, có đề cập trực tiếp hoa văn chim Lạc." }
```

- `verdict` ∈ `{"dat", "khong_dat"}` — Go ghi thẳng vào `ai_verdict`/`ai_note` (`claim_reference`, D-SD03-009 (¶2.9) ) hoặc `content_ai_verdict`/`content_ai_note` (`claim`, D-SD03-008 (¶2.8)) tuỳ ngữ cảnh gọi.
- Dùng chung cho cả 2 trường hợp: (a) văn bản — `source_text` lấy từ `transcript_storage_key` (text) tại đúng `{page, line}`; (b) âm thanh/phim — `source_text` lấy từ segment transcript audio tại đúng khoảng `{start_time, end_time}`. Go chịu trách nhiệm tra cứu đúng đoạn text trước khi gọi endpoint này — AI Gateway không tự tra cứu vị trí.
- **Không kiểm tra "vị trí hợp lệ"** (page có tồn tại không, timestamp có vượt quá độ dài file không) — việc đó Go tự làm bằng cách so `location` với `source_file.metadata` (D-SD03-004 (¶2.4) ) **trước khi** gọi endpoint này; endpoint này giả định vị trí đã hợp lệ và `source_text` đã trích đúng.

### 3.7. [D-SD06-009] `POST /v1/verify/image-region`

Request:
```json
{
  "claim_text": "Trống đồng Đông Sơn thường có hoa văn hình chim Lạc ở vành ngoài mặt trống",
  "image_storage_key": "sources/abc/mat_trong.jpg",
  "bbox": { "top": 120, "left": 300, "right": 480, "bottom": 460 }
}
```

Response:
```json
{ "verdict": "dat", "note": "Vùng ảnh cho thấy hoa văn hình chim, khớp với mô tả." }
```

- `image_storage_key`: với hình ảnh, trỏ thẳng tới `source_file`/`knowledge_object_file`; với khung hình phim, Go/`worker` phải **tự trích frame** tại `start_time` bằng `ffmpeg` (ghi tạm vào Object storage hoặc truyền qua `image_bytes` base64 — ⚠ xem ¶8) rồi mới gọi endpoint này — AI Gateway không tự trích frame từ file video.
- `bbox` optional — bỏ qua thì VLM đọc toàn bộ ảnh/khung hình (áp dụng khi phim không khai báo khung ảnh, R-KB-062 (§2.2.4.2.4) "khung ảnh không bắt buộc").
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem ¶8)**: **Qwen3-VL** (đề xuất bản 32B làm điểm khởi đầu) — thế hệ mới hơn ví dụ Qwen2-VL/InternVL đã nêu ở D-SD01-006 (¶6), được vLLM hỗ trợ đầy đủ, đạt chất lượng gần ngang GPT-4o ở bản 72B trên benchmark MMBench-EN; bản 32B được chọn làm điểm khởi đầu vì cân bằng chất lượng/VRAM tốt hơn (không cần multi-GPU) so với việc phải lên thẳng 72B như họ Qwen2-VL.

### 3.8. [D-SD06-014] `POST /v1/generate-entry-draft`

Request:
```json
{
  "entry_title": "Trống đồng Đông Sơn",
  "sources": [
    {
      "title": "Hoa văn trống đồng Ngọc Lũ",
      "claims": ["Mặt trống có ngôi sao 14 cánh ở tâm…"],
      "transcript_storage_keys": ["knowledge/…/transcript.json"],
      "images": [ { "image_id": "uuid", "storage_key": "knowledge/…/mat_trong.jpg" } ]
    }
  ]
}
```

Response:
```json
{
  "blocks": [
    { "type": "heading", "level": 2, "text": "Hoa văn" },
    { "type": "paragraph", "text": "…" },
    { "type": "image", "image_id": "uuid", "caption": "Mặt trống đồng Ngọc Lũ" }
  ]
}
```

- AI Gateway tự đọc transcript và ảnh từ Object storage (D-SD06-001 (¶1)).
- Chỉ dùng thông tin trong `sources`, không dùng kiến thức nền của model; văn phong bách khoa, tiếng Việt (R-NFR-020 (§3.3.5)). `level` chỉ nhận 2 hoặc 3.
- Ảnh: ở `gpu-onprem`, VLM đọc ảnh để chọn vị trí chèn và viết `caption`; ở chế độ không có VLM, ảnh được xếp cuối, `caption` rỗng.
- Tổng nội dung vượt giới hạn ngữ cảnh của model → HTTP 422 `source_content_too_long`, không sinh nội dung.
- Model cấu hình riêng cho năng lực này (LLM và VLM); không cấu hình thì dùng LLM của `gateway.generate` và VLM của `gateway.verifyImageRegion`. ⚠ Model cụ thể chọn sau benchmark (¶8).

## 4. [D-SD06-010] Model & pipeline theo từng chế độ backend (`AI_GATEWAY_MODE`, D-SD01-006 (¶6))

| Năng lực | `mock` | `cpu-small` | `gpu-onprem` |
|---|---|---|---|
| `gateway.embed` | Vector giả (hash-based, deterministic theo input text, đúng `dim`) | `sentence-transformers` đa ngôn ngữ/tiếng Việt chạy CPU | **Qwen3-Embedding (0.6B)** hoặc **BGE-M3** qua vLLM (⚠ ứng viên, benchmark trước khi pin — ¶8) |
| `gateway.generate` | Câu trả lời mẫu cố định, ghép tên `entry` đầu tiên trong `context_chunks` | LLM quantize nhỏ qua `llama.cpp` (Vietnamese-capable) | **Qwen3-30B-A3B-Instruct-2507** (MoE) qua vLLM (⚠ ứng viên, benchmark trước khi pin — ¶8) |
| `gateway.rewriteQuery` | Trả thẳng `question` gốc làm `rewritten_question` | Cùng LLM `generate` qua `llama.cpp`, prompt rewrite | Cùng LLM `generate` (**Qwen3-30B-A3B-Instruct-2507**) qua vLLM — hoặc model nhỏ/nhanh hơn nếu benchmark cho thấy cần (¶8) |
| `gateway.selfAudit` | Luôn trả `flags: []` | Cùng LLM `generate`, prompt khác (vai trò kiểm tra) | Cùng LLM `generate` (Qwen3-30B-A3B-Instruct-2507) hoặc model riêng, qua vLLM |
| `gateway.transcribe` | 1 segment giả, `text` = `"[mock transcript]"`, phủ toàn bộ độ dài file (đọc metadata qua `ffprobe` để biết độ dài) | `faster-whisper` model nhỏ (`base`/`small`), CPU — chậm | **EraX-WoW-Turbo** (ứng viên chính) / **PhoWhisper** (runner-up) self-host (⚠ ứng viên, benchmark trước khi pin — ¶8) |
| `gateway.verifyTextMatch` | Luôn `verdict: "dat"` (⚠ có thể cấu hình để test đường "khong_dat" — ¶8) | Cùng LLM `generate` làm judge | LLM judge qua vLLM (cùng ứng viên `gateway.generate`) |
| `gateway.verifyImageRegion` | Luôn `verdict: "dat"` | **Không hỗ trợ đầy đủ** — VLM không khả thi chạy tốt trên CPU nhỏ; trả `verdict: "dat"` kèm `note: "cpu-small mode: bỏ qua kiểm VLM"` (⚠ xem ¶8) | **Qwen3-VL** (đề xuất bản 32B, ⚠ ứng viên — ¶8) qua vLLM |
| `gateway.generateEntryDraft` | Khối mẫu cố định: 1 heading + 1 paragraph ghép `entry_title`, kèm ảnh đầu tiên nếu có | LLM qua `llama.cpp`, không VLM (ảnh xếp cuối) | LLM của `gateway.generate` + Qwen3-VL cho ảnh, qua vLLM |

Chọn backend qua factory pattern trong code Python — 1 interface chung (`AIBackend`) với 3 implementation (`MockBackend`, `CPUSmallBackend`, `GPUOnpremBackend`), khởi tạo theo biến môi trường `AI_GATEWAY_MODE` lúc service start — đúng nguyên tắc "đổi implementation không viết lại tầng gọi" đã chốt ở D-SD01-006 (¶6).

## 5. [D-SD06-011] Prompt design (khung, chưa chốt nội dung chi tiết)

- **`gateway.generate`** — system prompt ép: (a) chỉ dùng thông tin trong `context_chunks`, không dùng kiến thức nền của model; (b) nếu `context_chunks` không đủ thông tin trả lời, trả lời đúng nguyên văn `no_answer_text` (D-SD06-004 (¶3.2)) hoặc câu mặc định nếu không có, thay vì bịa; (c) văn phong phù hợp bách khoa toàn thư (trung lập, không suy diễn).
- **`gateway.rewriteQuery`** — system prompt yêu cầu model viết lại câu hỏi hiện tại thành một câu **độc lập, đầy đủ ngữ cảnh** (self-contained) dựa trên `history`: thay đại từ/tham chiếu ngầm ("nó", "cái đó", "còn về X thì sao") bằng chủ thể cụ thể đã nhắc ở các lượt trước; **không trả lời** câu hỏi, không thêm thông tin mới, không suy diễn; nếu câu hỏi vốn đã độc lập thì trả lại gần như nguyên văn.
- **`gateway.selfAudit`** — system prompt yêu cầu model liệt kê từng câu/mệnh đề trong `answer`, đối chiếu xem có được `context_chunks` hỗ trợ trực tiếp không, gắn cờ nếu không.
- **`gateway.verifyTextMatch`** — system prompt đóng vai "chuyên gia đối chiếu tư liệu", yêu cầu trả lời đúng 1 trong 2 nhãn (`dat`/`khong_dat`) kèm giải thích ngắn — ép output có cấu trúc (JSON mode của LLM nếu backend hỗ trợ, hoặc parse từ text có định dạng cố định).
- **`gateway.verifyImageRegion`** — tương tự nhưng input đa phương thức (ảnh + text) qua VLM, cùng yêu cầu output có cấu trúc.
- **`gateway.generateEntryDraft`** — system prompt ép chỉ dùng `sources`, không suy diễn; tổ chức nội dung theo mục có tiêu đề; mỗi ảnh dùng tối đa một lần; output JSON đúng schema D-SD06-014 (¶3.8).
- ⚠ Nội dung prompt cụ thể (câu chữ, few-shot example...) để lại cho lúc implement + benchmark thực tế (cùng tinh thần "chốt sau khi có số liệu thực tế" ở `01` ¶9) — mục này chỉ chốt khung/yêu cầu, không chốt câu chữ.

## 6. [D-SD06-012] Xử lý lỗi, timeout, retry

- Response lỗi chuẩn hoá, nhất quán với quy ước chung D-SD01-003 (¶3): `{ "error_code": "...", "message": "...", "trace_id": "..." }`.
- **Job nền** (`gateway.embed`, `gateway.transcribe`, `/v1/verify/*`, `gateway.generateEntryDraft`, gọi từ `/cmd/worker`): lỗi/timeout để job tự thất bại và dựa vào cơ chế retry/dead-letter sẵn có của river (D-SD01-001 (¶1), D-SD01-004 (¶4)) — không tự implement retry riêng trong AI Gateway hay trong code gọi.
- **Request đồng bộ từ người dùng** (`gateway.generate`, `gateway.rewriteQuery`, `gateway.selfAudit`, gọi từ `/cmd/api` khi chat): lỗi/timeout trả thẳng lỗi cho người dùng qua endpoint `assistant.chat` (không retry ở tầng này vì người dùng đang chờ trực tiếp) — Go trả mã lỗi rõ ràng ("AI Văn Minh Việt tạm thời không phản hồi được, thử lại sau") thay vì để timeout im lặng. Ngoại lệ: lỗi/timeout của `gateway.selfAudit` không trả lỗi cho người dùng, vì câu trả lời đã được stream xong trước đó — xem D-SD06-006 (¶3.4).
- Timeout cụ thể theo từng endpoint (đề xuất, điều chỉnh khi có số liệu thực tế): `gateway.embed` 5s, `gateway.rewriteQuery` 5s (nằm trên đường tương tác, phải rất nhanh — xem rủi ro độ trễ ở `05` ¶6), `gateway.generate` không đặt timeout cứng (stream tới khi xong, nhưng có timeout tổng ứng với NFR ≤15s p95 — D-SD01-008 (¶8)/R-NFR-011 (§3.2.2)), `gateway.selfAudit` 10s, `gateway.transcribe` theo độ dài file (ví dụ 2× độ dài audio, vì không cần real-time — D-SD01-008 (¶8)), `/v1/verify/*` 15s, `gateway.generateEntryDraft` 300s ⚠.
- **Tải chồng lấn giữa chat (tương tác) và job nền (AI Verification)** trên cùng GPU on-prem — ⚠ vấn đề mở, xem D-SD06-013 (¶7).

## 7. [D-SD06-013] Cấu hình & vận hành

- Biến môi trường chính: `AI_GATEWAY_MODE` (`mock`/`cpu-small`/`gpu-onprem`, đã chốt ở D-SD01-006 (¶6)), `AI_GATEWAY_INTERNAL_SECRET` (shared secret xác thực từ Go), `ENTRY_DRAFT_LLM_MODEL`/`ENTRY_DRAFT_VLM_MODEL` (tuỳ chọn — model riêng cho `gateway.generateEntryDraft`, mặc định như D-SD06-014 (¶3.8)), `MINIO_ENDPOINT`/`MINIO_ACCESS_KEY`/`MINIO_SECRET_KEY` (quyền đọc riêng cho AI Gateway, D-SD06-001 (¶1)), model path/tên model theo từng năng lực (pin version cụ thể khi benchmark xong — `01` ¶9).
- `GET /v1/health` (operationId `gateway.getHealth`) — health check cho container orchestration (D-SD01-001 (¶1)); trả kèm `mode` đang chạy (`mock`/`cpu-small`/`gpu-onprem`) để dễ debug môi trường nào đang gọi backend nào.
- Đóng gói Docker riêng, deploy độc lập với Go monolith (đã chốt D-SD01-001 (¶1)/D-SD01-002 (¶2)) — cùng container hoặc tách container theo từng năng lực (RAG vs. Verification vs. ASR) là quyết định vận hành, không ảnh hưởng hợp đồng API ở tài liệu này.

## 8. Vấn đề mở / giả định

- **Ưu tiên tải GPU giữa chat tương tác và AI Verification nền** — ⚠ đặc tả chỉ cho biết 2 NFR khác nhau (chat ≤3s/≤15s, Verification "vài phút chấp nhận được" — D-SD01-008 (¶8)/R-NFR-011 (§3.2.2)) nhưng không có cơ chế admission-control/priority queue cụ thể ở tầng AI Gateway khi cả hai cùng tranh chấp GPU. Đề xuất: request queue riêng ưu tiên `gateway.generate`/`gateway.rewriteQuery`/`gateway.selfAudit` (đường chat) hơn `gateway.embed`/`gateway.transcribe`/`/v1/verify/*`/`gateway.generateEntryDraft` (đường nền) — cần benchmark thực tế trước khi chốt cơ chế cụ thể (cùng tinh thần "chốt sau khi có số liệu" — `01` ¶9).
- **`cpu-small` không hỗ trợ đầy đủ VLM** (`gateway.verifyImageRegion`, D-SD06-010 (¶4)) — môi trường dev local không GPU sẽ luôn trả `dat` cho tiêu chí hình ảnh, nghĩa là **không test được đường "khong_dat" của tiêu chí này** khi phát triển local. Chấp nhận được cho giai đoạn dev (mục đích `cpu-small` chỉ để test luồng nghiệp vụ, không cần chất lượng AI thật — D-SD01-006 (¶6)), nhưng cần lưu ý khi viết test tự động.
- **Cách truyền frame video đã trích xuất tới `gateway.verifyImageRegion`** (D-SD06-009 (¶3.7)) — 2 phương án: (a) Go/`worker` tự trích frame bằng `ffmpeg`, ghi tạm vào Object storage rồi truyền `image_storage_key`; (b) Go/`worker` trích frame rồi truyền thẳng `image_bytes` (base64) trong request, không ghi Object storage. Tài liệu này tạm chọn phương án (a) cho nhất quán với cách các endpoint khác đều truyền `storage_key` thay vì bytes — nhưng đây là chi tiết kỹ thuật có thể đổi khi implement, không ảnh hưởng ai_verdict/nghiệp vụ.
- **Cần cấu hình khả năng "trả lời giả để test đường không đạt" cho `mock` mode** (D-SD06-010 (¶4), dòng `gateway.verifyTextMatch`/`image-region`) — ví dụ qua query param hoặc theo nội dung `claim_text` chứa từ khoá đặc biệt (`"__mock_fail__"`) — chi tiết cụ thể để lại cho lúc viết test, chỉ ghi nhận nhu cầu ở đây.
- REST thay vì gRPC (D-SD06-001 (¶1)) — quyết định của tài liệu này, chưa qua xác nhận Requirements (không cần, thuộc phạm vi kỹ thuật thuần tuý) nhưng khác với cách D-SD01-006 (¶6) để ngỏ ban đầu ("gRPC/REST") — ghi nhận rõ ở đây để không hiểu nhầm là đã chốt gRPC. ⚠ D-SD01-006 (¶6) và D-SD05-011 (¶4.5) vẫn còn câu chữ "gRPC/REST" ở một vài chỗ, chưa đồng bộ theo quyết định này — điểm dọn tài liệu còn treo, không ảnh hưởng thiết kế.
- **Endpoint `gateway.rewriteQuery` (D-SD06-005 (¶3.3))** — ⚠ bổ sung 2026-09-23: `05-ai-assistant.md` trước đó mô tả bước Rewrite query "dùng chung endpoint Generate, đổi prompt", nhưng schema của `gateway.generate` (`{question, context_chunks}`) không có chỗ truyền lịch sử hội thoại, và kiểu trả cũng khác (streaming SSE vs. JSON một lần). Tách thành endpoint riêng theo đúng tiền lệ `gateway.selfAudit` — cùng LLM, khác prompt, khác hợp đồng. Không phát sinh model mới, không đổi hành vi nghiệp vụ.
- **Model cụ thể cho từng năng lực + giả định phần cứng làm cơ sở (⚠ đề xuất bổ sung, chưa benchmark)**:
  - Embedding → **Qwen3-Embedding** (0.6B, ứng viên chính) / **BGE-M3** (ứng viên phụ)
  - LLM (`generate`/`rewrite-query`/`self-audit`) → **Qwen3-30B-A3B-Instruct-2507** (kiến trúc MoE, 30B tổng/~3.3B active)
  - VLM (`verify/image-region`) → **Qwen3-VL** (đề xuất bản 32B)
  - ASR (`transcribe`) → **EraX-WoW-Turbo** (ứng viên chính) / **PhoWhisper** (runner-up)

  Các ứng viên này mới hơn ví dụ đã nêu ở D-SD01-006 (¶6) (Qwen2-VL/InternVL, Whisper/PhoWhisper) — **D-SD01-006 (¶6) chưa được đồng bộ theo các ứng viên mới này**, cần cập nhật riêng nếu muốn nhất quán.

  **Giả định phần cứng làm cơ sở chọn các ứng viên trên**: tối thiểu **1 GPU 40–48GB VRAM** (ví dụ A100 40GB hoặc L40S 48GB) — đủ tải đồng thời cả 4 model ở dạng lượng tử hoá 4-bit (ước tính tổng ~38GB VRAM), và **NVMe SSD tối thiểu 1TB** để lưu model gốc + bản lượng tử hoá (ước tính ~165GB cho cả 4 ứng viên). Nếu hạ tầng thực tế nhỏ hơn (ví dụ GPU 24GB), cần hạ xuống ứng viên nhẹ hơn (ví dụ Qwen3-VL-7B thay 32B); nếu lớn hơn (80GB+/multi-GPU), có thể cân nhắc bản lớn hơn (Qwen3-VL-72B, LLM 72B) để tăng chất lượng thay vì tối ưu VRAM. Đây chỉ là **giả định lập kế hoạch**, chưa phải cấu hình GPU on-prem đã chốt (`01` ¶9 vẫn để ngỏ mục này) — cần benchmark thật trên dữ liệu tư liệu gốc và tải GPU thực tế trước khi pin cả model lẫn cấu hình phần cứng.

---

**Ghi chú cá nhân (Phúc) — cấu hình dev trên máy cá nhân, không phải quyết định kiến trúc chung (2026-09-21):**

Đối chiếu với máy dev cá nhân thực tế (laptop, GPU NVIDIA T1200 4GB VRAM, RAM 64GB): **không đủ** chạy `gpu-onprem` (yêu cầu tối thiểu 1 GPU 40–48GB VRAM, xem giả định phần cứng ở trên — thiếu khoảng 10 lần). Máy này đủ RAM để chạy các model production ở trên (mục này) ở dạng lượng tử hoá qua CPU/llama.cpp thay vì vLLM, cho chất lượng gần production — khác mục đích đã chốt của `cpu-small` (D-SD06-010 (¶4), mode đó ưu tiên nhẹ/nhanh để test luồng nghiệp vụ, không cần chất lượng AI thật) nên **không** ghi chung vào bảng mode chính thức ở D-SD06-010 (¶4), chỉ ghi riêng ở đây để tự dùng:

| Năng lực | Model (giống production) | Dạng chạy | Dung lượng | Nơi chạy |
|---|---|---|---|---|
| Embedding | Qwen3-Embedding-0.6B | GGUF Q8_0 | ~0.64GB | GPU 4GB (thường trực) |
| LLM (generate/self-audit) | Qwen3-30B-A3B-Instruct-2507 | GGUF Q4_K_M | ~18.6GB | CPU (RAM 64GB) |
| ASR | EraX-WoW-Turbo-V1.1 | CT2 int8/fp16 | <1GB | GPU 4GB (thường trực) |
| VLM (verify/image-region) | Qwen3-VL-8B-Instruct *(hạ từ 32B)* | GGUF Q4_K_M | ~5GB | CPU (RAM 64GB) |

⚠ Chưa benchmark tốc độ thực tế trên CPU của máy này — chỉ dùng cho demo chất lượng câu trả lời, không đại diện NFR tốc độ (≤3s token đầu) của production.
