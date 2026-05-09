# Input Cleaning Record

## 1. Raw Input Boundary

本记录清洗 Issue4 中 A57 eDP 问题的新补充。新输入不是一个全新硬件案子，而是对既有 A57 eDP case 的 evidence update：

- 新增 DS90UB984 与 eDP1/2、eDP3/4 的架构映射；
- 新增 4 块解码板、多通道概率性异常和板间差异；
- 新增 Redriver 配置时序边界；
- 新增重复测试方式；
- 新增当前项目事项表和部分已完成/待完成状态。

清洗原则：保留用户原文中的事实、判断、已完成动作和计划动作；把“责任人”按项目表记录，但后续输出中仍应区分正式 owner 与候选执行人；旧 A57 结论只作为 context，除非本次补充重新确认，否则不直接更新概率。

## 2. Entity / Alias Normalization

| raw_entity | normalized_entity | source_in_input | note |
|---|---|---|---|
| A57 | A57 项目 | user update | 项目名 |
| edp1, edp2 | DS90UB984-A 对应的两个 eDP 输出/通道 | user update | 同一颗 DS90UB984 解码芯片 |
| edp3, edp4 | DS90UB984-B 对应的两个 eDP 输出/通道 | user update | 另一颗 DS90UB984 解码芯片 |
| 984 / ds90ub984 / 解码芯片 | DS90UB984 decoder | user update | 具体芯片料号已从泛称“984”明确为 DS90UB984 |
| 解码板 | DS90UB984 decoder board | user update | 多块板参与验证 |
| redriver | eDP mainstream 中间 Redriver | user update | 设备上电后配置一次，重复测试期间不重新配置 |
| 重复测试 | 对 DS90UB984 重新上下电和重新配置 | user update | 不是整机重新上电，也不是 Redriver 重新配置 |
| 出图异常 / 无法出图 | eDP display-output failure | user update | 概率性通道输出异常 |

## 3. Observed / Confirmed Facts

| id | fact | source_in_input | provenance | confidence | staleness | affected_link_or_node |
|---|---|---|---|---|---|---|
| F1 | A57 eDP 出图异常是当前 Issue4 的目标 case | user update | raw_artifact | high | fresh | case scope |
| F2 | eDP1、eDP2 对应解码板上的一颗 DS90UB984 解码芯片 | user update | raw_artifact | high | fresh | decoder mapping |
| F3 | eDP3、eDP4 对应解码板上的另一颗 DS90UB984 解码芯片 | user update | raw_artifact | high | fresh | decoder mapping |
| F4 | eDP1、eDP2、eDP3、eDP4 都有概率出现问题 | user update | raw_artifact | high | fresh | symptom distribution |
| F5 | 一共测试了 4 块解码板，板间表现出差异 | user update | raw_artifact | high | fresh | multi-board matrix |
| F6 | 有一块板表现为 eDP3、eDP4 出图异常概率较高 | user update | raw_artifact | high | fresh | board-to-board variation |
| F7 | 另外三块板表现为 eDP1、eDP2 出图异常概率较高 | user update | raw_artifact | high | fresh | board-to-board variation |
| F8 | 同一颗 DS90UB984 对应的 eDP1/eDP2 没有严格一致性，出现一个好、一个不好的情况 | user update | raw_artifact | high | fresh | per-channel variation |
| F9 | eDP3/eDP4 同样没有严格一致性，也会出现同芯片下一个好、一个不好 | user update | raw_artifact | high | fresh | per-channel variation |
| F10 | eDP mainstream 中间有 Redriver | user update | raw_artifact | high | fresh | Redriver / data path |
| F11 | Redriver 在设备上电后已经配置好，后续重复测试中并未重新配置 | user update | raw_artifact | high | fresh | Redriver config boundary |
| F12 | 当前重复测试方式是对 DS90UB984 解码芯片重新上下电和重新配置 | user update | raw_artifact | high | fresh | decoder power/reconfig loop |
| F13 | eDP 上电时序测量需要包含 SerDes 参考时钟，当前计划责任人为吴峰，日期 2026/5/9 | project action table | raw_artifact | high | fresh | power/reset/clock |
| F14 | 前后 2 通道 eDP SerDes 电路差异已确认无差异 | project action table | raw_artifact | high | fresh | circuit comparison |
| F15 | Redriver 4 通道上电 PWDN 信号及 I2C/出图 PWDN 信号仍待确认 | project action table | raw_artifact | high | fresh | Redriver PWDN/control |
| F16 | 项目表写有“多测试几块 984 解码板【6块】”，但本次补充明确已经测试 4 块 | project action table + user update | raw_artifact | medium | fresh | sample count |
| F17 | 多板测试现象包括“单独勾选无法出图”，且目前没有一块可以稳定 4 通道出图 | project action table | raw_artifact | high | fresh | reproduction matrix |
| F18 | 前 2 通道 eDP DS90UB984 IIC 指令与后 2 通道 IIC 指令对比已完成，指令和 ini/-参数下发未发现问题 | project action table | raw_artifact | high | fresh | IIC/config intent |
| F19 | 读 eDP 解码芯片相关寄存器，以及模拟出图输出相关寄存器是否存在，需要和厂家确认 | project action table | raw_artifact | high | fresh | decoder status/readback |
| F20 | DS90UB984 关键管脚测量仍待硬件确认 | project action table | raw_artifact | high | fresh | pin/power/reset/clock |
| F21 | 旧版 A57 context 中曾有 AUX 正常、AU15P CDR/comma 异常、SerDes reset 无改善等信息 | previous A57 latest | derived | medium | requires_re_verification | prior receiver symptom |

