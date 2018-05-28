<template>
  <div>
    <app-nav></app-nav>
    <h1>Tank Table</h1>
   <!-- <div class="col-md-5" v-for="item in tanks" v-bind:key="item.name">
     <ul>
       <li>{{ item.name }} water level is {{ item.level_status }} and battery is {{ item.batt_status }}</li>
     </ul>
   </div> -->
   <table class='center'>
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
   <br><br>
   <button v-on:click="displayEdit()">Edit a tank</button>
   <div v-if="this.thingy == 'edit'">
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
         <tr>
           <td v-if="this.ColName == 'tank'">
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName == 'tank_status'">
             <select v-model="NewVal">
              <option disabled value="">Select water level status</option>
              <option value="OK">OK</option>
              <option value="bad">Low</option>
            </select>
           </td>
           <td v-if="this.ColName == 'batt_status'">
             <select v-model="NewVal">
              <option disabled value="">Select battery status</option>
              <option value="OK">OK</option>
              <option value="bad">Low</option>
            </select>
           </td>
           <td v-if="this.ColName =='id'">
             Must be a unique integer not shared by another tank and referenced in sensor code
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName =='diam'">
             The diameter of the tank in cm
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName =='max_dist'">
             The distance from the sensor to the empty level of tank
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName =='min_dist'">
             The distance from the sensor to the full level of tank
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName =='min_percent'">
             The percentage of tank fill when alert is triggered. Must be 0-100
             <input v-model="NewVal">
           </td>
           <td v-if="this.ColName == 'line_colour'">
             <select v-model="NewVal">
              <option disabled value="">Select Line colour from available colours</option>
              <option v-for="item in this.AvailColours" v-bind:key="item">{{ item }}</option>
            </select>
           </td>
         </tr>
       </table>
       <button v-on:click="updateTank({ 'col': ColName, 'name': tank.name, 'data': NewVal })">Update tank now</button>
     </div>
    </div>
    <button v-on:click="displayAdd()">Add a tank</button>
    <div v-if="this.thingy == 'add'">
     <table>
       <tr>
         <th>
           Tank name
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
       <tr>
         <td>
           <input v-model="NewName">
         </td>
         <td>
           <input v-model="NewID">
         </td>
         <td>
           <input v-model="NewDiam">
         </td>
         <td>
           <input v-model="NewMax">
         </td>
         <td>
           <input v-model="NewMin">
         </td>
         <td>
           <input v-model="NewMinVol">
         </td>
         <td>
           <input v-model="NewMinPercent">
         </td>
         <td>
           <select v-model="NewLine">
              <option disabled value="">Select Line colour from available colours</option>
              <option v-for="item in this.AvailColours" v-bind:key="item">{{ item }}</option>
            </select>
         </td>
       </tr>
       <tr>
         <td colspan="8">
          <button v-on:click="addATank({ 'name': NewName, 'nodeID': NewID, 'diam': NewDiam, 'max_payload': NewMax, 'invalid_min': NewMin, 'min_vol': NewMinVol, 'min_percent': NewMinPercent, 'line_colour': NewLine })">Add tank now</button>
         </td>
       </tr>
     </table>
   </div>
   <button v-on:click="displayDel()">Delete a tank</button>
   <div v-if="this.thingy == 'del'">
     <ul>
       <li>
        <select v-model="TankNameDel">
          <option disabled value="">Select tank to delete</option>
          <option v-for="item in tanks" v-bind:key="item.name">{{ item.name }}</option>
        </select>
      </li>
      <li>
        <button v-on:click="delATank(TankNameDel)">Delete tank now</button>
      </li>
    </ul>
  </div>
  </div>
</template>

<script>
import { getTanksList, getTanksDict, getATank, putTank, addTank, delTank } from '../../utils/tank-api'
import AppNav from './AppNav'
export default {
  name: 'status',
  data () {
    return {
      tanks: [],
      tanksdict: '',
      tank: '',
      TankName: '',
      display: false,
      DictList: ['tank', 'tank_status', 'batt_status', 'id', 'diam', 'max_dist', 'min_dist', 'min_percent', 'line_colour'],
      ColName: '',
      NewVal: '',
      LineColours: ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'],
      AvailColours: [],
      NewName: '',
      NewID: '',
      NewDiam: '',
      NewMax: '',
      NewMin: '',
      NewMinVol: '',
      NewMinPercent: '',
      NewLine: '',
      TankNameDel: '',
      thingy: ''
    }
  },
  components: {
    AppNav
  },
  methods: {
    Tanks () {
      getTanksList().then((ret) => {
        this.tanks = ret
      })
    },
    displayEdit () {
      this.thingy = 'edit'
    },
    displayAdd () {
      this.thingy = 'add'
    },
    displayDel () {
      this.thingy = 'del'
    },
    TanksDict () {
      getTanksDict().then((ret) => {
        // array.filter(function(currentValue, index, arr), thisValue)
        this.tanksdict = ret
        var x = this.tanksdict.line_colour
        // eslint-disable-next-line
        Array.prototype.diff = function (a) {
          return this.filter(function (i) { return a.indexOf(i) < 0 })
        }
        this.AvailColours = this.LineColours.diff(x)
      })
    },
    editTank (data) {
      getATank(data).then((ret) => {
        this.tank = ret
      })
      this.display = true
    },
    updateTank (data) {
      putTank(data)
    },
    addATank (data) {
      addTank(data)
    },
    delATank (data) {
      delTank(data)
    }
  },
  mounted () {
    this.Tanks()
    this.TanksDict()
    console.log('user = ' + this.$auth.user().username + ' role = ' + this.$auth.user().role)
    // this.makecolourArray()
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
</style>
