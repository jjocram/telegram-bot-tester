# telegram-bot-tester
A framework to automatize telegram bot testing, integrable in yours CI/CD

# About telegram-bot-tester
This framework was conceived to test how a telegram bot behave during conversation.

It works simulating a client (`FakeClient`) and a server (`FakeServer`).

FakeClient send messages (your tests) to FakeServer, your bot connect to FakeServer and retrieve message you sent, elaborate it adn send back the response to FakeServer. FakeServer send back bot response to FakeClient that can test it (for example with [PyTest](https://pypi.org/project/pytest/))

# How to test things
In this fast guide we assume that your bot is written with [python-telegram-bot](https://python-telegram-bot.org) and tested with [PyTest](https://pypi.org/project/pytest/)
1. Create a `test_bot.py` file
2. Instantiate a `Bot` object
    ```python
   from telegram-bot-tester.Model.bot_model import Bot
   test_bot = Bot(bot_id, bot_first_name, bot_username)
    ```
    bot_id, bot_first_name and bot_username can be retrieve at https://api.telegram.org/bot\<TOKEN>/getMe where \<TOKEN> is your bot's token
3. Instantiate at least one `User` object
    ```python
    from telegram-bot-tester.Model.user_model import User
    test_user = User(chat_id, user_first_name, user_last_name, username, language_code)
    ```
    chat_id is the only required argument to built an User object; user_first_name, user_last_name, username language_code are optionals but could be useful set them such that you can recognize them