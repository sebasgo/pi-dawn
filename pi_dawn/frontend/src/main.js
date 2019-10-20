import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vuetify from 'vuetify/lib'

require('./assets/fonts.css')

Vue.use(Vuetify)

const opts = {
    theme: {
        dark: true
    }
}

new Vue({
  el: '#app',
  router,
  store,
  vuetify: new Vuetify(opts),
  render: h => h(App)
})
