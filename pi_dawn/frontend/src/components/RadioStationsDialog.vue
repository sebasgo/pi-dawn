<template>
  <v-dialog :value="true" fullscreen hide-overlay>
    <v-card tile>

      <v-app-bar color="primary">
        <v-btn v-on:click="goBack()" icon>
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title>Radio Stations</v-toolbar-title>
      </v-app-bar>

      <v-list two-line v-model="selectedRadioStationIndex">
        <v-list-item-group v-model="selectedRadioStationIndex" color="primary">
          <RadioStationListItem
              v-for="station in radio_stations"
              :station="station" :key="station.id"
              v-on:edit="editStation(station)">
          </RadioStationListItem>
        </v-list-item-group>
      </v-list>

      <v-speed-dial v-model="fab" bottom right fixed direction="top" transition="fade">
        <template v-slot:activator>
          <v-btn v-model="fab" dark fab color="primary">
            <v-icon v-if="fab">mdi-close</v-icon>
            <v-icon v-else>mdi-plus</v-icon>
          </v-btn>
        </template>
        <v-tooltip left :value="true">
          <template v-slot:activator="{ on }">
            <v-btn dark small fab primary v-on="on" v-on:click="addStation()">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </template>
          <span>Add manually</span>
        </v-tooltip>
        <v-tooltip left :value="true">
          <template v-slot:activator="{ on }">
            <v-btn dark small fab primary v-on="on">
              <v-icon>mdi-search-web</v-icon>
            </v-btn>
          </template>
          <span>Search online</span>
        </v-tooltip>
      </v-speed-dial>

    </v-card>

    <RadioStationEditDialog v-model="editDialogVisible" :station_id="editDialogRadioStationId"></RadioStationEditDialog>

  </v-dialog>
</template>

<script>
  import { mapGetters } from 'vuex'
  import RadioStationListItem from './RadioStationListItem.vue'
  import RadioStationEditDialog from './RadioStationEditDialog.vue'

  export default {
      components: {
          RadioStationListItem,
          RadioStationEditDialog
      },
      data () {
          return {
              selectedRadioStationIndex: null,
              fab: false,
              editDialogVisible: false,
              editDialogRadioStationId: {}
          }
      },
      computed: mapGetters({
          radio_stations: 'radio_stations'
      }),
      watch: {
          selectedRadioStationIndex () {
              let station = this.radio_stations[this.selectedRadioStationIndex].id
              this.$store.dispatch("setRadioState", {station})
              this.goBack()
          }
      },
      methods: {
          goBack () {
              this.$router.go(-1)
          },
          addStation () {
              this.editDialogRadioStationId = null
              this.editDialogVisible = true
          },
          editStation (station) {
              this.editDialogRadioStationId = station.id
              this.editDialogVisible = true
          }
      },
      created () {
          this.$store.dispatch('getRadioStations')
      }
  }
</script>

