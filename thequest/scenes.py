

import os
import sys
from random import randint

import pygame as pg

from . import BACKGROUND_COLOUR, FPS, HEIGHT, LIFES, MAIN_TEXT_SIZE, MAXIMUM_REPEATED_ROCKS_LEVEL,  MESSAGE_COLOUR, TEXT_MARGIN,  WIDTH
from .objects import Rock, Bullet, Game_ended, Game_Over, Window, Level_1, Level_2, Level_3, LifesCounting, Plane, Points, Rock_large, Rock_medium, Rock_small
from .records2 import DBManager
from .inputbox import InputBox
BBDD = 'data/DBscore.db'


class Scenes:
    def __init__(self, screen: pg.Surface):
        self.screen = screen


class Home(Scenes):
    # first scene, home
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        self.logo = pg.image.load(
            os.path.join("resources", "images", "icon.png"))

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, MAIN_TEXT_SIZE)

        self.message = "'B' to start playing"
        self.information_text = "Push 'I' to read  game´s history and how to play"
        self.message_pos = 0.75 * HEIGHT
        self.information_pos = self.message_pos + MAIN_TEXT_SIZE + TEXT_MARGIN

    def play(self):
        exit = False

        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    exit = True
                if event.type == pg.KEYDOWN and event.key == pg.K_i:
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
        if key[pg.K_i]:
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

    def change_HallofFame_Home(self):
        return False

    def game_over(self):
        return False

    def game_finished(self):
        return False


class Information(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)
        ### Game messages or instructions ###
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

    def change_HallofFame_Home(self):
        return False

    def game_over(self):
        return False

    def game_finished(self):
        return False


