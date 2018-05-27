<template>
  <div>
    <h1>Login</h1>

    <hr/>

    <form v-on:submit.prevent="login()">
      <table class='center'><tr>
        <td>Username:</td>
        <td><input v-model="data.body.username" /></td>
      </tr><tr>
        <td>Password:</td>
        <td><input v-model="data.body.password" type="password" /></td>
      </tr><tr>
        <td></td>
        <td><label><input v-model="data.rememberMe" type="checkbox" /> Remember Me</label></td>
      </tr><tr>
        <td></td>
      </tr><tr>
        <td></td>
        <td><button type="submit">Login</button></td>
      </tr></table>

      <hr/>

      <div v-show="error" style="color:red; word-wrap:break-word;">{{ error | json }}</div>
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // context: 'login context',
      token: '',
      refresh_token: '',
      role: '',
      data: {
        body: {
          username: '',
          password: ''
        },
        rememberMe: true,
        fetchUser: false
        // redirect: '/users'
      },

      error: null
    }
  },
  // components: {
  //   role
  // },
  mounted () {
    console.log(this.$auth.redirect())
  },

  methods: {
    login () {
      var redirect = this.$auth.redirect()
      this.$auth.login({
        data: this.data.body, // Axios
        rememberMe: this.data.rememberMe,
        redirect: {name: redirect ? redirect.from.name : 'TankLord'},
        fetchUser: this.data.fetchUser,
        success (res) {
          var roleIn = res.data.data.role
          this.$auth.user({'role': roleIn, 'username': this.data.body.username})
          console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
        },
        error (res) {
          console.log('error ' + this.context)
          this.error = res.data
        }
      })
    }
  }
}
</script>
<style scoped>

.center {
  margin: auto;
}

</style>
