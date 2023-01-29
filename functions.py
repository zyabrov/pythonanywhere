from datetime import datetime, timedelta
from flask import make_response
from datetime import datetime, date, timedelta
from random import randint
import db_functions as db
from users import User, Admin, Subscriber, Manychat


def add_days(start_date, time_delta):
  start_date = datetime.fromisoformat(start_date)
  date_end = start_date + timedelta(days=time_delta)
  date_end = date_end.strftime("%Y-%m-%dT%H:%M:%S")+"+03:00"
  return date_end


def integer_generation():
  return randint(100000,999999)


def string_to_list(string):
  return list(eval(string))


def auth_check(auth):
  admin_data = db.get_raw('manychat_api', str(auth))
  if admin_data != None:
      auth_message = {
         'auth': 'auth_ok',
         'status': str(admin_data['status']),
         'data': admin_data
      }
  else:
      auth_message = 'auth_declined'
  return auth_message


def list_to_diclist(names, list_to_change):
    return dict(zip(names, list_to_change))


def add_admin(admin_id, data):
  fields_to_change = []
  admin_data = db.get_admin('id', int(admin_id))
  print("admin_data:", admin_data)
  if admin_data is None:
      id = int(admin_id)
      name = str(data['name'])
      tg_id = int(data['custom_fields']['telegram id'])
      status = 'active'
      manychat_api = 'API не встановлено'
      start_date = str(data['last_seen'])
      last_payment_date = str(data['last_seen'])#пізніше змінити
      end_date = add_days(start_date, 30)
      coupons = 'Не налаштовані'
      coupons_activated = " "
      points = 'Не налаштовані'
      bot_token = 'Токен боту не встановлений'
      values = [id, name, tg_id, status, manychat_api, start_date, last_payment_date, end_date, coupons, coupons_activated, points, bot_token]
      print(values)
      db.insert_raw_our_clients(values)
      response_message = f'Додали нового адміна: {admin_id}'
      status = 'ok'
  else:
      response_message = 'Адмін вже є в базі'
      status = 'error'
  return manychat_response(admin_id, status, fields_to_change, response_message)
  

def get_coupon(user, admin):
  
  """
  Отримати значення з Manychat:
    ID користувача
    Купон на отримання
  Отримати значення з бази Адмінбота (по назві купону):
    Опис купону
    Термін дії купону на отримання (днів)
    Вартість купону на отримання
  Отримати значення з бази Підписників:
    Діючі купони (для особистого кабінету)
    Кількість балів
  Порахувати:
    Дата, до якої діє купон = Поточна дата + Термін дії купону
    Нова Кількість балів = Кількість балів - вартість купону
    ID отриманого купону
  Записати у базу Підписника:
    Нова Кількість балів
    Діючі купони
  Записати у базу Купонів (чи може у базу Підписнкика? Чи і туди, і туди): # user.active_coupons = [{'coupon_id': 234234, 'coupon_name': 'За підписку', 'coupon_сost': 200, 'coupon_desc': 'sdfsdfasf', 'coupon_endtime': '12.02.2023'}]
    ID отриманого купону
    ID користувача, який отримав
    Дата, до якої діє
  Передати значення полів у Manychat:
    # Діючі купони (для особистого кабінету)
    # Дата, до якої діє купон
    Термін дії купону на отримання (днів)
    Нова кількість балів
  """
  user.coupon_to_get_name = user.manychat_data['custom_fields']['Купон на отримання']
  user.get_coupon_to_get_data(user.coupon_to_get_name, admin)
  user.coupon_to_get_enddate = add_days(user.manychat_data['last_seen'], user.coupon_to_get_time)
  user.points = int(user.points) - int(user.coupon_to_get_cost)
  user.coupon_to_get_id = integer_generation()
  user.set_coupon_to_get()
  admin.db_add_active_coupon(admin.coupon_to_get_id, admin.user_id, admin.coupon_to_get_enddate)
  return 'ok'


