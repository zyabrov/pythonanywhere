bot_token = "5809303804:AAFlJTthvlh0_HFu9ZRAv7g_yQ69eU9tMO8"
bot_user_name = "loyalty_adminbot"
webhook_url = f"https://ziabrov.pythonanywhere.com/{bot_token}"
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