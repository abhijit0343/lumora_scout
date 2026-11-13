# Streaming Protocol & Human-in-the-Loop (HITL) Architecture

## Metadata
- **Purpose**: Defines Server-Sent Events (SSE) streaming protocols, event schemas, human-in-the-loop checkpoint lifecycles, resume semantics, and error recovery procedures.
- **Scope**: Covers all SSE event types, Checkpoint A/B/C interrupt handling, client resume payloads, cancellation flows, and session state recovery.
- **Owner files**: `backend/app/api/sse.py`, `backend/app/schemas/events.py`, `backend/app/agents/graph.py`, `backend/app/persistence/checkpointer.py`.

---

## 1. Server-Sent Events (SSE) Protocol

### 1.1 Transport & Connection Management
- Streaming responses are served over `POST /compare/stream` using standard MIME type `text/event-stream`.
- Connections maintain keep-alive heartbeats every `SSE_HEARTBEAT_S=15` seconds (sent as SSE comments `: heartbeat

`) to prevent proxy timeouts.
- Each event conforms strictly to standard format: `event: <event_type>
data: <json_string>

`.

### 1.2 SSE Event Taxonomy
The streaming API emits ten distinct event types:

| Event Type | Description | Key Payload Fields |
| :--- | :--- | :--- |
| `status` | Workflow stage transitions and agent activity updates | `thread_id`, `node`, `message`, `timestamp` |
| `tool_start` | Dispatched tool invocation notification | `tool_name`, `target`, `parameters` |
| `tool_result` | Completed tool execution summary | `tool_name`, `target`, `status`, `summary` |
| `interrupt` | Human-in-the-loop breakpoint pause notification | `thread_id`, `checkpoint_type`, `payload`, `allowed_actions` |
| `matrix_row` | Real-time populated row in comparison criteria table | `criterion_id`, `name`, `val_a`, `val_b`, `evidence` |
| `token` | Live streamed token from final verdict synthesis | `token_text`, `index` |
| `blocked` | Guardrail violation halt notification | `layer`, `reason`, `violation_code` |
| `sources` | Comprehensive list of cited web pages and documents | `target`, `url`, `title`, `chunk_ids` |
| `error` | System or tool execution failure event | `code`, `message`, `details` |
| `done` | Clean termination of comparative analysis workflow | `thread_id`, `verdict_id`, `duration_s` |

---

## 2. Human-in-the-Loop (HITL) Architecture

### 2.1 Checkpoint Specifications
1. **Checkpoint A: Target Confirmation (`confirm_targets`)**
   - **Default State**: Enabled (`HITL_CONFIRM_TARGETS=true`).
   - **Trigger**: Occurs immediately after target resolution.
   - **Operator Action**: Inspects resolved domain names, entities, and URLs for side A and side B. The operator may approve targets as resolved or submit edited URLs.
2. **Checkpoint B: Criteria Alignment (`confirm_criteria`)**
   - **Default State**: Disabled by default (`HITL_CONFIRM_CRITERIA=false`), toggleable per request.
   - **Trigger**: Occurs after capability extraction and initial taxonomy alignment.
   - **Operator Action**: Operator reviews proposed comparison criteria; may re-order, add specific criteria, or remove irrelevant attributes.
3. **Checkpoint C: Borderline Safety Evaluation**
   - **Default State**: Active when `GUARD_UNCERTAIN_ACTION=ask`.
   - **Trigger**: Occurs when input or URL safety classification score falls into the uncertain threshold range (0.35 - 0.70).
   - **Operator Action**: Operator provides human safety override or confirms abortion.

### 2.2 Resume Workflow (`POST /compare/resume`)
- Client transmits resume request containing:
  - `thread_id`: Target session identifier.
  - `checkpoint_type`: Type of checkpoint being resumed (`confirm_targets`, `confirm_criteria`, `safety_override`).
  - `action`: Operator decision (`approve`, `edit`, `abort`).
  - `modified_payload`: Optional user edits (e.g., corrected target URLs, modified criteria list).
- Server reloads checkpoint state from SQLite checkpointer (`checkpoints.sqlite`).
- If URLs were edited, runs them through L2 URL and SSRF guardrails before continuing graph execution.
- Resumes SSE event streaming on original or newly established connection.

### 2.3 Expiration & Timeouts
- Unattended interrupt checkpoints expire after `INTERRUPT_TTL_MIN=30` minutes. Expired threads are closed and marked as aborted.

---

## 3. Session Control & Reload Recovery

### 3.1 Cancellation Flow (`POST /compare/{thread}/cancel`)
- Client sends cancellation request.
- Server sets cancellation event flag on active LangGraph task, releases scraper and tool resources, emits final `status` (Cancelled) and `done` events, and terminates execution.

### 3.2 Page Reload & State Recovery (`GET /compare/{thread}/state`)
- If the client disconnects or reloads the browser, the frontend calls `GET /compare/{thread}/state`.
- Returns the latest committed graph state, populated matrix rows, current checkpoint status, and active interrupt payloads, allowing seamless client-side rehydration.
