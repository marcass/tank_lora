<template>
    <div class="menu">
      <!-- <span v-show="!$auth.check()">
        <tree
          :data="nonauthtreeData"
          @node:selected="onNodeSelected"
        />
      </span> -->
      <!-- <span v-if="$auth.check()">
        <span v-if="$auth.check('admin')">
          <tree
            :data="authtreeData"
            class="tree--small"
            @node:selected="this.onNodeSelected"
          />
        </span>
        <span v-if="$auth.check('user')">
          <tree
            :data="this.usertreeData"
            @node:selected="onNodeSelected"
          />
        </span>
      </span>
      <span v-if="$auth.check(undefined)">
        <tree
          :data="this.nonauthtreeData"
          @node:selected="onNodeSelected"
        />
      </span> -->
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
      console.log('data ' + node.text)
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
        console.log('logout pressed')
        console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
        this.$router.push({name: 'Login'})
      } else {
        this.$router.push({name: node.text})
        // this.$router.push('/auth/login')
        // router.push({name: node.text})
      }
    }
    // checkCreds () {
    //   if (!this.$auth.check()) {
    //     this.nonauthtreeData = [{text: 'Login'}]
    //   } else {
    //     this.nonauthtreeData = []
    //     this.authtreeData = [{text: 'TankLord', children: [{text: 'Graphs'}, {text: 'Logout'}, {text: 'ManageUsers'}, {text: 'ManageTanks'}]}]
    //     this.usertreeData = [{text: 'TankLord', children: [{text: 'Graphs'}, {text: 'Logout'}]}]
    //   }
    // }
  },
  created () {
    this.checkCreds()
  },
  // beforeCreate () {
  //   this.nonauthtreeData = [{text: 'Login'}]
  // },
  components: {
    // [tree-nav.name]: LiquorTree
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
    // usertreeData: [
    //   {text: 'TankLord',
    //     children: [
    //       {text: 'Graphs'},
    //       {text: 'Logout'}
    //     ]
    //   }
    // ],
    // nonauthtreeData: [{text: 'Login'}]
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/*.navbar-right { margin-right: 0px !important}

.log {
  margin: 5px 10px 0 0;
}*/
</style>
