# Debug Decision Tree Skill - V0.99.10 语义 Validator 门禁

## 状态

当前状态：早期内部 pilot 候选。还不是团队级可推广版本，也不是 V1.0。

V0.99.10 在 V0.99.9 的语义先验校准基础上，把部分可机械检查的语义护栏前移到 `scripts/output_validator.py`：Evidence Audit 必须显式覆盖 stale 证据、直接症状 top-two、unknown/model-gap、cost priors、candidate owner；Architecture-First 必须显式写出 top-two 理由、model-gap 分支和 cost-prior 来源。

用户可读正文应跟随用户语言。对于中文输入，摘要、判断、行动项、审核意见应使用中文；固定 contract 标题、schema 字段、命令、路径、信号名、寄存器名、料号等为了校验和追溯可以保留原文。

这个包目前适合 1-2 个真实早期内部 pilot debug loop，在更大范围使用前还需要继续验证。

## 核心资产类型

```text
link_model       因果 / 架构 / 依赖模型
signature        强症状 -> 快速排查动作组合
case_record      复盘 / 经验 / 已验证案例
pattern_bundle   文章 / 论坛 / app-note 风格的坑点或排查模式集合
debug_principle  跨硬件 debug 领域可复用的原则
```

## 推荐调用流程

1. 将用户的自然语言 bug 描述视为足够启动的输入。
2. 用 `output_contracts/input_cleaning.md` 清洗原始输入。
3. 用清洗后的 router-ready brief 进入 `prompts/context_router.md`。
4. 通过 `routing/natural_language_intent_map.md` 理解用户措辞，再用 `routing/mode_router.md` 选择模式。
5. 基于清洗后的输入和内置资产建立第一版 link model 与 hypothesis tree。
6. 外部 workspace knowledge 只作为升级路径，不作为默认路径。
7. 通过 `output_contracts/default_debug_delivery.md` 和被选中的 mode contract 输出。
8. 读取 `assets/` 前先检查 `reasoning/asset_priority.md`。
9. root cause 未确认时，必须给出概率、hypothesis tree、action decision tree 和首批测量动作。
10. 复用或推广输出前运行 `scripts/output_validator.py`；保存或发布 pilot/debug 产物前再运行 Evidence Audit。
11. 正文语言跟随用户。中文输入时，摘要、判断、行动项、审核意见用中文，同时保留 validator 需要的 heading 和技术标识。
12. Architecture-First 输出应参考 `reasoning/cost_priors.yaml` 和 `reasoning/probability_time_cost_model.md`，并保留 `unknown / model gap` 概率。

结构验证通过只说明输出符合 contract，不代表 debug 推理一定正确。

## 外部知识升级

DebugTool 不应该拥有项目知识。项目原理图、datasheet、项目笔记、历史 debug 记录和原始文档应放在外部 workspace knowledge 中。

默认不查询外部知识。先基于清洗后的用户输入、内置资产和显式假设给出稳定的一阶 debug deliverable。只有出现以下触发条件时才升级到外部知识：

- 用户明确要求使用 wiki、知识库、原理图、datasheet、repo 或历史 debug 记录。
- 用户明确要求联网学习、搜索资料、广泛探索引用，或从外部资料建立模型。
- link model 存在高影响缺口，会改变首批动作、安全边界或 top hypothesis 排序。
- 当前模型缺少足够的领域/项目知识，无法识别关键节点或可观测证据。
- 第一版 debug 输出暴露模型冲突，例如芯片映射、板卡版本、信号归属或控制极性不确定。

升级时，先用 `retrieval/knowledge_source_resolution.md` 解析知识来源，再发出 `output_contracts/knowledge_request.md`，然后用 `output_contracts/wiki_claim_extraction.md` 提取紧凑的 documented claims。引用 source path 或 URL，不复制大段私有原文。

外部知识探索可以分为三类：

