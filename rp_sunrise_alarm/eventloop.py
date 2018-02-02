import attr
import queue
import threading

from rp_sunrise_alarm import model


@attr.s
class State(object):
    light_on = attr.ib(default=True)
    lock = attr.ib(default=attr.Factory(threading.Lock), init=False)


class EventLoopThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.event_queue = queue.Queue()
        self.app = None
        self.state = State()

    def run(self):
        print("here's the main loop")
        print(model.Alarm.query.all())
        while True:
            ev = self.event_queue.get()
            with self.state.lock:
                print(ev)
                if ev == 'stop':
                    print('got the stop event')
                    return
                elif ev == 'light-on':
                    print('on')
                    self.state.light_on = True
                elif ev == 'light-off':
                    print('of')
                    self.state.light_on = False


    def switch_light(self, on):
        if on:
            self.event_queue.put('light-on')
        else:
            self.event_queue.put('light-off')

    def wake_up(self):
        self.event_queue.put('tick')

    def stop(self):
        self.event_queue.put('stop')
        self.join()
