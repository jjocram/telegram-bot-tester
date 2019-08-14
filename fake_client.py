import requests
import json
from ast import literal_eval

from http.server import BaseHTTPRequestHandler, HTTPServer

from Model.bot_model import Bot
from Model.user_model import User
from Model.message_model import Message
from Model.callback_query_button_model import CallbackQueryButton

from os import environ


class ServerResponse:
    fake_server_response = {}

    def set_fakeServerResponse(self, r):
        self.fake_server_response = r


global fake_server_response
fake_server_response = ServerResponse()


class ReqeustHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        fake_server_response.set_fakeServerResponse(post_data.decode('utf-8'))  # <----- Save data

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


class FakeClient:

    def __init__(self, bot: Bot, user: User, server_address = ('', 8000)):
        self.bot = bot
        self.user = user

        if "token_tbt" not in environ:
            print("token_tbt not in environ")
            print("Look at 'instatiate fakeclient' in documentation")
            exit(1)

        self.fakeserver_url = "http://127.0.0.1:5000/" + environ["token_tbt"] + "/"

        # Handshake with fakeserver
        handshake_data = {
            "user": user.user_info()
        }

        r = requests.post(self.fakeserver_url + "handshake", json=json.dumps(handshake_data))
        if (json.loads(r.text))["status"] == "Ko":
            print("Failed handshake with fakeserver")
            exit(1)

        self.once_server = HTTPServer(server_address, ReqeustHandler)

    def send_message(self, message: Message):
        r = requests.post(self.fakeserver_url + "receiveMessage", json=json.dumps(message.get_message_info()))
        if (json.loads(r.text))["status"] == "Ko":
            print("Failed to send message to fakeserver")
            exit(1)

        self.once_server.handle_request()
        return literal_eval(fake_server_response.fake_server_response)

    def send_callback_query(self, callback_query: CallbackQueryButton):
        r = requests.post(self.fakeserver_url + "receiveMessage", json=json.dumps(callback_query.callback_query_button_info()))
        if (json.loads(r.text))["status"] == "Ko":
            print("Failed to send callback_query to fakeserver")
            exit(1)

        self.once_server.handle_request()
        return literal_eval(fake_server_response.fake_server_response)
