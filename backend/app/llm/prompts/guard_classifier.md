# Guardrail Classifier Prompt Specification

## Purpose
Performs high-speed adversarial safety screening on user inputs and scraped content to detect prompt injections, jailbreaks, malicious instruction overrides, and policy violations.

## Model Format
- Model: `GUARD_CLASSIFIER_MODEL` (`gemini-3.8-flash`)
- Thinking Level: `LLM_THINKING_LEVEL_GUARD=low`
- Note: VERIFY ON MODEL CARD for safety evaluation prompt formats and system role overrides.

## Input Variables
- `text_payload`: Text string to evaluate (user input or scraped HTML snippet).
- `evaluation_layer`: Guardrail layer identifier (`L1_INPUT` or `L3_CONTENT`).

## Output Schema
JSON object:
- `is_safe`: Boolean indicator (`true` or `false`).
- `confidence`: Float between 0.0 and 1.0.
- `violation_category`: Categorical tag (`prompt_injection`, `jailbreak`, `illicit_content`, `pii_leakage`, `none`).
- `explanation`: Brief technical justification for the determination.
