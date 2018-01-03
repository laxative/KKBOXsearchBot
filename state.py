#!/usr/bin/python3

import datetime

import urllib.request
from urllib.error import HTTPError, URLError

import urllib

import time
import os
import json
import requests

from transitions import State
from transitions.extensions import GraphMachine as Machine

from KKBOXparse import KKBOXparse
from TelegramBot import TGbot

class KKboxState(object):
    # member
    style = None
    date = None
    Type = None

    data = None

    # tgBOT
    bot = None

    # webparsing
    parse = None

    # keyboard setting for inline keyboard
    MusicStyle = [
            [
                {'text': 'Chinese', 'callback_data': 'Style:Chinese'},
                {'text': 'English', 'callback_data': 'Style:English'},
                {'text': 'Japanese', 'callback_data': 'Style:Japanese'}
                ],
            [
                {'text': 'Korean', 'callback_data': 'Style:Korean'},
                {'text': 'Taiwanese', 'callback_data': 'Style:Taiwanese'},
                {'text': 'Cantonese', 'callback_data': 'Style:Cantonese'}
                ]
            ]

    TypeChoice = [
            [
                {'text': 'newSong', 'callback_data': 'Type:new'},
                {'text': 'song', 'callback_data': 'Type:song' }
                ]
            ]

    # states
    states = [
            {'name': 'IDLE'},
            {'name': 'READY', 'on_enter': ['inlineKeyboard_method']},
            {'name': 'CHINESE'},
            {'name': 'ENGLISH'},
            {'name': 'JAPANESE'},
            {'name': 'KOREAN'},
            {'name': 'TAIWANESE'},
            {'name': 'CANTONESE'},
            {'name': 'TYPE', 'on_enter': ['inlineKeyboard_type']},
            {'name': 'DATE', 'on_enter': ['inlineKeyboard_date']},
            {'name': 'RESULT', 'on_enter': ['printResult']},
            {'name': 'MOREINFO', 'on_enter': ['inputRank']}
            ]

    # transitions
    transitions = [
            ['setup', 'IDLE', 'READY'],
            ['to_chinese', 'READY', 'CHINESE'],
            ['to_english', 'READY', 'ENGLISH'],
            ['to_japanese', 'READY', 'JAPANESE'],
            ['to_korean', 'READY', 'KOREAN'],
            ['to_taiwanese', 'READY', 'TAIWANESE'],
            ['to_cantonese','READY', 'CANTONESE'],
            ['to_type', ['READY', 'CHINESE', 'ENGLISH', 'JAPANESE', 'KOREAN', 'TAIWANESE', 'CANTONESE'], 'TYPE'],
            ['to_date', 'TYPE', 'DATE'],
            ['to_result', ['DATE', 'RESULT'], 'RESULT'],
            ['to_info', ['MOREINFO','RESULT'], 'MOREINFO'],
            ['reset', '*', 'READY']
        ]
    def __init__(self):
        machine = Machine(self, states=self.states, transitions=self.transitions, initial='IDLE', title='KKBOX search bot')
        self.get_graph().draw('state_diagram.png', prog='dot')
        # bot
        self.bot = TGbot(os.environ['TOKEN'])
        self.bot.setWebhook(os.environ['URL'])
        # parsing
        self.parse = KKBOXparse()
        print('init')

    def checkUpdate(self, res):
        if 'callback_query' in res:
            callback = res['callback_query']
            # get call back query data
            ID = callback['id']
            Data = callback['data']
            replyID = callback['message']['chat']['id']
            # split string
            dataSplit = Data.split(':')
            # member setting
            if dataSplit[0] == 'Date':
                self.date = dataSplit[1]
                self.to_result()
            elif dataSplit[0] == 'Style':
                self.style = dataSplit[1]
                self.to_type()
            elif dataSplit[0] == 'Type':
                self.Type = dataSplit[1]
                self.to_date()
        else:
            if res['message']['text'] == '/start':
                self.bot.getchatID(res)
                self.setup()
            elif res['message']['text'] == '/restart':
                self.bot.getchatID(res)
                self.reset()
            elif self.state == 'MOREINFO':
                index = int(res['message']['text'])
                searchdata = self.data[index-1]
                msg = 'Rank: ' + str(index) + '\nSong name: ' + searchdata[0] + '\nArtist: ' + searchdata[1] + '\nAlbum Name: ' + searchdata[2] + '\nPhoto url: ' + searchdata[3]
                self.bot.sendmessage(msg)
                self.to_info()

    def inlineKeyboard_method(self):
        self.bot.sendmessage('Welcome KKBOX song rank searching bot\n please select Style', self.MusicStyle)
    def inlineKeyboard_type(self):
        self.bot.sendmessage('Please select searching type', self.TypeChoice)
    def inlineKeyboard_date(self):
        dateChoice = []
        col = []
        # get pre 14 days
        for i in range(1,15):
            date = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            data = dict()
            data['text'] = date
            data['callback_data'] = 'Date:' + date
            col.append(data)
            if i is 7 or 14:
                dateChoice.append(col)
                col = []
        # sendmessage inlinekeyboard
        self.bot.sendmessage('Please select date', dateChoice)
    def printResult(self):
        self.data = self.parse.getData(self.Type, self.style, 'daily', self.date)
        # only print rank, artist, song
        result = ''
        index = 1
        for item in self.data:
            row = 'Rank ' + str(index) + ': ' + item[1] + ' - ' + item[0] + '\n'
            result = result + row
            index = index + 1
        self.bot.sendmessage(result)
        self.to_info()
    def inputRank(self):
        self.bot.sendmessage('Please input the rank that the song info you want to search\n(1 - 50)')


