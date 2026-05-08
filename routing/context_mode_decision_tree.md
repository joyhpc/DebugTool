# Context Mode Decision Table

| Condition | Mode | Required Output |
|---|---|---|
| Safety trigger | Safety Gate first | safety_level, forbidden actions |
| Strong signature | Fast Path | top actions, stop/escalate |
| Current architecture provided | Architecture-First | fault-domain map |
| Project knowledge available | Knowledge-Linked | fact table with sources |
| Classic link model fits | Assumption-Driven | assumptions to confirm |
| Too vague | Heuristic | provisional path plus at most 3 high-value questions |

Default behavior: a vague user bug report is not a blocker. Produce a bounded first-pass result with cleaned facts, assumptions, likely causes, first measurements, and the exact missing information that would change the tree.
