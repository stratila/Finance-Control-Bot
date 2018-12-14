help= { }


start = {'en' : 'Hello! For more information press /help', 'ru' : 'Привет!'}  #first start

help1 = {'en': 'Just enter amount that you\'ve spent to see the results in the future.',
         'ru': 'Вводите сумму, которую вы потратили, чтобы увидеть результаты в будуещем.'}

help2 = {'en': 'If want to see your results, simply enter /sum_up. You\'ll see the different categories',
         'ru': 'Просто введите /sum_up, чтобы увидеть результаты. Вы увидите разные категории.'}

help3 = {'en': 'When you enter your amount, you\'re suggested to choose type of purchase. '
               'But you can enter your own type. To do it just click /add_purchase_type.',
         'ru': 'Вам предлагается ввести тип покупки после того, как вы введёте вашу сумму. '
               'Но вы также можете добавить свою. Для этого введите /add_purchase_type.'}

help4 = {'en': 'Don\'t speak English? It\'s not a problem. Just click /language to change it.',
         'ru': 'Не хотите использовать русский язык? Просто поменяйте командой /language'}

help5 = {'en': 'You have got a three different currencies. That means that you can switch '
               'between of them. Enter /currency to do it. It\'s as simple as that.',
         'ru': 'В вашем распоряжении имеется три различные валюты. Это значит, что вы можете переключаться'
               ' между ними по мере необходимости. /currency'}




start_used = {'en' : 'Welcome back!', 'ru' : 'Рад видеть тебя снова'}  # when user have already used bot

change_lang_ask = {'en' : 'Please, choose the language:', 'ru' : 'Пожалуйста, выберете язык:'}

change_lang_end = {'en' : 'Your language successfully changed to English!', 'ru': 'Язык интерфейса бота теперь – русский.'}

total_amount = {'en' : 'Your amount is {amount} {curr}.', 'ru': 'Ваша сумма составляет {amount} {curr}.'}

choose_type = {'en' : 'Please choose the type of purchase:', 'ru' : 'Выберете тип вашей покупки:'}

custom_purchase = {'en' : 'Custom', 'ru' : 'Свой'}

large_amount = {'en' : 'Your amount is too large. Please try to enter fewer numbers.',
                'ru' : 'Ваша сумма слишком велика. Попробуйте ввести число поменьше.'}

successful_added_amount = {'en' : 'The amount {amount} was added successfully to {ptype} category.',
                           'ru' : 'Сумма {amount} была добавлена в категорию {ptype}.'}

enter_type_of_purchase = {'en' : 'Please enter your own type of purchase:',
                          'ru' : 'Введите свой тип покупки:'}

successful_added_ptype = {'en' : 'Your purchase type \"{ptype}\" was added to your configuration.',
                          'ru' : 'Пользовательский тип покупки \"{ptype}\" был добавлен в вашу конфигурацию.'}

purchase_type_size_error = {'en': 'Your text too big. Please, try to enter a little bit fewer characters.'
                                 '\n➡/add_purchase_type',
                           'ru': "Текст слишком длинный. Попытайтесь ввести меньше символов или введите текст "
                                 "на английском."
                                 "\n➡/add_purchase_type"}

already_have_ptype = {'en' : 'We\'re sorry, but we already have a type \"{ptype}\".',
                      'ru' : 'У нас уже есть пользовательский тип \"{ptype}\".'}

locale_ptypes = {'en' : {'market' : 'Market',
                         'food' : 'Food',
                         'restaurants' : 'Restaurants',
                         'transport' : 'Transport',
                         'taxi' : 'Taxi',
                         'internet' : 'Internet',
                         'post' : 'Post',
                         'shopping' : 'Shopping'},

                 'ru' : {'market' : 'Рынок',
                         'food' : 'Продукты',
                         'restaurants' : 'Рестораны',
                         'transport' : 'Транспорт',
                         'taxi' : 'Такси',
                         'internet' : 'Интернет',
                         'post' : 'Почта и кацелярия',

                         'shopping' : 'Покупки'}

                 }


choose_currency = {'en': 'Choose the currency for your costs:',
                   'ru' : 'Выберете валюту для учёта ваших трат:'}


successful_change_currency = {'en' : 'The currency for your costs changed from {prev_curr} to {curr_curr}.',
                              'ru' : 'Валюта для учёта ваших трат изменена с {prev_curr} на {curr_curr}.'}


currencies = {'usd': '$ (United States Dollar)',
              'uah': '₴ (Українська гривня)',
              'rub': '₽ (Российский рубль)'}

already_have_curr = {'en': 'The currency {curr} is already used.',
                     'ru': 'Валюта {curr} уже используется.'}

summing_up = {'en': 'Summing up. Clarify the desired results:',
              'ru': 'Подведение итогов. Уточните желаемый результат:'}

total_button = {'en': 'Total', 'ru': 'Общая сумма'}

total_sum_up = {'en' : 'Costs for all time:\n', 'ru': 'Траты за всё время:\n'}

period_button = {'en' : 'Costs for a period.', 'ru': 'Траты за временной промежуток.'}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# сделать словарь с ключевыми значениями этапа выбора года, меняя год, месяц, день и добавляя заполнители
period_sum_up = {'y1s': {'en': 'Costs for a certain period. Choose a year:\n____.__.__ — ____.__.__',
                         'ru': 'Траты за определенный временной промежуток. Выберете год:\n____.__.__ — ____.__.__'},
                 'y2s': {'en': 'Costs for a certain period. Choose a year:\n{year}.{month}.{day} — ____.__.__',
                        'ru': 'Траты за определенный временной промежуток. Выберете год:\n{year}.{month}.{day} — ____.__.__'},

                 'y1e' : {'en': 'Costs for a certain period. Choose a month:\n{year}.__.__ — ____.__.__',
                          'ru': 'Траты за определенный временной промежуток. Выберете месяц:\n{year}.__.__ — ____.__.__'},

                 'y2e' : {'en': 'Costs for a certain period. Choose a month:\n{year}.{month}.{day} — {year2}.__.__',
                        'ru': 'Траты за определенный временной промежуток. Выберете месяц:\n{year}.{month}.{day} — {year2}.__.__'},

                 'm1s' : {'en': 'Costs for a certain period. Choose a day:\n{year}.{month}.__ — ____.__.__',
                         'ru': 'Траты за определенный временной промежуток. Выберете день:\n{year}.{month}.__ — ____.__.__'},
                 'm2s': {'en': 'Costs for a certain period. Choose a day:\n{year}.{month}.{day} — {year2}.{month2}.__',
                        'ru': 'Траты за определенный временной промежуток. Выберете день:\n{year}.{month}.{day} — {year2}.{month2}.__'}


                 }

months_text = {'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
         'ru': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']}

erase_text = {'en': '🔙 Erase', 'ru': '🔙 Стереть'}

period_final = {'en': 'Your costs from {date1} to {date2}',
                'ru': 'Ваши траты от {date1} до {date2}'}

clear_hist_succ = {'en': 'Your history successfully removed ',
                   'ru': 'Ваша история удалена.'}


