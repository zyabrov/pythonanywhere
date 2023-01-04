import config
from config import Commands
from telebot import types


class Message:
    def __init__(self):
        self.markup = None
        self.text = None
        self.action = None
        self.nextdef = None
        self.fieldname = None
        self.obj = None


    def text_input(self, text):
        self.text = str(text)
        return self.text


class StartMessage(Message):
    def admin_message(self, user_id, user_status, end_date):
        self.text = f'Ваш ID: {user_id}\nСтатус: {user_status} до {end_date}'
        btn1 = types.InlineKeyboardButton('Активувати купон', callback_data='сoupon_activate')
        btn2 = types.InlineKeyboardButton('Налаштування', callback_data='settings')
        btn3 = types.InlineKeyboardButton('Особистий кабінет', callback_data='cabinet')
        btn4 = types.InlineKeyboardButton('Тех. підтримка', callback_data='support')
        markup = types.InlineKeyboardMarkup(row_width=2)
        self.markup = markup.add(btn1, btn2, btn3, btn4)
        self.action = 'send'

    def user_message(self):
        self.text = f'Hello User'
        btn1 = types.InlineKeyboardButton('Сплатити', callback_data='pay')
        markup = types.InlineKeyboardMarkup(row_width=2)
        self.markup = markup.add(btn1)
        self.action = 'send'




class CouponActivateMessage(Message):
    def __init__(self, coupon):
        super().__init__()
        self.coupon_status = None
        self.coupon_end_date = None
        self.coupon = coupon

    def get_coupon_data(self):
        self.coupon_status = self.coupon.coupon_status
        self.coupon_end_date = self.coupon.end_date

    def input(self):
        self.text = 'Напишіть номер купону (6 цифр)'
        self.action = 'input'

    def admin_message(self):
        if self.coupon_status == 'active':
            self.text = 'Купон активовано'
        elif self.coupon_status == 'activated':
            self.text = 'Купон вже використовувався'
        elif self.coupon_status == 'expired':
            self.text = f'Закінчився термін дії купону \n(діяв до {self.coupon_end_date})'
        elif self.coupon_status is None:
            self.text = 'Такий купон не знайдено у базі'
        self.markup = None
        self.action = 'send'

    def client_message_success(self):
        self.text = 'Купон активовано'
        self.markup = None
        self.action = 'send'


class AdminSettingsMessage(Message):
    def __init__(self, manychat_api, coupons, bonuses):
        super().__init__()
        self.text = f'<b>Manychat API: </b>{manychat_api} \n\n<b>Купони: </b>\n<i>(назва - вартість у балах - термін дії)</i>\n{coupons}\n\n<b>Бонуси:</b>\n{bonuses}\n\n<b><i>Що ви хочете налаштувати або змінити?</i></b>'
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Купони', callback_data='change_coupons')
        btn2 = types.InlineKeyboardButton('Бали', callback_data='change_points')
        btn3 = types.InlineKeyboardButton('Manychat API', callback_data='change_manychat_api')
        btn4 = types.InlineKeyboardButton('Назад', callback_data='start')
        self.markup = markup.add(btn1, btn2, btn3, btn4)
        self.action = 'send'


class ChangeCouponsMessage(Message):
    def message(self, coupon_data):
        coupon_name = coupon_data['coupon_name']
        coupon_cost = coupon_data['coupon_cos']
        coupon_time = coupon_data['coupon_time']
        coupon_description = coupon_data['coupon_description']
        coupon_i = coupon_data['coupon_i']
        coupon_info = f'<b>🆎 Назва</b>: {coupon_name}\n<b>💰 Вартість у балах:</b> {coupon_cost}\n<b>📆 - Термін дії:</b> {coupon_time} днів\n<b>ℹ️ Опис:</b> {coupon_description}'
        self.text = coupon_info + "\n\n➖➖➖➖➖➖\n<i><b>Змінити:</b>\n🆎 - назву, 💰 - вартість у балах, 📆 - термін дії, ℹ - опис, 🗑 - видалити</i>"
        markup = types.InlineKeyboardMarkup(row_width=5)
        btn1 = types.InlineKeyboardButton('🆎', callback_data='changecoupon_name_' + coupon_i)
        btn2 = types.InlineKeyboardButton('💰', callback_data=f'changecoupon_cost_' + coupon_i)
        btn3 = types.InlineKeyboardButton('📆', callback_data=f'changecoupon_time_' + coupon_i)
        btn4 = types.InlineKeyboardButton('ℹ', callback_data=f'changecoupon_description_' + coupon_i)
        btn5 = types.InlineKeyboardButton('🗑', callback_data=f'changecoupon_delete' + coupon_i)
        self.markup = markup.add(btn1, btn2, btn3, btn4, btn5)
        self.action = 'send'


class ChangePointsMessage(Message):
    pass


class SetManychatApiMessage(Message):
    def __init__(self):
        super().__init__()
        self.text = None
        self.action = None

    def input(self):
        self.text = '<b>Пришліть код Manychat API</b>\nДля цього зайдіть в налаштування Manychat, у розділ API та скопіюйте код (або спочатку згенеруйте, якщо поле пусте)'
        self.action = 'input'

    def check(self, bot_url):
        self.text = f'<b>Напишіть слово "Адмін" своєму боту {bot_url}</b>'


    def success(self):
        self.text = 'Manychat API встановлено'
        self.action = 'send'


class AdminCabinet(Message):
    pass


