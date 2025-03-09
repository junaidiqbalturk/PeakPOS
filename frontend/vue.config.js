const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  '__VUE_OPTIONS_API__': true,
  '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false
})
