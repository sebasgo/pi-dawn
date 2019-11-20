<template>
  <v-app>
    <v-app-bar app fixed color="indigo darken-4">
      <img id="logo" src="/static/icon-96x96.png">
      <v-toolbar-title>Pi Dawn</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon v-on:click="reload()">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <router-view/>
    </v-content>
    <v-bottom-navigation app fixed :value="true" background-color="indigo darken-2">
      <v-btn to='/alarms' router>
        <span>Alarms</span>
        <v-icon>mdi-alarm</v-icon>
      </v-btn>
      <v-btn to='/light' router>
        <span>Light</span>
        <v-icon>mdi-lightbulb-outline</v-icon>
      </v-btn>
      <v-btn to='/radio' router>
        <span>Radio</span>
        <v-icon>mdi-radio</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
      }
    },
    methods: {
      reload () {
        this.$store.dispatch('getAlarms')
        this.$store.dispatch('getLight')
        this.$store.dispatch('getRadioStations')
        this.$store.dispatch('getRadioState')
      }
    }
  }
</script>

<style>
  #logo {
    border: 1px solid #000;
    border-radius: 3px;
    width: 32px;
    height: 32px;
    margin-right: 16px;
  }
</style>
