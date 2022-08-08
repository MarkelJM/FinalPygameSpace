import os
from random import randint
from turtle import width


import pygame as pg
from pygame.sprite import Sprite

from thequest import BULLET_MARGIN_OUT_SCREEN, BULLET_SPEED, HEIGHT, MAIN_POINTS, MESSAGE_COLOUR, ROCK_LIFE_LIST, ROCK_MARGIN_OUT_SCREEN, SPEED_LIST, WIDTH


class Plane(Sprite):

    x_margin = 20
    speed = 10

    def __init__(self):
        super().__init__()

        self.image = pg.image.load(
            os.path.join("resources", "images", "plane.png"))

        self.rect = self.image.get_rect(midleft=(self.x_margin, HEIGHT/2))

    def update(self, status):
        if status == False:
            button = pg.key.get_pressed()
            if button[pg.K_RIGHT]:
                self.rect.x += self.speed
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH
            if button[pg.K_LEFT]:
                self.rect.x -= self.speed
                if self.rect.left < 0:
                    self.rect.left = 0
            if button[pg.K_UP]:
                self.rect.y -= self.speed
                if self.rect.top < 0:
                    self.rect.top = 0
            if button[pg.K_DOWN]:
                self.rect.y += self.speed
                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT


class Rock_small(Sprite):
    def __init__(self, position_x, position_y):  # , points
        super().__init__()

        self.image = pg.image.load(os.path.join(
            "resources", "images", "rock_yellow0.png"))
        self.pos_y = position_y
        self.pos_x = position_x
        self.rect = self.image.get_rect(x=self.pos_x,  y=self.pos_y)

        self.rock_speed = self.choose_speed()
        self.rock_final_life = 2
        #rock_life = self.get_lifes()
        #self.rock_final_life = rock_life
        #self.rock_point = self.get_points()

    def rock_lost_life(self):
        self.rock_final_life = self.rock_final_life - 1
        return self.rock_final_life

    """
    def get_lifes(self):
        self.rock_life_list = ROCK_LIFE_LIST
        self.hits = self.rock_life_list[self.size_number]
        
        return self.hits
        """
    """ 
    def get_points(self):
        points_list = MAIN_POINTS
        size_table = points_list[self.size_number]
        points = size_table[self.speed_number]
        
        return points
        """
    """ 
    def choose_size(self):
        self.rock_list = []
        for i in range(3):
            self.rock_list.append(
                
            )
        
        self.size_number = randint(0,2)

        self.rock_size = self.rock_list[self.size_number]
        return self.rock_size
        """

    def choose_speed(self):
        self.list_speed = SPEED_LIST
        self.speed_number = randint(0, 2)
        self.rock_speed = self.list_speed[self.speed_number]

        return self.rock_speed

    def update(self):

        if self.rect.x > 0:
            self.rect.x -= self.rock_speed

        if self.rect.x < 0 or self.rect.x == 0:
            self.rect.x = 0 - ROCK_MARGIN_OUT_SCREEN


