from flask import Flask, request
import telebot
from credentials import bot_token, webhook_url
import time
import git

TOKEN = bot_token
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

@app.route('/git')
def git_request():
    if request.method == 'POST':
        repo = git.Repo('zyabrov/pythonanywhere')
        origin = repo.remotes.origin
        repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@bot.message_handler(commands=['start'])
def start(message):
    print("message:", message)
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    print(json_string)
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    # bot.remove_webhook()
    print("got new webhook")
    time.sleep(0.1)
    # bot.set_webhook(url=webhook_url)
    print("bot new updates")
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







"""
@app.route('/manychat/<method>', methods=['POST'])
def manychat(method):
    data = request.get_json()
    subscriber_id = data['id']
    if method == 'cabinet':
        # Кількість отриманих бонусів
        # Діючі купони (для особистого кабінету)
        # Всього балів
        # Кількість отриманих бонусів
        functions.cabinet(subscriber_id, data)
    elif method == 'get_tasks':
        # Доступні завдання (кількість)
        # Доступне завдання 1
        # Доступне завдання 2
        # Доступне завдання 3
        functions.get_tasks(subscriber_id,data)
    elif method == 'get_coupon':
         functions.get_coupon(subscriber_id, data)
    return 'ok'
    """

