class Bot:

    """
    This class represent your bot during test.
    All information required to build a Bot object are retrievable at: https://api.telegram.org/bot<TOKEN>/getMe
    """

    def __init__(self, id, first_name, username):
        self.id = id
        self.first_name = first_name
        self.username = username

    def bot_info(self):
        bot_info = {
            "id": self.id,
            "is_bot": True,
            "first_name": self.first_name,
            "username": self.username
        }

        return bot_info