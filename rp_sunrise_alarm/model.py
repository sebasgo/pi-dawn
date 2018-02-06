import datetime

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False, default='00:00')
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    repeat = db.Column(db.Boolean, nullable=False, default=False)
    repeatDays = db.Column(db.Integer, nullable=False, default=0)
    nextAlarm = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'enabled': self.enabled,
            'repeat': self.repeat,
            'repeatDays': self.repeatDays
        }

    def update_from_dict(self, data):
        self.time = data.get('time', self.time)
        self.enabled = data.get('enabled', self.enabled)
        self.repeat = data.get('repeat', self.repeat)
        self.repeatDays = data.get('repeatDays', self.repeatDays)

    def next_alarm(self):
        today = datetime.date.today()
        h, m = self.time.split(':')
        return datetime.datetime(today.year, today.month, today.day, int(h), int(m))

