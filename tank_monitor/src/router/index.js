import Vue from 'vue'
import Router from 'vue-router'
import TankLord from '@/components/Landing'
import Graphs from '@/components/GraphTanks'
import Graph from '@/components/GraphATank'
import ManageUsers from '@/components/ManageUsers'
import ManageTanks from '@/components/ManageTanks'
import Login from '@/components/Login'
import Three from '@/components/403'
import Four from '@/components/404'

Vue.use(Router)

export default new Router({
  routes: [
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
      path: '/graph/tank',
      name: 'Graph',
      component: Graph
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
    },
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/403',
      name: '403',
      component: Three
    },
    {
      path: '/404',
      name: '404',
      component: Four
    }
  ]
})
