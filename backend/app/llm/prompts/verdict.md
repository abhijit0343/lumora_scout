# Comparative Verdict Prompt Specification

## Purpose
Synthesizes the final comparative evaluation, weighing capabilities, quantitative scores, grounding context, and trade-offs into an executive verdict and recommendation.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_VERDICT=high`
- Note: VERIFY ON MODEL CARD for streaming token generation settings and reasoning token output tags.

## Input Variables
- `target_a`: Canonical name and details of Target A.
- `target_b`: Canonical name and details of Target B.
- `aligned_matrix`: Populated capability comparison matrix with evidence.
- `scores`: Aggregated scores and similarity percentages.
- `rag_grounding`: Evidence from uploaded reference documents.

## Output Structure
Markdown-formatted analysis containing:
- Executive Summary & Overall Winner.
- Strengths & Differentiators for Target A.
- Strengths & Differentiators for Target B.
- Critical Trade-offs (Pricing vs Features, Complexity vs Simplicity).
- Final Recommendation Persona Guide ("Choose A if... Choose B if...").
