<template>
    <v-container fill-height text-center>
        <v-row dense>
            <v-col cols="12">
                <h2 v-text="station.name"></h2>
            </v-col>
            <v-col cols="12">
                <v-card>
                <v-img
                    :src="station.artwork_url"
                    aspect-ratio="1"
                ></v-img>
                </v-card>
            </v-col>
            <v-col cols="12">
                <v-btn to="/radio/stations" class="ma-3" icon router>
                    <v-icon>mdi-playlist-music</v-icon>
                </v-btn>
                <v-btn class="ma-3" fab color="primary" v-on:click="toggleIsPlaying()">
                    <v-icon v-text="playButtonIcon"></v-icon>
                </v-btn>
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

<style scoped>
</style>

<script>

export default {
    data () {
        return {
        }
    },
    computed: {
        isPlaying: {
            get () {
                return this.$store.state.radio.radioState.is_playing
            },
            set (is_playing) {
                this.$store.dispatch('setRadioState', {is_playing})
            }
        },
        playButtonIcon: {
            get () {
                return this.isPlaying? "mdi-pause": "mdi-play"
            }
        },
        stationId: {
            get () {
                return this.$store.state.radio.radioState.station
            }
        },
        station: {
            get () {
                if (this.stationId !== -1) {
                    return this.$store.getters.getStationById(this.stationId)
                }
                else {
                    return {}
                }
            }
        },
        volume: {
            get () {
                return this.$store.state.radio.radioState.volume
            },
            set (volume) {
                this.$store.dispatch('setRadioState', {volume})
            }
        }
    },
    methods: {
        toggleIsPlaying () {
            this.isPlaying = !this.isPlaying
        }
    },
    created () {
        this.$store.dispatch('getRadioStations')
        this.$store.dispatch('getRadioState')
    }
}
</script>
