# A57 eDP Visual Architecture Brief

## Artifact Navigation

- Start here for system placement, subsystem ownership, and Mode A / Mode B routing.
- Then read `latest-architecture-first.md` for detailed boundary/mechanism reasoning.
- Use `field-action-plan.md` for same-window evidence capture and stop conditions.
- Use `latest-input-cleaning.md` for raw-fact provenance and stale evidence handling.
- Return to `README.md` for the full case index and archive list.

## 0. Executive Frame

当前 A57 eDP bug 先按 **Mode A: CR/EQ fail + 持续 training pattern + 无图** 处理。

关键判断：在当前实现里，CR/EQ pass/fail 不是 SerDes/Main Link 的真实闭环反馈，而是 FPGA/DPCD responder 通过 AUX 返回给 A57 Source 的合成训练状态。因此，当前 bug 首先落在 **training-control plane**，不是 AU15P/SerDes 眼图或 Redriver 主数据链。

行动路线：

1. 先拿 A57 driver 的精确 fail reason。
2. 同窗口抓成功/失败 AUX transaction diff。
3. 审 FPGA/DPCD responder 的 status-map 和 lane/rate/training-stage 语义。
4. 同窗口测 AUX+/AUX-/HPD 波形、温度、机械扰动。
5. 如果 AUX 物理和 status-map 干净，再查 responder timing race / stale status。
6. 只有 CR/EQ 稳定 pass 但仍无图，才切到 Mode B 的 DS90UB984 -> Redriver -> AU15P 主数据链。

## 1. System Placement

```mermaid
flowchart LR
  subgraph SYS["A57 eDP debug system"]
    SRC["A57 eDP Source\nDriver + link-training FSM"]

    subgraph TCP["Mode A: training-control plane\ncurrent bug lives here until proven otherwise"]
      AUXPHY["AUX+/AUX-/HPD\nphysical layer"]
      AUXFE["FPGA AUX front-end\ntransaction decode"]
      DPCD["FPGA/DPCD responder\nsynthetic CR/EQ status"]
      LOG["Responder log\nstatus update timestamp"]
    end

    subgraph MDP["Mode B: main data path\nonly after CR/EQ is stable pass"]
      DS90A["DS90UB984-A\neDP1/eDP2"]
      DS90B["DS90UB984-B\neDP3/eDP4"]
      RED["Redriver\nstatic PWDN/I2C/EQ/path"]
      AU15P["AU15P / FPGA RX\ninput CDR comma lane status"]
      VID["PCS / video valid / display"]
    end
  end

  SRC -->|"AUX read/write\nDPCD link training"| AUXPHY
  AUXPHY --> AUXFE
  AUXFE --> DPCD
  DPCD -->|"CR_DONE / EQ_DONE / SYMBOL_LOCKED\nLANE_ALIGN / ADJUST_REQUEST"| SRC
  DPCD -.->|"status not derived from"| AU15P
  AUXFE --> LOG
  LOG --> DPCD

  SRC -->|"Main Link training pattern / video"| DS90A
  SRC -->|"Main Link training pattern / video"| DS90B
  DS90A --> RED
  DS90B --> RED
  RED --> AU15P
  AU15P --> VID
```

读图方式：如果 A57 driver 仍报 CR/EQ fail，Source 还没有稳定进入正常视频阶段。此时主数据链上的 DS90UB984、Redriver、AU15P 可以保留为背景，但不能作为第一 root-cause 路径。

## 2. Mode A Subsystem Architecture

```mermaid
flowchart TD
  A0["A57 driver starts link training"] --> A1["Write link rate / lane count\nDPCD 0x100 / 0x101"]
  A1 --> A2["Write TRAINING_PATTERN_SET\nDPCD 0x102 / 0x108"]
  A2 --> A3["Read lane status\nDPCD 0x202-0x207"]

  subgraph FAIL["Mode A first-fail boundaries"]
    TB1["TB1 AUX/HPD physical\nlevel, common-mode, glitch, HPD bounce"]
    TB2["TB2 DPCD status-map\nCR/EQ/lane-align bits incomplete"]
    TB3["TB3 responder timing\nrace, stale status, CDC issue"]
    TB4["TB4 training semantic mismatch\nrate, lane count, TPS, ADJUST_REQUEST"]
    TB5["TB5 shared margin\npower, clock, reset, temperature"]
  end

  A3 --> D0{"Driver sees complete pass state?"}
  D0 -->|"No: AUX fail / bad status / HPD event"| TB1
  D0 -->|"No: status bits not accepted"| TB2
  D0 -->|"Intermittent by timing / temperature"| TB3
  D0 -->|"Phase or lane/rate mismatch"| TB4
  D0 -->|"Correlates with common rails/temp"| TB5
  D0 -->|"Yes, CR/EQ stable pass"| MB["Enter Mode B main data path"]
```

