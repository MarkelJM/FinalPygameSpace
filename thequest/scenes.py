import os

import pygame as pg

from . import BACKGROUND_COLOUR, FPS, HEIGHT, LIFES,  MESSAGE_COLOUR,   WIDTH


class Scenes:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.time = pg.time.Clock()


class Home(Scenes):
    # first scene, home
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        # self.logo = pg.image.load(
        # os.path.join("resources", "images", "arkanoid_name.png"))

        #font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        #self.tipography = pg.font.Font(font_file, 40)

    def play(self):
        exit = False

        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    exit = True
                if event.type == pg.QUIT:
                    pg.quit()

            self.screen.fill(BACKGROUND_COLOUR)

            self.draw_logo()
            self.draw_text()

            pg.display.flip()

    def draw_logo(self):
        width_logo = self.logo.get_width()
        pos_x = (WIDTH - width_logo) / 2
        pos_y = HEIGHT / 3
        self.screen.blit(self.logo, (pos_x, pos_y))

    def draw_text(self):
        message = "'Space' to start playing"
        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (WIDTH - width_text) / 2     # ANCHO/2 - ancho_texto/2
        pos_y = .75 * HEIGHT
        self.screen.blit(text, (pos_x, pos_y))
