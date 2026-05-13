# A57 eDP Pilot Run

本目录是 A57 eDP / DS90UB984 出图异常 debug case 的规范工作区。

当前入口：

- `latest-input-cleaning.md` - 当前 Issue4 输入清洗记录，已合并 2026-05-13 CR/EQ fail 与 AUX/DPCD 代答更新。
- `latest-architecture-first.md` - 当前 Architecture-First 输出，已增加 CR/EQ fail 先查 AUX/DPCD 训练控制面的模式门。
- `visual-architecture-brief.md` - 当前 bug 的系统/子系统架构可视化入口，先给 Mode A/Mode B 框架、结论和行动路线。
- `field-action-plan.md` - 当前现场执行计划，使用通用 failure matrix 和 same-window evidence batch 模板做 A57 字段映射。
- `REVIEW.md` - 对当前 latest 的语义审核记录，以及已转化为 skill 规则的问题清单。

阅读顺序：

1. 先读 `visual-architecture-brief.md`：确认 bug 当前落在 Mode A training-control plane 还是 Mode B main data path。
2. 再读 `latest-architecture-first.md`：查看完整证据、概率、boundary/mechanism 和 decision tree。
3. 执行时读 `field-action-plan.md`：按同窗口 evidence batch 和 stop conditions 采证。
4. 需要追溯事实来源时读 `latest-input-cleaning.md` 与 `REVIEW.md`。

历史归档：

- `archive/input-cleaning-2026-05-08.md` - 较早的 input-cleaning-only 记录。
- `archive/architecture-first-initial-link-model.md` - 较早的 Architecture-First link-model 记录。
- `archive/architecture-first-english-before-cn-2026-05-08.md` - V0.99.8 中文输出规则生效前的英文 latest 版本。
- `archive/architecture-first-before-issue4-2026-05-09.md` - Issue4 补充前的中文 latest 版本。
- `archive/input-cleaning-before-aux-cr-eq-2026-05-13.md` - 2026-05-13 AUX/DPCD 代答更新前的 latest input-cleaning。
- `archive/architecture-first-before-aux-cr-eq-2026-05-13.md` - 2026-05-13 AUX/DPCD 代答更新前的 latest architecture-first。

维护规则：

- 每个 case/mode 只保留一个当前入口。
- 被替代的同案输出移动到 `archive/`，不要散落在 `pilot_runs/` 顶层。
- 不覆盖历史归档；需要保留旧版本时创建新的归档文件名。
- A57 专有名称只能放在本目录的 case configuration 或证据记录里；不要硬编码进 `scripts/`、`output_contracts/`、validator 或通用 `forms/`。
- 通用矩阵字段来自 `forms/failure_matrix_template.md`；同窗口证据批次字段来自 `forms/same_window_evidence_batch_checklist.md`。
