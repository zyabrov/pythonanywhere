#Manychat
manychat_api_url = "https://api.manychat.com"
manychat_api_key = "Bearer 509996:4acf40aefc22ca693e6763f6b8d425ae"
manychat_setCustomFields_url = "/fb/subscriber/setCustomFields"
manychat_sendContentByUserRef = "/fb/sending/sendContentByUserRef"
manychat_sendFlow = "/fb/sending/sendFlow"
manychat_headers = {
      'Authorization': 'Bearer ' + manychat_api_key,
      'Content-Type': 'application/json'
    }

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

#telegram
token = '5700135657:AAFaZqtAqe2VGBoUi7qhPAlcwCF_W5iMBTk'