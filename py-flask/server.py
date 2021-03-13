import logging
import os
import threading
import time
import traceback
import webbrowser
from argparse import ArgumentParser
from pathlib import Path
from urllib.request import urlopen

from flask import Flask, json, jsonify, request, send_from_directory
from flask_cors import CORS

import handlers

__doc__ = """
A Flask server that implements an RPC protocol, where the available
remote procedural calls are defined in the handlers module
"""


logger = logging.getLogger(__name__)

api = Flask(__name__)

CORS(api)

client_dir = Path(__file__).parent


@api.route("/", methods=["GET"])
def get_index():
    return send_from_directory(client_dir, "index.html")


# Static files are stored in the public directory and available
# in this URL route
@api.route("/<path:path>")
def send_public_file(path):
    f = client_dir / path
    if f.exists():
        return send_from_directory(client_dir, path)
    else:
        return send_from_directory(client_dir, "index.html")


@api.route("/kill-server", methods=["GET"])
def kill():
    logger.debug(f"kill-server")
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@api.route("/rpc-run", methods=["POST"])
def rpc_run():
    """
    Triggers a remote procedural call from the client, the requested
    procedure is defined in the post body as:
        request.data = {
          'jsonrpc': '2.0',
          'method': <str> - name of function
          'params': [arg,...] - list of parameters, which can be
                JSON literals, ie., dict, list, str and numbers
        }

    The 'method' is searched against functions the handlers module,
    and the resultant function is run. This function is expected to
    take the `params` as function arguments, and the function is
    expected to return a JSON object.

    This function is expected to raise Exceptions on any errors.

    WARNING: the returned JSON cannot have NaN or Infinity as a
    numerical value.

    :return: if the procedure completes successfully then the following
    JSON literal is returned:
        {
            "jsonrpc": "2.0",
            "result": returned JSON literal from procedure
        }
    However if the procedure raises an exception:
        {
            "jsonrpc": "2.0",
            "error": {
                "code": -1,
                "message": string of the exception
            },
        }
    """
    data = json.loads(request.data)
    id = data.get('id', None)
    method = data.get("method")
    if not hasattr(handlers, method):
        return jsonify({"error": {"code": -32601, "message": 'Method not found', "jsonrpc": "2.0", "id": id}})
    params = data.get("params", [])
    try:
        fn = getattr(handlers, method)
        result = fn(*params)
        return jsonify({"result": result, "jsonrpc": "2.0","id": id})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": {"code": -1, "message": str(e)}, "jsonrpc": "2.0", "id": id})


def open_url_in_background(url, sleep_in_s=1):
    """
    Setus up a background thread to poll the server until it
    has started, then attempts to open the webclient in the
    system web-browser
    """

    def inner():
        elapsed = 0
        while True:
            try:
                response_code = urlopen(url).getcode()
                if response_code < 400:
                    logger.info(f"open_url_in_background success")
                    webbrowser.open(url)
                    return
            except:
                time.sleep(sleep_in_s)
                elapsed += sleep_in_s
                logger.info(f"open_url_in_background waiting {elapsed}s")

    # creates a thread to poll server before opening client
    logger.debug(f"open_url_in_background searching {url}")
    threading.Thread(target=inner).start()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--no-open", "-n", action="store_true", help="don't open page")
    parser.add_argument("--silent", "-s", action="store_true", help="suppress logs")
    parser.add_argument("--debug", "-d", action="store_true", help="debug mode")
    parser.add_argument("--config", "-c", default="../config.json", help="debug mode")
    args = parser.parse_args()

    if args.silent:
        os.environ["WERKZEUG_RUN_MAIN"] = "true"
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("werkzeug").disabled = True
        api.logger.disabled = True
    else:
        logging.basicConfig(level=logging.DEBUG)
        logger_names = ["werkzeug"]
        for n in logger_names:
            logging.getLogger(n).setLevel(logging.ERROR)

    config = json.load(open(args.config))
    port = config["port"]
    host = config["host"]
    url = f"http://{host}:{port}"
    global client_dir
    client_dir = Path("..") / config["clientDir"]
    for k, v in config.items():
        handlers.setConfig(k, v)

    if not args.no_open:
        open_url_in_background(f"{url}")

    logger.info(url)
    api.run(debug=bool(args.debug), port=port)


if __name__ == "__main__":
    main()
