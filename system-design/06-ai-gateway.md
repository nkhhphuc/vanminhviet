# Thiết Kế: AI Gateway (service Python riêng)

> Trạng thái: đã chốt — đang được `03-cultural-knowledge-base.md` (mục 4.2–4.4, mục 8) và `05-ai-assistant.md` tham chiếu tới các endpoint cụ thể.
>
> Tài liệu này **không theo cấu trúc chuẩn module 02–05** (`00-claude-instructions.md` mục 5), vì AI Gateway không phải một module nghiệp vụ ánh xạ 1-1 với đặc tả gốc — nó là service hạ tầng đã được quyết định kiến trúc ở `01-architecture-and-tech-stack.md` mục 6 (self-host, GPU on-prem, vLLM + ASR riêng, 3 chế độ backend). Tài liệu này bổ sung phần `01` mục 6 còn để ngỏ: **hợp đồng API cụ thể** giữa Go monolith (`/assistant` — tài liệu 05, `/verification` — tài liệu 03) và AI Gateway, cùng **kiến trúc nội bộ** của chính service Python này — đủ chi tiết để tự implement (không chỉ để Go gọi vào).

## 1. Phạm vi & nguyên tắc

- AI Gateway phục vụ đúng 2 năng lực nghiệp vụ đã chốt ở `01` mục 6: **RAG cho AI Văn Minh Việt** (module 05) và **AI Verification đa phương thức** (module 03, R-KB-080 (§2.2.6.6)) — không phục vụ mục đích nào khác.
- **Không tự quyết định nghiệp vụ** (verdict cuối cùng ghi vào `claim_reference`/`claim`, quyết định trạng thái workflow...) — AI Gateway chỉ trả kết quả thô (verdict/note/embedding/answer) cho Go monolith; Go monolith (`/verification`, `/assistant`) chịu trách nhiệm ghi dữ liệu, validate quyền, quản lý transaction. Đúng nguyên tắc "AI Gateway chỉ là lớp trừu tượng hoá phía gọi" đã nêu ở `01` mục 6.
- **Không gọi trực tiếp tới CSDL Postgres của Go monolith** — nhận input qua request (text, URL file trong MinIO/S3 nếu cần đọc file), trả output qua response. Việc đọc file (Tư liệu gốc/Nội dung) từ MinIO/S3 do chính AI Gateway thực hiện khi cần (ví dụ ASR, VLM) — MinIO/S3 credentials cấp riêng cho AI Gateway (chỉ quyền đọc), không đi qua Go monolith để tránh proxy file nặng qua REST/JSON (nhất quán với nguyên tắc "không proxy file lớn" ở `01` mục 3).
- Giao thức: **REST/JSON**, không dùng gRPC — dù `01` mục 6 để ngỏ "gRPC/REST", chọn REST cho nhất quán với toàn bộ hệ thống (đã dùng REST/JSON cho mọi API khác — `01` mục 3), dễ debug/log, không cần thêm tooling codegen protobuf. ⚠ Quyết định bổ sung của tài liệu này — có thể đổi sang gRPC sau nếu đo được overhead JSON đáng kể ở tải cao.
- Mạng nội bộ (internal network), **không** đi qua reverse proxy/route `/api/v1/...` công khai (`01` mục 1, 2) — chỉ Go monolith (`/cmd/api`, `/cmd/worker`) gọi được. Xác thực bằng shared secret header (`X-Internal-Secret`), cùng kiểu cơ chế đã dùng cho webhook nội bộ ở `03-cultural-knowledge-base.md` mục 5.5 — không cần JWT/OAuth vì không phải endpoint người dùng gọi.
- Mỗi năng lực con có **endpoint riêng** ngay cả khi dùng chung model phía sau — ví dụ `/v1/generate`, `/v1/rewrite-query` và `/v1/self-audit` đều chạy trên cùng LLM nhưng khác prompt, khác schema input/output và khác kiểu trả (streaming vs. JSON một lần), nên không gộp thành một endpoint có cờ chế độ.

## 2. Danh sách năng lực & endpoint

