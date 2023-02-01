from datetime import datetime, timedelta
from flask import make_response
from datetime import datetime, date, timedelta
from random import randint
import db_functions as db
from users import User, Admin, Subscriber, Manychat


class Product:
    def __init__(self, id, product_id):
        self.product_id = product_id
        self.product_data = None
        self.product_name = None
        self.product_description = None
        self.product_cost = None
        self.channels = None
        self.product_template_url = None

    def get(self):
        query = db.GetRaw('products', id, self.product_id)
        self.product_data = query.data
        self.product_name = self.product_data['product_name']
        self.product_description = self.product_data['product_description']
        self.product_cost = self.product_data['product_cost']
        self.channels = self.product_data['channels']
        self.product_template_url = self.product_data['template_url']
        return query.data


class AdminBonus:
    def __init__(self):
        self.bonus_id = None
        self.bonus_name = None
        self.bonus_points = None
        self.bonus_list = ['following', 'comment', 'stories' ]

    def bonus_update(self, points):
        self.bonus_points = points
        self.update_admin_settings(f'points_{self.bonus_id}', self.bonus_points)


class BonusFollowing(AdminBonus):
    def __init__(self):
        super().__init__()
        self.bonus_id = 'following'
        self.bonus_name = 'за Підписку в Інстаграм'

    def get_points(self):
        self.get_admin_data()
        self.bonus_points = self.points_following


class BonusComment(AdminBonus):
    def __init__(self):
        super().__init__()
        self.bonus_id = 'comment'
        self.bonus_name = 'за Коментар в Інстаграм'

    def get_points(self):
        self.get_admin_data()
        self.bonus_points = self.points_comment


class BonusStories(AdminBonus):
    def __init__(self):
        super().__init__()
        self.bonus_id = 'stories'
        self.bonus_name = 'за Cторіс в Інстаграм з відміткою @профіля бізнеса'

    def get_points(self):
        self.get_admin_data()
        self.bonus_points = self.points_stories


class Coupon:
    def __init__(self):
        self.coupon_id = None
        self.admin_coupon_data = None
        self.coupon_data = None
        self.coupon_status = None
        self.activate_date = None
        self.coupons_list = []
        self.coupons = None
        self.coupon_i = None
        self.coupon_name = None
        self.coupon_cost = None
        self.coupon_time = None
        self.coupon_description = None
        self.client_id = None
        self.coupon_user_id = None
        self.start_date = None
        self.end_date = None
        self.activated_date = None
        self.coupon_params = [self.coupon_id, self.coupon_user_id, self.start_date, self.end_date, self.status,
                              self.activated_date, self.coupon_name, self.coupon_cost]

    def db_data(self):
        self.coupon_id = self.coupon_data['id']
        self.coupon_user_id = self.coupon_data['user_id']
        self.start_date = self.coupon_data['start_date']
        self.end_date = self.coupon_data['end_date']
        self.activated_date = self.coupon_data['activated_date']
        self.coupon_name = self.coupon_data['coupon_name']
        self.coupon_cost = self.coupon_data['coupon_cost']

    def check_coupon(self, coupon_data):
        if coupon_data is None:
            self.coupon_status = 'not_found'
        else:
            self.coupon_status = self.coupon_data['status']

    def activate_coupon(self):
        self.get_data(self.coupon_id)
        if self.coupon_status == 'active':
            self.coupon_status = 'activated'
            self.activate_date = config.current_time
            self.action = db.UpdateRaw(self.user_id, 'id', self.coupon_id, self.coupon_params)
            self.query.execute()

    def admin_coupon_data(self):
        self.admin_coupon_data = {
                'coupon_name': self.coupon_name,
                'coupon_cost': self.coupon_cost
        }


class Coupons:
    def __init__(self, user_id):
        self.coupons_list_string = None
        self.coupons_list = None

    def coupons_list(self):
        if self.coupons != 'Не налаштовані':
            self.coupons_list = functions.string_to_list(self.coupons)
            print(self.coupons_list)
            i = 0
            for coupon in self.coupons_list:
                i += 1
                coupon_i = i
                coupon_name = coupon[0]
                coupon_cost = coupon[1]
                coupon_time = coupon[2]
                coupon_description = coupon[3]

    #def coupons_list(self):
        if self.coupons != 'Не налаштовані':
            self.coupons_list = string_to_list(self.coupons)
            coupons_values = ['coupon_i', 'coupon_name', 'coupon_cost', 'coupon_time', 'coupon_description']
            print(self.coupons_list)
            for coupon in self.coupons_list:
                self.coupon_data = list_to_diclist(coupons_values, coupon)
                self.coupons_list_dic.append(self.coupon_data)
            print('self.coupons_list_dic:', self.coupons_list_dic)
            return self.coupons_list_dic


class AdminBot:
    def __init__(self):
        self.bot_mainadmin = None
        self.bot_username= None
        self.bot_url = None
        self.bot_token = None
        self.bot_botfather_message = None


class AdminsList:
    def __init__(self):
        self.admins_list = []
        self.admins_list_string = 'All data: \n\n'
        self.admins_id = []
        self.admins_id_string = 'All admins id \n\n'

    def get_all_data(self):
        all_data = db.get_admins()
        for admin_data in all_data:
            self.admins_list.append(admin_data)
            self.admins_list_string = self.admins_list_string.__add__(f'{admin_data} \n\n')

    def get_admins_id(self):
        self.get_all_data()
        for admin_data in self.admins_list:
            admin_id = admin_data[0]
            self.admins_id.append(admin_id)
            self.admins_id_string.__add__(admin_id + '\n')

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


def subscriber_cabinet(subscriber, manychat):
  # Перевіряємо активність купонів та формуємо список активних купонів
  subscriber.coupons_active_string = subscriber.get_active_coupons()
  # Setting list of new values for fields:
    # Кількість отриманих бонусів
    # Діючі купони (для особистого кабінету) - перед цим перевірити, чи не пройшов термін дії для кожного купону
    # Всього балів
  manychat.fields_to_change = [
      {'Кількість отриманих бонусів': subscriber.bonuses_quantity},
      {'Діючі купони (для особистого кабінету)': subscriber.coupons_active_string},
      {'Всього балів': subscriber.points}
    ]
  # Setting the message to Subscriber to send in Manychat
  manychat.message = ''
  return manychat.fields_to_change, manychat.message


def get_tasks(subscriber, manychat, admin):
    # Передати значення полів у Manychat (string):
      # Доступні завдання (кількість)
      # Доступне завдання 1
      # Доступне завдання 2
      # ...
      # Доступне завдання i
      # ПЛ - Доступні бонуси (масив)
    subscriber.get_active_tasks(admin)
    fields_to_change = [
    {'Доступні завдання (кількість)': user.bonuses_quantity},
    {'ПЛ - Доступні бонуси (масив)': user.coupons_active_string}
    ]
    for active_task in user.active_tasks:
      
    return fields_to_change
