<template>
  <div>
    <app-nav></app-nav>
    <h1>Tank Table</h1>
   <div class="col-md-5" v-for="item in tanks" v-bind:key="item.name">
     <ul>
       <!-- <li>{{ item.name }} is {{ item.level_status }}</li> -->
       <li>{{ item.name }} water level is {{ item.level_status }} and battery is {{ item.batt_status }}</li>
     </ul>
   </div>
  </div>
</template>

<script>
import { getTanks } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'status',
  data () {
    return {
      tanks: []
    }
  },
  components: {
    AppNav
  },
  methods: {
    getTanks () {
      getTanks().then((ret) => {
        this.tanks = ret
      })
    }
  },
  mounted () {
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
