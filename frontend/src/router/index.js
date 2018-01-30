import Vue from 'vue'
import Router from 'vue-router'
import Alarms from '@/components/Alarms'
import Light from '@/components/Light'

Vue.use(Router)

export default new Router({
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
    }
  ]
})
