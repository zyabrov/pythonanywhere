from flask import Flask
import requests


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
        self.manychat_data = Flask.request.get_json()

    def get_manychat_value(self, field, iscustom=False):
        value = None
        if iscustom == True:
            value = self.manychat_data['custom_fields'][field]
        else:
            value = self.manychat_data[field]
        return value    

    def set_values(self, message=None):
        # The number of custom fields is limited to 20 for one request.
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
        self.response(self)

    def response(self):
        self.response = {
            'status': self.status,
            'message': self.message,
            'fields_to_change': self.fields_to_change
        }
        return self.response

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



