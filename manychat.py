from users import User

class Manychat(User):
    def __init__(self, manychat_id):
        super().__init__()
        self.manychat_id = manychat_id

    def send_message(self):
        pass
