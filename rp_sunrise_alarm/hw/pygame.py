import attr
import pygame

from rp_sunrise_alarm import graphics


@attr.s(init=False)
class LedScreen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height, gamma_r=1, gamma_g=1, gamma_b=1):
        self.width = width
        self.height = height

        pygame.init()
        pygame.display.set_mode((10*self.width, 10*self.height))

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        pysurf = pygame.Surface((self.width, self.height), depth=32)
        pysurf.lock()
        for y in range(self.height):
            for x in range(self.width):
                pysurf.set_at((x,y), surface.get_pixel(x, y))
        pysurf.unlock()

        bg = pygame.display.get_surface()
        pygame.transform.scale(pysurf, (bg.get_width(), bg.get_height()), bg)
        pygame.display.flip()

