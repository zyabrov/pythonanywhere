from flask import Flask, request
import telebot
from credentials import bot_token, webhook_url
import time
import functions
from users import User, Subscriber, Admin
import config
import db_functions
from adminbot import Adminbot
from manychat import Manychat


TOKEN = bot_token
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
adminbot = Adminbot(bot)

"""

# ----------------
# Git AutoPulling (doesn't work)
# ----------------

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

# ----------------
# AdminBotHandlers
# ----------------


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    message = call.message
    data = call.data
    print('call_data:', data)
    print(message)
    adminbot.nav(message, data)


@bot.message_handler(func=lambda msg: msg.content_type == 'text')
def command_handler(message):
    print(message.text)
    data = message.text
    data = data.replace('/', '')
    print('command_data:', data)    
    adminbot.nav(message, data)



# ----------------
# AdminBotServerRequests
# ----------------


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


# ----------------
# ManychatRequests
# ----------------


@app.route('/manychat/<manychat_token>/<method>', methods=['POST'])
def manychat_requence(manychat_token, method):
    # geting request's ManychatData
    manychat = Manychat(manychat_token)
    manychat.get_manychat_data()

    # getting current Admin and AdminBotData
    query = db_functions.GetRaw(config.db_admintable, 'manychat_api', manychat_token)
    admin = Admin(query.data['id'])
    admin.get_admin_data('id', admin.admin_id)

    # setting ManychatData to Subscriber
    subscriber = Subscriber(manychat.get_manychat_value('id'))
    subscriber.manychat_data = manychat.manychat_data

    # getting SubscriberData from AdminDB or adding new Subscriber to AdminDB
    subscriber.get_db_data(admin.subscribers_table)
    if subscriber.db_data is None:
        subscriber.db_add_user()
    
    # navigation
    if method == 'cabinet':
        # Перевіряємо активність купонів та формуємо список активних купонів
        subscriber.get_active_coupons()
        # Setting list of new values for fields:
        manychat.fields_to_change = [
            {'Кількість отриманих бонусів': subscriber.bonuses_quantity},
            {'Діючі купони (для особистого кабінету)': subscriber.coupons_active_string},
            {'Всього балів': subscriber.points}
            ]
        # Setting the message to Subscriber to send in Manychat
        manychat.message = ''

    elif method == 'get_tasks':
        # Формуємо список невиконаних завдань (всі завдання з таблиці Адмінбота мінус виконані)
        subscriber.get_available_tasks(admin.tasks)
        if subscriber.available_tasks is not None:
            manychat.fields_to_change = [
                {'Доступні завдання (кількість)': len(subscriber.available_tasks)},
                {'ПЛ - Доступні бонуси (масив)': subscriber.available_tasks_string}
                        i += 1
        fields_to_change.append({f'Доступне завдання {i}': active_task})
            ]
        else:
            manychat.fields_to_change = [
                {'Доступні завдання (кількість)': 0},
                {'ПЛ - Доступні бонуси (масив)': subscriber.available_tasks_string}
            ]
        


        manychat.message = ''

    elif method == 'get_coupon':
        get_coupon(user, admin)
        manychat.message = 'Купон отримано'

    elif method == 'add_admin':
        manychat.fields_to_change = function.add_admin(user.user_id, data)

    # post Subscriber's changed fields to Manychat
    manychat.set_values(fields_to_change=manychat.fields_to_change, message=manychat.message)
    print(manychat.response)
    return manychat.response

    subscriber.get_active_tasks(admin)
    manychat.fields_to_change = [
        {'Доступні завдання (кількість)': subscriber.bonuses_quantity},
        {'ПЛ - Доступні бонуси (масив)': subscriber.coupons_active_string}
    ]
    for active_task in user.active_tasks:
      i += 1
      fields_to_change.append({f'Доступне завдання {i}': active_task})
    return fields_to_change
