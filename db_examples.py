from datetime import datetime, date, timedelta
import time
import sqlite3 as sql
import sqlalchemy
import random

purchase_types = ['food','market','clothes','internet', 'other']


def create_table():
    conn = sqlalchemy.create_engine('sqlite:///de.db')
    meta = sqlalchemy.MetaData()

    table_num = random.randint(0,10000) # random user's ID for example
    table = sqlalchemy.Table('id{number}'.format(number=table_num),meta,
                             sqlalchemy.Column('year',sqlalchemy.Integer),
                             sqlalchemy.Column('month',sqlalchemy.Integer),
                             sqlalchemy.Column('day',sqlalchemy.Integer),
                             sqlalchemy.Column('amount',sqlalchemy.Float),
                             sqlalchemy.Column('purchaseType',sqlalchemy.String))
    meta.create_all(conn)

    #filling a table
    begin_date = date(2012,1,1)
    one_day = timedelta(days=1)
    for i in range(0,365):
        temp_date = begin_date+i*one_day
        conn.execute(table.insert((temp_date.year, temp_date.month, temp_date.day,
                                   random.randint(0,10000), random.choice(purchase_types))))

def select_table():
    conn = sqlalchemy.create_engine('sqlite:///de.db')
    meta = sqlalchemy.MetaData()
    meta.reflect(bind=conn)

    table = meta.tables['id4669'] #user's ID should be pasted here

    result = conn.execute(table.select())
    "conn.execute(table.select(table.c.amount).where( sqlalchemy.and_(table.c.month == 2,table.c.purchaseType == 'food')))"
    years = []
    months = []
    for y, m, d, a, t in result:
        if not y in years:
            years.append(y)
        if not m in months:
            months.append(m)

    print('years: ', years)
    print('month: ', months)

    result = conn.execute(sqlalchemy.select([table.c.day]).where(table.c.month == 2))
    days = []
    for d, in result:
        days.append(d)
    print('days: ', days)









def create_db():
    conn = sql.connect('C:\\Users\\Bogdan\\Desktop\\de.db', detect_types = sql.PARSE_DECLTYPES)
    curs = conn.cursor()

    '''curs.execute('CREATE TABLE expenses ( year INT, \
                  month INT, day INT, amount DOUBLE, purchaseType VARCHAR(30))')
    for i in range(0,2):
       for j in range (0,4):
           for k in range(0,15):
               curs.execute('SELECT COUNT(*) FROM expenses')
               result, = curs.fetchone()

               today = date.today()+timedelta(days=k)
               year = today.year +i
               month = today.month+j
               day = today.day
               amount = random.randint(0,10000)
               ptype = random.choice(purchase_types)
               curs.execute('INSERT INTO expenses ( year, month, day, amount, purchaseType)  \
                             VALUES ( ?, ?, ?, ?, ?)',
                           (year,month,day,amount,ptype))'''

    curs.execute('SELECT amount FROM expenses WHERE year = 2019 AND month =7 AND purchaseType = "internet "')
    result = curs.fetchall()
    for amount, in result:
        print(amount)




    conn.commit()
    curs.close()
    conn.close()