Mode A 的最短闭环不是“继续猜哪个芯片坏”，而是把 driver 看到的 failure type、AUX transaction、DPCD 返回值、HPD/AUX 波形、responder 状态更新时间对齐到同一个 timestamp。

## 3. Mode Gate

```mermaid
flowchart TD
  S0{"Current visible symptom?"}
  S0 -->|"CR/EQ fail\ntraining pattern loops\nno image"| A["Mode A\ntraining-control batch"]
  S0 -->|"CR/EQ pass\nbut no image"| B["Mode B\nmain-data-path batch"]

  A --> A1["Driver fail reason"]
  A1 --> A2["AUX transaction pass/fail diff"]
  A2 --> A3["DPCD status-map audit"]
  A3 --> A4["AUX/HPD waveform + environment"]
  A4 --> A5["FPGA responder timing log"]
  A5 --> G{"Source reads and accepts\ncomplete pass state?"}

  G -->|"No"| FIXA["Fix AUX/HPD, DPCD map,\nresponder timing, or training semantics"]
  G -->|"Yes, CR/EQ stable pass"| B

  B --> B1["DS90UB984 per-channel raw status"]
  B1 --> B2["DS90UB984 rails reset refclk PLL"]
  B2 --> B3["Redriver PWDN I2C EQ input/output"]
  B3 --> B4["AU15P input CDR comma lane status"]
  B4 --> FIXB["Fix first invalid main-data boundary"]
```

工程原则：Mode A 未闭合时，Mode B 的主链路观测只能作为旁证；它不能解释 Source 为什么没有接受 CR/EQ pass。

## 4. High-Signal Evidence Stack

| priority | evidence | answers | if failing | if clean |
|---:|---|---|---|---|
| 1 | A57 driver fail reason | Source 到底拒绝了什么 | 分流到 AUX fail、status bit fail、HPD event、lane-align fail | 进入 transaction diff |
| 2 | AUX transaction diff | Source 实际读写到了什么 | NACK/DEFER/timeout/retry 或字节差异直接定位 | 进入 status-map / timing |
| 3 | DPCD status-map audit | responder 是否给了 Source 认可的完整 pass | 修 CR/EQ/lane-align/ADJUST_REQUEST/rate/lane 映射 | 进入物理和 timing |
| 4 | AUX+/AUX-/HPD waveform | 是否是物理层边际 | 修 AUX/HPD 电平、终端、共模、毛刺、去抖、连接器 | 降低 TB1，进入 responder race |
| 5 | FPGA responder log | 是否返回过早、过晚、stale、CDC 不稳 | 加 hold-off、DEFER、同步器、状态更新时间约束 | Mode A 基本闭合 |

## 5. Subsystem Conclusions

当前最该被画出来的架构不是完整视频链路，而是 **A57 Source link-training FSM 与 FPGA/DPCD responder 的控制闭环**。这是 bug 的第一系统边界。

主数据链仍然重要，但它现在是第二层：

- 如果 CR/EQ fail，优先系统是 AUX/DPCD/HPD/responder。
- 如果 CR/EQ pass 仍无图，优先系统才是 DS90UB984/Redriver/AU15P。

这个框架避免两个常见误判：

- 把温度敏感直接等同于 SerDes 眼图差。
- 把 FPGA 理论上“固定返回 OK”误当作 Source 已经实际读到并接受 OK。

## 6. Field Brief

给现场的第一句话：

> 这不是先查“为什么没图”的问题，而是先查“为什么 A57 Source 没有接受训练通过状态”的问题。

当天最小任务：

1. 打开 driver debug，拿到具体 fail reason。
2. 抓一组 pass 和一组 fail 的 AUX transaction。
3. 对照 DPCD `0x100/0x101/0x102/0x108/0x200-0x207`。
4. 同窗口测 AUX+/AUX-/HPD。
5. 导出 FPGA responder 的状态更新时间和返回值。

当天 stop 条件：

- 没有 driver fail reason，不继续争论 SerDes、Redriver 或 DS90UB984。
- 没有 AUX transaction diff，不声称 FPGA 已稳定把 CR/EQ OK 送到 Source。
- CR/EQ 没有稳定 pass，不把 AU15P CDR/comma 当主路径。
