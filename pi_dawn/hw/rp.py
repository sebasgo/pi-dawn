import attr

import Adafruit_WS2801
import Adafruit_GPIO.SPI

from pi_dawn import graphics

SPI_PORT = 0
SPI_DEVICE = 0


@attr.s(init=False)
class LedScreen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height, gamma_r=2, gamma_g=2, gamma_b=2):
        self.width = width
        self.height = height
        self.lut_r = self.build_gamma_lut(gamma_r)
        self.lut_g = self.build_gamma_lut(gamma_g)
        self.lut_b = self.build_gamma_lut(gamma_b)
        self.bayer_map = self.build_bayer_map()
        self.pixels = Adafruit_WS2801.WS2801Pixels(width*height, spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                r, g, b = surface.get_pixel(x, y)
                r, g, b = self.lut_r[r], self.lut_g[g], self.lut_b[b]
                t = self.bayer_map[y % 2][x % 2]
                r = max(0, min(255, round(r + t)))
                g = max(0, min(255, round(g + t)))
                b = max(0, min(255, round(b + t)))
                if x % 2 == 0:
                    offset = self.height - y - 1 + x * self.height
                else:
                    offset = y + x * self.height
                self.pixels.set_pixel_rgb(offset, r, b, g)
        self.pixels.show()

    @staticmethod
    def build_gamma_lut(g):
        inverse_g = 1 / g
        return [255 * ((i / 255) ** inverse_g) for i in range(256)]

    @staticmethod
    def build_bayer_map():
        map = [
            [0.0, 2.0],
            [3.0, 1.0],
        ]
        for x in range(2):
            for y in range(2):
                map[y][x] = 0.5 * map[y][x] - 1.0
        return map
