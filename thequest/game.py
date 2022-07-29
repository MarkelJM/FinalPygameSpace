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
        

        self.scenes = [
            Home(self.display),
            Information(self.display),
            Game(self.display)         
            ]
            
                   
            


        

    def play(self ):
        """
        desesperada...crear un metodo especifico para cada escenario posible 
        que devuelva true y no pida nada
        """       
        
        current_scene = Home(self.display)
        
        change = False
        
        while not change:
            current_scene.play()
            if current_scene.change_Home_Information() == True:
                current_scene = Information(self.display)
            elif current_scene.change_Home_Game() == True:
                current_scene = Game(self.display)
            elif current_scene.change_Information_Home() == True:
                current_scene = Home(self.display)
            elif current_scene.change_Information_Game() == True:
                current_scene = Game(self.display)
            elif current_scene.change_Game_Home() == True:
                current_scene = Home(self.display)
            
            
        

        



    def start(self):
        # in loop
        for scene in self.scenes:
            scene.play()

        
        
       

        

