

import os
import sys
from random import randint

import pygame as pg

from . import BACKGROUND_COLOUR, FPS, HEIGHT, LIFES, MAIN_TEXT_SIZE, MAXIMUM_REPEATED_ROCKS,  MESSAGE_COLOUR, TEXT_MARGIN,  WIDTH
from .objects import Bullet,LifesCounting, Plane, Rock


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

        self.message = "'Space' to start playing"
        self.information_text = "Push 'I' to read  game´s history and how to play"
        self.message_pos = 0.75 * HEIGHT
        self.information_pos = self.message_pos + MAIN_TEXT_SIZE + TEXT_MARGIN

    def play(self):
        exit = False

        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    exit = True
                if event.type == pg.KEYDOWN and event.key == pg.K_a:
                    exit = True
                if event.type == pg.KEYDOWN and event.key == pg.K_b:
                    exit = True

                    # go to information scene
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

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
        pos_x = (WIDTH - width_text) / 2

        self.screen.blit(text, (pos_x, sum_pos_y))

    def change_Home_Information(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            return True
    def change_Home_Game(self):
        key = pg.key.get_pressed()
        if key[pg.K_b]:            
            return True

    def change_Information_Home(self):
        return False
    def change_Information_Game(self):
        return False
    
    def change_Game_Home(self):
        return False


class Information(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)

        self.message = "'Space' to go back"
        self.information_text_1 = " Viaja de planeta en planeta"
        self.information_text_2 = "- EL objetivo es no ser golpeado por las rocas espaciales"
        self.information_text_3 = "- Al subir de nivel aumentará la dificultad"
        self.information_text_4 = "- Tendrás 3 vidas"

        self.message_pos = 0.3 * HEIGHT
        # to separate diferent lines, actually it should be in __init__
        self.separator = MAIN_TEXT_SIZE + TEXT_MARGIN
        self.information_pos = self.message_pos + self.separator

    def play(self):

        exit = False

        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_c:

                    exit = True
                if event.type == pg.KEYDOWN and event.key == pg.K_d:
                    exit = True

                    

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(BACKGROUND_COLOUR)

            self.draw_text(self.message, self.message_pos)
            self.draw_text(self.information_text_1,
                           self.information_pos + self.separator)
            self.draw_text(self.information_text_2,
                           self.information_pos + self.separator*2)
            self.draw_text(self.information_text_3,
                           self.information_pos + self.separator*3)
            self.draw_text(self.information_text_4,
                           self.information_pos + self.separator*4)

            pg.display.flip()

    

    def write_text(self):
        # creating

        self.information_text_1 = " Viaja de planeta en planeta"
        self.information_text_2 = "- EL objetivo es no ser golpeado por las rocas espaciales"
        self.information_text_3 = "- Al subir de nivel aumentará la dificultad"
        self.information_text_4 = "- Tendrás 3 vidas"

        self.text_list = [self.information_text_1, self.information_text_2,
                          self.information_text_3, self.information_text_4]
        self.line_amount = len(self.text_list)

    def draw_text(self, text_input, sum_pos_y):

        text = self.tipography.render(text_input, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (WIDTH - width_text) / 2

        self.screen.blit(text, (pos_x, sum_pos_y))

    def change_Information_Home(self):
        key = pg.key.get_pressed()
        if key[pg.K_c]:
            return True
    def change_Information_Game(self):
        key = pg.key.get_pressed()
        if key[pg.K_d]:            
            return True
    def change_Home_Information(self):
        return False
    def change_Home_Game(self):
        return False
    def change_Game_Home(self):
        return False

class Game(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        bg_file = os.path.join("resources", "images", "background.png")
        self.background = pg.image.load(bg_file)
        self.player = Plane()
        self.rocks_groups = self.rock_group()
        self.lifes_counter = LifesCounting(LIFES)
        #self.no_life = LifesCounting.no_lifes()
        self.bullets_groups = self.bullet_group()

        self.clock = pg.time.Clock()

    def play(self):
        self.shot_exist = False
        exit = False
        contador = 0
        while not exit:
            
            contador += 1
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    #print("si")
                    self.shot = self.create_bullet()
                    self.shot_exist = True
                    
                    

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            

            #ROCK CREATER CONTROLLER
            if contador == 1:  # create first rocks to don´t have problems with create method

                self.created_rock = self.create_rocks()
            if contador % 5 == 0:  # to control difficulty: allows to cntrolling creating rocks every X time

                self.created_rock = self.create_rocks()

            ### UPDATE OBJECTS SETUP ###

            self.player.update()
            
            if self.shot_exist:
                              
                self.bullet_object.update()
                self.bullets.update()

            self.rock_object.update()
            self.rocks.update()
            plane_crash =  pg.sprite.spritecollide(self.player, self.rocks, True)

            

            """implementar para que salga de game cuando vidas  se queden en 0"""
            if plane_crash:
                self.remove_life = self.lifes_counter.lost_life()            
                if self.remove_life == 0:
                    
                    self.without_lifes = self.lifes_counter.no_lifes()
                    
            

            self.screen.fill(BACKGROUND_COLOUR)
            ###  PAINT BACKGROUND METHOD    ###
            self.paint_background()
            self.screen.blit(
                self.player.image, self.player.rect)  # PLayer

            # draw in the game rocks
            self.rocks.draw(self.screen)
            #draw bullet
            if self.shot_exist:
                self.bullets.draw(self.screen)

            #draw lifes counting
            self.lifes_counter.paint_lifes(self.screen)

            pg.display.flip()
            self.clock.tick(FPS)

    # background method
    def paint_background(self):
        self.screen.blit(self.background, (0, 0))

    def bullet_group(self):
        self.bullets = pg.sprite.Group()
        self.bullets.empty()
    def create_bullet(self):
        pos_x = (self.player.rect.x) + 50
        pos_y = self.player.rect.y + 15

    
        self.bullet_object = Bullet(pos_x, pos_y)
        self.bullets.add(self.bullet_object)

    ### Create Rock group ###

    def rock_group(self):

        self.rocks = pg.sprite.Group()
        self.rocks.empty()

    def create_rocks(self):
        """
        pos_x = WIDTH
        repeated = randint(0, MAXIMUM_REPEATED_ROCKS)
        for i in range(repeated):
            pos_y = randint(0, HEIGHT)
            self.rock_object = Rock(pos_x,pos_y)
            self.rocks.add(self.rock_object)

        """
        pos_x = WIDTH
        pos_y = randint(0, HEIGHT)
        self.rock_object = Rock(pos_x, pos_y)
        self.rocks.add(self.rock_object)
    
    def change_Home_Information(self):
        return False
    def change_Home_Game(self):
        return False

    def change_Information_Home(self):
        return False
    def change_Information_Game(self):
        return False
    
    def change_Game_Home(self):
        key = pg.key.get_pressed()
        if key[pg.K_e]:            
            return True