| 模式 | 触发方式 | 行为 |
|---|---|---|
| Targeted | “查一下 PWDN 极性” / “看 my-wiki 里这个板子的记录” | 只查询指定缺口或来源，提取 claims，更新受影响节点 |
| Interactive | “边查边确认” / “我们一起建模型” | 分阶段推进：request、source plan、claim extraction、model update、user checkpoint |
| Broad | “网上学习一下再建模” / “广泛探索这个接口” | 搜索 workspace 或 online sources，优先项目资料和官方资料，合成带适用边界的模型 |

联网或 wiki 得到的材料是 documented evidence，不是当前板子的 target-system fact。它可以更新模型结构和先验概率，但直接测量、日志和用户确认仍然更强。

已有训练队列是 broad exploration 的第一批 source-registry seeds：

- `training/closed_loop/authoritative_training_queue.yaml`
- `training/dataset_1000/mipi_debug_queue.yaml`
- `training/dataset_1000/intel_altera_fpga_queue.yaml`
- `training/dataset_1000/public_solved_case_queue.yaml`
- `training/closed_loop/candidate_sources.yaml`

使用 `retrieval/high_value_source_registry.md` 选择这些来源，并在无边界 web search 之前先找相似问题。相似案例只能提供可迁移的排查方法和架构理解，不能证明当前 root cause。

知识来源解析顺序：

1. 用户请求中提供的路径。
2. 用户提供的 URL 或明确联网搜索指令。
3. `DEBUGTOOL_KB_ROOT`。
4. 本地 `knowledge_sources.yaml`。
5. workspace 平行目录发现，例如 `../my-wiki`、`../knowledge`、`../HW-knowledge-base`、`../wiki` 或 `../docs`。
6. 用户请求在线探索或确有必要时，使用官方/公开 web source。
7. 如果不可用，明确说明缺失知识会影响哪些判断。

提交到仓库的示例应使用相对路径，不应硬编码机器本地绝对路径。

可用 `retrieval/knowledge_sources.example.yaml` 作为本地配置模板。不要提交私有、机器相关的 `knowledge_sources.yaml`。

## 推荐 Founder-Pilot 流程

1. 用 `output_contracts/input_cleaning.md` 清洗并规范化原始用户 case。
2. 用 `prompts/context_router.md` 从清洗后的 brief 中选择模式。
3. 用被选中的 output contract 生成 debug 输出。
4. 只有当第一版 link model 无法支持稳定动作时，才升级到外部知识。
5. 对生成的 markdown 运行 `scripts/output_validator.py`。
6. 只执行已记录安全边界内的动作。
7. 将结果记录到 `forms/founder_pilot_result_form.md`。
8. 只有证据支持时，才运行 retrospective 并提出 case_record / regression 更新。

## V1.0 晋级标准

不要因为设计看起来完整就升级到 V1.0。

V1.0 至少需要：

- 至少 5 个真实项目 case 经 `training/real_project_cases/` 流程处理；
- 这些真实 case 的 top-3 hypothesis hit 或 near-hit rate 不低于 70%；
- 连续 30 天没有未解决的 P0 safety 或 contract bug；
- CI 中所有 validators、linters、smoke cases 和 regression-suite structure checks 通过；
- 人工审核显示 pilot case 中 safety-gate true positive 不低于 90%；
- pilot 操作中，从 cleaned input 到第一个可执行测量动作的中位时间不超过 3 分钟；
- 任何 breaking contract 或输出格式变更都有明确 changelog 记录。

这些阈值是临时标准，只有通过明确 release note 才能调整。

## 自然语言证据更新

用户不需要记住 input cleaning、link model、hypothesis probability、action decision tree 这些内部术语。

以下普通表达已经足够：

```text
有新线索：...
补充一下现场情况：...
刚测到：...
示波器看到：...
寄存器读到：...
这个线索说明什么？
帮我更新一下排查策略。
下一步怎么查？
```

DebugTool 应把这些视为 evidence update：保留 prior context，区分 fact 与 judgment，标记 stale assumptions，更新 hypothesis priority，并用普通语言给出下一步检查。

