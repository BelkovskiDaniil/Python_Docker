import sqlite3
import os
import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(host="db", database="postgres", user="postgres", password="root")

    def check_and_create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies
            (direction text, href text, vacancy text, location text)
        ''')
        self.conn.commit()
        # self.conn.close()

    def clear_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM vacancies
        ''')
        self.conn.commit()
        # self.conn.close()

    def add_entry(self, direction, href, vacancy, location):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vacancies VALUES (%s, %s, %s, %s)
        ''', (direction, href, vacancy, location))
        self.conn.commit()
        # self.conn.close()

    def print_table(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vacancies')
        rows = cursor.fetchall()
        grouped_rows = {}
        for row in rows:
            direction, href, vacancy, location = row
            if direction not in grouped_rows:
                grouped_rows[direction] = []
            grouped_rows[direction].append((href, vacancy, location))
        for direction, vacancies in grouped_rows.items():
            print(direction + ':')
            for href, vacancy, location in vacancies:
                print("    " + href + ", " + vacancy + ", " + location)
        # self.conn.close()

    def return_directions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vacancies')
        rows = cursor.fetchall()
        set_directions = set()
        for row in rows:
            direction, href, vacancy, location = row
            set_directions.add(direction)
        # self.conn.close()
        return set_directions

    def return_cities(self, direction_selected):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vacancies')
        rows = cursor.fetchall()
        set_cities = set()
        for row in rows:
            direction, href, vacancy, location = row
            if direction == direction_selected:
                for elem in location.split(', '):
                    set_cities.add(elem)
        # self.conn.close()
        return set_cities

    def return_vacancies(self, direction_selected, city_selected):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vacancies')
        rows = cursor.fetchall()
        array_vacancies = []
        were = set()
        for row in rows:
            direction, href, vacancy, location = row
            if direction == direction_selected:
                for elem in location.split(', '):
                    if elem == city_selected and vacancy not in were:
                        array_vacancies.append([vacancy, href])
                        were.add(vacancy)
        # self.conn.close()
        return array_vacancies
