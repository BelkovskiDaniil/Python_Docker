import telebot;
import tocken
from telebot import types

import requests


global direction
global city

bot = telebot.TeleBot(tocken.tocken)
map_dir = dict()
map_cities = dict()

print("I started")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Обновляю данные...")

        response = ''
        try:
            response = requests.get('http://project_globa_two_scrap_1:5001/scrap')
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'
        
        try:
            set_directions = set((requests.get('http://project_globa_two_scrap_1:5001/return_directions')).json())
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'

        # project_two.scrap.scrap()
        # set_directions = project_two.db.return_directions('positive.db')
        keyboard = types.InlineKeyboardMarkup()
        i = 0
        for elem in set_directions:
            name = 'direction_' + f'{i}'
            key = types.InlineKeyboardButton(text = elem, callback_data = name)
            map_dir[i] = elem
            keyboard.add(key)
            i += 1
        bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\n Выбери сферу, в которой хочешь работать:", reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Чтобы запустить бота нажмите /start\n Чтобы обновить бота введите /update", reply_markup=keyboard)
    elif message.text == "/update":
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
        keyboard.add(key)
        bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\n Чтобы обновить сведения о вакансиях - нажмите кнопку ниже", reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
        keyboard.add(key)
        bot.send_message(message.from_user.id, "Привет, я помогу тебе подобрать вакансии в прекрасной компании Positive technologies! \n\n Чтобы обновить сведения о вакансиях - нажмите кнопку ниже", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if 'direction_' in call.data:
        try:
            global direction
            direction = map_dir[int(call.data.split('_')[1])]
        
            try:
                url = f'http://project_globa_two_scrap_1:5001/return_cities?direction={direction}'
                set_cities = set((requests.get(url)).json())
            except requests.exceptions.RequestException as e:
                print('\n Cannot reach the pong service.')
                return 'Alarm\n'
            
            # set_cities = project_two.db.return_cities('positive.db', direction)
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
            bot.send_message(call.message.chat.id, "Упс, кажется нужно обновить данные по вакансиям! \n\n Чтобы обновить сведения о вакансиях - нажмите кнопку ниже", reply_markup=keyboard)
    elif 'city_' in call.data:
        # global city
        # city = map_cities[int(call.data.split('_')[1])]

        # try:
        #     url = f'http://pong-service-container:5001/return_vacancies?direction={direction}&city={city}'
        #     array_vacancies = (requests.get(url)).json()
        # except requests.exceptions.RequestException as e:
        #     print('\n Cannot reach the pong service.')
        #     return 'Alarm\n'
            
        # # array_vacancies = project_two.db.return_vacancies('positive.db', direction, city)
        # print(array_vacancies)
        # keyboard = types.InlineKeyboardMarkup()
        # for elem in array_vacancies:
        #     print(array_vacancies)
        #     key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
        #     keyboard.add(key)
        # bot.send_message(call.message.chat.id, "Вот то, что мы можем предложить вам в городе " + city + " по направлению "  + direction + ":", reply_markup=keyboard)
        try:
            global city
            city = map_cities[int(call.data.split('_')[1])]
            url = f'http://project_globa_two_scrap_1:5001/return_vacancies?direction={direction}&city={city}'
            array_vacancies = (requests.get(url)).json()

            # try:
            #     url = f'http://pong-service-container:5001/return_vacancies?direction={direction}&city={city}'
            #     array_vacancies = (requests.get(url)).json()
            # except requests.exceptions.RequestException as e:
            #     print('\n Cannot reach the pong service.')
            #     return 'Alarm\n'
            
            # array_vacancies = project_two.db.return_vacancies('positive.db', direction, city)
            # print(array_vacancies)
            keyboard = types.InlineKeyboardMarkup()
            for elem in array_vacancies:
                # print(array_vacancies)
                key = types.InlineKeyboardButton(text = elem[0], url=elem[1])
                keyboard.add(key)
            bot.send_message(call.message.chat.id, "Вот то, что мы можем предложить вам в городе " + city + " по направлению "  + direction + ":", reply_markup=keyboard)
        except:
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text = "Обновить данные", callback_data = "update")
            keyboard.add(key)
            bot.send_message(call.message.chat.id, "Упс, кажется нужно обновить данные по вакансиям! \n\n Чтобы обновить сведения о вакансиях - нажмите кнопку ниже", reply_markup=keyboard)
    elif 'update' in call.data:
        bot.send_message(call.message.chat.id, "Обновляю данные...")

        response = ''
        try:
            response = requests.get('http://project_globa_two_scrap_1:5001/scrap')
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'
        
        try:
            set_directions = set((requests.get('http://project_globa_two_scrap_1:5001/return_directions')).json())
        except requests.exceptions.RequestException as e:
            print('\n Cannot reach the pong service.')
            return 'Alarm\n'

        # project_two.scrap.scrap()
        # set_directions = project_two.db.return_directions('positive.db')
        keyboard = types.InlineKeyboardMarkup()
        i = 0
        print (set_directions)
        for elem in set_directions:
            name = 'direction_' + f'{i}'
            key = types.InlineKeyboardButton(text = elem, callback_data = name)
            map_dir[i] = elem
            keyboard.add(key)
            i += 1
        bot.send_message(call.message.chat.id, "Я нашел много вариантов! \n\n Выбери сферу, в которой хочешь работать:", reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, 'Ошибка')


bot.polling(none_stop=True, interval=0)
