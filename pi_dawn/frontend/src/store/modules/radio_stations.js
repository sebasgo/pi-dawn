import radio_stations from '@/api/radio_stations'
import * as types from '@/store/mutation-types'

const state = {
  radio_stations: []
}

const getters = {
  radio_stations: state => state.radio_stations
}

const actions = {
  getRadioStations ({ commit }) {
    radio_stations.getRadioStations(radio_stations => {
      commit(types.RECEIVE_RADIO_STATIONS, { radio_stations })
      commit(types.SORT_RADIO_STATIONS)
    })
  },
  addRadioStation({ commit }, {data}){
    radio_stations.addRadioStation(data, (radio_station) => {
      commit(types.ADD_RADIO_STATION, {radio_station})
      commit(types.SORT_RADIO_STATIONS)
    })
  },
  updateRadioStation({ commit }, {id, data}){
    commit(types.UPDATE_RADIO_STATION, {id, data})
    commit(types.SORT_RADIO_STATIONS)
    radio_stations.updateRadioStation(id, data, (radio_station) => {
      commit(types.UPDATE_RADIO_STATION, {id: radio_station.id, data: radio_station})
      commit(types.SORT_RADIO_STATIONS)
    })
  },
  deleteRadioStation({ commit }, {id}) {
    commit(types.DELETE_RADIO_STATION, {id})
    radio_stations.deleteRadioStation(id, () => {})
  }
}

const mutations = {
  [types.RECEIVE_RADIO_STATIONS] (state, { radio_stations }) {
    state.radio_stations = radio_stations
  },
  [types.SORT_RADIO_STATIONS] (state) {
    state.radio_stations.sort((a, b) => {
      return a.name.localeCompare(b.name)
    })
  },
  [types.ADD_RADIO_STATION] (state, { radio_station } ) {
    state.radio_stations.push(radio_station)
  },
  [types.UPDATE_RADIO_STATION] (state, { id, data} ) {
    const radio_station = state.radio_stations.find(radio_station => radio_station.id === id)
    Object.assign(radio_station, data)
  },
  [types.DELETE_RADIO_STATION] (state, {id} ) {
    state.radio_stations = state.radio_stations.filter(o => o.id !== id)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
