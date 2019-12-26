import threading
import time

import attr
import vlc


@attr.s
class VolumeFader:
    media_player = attr.ib()
    _base_volume = attr.ib(default=0, init=False)
    _target_volume = attr.ib(default=0, init=False)
    _step = attr.ib(default=0, init=False)
    _steps = attr.ib(default=0, init=False)
    _step_duration = attr.ib(default=0.05, init=False)
    _is_fading = attr.ib(default=False, init=False)
    _volume_lock = attr.ib(factory=threading.Lock, init=False, repr=False)
    _on_finished = attr.ib(default=None, init=False, repr=False)
    _fade_thread = attr.ib(default=None, init=False, repr=False)

    def set_volume(self, volume, fade_duration, on_finished=None):
        with self._volume_lock:
            self._base_volume = self.media_player.audio_get_volume()
            self._target_volume = volume
            self._step = 0
            self._on_finished = on_finished
            if fade_duration == 0:
                self._steps = 0
                self._volume_step = 0
            else:
                self._steps = fade_duration // self._step_duration
                self._volume_step = (self._target_volume - self._base_volume) / self._steps
            if not self._is_fading:
                self._is_fading = True
                self._fade_thread = threading.Thread(target=self.fade)
                self._fade_thread.start()
        if fade_duration == 0:
            self._fade_thread.join()

    def get_volume(self):
        return self._target_volume

    def fade(self):
        while True:
            with self._volume_lock:
                if self._step >= self._steps:
                    self.media_player.audio_set_volume(self._target_volume)
                    self._is_fading = False
                    if self._on_finished is not None:
                        self._on_finished()
                    return
                volume = round(self._base_volume + self._step * self._volume_step)
                self.media_player.audio_set_volume(volume)
                self._step += 1
            time.sleep(self._step_duration)


@attr.s
class RadioPlayer:

    fade_duration = attr.ib(default=0.5, converter=float)

    _station = attr.ib(default=None, init=False)
    _is_playing = attr.ib(default=False, init=False)
    _is_stopping = attr.ib(default=False, init=False)
    _volume = attr.ib(default=40, init=False)
    _media_player = attr.ib(factory=vlc.MediaPlayer, init=False, repr=False)
    _volume_fader = attr.ib(default=attr.Factory(lambda self:VolumeFader(self._media_player),
                                                 takes_self=True),
                            init=False, repr=False)

    def __attrs_post_init__(self):
        event_manager = self._media_player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self._handle_playing)

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, station):
        if self._station == station:
            return
        self._station = station
        self._is_stopping = False
        if self._station is None:
            self._is_stopping = True
            self._volume_fader.set_volume(0, self.fade_duration, self._stop)
        else:
            if not self._is_playing:
                self._media_player.audio_set_volume(0)
            self._media_player.set_media(vlc.Media(station.stream_url))
            self._media_player.play()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
        if self._is_playing:
            self._volume_fader.set_volume(volume, self.fade_duration)

    def _stop(self):
        if self._is_stopping:
            self._is_playing = False
            self._is_stopping = False
            self._media_player.stop()

    def _handle_playing(self, *args, **kwargs):
        self._is_playing = True
        self._volume_fader.set_volume(self._volume, self.fade_duration)
