from sqlite3 import OperationalError
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import request
from flask import Flask
import psycopg2
import socket
import time
import sys
app = Flask(__name__)

import requests

def is_database_ready():
    try:
        conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="root"
        )
        conn.close()
        return True
    except OperationalError:
        return False

while not is_database_ready():
    time.sleep(0.1)

from db import Database;

db = Database()
print("DB ready")

def scrap_submissive(url: str):

    options = FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(url)

    requirements = []

    try:
        h3s = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'h3'))
        )

        for h3 in h3s:
            if h3.text == "Требования:":
                sibling = h3
                key = True
                while key:
                    siblings = sibling.find_elements(By.XPATH, './following-sibling::*')
                    for sib in siblings:
                        if sib.tag_name == 'h3':
                            key = False
                            break
                        elif sib.tag_name == 'ul':
                            lis = sib.find_elements(By.TAG_NAME, 'li')
                            for li in lis:
                                requirements.append((li.text).replace("\n", ""))
                        elif sib.tag_name == 'br':
                            next_s = sib.find_elements(By.XPATH, './following-sibling::*[1]')
                            for next_elem in next_s:
                                if next_elem:
                                    requirements.append(((next_elem.text).replace("• ", "")).replace("\n", ""))
        return requirements
    finally:
        driver.quit()

@app.route('/')
def pong_service():
    return 'Hello, I am scrap service!'

@app.route('/scrap')
def scrap():
    print("On scrap", file=sys.stderr)
    options = FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get('https://www.ptsecurity.com/ru-ru/about/vacancy/')

    array_vac = []

    try:
        vacancies = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing__item'))
        )
        for vacancy in vacancies:
            h2 = vacancy.find_element("class name", "vacancies__title").text
            array_small = [h2.replace('\n', '')]
            vacancies_list = vacancy.find_element("class name", 'vacancies-list')
            vacancies_list_items = vacancies_list.find_elements("class name", 'vacancies-list__item')
            for elem in vacancies_list_items:
                href_list_items = elem.find_elements("class name", 'link.vacancies-list__title')
                cities_list_items = elem.find_elements("class name", 'vacancies-list__cities')
                alpha = href_list_items[0].get_attribute('href')
                betta = href_list_items[0].get_attribute('innerText')
                gamma = cities_list_items[0].get_attribute('innerText')
                array_small.append(alpha.replace('\n', ''))
                array_small.append(betta.replace('\n', ''))
                array_small.append(gamma.replace('\n', ''))
                array_small.append('@'.join(scrap_submissive(alpha.replace('\n', ''))).replace(';', ''))
            array_vac.append(array_small)

    finally:
        driver.quit()

    print("Adding", file=sys.stderr)
    print("check and create")
    db.check_and_create_db()
    for elem in array_vac:
        global_name = elem[0]
        for i in range(1, len(elem), 4):
            db.add_entry(global_name, elem[i], elem[i + 1], elem[i + 2], elem[i + 3])
    return "True"

@app.route('/return_directions')
def return_directions():
    return list(db.return_directions())

@app.route('/return_cities')
def return_cities():
    direction = request.args.get('direction')
    return list(db.return_cities(direction))

@app.route('/return_recomendations')
def return_recomendations():
    direction = request.args.get('direction')
    city = request.args.get('city')
    result = db.return_recomendations(direction, city)
    formatted_result = list(result)
    return formatted_result

@app.route('/return_vacancies')
def return_vacancies():
    direction = request.args.get('direction')
    city = request.args.get('city')
    result = db.return_vacancies(direction, city)
    formatted_result = list(list(item) for item in result)
    return formatted_result


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True)
