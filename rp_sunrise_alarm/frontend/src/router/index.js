import Vue from 'vue'
import Router from 'vue-router'
import Alarms from '@/components/Alarms'
import Light from '@/components/Light'
import FourOhFour from '@/components/FourOhFour'

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
      path: '*',
      name: 'FourOhFour',
      component: FourOhFour
    }
  ]
})
