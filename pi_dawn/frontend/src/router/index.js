import Vue from 'vue'
import Router from 'vue-router'
import Alarms from '@/components/Alarms'
import FourOhFour from '@/components/FourOhFour'
import Light from '@/components/Light'
import Radio from '@/components/Radio'
import RadioStationsDialog from '@/components/RadioStationsDialog'

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
      component: Alarms
    },
    {
      path: '/light',
      component: Light
    },
    {
      path: '/radio',
      component: Radio,
      children: [
        {
          path: 'stations',
          component: RadioStationsDialog
        }
      ]
    },
    {
      path: '*',
      component: FourOhFour
    }
  ]
})
