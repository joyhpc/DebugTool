# Input Cleaning Record

## 1. Raw Input Boundary

本记录清洗一个 A57 eDP stale-evidence replay 输入。用户给出当前症状：后通道不出图、AUX 正常、AU15P CDR 不锁、comma fail、SerDes reset 无效；同时强调 aux_in 弱下拉是早期记录，当前没有同一故障窗口的新 AUX 波形或 CDR/comma 状态。

清洗目标：保留当前症状，把旧 aux_in 信息标为 stale context，不让旧证据直接改变当前概率。

## 2. Entity / Alias Normalization

| raw_entity | normalized_entity | source_in_input | note |
|---|---|---|---|
| A57 | A57 project | user replay input | 项目名 |
| eDP 后通道 | failing eDP branch | user replay input | 当前 replay 没给出完整通道矩阵 |
| AUX | DisplayPort AUX control path | user replay input | 控制/管理路径，不等同于 main data path |
| AU15P CDR/comma | AU15P SerDes RX lock/alignment status | user replay input | receiver-side status |
| aux_in 弱下拉 | prior aux_in weak-pulldown experiment | user replay input | 早期记录，非当前故障窗口证据 |

## 3. Observed / Confirmed Facts

| id | fact | source_in_input | provenance | confidence | staleness | affected_link_or_node |
|---|---|---|---|---|---|---|
| F1 | A57 eDP 后通道当前有不出图症状 | user replay input | raw_artifact | high | fresh | symptom scope |
| F2 | 用户称 AUX 正常 | user replay input | raw_artifact | high | fresh | AUX control path |
| F3 | 用户称 AU15P CDR 不锁、comma fail | user replay input | raw_artifact | high | fresh | AU15P receiver |
| F4 | SerDes reset 无效 | user replay input | raw_artifact | high | fresh | AU15P receiver reset |
| F5 | 早期发现 aux_in 初始电平差异，尝试弱下拉没有解决 | user replay input | derived | medium | requires_re_verification | stale aux_in context |
| F6 | 当前没有同一故障窗口的新 AUX 波形 | user replay input | raw_artifact | high | fresh | evidence gap |
| F7 | 当前没有同一故障窗口的新 AU15P CDR/comma 状态 | user replay input | raw_artifact | high | fresh | evidence gap |

## 4. Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | 当前应优先切分 decoder output、path/Redriver、AU15P input、AU15P RX，而不是把 AUX 或 aux_in 作为主因 | F1,F2,F3,F4,F5 | medium | 同一故障窗口 AUX 波形显示 AUX retry/NACK/status stale，或 aux_in 电平在当前窗口直接影响训练状态 |
| J2 | 旧 aux_in 弱下拉信息只能形成 re-verification gap，must not directly change probabilities | F5,F6 | high | 新同窗口波形证明 aux_in 异常与当前失败同步 |
| J3 | CDR/comma fail 是 receiver-side symptom，不证明 decoder output 或 AU15P input 已有效 | F3,F7 | high | 同一故障窗口捕获到 AU15P input 有效且只有 CDR/comma 失败 |

## 5. Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | SerDes reset | AU15P receiver | 无改善 | reset 无法单独恢复，但不能证明 receiver 是 root cause | F4 |
| M2 | 早期 aux_in 弱下拉尝试 | aux_in prior branch | 未解决 | stale context；不能直接更新当前概率 | F5,F6 |

## 6. Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | 在同一失败窗口记录 decoder output/status、Redriver/path、AU15P input、AU15P CDR/comma | not stated | data-path boundary split | 同一 timestamp 下的 first-fail boundary | B1/B2/B3/B4 |
| P2 | 重新采集 AUX 波形和 status readback，仅用于复核 stale aux_in/AUX context | not stated | AUX control path | AUX retry/NACK/status 是否与当前失败同步 | stale context / observability gap |

## 7. Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | 旧 aux_in 初始电平差异可能影响判断 | aux_in 弱下拉是早期记录，当前没有同一故障窗口波形 | F5,F6 | 旧 aux_in 分支降为 requires_re_verification，不参与当前概率升降 |

## 8. Missing Information

| id | missing_information | why_it_matters |
|---|---|---|
| G1 | 同一故障窗口 decoder output/status、Redriver/path、AU15P input、AU15P CDR/comma | 直接切 first-fail boundary |
| G2 | 同一故障窗口 AUX waveform/status readback | 复核 F5 stale aux_in/AUX context，防止旧证据误导 |
| G3 | eDP 通道/板卡/测试次数矩阵 | 防止单次症状被写成共性模式 |

## 9. Router-Ready Case Brief

A57 eDP 后通道不出图，用户报告 AUX 正常、AU15P CDR 不锁、comma fail，SerDes reset 无效。早期 aux_in 初始电平差异和弱下拉无改善是 stale context，已标记 `requires_re_verification`；在当前没有同一故障窗口 AUX 波形前，它 must not directly change probabilities。下一步应走 Architecture-First：同窗口切分 decoder output/status、Redriver/path、AU15P input、AU15P RX CDR/comma，并把 AUX/aux_in 作为待复核的 observability gap。