class Game(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        bg_file = os.path.join("resources", "images", "background2.png")
        self.background = pg.image.load(bg_file)
        self.x_margin = 20
        self.player = Plane(midleft=(self.x_margin, HEIGHT/2))

        self.rocks_groups = self.rock_group()  # create method attribute

        self.activate_level_control = False
        self.lifes_counter = LifesCounting(
            LIFES, self.activate_level_control)  # create class attribute
        #self.levels = Levels(self.player)
        # se crean los planetas, pero están escondidos a la derecha del plano
        self.level1_planet = Level_1(self.player)  # create class attribute
        self.level2_planet = Level_2(self.player)  # create class attribute
        self.level3_planet = Level_3(self.player)  # create class attribute
        # self.no_life = LifesCounting.no_lifes()
        self.bullets_groups = self.bullet_group()  # create method attribute
        self.game_end = Game_Over(self.screen)  # create class attribute

        self.pointer = Points()  # create class attribute

        self.clock = pg.time.Clock()  # time attribute, but not the timing
        self.level_window = Window(self.screen)  # create class attribute
        # game finished pop up, with congrats and to go to HoF
        self.game_completed = Game_ended(self.screen)

        bullet_effect = os.path.join("resources", "sounds", "shot.wav")
        self.bullet_sound = pg.mixer.Sound(bullet_effect)
        hit_effect = os.path.join("resources", "sounds", "Game_hit.wav")
        self.explosion_sound = pg.mixer.Sound(hit_effect)
        background_music = os.path.join("resources", "sounds", "music.mp3")
        self.music = pg.mixer.music.load(background_music)
        pg.mixer.music.play(-1)
        # boolean to activate the option of creating exactly rocks
        self.create_leve_rock = True
        self.remove_life = 3  # three lifes

        self.database = DBManager(BBDD)

    def play(self):
        self.exit = False  # loop breaker variable
        contador = 0  # instead of using timing, counting to know when to create small rocks

        #counting_bullet_time = 0
        self.bullet_timer0 = 0  # instead of using timing, counting to know when to create bullets
        self.shot_exist = False  # boolean to know if shot is created
        self.shot_exist_2 = True  # boolean to know if shot is created 2

        # boolean to determinate if controls are locked
        self.activate_level_control = False
        self.time_start = pg.time.get_ticks()  # game start time
        # variable to know how timing the game is controlled by game
        self.pause_time_controller = 0
        # variable, this number is to don´t disturb level timing later are redefined
        self.pausa_time = 60000
        # variable, this number is to don´t disturb level timing later are redefined
        self.pausa_time2 = 120000
        # variable, this number is to don´t disturb level timing later are redefined
        self.limit_time = 60000
        # variable to know how time gap between real time and level bottom cliced(it shouldn´t exist)
        self.gap_time = 0
        self.level1 = True  # boolean to activate some level aspects
        self.level2 = False  # boolean to activate some level aspects
        self.level3 = False  # boolean to activate some level aspects
        self.level1_active = False  # boolean to activate some level aspects
        self.level2_active = False  # boolean to activate some level aspects
        self.level3_active = False  # boolean to activate some level aspects
        self.a = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        self.b = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        # as plane is hidden behing planet to stop collision pointer counting(just once)
        self.c = 0  # variable, because planet and plane hit is continusly hits, so it controls how many times gives points
        # to activate event in game over pop up and go back to Home
        self.game_over_active = False
        self.game_ended = False  # pop up antes del hall of fame, mensaje de juego terminado
        self.level1_done = False
        self.level2_done = False
        self.level3_done = False
        name_request = 0  # para que pida una sola vez el no

        while not self.exit:

            self.time_loop = pg.time.get_ticks()  # each loop timing
            self.timer = self.get_level_time_controller(
                self.time_start, self.time_loop)
            # control all level aspects, levels, windows etc.
            """self.timer está en desarrollo"""
            contador += 1  # increase each loop allows to controll when  creat rock

            for event in pg.event.get():
                if self.game_over_active == True and event.type == pg.KEYDOWN and event.key == pg.K_x:
                    self.exit = True
                if self.game_ended == True and event.type == pg.KEYDOWN and event.key == pg.K_w:
                    print("pulsando W")
                    self.exit = True

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:

                    # if counting_bullet_time == 0 or counting_bullet_time % 10 == 0:
                    bullet_time = self.time_loop - self.bullet_timer0
                    if self.bullet_timer0 == 0 or bullet_time >= 1000:
                        """if shot control are active  it is possible to shot every X seconds"""
                        if self.activate_level_control == False and self.shot_exist_2 == True:

                            self.shot = self.create_bullet()
                            #self.shot = self.create_bullet()
                            #self.shot = self.create_bullet()
                            self.bullet_sound.play()
                            self.shot_exist == True

                    #counting_bullet_time += 1
                        # to control as before mentioned when to be able to shot
                        self.bullet_timer0 = pg.time.get_ticks()

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            ###  PAINT BACKGROUND METHOD    ###
            self.paint_background()

            ### ROCK CREATER CONTROLLER ###
            # create first rocks to don´t have problems with create method
            if self.create_leve_rock == True and contador == 1 or contador % 20 == 0:
                self.created_rock = self.create_rocks()

            ### UPDATE OBJECTS SETUP ###

            self.player.update(self.activate_level_control, self.screen)

            if self.shot_exist:

                self.bullet_object.update()
            self.bullets.update()

            self.rock_object.update()
            self.rocks.update()
            for rocas in self.rocks:
                if rocas.rect.x < 0:
                    self.rocks.remove(rocas)

            ###  UPDATE PLANET MOVEMENT IF  EACH LEVEL BOOLEAN IS ACTIVATED  ###
            if self.level1_active:
                self.level1_planet.update_planet1(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            if self.level2_active:
                self.level2_planet.update_planet2(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            if self.level3_active:
                self.level3_planet.update_planet3(
                    self.activate_level_control, self.player)
                self.planet_group.update()
            ### KNOW IF COLLISION ARE EXISTING  ###
            plane_crash_small = pg.sprite.spritecollide(
                self.player, self.rocks, True)  # plane-rock crask
            rock_bullet_crash = pg.sprite.groupcollide(
                self.rocks, self.bullets, False, True, pg.sprite.collide_mask)  # plane-rock crask

            ### POINTER ###

            if rock_bullet_crash:
                for rock in rock_bullet_crash:
                    for bullet in rock_bullet_crash[rock]:
                        rock_life = rock.rock_lost_life()  # IF CRASK ROCK LOST LIFE
                        self.explosion_sound.play()  # explosion sound done
                        if rock_life == 0:  # if lifes 0 gives point and remove the rock

                            self.pointer.increase_points(rock.get_points())
                            self.rocks.remove(rock)

            """implementar para que salga de game cuando vidas  se queden en 0"""
            ### PLANE CRASH CONTROLLER ###
            if plane_crash_small and self.activate_level_control == False:
                # plane lost a life if crashed small rock
                self.remove_life = self.lifes_counter.lost_life()

            # self.screen.fill(BACKGROUND_COLOUR)

            self.planet_group.draw(self.screen)
            ### POP UP A WINDOW TO SHOW A MESSAGE IF YOU PASSED/WIN THE  LEVEL  ###
            if self.plane_in_planet1:  # level window
                self.screen.blit(self.level_window.image,
                                 self.level_window.rect)
                self.message_completed = "NIVEL COMPLETADO"
                self.level_window.draw_text(self.message_completed)
                self.level_window.draw_points(self.pointer.value)
                self.level_window.click_continue()  # pop up of bottom

            """self.screen.blit(self.player.image, self.player.rect)  # PLayer"""

            # draw in the game rocks

            self.rocks.draw(self.screen)

            # draw bullet

            self.bullets.draw(self.screen)

            # draw points counting
            self.pointer.draw_points(self.screen)

            # draw lifes counting
            self.lifes_counter.paint_lifes(self.screen)

            # level and planet draw

            if self.activate_level_control:
                self.planet_group.draw(self.screen)
                self.planet_group.update()
            ### GAME OVER POP UP ###
            if self.remove_life <= 0:
                print("no vidas")
                self.screen.blit(self.game_end.image, self.game_end.rect)
                self.game_over_message = "GAME OVER"
                self.game_end.draw_text(self.game_over_message, 300)
                self.restart = "Pulsa 'X' para ir a Inicio"
                self.game_end.draw_text(self.restart, HEIGHT - 100)
                self.game_over_active = True
                pg.mixer.music.pause()

            if self.game_ended == True:

                print("juego terminado")
                self.screen.blit(self.game_completed.image,
                                 self.game_completed.rect)
                self.congratulation_text = "¡FELICIDADES, JUEGO TERMINADO!"
                self.game_end.draw_text(self.congratulation_text, 100)
                self.HoF_message = "Pulsa 'W' para ir a Hall of Fame"
                self.game_end.draw_text(self.HoF_message, HEIGHT - 100)
                inputbox = InputBox(self.screen)

                if name_request == 0:
                    #name_player = self.database.ask_name()
                    inputbox = InputBox(self.screen)
                    name_player = inputbox.get_text()
                    name_request += 1
                    self.database.insert_data_DB(
                        BBDD, name_player, self.pointer.show_points())

                pg.mixer.music.pause()

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
        if self.create_leve_rock == True:
            pos_x = WIDTH
            repeated = randint(0, MAXIMUM_REPEATED_ROCKS_LEVEL)
            for i in range(repeated):
                pos_y = randint(0, HEIGHT)
                self.rock_object = Rock(pos_x, pos_y)
                self.rocks.add(self.rock_object)

    def remove_rock(self, rock):
        self.rocks.remove(rock)

    def get_level_time_controller(self, time0, time1):
        # to know each loop time, to know in which level should be
        self.real_time = (time1 - time0)

        self.planet_group = pg.sprite.GroupSingle()
        self.plane_in_planet1 = False
        self.plane_in_planet2 = False
        self.plane_in_planet3 = False
        # print(self.real_time)
        if self.real_time < 30000:  # level 1 timing and booleans
            #self.level1 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

        elif self.limit_time <= self.real_time < self.limit_time + 60000:
            # level 2 timing and booleans
            self.level2 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level2")

        elif self.pausa_time2 <= self.real_time < self.pausa_time2 + 120000:
            # level 3 timing and booleans
            self.level3 = True
            self.create_leve_rock = True
            self.activate_level_control = False
            self.shot_exist_2 = True

            print("level 3")
        else:

           # print("niveles")
            self.create_leve_rock = False

            # pause_time_controller = pg.time.get_ticks()
            if self.rock_object.rect.x <= - 20:  # when last rock created is out screen the controll starts

                self.activate_level_control = True
                self.shot_exist_2 = False
                if self.level1:
                    self.planet_group.add(self.level1_planet)
                    self.level1_active = True
                if self.level2:
                    self.planet_group.remove(self.level1_planet)
                    self.planet_group.add(self.level2_planet)
                    self.level2_active = True
                if self.level3:
                    self.planet_group.remove(self.level2_planet)
                    self.planet_group.add(self.level3_planet)
                    self.level3_active = True
                if self.level1_active:
                    #self.levels.update_planet1(self.activate_level_control, self.player)

                    self.plane_in_planet1 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)

                if self.level2_active:

                    #self.level2_planet.update_planet2(self.activate_level_control, self.player)
                    self.plane_in_planet2 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)
                if self.level3_active:
                    #self.level3_planet.update_planet3(self.activate_level_control, self.player)
                    self.plane_in_planet3 = pg.sprite.spritecollide(
                        self.player, self.planet_group, False)

                if self.plane_in_planet1:
                    # as plane and planet hit all the time(during this time) just increase once all the level points
                    if self.a == 0:
                        self.pointer.increase_points(100)
                        self.a += 1
                if self.plane_in_planet2:
                    if self.b == 0:  # as before
                        self.b += 1
                        self.pointer.increase_points(200)
                if self.plane_in_planet3:
                    if self.c == 0:  # as before
                        self.c += 1
                        self.pointer.increase_points(400)

                # self.level_window.draw_points(self.pointer.value)

                # self.level_window.click_continue()
                # self.level_window.draw_text()

                for event in pg.event.get():  # as main event checker are locked to dont creeate shots etc
                    # new event checr to exit and to know if mouse is clicking in continue bottom
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pressed_key = pg.mouse.get_pressed()
                        mouse_pos = pg.mouse.get_pos()
                        if pressed_key[0] and 80 <= mouse_pos[0] <= 447 and 165 <= mouse_pos[1] <= 261:
                            # mouse clicking area

                            # indicarlo en el init como pausa_time_controller= 0
                            self.pause_time_controller = pg.time.get_ticks()

                            if self.level1 == True:  # adapt timer for nexts levels, before game restart
                                self.pausa_time = (
                                    self.pause_time_controller - 30000)
                                self.gap_time = self.pause_time_controller - self.real_time
                                self.limit_time = self.pause_time_controller - self.gap_time
                                self.level1 = False
                                #self.rect = self.image.get_rect(midleft=(self.x_margin, HEIGHT/2))
                                self.level1_done = True
                                print("aqui 1")
                                print(self.pause_time_controller)
                                print(self.real_time)
                                print(self.gap_time)
                                print(self.pausa_time)
                                print(self.limit_time)

                            elif self.level2 == True:  # adapt timer for next level, before game restart
                                print("aqui 2")
                                self.gap_time = self.pause_time_controller - self.real_time
                                self.pausa_time2 = self.pause_time_controller - self.gap_time

                                #self.limit_time = self.pause_time_controller - self.pausa_time2
                                self.level2 = False
                                self.level2_done = True

                                self.player.rect.midleft
                                print(self.real_time)
                                print(self.gap_time)
                                print(self.pause_time_controller)
                                print(self.pausa_time2)
                                print(self.limit_time)
                            elif self.level3 == True:  # adapt timer for the last level, before game restart
                                print("aqui 3")
                                self.pausa_time2 = (
                                    self.pause_time_controller - self.limit_time + 60000)
                                self.limit_time = 60000 + 30000
                                self.level3 = False
                                self.level3_done = True
                                self.player.rect.midleft
                                print(self.pausa_time2)
                                print(self.limit_time)
                            if self.level1_done == True and self.level2_done == True and self.level3_done == True:
                                # to know that game has ended and Hall Of Fame scene should start
                                self.game_ended = True
                                print("termino")

    def change_Home_Information(self):
        return False

    def change_Home_Game(self):
        return False

    def change_Information_Home(self):
        return False

    def change_Information_Game(self):
        return False

    def change_Game_Home(self):  # read message!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """!!!!!!!!!!currently not working to decide if it should work or not"""
        key = pg.key.get_pressed()
        if key[pg.K_e]:
            return True

    def change_HallofFame_Home(self):
        return False

    def game_over(self):
        key = pg.key.get_pressed()
        if key[pg.K_x]:
            return True

    def game_finished(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            return True


class HallofFame(Scenes):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, MAIN_TEXT_SIZE)

        self.message = "HALL OF FAME"
        self.sub_message = "LAS MEJORES PUNTUACIONES"
        self.message_pos = 0.1 * HEIGHT
        self.sub_message_pos = self.message_pos + MAIN_TEXT_SIZE + TEXT_MARGIN
        self.database = DBManager(BBDD)
        self.db_list = self.database.get_DB()

    def play(self):
        exit = False
        i = 0
        while not exit:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_q:
                    exit = True

                    # go to information scene
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(BACKGROUND_COLOUR)
            self.draw_text(self.message, self.message_pos)
            self.draw_text(self.sub_message, self.sub_message_pos)

            text_pos_y = 0.3 * HEIGHT
            for list_item in self.db_list:
                self.database.draw_thebest(
                    self.screen, list_item["player_records"], text_pos_y, "key")
                self.database.draw_thebest(
                    self.screen, list_item["score_records"], text_pos_y, "values")
                text_pos_y += 50
            """
                i += 1
                
                if i == 5:
                    break
            
            for key, value in self.db_list.items():
                
                record_message = f"nombre={key}:puntos={value}"
                self.database.draw_thebest(self.screen, f"nombre={key}:puntos={value}", text_pos_y)
                """

            #self.congratulation_text = "¡FELICIDADES, JUEGO TERMINADO!"
            #self.game_end.draw_text(self.congratulation_text, 300)

            pg.display.flip()

    def draw_text(self, text_input, sum_pos_y):

        text = self.tipography.render(text_input, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (WIDTH - width_text) / 2

        self.screen.blit(text, (pos_x, sum_pos_y))

    def change_Home_Information(self):
        return False

    def change_Home_Game(self):
        return False

    def change_Information_Home(self):
        return False

    def change_Information_Game(self):
        return False

    def change_Game_Home(self):
        return False

    def change_HallofFame_Home(self):
        key = pg.key.get_pressed()
        if key[pg.K_q]:
            return True

    def game_over(self):
        return False

    def game_finished(self):
        return False
