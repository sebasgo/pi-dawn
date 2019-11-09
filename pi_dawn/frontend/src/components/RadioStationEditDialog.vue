<template>
  <v-dialog v-model="visible">
    <v-card tile>
      <v-card-title>
        <span class="headline" v-text="title"></span>
      </v-card-title>
      <v-card-text>
        <v-container fluid class="pa-0">
          <v-form v-model="valid">
            <v-row dense>
              <v-col cols="12">
                <v-text-field label="Name" v-model="station_data.name" :rules="[requiredRule]"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Description" v-model="station_data.description"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Stream URL" v-model="station_data.stream_url" :rules="[requiredRule, isUrlRule]"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Homepage URL" v-model="station_data.homepage_url" :rules="[isUrlRule]"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Artwork URL" v-model="station_data.artwork_url" :rules="[isUrlRule]"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete label="Codec" v-model="station_data.codec" :items="codecs"></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-text-field label="Bitrate" type="number" suffix="kbps" v-model="station_data.bitrate"></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" text @click="delete_()">Delete</v-btn>
        <v-spacer></v-spacer>
        <v-btn text @click="close()">Close</v-btn>
        <v-btn color="primary" text @click="save()" :disabled="!valid">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  import isURL from 'is-url'

  export default {
      data () {
          return {
              valid: false,
              station_data: {
                  name: "",
                  description: "",
                  stream_url: "",
                  artwork_url: "",
                  homepage_url: "",
                  codec: "",
                  bitrate: 320
              },
              requiredRule: v => !!v || 'Required',
              isUrlRule: v =>  v === '' || isURL(v) || 'Not a valid URL',
              codecs: ['MP3', 'AAC', 'AAC+', 'Ogg/Vorbis', 'Flac']
          }
      },
      props: {
          value: {
              type: Boolean,
              required: true
          },
          station_id: {
              required: false
          }
      },
      computed: {
          visible: {
              get () {
                  return this.value
              },
              set (value) {
                  this.$emit('input', value)
              }
          },
          title () {
              return this.station_id !== null? "Edit Radio Station": "Add Radio Station"
          }
      },
      watch: {
          station_id () {
              this.update()
          },
          visible () {
              this.update()
          }
      },
      methods: {
          update () {
              if (!this.visible) {
                  return
              }
              if (this.station_id !== null) {
                  var station = this.$store.getters.getStationById(this.station_id)
                  this.station_data.name = station.name
                  this.station_data.description = station.description
                  this.station_data.stream_url = station.stream_url
                  this.station_data.artwork_url = station.artwork_url
                  this.station_data.homepage_url = station.homepage_url
                  this.station_data.codec = station.codec
                  this.station_data.bitrate = station.bitrate
              }
              else {
                  this.station_data.name = ""
                  this.station_data.description = ""
                  this.station_data.stream_url = ""
                  this.station_data.artwork_url = ""
                  this.station_data.homepage_url = ""
                  this.station_data.codec = ""
                  this.station_data.bitrate = 320
              }
          },
          close () {
              this.visible = false
          },
          save () {
              let data = this.station_data
              if (this.station_id !== null) {
                  this.$store.dispatch('updateRadioStation', {id: this.station_id, data})
              }
              else {
                  this.$store.dispatch('addRadioStation', {data})
              }
              this.close()
          },
          delete_ () {
              if (this.station_id !== null) {
                  this.$store.dispatch('deleteRadioStation', {id: this.station_id})
                  this.close()
              }
          }
      }
  }
</script>

<style scoped>

</style>