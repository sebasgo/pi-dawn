import axios from 'axios'

const $axios = axios.create({
  baseURL: '/api/1.0/'
})

export default {
  getLight(cb) {
    $axios.get('light').then((response) => {
      cb(response.data)
    })
  },
  setLight(data, cb) {
    $axios.patch('light', data).then((response) => {
      cb(response.data)
    })
  }
}
