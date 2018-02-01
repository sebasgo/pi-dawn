<template>
  <v-container fluid grid-list-lg>
    <v-layout row wrap v-for="alarm in alarms" :key="alarm.id">
      <v-flex xs12>
        <v-card>
          <v-container fluid grid-list-lg>
            <v-layout row>
              <v-flex xs12 flexbox>
                <h3 class="display-1" v-on:click="setTime(alarm)">{{ alarm.time }}</h3>
              </v-flex>
              <v-flex>
                <v-switch :input-value="alarm.enabled" @click="toggleAlarmEnabled(alarm)" color="primary"/>
              </v-flex>
            </v-layout>
            <v-layout row>
              <v-flex xs12>
                <v-checkbox :input-value="alarm.repeat" @click="toggleAlarmRepeat(alarm)" label="Repeat" color="primary" hide-details/>
              </v-flex>
            </v-layout>
            <v-layout v-if="alarm.repeat" row justify-space-between wrap>
              <v-flex class="repeat-day-cell" v-for="day in repeatDays(alarm)" :key="day.id">
                <v-avatar v-on:click="toggleAlarmRepeatDay(alarm, day)" v-bind:class="{ indigo: day.on }" size="32px">
                  <span class="white--text">{{day.label}}</span>
                </v-avatar>
              </v-flex>
            </v-layout>
          </v-container>
          <v-card-actions>
            <v-btn v-on:click="deleteAlarm(alarm)" flat color="red">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout row justify-center>
      <v-dialog v-model="timePickerVisible" width="290px">
        <v-time-picker v-model="timePickerTime" actions format="24hr" :autosave="true" />
      </v-dialog>
    </v-layout>

    <v-btn id="add-btn" dark fab fixed bottom right color="primary" @click.native.stop="addAlarm"><v-icon>add</v-icon></v-btn>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Alarms',
  data () {
    return {
      timePickerVisible: false,
      timePickerAlarm: null,
      timePickerTime: "",
      days: [
        {id: 1, label: "MO"},
        {id: 2, label: "TU"},
        {id: 4, label: "WE"},
        {id: 8, label: "TH"},
        {id: 16, label: "FR"},
        {id: 32, label: "SA"},
        {id: 64, label: "SU"},
      ]
    }
  },
  computed: mapGetters({
    alarms: 'alarms'
  }),
  watch: {
    timePickerVisible (visible) {
      if (!visible) {
        var data = {}
        Object.assign(data, this.timePickerAlarm)
        data.time = this.timePickerTime
        data.enabled = true
        if (this.timePickerAlarm.id) {
          this.$store.dispatch('updateAlarm', {id: this.timePickerAlarm.id, data})
        }
        else {
          this.$store.dispatch('addAlarm', {data})
        }
      }
    },
  },
  methods: {
    toggleAlarmEnabled (alarm) {
      this.$store.dispatch ('updateAlarm', {id: alarm.id, data: {enabled: !alarm.enabled}})
    },
    toggleAlarmRepeat (alarm) {
      this.$store.dispatch ('updateAlarm', {id: alarm.id, data: {repeat: !alarm.repeat}})
    },
    toggleAlarmRepeatDay (alarm, day) {
      this.$store.dispatch ('updateAlarm', {id: alarm.id, data: {repeatDays: alarm.repeatDays ^ day.id}})
    },
    setTime (alarm) {
      this.timePickerAlarm = alarm
      this.timePickerTime = alarm.time
      this.timePickerVisible = true
    },
    addAlarm () {
      this.timePickerAlarm = {time: "00:00", enabled: true, repeat: false, repeatDays: 31}
      this.timePickerTime = "00:00"
      this.timePickerVisible = true
    },
    deleteAlarm (alarm) {
      this.$store.dispatch ('deleteAlarm', {id: alarm.id})
    },
    repeatDays (alarm) {
      var result = []
      for (let day of this.days) {
        result.push({id: day.id, label: day.label, on: day.id & alarm.repeatDays})
      }
      return result
    }
  },
  created () {
    this.$store.dispatch('getAlarms')
  }
}
</script>

<style>
  #add-btn {
    bottom: 70px;
  }

  .picker--time__title {
    margin: auto !important;
  }

  .repeat-day-cell {
    cursor: pointer;
    flex: 0;
  }
</style>
