# Mode Router

## Decision Order

```mermaid
flowchart TD
S([Natural-language debug problem]) --> C0[Input Cleaning]
C0 --> D0{Safety trigger?}
D0 -- Yes --> A0[Apply Safety Gate]
D0 -- No --> D1{Strong diagnostic signature?}
A0 --> D1
D1 -- Yes --> M1[Signature-Based Fast Path]
D1 -- No --> D2{Current architecture provided?}
D2 -- Yes --> M2[Architecture-First Mode]
D2 -- No --> D3{Project KB/docs/repo available?}
D3 -- Yes --> M3[Knowledge-Linked Mode]
D3 -- No --> D4{Classic link model can be assumed?}
D4 -- Yes --> M4[Assumption-Driven Mode]
D4 -- No --> M5[Heuristic Context Mode with provisional plan]
```

Current user-provided architecture takes priority over potentially stale KB.

## Natural-Language Default

Do not require the user to name a mode. If the user only says "help debug this" or provides a brief symptom, run Input Cleaning, choose the strongest available mode, and deliver a provisional plan with assumptions. Ask questions only after giving the first safe evidence-gathering actions.
