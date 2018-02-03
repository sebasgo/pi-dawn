import atexit
import os

import flask
import flask_restless
import requests

from rp_sunrise_alarm import model
from rp_sunrise_alarm import comm

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class VueFlask(flask.Flask):
    @property
    def static_folder(self):
        if self.debug:
            return None
        else:
            return os.path.join(ROOT_PATH, 'static')


def create_app():
    app = VueFlask(__name__,
                   static_folder=None,
                   template_folder=os.path.join(ROOT_PATH, 'frontend'))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['REDIS_QUEUE_KEY'] = 'rp_sunrise_alarm_alarm_queue'
    app.config['REDIS_STATE_KEY'] = 'rp_sunrise_alarm_state'

    model.db.init_app(app)
    model.db.app = app
    model.db.create_all()

    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=model.db)
    manager.create_api(model.Alarm,
                       url_prefix='/api/1.0',
                       methods=['GET', 'POST', 'PATCH', 'DELETE'])

    return app


app = create_app()


@app.route('/api/1.0/light', methods = ['GET'])
def get_light():
    state = comm.get_state(app)
    return flask.jsonify({'on': state.light_on})


@app.route('/api/1.0/light', methods = ['PATCH'])
def patch_light():
    state = comm.get_state(app)
    new_light_on = bool(flask.request.json.get('on'))
    if new_light_on != state.light_on:
        comm.send_message(app, comm.SetLightStateMessage(on=new_light_on))
    return flask.jsonify({'on': new_light_on})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return flask.render_template("index.html")

