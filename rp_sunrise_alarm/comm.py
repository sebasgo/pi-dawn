import attr
import pickle
import redis

redis_cli = redis.Redis()

@attr.s
class Message:
    pass


@attr.s
class StopMessage(Message):
    pass


@attr.s
class SetLightStateMessage(Message):
    on = attr.ib(type=bool)


@attr.s
class ReloadAlarmsMessage(Message):
    pass


@attr.s
class State:
    light_on = attr.ib(type=bool, default=False)
    active_alarm = attr.ib(type=int, default=-1)


def send_message(app, message):
    data = pickle.dumps(message)
    redis_cli.rpush(app.config['REDIS_QUEUE_KEY'], data)


def receive_message(app, timeout=1):
    data = redis_cli.blpop(app.config['REDIS_QUEUE_KEY'], timeout)
    if data is None:
        return None
    msg = pickle.loads(data[1])
    return msg


def set_state(app, state):
    data = pickle.dumps(state)
    redis_cli.set(app.config['REDIS_STATE_KEY'], data)


def get_state(app):
    data = redis_cli.get(app.config['REDIS_STATE_KEY'])
    if data is None:
        return State()
    return pickle.loads(data)