| # | Năng lực | Endpoint | Gọi bởi | Đồng bộ/bất đồng bộ |
|---|---|---|---|---|
| 1 | Sinh embedding | `POST /v1/embed` | `/assistant` (indexing, mục 3.1 tài liệu 05) | Đồng bộ, trong job nền |
| 2 | Sinh câu trả lời (RAG) | `POST /v1/generate` | `/assistant` (chat, mục 3.2 tài liệu 05) | Đồng bộ, streaming SSE — nằm trong request đồng bộ của người dùng |
| 3 | Viết lại câu hỏi theo ngữ cảnh hội thoại | `POST /v1/rewrite-query` | `/assistant` (chat multi-turn, bước 1 mục 3.2 tài liệu 05) | Đồng bộ, JSON một lần — nằm trong request đồng bộ của người dùng |
| 4 | Self-audit câu trả lời | `POST /v1/self-audit` | `/assistant` (chat, mục 3.2 tài liệu 05) | Đồng bộ, sau bước Generate |
| 5 | Trích transcript ASR | `POST /v1/transcribe` | `/knowledge`/`/shared` (job nền sinh `transcript_storage_key` cho audio/video — mục 4.4 tài liệu 03) | Đồng bộ, trong job nền |
| 6 | So khớp ngữ nghĩa văn bản | `POST /v1/verify/text-match` | `/verification` (AI Verification — văn bản, và âm thanh/phim sau khi có transcript, R-KB-081 (§2.2.6.6.1)) | Đồng bộ, trong job nền |
| 7 | So khớp nội dung vùng ảnh | `POST /v1/verify/image-region` | `/verification` (AI Verification — hình ảnh, và khung hình phim, R-KB-081 (§2.2.6.6.1)) | Đồng bộ, trong job nền |

**Không có endpoint riêng cho việc trích metadata file** (số trang, kích thước ảnh, độ dài audio/video — `01` mục 4) — đây là xử lý kỹ thuật thuần tuý (đọc header file), không cần model AI, thực hiện trực tiếp trong `/cmd/worker` bằng thư viện thông thường (ví dụ `ffprobe` cho audio/video, đọc thuộc tính ảnh, đếm trang PDF) — **không gọi AI Gateway**.

**Không có endpoint trích transcript cho file văn bản** (`source_file.transcript_storage_key`/`knowledge_object_file.transcript_storage_key` khi `file_type = text`, cấu trúc `[{page, line, text}]` — mục 2.4 tài liệu 03) — tư liệu Hán Nôm đã được số hoá/OCR ở hệ thống thượng nguồn trước khi vào MinIO/S3 (R-GEN-003 (§1.1.1) đặc tả gốc), nên đây là **trích xuất text đã có sẵn trong file** (PDF text layer/OCR layer), không phải nhận dạng lại — thực hiện bằng thư viện parsing thông thường (`pdfplumber`/tương tự) trong `/cmd/worker`, **không gọi AI Gateway**. Việc tách 2 đường sinh transcript được ghi ở `03-cultural-knowledge-base.md` mục 4.4: **ASR (audio/video) → AI Gateway `/v1/transcribe`**; **text → parsing thuần tuý, không qua AI Gateway**.

## 3. Chi tiết từng endpoint

### 3.1. `POST /v1/embed`

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

- Batch nhiều đoạn trong 1 request để giảm round-trip khi đánh chỉ mục hàng loạt (job `assistant.reindex_entry`, mục 3.1 tài liệu 05).
- `dim` phải khớp `vector(N)` đã khai báo cho cột `assistant_chunk.embedding` (mục 2.1 tài liệu 05) — đổi model embedding (khác `dim`) là thay đổi lớn, cần migration cột + re-index toàn bộ (đã nêu ở `01` mục 9 "chốt version model khi benchmark xong").
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem mục 8)**: **Qwen3-Embedding (bản 0.6B)** làm ứng viên chính — hỗ trợ hơn 100 ngôn ngữ (gồm tiếng Việt), instruction-aware, footprint nhỏ; **BGE-M3** làm ứng viên phụ vì có sẵn cơ chế hybrid (dense + sparse + multi-vector) trong cùng 1 model, khớp trực tiếp thiết kế retrieval hybrid đã chốt ở `01` mục 1. `model` trong response ở trên chỉ là ví dụ minh hoạ theo ứng viên chính, chưa phải quyết định cuối.

