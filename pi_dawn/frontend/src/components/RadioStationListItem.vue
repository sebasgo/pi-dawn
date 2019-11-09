<template>
  <v-list-item>
    <v-list-item-avatar tile>
      <v-img :src="station.artwork_url"></v-img>
    </v-list-item-avatar>
    <v-list-item-content>
      <v-list-item-title v-text="station.name"></v-list-item-title>
      <v-list-item-subtitle v-text="format_subtitle(station)"></v-list-item-subtitle>
    </v-list-item-content>
      <v-list-item-action>
        <v-btn icon v-on:click.stop="$emit('edit')">
          <v-icon color="grey lighten-1">mdi-pencil</v-icon>
        </v-btn>
      </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  props: {
    station: {
      type: Object,
      required: true
    }
  },
  methods: {
    format_subtitle (station) {
      var details = [station.description, station.codec, "" + station.bitrate + " kbps"]
        return details.filter(s => s !== "").join(" · ")
    }
  }
}
</script>