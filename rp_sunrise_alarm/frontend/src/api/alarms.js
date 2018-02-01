import axios from 'axios'

const $axios = axios.create({
  baseURL: '/api/1.0/'
})

export default {
  getAlarms(cb) {
    $axios.get('alarm').then((response) => {
      cb(response.data.objects)
    })
  },
  addAlarm(data, cb) {
    $axios.post('alarm', data).then((response) => {
      cb(response.data)
    })
  },
  updateAlarm(id, data, cb) {
    $axios.patch('alarm/' + id, data).then((response) => {
      cb(response.data)
    })
  },
  deleteAlarm(id, cb) {
    $axios.delete('alarm/' + id).then((response) => {
      cb()
    })
  }
}