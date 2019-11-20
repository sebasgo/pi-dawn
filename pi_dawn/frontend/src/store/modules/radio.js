import radio from '@/api/radio'
import * as types from '@/store/mutation-types'

const state = {
  radioState: {
    is_playing: false,
    station: -1,
    volume: 0,
  }
}

const getters = {
  radioState: state => state.radioState
}

const actions = {
  getRadioState ({ commit }) {
    radio.getRadioState((radioState) => {
      commit(types.SET_RADIO_STATE, radioState)
    })
  },
  setRadioState({ commit }, data){
    radio.setRadioState(data, (new_data) => {
      commit(types.SET_RADIO_STATE, new_data)
    })
  },
}

const mutations = {
  [types.SET_RADIO_STATE] (state,  radioState) {
    state.radioState = radioState
  },
}

export default {
  state,
  getters,
  actions,
  mutations
}