### 3.2. `POST /v1/generate`

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

- `no_answer_text` (tuỳ chọn): câu LLM phải dùng nguyên văn khi `context_chunks` không đủ thông tin trả lời; Go truyền giá trị cấu hình `assistant.no_context_answer` (`05` mục 3.2, `07-system-settings.md`). Không truyền → dùng câu mặc định trong prompt.

Response — **streaming SSE** (đáp ứng NFR token đầu ≤3s, `01` mục 8/R-NFR-011 (§3.2.2)):
```
data: {"delta": "Trống đồng Đông Sơn "}

data: {"delta": "thường có hoa văn hình chim Lạc..."}

data: {"done": true, "cited_entry_ids": ["uuid1", "uuid2"]}
```

- Go (`/assistant.GenerateAnswer`, mục 4.4 tài liệu 05) đọc stream này và relay tiếp thành SSE cho client cuối (`POST /assistant/chat`, mục 5.1 tài liệu 05) — 2 tầng SSE nối tiếp nhau, không buffer toàn bộ câu trả lời rồi mới gửi (giữ đúng mục tiêu token đầu ≤3s xuyên suốt cả 2 tầng).
- Prompt hệ thống (system prompt) ép LLM **chỉ trả lời dựa trên `context_chunks`**, không dùng kiến thức ngoài (R-AI-002 (§2.4.1), R-AI-005 (§2.4.4) đặc tả gốc) — chi tiết nội dung prompt ở mục 5.
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem mục 8)**: **Qwen3-30B-A3B-Instruct-2507** — kiến trúc MoE (30B tổng tham số, ~3.3B active mỗi token), context dài (262K token, dư sức chứa nhiều `context_chunks`), năng lực instruction-following mạnh — phù hợp trực tiếp yêu cầu bám sát context ở trên; tốc độ suy luận gần model 3B dù năng lực gần 30B, hỗ trợ đạt NFR token đầu ≤3s dễ hơn model dense cùng cỡ.

### 3.3. `POST /v1/rewrite-query`

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

- Chỉ được gọi khi hội thoại **đã có lượt trước đó**; lượt đầu tiên Go bỏ qua bước này và dùng thẳng câu hỏi gốc (mục 3.2 bước 1 tài liệu 05).
- `history` là N lượt gần nhất do Go cắt sẵn (số N chốt lúc code — `05` mục 6); AI Gateway không tự đọc DB.
- **JSON một lần, không streaming** — kết quả là một câu ngắn, dùng ngay cho bước Retrieve ở Go, người dùng không nhìn thấy trực tiếp.
- ⚠ Nằm **trên đường tương tác** của người dùng (trước Retrieve/Generate), nên độ trễ endpoint này cộng thẳng vào NFR token đầu ≤3s (R-NFR-011 (§3.2.2)) — xem rủi ro đã ghi ở `05` mục 6; cân nhắc model nhỏ/nhanh hơn riêng cho endpoint này khi benchmark.
- Dùng chung LLM với `/v1/generate`, prompt khác (mục 5).

### 3.4. `POST /v1/self-audit`

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

- `flags` rỗng nếu không phát hiện gì bất thường — ghi thẳng vào `assistant_query_log.self_audit_flags` (mục 2.3 tài liệu 05), không chặn việc trả lời (đã chốt ở `01` mục 6 bước 4).
- Go gọi endpoint này **sau khi** đã relay xong stream của `/v1/generate` cho người dùng (`05` mục 3.2 bước 4). Lỗi/timeout ở đây không làm hỏng lượt hỏi — Go gửi sự kiện `self_audit` với `flags: null` và ghi `self_audit_flags = NULL` (`05` mục 5.1).

### 3.5. `POST /v1/transcribe`

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

