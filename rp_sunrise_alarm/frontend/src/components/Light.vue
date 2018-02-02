<template>
  <v-container fill-height justify-center>
    <v-btn-toggle :input-value="toggleValue"><v-btn outline value="on" class="power-button" color="primary" @click="toggle">
        <v-icon class="power-button">power_settings_new</v-icon>
      </v-btn>
    </v-btn-toggle>
  </v-container>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Light',
  computed: {
    toggleValue() {
      return this.on? "on": ""
    },
    ...mapGetters({
      on: 'lightOn'
    })
  },
  methods: mapActions({
    toggle: 'toggleLight'
  }),
  created () {
    this.$store.dispatch('getLight')
  }
}

</script>

<style>
.power-button {
  width: 70vw;
  height: 70vw;
  margin: auto;
  font-size: 70vw !important;
}


</style>
