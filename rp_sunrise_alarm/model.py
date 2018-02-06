import datetime

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False, default='00:00')
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    repeat = db.Column(db.Boolean, nullable=False, default=False)
    repeatDays = db.Column(db.Integer, nullable=False, default=0)

    def next_alarm(self):
        today = datetime.date.today()
        h, m = self.time.split(':')
        return datetime.datetime(today.year, today.month, today.day, int(h), int(m))

