import logging
from pathlib import Path
import json
import traceback
import inspect

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app_dir = Path(__file__).resolve().parent.parent

config = json.load(open(app_dir / "config.json"))
client_dir = app_dir / config["clientDir"]
data_dir = app_dir / config["dataDir"]

handlers.setConfig("dataDir", str(data_dir))
for k, v in config.items():
    handlers.setConfig(k, v)


app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.post("/rpc-run")
async def rpc_run(data: dict):
    job_id = data.get("id", None)
    method = data.get("method")
    params = data.get("params", [])
    try:
        if not hasattr(handlers, method):
            raise Exception(f"rpc-run {method} is not found")
        fn = getattr(handlers, method)
        if inspect.iscoroutinefunction(fn):
            result = await fn(*params)
        else:
            result = fn(*params)
        logger.debug(f"rpc-run {method}")
        return {"result": result, "jsonrpc": "2.0", "id": job_id}
    except Exception as e:
        print(traceback.format_exc())
        return {
            "error": {"code": -1, "message": str(e)},
            "jsonrpc": "2.0",
            "id": job_id,
        }


@app.get("/")
async def serve_index(request: Request):
    return FileResponse(client_dir / "index.html")


# All other calls diverted to static files
app.mount("/", StaticFiles(directory=client_dir), name="dist")
