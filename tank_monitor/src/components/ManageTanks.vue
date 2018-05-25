<template>
  <div>
    <app-nav></app-nav>
    <h1>Tank Table</h1>
   <div class="col-md-5" v-for="item in tank_name">
     <ul>
       <!-- <li>{{ item.name }} is {{ item.level_status }}</li> -->
       <li>{{ item }} water level is {{ item in tank_water_status }}</li>
     </ul>
   </div>
  </div>
</template>

<script>
import { getTanks } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'doors',
  data () {
    return {
      tank_name: [],
      tank_water_status: [],
      tank_batt_status: []
    }
  },
  components: {
    AppNav
  },
  methods: {
    getTanks () {
      getTanks().then((ret) => {
        this.tank_name = ret.name
        this.tank_water_status = ret.level_status
        this.tank_batt_status = ret.batt_status
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
