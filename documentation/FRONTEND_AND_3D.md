# Frontend Architecture & Three.js 3D Arena

## Overview
The Lumora Scout user interface is built with React 18 and Vite, featuring an interactive Three.js 3D WebGL comparison arena, real-time SSE streaming telemetry, and responsive Human-in-the-Loop review panels.

---

## 📁 Directory Structure & How It Works

```
frontend/src/
├── components/          # UI components (matrix, modal, streaming text)
├── hooks/               # Custom hooks for SSE streams and HITL actions
├── pages/               # Main application views
├── three/               # Three.js 3D battle arena WebGL scenes
├── lib/                 # API clients and utility functions
└── styles/              # Design tokens, CSS modules, and themes
```

### Key Subsystems:
1. **Three.js 3D Battle Arena (`src/three/`)**:
   - Renders dual holographic platforms representing Target A and Target B.
   - Dynamically updates capability particle beams and holographic spheres based on real-time matrix scores.
2. **Streaming Telemetry Hook (`src/hooks/useCompareStream.js`)**:
   - Establishes connection to `POST /compare/stream`.
   - Handles automatic reconnection, heartbeats, backpressure, and dispatches SSE events to React state.
3. **HITL Review Modals (`src/components/HITLModal.jsx`)**:
   - Presents non-intrusive dialogs for verifying target URLs (Checkpoint A) and adjusting comparison criteria (Checkpoint B).
   - Submits resume payloads to `POST /compare/resume`.
