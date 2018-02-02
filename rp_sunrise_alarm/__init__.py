import atexit
import os

import flask
import flask_restless
import requests

from rp_sunrise_alarm import model
from rp_sunrise_alarm import eventloop

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

    model.db.init_app(app)
    model.db.app = app
    model.db.create_all()

    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=model.db)
    manager.create_api(model.Alarm,
                       url_prefix='/api/1.0',
                       methods=['GET', 'POST', 'PATCH', 'DELETE'])

    event_loop_thread = eventloop.EventLoopThread()
    event_loop_thread.app = app
    event_loop_thread.start()

    app.event_loop_thread = event_loop_thread

    atexit.register(event_loop_thread.stop)

    return app


app = create_app()

@app.route('/api/1.0/light', methods = ['GET'])
def get_light():
    state = app.event_loop_thread.state
    with state.lock:
        return flask.jsonify({'on': state.light_on})


@app.route('/api/1.0/light', methods = ['PATCH'])
def patch_light():
    state = app.event_loop_thread.state
    with state.lock:
        new_state = bool(flask.request.json.get('on'))
        print(new_state, state.light_on)
        if new_state != state.light_on:
            app.event_loop_thread.switch_light(new_state)
        return flask.jsonify({'on': new_state})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return flask.render_template("index.html")

