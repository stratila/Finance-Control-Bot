import sqlalchemy as sa
import random
import re
from datetime import date
from telebot import AsyncTeleBot, types
import languageMessages
import json

import sys
import os

from flask import Flask, request

server = Flask(__name__)


CONFIGURATION_TABLE = 'config'

purchaseTypes = ['market', 'food', 'restaurants', 'transport', 'taxi', 'internet', 'post', 'shopping']

wallet_types = ['usd', 'uah', 'rub']


# Creating a configuration table at database.
# When program starts at not the first time, except block will run to show
# that tables have already created.
try:
    conn = sa.create_engine('sqlite:///botDataBase.db')
    meta = sa.MetaData()
    sa.Table(CONFIGURATION_TABLE, meta,
             sa.Column('id', sa.Integer, primary_key=True),
             sa.Column('first_name', sa.String),
             sa.Column('lang_code', sa.String),
             sa.Column('curr', sa.String))  # configuration table
    meta.create_all(conn)
except Exception as e:
    print(e, '\nThe program have started at not the first time. '
             'Configuration tables have already created.')


TOKEN = '636547162:AAEcNQbYlIXr5oQbXYgo-7GMYM_QIn1XtlU'
bot = AsyncTeleBot(TOKEN)


def get_lang_code(uid):
    meta.reflect(bind=conn)
    table = meta.tables[CONFIGURATION_TABLE]
    lang_code = conn.execute(sa.select([table.c.lang_code]).where(table.c.id == uid))
    lc, = lang_code.fetchone()
    return lc

def get_curr(uid):
    meta.reflect(bind=conn)
    table = meta.tables[CONFIGURATION_TABLE]
    curr = conn.execute(sa.select([table.c.curr]).where(table.c.id == uid))
    lc, = curr.fetchone()
    return lc

def get_costs_table(uid,curr):
    meta.reflect(bind=conn)
    return meta.tables['id_{curr}_{id}'.format(curr=curr, id=uid)]

@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    lc = get_lang_code(chat_id)
    task = bot.send_document(chat_id=chat_id,
                             data='CgADAgAD6gEAAmMSqEpkEJEjmslmugI',
                             caption=languageMessages.help1[lc])
    task.wait()
    task = bot.send_document(chat_id=chat_id,
                             data='CgADAgAD6wEAAmMSqEoq19zQS2kKEgI',
                             caption=languageMessages.help2[lc])
    task.wait()
    task = bot.send_document(chat_id=chat_id,
                             data='CgADAgAD7AEAAmMSqErq9oCOOIWg_QI',
                             caption=languageMessages.help3[lc])
    task.wait()
    task = bot.send_document(chat_id=chat_id,
                             data='CgADAgAD7QEAAmMSqEqzT4JiEUISwAI',
                             caption=languageMessages.help4[lc])
    task.wait()
    task = bot.send_document(chat_id=chat_id,
                             data='CgADAgAD7gEAAmMSqEqPaxKSsOBFXAI',
                             caption=languageMessages.help5[lc])
    task.wait()





@bot.message_handler(commands=['start'])
def create_user(message):
    try:
        for curr in wallet_types:
            sa.Table('id_{curr}_{number}'.format(number=message.from_user.id, curr=curr), meta,
                     sa.Column('year', sa.Integer),
                     sa.Column('month', sa.Integer),
                     sa.Column('day', sa.Integer),
                     sa.Column('amount', sa.Float),
                     sa.Column('purchase_type', sa.String))  # creating user's purchases history

        sa.Table('pt{number}'.format(number=message.from_user.id), meta,
                 sa.Column('rec_id', sa.Integer, primary_key=True),
                 sa.Column('purchase_type', sa.String))  # creating user's purchase types

        meta.create_all(conn)
        meta.reflect(bind=conn)
        table = meta.tables[CONFIGURATION_TABLE]
        conn.execute(table.insert((message.from_user.id,
                                   message.from_user.first_name, 'en',
                                   'usd')))  # add user to config table

        lc = get_lang_code(message.from_user.id)
        task = bot.send_message(chat_id=message.chat.id, text=languageMessages.start[lc])
        task.wait()
    except Exception as exc:
        print(exc)
        lc = get_lang_code(message.from_user.id)
        task = bot.send_message(chat_id=message.chat.id, text=languageMessages.start_used[lc])
        task.wait()


