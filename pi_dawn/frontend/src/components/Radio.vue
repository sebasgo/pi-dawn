<template>
    <v-container fill-height text-center>
        <v-row dense>
            <v-col cols="12">
                <h2>Radio Paradise</h2>
            </v-col>
            <v-col cols="12">
                <v-card>
                <v-img
                    src="https://img.radioparadise.com/content/prod/home/graphics/radio_paradise_318.jpg"
                    aspect-ratio="1"
                ></v-img>
                </v-card>
            </v-col>
            <v-col cols="12">
                <v-btn to="/radio/stations" class="ma-3" icon router>
                    <v-icon>mdi-playlist-music</v-icon>
                </v-btn>
                <v-btn class="ma-3" fab color="primary"><v-icon>mdi-pause</v-icon></v-btn>
                <v-menu top offset-y nudge-top="20">
                    <template v-slot:activator="{ on }">
                        <v-btn class="ma-3" icon v-on="on"><v-icon>mdi-volume-high</v-icon></v-btn>
                    </template>
                    <v-slider
                        v-model="volume"
                        vertical
                        background-color="grey darken-4"
                        ></v-slider>
                </v-menu>
            </v-col>
        </v-row>

        <router-view></router-view>
    </v-container>
</template>

<style>
</style>

<script>
export default {
    data () {
        return {
            volume: 50,
        }
    }
}
</script>
