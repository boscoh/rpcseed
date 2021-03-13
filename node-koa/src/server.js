const fs = require('fs')
const path = require('path')

const Koa = require('koa')
const koaBody = require('koa-body')
const Router = require('koa-router')
const cors = require('@koa/cors')
const send = require('koa-send')

const destroyable = require('server-destroy')
const http = require('http')

const { openUrlInBackground } = require('./url.js')
const handlers = require('./handlers.js')


let configFname = path.join(path.dirname(__filename), `../../config.json`)
const config = JSON.parse(fs.readFileSync(configFname))

for (let [k, v] of Object.entries(config)) {
  handlers.setConfig(k, v)
}

const clientDir = path.join(path.dirname(configFname), `${config.clientDir}`)

const port = config.port


const router = new Router()

router.get('/', async context => {
  await send(context, 'index.html', { root: clientDir })
})

router.get('/:path', async context => {
  if (context.params?.path) {
    const f = `${clientDir}/${context.params.path}`
    if (fs.existsSync(f)) {
      await send(context, context.params.path, { root: clientDir })
    } else {
      await send(context, 'index.html', { root: clientDir })
    }
  }
})

router.post('/rpc-run', async context => {
  /**
   * Test with `curl -H "Content-Type: application/json" -X POST --data '{<payload>}' http://<url>`
   * :returns: if function completes:
   *     { "jsonrpc": "2.0", "result": return value of function }
   *   else if function raises Exception:
   *     { "jsonrpc": "2.0", "error": { "code": -1, "message": string - exception explanation }, }
   */
  const requestBody = context.request.body
  //  expected:
  //  {
  //    'method': string - name of fn in `handlers`
  //    'params': Array<Any> - parameters of fn
  //    'jsonrpc': '2.0',
  //    'id': string - id of request
  //  }
  let responseBody
  if (requestBody) {
    let method = requestBody?.method
    let id = requestBody?.id
    let params = requestBody?.params
    if (!(method in handlers)) {
      const message = `Method not found: ${method}`
      console.log(`rpc-run [error]: ${message}`)
      responseBody = { error: { message, code: -32601 }, jsonrpc: '2.0', id }
    } else {
      let fn = handlers[method]
      console.log(`rpc-run ${method}`, params)
      try {
        responseBody = { result: await fn(...params), jsonrpc: '2.0', id }
      } catch (e) {
        console.log(`rpc-run ${method} [excpetion]: ${e}`)
        responseBody = {
          error: { message: `${e}`, code: -32603 },
          jsonrpc: '2.0',
          id
        }
      }
    }
  } else {
    console.log(`rpc-run couldn't read post body`)
    responseBody = {
      error: { message: 'Parse error', code: -32700 },
      jsonrpc: '2.0'
    }
  }
  context.response.body = responseBody
})

openUrlInBackground(`http://localhost:${port}`)

const app = new Koa()
app.use(koaBody())
app.use(cors())
app.use(router.routes())
app.use(router.allowedMethods())

console.log(`Listening on http://localhost:${port}`)
const server = http.createServer(app.callback())
server.listen(port)
destroyable(server)
