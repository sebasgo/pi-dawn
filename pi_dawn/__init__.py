import errno
import subprocess
import os
import sys

import click
import flask

from pi_dawn import model
from pi_dawn import comm
from pi_dawn import templates

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = flask.Flask(__name__,
                      static_folder=os.path.join(ROOT_PATH, 'frontend', 'dist', 'static'),
                      template_folder=os.path.join(ROOT_PATH, 'frontend', 'dist'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/alarms.db'.format(app.instance_path)
    app.config['REDIS_QUEUE_KEY'] = 'pi_dawn_alarm_queue'
    app.config['REDIS_STATE_KEY'] = 'pi_dawn_state'
    app.config['ALARM_PRE_DURATION'] = 60 * 30
    app.config['ALARM_POST_DURATION'] = 60 * 15
    app.config['GAMMA_R'] = 0.45
    app.config['GAMMA_G'] = 0.38
    app.config['GAMMA_B'] = 0.45

    model.db.init_app(app)
    model.db.app = app

    return app


app = create_app()


@app.route('/api/1.0/alarm', methods=['GET'])
def get_alarms():
    alarms = model.Alarm.query.all()
    return flask.jsonify([alarm.to_dict() for alarm in alarms])


@app.route('/api/1.0/alarm', methods=['POST'])
def add_alarm():
    alarm = model.Alarm()
    alarm.update_from_dict(flask.request.json)
    alarm.schedule_next_alarm()
    model.db.session.add(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['GET'])
def get_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['PATCH'])
def update_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    alarm.update_from_dict(flask.request.json)
    alarm.schedule_next_alarm()
    model.db.session.add(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return flask.jsonify(alarm.to_dict())


@app.route('/api/1.0/alarm/<int:id>', methods=['DELETE'])
def delete_alarm(id):
    alarm = model.Alarm.query.filter(model.Alarm.id == id).first()
    if alarm is None:
        flask.abort(404)
    model.db.session.delete(alarm)
    model.db.session.commit()
    comm.send_message(app, comm.ReloadAlarmsMessage())
    return '', 204


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


@app.route('/api', defaults={'path': ''})
@app.route('/api/<path:path>')
def api_four_oh_four(path):
    flask.abort(404)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return flask.render_template("index.html")


@app.cli.command()
def initdb():
    if not os.path.exists(app.instance_path):
        os.mkdir(app.instance_path)
    model.db.create_all()

@app.cli.command()
@click.option('--sites-available-directory', default='/etc/nginx/sites-available')
@click.option('--sites-enabled-directory', default='/etc/nginx/sites-enabled')
@click.option('--server-name', default='_')
def setup_nginx(sites_available_directory, sites_enabled_directory, server_name):
    site = 'pi-dawn.conf'
    conf_file_path = os.path.abspath(os.path.join(sites_available_directory, site))
    link_file_path = os.path.join(sites_enabled_directory, site)
    default_site_path = os.path.join(sites_enabled_directory, 'default')
    with open(conf_file_path, mode='w') as conf_file:
        conf_file.write(templates.NGINX_CONF.format(server_name=server_name))
    try:
        os.symlink(conf_file_path, link_file_path)
    except IOError as e:
        if e.errno != errno.EEXIST:
            pass
    try:
        os.unlink(default_site_path)
    except IOError as e:
        if e.errno != errno.ENOENT:
            pass
    subprocess.check_call(['nginx', '-t'])
    subprocess.check_call(['nginx', '-s', 'reload'])


@app.cli.command()
@click.option('--target-directory', default='/etc/systemd/system')
@click.option('--effective-user', default='pi')
def install_services(target_directory, effective_user):
    bin_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    services = {
        'pi-dawn-web': templates.WEB_SERVICE,
        'pi-dawn': templates.MAIN_SERVICE,
    }
    for name, template in services.items():
        unit_file_path = os.path.abspath(os.path.join(target_directory, '{}.service'.format(name)))
        with open(unit_file_path, mode='w') as unit_file:
            unit_file.write(template.format(bin_path=bin_path, user=effective_user))

    subprocess.check_call(['systemctl', 'daemon-reload'])
    for name in services:
        subprocess.check_call(['systemctl', 'start', name])
        subprocess.check_call(['systemctl', 'enable', name])
