import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {},
  state: {
    menu: false
  },
  mutations: {
    SET_MENU(state, val) {
      state.menu = val
    }
  },
  actions: {
    showMenu({ commit }, val) {
      commit('SET_MENU', val)
    }
  }
})
