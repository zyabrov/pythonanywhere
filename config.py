

#tasks
tasks_quantity = 3
task_1_name = "Підписка в Інстаграм"
task_2_name = "Коментар в Інстаграм"
task_3_name = "Сторіс в Інстаграм"
tasks_list = [task_1_name, task_2_name, task_3_name]

#coupons
coupons_quantity = 3

#admindata
database = 'loyaltybots'
db_admintable = 'our_clients'
db = "db/loyaltybots.db"

from datetime import datetime

class DBTable:
    def __init__(self):
        self.table = None
        self.cols = None


class AdminsTable(DBTable):
    def __init__(self):
        super().__init__()
        self.table = 'our_clients'
        self.cols = 'id, status, manychat_api, start_date, last_payment_date, end_date, coupons, activated_coupons, points_following, points_comment, points_stories, bot_token, manychat_id, products, template_installed'


class AdminCouponsTable(DBTable):
    def __init__(self, admin_id):
        super().__init__()
        self.table = 'coupons_' + str(admin_id)
        self.cols = 'id, user_id, start_date, end_date, status, activated_date, coupon_name, coupon_cost, bot_username, bot_url'


class UsersTable(DBTable):
    def __init__(self):
        super().__init__()
        self.table = 'users'
        self.cols = 'id, name, telegram_username, bot_startdate, last_message, last_text_input, ref_url, refer, is_admin, points, bonuses, coupons'


class Commands:
    def __init__(self):
        self.commands_list = ['start', 'coupon_activate', 'settings']
        self.commands_list_settings = ['change_coupons', 'change_points', 'change_manychat_api']
        self.commands_list_manual = ['start_manual']


current_time = datetime.utcnow()

manychat_ref_url = ''