@bot.message_handler(commands=['language'])
def change_lang_ask(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    en_dict = {'type': 'lang', 'lang': 'en'}
    ru_dict = {'type': 'lang', 'lang': 'ru'}
    b1 = types.InlineKeyboardButton(text='🇷🇺', callback_data=json.dumps(ru_dict))
    b2 = types.InlineKeyboardButton(text='🇬🇧', callback_data=json.dumps(en_dict))
    markup.add(b1, b2)
    lc = get_lang_code(message.chat.id)
    task = bot.send_message(chat_id=message.chat.id, text=languageMessages.change_lang_ask[lc], reply_markup=markup)
    task.wait()


def if_change_lang(query):
    lang_dict = json.loads(query.data)
    if lang_dict['type'] == 'lang':
        return True
    else:
        return False


@bot.callback_query_handler(func=if_change_lang)
def change_lang_end(query):
    lang_dict = json.loads(query.data)
    chat_id = query.message.chat.id

    meta.reflect(bind=conn)
    table = meta.tables[CONFIGURATION_TABLE]

    conn.execute(table.update().where(table.c.id == chat_id).values(lang_code=lang_dict['lang']))

    task = bot.edit_message_text(message_id=query.message.message_id,
                                 chat_id=chat_id,
                                 text=languageMessages.change_lang_end[lang_dict['lang']])
    task.wait()


@bot.message_handler(commands=['currency'])
def change_currency_ask(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup_buttons = []
    currency_dict = {'type': 'curr'}
    for curr in wallet_types:
        currency_dict['curr'] = curr
        markup_buttons.append(types.InlineKeyboardButton(text=languageMessages.currencies[curr],
                                                         callback_data=json.dumps(currency_dict)))
    markup.add(*markup_buttons)
    task = bot.send_message(chat_id=message.chat.id,
                            text=languageMessages.choose_currency[get_lang_code(message.chat.id)],
                            reply_markup=markup)
    task.wait()


def if_change_curr(query):
    lang_dict = json.loads(query.data)
    if lang_dict['type'] == 'curr':
        return True
    else:
        return False


@bot.callback_query_handler(func=if_change_curr)
def change_currency_end(query):

    inf_dict = json.loads(query.data)
    chat_id = query.message.chat.id
    lc = get_lang_code(chat_id)

    meta.reflect(bind=conn)
    table = meta.tables[CONFIGURATION_TABLE]

    prev_curr, = conn.execute(sa.select([table.c.curr]).where(table.c.id == chat_id)).fetchone()
    if prev_curr == inf_dict['curr']:
        task = bot.edit_message_text(chat_id=chat_id,
                                     message_id=query.message.message_id,
                                     text=languageMessages.already_have_curr[lc].format(
                                                        curr=languageMessages.currencies[prev_curr]))
        task.wait()
        return

    conn.execute(table.update().where(table.c.id == chat_id).values(curr=inf_dict['curr']))

    task = bot.edit_message_text(message_id=query.message.message_id,
                                 chat_id=chat_id,
                                 text=languageMessages.successful_change_currency
                                 [
                                    lc
                                 ].format(prev_curr=languageMessages.currencies[prev_curr],
                                          curr_curr=languageMessages.currencies[inf_dict['curr']]))
    task.wait()


@bot.message_handler(commands=['add_purchase_type'])
def add_purchase_type_ask(message):
    lc = get_lang_code(message.chat.id)
    markup = types.ForceReply(selective=False)
    task = bot.send_message(chat_id=message.chat.id,
                            text=languageMessages.enter_type_of_purchase[lc],
                            reply_markup=markup)
    task.wait()


def if_add_ptype(message):
    if message.reply_to_message is None:
        return False

    lc = get_lang_code(message.chat.id)
    if message.reply_to_message.text == languageMessages.enter_type_of_purchase[lc]:
        return True
    else:
        return False


@bot.message_handler(func=if_add_ptype)
def add_purchase_type_end(message):
    meta.reflect(bind=conn)
    table = meta.tables['pt{id}'.format(id=message.chat.id)]

    res = tuple(conn.execute(sa.select([table.c.purchase_type])))
    lc = get_lang_code(message.chat.id)

    for pt, in res:
        if pt == message.text:
            task = bot.reply_to(message=message,
                                text=languageMessages.already_have_ptype[lc].format(ptype=message.text))
            task.wait()
            return
    print(sys.getsizeof(message.text.encode('utf-8')), message.text.encode('utf-8'))
    if_eng = len(message.text) == len(message.text.encode('utf-8'))
    if sys.getsizeof(message.text.encode('utf-8')) > 37 or not if_eng:
        task = bot.reply_to(message=message,
                                text=languageMessages.purchase_type_size_error[lc])
        task.wait()
        return

    rec_id, = tuple(conn.execute(sa.select([sa.func.count()]).select_from(table)).fetchone())
    conn.execute(table.insert((rec_id+1, message.text)))

    task = bot.send_message(chat_id=message.chat.id,
                            text=languageMessages.successful_added_ptype[lc].format(ptype=message.text))
    task.wait()


def is_custom_types(uid, pos):
    meta.reflect(bind=conn)
    table = meta.tables['pt{id}'.format(id=uid)]
    result = conn.execute(sa.select([table.c.purchase_type]).where(table.c.rec_id >= pos))

    if len(tuple(result)) != 0:
        return True
    else:
        return False


def add_inline_buttons(markup, amount, lc, uid):
    amount_dict = {'type': 'am', 'am': amount}  # am means amount
    buttons = []
    for ptype in purchaseTypes:
        amount_dict['ptype'] = ptype  # ptype means purchase type
        buttons.append(types.InlineKeyboardButton(text=languageMessages.locale_ptypes[lc][ptype],
                                                  callback_data=json.dumps(amount_dict)))

    if is_custom_types(uid=uid, pos=0):
        next_types_dict = {'type': 'nt', 'pg': 2, 'bp': 1, 'am': amount}
        markup.add(types.InlineKeyboardButton(text='➡',
                                              callback_data=json.dumps(next_types_dict)))

    markup.add(*buttons)


@bot.message_handler(regexp='\d+(\.\d+)?')
def ask_amount(message):
    meta.reflect(bind=conn)

    markup = types.InlineKeyboardMarkup(row_width=2)
    user_lang_code = get_lang_code(message.from_user.id)
    curr = get_curr(message.from_user.id)

    m = re.search('\d+(\.\d+)?', message.text)
    try:
        if m:
            amount = round(float(m.group()), 2)

            if amount > 100000000000:
                raise Exception(languageMessages.large_amount[user_lang_code])

            add_inline_buttons(markup=markup, amount=amount, lc=user_lang_code, uid=message.from_user.id)

            text = languageMessages.total_amount[user_lang_code].format(amount=str(amount), curr=curr.upper()) + \
             ' ' + languageMessages.choose_type[user_lang_code]

            task = bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            task.wait()
    except Exception as exc:
        task = bot.reply_to(message, text=exc)
        task.wait()


def if_add_amount(query):
    amount_dict = json.loads(query.data)
    if amount_dict['type'] == 'am':
        return True
    else:
        return False


@bot.callback_query_handler(func=if_add_amount)
def add_amount(query):
    meta.reflect(bind=conn)

    data_dict = json.loads(query.data)

    table = meta.tables['id_{curr}_{id}'.format(id=query.message.chat.id, curr=get_curr(query.message.chat.id))]
    amount = data_dict['am']
    ptype = data_dict['ptype']
    today = date.today()
    conn.execute(table.insert((today.year, today.month, today.day, amount, ptype)))

    lang_code = get_lang_code(query.message.chat.id)

    ptype_text = ptype
    if languageMessages.locale_ptypes[lang_code].get(ptype) is not None:
        ptype_text = languageMessages.locale_ptypes[lang_code].get(ptype)

    task = bot.edit_message_text(message_id=query.message.message_id,
                                 chat_id=query.message.chat.id,
                                 text=languageMessages.successful_added_amount[lang_code].format(amount=str(amount),
                                                                                                 ptype=ptype_text))
    task.wait()


def if_swipe_ptype(query):
    d = json.loads(query.data)
    if d['type'] == 'nt' or d['type'] == 'bt':
        return True
    else:
        return False


def swipe_page(uid, mid, table, direction, page, begin_pos, offset, amount):
    markup = types.InlineKeyboardMarkup(row_width=2)
    if page == 1:
        add_inline_buttons(markup, amount, get_lang_code(uid), uid)
    else:
        print('swipe')
        next_types_dict = {'type': 'nt', 'pg': page + 1, 'bp': begin_pos + offset, 'am': amount}
        prev_types_dict = {'type': 'bt', 'pg': page - 1, 'bp': begin_pos - offset, 'am': amount}
        result = tuple(conn.execute(
            sa.select([table.c.purchase_type]).where(sa.and_(table.c.rec_id >= begin_pos,
                                                             table.c.rec_id < begin_pos + 8))))

        types_buttons = []
        direction_buttons = []
        counter = 0
        for purchase_type, in result:
            counter += 1

            types_buttons.append(types.InlineKeyboardButton(text=purchase_type,
                                                            callback_data=json.dumps({'type': 'am',
                                                                                      'ptype': purchase_type,
                                                                                      'am': amount})))

        direction_buttons.append(types.InlineKeyboardButton(text='⬅',
                                                            callback_data=json.dumps(prev_types_dict)))

        if direction == 'nt':
            pos = begin_pos + offset
        else:
            pos = begin_pos - offset

        if counter == 8 and is_custom_types(uid=uid, pos=pos):
            direction_buttons.append(types.InlineKeyboardButton(text='➡',
                                                                callback_data=json.dumps(next_types_dict)))
        markup.add(*direction_buttons)
        markup.add(*types_buttons)
        print(types_buttons)
    task = bot.edit_message_reply_markup(chat_id=uid, message_id=mid, reply_markup=markup)
    r= task.wait()
    print(r)

@bot.callback_query_handler(func=if_swipe_ptype)
def change_page_ptype(query):
    uid = query.message.chat.id
    mid = query.message.message_id

    meta.reflect(bind=conn)
    table = meta.tables['pt{id}'.format(id=uid)]

    inf_dict = json.loads(query.data)
    amount = inf_dict['am']
    direction = inf_dict['type']
    page = inf_dict['pg']
    begin_pos = inf_dict['bp']

    swipe_page(uid=uid, mid=mid, table=table,
               direction=direction, page=page,
               begin_pos=begin_pos, offset=8,
               amount=amount)


def total_cost(costs_list):
    total_amount = float()
    for data_dict in costs_list:
        total_amount += data_dict['amount']
    return total_amount


def type_cost(costs_list, type_name):
    total_amount = float()
    for data_dict in costs_list:
        if data_dict['purchase_type'] == type_name:
            total_amount += data_dict['amount']
    return total_amount


def get_dollar_emoji_string(percent):
    return '💵'*int(round(percent/10))


def get_percent(total_amount, shared_amount):
    if shared_amount == 0:
        return 0
    return shared_amount*100/total_amount


def get_users_types(uid):
    meta.reflect(bind=conn)
    table1 = meta.tables['pt{id}'.format(id=uid)]
    purchase_types_list = purchaseTypes.copy()
    purchase_types_list.extend([ptype for ptype, in conn.execute(sa.select([table1.c.purchase_type]))])
    return purchase_types_list


@bot.message_handler(commands=['sum_up'])
def send_summing_up_buttons(message):
    lc = get_lang_code(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text=languageMessages.total_button[lc],
                                          callback_data=json.dumps({'type': 'total_sum_up'})))
    markup.add(types.InlineKeyboardButton(text=languageMessages.period_button[lc],
                                          callback_data=json.dumps({'type': 'prd', 'sl': 'y1s', 'd': str()})
                                          ))
    task = bot.send_message(chat_id=message.chat.id,
                            text=languageMessages.summing_up[lc],
                            reply_markup=markup)
    task.wait()



@bot.callback_query_handler(func=lambda query:
                                json.loads(query.data).get('type') == 'total_sum_up')
def send_total_costs(query):
    uid = query.message.chat.id
    lc = get_lang_code(uid)
    curr = get_curr(uid)

    meta.reflect(bind=conn)
    table = meta.tables['id_{curr}_{id}'.format(curr=curr, id=uid)]

    costs_list = [dict(year=year, month=month, day=day, amount=amount, purchase_type=purchase_type)
                  for year, month, day, amount, purchase_type in conn.execute(table.select()).fetchall()]
    total_amount = total_cost(costs_list)
    purchase_types_list = get_users_types(uid=uid)

    text = languageMessages.total_sum_up[lc]
    task = bot.edit_message_text(chat_id=uid, message_id=query.message.message_id, text=text)
    task.wait()

    for ptype in purchase_types_list:
        shared_amount = type_cost(costs_list=costs_list, type_name=ptype)
        percent = get_percent(total_amount, shared_amount)
        percent_string = '{0:<0.2f}'.format(percent) + '%'
        amount_string = '{0:<0.2f}'.format(shared_amount) + curr.upper()

        ptype_text = ptype
        if languageMessages.locale_ptypes[lc].get(ptype) is not None:
            ptype_text = languageMessages.locale_ptypes[lc].get(ptype)

        final_string = '{0:<1s}➡{1:<5s}💰{2:<15s}\n\n'.format(ptype_text, percent_string, amount_string)
        task = bot.send_message(chat_id=uid,text=final_string)
        task.wait()
        # text += final_string

    total_amount_string = '{0:0.2f}'.format(total_amount) + curr.upper()
    last_str = '{0:<15s} {1:15s}'.format(languageMessages.total_button[lc], total_amount_string)
    task = bot.send_message(chat_id=uid,text=last_str)
    task.wait()

    # task = bot.edit_message_text(chat_id=uid, message_id=query.message.message_id, text=text)


def deserialize_to_date(date_str):
    date_dict = {}
    if len(date_str) >= 4:
        date_dict['year1'] = int(date_str[:4])
    if len(date_str) >= 6:
        date_dict['month1'] = int(date_str[4:6])
    if len(date_str) >= 8:
        date_dict['day1'] = int(date_str[6:8])
    if len(date_str) >= 12:
        date_dict['year2'] = int(date_str[8:12])
    if len(date_str) >= 14:
        date_dict['month2'] = int(date_str[12:14])
    if len(date_str) >= 16:
        date_dict['day2'] = int(date_str[14:16])
    return date_dict

@bot.callback_query_handler(func=lambda query: json.loads(query.data).get('type') == 'prd')
def handle_period(query):
    uid = query.message.chat.id
    mid = query.message.message_id
    lc = get_lang_code(uid)
    curr = get_curr(uid)
    table = get_costs_table(uid,curr)
    raw_data  = json.loads(query.data)
    selector = raw_data['sl']
    markup = types.InlineKeyboardMarkup(row_width=2)
    erase_data = {}

    if selector == 'y1s' or selector == 'y2s':
        if selector == 'y1s':
            data = {'type': 'prd', 'sl': 'y1e', 'd' : str()}
            text = languageMessages.period_sum_up[selector][lc]  # new line, do the same with next lines
            begin_str = str()
        else:

            data = raw_data
            data['sl'] = 'y2e'
            year = deserialize_to_date(data.get('d')).get('year1')
            month = deserialize_to_date(data.get('d')).get('month1')
            day = deserialize_to_date(data.get('d')).get('day1')
            erase_data = {'type': 'prd', 'sl': 'm1s', 'd' : data.get('d')[0:6]}
            text = languageMessages.period_sum_up[selector][lc].format(year=year,
                                                                       month=month,
                                                                       day=day) # I stopped here
            begin_str = data.get('d')
        years = list()
        for year, in conn.execute(sa.select([table.c.year])):
            if year not in years:
                years.append(year)
                data['d'] += str(year)
                markup.add(types.InlineKeyboardButton(text=year, callback_data=json.dumps(data)))
                data['d'] = begin_str

        if selector=='y2s':
            markup.add(types.InlineKeyboardButton(text=languageMessages.erase_text[lc],
                                                        callback_data=json.dumps(erase_data)))
        task = bot.edit_message_text(chat_id=uid,
                                     message_id=mid,
                                     text=text,
                                     reply_markup=markup)
        task.wait()
    elif selector == 'y1e' or selector== 'y2e':
        markup.row_width = 3
        markup_list = list()

        if selector == 'y1e':
            year = deserialize_to_date(json.loads(query.data).get('d')).get('year1')
            erase_data = {'type': 'prd', 'sl': 'y1s'}
            month_data = {'type': 'prd', 'sl': 'm1s', 'd': str(year)}
            text = languageMessages.period_sum_up[selector][lc].format(year=year)
            begin_str=str(year)

        else:
            data = json.loads(query.data)
            year = deserialize_to_date(raw_data.get('d')).get('year1')
            month = deserialize_to_date(raw_data.get('d')).get('month1')
            day = deserialize_to_date(raw_data.get('d')).get('day1')
            year1 = deserialize_to_date(raw_data.get('d')).get('year2')
            erase_data = {'type': 'prd', 'sl': 'y2s', 'd' : raw_data.get('d')[0:8]}
            month_data = json.loads(query.data)
            month_data['sl'] = 'm2s'
            begin_str = raw_data.get('d')
            text = languageMessages.period_sum_up[selector][lc].format(year=year,
                                                                       month=month,
                                                                       day=day,
                                                                       year2=year1) # I stopped here
            year = year1

        months = list()
        for month, in conn.execute(sa.select([table.c.month]).where(table.c.year == year)):
            if month not in months:
                months.append(month)
                if(len(str(month)) < 2):
                    month_str = '0'+str(month)
                    month_data['d']+=month_str
                else:
                    month_data['d'] += str(month)
                markup_list.append(types.InlineKeyboardButton(text=languageMessages.months_text[lc][month-1],
                                                      callback_data=json.dumps(month_data)))
                month_data['d']=begin_str #reset month

        markup_list.append(types.InlineKeyboardButton(text=languageMessages.erase_text[lc],
                                                        callback_data=json.dumps(erase_data)))
        markup.add(*markup_list)
        task = bot.edit_message_text(text=text,
                                     chat_id=uid,
                                     message_id=mid,
                                     reply_markup=markup)
        task.wait()
    elif selector == 'm1s' or selector == 'm2s':
        markup.row_width = 7
        markup_list = list()
        raw_data = json.loads(query.data).get('d')


        if selector == 'm1s':
            year = deserialize_to_date(raw_data).get('year1')
            month = deserialize_to_date(raw_data).get('month1')
            erase_data = {'type': 'prd', 'sl': 'y1e', 'd': str(year)}
            day_data = {'type': 'prd', 'sl': 'y2s', 'd': raw_data}
            text = languageMessages.period_sum_up[selector][lc].format(year=year,month=month)

        else:
            year = deserialize_to_date(raw_data).get('year1')
            month = deserialize_to_date(raw_data).get('month1')
            day = deserialize_to_date(raw_data).get('day1')
            year1 = deserialize_to_date(raw_data).get('year2')
            month1 = deserialize_to_date(raw_data).get('month2')
            erase_data = {'type': 'prd', 'sl': 'y2e', 'd': raw_data[0:12]}
            day_data ={'type': 'prdfnl', 'd': raw_data}
            text =languageMessages.period_sum_up[selector][lc].format(year=year,
                                                                      month=month,
                                                                      day=day,
                                                                      year2=year1,
                                                                      month2=month1)

        days = list()
        for day, in conn.execute(sa.select([table.c.day]).where(sa.and_(table.c.year == year, table.c.month == month))):
            if day not in days:
                days.append(day)
                if len(str(day)) < 2:
                    day_str = '0' + str(day)
                    day_data['d'] += day_str
                else:
                    day_data['d'] += str(day)
                markup_list.append(types.InlineKeyboardButton(text=str(day),
                                                              callback_data=json.dumps(day_data)))
                day_data['d'] = raw_data

        markup_list.append(types.InlineKeyboardButton(text=languageMessages.erase_text[lc],
                                                      callback_data=json.dumps(erase_data)))

        markup.add(*markup_list)



        task = bot.edit_message_text(text=text,
                                     chat_id=uid,
                                     message_id=mid,
                                     reply_markup=markup)
        task.wait()



@bot.callback_query_handler(func=lambda query: json.loads(query.data).get('type') == 'prdfnl')
def handle_period_final(query):
    uid = query.message.chat.id
    mid = query.message.message_id
    lc = get_lang_code(uid)
    curr = get_curr(uid)

    raw_data = json.loads(query.data).get('d')
    year1 = deserialize_to_date(raw_data).get('year1')
    month1 = deserialize_to_date(raw_data).get('month1')
    day1 = deserialize_to_date(raw_data).get('day1')
    year2 = deserialize_to_date(raw_data).get('year2')
    month2 = deserialize_to_date(raw_data).get('month2')
    day2 = deserialize_to_date(raw_data).get('day2')


    final_strings = list()

    task = bot.edit_message_text(text='Handling...',
                                 chat_id=uid,
                                 message_id=mid)

    meta.reflect(bind=conn)
    table = meta.tables['id_{curr}_{id}'.format(curr=curr, id=uid)]

    costs_list = [dict(year=year, month=month, day=day, amount=amount, purchase_type=purchase_type)
                  for year, month, day, amount, purchase_type in conn.execute(sa.select([table.c.year, table.c.month, table.c.day, table.c.amount, table.c.purchase_type]).where(sa.and_(sa.and_(sa.and_(table.c.year>=year1,
                                                                                                                               table.c.year<=year2),
                                                                                                                       sa.and_(table.c.month>=month1,
                                                                                                                               table.c.month<=month2)),
                                                                                                               sa.and_(table.c.day>=day1,
                                                                                                                       table.c.day<=day2)))).fetchall()]

    total_amount = total_cost(costs_list)
    purchase_types_list = get_users_types(uid=uid)

    for ptype in purchase_types_list:
        shared_amount = type_cost(costs_list=costs_list, type_name=ptype)
        percent = get_percent(total_amount, shared_amount)
        percent_string = '{0:<0.2f}'.format(percent) + '%'
        amount_string = '{0:<0.2f}'.format(shared_amount) + curr.upper()

        ptype_text = ptype
        if languageMessages.locale_ptypes[lc].get(ptype) is not None:
            ptype_text = languageMessages.locale_ptypes[lc].get(ptype)

        final_strings.append('{0:<1s}➡{1:<5s}💰{2:<15s}\n\n'.format(ptype_text, percent_string, amount_string))

    total_amount_string = '{0:0.2f}'.format(total_amount) + curr.upper()
    last_str = '{0:<15s} {1:15s}'.format(languageMessages.total_button[lc], total_amount_string)
    final_strings.append(last_str)
    result = task.wait()

    first_date = str(day1)+ '.' + str(month1) + '.' + str(year1)
    second_date = str(day2) + '.' + str(month2) + '.' + str(year2)

    task = bot.edit_message_text(message_id=result.message_id, chat_id=result.chat.id,
                                 text=languageMessages.period_final[lc].format(date1=first_date,date2=second_date))
    task.wait()
    for s in final_strings:
        task = bot.send_message(chat_id=uid,text=s)
        task.wait()


@server.route('/'+TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://financepy.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
