import sqlite3
from unittest import result


class DBManager:
    def __init__(self, link):
        self.link = link

    def get_DB(self):
        query = 'SELECT * FROM scoreboard ORDER BY score DESC'
        connection = sqlite3.connect(self.link)
        path = connection.cursor()
        path.execute(query)

        self.scores = []
        column_name = []

        for column in path.description:
            column_name.append(column[0])

        info = path.fetchall()
        for dato in info:
            moves = {}
            i = 0
            for name in column_name:
                moves[name] = dato[i]
                i += 1
            self.scores.append(moves)

        connection.close()

        return self.scores

    def select_best_players(self):
        query = 'SELECT * FROM HallofFamescore ORDER BY score DESC'
        connection = sqlite3.connect(DBM_PATH)
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            print(row)
        connection.close()
        return result

    def select_min_score(self):
        query = 'select min(score) from (select score from HallofFamescore ORDER BY score DESC LIMIT 5)'
        connection = sqlite3.connect(DBM_PATH)
        cur = connection.cursor()
        cur.execute(query)
        score = cur.fetchall()[0][0]
        if score == None:
            score = 0
        connection.close()
        return score

    def save_or_update_info(self, name, score, level):
        insert_update = ''
        name = name.upper()
        if self.exist_player(name):
            insert_update = f'UPDATE HallofFamescore SET score={score}, last_level={level} WHERE player=\'{name}\''
        else:
            insert_update = f'INSERT INTO HallofFamescore VALUES(\'{name}\',{score},{level})'
        connection = sqlite3.connect(DBM_PATH)
        cur = connection.cursor()
        cur.execute(insert_update)
        connection.commit()
        connection.close()
        self.clear_table()

    def clear_table(self):
        delete = 'DELETE FROM scoreboard where score not BETWEEN (select min(score)from (select score from scoreboard ORDER BY score DESC LIMIT 5)) and (select max(score)from (select score from scoreboard ORDER BY score DESC LIMIT 5))'
        connection = sqlite3.connect(DBM_PATH)
        cur = connection.cursor()
        cur.execute(delete)
        connection.commit()
        connection.close()

    def exist_player(self, name):
        connection = sqlite3.connect(DBM_PATH)
        cur = connection.cursor()
        query = f'SELECT COUNT(*) FROM scoreboard WHERE player=\'{name}\''
        cur.execute(query)
        count = cur.fetchall()[0][0]
        connection.close()
        return count > 0
