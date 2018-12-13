from telebot import AsyncTeleBot, types
import time
import random
import re
bot = AsyncTeleBot('636547162:AAEcNQbYlIXr5oQbXYgo-7GMYM_QIn1XtlU')

markup = types.InlineKeyboardMarkup(row_width=1)
b1 = types.InlineKeyboardButton(text='1', callback_data='one')
b2 = types.InlineKeyboardButton(text='2',callback_data='two')
markup.add(b1,b2)

@bot.message_handler(commands=['send_buttons'])
def select_buttons(message):





    task = bot.send_message(
                            chat_id=message.chat.id,
                            text='Select one of those buttons below',
                            reply_markup=markup)
    result = task.wait()
    print(result)

@bot.message_handler(regexp='\d*\.\d*')
def send_plus_one(message):
    m = re.search('\d*\.\d*',message.text)
    if m:
        num = float()
        num+=1.0
        task =  bot.reply_to(message,text=str(num))
        task.wait()

@bot.message_handler(func=lambda message: True)
def some_message(message):
    task = bot.reply_to(message,text='Handling...')
    time.sleep(15)

    result = task.wait()
    print()
    task = bot.edit_message_text(message_id=result.message_id,chat_id=result.chat.id,text=str(random.randint(0,10)))
    task.wait()


@bot.callback_query_handler(func=lambda query: True)
def change_text(query):
    task = bot.edit_message_text(message_id=query.message.message_id,chat_id=query.message.chat.id,text=query.data,reply_markup=markup)
    task.wait()



bot.polling()




