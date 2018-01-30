<template>
  <v-container fluid>
    <v-card>
      <v-container fluid>
        <v-layout row>
          <v-flex xs12 flexbox>
            <h3 class="display-1">{{ time }}</h3>
          </v-flex>
          <v-flex>
            <v-switch v-model="enabled" color="primary"/>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex xs12>
            <v-checkbox v-model="repeat" label="Repeat" color="primary"/>
          </v-flex>
        </v-layout>
        <v-layout justify-space-between>
          <v-flex>
            <v-avatar class="indigo"><span class="white--text">M</span></v-avatar>
          </v-flex>
          <v-flex>
            <v-avatar class="indigo lighten-4"><span class="black--text">T</span></v-avatar>
          </v-flex>
          <v-flex>
            <v-avatar class="indigo lighten-4"><span class="black--text">W</span></v-avatar>
          </v-flex>
          <v-flex>
            <v-avatar class="indigo lighten-4"><span class="black--text">T</span></v-avatar>
          </v-flex>
          <v-flex>
            <v-avatar class="indigo lighten-4"><span class="black--text">S</span></v-avatar>
          </v-flex>
          <v-flex>
            <v-avatar class="indigo lighten-4"><span class="black--text">S</span></v-avatar>
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-btn flat color="red">Delete</v-btn>
      </v-card-actions>
    </v-card>

    <v-layout row justify-center>
      <v-dialog v-model="showAddDialog" width="290px">
        <v-time-picker v-model="time" actions format="24hr" autosave="true">
        </v-time-picker>
      </v-dialog>
    </v-layout>

    <v-btn id="add-btn" dark fab fixed bottom right color="primary" @click.native.stop="showAddDialog = true"><v-icon>add</v-icon></v-btn>
  </v-container>
</template>

<script>
export default {
  name: 'Alarms',
  data () {
    return {
      enabled: true,
      repeat: true,
      showDialog: false,
      time: "07:00",
      showAddDialog: false,
    }
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
</style>
