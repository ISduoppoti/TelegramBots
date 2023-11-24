import telebot
import sqlite3
import openai

API_KEY = ""
openai.api_key = API_KEY

bot = telebot.TeleBot('6353292333:AAF_R2F4jequ90S6DYeVDSc88ZgnQtN6frE')

#Some user_data
businessArea = None

@bot.message_handler(commands=['start', 'help'])
def OnStart(message):

    conn = sqlite3.connect('BotData.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), area varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    user_last_name = ""
    if message.from_user.last_name != None:
        user_last_name = message.from_user.last_name

    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} {user_last_name}! '+ 
                     'Ось список команд які я розумію:\n\n'+
                     '/counseling - розпочати консультацію\n'+
                     '/site - зайти на сайт\n'+
                     '/help - ще раз вивести цей блок\n\n'+
                     'Чекаю від тебе команду ^_^\n')


@bot.message_handler(commands=['site'])
def OnSite(message):
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Перейти на сайт->', url = 'https://bit.ly/2INu92g'))
    bot.send_message(message.chat.id, f'Ось посилання на сайт ^_^:\n', reply_markup=markup)
    print('Polsovatel:', message.from_user.first_name, message.from_user.last_name, 'otkril site')
    

@bot.message_handler(commands=['counseling'])
def OnCounsel(message):
    
    bot.send_message(message.chat.id, f'Розпочнемо! Скажіть яка сфера бізнесу вас цікавить?')
    bot.register_next_step_handler(message, MakeCounsel)

def MakeCounsel(message):
    global businessArea
    businessArea = message.text.strip()

    print(businessArea)
    #bot.send_message(message, 'Отправить чат gpt запрос "Уявм себе"')

    markup = telebot.types.InlineKeyboardMarkup()
    button_onebuyer = telebot.types.InlineKeyboardButton('Одиночні покупці', callback_data="OneBuyer")
    button_optbuyer = telebot.types.InlineKeyboardButton('Оптові покупці', callback_data="OptBuyer")
    button_dontknow = telebot.types.InlineKeyboardButton('Я хз', callback_data="DontKnow")

    markup.row(button_onebuyer, button_optbuyer)
    markup.row(button_dontknow)

    bot.send_message(message.chat.id, 'Оберіть на яких клієнтів ви націлитеся\n', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["OneBuyer", "OptBuyer", "DontKnow"])
def callback_handler(call):

    if call.data == "OneBuyer":

        bot.send_message(call.message.chat.id, f"Отправить запрос GPT с данными {businessArea} + на мелкие продажи")
    elif call.data == "OptBuyer":

        bot.send_message(call.message.chat.id, f"Отправить запрос GPT с данными {businessArea} + на оптовые продажи")
    elif call.data == "DontKnow":

        bot.send_message(call.message.chat.id, f"Отправить запрос GPT с данными {businessArea} + какие есть покупатели и отправить боту телеграма")



@bot.message_handler()
def OnNotCommand(message):

    bot.send_message(message.chat.id, f'Не зрозумів що ти написав...Краще перевір команду "/site"')


bot.polling(none_stop = True)