import os
from random import randint

import pygame as pg
from pygame.sprite import Sprite

from thequest import HEIGHT, WIDTH

class Plane(Sprite):

    x_margin = 20
    speed = 10

    def __init__(self):
        super().__init__()

        self.image = pg.image.load(
                    os.path.join("resources", "images", "plane.png"))

        self.rect = self.image.get_rect(midleft=(self.x_margin, HEIGHT/2))

    def update(self):
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
            if self.rect.bottom  > HEIGHT:
                self.rect.bottom = HEIGHT



class Rock(Sprite):
    def __init__(self, position_y): # , points
        super().__init__()

        self.image = self.choose_size()
        
        #width = self.image.get_width()
        #height = self.image.get_height()
        #self.points = points
        
        self.pos_y = position_y
        
        
        

        
        self.choose_speed()

    def choose_size(self):
        self.rock_list = []
        for i in range(3):
            self.rock_list.append(
                pg.image.load(
                    os.path.join("resources", "images", f"rock_yellow{i}.png")
                )
            )
        
        number = randint(0,2)

        self.rock_size = self.rock_list[number]
        return self.rock_size

    def choose_speed(self):
        self.list_speed = [5,10,20]
        number = randint(0,2)
        self.rock_speed = self.list_speed[number]
        return self.rock_speed

    def update(self):
        self.pos_x = WIDTH
        self.rect = self.image.get_rect(x= self.pos_x, y= self.pos_y)
        
        rock_speed = self.choose_speed()
        self.rect.x -=  rock_speed
        if self.rect.x < 0:
            self.rect.x = 0 - self.rect -10
        
        
        


   
