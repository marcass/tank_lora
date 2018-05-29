// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// import AppNav from './components/AppNav'
import router from './router'
import VueAuth from '@websanova/vue-auth'

// const BASE_URL = 'https://skibo.duckdns.org/tanktestapi'

Vue.router = router

// Vue.http.options.root = 'https://skibo.duckdns.org/tanktestapi'
// Vue.https.options.root = 'https://skibo.duckdns.org/tanktestapi'

Vue.use(VueAuth, {
  auth: require('./bearer.js'),
  http: require('@websanova/vue-auth/drivers/http/axios.1.x.js'),
  router: require('@websanova/vue-auth/drivers/router/vue-router.2.x.js'),
  loginData: {url: 'https://skibo.duckdns.org/tanktestapi/auth/login', method: 'POST', redirect: {name: 'TankLord'}},
  // refreshData: {enabled: false},
  refreshData: {url: 'https://skibo.duckdns.org/tanktestapi/auth/refresh', method: 'POST', enabled: true, interval: 30},
  rolesVar: 'role',
  fetchData: {url: 'https://skibo.duckdns.org/tanktestapi/auth/user', method: 'GET', enabled: false},
  authRedirect: {path: '/'}
  // loginData: {url: '/auth/login'}
  // _parseUserData: function (data) {
  //   console.log(data.data)
  //   return data.data
  // }
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
