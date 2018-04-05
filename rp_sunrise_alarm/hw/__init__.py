import os

if os.environ.get('DEBUG', '0') == '1':
    from rp_sunrise_alarm.hw.pygame import LedScreen
else:
    from rp_sunrise_alarm.hw.rp import LedScreen

__ALL__ = [LedScreen]