## 4. Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | 这个 case 应从“后两通道问题”改写为“四个 eDP 都可能概率性出图异常，概率随板和通道变化” | F4,F5,F6,F7 | high | 后续完整矩阵显示只有某个固定通道组失败 |
| J2 | “一颗 DS90UB984 整体异常导致同芯片两个通道一起坏”的解释被削弱 | F8,F9 | medium | 同芯片内部状态读回显示两个通道共享的 PLL/reset/output block 异常且能解释不一致现象 |
| J3 | per-channel mainstream path、DS90UB984 单通道 output state、lane mapping/SI、AU15P input 边界应升为优先切分对象 | F4,F8,F9,F14,F17,F21 | high | 同一故障窗口证明每个通道的 decoder output 和 AU15P input 都稳定有效 |
| J4 | Redriver“动态重新配置错误”分支应降级，因为重复测试期间 Redriver 不重新配置 | F10,F11,F12 | high | 发现重复测试过程中 Redriver 仍被隐式改写、复位或 PWDN 抖动 |
| J5 | Redriver 仍不能排除，因为静态 PWDN、I2C 初始化、通道使能、EQ、path 和 output activity 仍未闭合 | F10,F11,F15 | high | 同一故障窗口证明 PWDN/I2C/static config、Redriver input/output 全部正确 |
| J6 | IIC 指令/ini 参数对比完成会降低“前后两颗 decoder 下发参数明显不同”的概率，但不能替代故障态 readback/status | F18,F19 | high | 故障态 readback 发现参数未保持、关键状态异常或厂家确认缺失寄存器 |
| J7 | 板间表现差异说明不能把问题简单归为单板问题或共性设计问题，需要按 board_id、chip_id、channel_id 建矩阵 | F5,F6,F7,F17 | high | 后续 6 块或更多板显示稳定单一模式 |
| J8 | 当前仍不能下 root cause 结论；最有价值的是把 decoder channel output、Redriver output、AU15P input、receiver lock 放到同一故障窗口里切边界 | F4,F8,F9,F15,F19,F20,F21 | high | 任一待测项直接给出可复现的故障机制 |

## 5. Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | 测试 4 块 DS90UB984 解码板 | board/sample variation | 4 块板都有异常表现，且板间异常倾向不同 | 从单板样本升级为多板概率性问题，但仍需完整 test count/fail count 矩阵 | F5,F6,F7,F17 |
| M2 | 观察同一 DS90UB984 下两个 eDP 通道的一致性 | chip-level commonality | eDP1/2 和 eDP3/4 都可出现一个好、一个不好 | 削弱整颗 decoder 共同前提失效作为唯一解释，提升 per-channel 边界 | F8,F9 |
| M3 | 重复测试时对 DS90UB984 重新上下电和重新配置 | decoder reinit loop | 重复过程中仍出现概率性出图异常 | 失败与 decoder power/reconfig loop 强相关；Redriver 动态 reconfig 不是当前重复变量 | F11,F12 |
| M4 | 确认前后 2 通道 eDP SerDes 电路差异 | SerDes circuit path | 已确认无差异 | 降低“前后通道电路设计差异”作为主因，但不排除板级装配/SI/通道路径差异 | F14 |
| M5 | 对比前 2 通道与后 2 通道 DS90UB984 IIC 指令、ini 和参数下发 | IIC/config intent | 未发现问题，已完成 | 降低“显式指令/参数不同”分支，但 readback/status 仍待查 | F18,F19 |

