#!/usr/bin/python3

import os
import json
from flask import Flask
from flask import request

import requests

from state import KKboxState

from TelegramBot import TGbot

app = Flask(__name__)

global kkbox

@app.route('/', methods=['GET', 'POST'])
def openBot():
    res = json.loads(request.data.decode('utf-8'))
    print(res)
    state.checkUpdate(res)
    return 'hi'

if __name__  == '__main__':
    state = KKboxState()
    app.run()