- `storage_key` là đường dẫn MinIO/S3 (từ `source_file.storage_key`/`knowledge_object_file.storage_key`) — AI Gateway tự đọc file bằng credentials riêng (mục 1), Go không upload/proxy file audio/video qua request này.
- `media_type = "video"`: AI Gateway tự tách audio track trước khi chạy ASR (dùng `ffmpeg` nội bộ) — Go không cần tách trước.
- Response ghi thẳng vào `transcript_storage_key` (JSON file mới trong Object storage, do Go/`worker` ghi lại sau khi nhận response — AI Gateway không tự ghi vào Object storage của hệ thống, tránh 2 phía cùng ghi 1 kho).
- Cấu trúc `segments` khớp trực tiếp định dạng `transcript_storage_key` cho audio/video đã chốt ở mục 2.4 tài liệu 03 (`[{start_time, end_time, text}]`) — không cần transform thêm.
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem mục 8)**: **EraX-WoW-Turbo** (fine-tune tiếng Việt trên nền Whisper-turbo — nhẹ, nhanh) làm ứng viên chính; **PhoWhisper** (fine-tune tiếng Việt trên nền Whisper large-v3) làm ứng viên dự phòng (runner-up) nếu EraX-WoW-Turbo không đạt đủ chất lượng trên dữ liệu âm thanh phỏng vấn nghệ nhân thật.

### 3.6. `POST /v1/verify/text-match`

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

- `verdict` ∈ `{"dat", "khong_dat"}` — Go ghi thẳng vào `ai_verdict`/`ai_note` (`claim_reference`, mục 2.9 tài liệu 03) hoặc `content_ai_verdict`/`content_ai_note` (`claim`, mục 2.8) tuỳ ngữ cảnh gọi.
- Dùng chung cho cả 2 trường hợp: (a) văn bản — `source_text` lấy từ `transcript_storage_key` (text) tại đúng `{page, line}`; (b) âm thanh/phim — `source_text` lấy từ segment transcript audio tại đúng khoảng `{start_time, end_time}`. Go chịu trách nhiệm tra cứu đúng đoạn text trước khi gọi endpoint này — AI Gateway không tự tra cứu vị trí.
- **Không kiểm tra "vị trí hợp lệ"** (page có tồn tại không, timestamp có vượt quá độ dài file không) — việc đó Go tự làm bằng cách so `location` với `source_file.metadata` (mục 2.4 tài liệu 03) **trước khi** gọi endpoint này; endpoint này giả định vị trí đã hợp lệ và `source_text` đã trích đúng.

### 3.7. `POST /v1/verify/image-region`

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

- `image_storage_key`: với hình ảnh, trỏ thẳng tới `source_file`/`knowledge_object_file`; với khung hình phim, Go/`worker` phải **tự trích frame** tại `start_time` bằng `ffmpeg` (ghi tạm vào Object storage hoặc truyền qua `image_bytes` base64 — ⚠ xem mục 8) rồi mới gọi endpoint này — AI Gateway không tự trích frame từ file video.
- `bbox` optional — bỏ qua thì VLM đọc toàn bộ ảnh/khung hình (áp dụng khi phim không khai báo khung ảnh, R-KB-062 (§2.2.4.2.4) "khung ảnh không bắt buộc").
- **⚠ Model đề xuất (ứng viên, chưa benchmark — xem mục 8)**: **Qwen3-VL** (đề xuất bản 32B làm điểm khởi đầu) — thế hệ mới hơn ví dụ Qwen2-VL/InternVL đã nêu ở `01` mục 6, được vLLM hỗ trợ đầy đủ, đạt chất lượng gần ngang GPT-4o ở bản 72B trên benchmark MMBench-EN; bản 32B được chọn làm điểm khởi đầu vì cân bằng chất lượng/VRAM tốt hơn (không cần multi-GPU) so với việc phải lên thẳng 72B như họ Qwen2-VL.

## 4. Model & pipeline theo từng chế độ backend (`AI_GATEWAY_MODE`, `01` mục 6)

