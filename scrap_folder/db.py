import sqlite3
import os
import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(host="db", database="postgres", user="postgres", password="root")

    def check_and_create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_database
            (direction text, href text, vacancy text, location text, recomendations text)
        ''')
        self.conn.commit()
        # self.conn.close()

    def clear_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM new_database
        ''')
        self.conn.commit()
        # self.conn.close()

    def add_entry(self, direction, href, vacancy, location, recomendations):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO new_database VALUES (%s, %s, %s, %s, %s)
        ''', (direction, href, vacancy, location, recomendations))
        self.conn.commit()
        # self.conn.close()


    def return_directions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM new_database')
        rows = cursor.fetchall()
        set_directions = set()
        for row in rows:
            direction, href, vacancy, location, recomendations = row
            set_directions.add(direction)
        # self.conn.close()
        return set_directions

    # def return_cities(self, direction_selected):
    #     cursor = self.conn.cursor()
    #     cursor.execute('SELECT * FROM new_database')
    #     rows = cursor.fetchall()
    #     set_cities = set()
    #     for row in rows:
    #         direction, href, vacancy, location, recomendations = row
    #         if direction == direction_selected:
    #             for elem in location.split(', '):
    #                 set_cities.add(elem)
    #     # self.conn.close()
    #     return set_cities

    def return_cities(self, direction_selected):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM new_database WHERE direction = %s", (direction_selected,))
        rows = cursor.fetchall()
        set_cities = set()
        for row in rows:
            direction, href, vacancy, location, recomendations = row
            for elem in location.split(', '):
                set_cities.add(elem)
        # self.conn.close()
        return set_cities


    
    # def return_recomendations(self, direction_selected, city_selected):
    #     cursor = self.conn.cursor()
    #     cursor.execute('SELECT * FROM new_database')
    #     rows = cursor.fetchall()
    #     array_vacancies = []
    #     were_recom = set()
    #     for row in rows:
    #         direction, href, vacancy, location, recomendations = row
    #         if direction == direction_selected:
    #             for elem in location.split(', '):
    #                 if elem == city_selected and vacancy not in were_recom:
    #                     for element in recomendations.split('@'):
    #                         if element not in were_recom:
    #                             array_vacancies.append(element.title())
    #                             were_recom.add(element)
    #     # self.conn.close()
    #     return array_vacancies

    def return_recomendations(self, direction_selected, city_selected):
        cursor = self.conn.cursor()
        query = """
        SELECT * FROM new_database 
        WHERE direction = %s AND location LIKE %s
        """
        cursor.execute(query, (direction_selected, '%' + city_selected + '%',))
        rows = cursor.fetchall()
        array_vacancies = []
        were_recom = set()
        for row in rows:
            direction, href, vacancy, location, recomendations = row
            for elem in location.split(', '):
                if elem == city_selected and vacancy not in were_recom:
                    for element in recomendations.split('@'):
                        if element not in were_recom:
                            array_vacancies.append(element.title())
                            were_recom.add(element)
        # self.conn.close()
        return array_vacancies




    # def return_vacancies(self, direction_selected, city_selected):
    #     cursor = self.conn.cursor()
    #     cursor.execute('SELECT * FROM new_database')
    #     rows = cursor.fetchall()
    #     array_vacancies = []
    #     were = set()
    #     for row in rows:
    #         direction, href, vacancy, location, recomendations = row
    #         if direction == direction_selected:
    #             for elem in location.split(', '):
    #                 if elem == city_selected and vacancy not in were:
    #                     array_vacancies.append([vacancy, href, recomendations])
    #                     were.add(vacancy)
    #     # self.conn.close()
    #     return array_vacancies

    def return_vacancies(self, direction_selected, city_selected):
        cursor = self.conn.cursor()
        query = """
        SELECT * FROM new_database 
        WHERE direction = %s AND location LIKE %s
        """
        cursor.execute(query, (direction_selected, '%' + city_selected + '%',))
        rows = cursor.fetchall()
        array_vacancies = []
        were = set()
        for row in rows:
            direction, href, vacancy, location, recomendations = row
            for elem in location.split(', '):
                if elem == city_selected and vacancy not in were:
                    array_vacancies.append([vacancy, href, recomendations])
                    were.add(vacancy)
        # self.conn.close()
        return array_vacancies


