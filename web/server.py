"""FastAPI app exposing the DebugTool debug loop over HTTP.

Pluggable layer: nothing in the skill package imports this module. Deleting
web/ leaves the repository as a plain skill package.

Run from the repo root:  python -m web.server
"""

from __future__ import annotations

import json
import threading
from collections.abc import Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from web.config import DEFAULT_CLI, HOST, MAX_CONCURRENCY, PORT, STATIC_DIR
from web.runner import run_debug
from web.validate import available_modes, run_validation

app = FastAPI(title="DebugTool Web", version="0.1.0")

_run_slots = threading.Semaphore(MAX_CONCURRENCY)


class DebugRequest(BaseModel):
    input: str
    mode: str | None = None
    cli: str = DEFAULT_CLI


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/modes")
def modes() -> dict:
    return {"modes": available_modes()}


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


def _debug_stream(req: DebugRequest) -> Iterator[str]:
    with _run_slots:
        for event in run_debug(req.input, req.cli):
            if event["type"] == "deliverable":
                validation = run_validation(event["markdown"], req.mode) if req.mode else None
                yield _sse(
                    {
                        "type": "result",
                        "deliverable": event["markdown"],
                        "deliverable_found": event["found"],
                        "validation": validation,
                    }
                )
            else:
                yield _sse(event)


@app.post("/debug")
def debug(req: DebugRequest) -> StreamingResponse:
    if not req.input.strip():
        return StreamingResponse(
            iter([_sse({"type": "error", "message": "input is empty"})]),
            media_type="text/event-stream",
        )
    return StreamingResponse(_debug_stream(req), media_type="text/event-stream")


# Mounted last so the API routes above take precedence over the static catch-all.
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


def main() -> None:
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