class LifesCounting():
    def __init__(self, first_lifes_count,status):
        self.status = status
        self.lifes = first_lifes_count
        font_file = os.path.join(
            "resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)

    def lost_life(self):
        
        self.lifes -= 1
        return self.lifes
    

    def no_lifes(self):
        return True

    def paint_lifes(self, screen):

        message = f"Vidas: {self.lifes}"
        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        pos_x = WIDTH-20-text.get_width()
        pos_y = HEIGHT-text.get_height()-10
        screen.blit(text, (pos_x, pos_y))


class Bullet(Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        self.pos_y = position_y
        self.pos_x = position_x

        self.image = pg.image.load(
            os.path.join("resources", "images", "bullet.png")
        )

        self.rect = self.image.get_rect(x=self.pos_x, y=self.pos_y)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

        self.bullet_speed = BULLET_SPEED

    def update(self):

        if self.rect.x < WIDTH:
            self.rect.x += self.bullet_speed

        if self.rect.x > WIDTH or self.rect.x == WIDTH:
            self.rect.x = WIDTH + BULLET_MARGIN_OUT_SCREEN


class Points():
    def __init__(self):
        self.value = 0
        font_file = os.path.join(
            "resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)

    def increase_points(self, points):
        self.value += points

    def draw_points(self, screen):

        message = f"Points: {self.value}"
        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        pos_x = 20
        pos_y = HEIGHT-text.get_height() - 10
        screen.blit(text, (pos_x, pos_y))


class Levels(Sprite):
    def __init__(self, player):
        super().__init__()
        self.create_leve_rock = True
        self.speed_planet = 10
        self.activate_level_control = False
        self.player = player

    def start_level_1(self):
        self.image1 = pg.image.load(os.path.join(
            "resources", "images", "planet0.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image1.get_rect(
            x=self.pos_x,  y=self.pos_y, right=WIDTH - self.image1.get_width())

    def start_level_2(self):
        self.image2 = pg.image.load(os.path.join(
            "resources", "images", "planet2.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image2.get_rect(
            x=self.pos_x,  y=self.pos_y, right=WIDTH - self.image2.get_width())

    def start_level_3(self):
        self.image3 = pg.image.load(os.path.join(
            "resources", "images", "planet1.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image3.get_rect(
            x=self.pos_x,  y=self.pos_y, right=WIDTH - self.image3.get_width())

    def update_planet1(self,status, player):
        self.player = player
        if status == True:
            if self.rect.x >= self.rect.right:
                self.rect.x -= self.speed_planet 
            print(self.speed_planet)
            print(self.rect.x)
            print(self.rect.right)
            if self.rect.x >= self.rect.right:
                self.rect.x = self.rect.right
                print(self.rect.x)
                
            self.player.rect.x += self.speed_planet
            if self.player.rect.x >= WIDTH - self.image1.get_width() + 20:
                self.player.rect.x = WIDTH - self.image1.get_width() + 20
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2

    def update_planet2(self,status, player):
        self.player = player
        if status == True:
            self.rect.x -= self.speed_planet  # Planet movement
            if self.rect.x <= self.rect.right:
                self.rect.x = self.rect.right
            self.player.rect.x += self.speed_planet
            if self.player.rect.x >= WIDTH - self.image2.get_width() + 20:
                self.player.rect.x = WIDTH - self.image2.get_width() + 20
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2

    def update_planet3(self,status, player):
        self.player = player
        if status == True:
            self.rect.x -= self.speed_planet  # Planet movement
            if self.rect.x <= self.rect.right:
                self.rect.x = self.rect.right
            self.player.rect.x += self.speed_planet
            if self.player.rect.x >= WIDTH - self.image3.get_width() + 20:
                self.player.rect.x = WIDTH - self.image3.get_width() + 20
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2


class Completed(Sprite):
    def __init__(self, screen, points):
        super().__init__()
        self.screen = screen
        self.wn_x = 10
        self.wn_y = 10
        self.wn_width = 300
        self.wn_height = 300
        pg.draw.rect(screen, (255, 255, 255), (self.wn_x,
                     self.wn_y, self.wn_width, self.wn_height))

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 30)

        message_completed = "NIVEL COMPLETADO"
        message_pos_level = self.wn_y + 30
        self.draw_text(message_completed, message_pos_level)

        text_continue = "CONTINUAR"
        text_continue_position = self.wn_height - self.continue_height -10
        self.draw_text(text_continue, text_continue_position)

        self.draw_text(message_completed)
        self.draw_points(points)
        self.click_continue()
        print("play")
    def click_continue(self):
        self.continue_width = 80
        self.continue_height = 60

        pos_x = (self.wn_width - self.continue_width)/2
        pos_y = self.wn_height - self.continue_height - 20 #20 de margen inferior
        pg.draw.rect(self.screen, (0, 0, 0,), (pos_x, pos_y,
                     self.continue_width, self.continue_height))

        

    def draw_text(self, message1, position):

        text = self.tipography.render(message1, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (self.wn_width - width_text) / 2

        self.screen.blit(text, (pos_x, position))

    def draw_points(self,  points):

        message = f"Puntos: {points}"
        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (self.wn_width - width_text) / 2
        pos_y = self.wn_height + 150
        self.screen.blit(text, (pos_x, pos_y))
