import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

import 'material-icons/iconfont/material-icons.css'
import 'vuetify/dist/vuetify.min.css'
import Vuetify from 'vuetify'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
  theme: {
    primary: colors.orange.darken2,
    secondary: colors.deepPurple.accent1,
    accent: colors.deepOrange
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
