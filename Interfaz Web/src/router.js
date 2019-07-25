import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Credits from './views/Credits.vue'
import How from './views/How.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/credits',
      name: 'credits',
      component: Credits
    },
    {
      path: '/how',
      name: 'how',
      component: How
    }
  ]
})
