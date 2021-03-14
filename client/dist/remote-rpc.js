const rpcPort = 8000
const rpcHost = "localhost"
const url = `http://${rpcHost}:${rpcPort}/rpc-run`
// const url = `./rpc-run`

async function rpc (method, ...params) {
  const id = Math.random().toString(36).slice(-6);
  console.log(`rpc-run ${method}:`, params)
  try {
    const payload = { method, params, jsonrpc: '2.0', id }
    if ('electron' in window) {
      return await window.electron.rpc(payload)
    } else {
      const response = await fetch(url, {
        method: 'post',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(payload),
      })
      return await response.json()
    }
  } catch (e) {
    console.log(`rpc-run [fail] ${method} ${e}`)
    return { error: { message: `${e}`, code: -32000 }, jsonrpc: '2.0', id }
  }
}

class RemoteRpcProxy {
    constructor(){
        return new Proxy(this, {
            get(target, prop) {
                return async function() {
                    return await rpc(prop, ...arguments)
                };
            }
        });
    }
}

window.remote = new RemoteRpcProxy();