| Năng lực | `mock` | `cpu-small` | `gpu-onprem` |
|---|---|---|---|
| `/v1/embed` | Vector giả (hash-based, deterministic theo input text, đúng `dim`) | `sentence-transformers` đa ngôn ngữ/tiếng Việt chạy CPU | **Qwen3-Embedding (0.6B)** hoặc **BGE-M3** qua vLLM (⚠ ứng viên, benchmark trước khi pin — mục 8) |
| `/v1/generate` | Câu trả lời mẫu cố định, ghép tên `entry` đầu tiên trong `context_chunks` | LLM quantize nhỏ qua `llama.cpp` (Vietnamese-capable) | **Qwen3-30B-A3B-Instruct-2507** (MoE) qua vLLM (⚠ ứng viên, benchmark trước khi pin — mục 8) |
| `/v1/rewrite-query` | Trả thẳng `question` gốc làm `rewritten_question` | Cùng LLM `generate` qua `llama.cpp`, prompt rewrite | Cùng LLM `generate` (**Qwen3-30B-A3B-Instruct-2507**) qua vLLM — hoặc model nhỏ/nhanh hơn nếu benchmark cho thấy cần (mục 8) |
| `/v1/self-audit` | Luôn trả `flags: []` | Cùng LLM `generate`, prompt khác (vai trò kiểm tra) | Cùng LLM `generate` (Qwen3-30B-A3B-Instruct-2507) hoặc model riêng, qua vLLM |
| `/v1/transcribe` | 1 segment giả, `text` = `"[mock transcript]"`, phủ toàn bộ độ dài file (đọc metadata qua `ffprobe` để biết độ dài) | `faster-whisper` model nhỏ (`base`/`small`), CPU — chậm | **EraX-WoW-Turbo** (ứng viên chính) / **PhoWhisper** (runner-up) self-host (⚠ ứng viên, benchmark trước khi pin — mục 8) |
| `/v1/verify/text-match` | Luôn `verdict: "dat"` (⚠ có thể cấu hình để test đường "khong_dat" — mục 8) | Cùng LLM `generate` làm judge | LLM judge qua vLLM (cùng ứng viên `/v1/generate`) |
| `/v1/verify/image-region` | Luôn `verdict: "dat"` | **Không hỗ trợ đầy đủ** — VLM không khả thi chạy tốt trên CPU nhỏ; trả `verdict: "dat"` kèm `note: "cpu-small mode: bỏ qua kiểm VLM"` (⚠ xem mục 8) | **Qwen3-VL** (đề xuất bản 32B, ⚠ ứng viên — mục 8) qua vLLM |

Chọn backend qua factory pattern trong code Python — 1 interface chung (`AIBackend`) với 3 implementation (`MockBackend`, `CPUSmallBackend`, `GPUOnpremBackend`), khởi tạo theo biến môi trường `AI_GATEWAY_MODE` lúc service start — đúng nguyên tắc "đổi implementation không viết lại tầng gọi" đã chốt ở `01` mục 6.

## 5. Prompt design (khung, chưa chốt nội dung chi tiết)

