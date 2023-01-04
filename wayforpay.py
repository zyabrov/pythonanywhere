from app import functions
import bot_functions
from adminbot import bot


# WayforPay

class PaymentResponse:
    def __init__(self, json_string):
        self.json_string = json_string
        order = functions.string_to_list(self.json_string)
        print(order)
        self.product = None
        self.orderReference = int(order['orderReference'])  # Унікальний номер замовлення в системі торговця
        self.amount = int(order['amount'])  # Сума замовлення
        self.currency = order['currency']  # Валюта замовлення (UAH)
        self.authCode = int(order['authCode'])  # Код авторизації - присвоюється банком
        self.email = order['email']  # email@mail.com
        self.phone = order['phone']  # Номер телефону платника +38063-333-33-33
        self.processingDate = order['processingDate']  # Дата процесування транзакції (UTC) 12345678
        self.transactionStatus = order['transactionStatus']  # статус транзакції (Approved)
        self.reason = order['reason']  # Причина відмови
        self.reasonCode = int(order['reasonCode'])  # Код відмови
        self.user_id = None
        self.user_data = None

    def check_payment_status(self):
        if self.transactionStatus == 'Approved':
            SuccessPayment(self.json_string)
        else:
            PaymentDeclined(self.json_string)


class SuccessPayment(PaymentResponse):
    def success_payment(self):
        print('Got payment: ', self.json_string)
        self.insert_payment_db()
        self.find_user()
        self.new_admin()
        self.admin_message()
        self.superadmin_message()

    def insert_payment_db(self):
        values = [self.orderReference, self.transactionStatus, self.processingDate, self.amount, self.product, self.phone, self.email]
        db_functions.db_insert_raw('payments', values)

    def find_user(self):
        self.user_data = db_functions.db_raw_select('our_clients', 'phone', self.phone)
        self.user_id = self.user_data['id']

    def new_admin(self):
        admin = bot_functions.Admin(self.user_id)
        admin.db_add_admin(self.user_data['name'], 'active', self.phone, self.email)

    def admin_message(self):
        text = 'Дякуємо за покупку'
        bot.send_message(self.user_id, text)

    def superadmin_message(self):
        superadmin_id = bot_functions.SuperAdmin().user_id
        text = 'Нова оплата'
        bot.send_message(superadmin_id, text)

    # Create New Payment in payments_db
    # Find User in our_clients_db
    # Create New Admin in our_clients_db with status 'active' (or update, if already exists)
    # Send message to admin
    # Send message to superadmin


class PaymentDeclined(PaymentResponse):
    def declined_payment(self):
        print('Payment declined. Error: ', self.reasonCode, 'Reason: ', self.reason)


class PaymentUrl:
    def __init__(self):
        self.instagram_template_url = 'https://secure.wayforpay.com/button/bef18e556c4b4'
