import signal
import datetime

from rp_sunrise_alarm import app
from rp_sunrise_alarm import comm
from rp_sunrise_alarm import graphics
from rp_sunrise_alarm import model
from rp_sunrise_alarm import hw


def shutdown(signum, frame):
    comm.send_message(app, comm.StopMessage())


def configure_led_screen(state, alarms, led_screen, sunrise_alarm):
    surface = led_screen.make_surface()

    if state.light_on:
        surface.fill(255, 255, 255)
    else:
        active_alarm, alarm_pos = find_active_alarm(alarms)
        if active_alarm is None:
            surface.fill(0, 0, 0)
            state.active_alarm = -1
        else:
            state.active_alarm = active_alarm.id
            sunrise_alarm.draw(surface, alarm_pos)

    led_screen.draw_surface(surface)


def reschedule_alarms(alarms):
    dirty = False
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=app.config['ALARM_POST_DURATION'])
    for alarm in alarms:
        if alarm.next_alarm is not None and alarm.next_alarm < cutoff:
            dirty = True
            if not alarm.repeat:
                alarm.enabled = False
            alarm.schedule_next_alarm()
    if dirty:
        model.db.session.commit()


def find_active_alarm(alarms):
    now = datetime.datetime.now()
    for alarm in alarms:
        alarm_time = alarm.next_alarm
        if alarm_time is None:
            continue
        diff = (now - alarm_time).total_seconds()
        if diff < 0 and -diff < app.config['ALARM_PRE_DURATION']:
            return alarm, diff / app.config['ALARM_PRE_DURATION']
        elif diff > 0 and diff < app.config['ALARM_POST_DURATION']:
            return alarm, diff / app.config['ALARM_POST_DURATION']
    return None, 0


def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    state = comm.State()
    led_screen = hw.LedScreen(width=10, height=32, gamma_r=app.config['GAMMA_R'], gamma_b=app.config['GAMMA_B'],
                              gamma_g=app.config['GAMMA_G'])
    sunrise_alarm = graphics.Sunrise(led_screen)
    alarms = model.Alarm.query.order_by(model.Alarm.time).all()

    while True:
        msg = comm.receive_message(app, timeout=1)
        if isinstance(msg, comm.StopMessage):
            break
        elif isinstance(msg, comm.SetLightStateMessage):
            state.light_on = msg.on
        elif isinstance(msg, comm.ReloadAlarmsMessage):
            model.db.session.rollback()
            alarms = model.Alarm.query.order_by(model.Alarm.time).all()
        configure_led_screen(state, alarms, led_screen, sunrise_alarm)
        reschedule_alarms(alarms)
        comm.set_state(app, state)