- **`/v1/generate`** — system prompt ép: (a) chỉ dùng thông tin trong `context_chunks`, không dùng kiến thức nền của model; (b) nếu `context_chunks` không đủ thông tin trả lời, trả lời đúng nguyên văn `no_answer_text` (mục 3.2) hoặc câu mặc định nếu không có, thay vì bịa; (c) văn phong phù hợp bách khoa toàn thư (trung lập, không suy diễn).
- **`/v1/rewrite-query`** — system prompt yêu cầu model viết lại câu hỏi hiện tại thành một câu **độc lập, đầy đủ ngữ cảnh** (self-contained) dựa trên `history`: thay đại từ/tham chiếu ngầm ("nó", "cái đó", "còn về X thì sao") bằng chủ thể cụ thể đã nhắc ở các lượt trước; **không trả lời** câu hỏi, không thêm thông tin mới, không suy diễn; nếu câu hỏi vốn đã độc lập thì trả lại gần như nguyên văn.
- **`/v1/self-audit`** — system prompt yêu cầu model liệt kê từng câu/mệnh đề trong `answer`, đối chiếu xem có được `context_chunks` hỗ trợ trực tiếp không, gắn cờ nếu không.
- **`/v1/verify/text-match`** — system prompt đóng vai "chuyên gia đối chiếu tư liệu", yêu cầu trả lời đúng 1 trong 2 nhãn (`dat`/`khong_dat`) kèm giải thích ngắn — ép output có cấu trúc (JSON mode của LLM nếu backend hỗ trợ, hoặc parse từ text có định dạng cố định).
- **`/v1/verify/image-region`** — tương tự nhưng input đa phương thức (ảnh + text) qua VLM, cùng yêu cầu output có cấu trúc.
- ⚠ Nội dung prompt cụ thể (câu chữ, few-shot example...) để lại cho lúc implement + benchmark thực tế (cùng tinh thần "chốt sau khi có số liệu thực tế" ở `01` mục 9) — mục này chỉ chốt khung/yêu cầu, không chốt câu chữ.

## 6. Xử lý lỗi, timeout, retry

- Response lỗi chuẩn hoá, nhất quán với quy ước chung `01` mục 3: `{ "error_code": "...", "message": "...", "trace_id": "..." }`.
- **Job nền** (`/v1/embed`, `/v1/transcribe`, `/v1/verify/*`, gọi từ `/cmd/worker`): lỗi/timeout để job tự thất bại và dựa vào cơ chế retry/dead-letter sẵn có của river (`01` mục 1, 4) — không tự implement retry riêng trong AI Gateway hay trong code gọi.
- **Request đồng bộ từ người dùng** (`/v1/generate`, `/v1/rewrite-query`, `/v1/self-audit`, gọi từ `/cmd/api` khi chat): lỗi/timeout trả thẳng lỗi cho người dùng qua endpoint `/assistant/chat` (không retry ở tầng này vì người dùng đang chờ trực tiếp) — Go trả mã lỗi rõ ràng ("AI Văn Minh Việt tạm thời không phản hồi được, thử lại sau") thay vì để timeout im lặng. Ngoại lệ: lỗi/timeout của `/v1/self-audit` không trả lỗi cho người dùng, vì câu trả lời đã được stream xong trước đó — xem mục 3.4.
- Timeout cụ thể theo từng endpoint (đề xuất, điều chỉnh khi có số liệu thực tế): `/v1/embed` 5s, `/v1/rewrite-query` 5s (nằm trên đường tương tác, phải rất nhanh — xem rủi ro độ trễ ở `05` mục 6), `/v1/generate` không đặt timeout cứng (stream tới khi xong, nhưng có timeout tổng ứng với NFR ≤15s p95 — `01` mục 8/R-NFR-011 (§3.2.2)), `/v1/self-audit` 10s, `/v1/transcribe` theo độ dài file (ví dụ 2× độ dài audio, vì không cần real-time — `01` mục 8), `/v1/verify/*` 15s.
- **Tải chồng lấn giữa chat (tương tác) và job nền (AI Verification)** trên cùng GPU on-prem — ⚠ vấn đề mở, xem mục 7.

## 7. Cấu hình & vận hành

- Biến môi trường chính: `AI_GATEWAY_MODE` (`mock`/`cpu-small`/`gpu-onprem`, đã chốt ở `01` mục 6), `AI_GATEWAY_INTERNAL_SECRET` (shared secret xác thực từ Go), `MINIO_ENDPOINT`/`MINIO_ACCESS_KEY`/`MINIO_SECRET_KEY` (quyền đọc riêng cho AI Gateway, mục 1), model path/tên model theo từng năng lực (pin version cụ thể khi benchmark xong — `01` mục 9).
- `GET /v1/health` — health check cho container orchestration (`01` mục 1); trả kèm `mode` đang chạy (`mock`/`cpu-small`/`gpu-onprem`) để dễ debug môi trường nào đang gọi backend nào.
- Đóng gói Docker riêng, deploy độc lập với Go monolith (đã chốt `01` mục 1/2) — cùng container hoặc tách container theo từng năng lực (RAG vs. Verification vs. ASR) là quyết định vận hành, không ảnh hưởng hợp đồng API ở tài liệu này.

