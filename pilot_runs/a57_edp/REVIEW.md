# A57 eDP 最新生成物审核记录

审核对象：`pilot_runs/a57_edp/latest-architecture-first.md`

审核结论：当前输出真实可用，不是 demo；但暴露了 DebugTool skill 层面的若干可制度化问题。

## 做得对

- `Input Cleaning` 能区分已确认事实、判断和已尝试方法，并保留 source 与 confidence。
- link model 按控制、上电/复位/时钟、主数据链路、FPGA 接收链路、对照轴分层。
- `Link Evidence Boundary Table` 将 known / inferred / unknown / evidence-to-move-boundary 分开。
- `Not Applied` 明确拒绝了 decoder 已证明异常、Redriver 已排除、单板问题等过度结论。
- `Stop / Escalation Conditions` 能阻止 AUX-first、SerDes tuning-first、Redriver 过早排除等 stale branch。

## 主要问题

1. H1 配置/读回高于 H4 decoder output absent/invalid，不符合“直接物理症状最简解释优先”原则。
2. A1、A4 等 lab capture 的 time_min 明显偏乐观，会扭曲 priority_score。
3. DEV3-only vs DEV3+DEV4 的 selection-dependent 线索应更强地支持 Redriver/lane/path 分支。
4. 最优路径缺少累计路径成本，难以用于排期。
5. aux_in 弱下拉未解决属于旧证据，应标为 `requires_re_verification`，不能直接影响概率。
6. owner 表基于聊天露面推断，必须改为候选 owner，并注明需 PM/项目负责人确认。
7. hypothesis table 应保留 `unknown / model gap` 概率。
8. PWDN 极性属于低成本 point check，不应和 broad Knowledge-Linked exploration 混在一起。

## 已转化为 skill 规则

- 在 `SKILL.md` 增加直接症状最简解释、stale 证据隔离、unknown/model-gap、candidate owner、cost priors 等 mandatory rules。
- 在 `output_contracts/input_cleaning.md` 增加 `staleness` 字段。
- 在 `output_contracts/architecture_first_output.md` 增加概率、cost、owner 和 point-check 要求。
- 在 `output_contracts/evidence_audit.md` 增加 semantic review 检查项。
- 新增 `reasoning/cost_priors.yaml`。

## A57 latest 修订要求

- H3/H4 调整到 top two。
- H1 下调，避免配置分支压过最近物理边界。
- F15 标为 stale/re-verify，不作为概率降权依据。
- F16 显式进入 H3 的 raise evidence。
- A1/A4/A6/A7/A2 使用更现实的 cost prior。
- §11 增加累计路径成本。
- §15 owner 改成 candidate owner。

## Issue4 补充后审核记录

审核对象：`pilot_runs/a57_edp/latest-input-cleaning.md` 与 `pilot_runs/a57_edp/latest-architecture-first.md`

审核结论：Issue4 补充改变了 case 边界，latest 已从“后两通道概率性不出图”改为“四个 eDP 通道都可能概率性出图，概率随板和通道变化”。当前输出仍不能下 root cause 结论，但已经把下一步动作收敛到更可执行的边界切分。

关键修订：

- 新增 current input-cleaning 入口，保留 Issue4 的架构映射、多板测试、Redriver 配置边界和重复测试方式。
- 将旧 latest 归档到 `archive/architecture-first-before-issue4-2026-05-09.md`。
- 将 eDP1/2 与 eDP3/4 映射到两颗 DS90UB984，并明确同芯片两个通道不严格一致。
- 降级“后两通道专属”“Redriver 动态重配置”“前后 IIC intent 差异”分支。
- 上调 DS90UB984 per-channel output/status、Redriver static path、board/channel/SI matrix 的排查优先级。
- 保留旧 AUX/CDR/comma 证据为 `requires_re_verification` context，避免 stale evidence 直接更新概率。

残余风险：

- 当前多板数据仍缺标准化 `board_id / chip_id / channel_id / test_count / fail_count` 矩阵。
- DS90UB984 output/status 寄存器和 Redriver PWDN/I2C/static config 仍未闭合。
- AU15P CDR/comma 旧证据需要按新的 eDP1-4 四通道矩阵重新对齐。

## 2026-05-13 Same-Case Retrieval Failure

触发例子：用户补充 A57 eDP 群聊信息后问“这些信息记录到哪里？”，系统没有先匹配到已有 `pilot_runs/a57_edp/`，而是建议新建一个孤立文档。

Skill layer diagnosis：

- `artifact_lifecycle`：缺少全局 case index，只有 case 目录 README，短问句无法快速定位已有 case。
- `routing`：record-location 请求没有被识别为“先查同案，再决定新建还是合并”。
- `intake`：A57/eDP/AUX/CR/EQ/SerDes 等同案 tokens 没有被当成 case identity evidence。

修复：

- 新增 `pilot_runs/CASE_INDEX.md`，维护 case_id、aliases/current entry/status/routing note。
- 更新 `lifecycle/case_artifact_hygiene.md`，要求保存或回答记录位置前先查 case index。
- 更新 `SKILL.md`、`prompts/context_router.md`、`routing/natural_language_intent_map.md`，把“记录到哪里 / 合并之前案子 / 前面讨论过”路由到同案索引匹配。

后续规则：A57/eDP/DS90UB984/AUX/CR/EQ/训练字/SerDes/解码板等词出现时，应强匹配 `A57-EDP`，先打开 `pilot_runs/a57_edp/README.md` 和 current `latest-*`，再更新或回复。
