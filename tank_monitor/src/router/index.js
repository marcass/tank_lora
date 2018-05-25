import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TankLord from '@/components/Landing'
import Graphs from '@/components/GraphTanks'
import ManageUsers from '@/components/ManageUsers'
import ManageTanks from '@/components/ManageTanks'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/landing',
      name: 'TankLord',
      component: TankLord
    },
    {
      path: '/graph/tanks',
      name: 'Graphs',
      component: Graphs
    },
    {
      path: '/user/management',
      name: 'ManageUsers',
      component: ManageUsers
    },
    {
      path: '/tank/management',
      name: 'ManageTanks',
      component: ManageTanks
    }
  ]
})
