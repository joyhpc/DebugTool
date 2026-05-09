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
