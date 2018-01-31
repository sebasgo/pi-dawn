import os

import flask
import flask_sqlalchemy
import flask_restless
import requests

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class VueFlask(flask.Flask):
    @property
    def static_folder(self):
        if self.debug:
            return None
        else:
            return os.path.join(ROOT_PATH, 'static')


db = flask_sqlalchemy.SQLAlchemy()


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False, default='00:00')
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    repeat = db.Column(db.Boolean, nullable=False, default=False)
    repeatDays = db.Column(db.Integer, nullable=False, default=0)


def create_app():
    app = VueFlask(__name__,
                   static_folder=None,
                   template_folder=os.path.join(ROOT_PATH, 'frontend'))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    db.app = app
    db.create_all()
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(Alarm,
                       url_prefix='/api/1.0',
                       methods=['GET', 'POST', 'PATCH', 'DELETE'])
    return app


app = create_app()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return flask.render_template("index.html")