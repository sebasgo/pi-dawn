import light from '@/api/light'
import * as types from '@/store/mutation-types'

const state = {
  on: false
}

const getters = {
  lightOn: state => state.on
}

const actions = {
  getLight ({ commit }) {
    light.getLight((light) => {
      commit(types.SET_LIGHT, { on: light.on })
    })
  },
  toggleLight({ commit, state}) {
    let on = !state.on
    commit(types.SET_LIGHT, { on })
    light.setLight({ on }, (light) => {
      commit(types.SET_LIGHT, { on: light.on })
    })
  }
}

const mutations = {
  [types.SET_LIGHT] (state, { on }) {
    state.on = on
  },
}

export default {
  state,
  getters,
  actions,
  mutations
}
