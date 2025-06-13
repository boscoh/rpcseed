<template lang="pug">
.d-flex.flex-row.justify-content-center(style="height: calc(100vh);")
  #col1.mt-5.p-2.d-flex.flex-column
    h1 3D Model Hotspots
    pre {{ config }}
</template>

<style>
body {
  overflow: hidden;
}
</style>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import _ from 'lodash'
import {remote} from '../modules/rpc'

function asyncDelay (time) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve(time)
    }, time)
  })
}

export default {
  name: 'Page',
  data () {
    return {
      message: '',
      config: {},
    }
  },
  async mounted () {
    document.oncontextmenu = _.noop
    document.onkeydown = e => {
      this.onkeydown(e)
    }
    let response = await remote.getConfig()
    console.log(response)
    this.config = JSON.stringify(response.result, null, 2)
  },
  methods: {
    lockKeyboard() {
      window.keyboardLock = true
    },
    unlockKeyboard() {
      window.keyboardLock = false
    },
    onkeydown (event) {
      if (!window.keyboardLock) {
        let c = String.fromCharCode(event.keyCode).toUpperCase()
      }
    }
  }
}
</script>
