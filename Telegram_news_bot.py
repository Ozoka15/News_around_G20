
import telebot
import requests
import json
import random as rd
import fake_useragent
from bs4 import BeautifulSoup as bs
from newsapi.newsapi_client import NewsApiClient
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError


bot = telebot.TeleBot('5568824717:AAEl0bNR7dF0i64B74OHxn7icyOX8GLCk7Y')
newsapi = NewsApiClient(api_key = '52a2b572ebf549149b492212fa1d789d')

ua = fake_useragent.UserAgent()
headers = {'User-Agent': ua.random}


from telebot import types
from datetime import datetime


@bot.message_handler(commands=['start'])
def get_started(message):
    first_reaction = bot.send_message(message.chat.id, 'Hello! You can now catch up with news about one of the G20 countries. Write me something :)')
    bot.register_next_step_handler(first_reaction, set_country)

def set_country(message):
    countries = ['Australia', 'Argentina', 'Brazil', 'Canada', 'China', 'EU', 'France',
                  'Germany', 'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'Russia',
                  'Saudi Arabia', 'South Korea', 'South Africa', 'Turkey', 'UK', 'USA']
    keyboard = types.InlineKeyboardMarkup()
    message_info = bot.send_message(message.from_user.id, text = 'Choose the country:')
    message_id = message_info.id
    for i in range(0, len(countries), 2):
        buttons = []
        buttons.append(types.InlineKeyboardButton(text = countries[i], callback_data = 'country_'+countries[i]+'_'+str(message_id)))
        buttons.append(types.InlineKeyboardButton(text = countries[i+1], callback_data = 'country_'+countries[i+1]+'_'+str(message_id)))
        keyboard.add(*buttons)
    bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = 'Choose the country:', reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    categories = ['economy', 'policy', 'society', 'security', 'ecology', 'science', 'sport', 'culture and art', 'celebrities', 'foreign policy']
    user_id = call.from_user.id
    if call.data.split('_')[0] == 'country':
        users = json_communicate('r', 'my_dick.json')
        users[str(call.message.chat.id)] = {'country': call.data.split('_')[1]}
        users[str(call.from_user.id)]['id_of_message'] = call.data.split('_')[2]
        json_communicate('w', 'my_dick.json', users)
        keyboard = types.InlineKeyboardMarkup()
        for o in range (0, len(categories), 2):
            knopki = []
            knopki.append(types.InlineKeyboardButton(text = categories[o], callback_data = 'category_'+categories[o]+'_'+str(user_id)))
            knopki.append(types.InlineKeyboardButton(text = categories[o+1], callback_data = 'category_'+categories[o+1]+'_'+str(user_id)))
            keyboard.add(*knopki)
        with open('my_dick.json') as trash:
            goal = json.load(trash)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = goal[str(user_id)]["id_of_message"], text = 'Choose the category:', reply_markup = keyboard)
    if call.data.split('_')[0] == 'category':
        users = json_communicate('r', 'my_dick.json')
        users[str(call.from_user.id)]['category'] = call.data.split('_')[1]
        json_communicate('w', 'my_dick.json', users)
        keyboard = types.InlineKeyboardMarkup()
        for w in range(1, 11, 2):
            stuff = []
            stuff.append(types.InlineKeyboardButton(text = w, callback_data = 'amount_'+str(w)+'_'+str(user_id)))
            stuff.append(types.InlineKeyboardButton(text = w+1, callback_data = 'amount_'+str(w+1)+'_'+str(user_id)))
            keyboard.add(*stuff)
        with open('my_dick.json') as trash:
            goal = json.load(trash)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = goal[str(user_id)]["id_of_message"], text = 'Select the required number of news items:', reply_markup = keyboard)
    if call.data.split('_')[0] == 'amount':
        users = json_communicate('r', 'my_dick.json')
        users[str(call.from_user.id)]['amount'] = call.data.split('_')[1]
        json_communicate('w', 'my_dick.json', users)
        with open('my_dick.json') as trash:
            goal = json.load(trash)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = goal[str(user_id)]["id_of_message"], text ='Write the word "news" :)')

def json_communicate(method, file, data=None):
    if method == 'r':
        with open(file, 'r') as info:
            return json.load(info)
    else:
        with open(file, 'w') as info:
            json.dump(data, info)
        return True

@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.text.lower().split()[0] == 'news':
        get_news(message)
    else:
        search_text = '%20'.join(''.join([i for i in message.text if (i.isalpha() or i == ' ')]).split())
        site = requests.get('https://yandex.ru/images/search?text=' + search_text)
        if str(site) == '<Response [200]>':
            print(site.text)
            data = bs(site.text, features='lxml')
            result = data.find_all('img', class_='serp-item__thumb justifier__thumb')
            if not result:
                bot.send_message(message.from_user.id, "I couldn't find any pictures of this")
            else:
                choosen_picture = 'https:' + rd.choice(result).get('src')
                bot.send_photo(message.from_user.id, choosen_picture, 'Get it :)')
        else:
            bot.send_message(message.from_user.id, 'Everything is broken :(')
            

def get_news(message):
    user_id = message.from_user.id
    with open('my_dick.json') as trash:
        goal = json.load(trash)
    land = goal[str(user_id)]["country"].lower()
    topic = goal[str(user_id)]["category"]
    required_date = datetime.now().date()
    answer = requests.get(f'https://newsapi.org/v2/everything?q={topic}%20of%20{land}&from={required_date}&to={required_date}&sortBy=popularity&apiKey=52a2b572ebf549149b492212fa1d789d')
    fuck = str(answer.text)
    replace_answer = fuck.replace('null','None')
    dct = eval(replace_answer)
    quantity = int(goal[str(user_id)]["amount"]) if len(dct['articles']) > int(goal[str(user_id)]["amount"]) else len(dct['articles'])
    parsing(message, dct, quantity)

def parsing(message, dct, quantity):
    for s in range(quantity):
        resource = dct['articles'][s]['source']['name']
        running_line = dct['articles'][s]['title']
        content = dct['articles'][s]['description']
        link = dct['articles'][s]['url']
        result = 'From '+resource+'\n\n'+running_line.upper()+'\n\n'+content+'\n\n'+link
        bot.send_message(message.from_user.id, result)

bot.polling(none_stop=True, interval=0)




