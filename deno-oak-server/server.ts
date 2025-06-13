import {
  Application,
  Context,
  Router,
  send
} from 'https://deno.land/x/oak/mod.ts'
import { oakCors } from 'https://deno.land/x/cors/mod.ts'
import { existsSync } from 'https://deno.land/std/fs/mod.ts'
import * as path from "https://deno.land/std@0.90.0/path/mod.ts";
import { parse } from 'https://deno.land/std/flags/mod.ts'

// Imports the handlers used in the route /rpc-run
import { handlers } from './handlers.ts'

const args = parse(Deno.args)
console.dir(args)

let config_fname = `../config.json`
if (args.c) {
  config_fname = args.c
}

const text = await Deno.readTextFile(config_fname);
const config: any = JSON.parse(text);
for (let [k, v] of Object.entries(config)) {
  handlers.setConfig(k, v)
}
const clientDir = `../${config.clientDir}`
const socket = `${config.host}:${config.port}`
const router = new Router()

router.get('/', async context => {
  await send(context, 'index.html', { root: clientDir })
})

router.get('/:path', async context => {
  if (context.params?.path) {
    const f = path.join(clientDir, context.params.path)
    console.log('fetching file', f, existsSync(f))
    if (existsSync(f)) {
      await send(context, context.params.path, { root: clientDir })
    } else {
      await send(context, 'index.html', { root: clientDir })
    }
  }
})

/**
 * Triggers a function in the `handlers` dictionary of functions, with request payload:
 *       {
 *         'jsonrpc': '2.0',
 *         'method': string - name of function in `handlers`
 *         'params': Array<any> - list of parameters
 *       }
 * Test with `curl -H "Content-Type: application/json" -X POST --data '{<payload>}' http://<url>`
 *
 * :return: if function completes successfully then:
 *      {
 *           "jsonrpc": "2.0",
 *           "result": any - return value of function
 *       }
 *   else if function raises Exception:
 *       {
 *           "jsonrpc": "2.0",
 *           "error": {
 *               "code": -1,
 *               "message": string - exception in string form
 *           },
 *       }
 */
router.post('/rpc-run', async (context: Context) => {
  let responseBody: any
  const requestBody = context.request.body
  if (requestBody.type() === 'json') {
    let value = await requestBody.json()
    let id = value?.id
    let method = value?.method
    if (!(method in handlers)) {
      const message = `Method not found`
      responseBody = { error: { message, code: -32601 }, jsonrpc: '2.0', id }
    } else {
      try {
        let fn = handlers[method]
        let params = value?.params ? value.params : []
        const paramStr = params ? params.join(',') : ''
        console.log(`rpc-run await ${method}(${paramStr})`)
        const result = await fn(...params)
        responseBody = { result, jsonrpc: '2.0', id }
      } catch (e) {
        const message = `${e}`
        responseBody = { error: { message, code: -32603 }, jsonrpc: '2.0', id }
      }
    }
  } else {
    responseBody = {
      error: { message: 'Parse error', code: -32700 },
      jsonrpc: '2.0'
    }
  }
  context.response.body = responseBody
})

const app = new Application()
app.use(oakCors())
app.use(router.routes())
app.use(router.allowedMethods())

console.log(`Listening on http://${socket}`)
await app.listen(socket)
