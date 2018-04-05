import attr

from rp_sunrise_alarm import hw

@attr.s
class GradientStop:
    pos = attr.ib(type=float)
    r = attr.ib(type=int)
    g = attr.ib(type=int)
    b = attr.ib(type=int)


@attr.s(init=False)
class Surface:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.data = 3 * self.width * self.height * [0]

    def fill(self, r, g, b):
        self.data = self.width * self.height * [r, g, b]

    def get_pixel(self, x, y):
        offset = 3 * (y * self.width + x)
        r = self.data[offset]
        g = self.data[offset+1]
        b = self.data[offset+2]
        return r, g, b

    def draw_gradient(self, stops):
        for y in range(self.height):
            pos = y / self.height
            lower_stop = stops[0]
            upper_stop = stops[-1]
            for stop in stops:
                if pos >= stop.pos and stop.pos > lower_stop.pos:
                    lower_stop = stop
                if pos < stop.pos and stop.pos < upper_stop.pos:
                    upper_stop = stop

            pos_diff = upper_stop.pos - lower_stop.pos
            pos_between_stops = (pos - lower_stop.pos) / pos_diff
            pos_between_stops_inverse = 1 - pos_between_stops

            r = round(lower_stop.r * pos_between_stops_inverse + upper_stop.r * pos_between_stops)
            g = round(lower_stop.g * pos_between_stops_inverse + upper_stop.g * pos_between_stops)
            b = round(lower_stop.b * pos_between_stops_inverse + upper_stop.b * pos_between_stops)

            self.draw_line(y, r, g, b)

    def draw_line(self, y, r, g, b):
        offset = 3 * y * self.width
        for x in range(self.width):
            self.data[offset + 3*x] = r
            self.data[offset + 3*x + 1] = g
            self.data[offset + 3*x + 2] = b

    def interpolate(self, other, factor):
        factor_inverse = 1 - factor
        for i in range(len(self.data)):
            self.data[i] = round(self.data[i] * factor + other.data[i] * factor_inverse)


@attr.s
class SunriseAlarmStep:
    time = attr.ib()
    gradient = attr.ib()


@attr.s
class KeyFrame:
    time = attr.ib()
    surface = attr.ib()

@attr.s(init=False)
class Sunrise:

    steps = [
        SunriseAlarmStep(time=-1.0, gradient=[
            GradientStop(0.0, 0, 0, 0),
            GradientStop(1.0, 0, 0, 0),

        ]),
        SunriseAlarmStep(time=-0.67, gradient=[
            GradientStop(0.0, 51, 0, 105),
            GradientStop(0.75, 51, 0, 105),
            GradientStop(1.0, 255, 0, 0),
        ]),
        SunriseAlarmStep(time=-0.33, gradient=[
            GradientStop(0.0, 127, 0, 0),
            GradientStop(0.5, 127, 0, 0),
            GradientStop(1.0, 255, 255, 0),
        ]),
        SunriseAlarmStep(time=0, gradient=[
            GradientStop(0.0, 255, 255, 255),
            GradientStop(1.0, 255, 255, 255),
        ]),
        SunriseAlarmStep(time=1, gradient=[
            GradientStop(0.0, 255, 255, 255),
            GradientStop(1.0, 255, 255, 255),
        ]),
    ]

    def __init__(self, led_screen: hw.LedScreen):
        self.key_frames = []

        for step in self.steps:
            surface = led_screen.make_surface()
            surface.draw_gradient(step.gradient)
            self.key_frames.append(KeyFrame(step.time, surface))

    def draw(self, surface: Surface, time: float):
        lower_key_frame = self.key_frames[0]
        upper_key_frame = self.key_frames[-1]
        for key_frame in self.key_frames:
            if time >= key_frame.time and key_frame.time > lower_key_frame.time:
                lower_key_frame = key_frame
            if time < key_frame.time and key_frame.time < upper_key_frame.time:
                upper_key_frame = key_frame
        time_between_key_frames = (time - lower_key_frame.time) / (upper_key_frame.time - lower_key_frame.time)
        surface.data = lower_key_frame.surface.data[:]
        surface.interpolate(upper_key_frame.surface, 1-time_between_key_frames)
