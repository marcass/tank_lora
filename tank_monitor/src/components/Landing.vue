<template>
  <div>
    <app-nav></app-nav>
    <h1>This is what's been happening in the last day</h1>
    <img v-bind:src="'data:image/png;base64,'+graphic" />
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
      tankList: []
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
        })
      })
    }
  },
  mounted () {
    this.graph()
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
