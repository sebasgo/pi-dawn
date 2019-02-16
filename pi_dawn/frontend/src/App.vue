<template>
  <v-app dark>
    <v-toolbar fixed app color="indigo darken-4">
      <img id="logo" src="/static/icon-96x96.png">
      <v-toolbar-title>Pi Dawn</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon v-on:click="reload()">
        <v-icon>refresh</v-icon>
      </v-btn>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
    <v-footer :fixed="fixed" :height="56" app>
      <v-bottom-nav :value="true" color="indigo darken-2">
        <v-btn flat to='/alarms' router>
          <span>Alarms</span>
          <v-icon>alarm</v-icon>
        </v-btn>
        <v-btn flat to='/light' router>
          <span>Light</span>
          <v-icon>lightbulb_outline</v-icon>
        </v-btn>
      </v-bottom-nav>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        clipped: false,
        drawer: true,
        fixed: false,
        items: [
          { icon: 'bubble_chart', title: 'Inspire' }
        ],
        miniVariant: false,
        right: true,
        rightDrawer: false,
        title: 'Vuetify.js'
      }
    },
    methods: {
      reload () {
        this.$store.dispatch('getAlarms')
        this.$store.dispatch('getLight')
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
  }
  .footer > *:first-child {
    margin: 0;
  }
</style>
