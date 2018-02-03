import signal

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

alarms = model.Alarm.query.all()
led_screen = hw.LedScreen(width=10, height=32)

surface = led_screen.make_surface()
surface.draw_gradient([
    graphics.GradientStop(0.0, 0, 0, 0),
    graphics.GradientStop(0.8, 0, 0, 0),
    graphics.GradientStop(1.0, 255, 0, 0),
])
led_screen.draw_surface(surface)

comm.set_state(app, state)


def handle_light_switch(state: comm.State, on: bool, led_screen):
    if on:
        state.light_on = True
        surface = led_screen.make_surface()
        surface.fill(255, 255, 255)
        led_screen.draw_surface(surface)
    else:
        state.light_on = False
        surface = led_screen.make_surface()
        surface.fill(0, 0, 0)
        led_screen.draw_surface(surface)


def schedule_alarms(app, state, alarms):
    pass


while True:
    msg = comm.receive_message(app, timeout=1)
    print(msg, isinstance(msg, comm.StopMessage))
    if isinstance(msg, comm.StopMessage):
        break
    elif isinstance(msg, comm.SetLightStateMessage):
        handle_light_switch(state, msg.on, led_screen)
    elif isinstance(msg, comm.ReloadAlarmsMessage):
        alarms = model.Alarm.query.all()
    print(state)

    comm.set_state(app, state)


