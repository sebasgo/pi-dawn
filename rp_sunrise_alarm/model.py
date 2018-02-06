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
            'repeatDays': self.repeat_days

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
            print(self.repeat_days)
            print([2**(d%7) for d in range(today.weekday(), today.weekday()+7)])
            day_offsets = [d - wd for d in range(wd, wd+8) if (2**(d%7)) & self.repeat_days]
        else:
            day_offsets = [0, 1]
        print(day_offsets)
        for day_offset in day_offsets:
            next_alarm = datetime.datetime(today.year, today.month, today.day+day_offset, hour, minute)
            if next_alarm > now:
                self.next_alarm = next_alarm
                print(self.next_alarm)
                return
        self.next_alarm = None


