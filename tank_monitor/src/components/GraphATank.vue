<template>
  <div>
    <app-nav></app-nav>
    <h1>Graph a tank</h1>
    <img v-bind:src="'data:image/png;base64,'+graphic" />
  </div>
</template>

<script>
import { getGraph } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'graphs',
  data () {
    return {
      graphic: '',
      tanks: [],
      // payload: '',
      tank_name: '',
      graph_type: '',
      period: '',
      sel_tanks: []
    }
  },
  components: {
    AppNav
  },
  methods: {
    graph () {
      getGraph({'name': 'main', 'type': 'water', 'range': 'days', 'period': '1'}).then((ret) => {
        this.graphic = ret
      })
    }
  },
  mounted () {
    this.graph()
    console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
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
