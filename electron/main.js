// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')

function createWindow (clientDir) {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(clientDir, 'index.html'))

  // Open the DevTools.
  mainWindow.webContents.openDevTools()
}

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

const handlers = require('../node-koa/src/handlers')

let configFname = path.join(path.dirname(__filename), `../config.json`)
const config = JSON.parse(fs.readFileSync(configFname))

for (let [k, v] of Object.entries(config)) {
  handlers.setConfig(k, v)
}

const clientDir = path.join(path.dirname(configFname), `${config.clientDir}`)

app.whenReady().then(() => {
  createWindow(clientDir)

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

ipcMain.handle('rpc', async (event, payload) => {
  const method = payload?.method
  const params = payload?.params
  const id = payload?.id
  if (!(method in handlers)) {
    const message = `Method ${method} not found in handlers`
    console.log(`rpc-run [error]: ${message}`)
    return { error: { message, code: -32601 }, jsonrpc: '2.0', id }
  } else {
    console.log(`rpc-run ${method}`, params)
    try {
      const fn = handlers[method]
      return { result: await fn(...params), jsonrpc: '2.0', id }
    } catch (e) {
      console.log(`rpc-run ${method} [exception]: ${e}`)
      return {
        error: { message: `${e}`, code: -32603 },
        jsonrpc: '2.0',
        id
      }
    }
  }
})
