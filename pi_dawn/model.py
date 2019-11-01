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
        for day_offset in day_offsets:
            next_alarm = datetime.datetime(today.year, today.month, today.day, hour, minute)
            next_alarm += datetime.timedelta(days=day_offset)
            if next_alarm > now:
                self.next_alarm = next_alarm
                return
        self.next_alarm = None


