# telegram-bot-tester
A framework to automatize telegram bot testing, integrable in yours CI/CD

# About telegram-bot-tester
This framework was conceived to test how a telegram bot behave during conversation.

It works simulating a client (`FakeClient`) and a server (`FakeServer`).

FakeClient send messages (your tests) to FakeServer, your bot connect to FakeServer and retrieve message you sent, elaborate it adn send back the response to FakeServer. FakeServer send back bot response to FakeClient that can test it (for example with [PyTest](https://pypi.org/project/pytest/))

# How to test things
In this fast guide we assume that your bot is written with [python-telegram-bot](https://python-telegram-bot.org) and tested with [PyTest](https://pypi.org/project/pytest/).

Please, read all points below before starting using it
1. Create a `test_bot.py` file
2. Instantiate a `Bot` object
    ```python
   from telegram-bot-tester.Model.bot_model import Bot
   test_bot = Bot(bot_id, bot_first_name, bot_username)
    ```
    bot_id, bot_first_name and bot_username can be retrieve at https://api.telegram.org/bot \<TOKEN>/getMe where \<TOKEN> is your bot's token
3. Instantiate at least one `User` object
    ```python
    from telegram-bot-tester.Model.user_model import User
    test_user = User(chat_id, user_first_name, user_last_name, username, language_code)
    ```
    chat_id is the only required argument to built an User object; user_first_name, user_last_name, username language_code are optionals but could be useful set them such that you can recognize them
4. Instantiate one FakeClient object
    ```python
    from telegram-bot-tester.fake_client import FakeClient
    fake_client = FakeClient(test_bot, test_user)
    ```
    test_bot and test_user are the same object instantiated in point 2 and 3
5. Create your first message
    ```python
    from telegram-bot-tester.Model.message_model import Message
    start_message = Message(message_id=123, test_user, test_bot, "/start")
    ```
    message_id is an arbitrary number, you can choose whatever you want
6. Send your first message and assert the response
    ```python
    bot_response = fake_client.send_message(start_message)
    assert bot_response["text"] == "This is the response for /start command"
    ```
7. Last requirements before testing:

    - You need some environmental variables to start to test things, you can use `export envName=envVal` to set them
    
        - token_tbt: your bot token
        - botId_tbt: your bot id (the same used in point 2)
        - botFirstName_tbt: your bot first name (the same used in point 2)
        - botUsername_tbt: your bot username (the same used in point 2)
    - Your bot needs to behave in a different way than usual; if you have used [python-telegram-bot](https://python-telegram-bot.org) you can follow this guide otherwise look in example directory
        
        - set another environmental variables(for example): `export TEST_TBT=1`
        - in your main bot script modify the behaviour when TEST_TBT is set
            ```python
            from sys import environ
            def main():
              .
              .
              .
              if "TEST_TBT" in environ:
                  updater = Updater(TOKEN, base_url="http://127.0.0.1:5000/")
                  bot = telegram.Bot(TOKEN, base_url="http://127.0.0.1:5000/")
              .
              .
              .
              if "TEST_TBT" in environ:
                  updater.start_polling(poll_interval=3.0)
            ```
            Note that you have to change base_url and set which where fake_server is running and you have to change the pulling time.
8. Start testing:
    To test you bot you need to run 3 process, its safer run them in only one command line 
    
    `python3 bot.py& ./fake_server.py& python3 test_bot.py`
    
    Note that bot.py and fake_server.py run in background; you can change `python3 test_bot.py` with your [PyTest](https://pypi.org/project/pytest/) run command