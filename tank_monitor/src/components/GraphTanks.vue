<template>
  <div>
    <app-nav></app-nav>
    <h1>Graph some tanks</h1>
    <div v-if="graphic != ''">
      <img v-bind:src="'data:image/png;base64,'+graphic" />
    </div>
    <div>
      <ul>
      <li>
        <select v-model="sel_tanks" multiple>
          <option disabled value="">Select tanks(s) to graph</option>
          <option v-for="item in tanks" v-bind:key="item.name">{{ item.name }}</option>
        </select>
        <!-- <br>
        <span>Selected: {{ sel_tanks }}</span> -->
      </li>
      <li>
        <select v-model="graph_type">
          <option disabled value="">Select graph type</option>
          <option value="water">Water level</option>
          <option value="batt">Battery charge</option>
        </select>
        <!-- <span>Selected graph type: {{ graph_type }}</span> -->
      </li>
      <li>
        <select v-model="range">
          <option disabled value="">Select graph range</option>
          <option value="hours">Hours</option>
          <option value="days">Days</option>
        </select>
        <!-- <span>Selected time range: {{ range }}</span> -->
      </li>
      <li>
        <select v-model="period">
          <option disabled value="">Select graph period</option>
          <option v-for="n in 365" v-bind:key="n">{{ n }}</option>
        </select>
        <!-- <span>Selected time range: {{ period }}</span> -->
      </li>
      <!-- <li>
        <span>Selected period: {{ period }}</span>
        <input v-model="period">
      </li> -->
      <li>
        <button v-on:click="graph(JSON.stringify({'tanks':sel_tanks, 'type':graph_type, 'range':range, 'period':period}))">Make the graph</button>
      </li>
    </ul>
    </div>
  </div>
</template>

<script>
import { getGraphs, getTanksList } from '../../utils/tank-api'
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
      range: ''
    }
  },
  components: {
    AppNav
  },
  methods: {
    graph (payload) {
      getGraphs(payload).then((ret) => {
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

div {
  clear: both;
}
</style>
