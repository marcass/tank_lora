<template>
    <div class="menu">
      <!-- <span v-show="!$auth.check()">
        <tree
          :data="nonauthtreeData"
          @node:selected="onNodeSelected"
        />
      </span>
      <span v-show="$auth.check()">
        <span v-show="$auth.check('admin')">
          <tree
            :data="authtreeData"
            class="tree--small"
            @node:selected="onNodeSelected"
          />
        </span>
        <span v-show="$auth.check('user')">
          <tree
            :data="usertreeData"
            @node:selected="onNodeSelected"
          />
        </span>
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
    // logout () {
    //   this.$auth.logout({
    //     makeRequest: false,
    //     success () {
    //       console.log('success ' + this.context)
    //     },
    //     error () {
    //       console.log('error ' + this.context)
    //     }
    //   })
    // },
    onNodeSelected (node) {
      // var data = this.data
      console.log('data ' + node.text)
      if (node.text === 'Logout') {
        // this.$auth.logout({
        //   makeRequest: false,
        //   success () {
        //     console.log('success ' + this.context)
        //   },
        //   error () {
        //     console.log('error ' + this.context)
        //   }
        // })
        console.log('logout pressed')
      } else {
        this.$router.push({name: node.text})
        // this.$router.push('/auth/login')
        // router.push({name: node.text})
      }
    }
  },
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
    ],
    usertreeData: [
      {text: 'TankLord',
        children: [
          {text: 'Graphs'},
          {text: 'Logout'}
        ]
      }
    ],
    nonauthtreeData: [
      {text: 'TankLord',
        children: [
          {text: 'login'}
        ]
      }
    ]
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