class NewAdmin(Message):
    def __init__(self, user):
        super().__init__()
        if user.status:
            self.text = 'Вітаю, новий Адміне\nЯ допоможу тобі налаштувати твій Чатбот Лояльності.\n<b><i>Тисни кнопку Почати</i></b>'
            btn1 = types.InlineKeyboardButton('Почати', callback_data='start_manual')
            markup = types.InlineKeyboardMarkup(row_width=2)
            self.markup = markup.add(btn1)
        else:
            self.text = 'admin is already exists in db'
        self.action = 'send'




class Manual(Message):
    def __init__(self):
        super().__init__()
        self.text = None
        self.markup = None

    def start(self):
        self.text = '<b>Як хочеш приєднати Чатбот Лояльності?</b>\n\nВибери варіант:\n<b><i>1 - Cворити новий бот\n2 - Приєднати до існуючого боту в Manychat'
        self.markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Створити новий')
        btn2 = types.InlineKeyboardButton('Приєднати до існуючого')
        self.markup.add(btn1, btn2)

    def start_answer(self, answer):
        self.markup = None
        self.text = None
        if answer == 'Створити новий':  # ще не зареєстрований
            self.text = f'Тоді зроби ці кроки:\n\n1. Зареєструйся в Manychat за посиланням: {config.manychat_ref_url}, або увійди, якщо вже зареєстрований\n2. Свори новий проект та активуй для нього Pro-акаунт (необхідно для роботи шаблону, перші 7+ діб безкоштовно).\n3. Зайди в Налаштунки(Settings) Manychat -> розділ API та скопіюй API-ключ (згенеруй код, якщо поле пусте)\n\n<b><i>4. Відправ мені скопійований API-ключ</i></b>'

        elif answer == 'Приєднати до існуючого': # приєднати до існуючого боту
            self.text = 'Ок. Тоді зайди в Налаштунки Manychat -> розділ API та скопіюй API-ключ (згенеруй, якщо поле пусте)\n<b><i>Відправ мені скопійований API-ключ</i></b>'

    def set_template(self, product_template_url):
        self.text = f'✅ Manychat API встановлено\n\n1. Тепер установи шаблон за посиланням:\n{product_template_url}\n\n<b>2. Як закінчиш установку шаблону, тисни кнопку "Шаблон встановлено"'
        self.markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Шаблон встановлено', callback_data='template_installed')
        self.markup.add(btn1)

    def set_template_check(self):
        self.text = 'Ок. Давай перевіримо, чи все правильно працює.\n\nДля цього перейди у свій бот та <b>відправ йому слово <i>Адмін</i></b>'


    def template_success(self):
        self.text = 'Вітаю! Шаблон встановлено успішно.'



class SetAdminBotData(Message):
    def __init__(self):
        super().__init__()
        self.text = f"Відправ Псевдонім твого боту (без @, наприклад, loyaltybots_bot).\nЗнайти його можеш або у профілі самого боту (в інфо), або у @BotFather (у повідомленні, коли створювавав бот)"

    def input_bot_data_success(self, bot_username):
        self.text = f"Бот @{bot_username} підключено"



class SetBonusPoints(Message):
    def __init__(self):
        super().__init__()
        self.text = 'Тепер давай налаштуємо кількість балів за кожну Інстаграм-дію.'
        self.bonus_name = None
        self.bonus_points = None

    def input(self, bonus_name):
        self.bonus_name = bonus_name
        self.text = f'Скільки балів нараховуємо <b>{bonus_name}</b>?\n(напиши тільки число цифрами)'

    def set(self, bonus_points):
        self.bonus_points = bonus_points

    def answer_success(self):
        self.text = f'{self.bonus_name} встановлено {self.bonus_points} балів'

    def success(self):
        self.text = 'Бали за Інстаграм-дії встановлено'


class SetCoupon(Message):
    def __init__(self):
        super().__init__()
        self.text = 'Тепер давайте налаштуємо хоча б 1 купон'
        self.coupon_name = None
        self.coupon_cost = None

    def input_name(self):
        self.text = '<b>Вкажіть назву купону</b>\n(наприклад, Купон100, Купон30%, Кава)'

    def input_cost(self):
        self.text = f'<b>Напишіть необхідну кількість балів для отримання купону {self.coupon_name}</b>'

    def success(self):
        self.text = f'Купон {self.coupon_name} налаштовано\nЗмінити та додати купони ви зможете потім в Особистому кабінеті після закінчення базового налаштування боту'
        self.button_name = 'Зрозуміло'
        self.button_callback = ''





class Keyboard:
    def __init__(self, row_width):
        self.row_width = row_width
        self.markup = None


class Button:
    def __init__(self, btn_text, btn_url, btn_callback_data):
        self.btn_text = btn_text
        self.btn_url = btn_url
        self.btn_callback_data = btn_callback_data
        self.button = None


class InlineButton(Button):
    def button(self):
        self.button = types.InlineKeyboardButton(self.btn_text, url=self.btn_url, callback_data=self.btn_callback_data)


class KeyboardBack(Keyboard):
    pass


class MainMenu:
    def __init__(self):
        pass


class SendMessage(Message):
    pass

class UserInput(SendMessage):
    pass


class CommandsMessage(Message):
    def message(self):
        self.text = Commands().commands_list


class CommandsMessageSettings(Message):
    def message(self):
        text = Commands()
        self.text = text.commands_list
