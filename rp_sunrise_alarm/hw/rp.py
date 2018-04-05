import attr

import Adafruit_WS2801
import Adafruit_GPIO.SPI

from rp_sunrise_alarm import graphics

SPI_PORT = 0
SPI_DEVICE = 0


@attr.s(init=False)
class LedScreen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height, gamma_r=2, gamma_g=2, gamma_b=2):
        self.width = width
        self.height = height
        self.pixels = Adafruit_WS2801.WS2801Pixels(width*height, spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        self.lut_r = self.build_gamma_lut(gamma_r)
        self.lut_g = self.build_gamma_lut(gamma_g)
        self.lut_b = self.build_gamma_lut(gamma_b)

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                r, g, b = surface.get_pixel(x, y)
                r, g, b = self.lut_r[r], self.lut_g[g], self.lut_b[b]
                if x % 2 == 0:
                    offset = self.height - y - 1 + x * self.height
                else:
                    offset = y + x * self.height
                self.pixels.set_pixel_rgb(offset, r, b, g)
        self.pixels.show()

    @staticmethod
    def build_gamma_lut(g):
        inverse_g = 1 / g
        return [int(255 * ((i / 255) ** inverse_g)) for i in range(256)]
