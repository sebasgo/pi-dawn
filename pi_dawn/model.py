import datetime

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False, default='00:00')
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    repeat = db.Column(db.Boolean, nullable=False, default=False)
    repeat_days = db.Column(db.Integer, nullable=False, default=0)
    next_alarm = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'enabled': self.enabled,
            'repeat': self.repeat,
            'repeatDays': self.repeat_days,
            'nextAlarm': self.next_alarm.isoformat() if self.next_alarm else None
        }

    def update_from_dict(self, data):
        self.time = data.get('time', self.time)
        self.enabled = data.get('enabled', self.enabled)
        self.repeat = data.get('repeat', self.repeat)
        self.repeat_days = data.get('repeatDays', self.repeat_days)

    def schedule_next_alarm(self):
        if not self.enabled:
            self.next_alarm = None
            return
        now = datetime.datetime.now()
        today = datetime.date.today()
        hour, minute = self.time.split(':')
        hour, minute = int(hour), int(minute)
        if self.repeat:
            wd = today.weekday()
            day_offsets = [d - wd for d in range(wd, wd+8) if (2**(d%7)) & self.repeat_days]
        else:
            day_offsets = [0, 1]
        print(day_offsets)
        for day_offset in day_offsets:
            next_alarm = datetime.datetime(today.year, today.month, today.day+day_offset, hour, minute)
            if next_alarm > now:
                self.next_alarm = next_alarm
                return
        self.next_alarm = None


class RadioStation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default='')
    description = db.Column(db.String, nullable=False, default='')
    stream_url = db.Column(db.String, nullable=False, default='')
    homepage_url = db.Column(db.String, nullable=False, default='')
    artwork_url = db.Column(db.String, nullable=False, default='')
    codec = db.Column(db.String, nullable=False, default='')
    bitrate = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'stream_url': self.stream_url,
            'homepage_url': self.homepage_url,
            'artwork_url': self.artwork_url,
            'codec': self.codec,
            'bitrate': self.bitrate,
        }

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.description = data.get('description', self.description)
        self.stream_url = data.get('stream_url', self.stream_url)
        self.homepage_url = data.get('homepage_url', self.homepage_url)
        self.artwork_url = data.get('artwork_url', self.artwork_url)
        self.codec = data.get('codec', self.codec)
        self.bitrate = data.get('bitrate', self.bitrate)
