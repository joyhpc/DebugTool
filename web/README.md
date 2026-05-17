# DebugTool Web 层

DebugTool 的**可插拔**本地 web 服务。让工程师在浏览器里贴 bug 描述、跑完整 debug loop,同时对现有 skill 包零侵入。

## 工作原理

web 后端不重新实现任何调试逻辑。一次 `POST /debug`:

1. 把用户输入包进引导 prompt;
2. `subprocess` 启动 codex/claude CLI(cwd = 仓库根),CLI agent 在仓库内自读 `SKILL.md` / `prompts/` / `output_contracts/`,跑 input cleaning → safety → routing → 生成;
3. 逐行转发 CLI 的 JSONL 事件作为 SSE 进度;
4. 按标记抽取交付物,import `scripts/output_validator.py` 做结构校验;
5. 返回 `{deliverable, validation}`。

## 可插拔保证

- 所有代码都在 `web/` 目录内;依赖方向单向:`web/ → scripts/ + 资产(只读)`。
- 现有任何文件都不 import `web`。
- 删除 `web/` 目录后,codex 直接用法、`scripts/` CLI、CI 全部不受影响。

## 启动

```bash
pip install -r web/requirements-web.txt
python -m web.server
```

从仓库根运行,然后浏览器打开 `http://127.0.0.1:8000`。

## 端点

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 探活 |
| GET | `/modes` | 可选的 validator 模式列表 |
| POST | `/debug` | body `{input, mode?, cli?}`,SSE 流式返回进度与 `{deliverable, validation}` |
| GET | `/` | 极简前端页面 |

## 配置

改 `web/config.py`:端口、超时、并发数、`CLI_PROFILES`(codex/claude 的 argv 模板)、引导 prompt 模板。`CLI_PROFILES` 里的 flag 细节随 CLI 版本演进,用 `codex exec --help` / `claude --help` 校准后改这里即可,无需改代码。

## 拔除

删除整个 `web/` 目录,仓库即恢复为纯 skill 包。
