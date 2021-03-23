import logging
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import handlers

fname = Path(__file__).parent / ".." / "config.json"
config = json.load(open(fname))

for k, v in config.items():
    handlers.setConfig(k, v)

client_dir = fname.parent / config["clientDir"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.post("/rpc-run")
async def rpc_run(data: dict):
    logger.debug(data)
    id = data.get("id", None)
    method = data.get("method")
    if not hasattr(handlers, method):
        return jsonify(
            {
                "error": {
                    "code": -32601,
                    "message": "Method not found",
                    "jsonrpc": "2.0",
                    "id": id,
                }
            }
        )
    params = data.get("params", [])
    try:
        fn = getattr(handlers, method)
        result = fn(*params)
        return {"result": result, "jsonrpc": "2.0", "id": id}
    except Exception as e:
        print(traceback.format_exc())
        return {"error": {"code": -1, "message": str(e)}, "jsonrpc": "2.0", "id": id}


@app.get("/")
async def serve_index_htm(request: Request):
    return FileResponse(client_dir / "index.html")


# All other calls diverted to static files
app.mount("/", StaticFiles(directory=client_dir), name="dist")
