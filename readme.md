
# RPC Seed

Tiny rpc server/client for webapp prototyping. 

Provides a single web-client that can talk (using JSON-RPC) to the following web-servers:

  * Deno (Typescript/Oak) - cleanest code
  * Node (Javascript/Koa) 
  * Python 3 WSGI (Flask) 
  * Python 3 ASGI (Fastapi) - async and math libraries
  * Electron - fake native apps

The web-client uses Vue, which allows a simple no-compile html file. That way I can focus on business logic.


### Quick start
 
__Deno__
1. install Deno `curl -fsSL https://deno.land/x/install/install.sh | sh`
2. `./run-deno.sh``

__Python/Flask__
1. `pip install -r py-flask/requirements.txt`
2. `./run-flask.sh`
  
__Python/Fastapi__
1. `pip install -r py-fastapi/requirements.txt`
2. `./run-fastapi.sh`
  
__Node__
1. `cd node-koa; npm install; cd ..`
2. `./run-node.sh`

__Electron__
1. `cd elecstron; npm install; cd ..`
2. `./run-electron.sh`

Except for Electron, the web-client is served on <http://localhost:8000>

### Client to server

Communication with the server is directed by the client
through via the RPC-JSON protocol:

```js
let data = await remote.serverFunction(param1, param2)
if (data.result) {
    console.log(data.result)
    // { "success": true }
} else {
    console.log(data.error)
    // { "code": -1, "message": "You got an error" }
}
```

In the server, actions are defined in the `handlers` module of the server.
For Node, the function is defined in `mode-koa/handlers.ts`:

```typescript
function serverFunction(param1, param2) {
    return {success: true}
}
```

In Python, it's `py-fastapi/handlers.py`:

```python
def serverFunction(param1, param2):
    return {"success": True}
```

### Configuration

In the client, set `rpcHost` and `rpcPort` to define the url to communicate with the server.

For the server, set the receiving `port` in the top level `config.json`. It's up to you 
to decide where to deploy, normally `localhost` if we run locally.

