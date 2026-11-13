# Criteria Aligner Prompt Specification

## Purpose
Reconciles disparate capability taxonomies extracted independently from Side A and Side B into a unified, fair, and objective comparison criteria matrix.

## Model Format
- Model: `LLM_PRIMARY_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_DEFAULT=medium`
- Note: VERIFY ON MODEL CARD for structured list generation guidelines.

## Input Variables
- `target_a_name`: Name of Side A.
- `target_b_name`: Name of Side B.
- `capabilities_a`: Extracted capabilities list for Side A.
- `capabilities_b`: Extracted capabilities list for Side B.
- `user_instructions`: Optional user emphasis or priorities.

## Output Schema
JSON list of aligned comparison criteria:
- `criterion_id`: Standardized slug.
- `criterion_name`: Display name.
- `importance`: High, Medium, or Low.
- `evaluation_guideline`: Objective criteria for scoring this dimension.
