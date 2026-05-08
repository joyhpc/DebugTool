# Default Natural-Language Debug Delivery Contract

Use this contract when a user gives a bug report in plain language and does not explicitly ask for a narrower output.

The user should not need to know mode names. Convert the raw request into a complete debug deliverable.

```md
# Debug Case Delivery

## 1. Cleaned Understanding
## 2. Safety Gate
## 3. Selected Mode And Why
## 4. Link Model / Influence Map
## 5. Known Facts vs Assumptions
## 6. Possible Causes With Probability Estimates
## 7. Hypothesis Tree
## 8. Action Decision Tree
## 9. First Actions And Expected Evidence
## 10. Missing Information That Would Change The Plan
## 11. Stop / Escalation Conditions
## 12. Follow-Up Update Format
```

Rules:

- Do not answer with only questions unless the input is safety-critical and action would be dangerous.
- Match the user's language for prose. Keep fixed headings or machine-checked fields in the required form if needed for validation.
- If the user gives a vague symptom, build a provisional model and ask at most three high-value questions.
- If the user gives a chain, module list, register state, waveform, log, or "latest conclusion", use Architecture-First.
- If the root cause is unknown, always include possible causes, probabilities, and an action decision tree.
- If a prior assumption was revised by new evidence, explicitly lower or remove stale branches.
- Keep the top answer operational: what to measure next, where to measure, what result means, and which branch it affects.
