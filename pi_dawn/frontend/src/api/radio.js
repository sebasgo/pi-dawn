import axios from 'axios'

const $axios = axios.create({
  baseURL: '/api/1.0/'
})

export default {
  getRadioState(cb) {
    $axios.get('radio').then((response) => {
      cb(response.data)
    })
  },
  setRadioState(data, cb) {
    $axios.patch('radio', data).then((response) => {
      cb(response.data)
    })
  }
}
