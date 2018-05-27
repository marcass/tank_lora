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

export { updateUser, delUser, addUser, getUsers, getTanksDict, getGraph, getGraphsRaw, getGraphs, getTanksList, getATank, putTank, addTank, delTank };

function simple_get(url) {
  return axios.get(url)
  .then(function (response) {
      return response.data
  });
}

function getTanksDict() {
  const url = BASE_URL+'/tanksdict'
  return simple_get(url)
}

function getTanksList() {
  const url = BASE_URL+'/tankslist'
  return simple_get(url)
}

function getATank(data) {
  const url = BASE_URL+'/tank/'
  return simple_get(url+data)
}

function getGraph(payload) {
  const url = BASE_URL+'/tank/graph'
  return axios.post(url, payload)
  .then(function (response) {
      return response.data
  });
}

function getGraphsRaw(payload) {
  const url = BASE_URL+'/tank/rawgraphs'
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

function putTank(payload) {
  const url = BASE_URL+'/tank'
  return axios.put(url, payload);
}

function addTank(payload) {
  const url = BASE_URL+'/tank/add'
  return axios.post(url, payload)
  .then(function (response) {
      return response.data
  });
}

function delTank(tank) {
  const url = BASE_URL+'/tank/remove/'
  return axios.delete(url+tank)
  .then(function (response) {
      return response.data
  });
}

function getUsers() {
  const url = BASE_URL+'/users'
  return simple_get(url)
}

function addUser(payload) {
  const url = BASE_URL+'/user'
  return axios.post(url, payload)
  .then(function (response) {
      return response.data
  });
}

function delUser(user) {
  const url = BASE_URL+'/user/'
  return axios.delete(url+user)
  .then(function (response) {
      return response.data
  });
}

function updateUser(payload) {
  const url = BASE_URL+'/user'
  return axios.put(url, payload)
  .then(function (response) {
      return response.data
  });
}
