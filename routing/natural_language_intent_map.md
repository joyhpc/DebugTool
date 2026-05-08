# Natural-Language Intent Map

Users should be able to access every debug function by ordinary language. Do not require mode names.

| User wording | Internal behavior | Required deliverable |
|---|---|---|
| "帮我处理这个 bug" / "help debug this" | Run full default flow | cleaned understanding, safety gate, selected mode, hypotheses, action tree, next measurements |
| "可能原因有哪些" / "what could cause this" | Emphasize hypothesis generation | probability-ranked causes with evidence for/against and falsifiers |
| "给我决策树" / "decision tree" | Emphasize action planning | Mermaid decision tree plus node table with expected observations |
| "给我链路模型/影响因素图" / "link model" | Use architecture-first or assumption-driven | evidence-aware link model graph and node table |
| "这个结论靠谱吗" / "review this conclusion" | Run evidence audit | fact vs inference split, stale branches, missing evidence, confidence limits |
| "这是新证据" / "update with this evidence" | Re-run input cleaning and probability update | changed facts, demoted hypotheses, updated first actions |
| "整理成 issue 同步" | Produce operational summary | current facts, likely domains, action owners, expected evidence, stop conditions |
| "复盘/沉淀资产" | Run retrospective | root cause, misleading paths, case_record draft, regression candidate |
| "资料/文章里学到什么" | Use pattern_bundle intake | extracted patterns, evidence limits, promotion blockers |
| "只有一句现象" | Heuristic or assumption-driven provisional flow | provisional model, assumptions, first safe checks, at most three questions |

Routing rule: user intent modifies emphasis, not safety or evidence requirements. Full debug outputs still need input cleaning, safety gate, fact/inference separation, hypothesis probabilities, and action evidence mapping.
