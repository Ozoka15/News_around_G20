#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
from bs4 import BeautifulSoup as bs
import requests
import json
from newsapi import NewsApiClient


bot = telebot.TeleBot('5568824717:AAEl0bNR7dF0i64B74OHxn7icyOX8GLCk7Y')
newsapi = NewsApiClient(api_key = '52a2b572ebf549149b492212fa1d789d')


from telebot import types
from datetime import datetime


@bot.message_handler(commands=['start'])
def get_started(message):
    first_reaction = bot.send_message(message.chat.id, 'Привет :)')
    bot.register_next_step_handler(first_reaction, set_country)
    
def set_country(message):
    countries = ['australia', 'argentina', 'brazil', 'canada', 'china', 'eu', 'france',
                  'germany', 'india', 'indonesia', 'italy', 'japan', 'mexico', 'russia',
                  'saudi arabia', 'south korea', 'south africa', 'turkey', 'uk', 'usa']
    keyboard = types.InlineKeyboardMarkup()
    message_info = bot.send_message(message.from_user.id, text = 'Выбери страну:')
    message_id = message_info.id
    for i in countries:
        keyboard.add(types.InlineKeyboardButton(text = i, callback_data = 'country_'+i+'_'+str(message_id)))
    bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = 'Выбери страну:', reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    categories = ['economy', 'policy', 'society', 'security', 'ecology', 'science', 'sport', 'culture and art', 'celebrities', 'foreign policy']
    user_id = call.from_user.id
    if call.data.split('_')[0] == 'country':
        bot.send_message(call.from_user.id, 'Молодец!')
        users = json_communicate('r', 'my_dick.json')
        users[str(call.message.chat.id)] = {'country': call.data.split('_')[1]}
        users[str(call.from_user.id)]['id_of_message'] = call.data.split('_')[2]
        json_communicate('w', 'my_dick.json', users)
        keyboard = types.InlineKeyboardMarkup()
        for o in categories:
            keyboard.add(types.InlineKeyboardButton(text = o, callback_data = 'category_'+o))
        with open('my_dick.json') as trash:
            goal = json.load(trash)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = goal[str(user_id)]["id_of_message"], text = 'Выбери категорию:', reply_markup = keyboard)
    if call.data.split('_')[0] == 'category':
        users = json_communicate('r', 'my_dick.json')
        users[str(call.from_user.id)]['category'] = call.data.split('_')[1]
        json_communicate('w', 'my_dick.json', users)  
        keyboard = types.InlineKeyboardMarkup()
        for w in range(1,11):
            keyboard.add(types.InlineKeyboardButton(text = w, callback_data = 'amount_'+str(w)))
        with open('my_dick.json') as trash:
            goal = json.load(trash)
        bot.edit_message_text(chat_id = call.from_user.id, message_id = goal[str(user_id)]["id_of_message"], text = 'Выбери необходимое количество новостей:', reply_markup = keyboard)
    if call.data.split('_')[0] == 'amount':
        users = json_communicate('r', 'my_dick.json')
        users[str(call.from_user.id)]['amount'] = call.data.split('_')[1]
        json_communicate('w', 'my_dick.json', users)
        bot.send_message(call.message.chat.id, text ='Напиши слово "новости" :)')

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
    if message.text.lower().split()[0] == 'новости':
        get_news(message)
    else:
        bot.send_message(message.from_user.id, 'Вы не написали первым слово "новости" :(')
    

def get_news(message):
    user_id = message.from_user.id
    with open('my_dick.json') as trash:
        goal = json.load(trash)
    land = goal[str(user_id)]["country"]
    topic = goal[str(user_id)]["category"]
    quantity = int(goal[str(user_id)]["amount"])
    required_date = datetime.now().date()
    answer = requests.get(f'https://newsapi.org/v2/everything?q={topic}%20of%20{land}&from={required_date}&to={required_date}&sortBy=popularity&apiKey=52a2b572ebf549149b492212fa1d789d')
    fuck = str(answer.text)
    replace_answer = fuck.replace('null','None')
    dct = eval(replace_answer)
    parsing(message, dct, quantity)
    
def parsing(message, dct, quantity):
    for s in range(quantity):
        resource = dct['articles'][s]['source']['name']
        running_line = dct['articles'][s]['title']
        content = dct['articles'][s]['description']
        link = dct['articles'][s]['url']
        result = 'From '+resource+'\n\n'+running_line.upper()+'\n\n'+content+'\n\n'+link
        print(dct)
        bot.send_message(message.from_user.id, result)
    
bot.polling(none_stop=True, interval=0)


# In[ ]:




