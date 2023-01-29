import config
from datetime import datetime
import functions
import db_functions
from flask import request
import requests


class User:
    def __init__(self, id):
        self.user_id = id
        self.name = None
        self.telegram_username = None
        self.user_data = None
        self.user_category = None
        self.bot_startdate = None
        self.last_message = None
        self.ref_url = None
        self.refer = None
        self.is_admin = None
        self.points = None
        self.bonuses = None
        self.coupons = None
        self.table = config.UsersTable().table
        self.last_text_input = None
        self.last_action = None # datetime
        self.values = None

    def check_is_admin(self):
        self.check_user_category()
        if self.user_category == 'admin_active':
            self.is_admin = True
        else:
            self.is_admin = False

    def check_user_category(self):
        if self.user_data is None:
            user_category = 'non_admin'
        else:
            status = self.user_data['status']
            if status == 'active':
                user_category = 'admin_active'
            else:
                user_category = 'admin_non_active'
        return user_category

    def get_user_data(self, message):
        query = db_functions.GetRaw(self.table, 'id', self.user_id)
        self.user_data = query.data
        if self.user_data is not None:
            self.name = self.user_data['name']
            self.bot_startdate = self.user_data['bot_startdate']
            self.last_message = self.user_data['last_message']
            self.ref_url = self.user_data['ref_url']
            self.refer = self.user_data['refer']
            self.is_admin = self.user_data['is_admin']
            self.points = self.user_data['points']
            self.bonuses = self.user_data['bonuses']
            self.coupons = self.user_data['coupons']
            self.last_text_input = self.user_data['last_text_input']
            self.telegram_username = self.user_data['telegram_username']
            self.last_action = self.user_data['last_action']
        else:
            self.add_new_user(message)

    def add_new_user(self, message):
        self.name = message.from_user.first_name + ' ' + message.from_user.last_name
        self.telegram_username = message.from_user.username
        self.user_id = message.chat.id
        self.bot_startdate = datetime.now()
        self.last_action = datetime.now()
        self.is_admin = False
        self.values = [int(self.user_id), self.name, self.telegram_username, self.bot_startdate, None, message.text, self.ref_url, self.refer, self.is_admin, None, None, None, self.last_action]
        db_functions.InsertRaw(self.table, self.values)


class SuperAdmin:
    def __init__(self):
        self.user_id = '291651795'
        self.user_category = 'SuperAdmin'


