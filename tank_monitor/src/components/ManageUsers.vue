<template>
  <div>
    <app-nav></app-nav>
    <h2>All users</h2>
    <table class='center'>
      <tr>
        <th>
          User
        </th>
        <td v-for="item in this.userlist.users" v-bind:key="item">
          {{ item }}
        </td>
      </tr>
      <tr>
        <th>
          Role
        </th>
        <td v-for="item in this.userlist.role" v-bind:key="item">
          {{ item }}
        </td>
      </tr>
    </table>
    <br><br>
    <button v-on:click="displayAdd()">Add a user</button>
    <br><br>
    <div v-if="this.display == 'add'">
      <table class='center'>
      <tr>
        <td>
          Username
        </td>
        <td>
          Role
        </td>
          <td>
          Password
        </td>
      </tr>
      <tr>
        <td>
          <input v-model="NewUser">
        </td>
        <td>
          <select v-model="Newrole">
            <option disabled value="">Select role for new user</option>
            <option value="admin">Superuser</option>
            <option value="user">Normal user</option>
          </select>
        </td>
        <input v-model="password" type="password">
      </tr>
      <tr>
        <td colspan="3">
          <br><br>
          <button v-on:click="addAUser({'username': NewUser, 'password': password, 'role': Newrole })">Add user now</button>
          <br><br>
        </td>
      </tr>
    </table>
    </div>
    <br><br>
    <button v-on:click="displayDel()">Delete a user</button>
    <br><br>
    <div v-if="this.display == 'del'">
      <ul class='center'>
        <li>
          <select v-model="DelUser">
           <option disabled value="">Select user to delete</option>
           <option v-for="item in this.userlist.users" v-bind:key="item">{{ item }}</option>
         </select>
        </li>
        <li>
          <button v-on:click="delAUser(DelUser)">Delete user now</button>
        </li>
      </ul>
    </div>
    <br><br>
    <button v-on:click="displayUpdate()">Update a user</button>
    <br><br>
    <div v-if="this.display == 'update'">
      <ul>
        <li>
          <select v-model="UpdateUser">
           <option disabled value="">Select user to update</option>
           <option v-for="item in this.userlist.users" v-bind:key="item">{{ item }}</option>
         </select>
        </li>
        <li>
          <select v-model="UpdateUserRole">
           <option disabled value="">Select role</option>
           <option value='admin'>Superuser</option>
           <option value='user'>Normal user</option>
         </select>
         <button v-on:click="updateAUser({'username': UpdateUser, 'col': 'role', 'data': UpdateUserRole })">Update user now</button>
        </li>
        <li>
          New password
          <input v-model="NewPass">
          <button v-on:click="updateAUser({'username': UpdateUser, 'col': 'password', 'data': NewPass })">Update user now</button>
        </li>
      </ul>
    </div>
    <div v-if="this.message">
      {{ this.message.message }}
    </div>
  </div>
</template>

<script>
import { getUsers, addUser, delUser, updateUser } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'users',
  data () {
    return {
      userlist: [],
      Newrole: '',
      NewUser: '',
      password: '',
      DelUser: '',
      display: '',
      UpdateUser: '',
      UpdateUserRole: '',
      NewPass: '',
      messsage: '',
      disp: ''
    }
  },
  components: {
    AppNav
  },
  methods: {
    getUsers () {
      getUsers().then((ret) => {
        this.userlist = ret
      })
    },
    addAUser (data) {
      this.disp = ''
      addUser(data).then((ret) => {
        this.message = ret
        this.getUsers()
        this.disp = '1'
        console.log(ret)
      })
    },
    delAUser (data) {
      this.disp = ''
      delUser(data).then((ret) => {
        this.message = ret
        this.getUsers()
        this.disp = '1'
        console.log(ret)
      })
    },
    displayDel () {
      this.display = 'del'
    },
    displayAdd () {
      this.display = 'add'
    },
    displayUpdate () {
      this.display = 'update'
    },
    updateAUser (data) {
      this.disp = ''
      updateUser(data).then((ret) => {
        this.message = ret
        this.disp = '1'
        console.log(ret)
      })
    }
  },
  mounted () {
    this.getUsers()
    console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

.center {
  margin: auto;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b283;
}
</style>
