let config = {}

const handlers = {
  setConfig (key, value) {
    config[key] = value
  },

  getConfig () {
    return config
  }
}

module.exports = handlers
