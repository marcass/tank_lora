//following block for jwt (see https://github.com/websanova/vue-auth/blob/master/docs/StepByStepGuide.md)

import axios from 'axios'
import VueAxios from 'vue-axios'
import Vue from 'vue'

Vue.use(VueAxios, axios)

// const BASE_URL = 'https://skibo.duckdns.org/api';
const BASE_URL = 'http://localhost:5000';
Vue.axios.defaults.baseURL = BASE_URL;
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';
axios.defaults.headers.delete['Content-Type'] = 'application/json';

// access axios with Vue or use the 'this' reference in components
// Vue.axios.post(...).then(res => {
//     console.log('RES', res);
// });

export { getTanks, getGraph, getGraphs };

function simple_get(url) {
  return axios.get(url)
  .then(function (response) {
      return response.data
  });
}

function getTanks() {
  const url = BASE_URL+'/tanks'
  return simple_get(url)
}

function getGraph(payload) {
  const url = BASE_URL+'/tank/graph'
  return axios.post(url, payload)
  .then(function (response) {
      return response.data
  });
}

function getGraphs(payload) {
  const url = BASE_URL+'/tank/graphs'
  return axios.post(url, payload)
  .then(function (response) {
      return response.data
  });
}

// function getUser(user) {
//   const url = BASE_URL+'/user/data/'+user
//   return simple_get(url)
// }
//
// function getVerifyUser(user, pass) {
//   const url = BASE_URL+'/auth/user/'
//   return axios.get(url+user, pass)
//   .then(function (response) {
//       return response.data
//   });
// }
//
// function getDoors() {
//   const url = BASE_URL+'/doors'
//   return simple_get(url)
// }
//
// function getDoorStatus() {
//   const url = BASE_URL+'/door/status'
//   return simple_get(url)
// }
//
// function getADoorStatus(door) {
//   const url = BASE_URL+'/door/status/'
//   return simple_get(url+door)
// }
//
// function getLog(door, payload) {
//   const url = BASE_URL+'/door/log/'
//   return axios.post(url+door, payload)
//   .then(function (response) {
//       return response.data
//   });
// }
//
// function getAllowedUsers() {
//   const url = BASE_URL+'/listallowed'
//   return simple_get(url)
// }
//
// function login(payload) {
//   // console.log(payload)
//   const url = BASE_URL+'/auth'
//   return axios.post(url, payload)
//   // .then(res => {
//   //   console.log('RES', res)
//   // })
// }
// function putUserData(payload, route) {
//   const url = BASE_URL+'/user/'
//   return axios.put(url+route, payload);
// }
//
// function putAllUserData(payload) {
//   const url = BASE_URL+'/user'
//   return axios.put(url, payload);
// }
//
// function postUserData(payload) {
//   const url = BASE_URL+'/user'
//   return axios.post(url, payload);
// }
//
// function postKeycode(payload) {
//   const url = BASE_URL+'/usekey'
//   return axios.post(url, payload)
//   .then(function (response) {
//       return response.data
//   });
// }
//
// function deleteUser(user) {
//   const url = BASE_URL+'/user/'
//   console.log(user)
//   return axios.delete(url+user)
//   .then(function (response) {
//       return response.data
//   });
// }
//
// function postAuth(user, pass) {
//   const url = BASE_URL+'/auth'
//   return axios.post(user, pass)
//   .then(function (response) {
//       return response.data
//   });
// }
