

import os
import sys
from random import randint

import pygame as pg

from . import BACKGROUND_COLOUR, FPS, HEIGHT, LIFES, MAIN_TEXT_SIZE, MAXIMUM_REPEATED_ROCKS,  MESSAGE_COLOUR, TEXT_MARGIN,  WIDTH
from .objects import Bullet,Completed, Levels, LifesCounting, Plane, Points, Rock_small


class Scenes:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        # self.time = pg.time.Clock()


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

        self.rocks_groups = self.rock_group_small()
        self.activate_level_control = False
        self.lifes_counter = LifesCounting(LIFES,self.activate_level_control)
        self.levels = Levels(self.player)
        # se crean los planetas, pero están escondidos a la derecha del plano
        self.level1_planet = self.levels.start_level_1()
        self.level2_planet = self.levels.start_level_2()
        self.level3_planet = self.levels.start_level_3()
        # self.no_life = LifesCounting.no_lifes()
        self.bullets_groups = self.bullet_group()

        self.pointer = Points()

        self.clock = pg.time.Clock()

    def play(self):

        self.exit = False
        contador = 0
        #counting_bullet_time = 0
        self.bullet_timer0= 0
        self.shot_exist = False
        self.shot_exist_2 = True
        self.create_leve_rock = True
        self.activate_level_control = False
        self.time_start = pg.time.get_ticks()
        self.level_endtime = 30001
        self.pause_time_controller = 0
        self.pausa_time = 60000
        self.pausa_time2 = 60000
        self.limit_time = 60000
        self.level1 = True
        while not self.exit:

            self.time_loop = pg.time.get_ticks()
            self.timer = self.get_level_time_controller(self.time_start, self.time_loop)
            """self.timer está en desarrollo"""
            contador += 1

            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    
                    #if counting_bullet_time == 0 or counting_bullet_time % 10 == 0:
                    bullet_time = self.time_loop - self.bullet_timer0
                    if self.bullet_timer0 == 0 or bullet_time >= 2000:
                        
                        if self.activate_level_control == False and self.shot_exist_2 == True :
                            
                            self.shot = self.create_bullet()
                            self.shot = self.create_bullet()
                            self.shot = self.create_bullet()
                            self.shot_exist == True
                            
                    #counting_bullet_time += 1
                        self.bullet_timer0 = pg.time.get_ticks()
                    

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            # ROCK CREATER CONTROLLER
            # create first rocks to don´t have problems with create method
            if self.create_leve_rock == True and contador == 1 or contador % 30 == 0:
                self.created_rock_small = self.create_rocks_small()
                print(self.create_leve_rock)

            ### UPDATE OBJECTS SETUP ###

            self.player.update()

            if self.shot_exist:
                
                self.bullet_object.update()
            self.bullets.update()
            
            self.rock_object_small.update()
            self.rocks_small.update()

            plane_crash = pg.sprite.spritecollide(
                self.player, self.rocks_small, True)  # plane-rock crask
            rock_small_bullet_crash = pg.sprite.groupcollide(
                self.rocks_small, self.bullets, False, True, pg.sprite.collide_mask)  # plane-rock crask

            ### POINTER ###

            if rock_small_bullet_crash:
                for rock in rock_small_bullet_crash:
                    for bullet in rock_small_bullet_crash[rock]:
                        rock_life = self.rock_object_small.rock_lost_life()
                        if rock_life == 0:
                            self.pointer.increase_points(5)
                            self.rocks_small.remove(rock)

            """implementar para que salga de game cuando vidas  se queden en 0"""
            if plane_crash and self.activate_level_control == False:
                self.remove_life = self.lifes_counter.lost_life()
                if self.remove_life == 0:

                    self.without_lifes = self.lifes_counter.no_lifes()

            self.screen.fill(BACKGROUND_COLOUR)
            ###  PAINT BACKGROUND METHOD    ###
            self.paint_background()
            self.screen.blit(self.player.image, self.player.rect)  # PLayer

            # draw in the game rocks
            
            self.rocks_small.draw(self.screen)
            # draw bullet
            
            self.bullets.draw(self.screen)

            # draw points counting
            self.pointer.draw_points(self.screen)

            # draw lifes counting
            self.lifes_counter.paint_lifes(self.screen)

            # level and planet draw

            if self.activate_level_control:
                self.levels.draw(self.screen)

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

    def rock_group_small(self):

        self.rocks_small = pg.sprite.Group()
        self.rocks_small.empty()

    def create_rocks_small(self):
        """
        pos_x = WIDTH
        repeated = randint(0, MAXIMUM_REPEATED_ROCKS)
        for i in range(repeated):
            pos_y = randint(0, HEIGHT)
            self.rock_object = Rock(pos_x,pos_y)
            self.rocks.add(self.rock_object)

        """
        if self.create_leve_rock == True :
            pos_x = WIDTH
            pos_y = randint(0, HEIGHT)
            self.rock_object_small = Rock_small(pos_x, pos_y)
            print("si")
            self.rocks_small.add(self.rock_object_small)
            

    def remove_rock_small(self, rock):
        self.rocks_small.remove(rock)

    def get_level_time_controller(self, time0, time1):
        real_time = (time1 - time0)
        # limit_time----> indicar ambos en ele init como 6000 asi nos aseguramos que permanecera minimo un minuto con los planetas y puntos
        # pausa_time---->, pero si le damos play obtendremos un numero numero para ambos y podra saltal siguiente nivel
        # pausa_time2
        if real_time < 10000:
            self.level1 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level 1")

        elif 10000 + self.pausa_time < real_time < self.limit_time + 20000:
            self.level2 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True
            print("level2")
            # pass  # meter class nivel 2
        elif self.limit_time + 20000 + self.pausa_time2 < real_time < self.limit_time + 20000 + self.pausa_time2 + 30000:

            self.level3 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True
            print("level 3")
        else:
            print("niveles")
            self.create_leve_rock = False
            print(self.create_leve_rock)

            # pause_time_controller = pg.time.get_ticks()
            if self.rock_object_small.rect.x <= 0 -300:
                print("x menor 0")
                self.activate_level_control = True
                self.shot_exist_2 = False
                if self.level1:
                    self.levels.update_planet1()
                    plane_in_planet1 = pg.sprite.collide_rect(self.player, self.level1_planet)

                if self.level2:
                    self.levels.update_planet2()
                    plane_in_planet2 = pg.sprite.collide_rect(self.player, self.level2_planet)
                if self.level3:
                    self.levels.update_planet2()
                    plane_in_planet3 = pg.sprite.collide_rect(self.player, self.level3_planet)

                if plane_in_planet1 or plane_in_planet2 or plane_in_planet3:
                    if plane_in_planet1:
                        self.pointer.increase_points(100)
                    if plane_in_planet2:
                        self.pointer.increase_points(200)
                    if plane_in_planet3:
                        self.pointer.increase_points(400)


                    self.level_window = Completed()
                    for event in pg.event.get():
                        if event.type == pg.MOUSEBUTTONDOWN :
                            pressed_key = pg.mouse.get_pressed()
                            mouse_pos = pg.mouse.get_pos()
                            if pressed_key[0] and 120 <= mouse_pos[0] <= 200 and 230 <= mouse_pos[1] <= 290:                           

                                self.pause_time_controller =  pg.time.get_ticks() #indicarlo en el init como pausa_time_controller= 0
                                if self.level1 == True:            #necesitamos la informacion del level 1 para prepar el nivel 2
                                    pausa_time = (self.pause_time_controller - 10000)
                                    limit_time =10000 + pausa_time
                                    self.level1 = False
                                    self.level2 = True
                                if self.level2 ==True:
                                    pausa_time2 = (self.pause_time_controller - limit_time + 20000)
                                    limit_time =20000 + pausa_time2
                                    self.level2 = False
                                    self.level3 = True
                                if self.level3 == True:
                                    pausa_time2 = (self.pause_time_controller - limit_time + 20000)
                                    limit_time =20000 + pausa_time2
                                    self.level3 = False
                                    if level1 == False and level2 == False and level3 == False:
                                        self.exit = True
                                        print("termino")
        

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
