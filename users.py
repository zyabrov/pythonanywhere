import config
from datetime import datetime
import functions
import db_functions as db

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
        query = db.GetRaw(self.table, 'id', self.user_id)
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
        db.InsertRaw(self.table, self.values)


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
        query = db.GetRaw(self.table, param, value)
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
            self.tasks = self.admin_data['tasks']
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
            db.InsertRaw(self.table, self.values)
            # change is admin in users table
            db.UpdateValue(User().table, 'id', self.user_id, 'is_admin', True)
            # create coupons table
            db.CreateTable(self.coupons_table, self.coupons_table_cols)
            # create users table
            db.CreateTable(self.subscribers_table, self.subscribers_table_cols)
            return True
        else:
            return False

    def update_admin_settings(self, parameter, value):
        db.UpdateValue(self.table, 'id', int(self.admin_id), parameter, value)


    def db_add_active_coupon(self, coupon_id, subscriber_id, coupon_enddate):
        values = [coupon_id, subscriber_id, coupon_enddate]
        db.InsertRaw(self.coupons_table, values)


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
        self.table = table
        query = db.GetRaw(self.table, 'manychat_id', self.manychat_id)
        self.db_data = query.data
        self.bonuses_quantity = int(self.db_data['bonuses_quantity'])
        self.active_coupons = self.db_data['active_coupons']
        self.points = int(self.db_data['points'])
        self.available_tasks = self.db_data['available_tasks']
        self.finished_tasks = self.db_data['finished_tasks']
        if self.active_coupons is None:
            self.active_coupons = 'Немає активних купонів'
        
    def get_active_coupons(self):
        if self.active_coupons is not None:
            # Перевіряємо, чи не вийшов термін дії кожного купону, формуємо новий список активних купонів
            current_time = self.manychat_data['last_seen']
            for coupon in self.active_coupons:
                coupon_endtime = coupon['coupon_endtime']
                if current_time < coupon_endtime:
                    self.active_coupons_checked.append(coupon)
            # перетворюємо список на string для передачі в Manychat
            self.coupons_active_string = self.active_coupons_string()
            return self.coupons_active_string


    def active_coupons_string(self):
        for coupon in self.active_coupons_checked:
            coupon_string = f"<b>{coupon['coupon_name']}</b>, діє до {coupon['coupon_endtime']}"
            if self.coupons_active_string is None:
                self.coupons_active_string = coupon_string
            else:
                self.coupons_active_string = self.coupons_active_string + "\n" + coupon_string
            return self.coupons_active_string


    def get_available_tasks(self, all_tasks):
        self.available_tasks = []
        for task in all_tasks:
            if task not in self.finished_tasks:
                self.available_tasks.append(task)
        self.available_tasks_string()
    

    def available_tasks_string(self):
        if self.available_tasks is not None:
            self.available_tasks_string = "<b>Доступні бонуси:</b>\n\n"
            for task in self.available_tasks:
                self.available_tasks_string = self.available_tasks_string + "\n" + task
        else:
            self.available_tasks_string = 'Немає доступних бонусів'
        return self.available_tasks_string

            
    def db_add_user(self):
        db.InsertRaw(self.table, self.table_values)
    
    def db_update_user(self, parameter, value):
        db.UpdateValue(self.table, 'user_id', int(self.user_id), parameter, value)

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

