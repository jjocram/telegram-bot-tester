from flask import Flask, request
import json
import requests
import logging
from datetime import datetime

from os import environ
from sys import exit

from Model.bot_model import Bot
from Model.user_model import User
from Model.update_model import Update

if "token_tbt" not in environ:
    print("token_tbt not in environ")
    print("Look at 'start fakeserver' in documentation")
    exit(1)
TOKEN = "/" + environ["token_tbt"] + "/"

if "botId_tbt" not in environ:
    print("botId_tbt not in environ")
    print("Look at 'start fakeserver' in documentation")
    exit(1)

if "botFirstName_tbt" not in environ:
    print("botFirstName_tbt not in environ")
    print("Look at 'start fakeserver' in documentation")
    exit(1)

if "botUsername_tbt" not in environ:
    print("botUsername_tbt not in environ")
    print("Look at 'start fakeserver' in documentation")
    exit(1)

global bot
bot = Bot(environ["botId_tbt"], environ["botFirstName_tbt"], environ["botUsername_tbt"])

global user
user = User(1234)

global update
update = Update()

app = Flask(__name__)


# Connection with fakeclient
@app.route(TOKEN + "handshake", methods=['GET', 'POST'])
def handshake():
    try:
        data = json.loads(request.json)
        j_user = data["user"]

        user.id = j_user["id"]
        user.first_name = j_user["first_name"]
        user.last_name = j_user["last_name"]
        user.username = j_user["username"]
        user.language_code = j_user["language_code"]

        return {'status': 'Ok'}
    except:
        return {'status': 'Ko'}


@app.route(TOKEN + "receiveCallbackQuery", methods=['POST'])
def receiveCallBackQuery():
    try:
        update.appendQueryCallbackToResult(json.loads(request.get_json()))
        update.first_update = True
        return {'status': 'Ok'}
    except:
        return {'status': 'Ko'}

@app.route(TOKEN + "receiveMessage", methods=['POST'])
def receiveMessage():
    try:
        update.appendMessageToResult(json.loads(request.get_json()))
        update.first_update = True
        return {'status': 'Ok'}
    except:
        return {'status': 'Ko'}

# Connection with bot
@app.route(TOKEN + "deleteWebhook", methods=['GET', 'POST'])
def deleteWebhook():
    response = {"ok": True,
                "result": True,
                "description": "Webhook is already deleted"
                }
    return response


@app.route(TOKEN + "getMe", methods=['GET', 'POST'])
def getMe():
    response = {
        "ok": True,
        "result": bot.bot_info()
    }

    return response


@app.route(TOKEN + "getUpdates", methods=['GET', 'POST'])
def getUpdates():
    res = update.sendUpdate()
    if update.first_update:
        update.first_update = False
    else:
        update.popResults()

    return res


@app.route(TOKEN + "sendMessage", methods=['GET', 'POST'])
def sendMessage():
    response = {
        "ok": True,
        "result": {
            "message_id": 25,
            "from": bot.bot_info(),
            "chat": user.user_info_for_chat(),
            "date": datetime.timestamp(datetime.now()),
            "text": json.loads(request.data.decode('utf-8'))["text"]
        }
    }
    try:
        requests.post("http://127.0.0.1:8000", request.data)
    except:
        print("Exception while sending response to fakeclient")
    return response


@app.route(TOKEN + "editMessageText", methods=['GET', 'POST'])
def editMessageText():
    # print(request.data.decode('utf-8'))
    # Bootstrap
    response = {
        "ok": True,
        "result": {
            "message_id": 25,
            "from": bot.bot_info(),
            "chat": user.user_info_for_chat(),
            "date": datetime.timestamp(datetime.now()),
            "text": json.loads(request.data.decode('utf-8'))["text"]
        }
    }

    return response


if __name__ == '__main__':
    app.run()