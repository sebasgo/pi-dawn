<template>
  <v-dialog v-model="dialog" fullscreen hide-overlay>
    <v-card tile>
      <v-app-bar color="primary">
        <v-btn v-on:click="goBack()" icon>
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title>Radio Stations</v-toolbar-title>
      </v-app-bar>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
      data () {
          return {
              dialog: true
          }
      },
      methods: {
          goBack () {
              this.$router.go(-1)
          }
      }
  }
</script>

