import os

import pygame as pg


from thequest import WIDTH, HEIGHT
from thequest.scenes import  Home, Information, Game


class MainGame:
    def __init__(self):
        pg.init()
        # create the display screen

        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        # create title name
        pg.display.set_caption("The Quest MJM")
        # create logo: 1. upload 2. set
        # NOTE:this is the code, but I have to create the logo an named it
        
        icon = pg.image.load(
            os.path.join("resources", "images", "icon.png"))
        pg.display.set_icon(icon)
        

        
            
                   
            

    def start(self):
        self.pantalla = Home(self.display)
        self.pantalla.play()
        
       

        
