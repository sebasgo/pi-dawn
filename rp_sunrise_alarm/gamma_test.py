import argparse
import sys
import time

from rp_sunrise_alarm import hw


def main():
    parser = argparse.ArgumentParser('test gamma correction')
    parser.add_argument('channel', choices=['r', 'g', 'b'])
    parser.add_argument('gamma', type=float)
    args = parser.parse_args(sys.argv[1:])
    led_screen = hw.LedScreen(width=10, height=32, gamma_r=args.gamma, gamma_g=args.gamma, gamma_b=args.gamma)
    surface = led_screen.make_surface()
    steps = list(range(32)) + list(range(30, 0, -1))
    try:
        while True:
            for step in steps:
                v = 8*(step+1) - 1
                if args.channel == 'r':
                    color = (v, 0, 0)
                elif args.channel == 'g':
                    color = (0, v, 0)
                else:
                    color = (0, 0, v)
                surface.fill(*color)
                led_screen.draw_surface(surface)
                time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    surface.fill(0, 0, 0)
    led_screen.draw_surface(surface)
