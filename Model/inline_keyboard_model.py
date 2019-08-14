class InlineKeyboard:

    def __init__(self, text, callback_data):
        self.text = text,
        self.callback_data = callback_data

    def inline_keyborad_info(self):
        inline_keyboard = {
            "text": self.text,
            "callback_data": self.callback_data
        }

        return inline_keyboard