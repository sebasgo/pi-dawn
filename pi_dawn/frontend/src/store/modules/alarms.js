import alarms from '@/api/alarms'
import * as types from '@/store/mutation-types'

const state = {
  alarms: []
}

const getters = {
  alarms: state => state.alarms
}

const actions = {
  getAlarms ({ commit }) {
    alarms.getAlarms(alarms => {
      commit(types.RECEIVE_ALARMS, { alarms })
      commit(types.SORT_ALARMS)
    })
  },
  addAlarm({ commit }, {data}){
    alarms.addAlarm(data, (alarm) => {
      commit(types.ADD_ALARM, {alarm})
      commit(types.SORT_ALARMS)
    })
  },
  updateAlarm({ commit }, {id, data}){
    commit(types.UPDATE_ALARM, {id, data})
    commit(types.SORT_ALARMS)
    alarms.updateAlarm(id, data, (alarm) => {
      commit(types.UPDATE_ALARM, {id: alarm.id, data: alarm})
      commit(types.SORT_ALARMS)
    })
  },
  deleteAlarm({ commit }, {id}) {
    commit(types.DELETE_ALARM, {id})
    alarms.deleteAlarm(id, () => {})
  }
}

const mutations = {
  [types.RECEIVE_ALARMS] (state, { alarms }) {
    state.alarms = alarms
  },
  [types.SORT_ALARMS] (state) {
    state.alarms.sort((a, b) => a.time > b.time)
  },
  [types.ADD_ALARM] (state, { alarm } ) {
    state.alarms.push(alarm)
  },
  [types.UPDATE_ALARM] (state, { id, data} ) {
    const alarm = state.alarms.find(alarm => alarm.id === id)
    Object.assign(alarm, data)
  },
  [types.DELETE_ALARM] (state, {id} ) {
    state.alarms = state.alarms.filter(o => o.id !== id)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
