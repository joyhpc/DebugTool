# Input Cleaning Record

## 1. Raw Input Boundary

本记录清洗一个 synthetic dry-run 输入，不是真实已验证项目案例：

> 交换机在长时间工作后，出现概率性丢包的现象。100 台里面有一台。交换机芯片方案用的 rtl8370。

输入目前只包含自然语言现象和一个芯片方案名称；没有日志、抓包、端口计数器、温度、电源、链路状态、具体流量模型或复现时间。

## 2. Entity / Alias Normalization

| raw_entity | normalized_entity | source_in_input | note |
|---|---|---|---|
| 交换机 | switch unit | user synthetic case | 被测整机或板卡 |
| 长时间工作 | long-uptime operation | user synthetic case | 具体时长未给出 |
| 概率性丢包 | intermittent packet loss | user synthetic case | 未说明是单端口、全局、单方向还是特定流量 |
| 100 台里面有一台 | 1/100 affected sample distribution | user synthetic case | 样本分布线索，不等于 root cause |
| rtl8370 | RTL8370 switch-chip scheme | user synthetic case | 仅作为本案例 subsystem alias，不使用外部 datasheet 假设 |

## 3. Observed / Confirmed Facts

| id | fact | source_in_input | provenance | confidence | staleness | affected_link_or_node |
|---|---|---|---|---|---|---|
| F1 | 交换机长时间工作后出现概率性丢包 | user synthetic case | team_attestation_unverified | medium | fresh | symptom / data path |
| F2 | 当前描述为 100 台里面有一台出现该现象 | user synthetic case | team_attestation_unverified | medium | fresh | sample distribution |
| F3 | 交换机芯片方案使用 RTL8370 | user synthetic case | team_attestation_unverified | medium | fresh | switch subsystem alias |
| F4 | 未提供具体端口、方向、流量类型、丢包率、工作时长、温度、电源和日志 | absence in input | derived | high | fresh | observability gap |

## 4. Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | 这个 case 更适合 Architecture-First，而不是 signature fast path | F1,F2,F4 | medium | 后续出现明确已知签名，例如固定端口 PHY error 或固定配置项错误 |
| J2 | 1/100 分布使单台样本差异、装配、热/电源/时钟 margin、端口链路 margin 比全局配置 bug 更优先 | F2 | medium | 完整矩阵显示同批次多台在相同 uptime 和流量下都有同类丢包 |
| J3 | 长时间工作后才出现，提升热漂移、资源泄漏、计数器/表项状态、配置保持性或链路 margin 的优先级 | F1 | medium | 同窗口日志显示丢包从上电即存在或只与外部测试设备有关 |
| J4 | 目前不能把 RTL8370 本体定为 root cause，因为端口链路、测试仪、板级供电/时钟/温度和配置状态都没有闭合 | F3,F4 | high | 同窗口证据证明外部链路与板级前提全部正常且芯片内部 drop/error 状态异常 |

## 5. Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | not stated | switch packet-loss case | not stated | 当前没有已完成测量，不能排除任何边界 | F4 |

## 6. Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | 建立 100 台样本中的 unit/port/traffic/uptime/fail_count 矩阵 | not stated | sample distribution | 区分单台、单端口、单方向、流量相关或测试环境相关 | B0/M5 |
| P2 | 对故障窗口做同时间抓包和端口统计快照 | not stated | data path boundary | 判断包是在 ingress、switch forwarding、egress、PHY/link 还是测试端丢失 | B2/B3/B4 |
| P3 | 长时间运行期间记录温度、电源、时钟、link status 和 error/drop counters | not stated | uptime drift / prerequisites | 判断是否存在热漂移、电源/时钟 margin、PHY error 或内部 drop 计数上升 | M1/M2/M3 |
| P4 | 比较故障机和相邻正常机的配置 readback、固件版本、strap/EEPROM/board revision | not stated | configuration / sample delta | 判断是否有单台配置差异或状态保持异常 | M4/M5 |

## 7. Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | not stated | not stated | 当前输入没有旧结论或修订 | 无 |

## 8. Missing Information

| id | missing_information | why_it_matters |
|---|---|---|
| G1 | 长时间工作具体时长、出现前后的温度、环境、负载和供电条件 | 区分热/电源/时钟 drift 与纯流量相关问题 |
| G2 | 丢包是单端口、某方向、某 VLAN/队列、广播/单播，还是全局随机 | 决定 first-fail boundary 在 PHY、port、forwarding、queue、CPU/control 还是测试设备 |
| G3 | 故障窗口的 ingress/egress 抓包、序号、端口 MIB、drop/error/CRC/alignment/link flap counters | 同窗口判断包第一次在哪里消失 |
| G4 | 故障机和正常机的配置 readback、固件、strap/EEPROM、板卡版本、物料和生产批次差异 | 判断 1/100 是否来自样本差异或配置差异 |
| G5 | 是否替换网线、端口、流量仪、对端设备后故障跟随 | 防止把测试夹具或外部链路误判为交换机问题 |

## 9. Router-Ready Case Brief

这是一个 synthetic dry-run：交换机在长时间工作后概率性丢包，100 台中 1 台出现，芯片方案名称为 RTL8370。当前没有同窗口抓包、端口计数器、温度、电源、时钟、link 状态、配置 readback 或测试矩阵。应按 Architecture-First 处理：先建立 sample/port/traffic/uptime/fail matrix，再在同一故障窗口采集 ingress/egress 抓包、端口 MIB/drop/error counters、link/PHY 状态、温度/电源/时钟和配置 readback。当前不能把 root cause 归到芯片本体，也不能排除测试设备、外部链路、单台板级 margin 或配置保持性。