## 6. Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | 补齐 4/6 块解码板的 board_id、DS90UB984 chip_id、channel_id、test_count、fail_count、fail_condition 矩阵 | 吴志安 / 陈斌 per project table | multi-board reproduction matrix | 每个通道的失败率、板间差异和是否能稳定 4 通道出图 | B0/M5 |
| P2 | 测量 eDP 上电时序，包含 DS90UB984 rails、reset、refclk/PLL、SerDes 参考时钟和关键 enable | 吴峰 per project table | power/reset/clock prerequisites | good/fault 对比 timing waveform 和状态表 | M1 |
| P3 | 确认 Redriver 4 通道上电 PWDN、I2C 初始化状态、出图相关 PWDN 信号，以及重复测试期间是否保持不变 | 吴峰 per project table | Redriver static config/PWDN | PWDN/I2C/static config/input-output coverage note | B3/M4 |
| P4a | 先读取 DS90UB984 故障态所有可访问关键寄存器，不等待厂家解释 | 陈斌 per project table | decoder channel status/output | per-channel raw readback dump | B1/B2/M2/M3 |
| P4b | 和厂家确认是否存在模拟出图输出、stream-detect、output-valid、error/status 相关寄存器及解释 | 陈斌 per project table | decoder register semantics | vendor confirmation mapped back to P4a dump | M3 |
| P5 | 测量 DS90UB984 关键管脚 | 陈斌、吴峰 per project table | decoder pins and prerequisites | per-pin voltage/timing/pass-fail table | B1/B2/M1 |
| P6 | 在同一故障窗口记录 DS90UB984 output-valid/Redriver output/AU15P input/CDR/comma 状态 | candidate: 吴峰 + FPGA debug owner, PM/project lead to confirm | data boundary split | decoder output valid? Redriver output valid? AU15P input valid? receiver lock? | B1/B2/B3/B4/B5/M1-M6 |

## 7. Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | 旧输出把 case 主要描述为 eDP 后两通道问题 | 新补充表明 eDP1、eDP2、eDP3、eDP4 都有概率出现问题 | F4,F5,F6,F7 | 输出范围改为四通道概率性出图异常，不能继续只按后两通道建模 |
| R2 | 旧输入中 eDP1/eDP2 曾作为前通道稳定对照 | 新补充显示三块板上 eDP1/eDP2 异常概率反而较高 | F6,F7 | 前/后通道对照轴降级，board/chip/channel 矩阵升级 |
| R3 | 可能把一颗 DS90UB984 的两个通道视为强一致单元 | 同一芯片下两个通道没有严格一致性 | F8,F9 | decoder-chip-level global branch 降级，per-channel branch 升级 |
| R4 | Redriver 控制/配置可能被当作重复测试变量 | Redriver 设备上电后配置好，后续并未重新配置；重复变量是 DS90UB984 上下电和重新配置 | F10,F11,F12 | Redriver 动态 reconfig 分支降级，Redriver static path/PWDN 仍保留 |
| R5 | 项目表中有“6块”计划和“2块板子多块板子测试”等表述 | 本次补充明确“一共测试了4块解码板”，但仍有另外 2 块待确认计划 | F5,F16 | 需要规范化 sample matrix，避免 test count 混乱影响结论 |

## 8. Missing Information

| id | missing_information | why_it_matters |
|---|---|---|
| G1 | 4 块已测板和计划 6 块之间的完整 board_id/test_count/fail_count/channel matrix，并标明同芯片内具体哪个 channel failed | 用于区分共性、板差、通道差、同芯片通道差和样本偏差 |
| G2 | 每次失败是否来自同一故障窗口的 DS90UB984 status、Redriver status、AU15P CDR/comma | 防止 stale evidence 影响概率 |
| G3 | DS90UB984 两颗芯片的供电、reset、refclk/PLL、SerDes 参考时钟时序对比 | 判断重复上下电/重配置是否造成状态机或时钟前提异常 |
| G4 | DS90UB984 per-channel output-valid、stream-detect、error/status 寄存器含义和 readback | 直接判断 decoder 输出是否缺失或无效 |
| G5 | Redriver PWDN/I2C/static config、4 通道 input/output activity 是否在故障窗口有效 | 切分 Redriver/static path 与 decoder/AU15P |
| G6 | AU15P input activity、CDR/comma 状态是否覆盖 eDP1-4 每个通道 | 验证 prior receiver symptom 是否适用于新的四通道矩阵 |
| G7 | “单独勾选无法出图”的具体含义、勾选对象、操作顺序和是否影响 DS90UB984 reconfig | 可能解释通道选择、lane mapping 或 reinit 顺序问题 |
| G8 | 厂家对 DS90UB984 模拟出图输出寄存器/诊断位的确认 | 决定能否低成本用 status split 替代高速探测 |

## 9. Router-Ready Case Brief

A57 Issue4 现在应建模为 DS90UB984 解码板上的四通道概率性 eDP 出图异常，而不是单纯的后两通道问题。架构上，eDP1/2 来自一颗 DS90UB984，eDP3/4 来自另一颗 DS90UB984；但同一芯片下两个通道并不严格同好同坏。已测试 4 块解码板，板间表现不同：一块板 eDP3/4 异常概率较高，另外三块板 eDP1/2 异常概率较高，且目前没有一块稳定 4 通道出图。Redriver 位于 eDP mainstream 中间，设备上电后已配置，重复测试过程中不重新配置；重复测试变量主要是 DS90UB984 重新上下电和重新配置。前后 SerDes 电路差异已确认无差异，前/后 DS90UB984 IIC 指令、ini 和参数下发对比未发现问题。当前最需要切分的是：DS90UB984 per-channel 输出/状态、Redriver 静态 PWDN/I2C/path、AU15P input/CDR/comma、以及板/通道概率矩阵；仍不能下 root cause 结论。
