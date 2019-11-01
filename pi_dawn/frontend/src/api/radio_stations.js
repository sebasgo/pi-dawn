import axios from 'axios'

const $axios = axios.create({
  baseURL: '/api/1.0/'
})

export default {
  getRadioStations(cb) {
    $axios.get('radio_station').then((response) => {
      cb(response.data)
    })
  },
  addRadioStation(data, cb) {
    $axios.post('radio_station', data).then((response) => {
      cb(response.data)
    })
  },
  updateRadioStation(id, data, cb) {
    $axios.patch('radio_station/' + id, data).then((response) => {
      cb(response.data)
    })
  },
  deleteRadioStation(id, cb) {
    $axios.delete('radio_station/' + id).then(() => {
      cb()
    })
  }
}
