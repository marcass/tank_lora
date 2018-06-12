<template>
    <div class="menu">
      <span>
        <tree
          :data="authtreeData"
          class="tree--small"
          @node:selected="onNodeSelected"
        />
      </span>
    </div>
</template>

<script>
import Vue from 'vue'
import LiquorTree from 'liquor-tree'
// global registration
Vue.use(LiquorTree)
export default {
  name: 'app-nav',
  methods: {
    onNodeSelected (node) {
      // var data = this.data
      // console.log('data ' + node.text)
      if (node.text === 'Logout') {
        this.$auth.logout({
          makeRequest: false,
          success () {
            console.log('success ' + this.context)
          },
          error () {
            console.log('error ' + this.context)
          }
        })
        // console.log('logout pressed')
        // console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
        this.$router.push({name: 'Login'})
      } else {
        this.$router.push({name: node.text})
      }
    }
  },
  components: {
  },
  data: () => ({
    authtreeData: [
      {text: 'TankLord',
        children: [
          {text: 'Graphs'},
          {text: 'Logout'},
          {text: 'ManageUsers'},
          {text: 'ManageTanks'}
        ]
      }
    ]
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
