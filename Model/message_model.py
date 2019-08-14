from .user_model import User
from .bot_model import Bot
from .inline_keyboard_model import InlineKeyboard

from datetime import datetime


class Message:

    def __init__(self, message_id, user: User, bot: Bot, text, inline_keyboards=[],
                 date=datetime.timestamp(datetime.now())):
        self.message_id = message_id
        self.user = user
        self.bot = bot
        self.date = date
        self.text = text

        self.inline_keyboards: [InlineKeyboard] = []
        for inline_keyboard in inline_keyboards:
            self.inline_keyboards.append(inline_keyboard.inline_keyborad_info)

        self.entities = None
        if text[0] == '/':
            self.entities = [
                {
                    "offset": 0,
                    "length": len(text),
                    "type": "bot_command"
                }
            ]

    def get_message_info(self):
        message = {
            "message_id": self.message_id,
            "from": self.user.user_info_for_sender(),
            "chat": self.user.user_info_for_chat(),
            "date": self.date,
            "text": self.text
            # "entities": self.entities
        }
        if self.entities:
            message["entities"] = self.entities

        return message

    def get_message_for_callback_query(self):
        message = {
            "message_id": self.message_id,
            "from": self.bot.bot_info(),
            "chat": self.user.user_info_for_chat(),
            "date": self.date,
            "text": self.text,  # non è lo stesso text
            "reply_markup": {
                "inline_keyboard": [self.inline_keyboards]
            }
        }

        return message
