let config: { [Key: string]: any } = {}

const handlers: { [Key: string]: Function } = {
  setConfig (key: string, value: any) {
    config[key] = value
  },

  getConfig () {
    return config
  }
}

export { handlers }
