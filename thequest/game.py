import os


import pygame as pg


from thequest import WIDTH, HEIGHT
from thequest.scenes import  HallofFame, Home, Information, Game
from thequest.objects import LifesCounting as LC


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
        
       
            
                   
            


        

    def play(self ):
       
        self.current_scene = Home(self.display)
        
        change = False
        
        while not change:
            self.current_scene.play()
            if self.current_scene.change_Home_Information() == True:
                self.current_scene = Information(self.display)
            elif self.current_scene.change_Home_Game() == True:
                self.current_scene = Game(self.display)
            elif self.current_scene.change_Information_Home() == True:
                self.current_scene = Home(self.display)
            elif self.current_scene.change_Information_Game() == True:
                self.current_scene = Game(self.display)
            elif self.current_scene.change_Game_Home() == True:
                self.current_scene = Home(self.display)
                
           
            elif self.current_scene.game_over() == True:
                self.current_scene = Home(self.display)

            elif self.current_scene.game_finished() == True:
                self.current_scene = HallofFame(self.display)
            
            elif self.current_scene.change_HallofFame_Home() == True:
                self.current_scene = Home(self.display)
   
    

        
        
       

        

