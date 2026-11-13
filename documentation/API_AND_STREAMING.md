# API Routes, SSE Streaming & Human-in-the-Loop

## Overview
Lumora Scout exposes high-performance asynchronous REST endpoints and a real-time Server-Sent Events (SSE) streaming protocol via FastAPI.

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/api/sse.py`
- **Purpose**: Server-Sent Events (SSE) stream generator and keep-alive monitor.
- **How It Works**:
  - Consumes LangGraph state updates and serializes them into standard SSE format: `event: <type>
data: <json>

`.
  - Emits periodic keep-alive comments (`: heartbeat

`) every `SSE_HEARTBEAT_S=15` seconds to prevent reverse proxy and browser timeouts.

### 2. `backend/app/api/routes/compare.py`
- **Purpose**: Comparison session lifecycle controller.
- **Endpoints**:
  - `POST /compare/stream`: Initiates comparison and returns an active SSE stream.
  - `POST /compare/resume`: Resumes an interrupted session from Checkpoint A, B, or C.
  - `GET /compare/{thread}/state`: Returns latest session snapshot for page reload recovery.
  - `POST /compare/{thread}/cancel`: Aborts active agent execution and frees resources.

### 3. `backend/app/api/routes/documents.py`
- **Purpose**: Document ingestion controller for RAG grounding.
- **Endpoint**:
  - `POST /documents`: Accepts multipart file uploads (`pdf`, `docx`, `txt`, `md`), chunks text, generates EmbeddingGemma 2 embeddings, and updates FAISS/BM25 indexes.

### 4. `backend/app/api/routes/health.py`
- **Purpose**: System diagnostics and readiness probe.
- **Endpoint**:
  - `GET /health`: Verifies model connectivity, SQLite checkpointer availability, and index integrity.

---

## 📡 The 10 Server-Sent Event (SSE) Types

| Event Type | Emitted When | Payload Content |
| :--- | :--- | :--- |
| `status` | Workflow transitions between nodes | Stage message, node name, timestamp |
| `tool_start` | Tool scraper is dispatched | Tool name, target URL/identifier |
| `tool_result` | Tool execution completes | Status, execution time, result summary |
| `interrupt` | Human-in-the-loop checkpoint is reached | Checkpoint type, candidate targets/criteria |
| `matrix_row` | A capability row is evaluated | Criterion name, Side A value, Side B value, evidence |
| `token` | Final verdict is generating | Live streaming token chunk |
| `blocked` | Guardrail blocks a prompt, URL, or content | Layer number, violation code, reason |
| `sources` | Evidence is synthesized | Cited URLs, document names, chunk offsets |
| `error` | System or tool exception occurs | Error code, explanation |
| `done` | Workflow completes successfully | Thread ID, verdict ID, total duration |

---

## 🛑 Human-in-the-Loop (HITL) Checkpoints

1. **Checkpoint A (`confirm_targets`)**:
   - Default: Enabled (`HITL_CONFIRM_TARGETS=true`).
   - Trigger: Occurs immediately after target resolution.
   - Operator Action: User inspects resolved domain names and URLs; can approve or submit corrected URLs.
2. **Checkpoint B (`confirm_criteria`)**:
   - Default: Disabled (`HITL_CONFIRM_CRITERIA=false`).
   - Trigger: Occurs after capability alignment.
   - Operator Action: User re-orders, adds, or removes comparison criteria before scoring begins.
3. **Checkpoint C (Borderline Safety)**:
   - Default: Active when `GUARD_UNCERTAIN_ACTION=ask`.
   - Trigger: Safety classification confidence falls between 0.35 and 0.70.
   - Operator Action: User confirms whether to proceed or abort.
