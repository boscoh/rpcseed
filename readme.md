
# RPC Seed

Tiny rpc server/client for webapp prototyping.

Provides:

* single file Vue/Bootstrap client 
* server in Typescript (Deno/Oak)
* equivalent server in Python 3 (Flask)
* unrestricted JSON RPC communication protocol using CORS

This is the simplest client/server I use to get started on
webapp prototypes. 

Deno provides the cleanest client/server code, and
 Python for science/math libraries.

Vue is the fastest prototyping framework and one can
 swap a heavier framework when needed.

# Quick start

__Deno__. 
First install Deno on *nix:

```bash
curl -fsSL https://deno.land/x/install/install.sh | sh
```

Then 

```bash
./run-deno.sh
```

__Or for Python__. 
Install packages:

```bash
pip install -r flask-server/requirements.txt
```

Then:

```bash
./run-python.sh
```

Options for run scripts:

 * `-n` - don't open browser automatically
 * `-c` - alternate config.json
  
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
For Deno, the function is defined in `deno-server/handlers.ts`:

```typescript
function serverFunction(param1, param2) {
    return {success: true}
}
```

In Python, it's `flask-server/handlers.py`:

```python
def serverFunction(param1, param2):
    return {"success": True}
```

### Configuration

In the client code, set `rpcHost` and `rpcPort` to define the url to communicate with the server.

For the server, set the receiving `port` in the top level `config.json`. It's up to you 
to decide where to deploy, normally `localhost` if we run locally.

