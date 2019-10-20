import Vue from 'vue'
import Router from 'vue-router'
import Alarms from '@/components/Alarms'
import FourOhFour from '@/components/FourOhFour'
import Light from '@/components/Light'
import Radio from '@/components/Radio'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/alarms'
    },
    {
      path: '/alarms',
      name: 'Alarms',
      component: Alarms
    },
    {
      path: '/light',
      name: 'Light',
      component: Light
    },
    {
      path: '/radio',
      name: 'Radio',
      component: Radio
    },
    {
      path: '*',
      name: 'FourOhFour',
      component: FourOhFour
    }
  ]
})
