#!/usr/bin/python3

import requests
import json
import io

from KKBOXparse import KKBOXparse

from bs4 import BeautifulSoup

class TGbot:
    # member
    _api = 'https://api.telegram.org/bot'
    _token = None
    chat_id = None

    # parser
    parse = KKBOXparse()

    def __init__(self, token):
        self._token = token

    def getchatID(self, requestmsg):
        """bot get chat_id

        @param requestmsg: the request message
        @type  requestmsg: dict

        @return: chat_id

        """
        self.chat_id = requestmsg['message']['chat']['id']
        return self.chat_id

    def sendphoto(self, photopath):
        """bot send photo

        @param photopath: the photo path
        @type  photopath: string

        """
        ptr = open(photopath, 'rb')
        files = {
            'photo': ptr
        }
        data = {
            'chat_id': self.chat_id
        }
        msg = self._api + self._token + '/sendPhoto'
        return requests.post(msg, data=data, files=files)

    def sendmessage(self, message, inlineKeyBoard=None):
        """bot send message

        @param message: the message bot is going to send
        @return: request status

        """
        if inlineKeyBoard is None:
            data = {
                'chat_id': self.chat_id,
                'text': message
            }
        else:
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'reply_markup': {
                    'inline_keyboard': inlineKeyBoard
                    }
            }

        msg = self._api + self._token + '/sendMessage'
        return requests.post(msg, json=data)

    def setWebhook(self, url):

        """set webhook

        @param url: the url of ngrok
        @return: request status

        """
        data = {
            'url': url
        }
        msg = self._api + self._token + '/setWebhook'
        return requests.post(msg, json=data)
