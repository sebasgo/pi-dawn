import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Vuetify, {
  VApp,
  VAvatar,
  VBottomNav,
  VBtn,
  VBtnToggle,
  VCard,
  VCardActions,
  VCardOptions,
  VCheckbox,
  VContainer,
  VContent,
  VDialog,
  VFlex,
  VFooter,
  VGrid,
  VIcon,
  VLayout,
  VSpacer,
  VSwitch,
  VTimePicker,
  VToolbar,
  VToolbarTitle,
  transitions
} from 'vuetify/lib'

import {
  Ripple
} from 'vuetify/lib/directives'

require('vuetify/src/stylus/app.styl')

require('./assets/fonts.css')

Vue.use(Vuetify, {
  components: {
    VApp,
    VAvatar,
    VBottomNav,
    VBtn,
    VBtnToggle,
    VCard,
    VCardActions,
    VCardOptions,
    VCheckbox,
    VContainer,
    VContent,
    VDialog,
    VFlex,
    VFooter,
    VGrid,
    VIcon,
    VLayout,
    VSpacer,
    VSwitch,
    VTimePicker,
    VToolbar,
    VToolbarTitle,
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
