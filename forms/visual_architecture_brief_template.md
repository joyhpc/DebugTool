# Visual Architecture Brief Template

Use this template when a debug case is complex enough that readers need to know which system, subsystem, or mode currently owns the bug before reading detailed evidence tables.

Keep this template generic. Put project-specific device names, signal names, rails, channels, and owners in the case artifact, not in this template.

## 0. Executive Frame

Current conclusion:

- current visible symptom:
- current owning system:
- current owning subsystem:
- current mode / gate:
- strongest reason:
- first action:
- stop condition:

Action route:

1. TBD
2. TBD
3. TBD

## 1. System Placement

Use this diagram to show where the bug currently lives in the full system.

```mermaid
flowchart LR
  SRC["source / controller"]

  subgraph CONTROL["control / training / command plane"]
    CTRL_PHY["control physical layer"]
    CTRL_FSM["control transaction decoder"]
    CTRL_RESP["status responder / control state"]
  end

  subgraph DATA["data / power / functional plane"]
    DEV_A["active device or endpoint A"]
    PATH["conditioner / mux / path"]
    RX["receiver / sink"]
    OUT["functional output"]
  end

  SRC -->|"control transactions"| CTRL_PHY
  CTRL_PHY --> CTRL_FSM
  CTRL_FSM --> CTRL_RESP
  CTRL_RESP -->|"status / handshake"| SRC

  SRC -->|"data / functional traffic"| DEV_A
  DEV_A --> PATH
  PATH --> RX
  RX --> OUT
```

Reader note:

- If the current visible symptom is a control-plane failure, do not route first to the data plane.
- If the control plane is proven closed and the symptom remains, then move to the data plane.

## 2. Subsystem Architecture

Use this diagram to expand the currently owning subsystem.

```mermaid
flowchart TD
  S0["reproduction trigger"] --> S1["first transaction or state change"]
  S1 --> S2["status / measurement / readback"]
  S2 --> D0{"expected state accepted?"}

  D0 -->|"No: physical / transport failure"| B1["boundary 1 physical or transport"]
  D0 -->|"No: status content mismatch"| B2["boundary 2 status map or semantic mismatch"]
  D0 -->|"No: timing dependent"| B3["boundary 3 timing, stale state, CDC"]
  D0 -->|"Yes, symptom moves downstream"| NEXT["enter next system mode"]
```

## 3. Mode Gate

The mode gate is the top-level router. It should make it obvious when to stay in the current subsystem and when to switch.

| mode | visible symptom | first subsystem | required evidence batch | stop condition |
|---|---|---|---|---|
| Mode A |  |  |  |  |
| Mode B |  |  |  |  |

```mermaid
flowchart TD
  G0{"current visible symptom?"}
  G0 -->|"Mode A symptom"| A["Mode A evidence batch"]
  G0 -->|"Mode B symptom"| B["Mode B evidence batch"]
  A --> GA{"Mode A closed?"}
  GA -->|"No"| FA["fix Mode A boundary"]
  GA -->|"Yes"| B
  B --> FB["fix first invalid Mode B boundary"]
```

## 4. High-Signal Evidence Stack

Keep this table short. It is the first set of evidence a senior engineer would ask for.

| priority | evidence | answers | if failing | if clean |
|---:|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

## 5. Subsystem Conclusions

Write the highest-signal conclusion in plain language:

- current first subsystem:
- current non-goals:
- conditions to change route:
- most likely mistake to avoid:

## 6. Field Brief

One sentence for the field team:

> TBD

Minimum same-window tasks:

1. TBD
2. TBD
3. TBD

Stop conditions:

- TBD
- TBD
- TBD
