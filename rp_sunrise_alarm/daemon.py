import signal
import datetime

import attr

from rp_sunrise_alarm import app
from rp_sunrise_alarm import comm
from rp_sunrise_alarm import graphics
from rp_sunrise_alarm import model
from rp_sunrise_alarm import hw


def shutdown(signum, frame):
    comm.send_message(app, comm.StopMessage())


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

state = comm.State()

led_screen = hw.LedScreen(width=10, height=32)


comm.set_state(app, state)

sunrise_alarm = graphics.Sunrise(led_screen)


def configure_led_screen(state: comm.State, alarms, led_screen):
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



def find_active_alarm(alarms):
    now = datetime.datetime.now()
    for alarm in alarms:
        alarm_time = alarm.next_alarm()
        diff = (now - alarm_time).total_seconds()
        if diff < 0 and -diff < app.config['ALARM_PRE_DURATION']:
            return alarm, diff / app.config['ALARM_PRE_DURATION']
        elif diff > 0 and diff < app.config['ALARM_POST_DURATION']:
            return alarm, diff / app.config['ALARM_POST_DURATION']
    return None, 0


alarms = model.Alarm.query.all()

while True:
    model.db.session.rollback()
    msg = comm.receive_message(app, timeout=1)
    if isinstance(msg, comm.StopMessage):
        break
    elif isinstance(msg, comm.SetLightStateMessage):
        state.light_on = msg.on
    elif isinstance(msg, comm.ReloadAlarmsMessage):
        alarms = model.Alarm.query.order_by(model.Alarm.time).all()
    configure_led_screen(state, alarms, led_screen)
    print(state)

    comm.set_state(app, state)


