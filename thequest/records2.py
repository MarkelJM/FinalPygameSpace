import operator
import sqlite3
import os
import pygame as pg
from thequest import MESSAGE_COLOUR, WIDTH, HEIGHT
from unittest import result


class DBManager:
    def __init__(self, link):
        self.link = link
        font_file = os.path.join("resources", "fonts", "CabinSketch-Bold.ttf")
        self.tipography = pg.font.Font(font_file, 45)

    def get_DB(self):
        query = 'SELECT * FROM HallofFamescore ORDER BY score DESC'
        connection = sqlite3.connect(self.link)
        path = connection.cursor()
        path.execute(query)

        #self.scores = []
        column_name = []

        for column in path.description:
            column_name.append(column[0])

        info = path.fetchall()
        for dato in info:
            self.moves = {}
            i = 0
            for name in column_name:
                self.moves[name] = dato[i]
                i += 1
            # self.scores.append(moves)

        connection.close()

        return self.moves

    def update_DB(self, points):
        self.points = points

        for k, v in self.moves.items():
            if str(self.points) > str(v):
                name = self.ask_name()
                if name != TypeError:
                    # ordena el diccionario segun los values
                    db_update = sorted(
                        self.moves(), key=operator.itemgetter(1))
                    eliminated = db_update.popitem()

    def ask_name(self):
        loop = True
        while loop:
            name = input(
                "¿Con qué nombre o caracter quieres grabar la puntuación?(máximo 8 y mínimo 3 caracteres): ")
            try:
                if len(name) >= 3 and len(name) <= 8:
                    loop = False
            except:
                print("Por favor, debe ser más de 3 caracteres y menos de 8 caracteres")

    def insert_data_DB(self, link, name, points):
        query = f'INSERT INTO HallofFamescore (player_records, score_records) VALUES (?,?)'
        connection = sqlite3.connect(link)
        path = connection.cursor()
        path.execute(query,(name, points) )
        connection.commit()
        connection.close()

    def draw_thebest(self, message, pos_y):
        """if there is not problem with the message, because of double information
        we don´t need this method
        """
        # def draw_text(self,message, pos_y):
        #message = "GAME OVER"
        #pos_y = 100

        text = self.tipography.render(message, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        pos_x = (WIDTH - width_text) / 2

        self.screen.blit(text, (pos_x, pos_y))



