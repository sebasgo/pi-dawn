import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import {
  Vuetify,
  VApp,
  VAvatar,
  VBottomNav,
  VBtn,
  VBtnToggle,
  VCard,
  VCheckbox,
  VDialog,
  VFooter,
  VGrid,
  VIcon,
  VSwitch,
  VTimePicker,
  VToolbar,
  transitions
} from 'vuetify'

import {
  Ripple
} from 'vuetify/es5/directives'

require('vuetify/src/stylus/app.styl')

Vue.use(Vuetify, {
  components: {
    VApp,
    VAvatar,
    VBottomNav,
    VBtn,
    VBtnToggle,
    VCard,
    VCheckbox,
    VDialog,
    VFooter,
    VGrid,
    VIcon,
    VSwitch,
    VTimePicker,
    VToolbar,
    transitions
  },
  directives: {
    Ripple
  }
})

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
