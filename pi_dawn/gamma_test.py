import argparse
import sys
import time

from pi_dawn import hw
from pi_dawn import graphics


def main():
    parser = argparse.ArgumentParser('test gamma correction')
    parser.add_argument('mode', choices=['pulse', 'gradient'])
    parser.add_argument('channel', choices=['r', 'g', 'b'])
    parser.add_argument('gamma', type=float)
    args = parser.parse_args(sys.argv[1:])
    led_screen = hw.LedScreen(width=10, height=32, gamma_r=args.gamma, gamma_g=args.gamma, gamma_b=args.gamma)
    surface = led_screen.make_surface()
    try:
        if args.mode == 'pulse':
            pulse(led_screen, surface, args.channel)
        else:
            gradient(led_screen, surface, args.channel)
    except KeyboardInterrupt:
        pass
    surface.fill(0, 0, 0)
    led_screen.draw_surface(surface)


def pulse(led_screen, surface, channel):
    steps = list(range(32)) + list(range(30, 0, -1))
    while True:
        for step in steps:
            v = 8*(step+1) - 1
            if channel == 'r':
                color = (v, 0, 0)
            elif channel == 'g':
                color = (0, v, 0)
            else:
                color = (0, 0, v)
            surface.fill(*color)
            led_screen.draw_surface(surface)
            time.sleep(0.02)


def gradient(led_screen, surface, channel):
    if channel == 'r':
        stops = [graphics.GradientStop(0.0, 255, 0, 0), graphics.GradientStop(1.0, 7, 0, 0)]
    elif channel == 'g':
        stops = [graphics.GradientStop(0.0, 0, 255, 0), graphics.GradientStop(1.0, 0, 7, 0)]
    else:
        stops = [graphics.GradientStop(0.0, 0, 0, 255), graphics.GradientStop(1.0, 0, 0, 7)]
    surface.draw_gradient(stops)
    led_screen.draw_surface(surface)
    while True:
        time.sleep(0.02)