class Admin(User):
    def __init__(self, id):
        super().__init__(id)
        self.template_installed = None
        self.bot_token = None
        self.activated_coupons = None
        self.admin_id = self.user_id
        self.end_date = None
        self.coupons = None
        self.status = None
        self.phone = None
        self.email = None
        self.manychat_id = None
        self.manychat_api = None
        self.last_payment_date = None
        self.start_date = None
        self.coupons_list = None
        self.coupons_list_dic = []
        self.coupon_data = None
        self.coupons_table = config.AdminCouponsTable(self.admin_id).table
        self.coupons_table_cols = config.AdminCouponsTable(self.admin_id).cols
        self.admin_data = None
        self.table = config.AdminsTable().table
        self.admin_table_cols = config.AdminsTable().cols
        self.subscribers_table = f"subscribers_{self.admin_id}"
        self.subscribers_table_cols = ['user_id', 'tg_id', 'tg_username', 'manychat_instagram', 'instagram_username', 'finished_tasks', 'active_tasks']
        self.products = None
        self.points_following = None
        self.points_comment = None
        self.points_stories = None
        self.bonuses_set_success = None
        self.values = []
        self.product_id = None
        self.product_template_url = None
        self.last_message = None


    def get_admin_data(self, param, value):
        query = db_functions.GetRaw(self.table, param, value)
        self.admin_data = query.data
        if self.admin_data is not None:
            self.status = self.admin_data['status']
            self.manychat_api = self.admin_data['manychat_api']
            self.start_date = self.admin_data['start_date']
            self.last_payment_date = self.admin_data['last_payment_date']
            self.end_date = self.admin_data['end_date']
            self.coupons = self.admin_data['coupons']
            self.activated_coupons = self.admin_data['activated_coupons']
            self.points_following = self.admin_data['points_following']
            self.points_comment = self.admin_data['points_comment']
            self.points_stories = self.admin_data['points_stories']
            self.bot_token = self.admin_data['bot_token']
            self.manychat_id = self.admin_data['manychat_id']
            self.product_id = self.admin_data['product_id']
            self.template_installed = self.admin_data['template_installed']
        else:
            print('admin not found')

    def db_add_admin(self, message, product_id):
        # check existence
        self.get_admin_data()
        self.product_id = product_id
        if self.admin_data is None:
            # add user_data to admins table
            self.admin_id = message.chat.id
            self.start_date = str(datetime.now())
            self.last_payment_date = str(datetime.now())  # пізніше змінити
            self.end_date = functions.add_days(self.start_date, 30)
            self.status = 'active'
            print(self.values)
            db_functions.InsertRaw(self.table, self.values)
            # change is admin in users table
            db_functions.UpdateValue(User().table, 'id', self.user_id, 'is_admin', True)
            # create coupons table
            db_functions.CreateTable(self.coupons_table, self.coupons_table_cols)
            # create users table
            db_functions.CreateTable(self.subscribers_table, self.subscribers_table_cols)
            return True
        else:
            return False

    def update_admin_settings(self, parameter, value):
        db_functions.UpdateValue(self.table, 'id', int(self.admin_id), parameter, value)


    def db_add_active_coupon(self, coupon_id, subscriber_id, coupon_enddate):
        values = [coupon_id, subscriber_id, coupon_enddate]
        db_functions.InsertRaw(self.coupons_table, values)


class Subscriber:
    def __init__(self, manychat_id) -> None:
        self.manychat_id = manychat_id
        self.admin_id = None
        self.manychat_data = None
        self.bonuses_quantity = None
        self.active_coupons = None
        self.active_coupons_checked = dict()
        self.points = None
        self.coupons_active_string = None
        self.available_tasks = []
        self.finished_tasks = []
        self.available_tasks_quantity = None
        self.available_tasks_string = None
        self.coupon_to_get = None
        self.coupon_to_get_name = None
        self.coupon_to_get_cost = None
        self.coupon_to_get_desc = None
        self.coupon_to_get_enddate = None
        self.coupon_to_get_id = None
        self.table = None
        self.table_cols = None
        self.table_values = [self.manychat_id, 0, None, 0, None]
        self.finished_tasks = []


        
    def get_db_data(self, table):
        query = db_functions.GetRaw(self.table, 'manychat_id', self.manychat_id)
        self.db_data = query.data
        if self.db_data is not None:
            self.bonuses_quantity = int(self.db_data['bonuses_quantity'])
            self.active_coupons = self.db_data['active_coupons']
            self.points = int(self.db_data['points'])
            self.available_tasks = self.db_data['available_tasks']
            self.finished_tasks = self.db_data['finished_tasks']
        else:
            self.db_add_user(self)
        if self.active_coupons is None:
            self.active_coupons = 'Немає активних купонів'
        else:
            # Перевіряємо, чи не вийшов термін дії кожного купону, формуємо новий список активних купонів
            self.check_active_coupons()
            # перетворюємо список на string для передачі в Manychat
            self.active_coupons_string()
        

    def check_active_coupons(self):
        current_time = self.manychat_data['last_seen']
        for coupon in self.active_coupons:
            coupon_endtime = coupon['coupon_endtime']
            if current_time < coupon_endtime:
                self.active_coupons_checked.append(coupon)


    def active_coupons_string(self):
        for coupon in self.active_coupons_checked:
            coupon_string = f"<b>{coupon['coupon_name']}</b>, діє до {coupon['coupon_endtime']}"
            if self.coupons_active_string is None:
                self.coupons_active_string = coupon_string
            else:
                self.coupons_active_string = self.coupons_active_string + "\n" + coupon_string
            return self.coupons_active_string

            
    def db_add_user(self):
        db_functions.InsertRaw(self.table, self.table_values)
    
    def db_update_user(self, parameter, value):
        db_functions.UpdateValue(self.table, 'user_id', int(self.user_id), parameter, value)

    def get_coupon_to_get_data(self, admin):
        self.coupon_to_get_data = admin.coupons[f'{self.coupon_name}']
        self.coupon_to_get_desc = self.coupon_to_get_data['coupon_desc']
        self.coupon_to_get_cost = self.coupon_to_get_data['coupon_cost']
        self.coupon_to_get_time = self.coupon_to_get_data['time']
        return self.coupon_to_get_data

    def set_coupon_to_get(self):
        self.coupon_to_get = {
            'coupon_id': self.coupon_to_get_id, 
            'coupon_name': self.coupon_to_get_name, 
            'coupon_сost': self.coupon_to_get_cost, 
            'coupon_desc': self.coupon_to_get_desc, 
            'coupon_enddate': self.coupon_to_get_enddate
            }
        self.active_coupons_checked.append(self.coupon_to_get)
        self.db_update_user('active_coupons', self.active_coupons_checked)

    def get_active_tasks(self):
        self.available_tasks = []
        for task in self.admin.tasks:
            if task not in self.finished_tasks:
                self.available_tasks.append(task)
        return self.available_tasks




