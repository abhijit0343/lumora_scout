# API Contract Specification

## Metadata
- **Purpose**: Formal specification of all backend REST endpoints and Server-Sent Event streaming interfaces for Lumora Scout.
- **Scope**: Request/response contracts, field definitions, HTTP status codes, validation rules, and error envelopes.
- **Owner files**: `backend/app/api/routes/*`, `backend/app/schemas/*`, `backend/app/main.py`.

---

## 1. Endpoints Overview

| Method | Path | Description | Response Content-Type |
| :--- | :--- | :--- | :--- |
| `POST` | `/compare/stream` | Initiates new comparison and streams SSE events | `text/event-stream` |
| `POST` | `/compare/resume` | Submits HITL decision and resumes execution | `application/json` or `text/event-stream` |
| `GET` | `/compare/{thread}/state` | Fetches current snapshot and checkpoint status | `application/json` |
| `POST` | `/compare/{thread}/cancel` | Aborts active comparison session | `application/json` |
| `POST` | `/documents` | Uploads and indexes documents for RAG grounding | `application/json` |
| `GET` | `/health` | System health check and model availability | `application/json` |

---

## 2. Endpoint Details

### 2.1 `POST /compare/stream`
Initiates comparative analysis between two target websites or products.

#### Request Body (`application/json`)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `target_a` | string | Yes | Name, brand, or URL for side A |
| `target_b` | string | Yes | Name, brand, or URL for side B |
| `user_instructions` | string | No | Optional guidance on criteria or focus areas |
| `enable_hitl_criteria` | boolean | No | Force enable Checkpoint B (default: false) |
| `document_ids` | array[string] | No | List of uploaded document IDs for RAG grounding |

#### Streaming Response (`text/event-stream`)
Streams SSE events: `status`, `tool_start`, `tool_result`, `interrupt`, `matrix_row`, `token`, `blocked`, `sources`, `error`, `done`.

---

### 2.2 `POST /compare/resume`
Resumes an agent execution paused at a Human-in-the-Loop checkpoint.

#### Request Body (`application/json`)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `thread_id` | string | Yes | UUID of the paused comparison session |
| `checkpoint_type` | string | Yes | `confirm_targets`, `confirm_criteria`, or `safety_override` |
| `action` | string | Yes | `approve`, `edit`, or `abort` |
| `modified_targets` | object | No | Updated URLs/identities if editing at Checkpoint A |
| `modified_criteria`| array[string] | No | Updated criteria list if editing at Checkpoint B |

#### Response (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `status` | string | Status of resumption (`resumed`, `aborted`, `invalid`) |
| `thread_id` | string | Active session thread identifier |

---

### 2.3 `GET /compare/{thread}/state`
Fetches complete serialized state and current progress for a given session.

#### Path Parameters
- `thread`: UUID string of the session.

#### Response (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `thread_id` | string | Session identifier |
| `phase` | string | Current graph node/phase |
| `is_interrupted` | boolean | Whether execution is waiting on human input |
| `checkpoint_data`| object | Pending checkpoint details if interrupted |
| `catalog_a` | object | Resolved target A information |
| `catalog_b` | object | Resolved target B information |
| `matrix` | array[object]| Populated capability comparison rows |
| `verdict` | string | Synthesized final verdict if available |

---

### 2.4 `POST /compare/{thread}/cancel`
Cancels execution of an active comparison thread.

#### Path Parameters
- `thread`: UUID string of the session.

#### Response (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `thread_id` | string | Cancelled session identifier |
| `status` | string | Constant `cancelled` |

---

### 2.5 `POST /documents`
Uploads reference documents for chunking, vector embedding, and RAG retrieval.

#### Request Format (`multipart/form-data`)
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | binary file | Yes | Document file (`pdf`, `docx`, `txt`, `md`) <= 15MB |
| `description` | string | No | Optional human description of document scope |

#### Response (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `document_id` | string | Unique document UUID |
| `filename` | string | Original filename |
| `chunks_indexed`| integer | Number of chunks generated and indexed |
| `embedding_dim` | integer | Vector dimension (768) |

---

### 2.6 `GET /health`
Validates backend system integrity, model provider configurations, and index readiness.

#### Response (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `status` | string | System status (`healthy`, `degraded`) |
| `version` | string | Application version (`0.1.0`) |
| `primary_llm` | string | Primary LLM provider status and model ID |
| `embedding_model`| string | Embedding model status |
| `checkpointer` | string | SQLite checkpointer connection status |
