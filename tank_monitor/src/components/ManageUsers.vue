<template>
  <div class="users">
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
      <div v-if="this.display == 'add'">
        <table>
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
          <input v-model="password">
        </tr>
        <tr>
          <td colspan="3">
            <button v-on:click="addAUser({'username': NewUser, 'password': password, 'role': Newrole })">Add user now</button>
          </td>
        </tr>
      </table>
      </div>
      <button v-on:click="displayDel()">Delete a user</button>
      <div v-if="this.display == 'del'">
        <ul>
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
  </div>
</template>

<script>
import { getUsers, addUser, delUser } from '../../utils/tank-api'
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
      display: ''
    }
  },
  components: {
    AppNav
  },
  methods: {
    getUsers () {
      getUsers().then((ret) => {
        console.log(ret)
        this.userlist = ret
      })
    },
    addAUser (data) {
      addUser(data)
    },
    delAUser (data) {
      delUser(data)
    },
    displayDel () {
      this.display = 'del'
    },
    displayAdd () {
      this.display = 'add'
    }
  },
  mounted () {
    this.getUsers()
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
