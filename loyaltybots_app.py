from flask import Flask, request
import telebot
from credentials import bot_token, webhook_url
import time
import functions
import bot_functions
import users
from users import User, Subscriber, Admin, AdminsList, Manychat
import messages
import config
import db_functions


TOKEN = bot_token
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

"""
@app.route('/git')
def git_request():
    print ('Got git request')
    if request.method == 'POST':
        repo = git.Repo('./pythonanywhere')
        origin = repo.remotes.origin
        repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
    
"""


@bot.message_handler(commands=['start_admin'])
def start(message):
    print("message:", message)
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    message = call.message
    data = call.data
    print('call_data:', data)
    print(message)
    nav(message, data)


@bot.message_handler(func=lambda msg: msg.content_type == 'text')
def command_handler(message):
    print(message.text)
    data = message.text
    data = data.replace('/', '')
    print('command_data:', data)
    nav(message, data)


def nav(message, data):
    user = User()
    user.last_message = message
    if data == 'help':
        msg = messages.CommandsMessage()
        msg.message()
        send(message.chat.id, msg)
    else:
        # get user data
        user.get_user_data(message)
        print('user_data: ', user.user_data)
        if user.is_admin:
            user = Admin()
        print('user is admin:', isinstance(user, Admin))
        commands = config.Commands()
        if data in commands.commands_list:
            main_nav(message, data, user)
        elif data in commands.commands_list_manual:
            manual_nav(message, data, user)
        else:
            msg = None
            if data == '111':
                user.db_add_admin(message, product_id=0)
                msg = messages.NewAdmin(user)
            elif data == '222':
                admins = AdminsList()
                admins.get_all_data()
                msg = bot_functions.Message()
                text = admins.admins_list_string
                msg.text_input(text)
            user_id = user.user_id
            send(user_id, msg)


# different messages for admin and user
# different messages for active admin and non active admin


def main_nav(message, data, user):
    if data == 'start_admin':
        start(message, user)
    elif data == 'coupon_activate':
        coupon_activate(message, user)
    #elif data == 'settings':
        #settings_nav(message, data, user)


def manual_nav(message, data, admin):
    if data == 'start_manual':
        manual_start(message, admin)
    elif data == 'template_installed':
        manual_template_installed(message, admin)


def start(message, user):
    msg = messages.StartMessage()
    if user.is_admin:
        admin = Admin()
        print(isinstance(admin, Admin))
        msg.admin_message(admin.user_id, admin.status, admin.end_date)
    else:
        msg.user_message()
    # Send Message
    user_id = user.user_id
    send(user_id, msg)


def manual_start(message, admin):
    print(isinstance(admin, Admin))
    msg = messages.Manual()
    msg.start()
    user_id = admin.user_id
    send(user_id, msg)
    bot.register_next_step_handler(message, manual_get_manychat_api, admin)


def manual_get_manychat_api(message, admin):
    print(isinstance(admin, Admin))
    msg = messages.Manual()
    msg.start_answer(message.text)
    user_id = admin.user_id
    send(user_id, msg)
    bot.register_next_step_handler(message, manual_set_template, admin) # get manychat api


def manual_set_template(message, admin):
    print(isinstance(admin, Admin))
    admin.update_admin_settings('manychat_api', message.text)
    msg = messages.Manual()
    msg.set_template(product_template_url=admin.product_template_url)
    user_id = admin.user.id
    send(user_id, msg)


def manual_template_installed(message, admin):
    #перевірити, чи правильно налаштовано - написати слово Адмін
    msg = messages.Manual()
    msg.set_template_check()
    user_id = admin.user_id
    send(user_id, msg)

#Отримуємо manychat data Адміна
def get_admin_manychat_id(admin, manychat_data):
    manychat_id = manychat_data['user_id']
    admin.update_admin_settings('manychat_id', manychat_id)
    admin.update_admin_settings('template_installed', True)
    msg = messages.Manual()
    msg.template_success()
    user_id = admin.user_id
    send(user_id, msg)
    manual_bonuses(admin)


def manual_bonuses(admin):
    msg = messages.SetBonusPoints()
    user_id = admin.user_id
    send(user_id, msg)
    manual_get_points(admin)

def manual_get_points(admin):
    user_id = admin.user_id
    bonus = None
    admin.bonuses_set_success = False
    if admin.points_following is None:
        bonus = users.BonusFollowing()
    else:
        if admin.points_comment is None:
            bonus = users.BonusComment()
        else:
            if admin.points_stories is None:
                bonus = users.BonusStories()
            else:
                print('All bonuses are set')
                admin.bonuses_set_success = True
    if bonus.bonuses_set_success:
        msg = messages.SetBonusPoints()
        msg.success()
        send(user_id, msg)
        manual_get_coupon_data(admin)
    else:
        msg = messages.SetBonusPoints()
        msg.input(bonus.bonus_name)
        send(user_id, msg)
        # bot.register_next_step_handler(message, 'manual_set_points', admin, bonus, msg)
        message = admin.last_message
        print()
        bot.register_next_step_handler(message, 'manual_set_points', admin, bonus, msg)


def manual_set_points(message, admin, bonus, msg):
    print(bonus.bonus_name)
    bonus.bonus_update(message.text)
    msg.set(message.text)
    msg.answer_success()
    user_id = admin.user_id
    send(user_id, msg)
    manual_get_points(message, admin)


