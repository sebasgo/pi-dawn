<template>
  <v-container fill-height justify-center>
    <v-btn-toggle v-model="on">
      <v-btn outline value="on" class="power-button" color="primary">
        <v-icon class="power-button">power_settings_new</v-icon>
      </v-btn>
    </v-btn-toggle>
  </v-container>
</template>

<script>

export default {
  name: 'Light',
  data () {
    return {
        on: ''
    }
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