## 8. Vấn đề mở / giả định

- **Ưu tiên tải GPU giữa chat tương tác và AI Verification nền** — ⚠ đặc tả chỉ cho biết 2 NFR khác nhau (chat ≤3s/≤15s, Verification "vài phút chấp nhận được" — `01` mục 8/R-NFR-011 (§3.2.2)) nhưng không có cơ chế admission-control/priority queue cụ thể ở tầng AI Gateway khi cả hai cùng tranh chấp GPU. Đề xuất: request queue riêng ưu tiên `/v1/generate`/`/v1/rewrite-query`/`/v1/self-audit` (đường chat) hơn `/v1/embed`/`/v1/transcribe`/`/v1/verify/*` (đường nền) — cần benchmark thực tế trước khi chốt cơ chế cụ thể (cùng tinh thần "chốt sau khi có số liệu" — `01` mục 9).
- **`cpu-small` không hỗ trợ đầy đủ VLM** (`/v1/verify/image-region`, mục 4) — môi trường dev local không GPU sẽ luôn trả `dat` cho tiêu chí hình ảnh, nghĩa là **không test được đường "khong_dat" của tiêu chí này** khi phát triển local. Chấp nhận được cho giai đoạn dev (mục đích `cpu-small` chỉ để test luồng nghiệp vụ, không cần chất lượng AI thật — `01` mục 6), nhưng cần lưu ý khi viết test tự động.
- **Cách truyền frame video đã trích xuất tới `/v1/verify/image-region`** (mục 3.7) — 2 phương án: (a) Go/`worker` tự trích frame bằng `ffmpeg`, ghi tạm vào Object storage rồi truyền `image_storage_key`; (b) Go/`worker` trích frame rồi truyền thẳng `image_bytes` (base64) trong request, không ghi Object storage. Tài liệu này tạm chọn phương án (a) cho nhất quán với cách các endpoint khác đều truyền `storage_key` thay vì bytes — nhưng đây là chi tiết kỹ thuật có thể đổi khi implement, không ảnh hưởng ai_verdict/nghiệp vụ.
- **Cần cấu hình khả năng "trả lời giả để test đường không đạt" cho `mock` mode** (mục 4, dòng `/v1/verify/text-match`/`image-region`) — ví dụ qua query param hoặc theo nội dung `claim_text` chứa từ khoá đặc biệt (`"__mock_fail__"`) — chi tiết cụ thể để lại cho lúc viết test, chỉ ghi nhận nhu cầu ở đây.
- REST thay vì gRPC (mục 1) — quyết định của tài liệu này, chưa qua xác nhận Requirements (không cần, thuộc phạm vi kỹ thuật thuần tuý) nhưng khác với cách `01` mục 6 để ngỏ ban đầu ("gRPC/REST") — ghi nhận rõ ở đây để không hiểu nhầm là đã chốt gRPC. ⚠ `01` mục 6 và `05` mục 4.5 vẫn còn câu chữ "gRPC/REST" ở một vài chỗ, chưa đồng bộ theo quyết định này — điểm dọn tài liệu còn treo, không ảnh hưởng thiết kế.
- **Endpoint `/v1/rewrite-query` (mục 3.3)** — ⚠ bổ sung 2026-09-23: `05-ai-assistant.md` trước đó mô tả bước Rewrite query "dùng chung endpoint Generate, đổi prompt", nhưng schema của `/v1/generate` (`{question, context_chunks}`) không có chỗ truyền lịch sử hội thoại, và kiểu trả cũng khác (streaming SSE vs. JSON một lần). Tách thành endpoint riêng theo đúng tiền lệ `/v1/self-audit` — cùng LLM, khác prompt, khác hợp đồng. Không phát sinh model mới, không đổi hành vi nghiệp vụ.
- **Model cụ thể cho từng năng lực + giả định phần cứng làm cơ sở (⚠ đề xuất bổ sung, chưa benchmark)**:
  - Embedding → **Qwen3-Embedding** (0.6B, ứng viên chính) / **BGE-M3** (ứng viên phụ)
  - LLM (`generate`/`rewrite-query`/`self-audit`) → **Qwen3-30B-A3B-Instruct-2507** (kiến trúc MoE, 30B tổng/~3.3B active)
  - VLM (`verify/image-region`) → **Qwen3-VL** (đề xuất bản 32B)
  - ASR (`transcribe`) → **EraX-WoW-Turbo** (ứng viên chính) / **PhoWhisper** (runner-up)

  Các ứng viên này mới hơn ví dụ đã nêu ở `01` mục 6 (Qwen2-VL/InternVL, Whisper/PhoWhisper) — **`01` mục 6 chưa được đồng bộ theo các ứng viên mới này**, cần cập nhật riêng nếu muốn nhất quán.

  **Giả định phần cứng làm cơ sở chọn các ứng viên trên**: tối thiểu **1 GPU 40–48GB VRAM** (ví dụ A100 40GB hoặc L40S 48GB) — đủ tải đồng thời cả 4 model ở dạng lượng tử hoá 4-bit (ước tính tổng ~38GB VRAM), và **NVMe SSD tối thiểu 1TB** để lưu model gốc + bản lượng tử hoá (ước tính ~165GB cho cả 4 ứng viên). Nếu hạ tầng thực tế nhỏ hơn (ví dụ GPU 24GB), cần hạ xuống ứng viên nhẹ hơn (ví dụ Qwen3-VL-7B thay 32B); nếu lớn hơn (80GB+/multi-GPU), có thể cân nhắc bản lớn hơn (Qwen3-VL-72B, LLM 72B) để tăng chất lượng thay vì tối ưu VRAM. Đây chỉ là **giả định lập kế hoạch**, chưa phải cấu hình GPU on-prem đã chốt (`01` mục 9 vẫn để ngỏ mục này) — cần benchmark thật trên dữ liệu tư liệu gốc và tải GPU thực tế trước khi pin cả model lẫn cấu hình phần cứng.

