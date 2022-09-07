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
        self.tipography = pg.font.Font(font_file, 15)
        self.text = ""  # to write record name

    def get_DB(self):
        query = 'SELECT * FROM HallofFamescore ORDER BY score_records DESC LIMIT 5'
        connection = sqlite3.connect(self.link)
        path = connection.cursor()
        path.execute(query)

        column_name = []

        for column in path.description:
            column_name.append(column[0])
        print(column_name)
        info = path.fetchall()
        self.moves = []
        print(info)

        for dato in info:
            move = {}
            i = 0
            for name in column_name:
                move[name] = dato[i]
                i += 1
            self.moves.append(move)

        connection.close()
        print(self.moves)
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

    """
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

        return name
        """

    def ask_name(self,screen):
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
            # self.pintar()
            pg.display.flip()
        return self.text
    
    def pintar(self): #no lo uso, es de toni
        pg.draw.rect(self.screen, self.color_fondo, self.fondo)
        self.pantalla.blit(self.titulo, (self.x_titulo, self.y_titulo))

        superficie_texto = self.tipografia.render(
            self.texto, True, self.color_texto, self.color_fondo)
        pos_x = self.x_titulo
        pos_y = self.y_titulo + self.titulo.get_height()
        self.pantalla.blit(superficie_texto, (pos_x, pos_y))
    

    def insert_data_DB(self, link, name, points):
        print(name, points)
        query = 'INSERT INTO HallofFamescore (player_records, score_records) VALUES (?,?)'
        connection = sqlite3.connect(link)
        path = connection.cursor()
        path.execute(query, (name, points))
        connection.commit()
        connection.close()

    def draw_thebest(self, screen, message, pos_y, dictionary):
        """if there is not problem with the message, because of double information
        we don´t need this method
        """
        # def draw_text(self,message, pos_y):
        #message = "GAME OVER"
        #pos_y = 100
        message_str = str(message)
        if message_str == "":
            message_str = self.no_name_record(message_str)
        self.screen = screen
        text = self.tipography.render(message_str, True, MESSAGE_COLOUR)
        width_text = text.get_width()
        if dictionary == "key":
            pos_x = (WIDTH/2) - width_text -10
        elif dictionary == "values":
            pos_x = (WIDTH/2) + 10

        self.screen.blit(text, (pos_x, pos_y))

    def no_name_record(self, name):
        name_anonimo = "Anonimo"
        if name == "":
            return name_anonimo
            