def manual_get_coupon_data(message, admin):
    user_id = admin.user_id
    msg = messages.SetCoupon()
    send(user_id, msg)
    msg.input_name()
    send(user_id, msg)
    # bot.register_next_step_handler(message, 'manual_set_coupon_name', admin, msg)
    bot.register_next_step_handler(message, manual_set_coupon_name, admin, msg)


def manual_set_coupon_name(message, admin, msg):
    user_id = admin.user_id
    coupon = users.Coupon()
    coupon.coupon_name = message.text
    msg.input_cost(coupon.coupon_name)
    send(user_id, msg)
    bot.register_next_step_handler(message, manual_set_coupon_cost, admin, msg, coupon)


def manual_set_coupon_cost(message, admin, msg, coupon):
    coupon.coupon_cost = message.text
    coupon.admin_coupon_data()
    admin.update_admin_settings('admin_coupons', coupon.admin_coupon_data)
    msg.success()
    user_id = admin.user_id
    send(user_id, msg)
    # bot.register_next_step_handler(message, 'get_bot_data', admin)
    bot.register_next_step_handler(message, get_bot_data, admin)


def get_bot_data(message, admin):
    user_id = admin.user_id
    msg = messages.SetAdminBotData()
    send(user_id, msg)
    # bot.register_next_step_handler(message, 'set_bot_data', admin, msg)
    bot.register_next_step_handler(message, set_bot_data, admin, msg)


def set_bot_data(message, admin, msg):
    user_id = admin.user_id
    adminbot = users.AdminBot(admin.admin_id)
    adminbot.bot_username = message.text
    adminbot.bot_url = f'https://t.me/{adminbot.bot_username}'
    admin.update_admin_settings('bot_username', adminbot.bot_username)
    admin.update_admin_settings('bot_url', adminbot.bot_url)
    msg.input_bot_data_success(admin.bot_username)
    send(user_id, msg)


def coupon_activate(message, admin):
    # get input from admin width coupon_id
    user_id = admin.user_id
    coupon = users.Coupon()
    msg = messages.CouponActivateMessage(coupon)
    send(user_id, msg)
    bot.register_next_step_handler(message, check_id, admin)


def settings(admin):
    msg = messages.AdminSettingsMessage()
    msg.message(admin.manychat_api, admin.coupons, admin.points)
    send(admin.user_id, msg)


def check_id(message, coupon):
    # get, check and activate coupon
    coupon.activate_coupon()
    # send message to admin
    msg = messages.CouponActivateMessage(coupon)
    send(message.chat.id, msg.admin_message())
    # send message to client
    send(coupon.client_id, msg.client_message_su8ccess())

"""
def settings_nav(data, admin):
    if data == 'change_coupons':
        coupons = admin.coupons_list()
        for coupon_data in coupons:
            msg = messages.ChangeCouponsMessage()
            msg.message(coupon_data)
            send(admin.user_id, msg)
    elif data == 'change_points':
        msg = messages.ChangePointsMessage()
    elif data == 'change_manychat_api':
        msg = messages.ChangeManychatApiMessage()
        msg.input()
        send(admin.user_id, msg)
        bot.register_next_step_handler(admin.last_message, set_api)
        settings_nav(admin.last_message, data, admin)


def set_api(admin_id, data):
  manychat_api_new = "Bearer " + data['custom_fields']['manychat_api']
  config.db.set_api(manychat_api_new, int(admin_id))
  fields_to_change = functions.add_field_to_change('manychat_api', manychat_api_new)
  response_message = 'Manychat Api змінено'
  return functions.manychat_response(admin_id, 'ok', fields_to_change, response_message)

"""
def send(user_id, msg):
    bot.send_message(user_id, msg.text, reply_markup=msg.markup, parse_mode='html', disable_notification=False)



@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    print(json_string)
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/api/<api_method>', methods=['POST', 'GET'])
def api_request(api_method):
    print('got request:', api_method)
    return "ok", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    print("clear old webhooks and set new")
    time.sleep(0.1)
    bot.set_webhook(url=webhook_url)
    return 'ok', 200


@app.route('/manychat/<manychat_token>/<method>', methods=['POST'])
def manychat_requence(manychat_token, method):
    manychat = Manychat(manychat_token)
    manychat.get_manychat_data()
    query = db_functions.GetRaw(config.db_admintable, 'manychat_api', manychat_token)
    admin = Admin(query.data['id'])
    admin.get_admin_data('id', admin.admin_id)
    user = Subscriber(manychat.user_id)
    user.get_db_data(admin.subscribers_table)
    user.manychat_data = manychat.manychat_data

    if method == 'cabinet':
        manychat.fields_to_change = functions.subscriber_cabinet(user)
        manychat.message = 'Дані отримано'
    elif method == 'get_tasks':
        manychat.fields_to_change = functions.get_tasks(user)
        manychat.message = ''
    elif method == 'get_coupon':
        functions.get_coupon(user, admin)
        manychat.message = 'Купон отримано'
    elif method == 'add_admin':
        manychat.fields_to_change = function.add_admin(user_id, data)
    response = manychat.set_values()
    print(response)
    return response