## Python 依赖

`scripts/output_validator.py` 只使用 Python 标准库。资产和 regression-suite lint 需要 PyYAML：

```bash
python -m pip install -r requirements.txt
```

## 常用命令

验证不同 mode 的输出：

```bash
python scripts/output_validator.py --mode input_cleaning --file cleaned.md
python scripts/output_validator.py --mode standard --file output.md
python scripts/output_validator.py --mode knowledge_linked --file output.md
python scripts/output_validator.py --mode architecture_first --file output.md
python scripts/output_validator.py --mode fast_path --file output.md
python scripts/output_validator.py --mode assumption_driven --file output.md
python scripts/output_validator.py --mode retrospective --file retrospective.md
python scripts/output_validator.py --mode evidence_audit --file audit.md
python scripts/output_validator.py --mode skill_improvement --file review.md
```

运行资产和 suite 检查：

```bash
python scripts/lint_assets.py
python scripts/regression_suite_linter.py
```

运行 output-validator smoke cases：

```bash
python scripts/run_output_validator_smoke.py
```

运行 closed-loop training record 检查：

```bash
python scripts/lint_closed_loop.py
```

运行 real project case intake 检查：

```bash
python scripts/lint_real_project_cases.py
```

运行 1000-unit training program 检查：

```bash
python scripts/lint_dataset_1000.py
```

## Closed-Loop Training

`training/closed_loop/` 用于公共或用户提供的 debug records。流程是：提取初始现象和背景，在揭示最终解决方案前先生成 predicted debug tree，然后揭示实际修复，评分覆盖情况，只将重复出现的学习沉淀为 assets。

`training/closed_loop/authoritative_training_queue.yaml` 包含 100 个来自 vendor application notes、官方 checklist、design guides 和 training articles 的官方训练单元。截至 V0.99.2，全部 100 个 queue units 都已映射到 `training/closed_loop/queue_closure_index.yaml`。这些是 official-source training closures，不是已验证的真实项目案例。

## Cost-Aware Ordering

使用 `reasoning/probability_time_cost_model.md` 按单位时间预期诊断价值对候选动作排序。Safety gates 和 prerequisite measurements 仍然优先于裸概率。

## Real Project Cases

真实项目材料使用 `forms/real_project_case_intake_form.md` 和 `training/real_project_cases/`。真实 case 必须 anonymized、blind-predicted、revealed、scored、reflected，然后才能提升为 `case_record`、`signature`、`link_model` 或 regression。

## 1000-Unit Program

`training/dataset_1000/` 用于扩展官方资料之外的先验。目标组合是：300 个 official priors、300 个 public solved cases、150 个 vendor/FAE resolved cases、100 个 real project cases、100 个 near-hit/miss counterexamples、50 个 safety-high-risk cases。

`training/dataset_1000/intel_altera_fpga_queue.yaml` 是 Intel/Altera FPGA 分支，覆盖 JTAG、Quartus Programmer、configuration status pins、Download Cable II、Nios debug nodes、PLL lock、EMIF 和 Platform Designer bring-up。

`training/dataset_1000/mipi_debug_queue.yaml` 是 MIPI DSI/CSI 分支，覆盖 D-PHY LP/HS state、DSI bridge no-video、CSI no-frame、packet counters、lane configuration、host graph binding、bridge/camera timing。

官方 vendor documents 被视为 authoritative priors；公共论坛记录只有在后续被项目证据校准后，才可作为 real cases 晋级。

## 模式选择顺序

```text
0. Input Cleaning
1. Safety Gate
2. Signature-Based Fast Path
3. Architecture-First
4. Knowledge-Linked
5. Assumption-Driven
6. Heuristic Context
7. Retrospective after solution
```

## 当前下一步

继续用真实 debug prompt 验证自然语言流程：只有一句现象、Issue 同步、架构信息丰富的 case、以及新证据更新。只有当首批两个推荐动作更好，或新证据后 stale branch 被明确降级时，pilot 才算真正有进展。
