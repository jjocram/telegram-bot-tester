class User:

    """
        This class represent an user that use your bot.
        All information required to build an User object con be choose by you; consider that 'id' is equal to chat_id
    """

    def __init__(self, id, first_name="first_name", last_name="last_name", username="username", language_code="it"):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code


    def user_info(self):
        info = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "language_code": self.language_code
        }

        return info

    def user_info_for_sender(self):
        sender = {
            "id": self.id,
            "is_bot": False,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "language_code": self.language_code
        }

        return sender

    def user_info_for_chat(self):
        chat = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "type": "private"
        }

        return chat