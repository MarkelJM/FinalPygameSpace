import os

import pygame as pg

from . import BACKGROUND_COLOUR, FPS, HEIGHT, LIFES, MAIN_TEXT_SIZE,  MESSAGE_COLOUR, TEXT_MARGIN,  WIDTH


class Scenes:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.time = pg.time.Clock()


class Home(Scenes):
    # first scene, home
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        self.logo = pg.image.load(
            os.path.join("resources", "images", "icon.png"))

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, MAIN_TEXT_SIZE)

        self.message =  "'Space' to start playing"
        self.information_text = "Push 'I' to read  game´s history and how to play"
        self.message_pos =  0.75 * HEIGHT
        self.information_pos = self.message_pos + MAIN_TEXT_SIZE + TEXT_MARGIN
        

    def play(self):
        exit = False

        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    exit = True
                if event.type == pg.KEYDOWN and event.key == pg.K_i:
                    exit = True
                    #go to information scene
                if event.type == pg.QUIT:
                    pg.quit()

            self.screen.fill(BACKGROUND_COLOUR)

            self.draw_logo()
            self.draw_text(self.message, self.message_pos)
            self.draw_text(self.information_text, self.information_pos)

            pg.display.flip()

    def draw_logo(self):
        width_logo = self.logo.get_width()
        pos_x = (WIDTH - width_logo) / 2
        pos_y = HEIGHT / 3
        self.screen.blit(self.logo, (pos_x, pos_y))

    def draw_text(self, text_input, sum_pos_y):
        
        text = self.tipography.render(text_input, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (WIDTH - width_text) / 2     # ANCHO/2 - ancho_texto/2
        
        self.screen.blit(text, (pos_x, sum_pos_y))


class Information(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)        

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)

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
