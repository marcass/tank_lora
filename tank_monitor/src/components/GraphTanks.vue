<template>
  <div>
    <app-nav></app-nav>
    <h1>Graph some tanks</h1>
    <ul>
      <li>
        <div v-if="graphic != ''">
          <img v-bind:src="'data:image/png;base64,'+graphic" />
        </div>
      </li>
    <!-- <img v-bind:src="'data:image/png;base64,'+graphic" /> -->
      <li>
        <div v-for="item in tanks" v-bind:key="item.name">
          <input type="checkbox" id="item.id" :value="item.name" v-model="sel_tanks">
          <label for="item.id">{{ item.name }}</label>
          <br>
        </div>
        <!-- <span>Selected tanks: {{ sel_tanks }}</span> -->
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
        <span>Selected period: {{ period }}</span>
        <input v-model="period">
      </li>
      <li>
        <button v-on:click="graph(JSON.stringify({'tanks':sel_tanks, 'type':graph_type, 'range':range, 'period':period}))">Make the graph</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { getGraphs, getTanks } from '../../utils/tank-api'
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
      // getGraph({'name': 'main', 'type': 'water', 'range': 'days', 'period': '1'}).then((ret) => {
      getGraphs(payload).then((ret) => {
        this.graphic = ret
      })
    },
    getTanks () {
      getTanks().then((ret) => {
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
</style>
