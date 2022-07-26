import operator
import sqlite3
import os
import pygame as pg
from thequest import MESSAGE_COLOUR, WIDTH
from unittest import result


class DBManager:
    def __init__(self, link):
        self.link = link
        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 15)
        self.text = ""  # to write record name

    def get_DB(self):
        """cretaes a list with dict inside"""
        query = 'SELECT * FROM HallofFamescore ORDER BY score_records DESC LIMIT 5'
        connection = sqlite3.connect(self.link)
        path = connection.cursor()
        path.execute(query)

        column_name = []

        for column in path.description:
            column_name.append(column[0])
        
        info = path.fetchall()
        self.moves = []
        

        for dato in info:
            move = {}
            i = 0
            for name in column_name:
                move[name] = dato[i]
                i += 1
            self.moves.append(move)

        connection.close()
        
        return self.moves
 

    def ask_name(self, screen):
        self.screen = screen
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(self.text) > 0:
                        self.text = self.text[:-1]
                    elif event.key == pg.K_RETURN:
                        salir = True
                    else:
                        self.text += event.unicode

            pg.display.flip()
        return self.text
     
        

    def insert_data_DB(self, link, name, points):
        print(name, points)
        query = 'INSERT INTO HallofFamescore (player_records, score_records) VALUES (?,?)'
        connection = sqlite3.connect(link)
        path = connection.cursor()
        path.execute(query, (name, points))
        connection.commit()
        connection.close()

    def draw_thebest(self, screen, message, pos_y, dictionary):

        message_str = str(message)
        if message_str == "":
            message_str = self.no_name_record(message_str)
        self.screen = screen
        text = self.tipography.render(message_str, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        if dictionary == "key":
            pos_x = (WIDTH/2) - width_text - 10
        elif dictionary == "values":
            pos_x = (WIDTH/2) + 10

        self.screen.blit(text, (pos_x, pos_y))

    def no_name_record(self, name):
        
        name_anonimo = "Anonimo"
        return name_anonimo
