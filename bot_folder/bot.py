import sys
import telebot;
import tocken
import threading
import time
from telebot import types
from flask import Flask
app = Flask(__name__)
import requests


global direction
global city
global key_character
global update_locker

update_locker = 0
key_character = 0
bot = telebot.TeleBot(tocken.tocken)
map_dir = dict()
map_cities = dict()
map_recom = dict()

def updater_func():
    global update_locker
    update_locker = 1
    print("Function is running", file=sys.stderr)
    response = ''
    try:
        response = requests.get('http://project_globa_two_scrap_1:5001/scrap')
    except requests.exceptions.RequestException as e:
        print('\n Cannot reach the pong service.', file=sys.stderr)
    update_locker = 0
    print("FINISHED UPDATE", file=sys.stderr)

def run_thread():
    updater_func()
    while True:
        time.sleep(3 * 60 * 60)
        updater_func()

thread = threading.Thread(target=run_thread)
thread.start()

print("I started", file=sys.stderr)

def create_keyboards(array_vacancies, array_of_skills):
    one_counter = 0
    two_counter = 0
    three_counter = 0
    keyboard_one = types.InlineKeyboardMarkup()
    keyboard_two = types.InlineKeyboardMarkup()
    keyboard_three = types.InlineKeyboardMarkup()

    for elem in array_vacancies:
        counter = 0
        if (elem[2].replace("@", "").replace("Требования:", "").replace("Задачи:", "").replace("Приветствуются:", "") == ""):
            print("If empty", file=sys.stderr)
            key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
            keyboard_one.add(key)
        else:
            print("If not empty", file=sys.stderr)
            for element in array_of_skills:
                print(str(element), file=sys.stderr)
                if element.lower() in elem[2].lower():
                    if counter == 0:  
                        key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                        keyboard_one.add(key)
                        counter += 1
                        one_counter += 1
                    elif counter == 1:
                        key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                        keyboard_two.add(key)
                        counter += 1
                        two_counter += 1
                    elif counter == 2:
                        key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                        keyboard_three.add(key)
                        counter += 1
                        three_counter += 1
    return keyboard_one, keyboard_two, keyboard_three, one_counter, two_counter, three_counter

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if update_locker == 1:
        bot.send_message(message.chat.id, "Происходит обновление данных, пожалуйста, ожидайте...")

    elif message.text == "/start":
        global key_character
        key_character = 0
        bot.send_message(message.from_user.id, "Обновляю данные...")
        
        try:
            set_directions = set((requests.get('http://project_globa_two_scrap_1:5001/return_directions')).json())
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'

        keyboard = types.InlineKeyboardMarkup()
        i = 0
        for elem in set_directions:
            name = 'direction_' + f'{i}'
            key = types.InlineKeyboardButton(text = elem, callback_data = name)
            map_dir[i] = elem
            keyboard.add(key)
            i += 1
        bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\nВыбери сферу, в которой хочешь работать:", reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Чтобы запустить бота нажмите /start\n Чтобы обновить бота введите /update", reply_markup=keyboard)
    elif message.text == "/update":
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text = "Начать", callback_data = "update")
        keyboard.add(key)
        bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\nДавай начнем", reply_markup=keyboard)
    else:
        print("Key: " + str(key_character), file=sys.stderr)
        if (key_character == 1):
            key_character = 0
            print(message.text, file=sys.stderr)
            if message.text == "_":
                try:
                    print("Tried first", file=sys.stderr)
                    url = f'http://project_globa_two_scrap_1:5001/return_vacancies?direction={direction}&city={city}'
                    array_vacancies = (requests.get(url)).json()
                    keyboard = types.InlineKeyboardMarkup()
                    for elem in array_vacancies:
                        key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                        keyboard.add(key)
                    bot.send_message(message.chat.id, "Вот то, что мы можем предложить вам в городе " + city + " по направлению "  + direction + ":", reply_markup=keyboard)
                except:
                    keyboard = types.InlineKeyboardMarkup()
                    key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
                    keyboard.add(key)
                    bot.send_message(message.chat.id, "Упс, кажется нужно обновить данные о вас! \n\nЧтобы обновить сведения о вас - нажмите кнопку ниже", reply_markup=keyboard)

            else:
                array_of_skills = message.text.split(",")
                print("Array_of_skills: " + ' '.join(array_of_skills), file=sys.stderr)
                try:
                    print("Tried second", file=sys.stderr)
                    url = f'http://project_globa_two_scrap_1:5001/return_vacancies?direction={direction}&city={city}'
                    array_vacancies = (requests.get(url)).json()

                    keyboard_one, keyboard_two, keyboard_three, one_counter, two_counter, three_counter = create_keyboards(array_vacancies, array_of_skills)
                    print("Returned", file=sys.stderr)
                    if one_counter == 0:
                        bot.send_message(message.chat.id, "К сожалению не смогли вам ничего подобрать(")
                    else:
                        print("Else", file=sys.stderr)
                        if one_counter != 0:
                            bot.send_message(message.chat.id, "Вот то, в чем вы можете себя попробовать (минимум 1 совпадение) в городе " + city + " по направлению "  + direction + " учитывая ваш опыт:", reply_markup=keyboard_one)
                        if two_counter != 0:
                            bot.send_message(message.chat.id, "Вот то, в чем вы хорошо разбираетесь (минимум 2 совпадения) в городе " + city + " по направлению "  + direction + " учитывая ваш опыт:", reply_markup=keyboard_two)
                        if three_counter != 0:
                            bot.send_message(message.chat.id, "Вот то, в чем вы профи (минимум 3 совпадения) в городе " + city + " по направлению "  + direction + " учитывая ваш опыт:", reply_markup=keyboard_three)
                except:
                    keyboard = types.InlineKeyboardMarkup()
                    key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
                    keyboard.add(key)
                    bot.send_message(message.chat.id, "Упс, кажется нужно обновить данные о вас! \n\nЧтобы обновить сведения о вас - нажмите кнопку ниже", reply_markup=keyboard)

        else:
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
            keyboard.add(key)
            bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\nЧтобы обновить сведения о вакансиях - нажмите кнопку ниже", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if update_locker == 1:
        bot.send_message(call.message.chat.id, "Происходит обновление данных, пожалуйста, ожидайте...")

    elif 'direction_' in call.data:
        try:
            global direction
            direction = map_dir[int(call.data.split('_')[1])]
        
            try:
                url = f'http://project_globa_two_scrap_1:5001/return_cities?direction={direction}'
                set_cities = set((requests.get(url)).json())
            except requests.exceptions.RequestException as e:
                print('\n Cannot reach the pong service.')
                return 'Alarm\n'
            
            keyboard = types.InlineKeyboardMarkup()
            i = 0
            for elem in set_cities:
                name = 'city_' + f'{i}'
                key = types.InlineKeyboardButton(text = elem, callback_data = name)
                map_cities[i] = elem
                keyboard.add(key)
                i += 1
            bot.send_message(call.message.chat.id, "Где бы вы хотели работать по направлению " + direction + "?", reply_markup=keyboard)
        except:
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
            keyboard.add(key)
            bot.send_message(call.message.chat.id, "Упс, кажется нужно обновить данные о вас! \n\nЧтобы обновить сведения о вас - нажмите кнопку ниже", reply_markup=keyboard)

    elif 'city_' in call.data:
        try:
            global city
            global key_character
            if direction == "Хакеры":
                city = map_cities[int(call.data.split('_')[1])]
                url = f'http://project_globa_two_scrap_1:5001/return_vacancies?direction={direction}&city={city}'
                array_vacancies = (requests.get(url)).json()
                keyboard = types.InlineKeyboardMarkup()
                for elem in array_vacancies:
                    key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                    keyboard.add(key)
                bot.send_message(call.message.chat.id, "Вот то, что мы можем предложить вам в городе " + city + " по направлению "  + direction + ":", reply_markup=keyboard)
            else:
                key_character = 1
                city = map_cities[int(call.data.split('_')[1])]
                url = f'http://project_globa_two_scrap_1:5001/return_recomendations?direction={direction}&city={city}'
                array_vacancies = (requests.get(url)).json()
                bot.send_message(call.message.chat.id, "Какими навыками вы обладаете? \n\nНапишите через запятую то, с чем вы работали \n\nНапример: python, rest api, C++. \n\nЕсли вы хотите пропустить этот этап, то наберите _ .")
        except:
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
            keyboard.add(key)
            bot.send_message(call.message.chat.id, "Упс, кажется нужно обновить данные о вас! \n\nЧтобы обновить сведения о вас - нажмите кнопку ниже", reply_markup=keyboard)

    elif 'update' in call.data:
        
        try:
            set_directions = set((requests.get('http://project_globa_two_scrap_1:5001/return_directions')).json())
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'

        keyboard = types.InlineKeyboardMarkup()
        i = 0
        print (set_directions)
        for elem in set_directions:
            name = 'direction_' + f'{i}'
            key = types.InlineKeyboardButton(text = elem, callback_data = name)
            map_dir[i] = elem
            keyboard.add(key)
            i += 1
        bot.send_message(call.message.chat.id, "Я нашел много вариантов! \n\nВыбери сферу, в которой хочешь работать:", reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, 'Ошибка')


bot.polling(none_stop=True, interval=0)
