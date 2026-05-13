# A57 eDP Pilot Run

本目录是 A57 eDP / DS90UB984 出图异常 debug case 的规范工作区。

当前入口：

- `latest-input-cleaning.md` - 当前 Issue4 输入清洗记录，已合并 2026-05-13 CR/EQ fail 与 AUX/DPCD 代答更新。
- `latest-architecture-first.md` - 当前 Architecture-First 输出，已增加 CR/EQ fail 先查 AUX/DPCD 训练控制面的模式门。
- `REVIEW.md` - 对当前 latest 的语义审核记录，以及已转化为 skill 规则的问题清单。

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
