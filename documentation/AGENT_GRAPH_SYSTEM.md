# LangGraph Multi-Agent Architecture & State Machine

## Overview
Lumora Scout coordinates comparative reasoning through a state machine built with **LangGraph** and persisted by an SQLite checkpointer. The architecture supports parallel fan-out extraction for Target A and Target B, deterministic Human-in-the-Loop checkpoints, and self-correcting retry loops.

---

## 📁 File Responsibilities & How They Work

### 1. `backend/app/agents/state.py`
- **Purpose**: Defines the global state schema (`CompareState`).
- **How It Works**:
  - Implemented as a `TypedDict` containing all session variables:
    - `thread_id`: Unique session UUID matching SQLite checkpointer thread.
    - `user_query`: Original user comparison instruction.
    - `target_a_raw` / `target_b_raw`: Raw inputs provided by user.
    - `resolved_target_a` / `resolved_target_b`: Structured `CatalogItem` records (canonical names, URLs, domains, entity types).
    - `capabilities_a` / `capabilities_b`: Extracted capabilities and evidence lists.
    - `aligned_matrix`: Comparison matrix rows aligning criteria to evidence from both sides.
    - `rag_grounding_context`: Retrieved document chunks and similarity percentages.
    - `scores`: Quantitative capability scores and winner metrics.
    - `verdict`: Final comparative analysis and recommendation.
    - `guardrail_status`: State of L1-L4 checks and violation codes.
    - `interrupt_data`: Payloads delivered to human operators during pause states.

### 2. `backend/app/agents/graph.py`
- **Purpose**: Graph constructor and workflow compiler.
- **How It Works**:
  - Constructs the `StateGraph` parameterized with `CompareState`.
  - Registers all 11 workflow nodes and wires sequential, parallel, and conditional edges.
  - Binds the `SqliteSaver` checkpointer so state is written to SQLite after every node execution.
  - Exposes `.stream()` and `.resume()` interfaces utilized by FastAPI endpoints.

---

## 🔄 Node Walkthrough & Execution Lifecycle

| Step | Node | File | Description |
| :--- | :--- | :--- | :--- |
| 1 | `guard_in` | `nodes/guard_in.py` | L1 input safety screening. Blocks prompt injections. |
| 2 | `resolve` | `nodes/resolve.py` | Uses `router.md` & `resolver.md` to identify products and official URLs. |
| 3 | `confirm_targets` | `nodes/confirm_targets.py` | **Checkpoint A (HITL)**: Interrupts workflow to allow operator to review/edit targets. |
| 4 | `guard_urls` | `nodes/guard_urls.py` | L2 URL/SSRF guardrail inspecting resolved or human-edited URLs. |
| 5 | `fetch_extract` | `nodes/fetch_extract.py` | **Parallel Fan-out**: Runs independently for Target A and Target B (fetch -> L3 guard -> extract). |
| 6 | `align` | `nodes/align.py` | Synchronizes parallel outputs, reconciling feature taxonomies into unified criteria. |
| 7 | `confirm_criteria` | `nodes/confirm_criteria.py`| **Checkpoint B (HITL)**: Interrupts workflow if criteria confirmation is enabled. |
| 8 | `rag_ground` | `nodes/rag_ground.py` | Retrieves uploaded document context; grades evidence with up to 2 query rewrites. |
| 9 | `score` | `nodes/score.py` | Computes quantitative capability scores and top-k chunk mean similarities. |
| 10| `verdict` | `nodes/verdict.py` | High-thinking LLM synthesizes trade-offs and verdict; streams live tokens via SSE. |
| 11| `guard_out` | `nodes/guard_out.py` | L4 output safety screening. Scrubs PII and leaks before terminal `done` event. |

---

## 🔀 Parallel Fan-Out Execution

After `guard_urls` verifies both URLs, LangGraph splits execution into two concurrent asynchronous tasks:
- `fetch_extract_a`: Scrapes Target A, applies L3 content guardrails, and extracts structured capabilities.
- `fetch_extract_b`: Scrapes Target B, applies L3 content guardrails, and extracts structured capabilities.

The graph joins both branches at the `align` node, ensuring neither side blocks the other and halving total extraction latency.
