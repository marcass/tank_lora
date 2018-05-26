<template>
  <div>
    <app-nav></app-nav>
    <h1>Tank Table</h1>
   <!-- <div class="col-md-5" v-for="item in tanks" v-bind:key="item.name">
     <ul>
       <li>{{ item.name }} water level is {{ item.level_status }} and battery is {{ item.batt_status }}</li>
     </ul>
   </div> -->
   <table>
     <tr>
       <th>
         Tank name
       </th>
       <th>
         Water status
       </th>
       <th>
         Battery status
       </th>
       <th>
         Tank ID
       </th>
       <th>
         Daimeter
       </th>
       <th>
         Maximum distance
       </th>
       <th>
         Minimum distance
       </th>
       <th>
         Minimum volume
       </th>
       <th>
         Alert percent
       </th>
       <th>
         Graph colour
       </th>
     </tr>
     <tr v-for="item in tanks" v-bind:key="item.name">
       <td>
         {{ item.name }}
       </td>
       <td>
         {{ item.level_status }}
       </td>
       <td>
         {{ item.batt_status }}
       </td>
       <td>
         {{ item.id }}
       </td>
       <td>
         {{ item.diam }}
       </td>
       <td>
         {{ item.max }}
       </td>
       <td>
         {{ item.min }}
       </td>
       <td>
         {{ item.min_vol }}
       </td>
       <td>
         {{ item.min_percent }}
       </td>
       <td>
         {{ item.line_colour }}
       </td>
     </tr>
   </table>
   <h2>Edit a tank</h2>
     <ul>
       <li>
        <select v-model="TankName">
          <option disabled value="">Select tank to edit</option>
          <option v-for="item in tanks" v-bind:key="item.name">{{ item.name }}</option>
        </select>
        <!-- <span>Selected graph type: {{ graph_type }}</span> -->
      </li>
      <li>
       <select v-model="ColName">
         <option disabled value="">Select attribute to edit</option>
         <option v-for="item in DictList" v-bind:key="item">{{ item }}</option>
       </select>
       <!-- <span>Selected graph type: {{ graph_type }}</span> -->
     </li>
      <li>
        <!-- <button v-on:click="editTank(TankName)">Click to edit</button> -->
        <button v-on:click="editTank(TankName)">Click to edit</button>
      </li>
     </ul>
     <div v-if="this.display == true">
       <table>
         <!-- <tr>
           <th colspan=10>
             <h3>{{ TankName }} tank</h3>
           </th>
         </tr>
         <tr>
           <th>
             {{ ColName }}
           </th>
         <tr>
           <td>
             {{ tank.ColName }}
           </td>
        </tr>
        <tr>
          <td>
            {{ tank.ColName }}
          </td>
       </tr> -->
         <tr>
           <td>
             <input v-model="NewVal">
           </td>
         </tr>
       </table>
       <button v-on:click="updateTank({ 'col': ColName, 'name': tank.name, 'data': NewVal })">Update tank now</button>
     </div>
  </div>
</template>

<script>
import { getTanksList, getATank, putTank } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'status',
  data () {
    return {
      tanks: [],
      tank: '',
      TankName: '',
      display: false,
      NewName: '',
      NewLevelStatus: '',
      NewBattStatus: '',
      NewID: '',
      NewDiam: '',
      NewMaxDist: '',
      NewMinDist: '',
      NewMinVol: '',
      NewMinPercent: '',
      NewLineColour: '',
      NewList: [],
      DictList: ['name', 'level_status', 'batt_status', 'id', 'diam', 'max_dist', 'min_dist', 'min_vol', 'min_percent', 'line_colour'],
      ColName: '',
      NewVal: ''
    }
  },
  components: {
    AppNav
  },
  methods: {
    Tanks () {
      getTanksList().then((ret) => {
        console.log(ret)
        this.tanks = ret
      })
    },
    editTank (data) {
      getATank(data).then((ret) => {
        this.tank = ret
      })
      this.display = true
    },
    updateTank (data) {
      console.log(data)
      putTank(data)
    }
  },
  mounted () {
    this.Tanks()
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