def update_manychat_values(manychat_apikey):


  """fields_to_change = []
  points = data['custom_fields']['ПЛ - Всього балів']
  діючі_купони = (data['custom_fields']['Діючі купони (для особистого кабінету)'])
  coupon_data = data['custom_fields']['Купон на отримання']
  coupon_data_list = string_to_list(coupon_data)
  print(coupon_data_list)
  coupon_cost = coupon_data_list[1]  
  print(coupon_cost)
  coupon_name = coupon_data_list[0]
  coupon_start_date = data['last_seen']
  coupon_timedelta = int(coupon_data_list[2])
  coupon_description = coupon_data_list[3]
  points = int(points)-int(coupon_cost)
  сoupon_end_date = add_days(coupon_start_date, coupon_timedelta)
  coupon_id = integer_generation()
  fields_to_change = add_field_to_change("ПЛ - Всього балів", points)
  if діючі_купони == "➖" or діючі_купони == None:
      діючі_купони = f'{coupon_name} діє до {сoupon_end_date}'
  else:
      діючі_купони = f'{діючі_купони} \n{coupon_name} діє до {сoupon_end_date}'

  fields_to_change = add_field_to_change("Діючі купони (для особистого кабінету)", діючі_купони) 
  fields_to_change = add_field_to_change('Купон на отримання', coupon_name)
  fields_to_change = add_field_to_change('Дата, до якої діє купон', сoupon_end_date)     
  fields_to_change = add_field_to_change('Термін дії купону на отримання (днів)', coupon_timedelta) 
  coupons_quantity = config.coupons_quantity
  i = 1
  while i <= coupons_quantity:
    name = f'Діючий купон {i}'
    coupon = data['custom_fields'][name]
    if coupon == None:
      fields_to_change = add_field_to_change(name, coupon_name)
      fields_to_change = add_field_to_change(f'{name} (дата отримання)', coupon_start_date)
      fields_to_change = add_field_to_change(f'{name} (дата до)', сoupon_end_date)
      fields_to_change = add_field_to_change(f'{name} (опис)', coupon_description)   
      fields_to_change = add_field_to_change(f'{name} (ID)', coupon_id)      
      break    
    else: i=i+1
  r = manychat_setvalues(subscriber_id, fields_to_change)
  print (r)
  return r  
  """


def subscriber_cabinet(user):
      # Отримати значення з бази данних підписників адміна:
        # Кількість отриманих бонусів
        # Діючі купони (для особистого кабінету)
        # Всього балів
      # Передати значення в поля Manychat
  fields_to_change = [
    {'Кількість отриманих бонусів': user.bonuses_quantity},
    {'Діючі купони (для особистого кабінету)': user.coupons_active_string},
    {'Всього балів': user.points}
  ]
  return fields_to_change


def get_tasks(user):
    # Отримати доступні завдання з бази: всі завдання - виконані (list)
    # Передати значення полів у Manychat (string):
      # Доступні завдання (кількість)
      # Доступне завдання 1
      # Доступне завдання 2
      # ...
      # Доступне завдання i
      # ПЛ - Доступні бонуси (масив)
    user.get_active_tasks
    fields_to_change = [
    {'Доступні завдання (кількість)': user.bonuses_quantity},
    {'ПЛ - Доступні бонуси (масив)': user.coupons_active_string}
    ]
    for active_task in user.active_tasks:
      i += 1
      fields_to_change.append({f'Доступне завдання {i}': active_task})
    return fields_to_change

    """fields_to_change = []
    available_tasks = []
    all_tasks = config.tasks_list
    finished_tasks_string = data['custom_fields']['ПЛ - Отримані бонуси']
    finished_tasks_list = [finished_tasks_string]
    for i in range(len(all_tasks)):
        task = all_tasks[i]
        print(task)
        if task in finished_tasks_list:
            pass
        else:
            available_tasks.append(task)
    available_tasks_string = "".join([str(n)+"\n" for n in available_tasks]) 
    fields_to_change = add_field_to_change('ПЛ - Доступні бонуси (масив)', available_tasks_string)
    fields_to_change = add_field_to_change("Доступні завдання (кількість)", len(available_tasks))
    for i in range(len(available_tasks)):
        available_task = available_tasks[i]
        fields_to_change = add_field_to_change(f"Доступне завдання {i+1}", available_task)  
    r = manychat_setvalues(subscriber_id, fields_to_change)
    return r   


def add_field_to_change(field_name, field_value):
    global fields_to_change
    field = {
    'field_name': field_name,
    'field_value': field_value
    }
    fields_to_change.append(field)
    return fields_to_change


#-------------  
#manychat_functions
#-------------  
"""