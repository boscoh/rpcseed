import logging
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import handlers

this_dir = Path(__file__).parent
config_fname = this_dir.parent / '..' / 'config.json'
config = json.load(open(config_fname))
for k, v in config.items():
    handlers.setConfig(k, v)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.post("/rpc-run")
async def read_item(data: dict):
    logger.debug(data)
    id = data.get('id', None)
    method = data.get("method")
    if not hasattr(handlers, method):
        return jsonify({"error": {"code": -32601, "message": 'Method not found', "jsonrpc": "2.0", "id": id}})
    params = data.get("params", [])
    try:
        fn = getattr(handlers, method)
        result = fn(*params)
        return {"result": result, "jsonrpc": "2.0","id": id}
    except Exception as e:
        print(traceback.format_exc())
        return {"error": {"code": -1, "message": str(e)}, "jsonrpc": "2.0", "id": id}

client_dir = config_fname.parent / config["clientDir"]
print(client_dir, client_dir.exists())

@app.get("/")
async def example(request: Request):
    return FileResponse(client_dir / "index.html")

app.mount("/", StaticFiles(directory=client_dir), name="dist")