---

**Ghi chú cá nhân (Phúc) — cấu hình dev trên máy cá nhân, không phải quyết định kiến trúc chung (2026-09-21):**

Đối chiếu với máy dev cá nhân thực tế (laptop, GPU NVIDIA T1200 4GB VRAM, RAM 64GB): **không đủ** chạy `gpu-onprem` (yêu cầu tối thiểu 1 GPU 40–48GB VRAM, xem giả định phần cứng ở trên — thiếu khoảng 10 lần). Máy này đủ RAM để chạy các model production ở trên (mục này) ở dạng lượng tử hoá qua CPU/llama.cpp thay vì vLLM, cho chất lượng gần production — khác mục đích đã chốt của `cpu-small` (mục 4, mode đó ưu tiên nhẹ/nhanh để test luồng nghiệp vụ, không cần chất lượng AI thật) nên **không** ghi chung vào bảng mode chính thức ở mục 4, chỉ ghi riêng ở đây để tự dùng:

| Năng lực | Model (giống production) | Dạng chạy | Dung lượng | Nơi chạy |
|---|---|---|---|---|
| Embedding | Qwen3-Embedding-0.6B | GGUF Q8_0 | ~0.64GB | GPU 4GB (thường trực) |
| LLM (generate/self-audit) | Qwen3-30B-A3B-Instruct-2507 | GGUF Q4_K_M | ~18.6GB | CPU (RAM 64GB) |
| ASR | EraX-WoW-Turbo-V1.1 | CT2 int8/fp16 | <1GB | GPU 4GB (thường trực) |
| VLM (verify/image-region) | Qwen3-VL-8B-Instruct *(hạ từ 32B)* | GGUF Q4_K_M | ~5GB | CPU (RAM 64GB) |

⚠ Chưa benchmark tốc độ thực tế trên CPU của máy này — chỉ dùng cho demo chất lượng câu trả lời, không đại diện NFR tốc độ (≤3s token đầu) của production.
