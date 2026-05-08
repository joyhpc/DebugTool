# Natural-Language Intent Map

Users should be able to access every debug function by ordinary language. Do not require mode names.

| User wording | Internal behavior | Required deliverable |
|---|---|---|
| "帮我处理这个 bug" / "help debug this" | Run full default flow | cleaned understanding, safety gate, selected mode, hypotheses, action tree, next measurements |
| "可能原因有哪些" / "what could cause this" | Emphasize hypothesis generation | probability-ranked causes with evidence for/against and falsifiers |
| "给我决策树" / "decision tree" | Emphasize action planning | Mermaid decision tree plus node table with expected observations |
| "给我链路模型/影响因素图" / "link model" | Use architecture-first or assumption-driven | evidence-aware link model graph and node table |
| "这个结论靠谱吗" / "review this conclusion" / "你满意这个生成物吗" | Run evidence audit using `output_contracts/evidence_audit.md` | verdict, fact vs inference split, stale branches, missing evidence, confidence limits, required fixes |
| "这是新证据" / "update with this evidence" | Re-run input cleaning and probability update | changed facts, demoted hypotheses, updated first actions |
| "有新线索" / "补充一下现场情况" | Treat as evidence update | what changed, what stays uncertain, updated next checks |
| "帮我更新一下排查策略" / "下一步怎么查" | Update current debug plan from new information | revised priority, stale branches, next 1-3 actions |
| "刚测到..." / "示波器看到..." / "寄存器读到..." | Treat measurement as new evidence | measurement classification, affected hypotheses, updated action ranking |
| "刚才的判断要不要改" / "这个线索说明什么" | Run evidence-impact review | raised/lowered hypotheses, evidence limits, action changes |
| "整理成 issue 同步" | Produce operational summary | current facts, likely domains, action owners, expected evidence, stop conditions |
| "复盘/沉淀资产" | Run retrospective | root cause, misleading paths, case_record draft, regression candidate |
| "资料/文章里学到什么" | Use pattern_bundle intake | extracted patterns, evidence limits, promotion blockers |
| "查 my-wiki/知识库/历史记录" | Use Knowledge-Linked workspace exploration | Knowledge Request, source resolution, extracted claims, updated link model |
| "联网学习/网上查资料建立模型" | Use Knowledge-Linked broad exploration | source plan, cited claims, applicability limits, updated model |
| "广泛探索一下/先学习这个接口" | Use Knowledge-Linked broad exploration | broad source search, claim extraction, model synthesis, confidence limits |
| "找相似问题/类似案例/别人怎么解决的" | Use Knowledge-Linked similar-problem expansion | similar case candidates, transferable tactics, applicability limits, updated action ranking |
| "边查边确认/一起建模型/高度交互" | Use Knowledge-Linked interactive exploration | staged checkpoints: request, source plan, claims, model update, next actions |
| "只有一句现象" | Heuristic or assumption-driven provisional flow | provisional model, assumptions, first safe checks, at most three questions |

Routing rule: user intent modifies emphasis, not safety or evidence requirements. Full debug outputs still need input cleaning, safety gate, fact/inference separation, hypothesis probabilities, and action evidence mapping.
