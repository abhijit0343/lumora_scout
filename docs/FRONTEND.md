# Frontend Architecture & UI Specification

## Metadata
- **Purpose**: Details the frontend component hierarchy, Three.js 3D battle arena, state machine, and streaming UX.
- **Scope**: React components, Vite configuration, Three.js scenes, custom SSE hooks, and design system.
- **Owner files**: `frontend/*`, `frontend/src/*`, `docs/frontend/LUMORA_DESIGN_PROMPT.md`.

---

## 1. User Experience & Design Philosophy Outline
- **Cyber-Intel Aesthetic**: High-contrast, dark-mode futuristic dashboard styled with clean typography and cyber-intel accents.
- **Real-Time Transparency**: Real-time visibility into agent reasoning, tool invocations, and capability extraction progress via live SSE telemetry.
- **Seamless Human Intervention**: Prominent, non-intrusive modal and inline dialogs for HITL checkpoints A (targets), B (criteria), and C (safety).

## 2. Component Hierarchy Outline
- **Layout Shell (`src/pages/Home.jsx`)**: Main container housing header, query bar, 3D viewport, comparison matrix, and verdict panel.
- **3D Comparison Arena (`src/three/BattleArena.jsx`)**: Interactive Three.js canvas featuring dual holographic platforms representing Side A and Side B.
- **Capability Matrix View (`src/components/CapabilityMatrix.jsx`)**: Responsive comparison grid displaying side-by-side criteria, evidence, and scores.
- **HITL Modal Dialogs (`src/components/HITLModal.jsx`)**: User review panels for verifying target URLs and tailoring comparison criteria.
- **Streaming Verdict Reader (`src/components/VerdictStream.jsx`)**: Live markdown token stream presenting trade-offs and verdict recommendations.

## 3. State Management & Hooks Outline
- **SSE Stream Hook (`src/hooks/useCompareStream.js`)**: Manages EventSource/fetch streaming, backpressure, reconnection, and event dispatching.
- **HITL Resume Hook (`src/hooks/useHITL.js`)**: Coordinates user approvals and edits submitted to `/compare/resume`.