class Product(Admin):
    def __init__(self, id, product_id):
        super().__init__(id)
        self.product_id = product_id
        self.product_data = None
        self.product_name = None
        self.product_description = None
        self.product_cost = None
        self.channels = None
        self.product_template_url = None

    def get(self):
        query = db_functions.GetRaw('products', id, self.product_id)
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
            self.action = db_functions.UpdateRaw(self.user_id, 'id', self.coupon_id, self.coupon_params)
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
            self.coupons_list = functions.string_to_list(self.coupons)
            coupons_values = ['coupon_i', 'coupon_name', 'coupon_cost', 'coupon_time', 'coupon_description']
            print(self.coupons_list)
            for coupon in self.coupons_list:
                self.coupon_data = functions.list_to_diclist(coupons_values, coupon)
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
        all_data = db_functions.get_admins()
        for admin_data in all_data:
            self.admins_list.append(admin_data)
            self.admins_list_string = self.admins_list_string.__add__(f'{admin_data} \n\n')

    def get_admins_id(self):
        self.get_all_data()
        for admin_data in self.admins_list:
            admin_id = admin_data[0]
            self.admins_id.append(admin_id)
            self.admins_id_string.__add__(admin_id + '\n')




class Manychat:
    def __init__(self, manychat_token) -> None:
        self.manychat_token = manychat_token
        self.manychat_api_url = 'https://' # get from manychat api docs
        self.manychat_headers = f'Autorization: Bearer {self.manychat_token}; Application: Json/' # get from manychat api docs
        self.user_id = None
        self.fields_to_change = None
        self.message = None
        self.url = None
        self.data = None
        self.status = None
        self.manychat_data = None

    def get_manychat_data(self):
        self.manychat_data = request.get_json()
        self.manychat_id = self.manychat_data['user_id']          

    def set_values(self, message=None):
        # The number of custom               fields is limited to 20 for one request.
        # Use field_id OR field_name to specify the field.
        self.message = message
        self.url = f"{self.manychat_api_url}/setCustomFields"
        self.data = {
        'subscriber_id': self.user_id,
        'fields': self.fields_to_change   
        }
        req_post = requests.post(self.url, json=self.data, headers=self.manychat_headers)
        print("manychat request: ", req_post.content, req_post.status_code, req_post.headers.items())
        if req_post.status_code == 200: 
            self.status = 'ok'
        else:
            self.status = 'error'
        response = {
        'status': self.status,
        'message': self.message,
        'fields_to_change': self.fields_to_change
        }
        self.fields_to_change = None
        return response

"""
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


"""



