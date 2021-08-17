let config: { [Key: string]: any } = {}

const handlers: { [Key: string]: Function } = {
  async setConfig (key: string, value: any) {
    config[key] = value
  },

  async getConfig () {
    return config
  }
}

export { handlers }
