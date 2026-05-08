---
name: debug-decision-tree
description: Hardware debug reasoning skill for natural-language bug reports, link-model analysis, hypothesis trees, action decision trees, probability/time-cost ranked troubleshooting, input cleaning, safety gating, and retrospective asset promotion. Use when Codex needs to analyze a hardware, FPGA, embedded, power, high-speed interface, video, I2C, SPI, MIPI, eDP, PCIe, USB, JTAG, or system bring-up/debug issue; when the user asks for possible causes, probabilities, measurements, debug plan, decision tree, link model, or reusable case learning; or when a terse user bug report needs a complete first-pass debug deliverable.
---

# Debug Decision Tree Skill - V0.99.6 Natural-Language Agent Contract

## Purpose

Generate complete hardware debug deliverables from ordinary user language. The user does not need to know the internal modes, asset types, or forms.

This package is still a founder-pilot candidate, not V1.0 and not a formally validated operations system. Treat its probabilities as decision priors unless calibrated by solved-case regression.

## Default User Experience

When the user gives any debug symptom, issue note, waveform description, chat excerpt, or "help me debug this" request:

1. Run Input Cleaning using `output_contracts/input_cleaning.md`.
2. Run Safety Gate before recommending actions.
3. Route using `routing/mode_router.md`.
4. Load only relevant assets after checking `reasoning/asset_priority.md`.
5. Deliver through `output_contracts/default_debug_delivery.md` and the selected mode contract.
6. Include a link model or influence map whenever the failure spans more than one component, interface, power domain, clock/reset path, or software-control boundary.
7. Include possible causes with probability estimates whenever root cause is not confirmed.
8. Include a hypothesis tree and an action decision tree in full debug outputs.
9. If details are missing, make assumptions explicit and ask at most three high-value questions after giving the first safe evidence-gathering actions.

Do not respond with only a questionnaire unless any action would be unsafe.

## Mandatory Rules

0. Run Input Cleaning before Safety Gate, mode routing, candidate matching, or debug-tree generation.
1. Preserve facts, judgments, actions tried, proposed methods, revisions, and missing information separately.
2. Run Safety Gate before any debug action.
3. Do not repeat destructive reproduction without a changed hypothesis and a documented safety envelope.
4. Use current observations over generic experience.
5. Use link models when experience is absent.
6. Do not adopt narrow assets without required evidence.
7. Always list Adopted / Deferred / Not Applied for full-tree modes.
8. Always put the optimal path before the full tree.
9. Every action node must use `output_contracts/node_table_schema.md`.
10. Every action node must include `action_type`, `tool_required`, `safety_level`, `cost`, `reversibility`, and `evidence_refs`.
11. S2/S3 nodes must include explicit safety warning or mitigation language.
12. Mermaid decision-tree node IDs must match Node Explanation Table IDs.
13. Every knowledge-linked claim must include fact source and confidence.
14. Solved cases must produce a case_record draft and regression candidate.
15. Before promoting or saving an output, run `scripts/output_validator.py` with the correct mode.
16. Full debug trees must rank early actions by probability, time cost, safety risk, and exclusion value.
17. MIPI/eDP/video failures must separate control path, power/reset/clock, source/decoder output, redriver/PHY path, receiver CDR/comma/packet/video pipeline, and downstream display/capture before blind tuning.
18. FPGA JTAG/configuration failures must separate host cable visibility, target VREF, physical JTAG path, configuration-status pins, and internal debug-node visibility before bitstream or IDE changes.

## Mode Selection Order

```text
0. Input Cleaning
1. Safety Gate
2. Signature-Based Fast Path
3. Architecture-First
4. Knowledge-Linked
5. Assumption-Driven
6. Heuristic Context
7. Retrospective after solution
```

Use `prompts/context_router.md` for general natural-language requests. Use `prompts/architecture_first.md` when the user provides a chain, module list, register state, waveform relationship, or updated debug conclusion.

Use `routing/natural_language_intent_map.md` to translate ordinary user wording into internal behavior without exposing mode names.

## Asset Types

```text
link_model       causal / architecture / dependency model
signature        strong symptom -> fast-path action cluster
case_record      solved retrospective / validated experience
pattern_bundle   article/forum/app-note pitfall or debug-pattern bundle
debug_principle  generalized cross-domain debug rule
```

## Output Expectations

Full debug outputs must distinguish:

- symptom: what failed
- root cause: only after evidence proves it
- measurement: what was observed and where
- hypothesis: plausible explanation with probability and falsifier
- action: next measurement/change with expected evidence

For unclear user input, produce a provisional result instead of blocking:

- cleaned understanding
- assumptions
- top possible causes with probabilities
- first safe measurements
- action decision tree
- missing information that would change the plan

## Validator Commands

```bash
python scripts/output_validator.py --mode input_cleaning --file cleaned.md
python scripts/output_validator.py --mode standard --file output.md
python scripts/output_validator.py --mode knowledge_linked --file output.md
python scripts/output_validator.py --mode architecture_first --file output.md
python scripts/output_validator.py --mode fast_path --file output.md
python scripts/output_validator.py --mode assumption_driven --file output.md
python scripts/output_validator.py --mode retrospective --file retrospective.md
```

Structural validation means the output matches the contract. It does not prove the reasoning is correct.
