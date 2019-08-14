from .user_model import User
from .message_model import Message


class CallbackQueryButton:

    def __init__(self, id, user: User, relative_message: Message, chat_instance, data):
        self.id = id
        self.sender = user.get_user_for_sender()
        self.message = relative_message.get_message_for_callback_query()
        self.chat_instance = chat_instance
        self.data = data

    def get_callback_query_button_info(self):
        callback_query_button_clicked = {
            "id": self.id,
            "from": self.sender,
            "message": self.message,
            "chat_instance": self.chat_instance,
            "data": self.data
        }
        return callback_query_button_clicked
