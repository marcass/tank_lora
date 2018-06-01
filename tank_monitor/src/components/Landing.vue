<template>
  <div>
    <app-nav></app-nav>
    <h1>This is what's been happening in the last day</h1>
    <div v-if="this.display">
      <img v-bind:src="'data:image/png;base64,'+graphic" />
    </div>
    <div v-else>
      <h4>Loading graph......</h4>
    </div>
  </div>
</template>

<script>
import { getGraphs, getTanksDict } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'graphs',
  data () {
    return {
      graphic: '',
      tankList: [],
      display: false
    }
  },
  components: {
    AppNav
  },
  methods: {
    graph () {
      var tankList
      getTanksDict().then((ret) => {
        tankList = ret.name
        getGraphs(JSON.stringify({'tanks': tankList, 'type': 'water', 'range': 'days', 'period': '1'})).then((ret) => {
        // getGraphs(JSON.stringify({'tanks': ['main', 'noels'], 'type': 'water', 'range': 'days', 'period': '1'})).then((ret) => {
          this.graphic = ret
          this.display = true
        })
      })
    }
  },
  mounted () {
    this.graph()
    console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
    // this.Tanks()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
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
