<template>
  <div>
    <app-nav></app-nav>
    <h1>Graph some tanks</h1>
    <div v-if="graphing">
      <div v-if="graphic != ''">
        <img v-bind:src="'data:image/png;base64,'+graphic" />
      </div>
      <div v-else>
        <p>Building your graph, please be patient...</p>
      </div>
    </div>
    <!-- <div v-if="graphic != ''">
      <img v-bind:src="'data:image/png;base64,'+graphic" />
    </div> -->
    <div>
      <table class='center'>
        <tr>
          <td>
            <select v-model="sel_tanks" multiple>
              <option disabled value="">Select tanks(s) to graph</option>
              <option v-for="item in tanks" v-bind:key="item.name">{{ item.name }}</option>
            </select>
            <!-- <br>
            <span>Selected: {{ sel_tanks }}</span> -->
          </td>
          <td>
            <select v-model="graph_type">
              <option disabled value="">Select graph type</option>
              <option value="water">Water level</option>
              <option value="batt">Battery charge</option>
            </select>
            <!-- <span>Selected graph type: {{ graph_type }}</span> -->
          </td>
          <td>
            <select v-model="range">
              <option disabled value="">Select graph range</option>
              <option value="hours">Hours</option>
              <option value="days">Days</option>
            </select>
            <!-- <span>Selected time range: {{ range }}</span> -->
          </td>
          <td>
            <select v-model="period">
              <option disabled value="">Select graph period</option>
              <option v-for="n in 365" v-bind:key="n">{{ n }}</option>
            </select>
            <!-- <span>Selected time range: {{ period }}</span> -->
          </td>
          <!-- <li>
            <span>Selected period: {{ period }}</span>
            <input v-model="period">
          </li> -->
        </tr>
        <tr>
          <td colspan="4">
            <button v-on:click="graph(JSON.stringify({'tanks':sel_tanks, 'type':graph_type, 'range':range, 'period':period}))">Make the graph</button>
            <button v-on:click="graphRaw(JSON.stringify({'tanks':sel_tanks, 'type':graph_type, 'range':range, 'period':period}))">Make raw graph</button>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import { getGraphs, getTanksList, getGraphsRaw } from '../../utils/tank-api'
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
      sel_tanks: [],
      range: '',
      graphing: false
    }
  },
  components: {
    AppNav
  },
  methods: {
    graph (payload) {
      this.graphing = true
      getGraphs(payload).then((ret) => {
        this.graphic = ret
      })
    },
    graphRaw (payload) {
      this.graphing = true
      getGraphsRaw(payload).then((ret) => {
        this.graphic = ret
      })
    },
    getTanks () {
      getTanksList().then((ret) => {
        this.tanks = ret
      })
    }
  },
  mounted () {
    // this.graph(),
    this.getTanks()
    // console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
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

div {
  clear: both;
}
</style>
