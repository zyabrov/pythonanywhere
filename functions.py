from datetime import datetime, timedelta
from flask import make_response
from datetime import datetime, date, timedelta
import requests
from random import randint
import config
import db_functions as db
from users import User, Admin

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
  

def get_coupon(subscriber_id, data):
  fields_to_change = []
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


def user_cabinet(user, manychat_data, admin):
      # Встановити нові значення:
        # Кількість отриманих бонусів
        # Діючі купони (для особистого кабінету)
        # Всього балів
        # Кількість отриманих бонусів
  fields_to_change = []
  coupons = admin.coupons
  if coupons is not None:
    coupons_active_string = None
    for coupon in coupons:
      i += 1
      name = f'Діючий купон {i+1}'
      current_time = manychat_data['last_seen']
      end_time = manychat_data['custom_fields'][name + ' (дата до)']
      if current_time < end_time:
          if coupons_active_string == None:
              coupons_active_string = coupon
          else:
              coupons_active_string = coupons_active_string + "\n" + coupon
    fields_to_change = add_field_to_change('Діючі купони (для особистого кабінету)', coupons_active_string)  
  else: 
      fields_to_change = add_field_to_change('Діючі купони (для особистого кабінету)', "➖")     
  r = manychat_setvalues(subscriber_id, fields_to_change)
  return r   


def get_tasks(subscriber_id, data):
    fields_to_change = []
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

def manychat_setvalues(subscriber_id, fields_to_change):
#The number of custom fields is limited to 20 for one request.
# Use field_id OR field_name to specify the field.
    url = config.manychat_api_url+config.manychat_setCustomFields_url
    data = {
      'subscriber_id': subscriber_id,
      'fields': fields_to_change   
    }
    req_post = requests.post(url, json=data, headers=config.manychat_headers)
    print("manychat request: ", req_post.content, req_post.status_code, req_post.headers.items())
    return req_post


def manychat_response(subscriber_id, status, fields_to_change=None, message=None): 
    fields_to_change = add_field_to_change('response_status', status)
    fields_to_change = add_field_to_change('response_message', message)
    print(fields_to_change)
    mc_setvalues_res = manychat_setvalues(subscriber_id, fields_to_change)
    print('mc_setvalues_res:', mc_setvalues_res)
    if status != 'error' and mc_setvalues_res.status_code == 200: 
        status = 'ok'
    response = {
      'status': status,
      'message': message,
      'fields_to_change': fields_to_change
    }
    fields_to_change = None
    return response
  

def manychat_sendflow(subscriber_id, flow_ns, api_key):
    data = {
        "subscriber_id": subscriber_id,
        "flow_ns": flow_ns
    }
    url = config.manychat_api_url+config.manychat_sendFlow
    req_post = requests.post(url, json=data, headers=config.manychat_headers)
    print("manychat request: ", req_post.content, req_post.status_code, req_post.headers.items())
    return req_post


def manychat_sendmessage_resp(text, buttons=None, actions=None, quick_replies=None):
  data = {
      "tag": "ACCOUNT UPDATE",
      "version": "v2",
      "content": {
        "messages": [
          {
            "type": "text",
            "text": text,
            "buttons": buttons
          }],
      "actions": actions,
      "quick_replies": quick_replies
    }
  }
  return make_response(data)


def manychat_sendmessage(subscriber_id, text, buttons=None, actions=None, quick_replies=None):
  url = config.manychat_api_url+config.manychat_sendContentByUserRef
  headers = {
      'Authorization': 'Bearer ' + config.manychat_api_key,
      'Content-Type': 'application/json'
  }
  data = {
      "version": "v2",
      "content": {
          "messages": [
              {
                  "type": "text",
                  "text": text,
                  "buttons": buttons
                  }],
      "actions": actions,
      "quick_replies": quick_replies

  }
  }
  json = {
      "user_ref": int(subscriber_id),
      "data": data
      }  
  print(json)
  req_post = requests.post(url, json=json, headers=headers)
  return req_post