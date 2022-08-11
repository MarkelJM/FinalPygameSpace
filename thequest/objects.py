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
    def __init__(self, first_lifes_count, status):
        self.status = status
        self.lifes = first_lifes_count
        font_file = os.path.join(
            "resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 20)

    def lost_life(self):

        self.lifes -= 1
        return self.lifes

    def no_lifes(self):
        if self.lifes == 0:
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


class Level_1(Sprite):
    def __init__(self, player):
        super().__init__()
        self.create_leve_rock = True
        self.speed_planet = 10
        self.activate_level_control = False
        self.player = player
        self.image = pg.image.load(os.path.join(
            "resources", "images", "planet0.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image.get_rect(x=self.pos_x,  y=self.pos_y )



    def update_planet1(self, status, player):
        self.player = player
        if status == True:
            
            if self.rect.x > WIDTH - self.image.get_width():
                self.rect.x -= self.speed_planet
        
            
            if self.rect.x <= WIDTH - self.image.get_width():
                self.rect.x = WIDTH - self.image.get_width()
                

            self.player.rect.x += self.speed_planet
            
            if self.player.rect.x >= WIDTH - self.image.get_width()  :
                self.player.rect.x = WIDTH - self.image.get_width()
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2


class Level_2(Sprite):
    def __init__(self, player):
        super().__init__()
        self.create_leve_rock = True
        self.speed_planet = 10
        self.activate_level_control = False
        self.player = player
        self.image = pg.image.load(os.path.join(
            "resources", "images", "planet2.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image.get_rect(
            x=self.pos_x,  y=self.pos_y)
    
    def update_planet2(self, status, player):
        self.player = player
        if status == True:
            
            if self.rect.x > WIDTH - self.image.get_width():
                self.rect.x -= self.speed_planet
        
            
            if self.rect.x <= WIDTH - self.image.get_width():
                self.rect.x = WIDTH - self.image.get_width()
                

            self.player.rect.x += self.speed_planet
            
            if self.player.rect.x >= WIDTH - self.image.get_width() :
                self.player.rect.x = WIDTH - self.image.get_width() 
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
    

class Level_3(Sprite):
    def __init__(self, player):
        super().__init__()
        self.create_leve_rock = True
        self.speed_planet = 10
        self.activate_level_control = False
        self.player = player
        self.image = pg.image.load(os.path.join(
            "resources", "images", "planet1.png"))
        self.pos_y = 0
        self.pos_x = WIDTH
        self.rect = self.image.get_rect(
            x=self.pos_x,  y=self.pos_y)

    

    

    def update_planet3(self, status, player):
        self.player = player
        if status == True:
            
            if self.rect.x > WIDTH - self.image.get_width():
                self.rect.x -= self.speed_planet
        
            
            if self.rect.x <= WIDTH - self.image.get_width():
                self.rect.x = WIDTH - self.image.get_width()
                

            self.player.rect.x += self.speed_planet
            
            if self.player.rect.x >= WIDTH - self.image.get_width() :
                self.player.rect.x = WIDTH - self.image.get_width()
            if self.player.rect.y <= HEIGHT/2:
                self.player.rect.y += self.speed_planet
                if self.player.rect.y >= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2
            if self.player.rect.y > HEIGHT/2:
                self.player.rect.y -= self.speed_planet
                if self.player.rect.y <= HEIGHT/2:
                    self.player.rect.y = HEIGHT/2


class Window(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.wn_x_margin = 10
        self.wn_y_margin = 30
        
        self.continue_height = 60
        self.image = pg.image.load(
            os.path.join("resources", "images", "window.png"))

        self.rect = self.image.get_rect(midleft=(self.wn_x_margin, self.wn_y_margin))

        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 30)

       
        
        #self.draw_text(message_completed, message_pos_level)

        #self.text_continue = "CONTINUAR"
        #self.text_continue_position = self.wn_height - self.continue_height - 10
        #self.draw_text(text_continue, text_continue_position)

        
        #self.draw_points(points)
        #self.click_continue()
        print("play")
        
    
    def click_continue(self):
        

        pos_x = 80
        pos_y = self.image.get_height() - 350
        image = pg.image.load(
            os.path.join("resources", "images", "continuar.png"))

        rect = image.get_rect()
        self.screen.blit(image, (pos_x, pos_y))
        

    def draw_text(self,message):
        
        pos_y = self.wn_y_margin + 30

        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (self.image.get_width() - width_text) / 2

        self.screen.blit(text, (pos_x, pos_y))

    def draw_points(self,  points):

        message = f"Puntos: {points}"
        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (self.image.get_width() - width_text) / 2
        pos_y = 100 
        self.screen.blit(text, (pos_x, pos_y))

    
        

