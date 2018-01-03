"""@package KKBOXparse

the module for parsing KKBOX website content
"""

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup


class KKBOXparse:
    # set dictionary
    Type = {'new': 'newrelease', 'song': 'song', 'album': 'album'}
    MusicStyle = {'Chinese': '297', 'English': '390', 'Japanese': '308',
            'Korean': '314', 'Taiwanese': '304', 'Cantonese': '320', 'OST': '343',
            'Electric': '325', 'Hiphop': '324', 'R&B': '335', 'Rock': '13',
            'Other': '331', 'Jazz': '69', 'Spirit': '336', 'Classical': '349',
            'Country': '352', 'Reggae': '348', 'Crosstalk': '356'}
    Day = {'daily': 'daily', 'weekly': 'weekly'}
    getKey = ['\"song_name\"', "\"artist_name\"", "\"album_name\"", "\"normal\"", "\"release_date\""]

    def geturl(self, Type, style, day, date):
        """get website url we want to parse

        @param song: the key of dict songType
        @param language: the key of dict languageType
        @param day: the key of dict dayType
        @param date: the date wanted to parse

        @return: the url for request.get

        """

        return "https://kma.kkbox.com/charts/" + self.Day[day] + "/" + self.Type[Type] + "?cate=" + self.MusicStyle[style] + "&date=" + date

    def getAllscriptTag(self, url):
        """get the content of all script tag

        @param url: the url of the website we want to parse

        @return scriptlist: string that contain all contents of script tag

        """

        data = requests.get(url)
        soup = BeautifulSoup(data.text, "lxml")
        scriptlist = soup.select("script")
        return scriptlist

    def findscript(self, scriptlist, stringname):
        """find the context of script that contain the stringname we want

        @param scriptlist: the whole contents
        @param stringname: the thing we want to parse

        @return script.text: the string that contain content we want(stringname), if not, return None

        """

        for script in scriptlist:
            if(stringname in script.text):
                return script.text

        return None

    def findAllsubstring(self, string, toFind):
        """find all string key in script context and return all their value

        @param string: the whole script string
        @param toFind: the string we want to find in the whole script string

        @return array: array that contain all value of key we input(toFind)

        """
        array = []
        # if not found, jump out of while loop
        while string.find(toFind) is not -1:
            index = string.index(toFind)
            # "key": "value", find the index of ":" and ","
            # get the string start at the index of ":" + 1, end at the index of "," - 1
            start = string.index(":", index)+2
            end   = string.index(",", index)-1
            if toFind == '\"normal\"':
                end = end + 1
            # because it is utf8 string, we need to transfer it to big5
            toSearch = bytes(string[start:end], "utf-8").decode("unicode-escape", "ignore")
            # there are '\\' and a ',' in photo url, dealing with it
            if toFind == '\"normal\"':
                toSearch = toSearch.replace('\\', '')
                toSearch = toSearch + ',0v1/fit/160x160.jpg'
            array.append(toSearch)
            # replace one string once time
            string = string.replace(toFind, " ", 1)
        return array

    def getData(self, Type, style, day, date):
        """get data and sort them

        @param song: the key of dict songType
        @param language: the key of dict languageType
        @param day: the key of dict dayType
        @param date: the date wanted to parse

        @return data: array of sorting data

        """

        url = self.geturl(Type, style, day, date)
        scriptlist = self.getAllscriptTag(url)
        # temp array, need deal with after getting data
        temp = []
        for i in range(0, len(self.getKey)):
            script = self.findscript(scriptlist, self.getKey[i])
            temp.append(self.findAllsubstring(script, self.getKey[i]))

        # real data array
        data = []

        # deal with data
        for i in range(0,50):
            tmp = []
            for item in temp:
                tmp.append(item[i])
            data.append(tmp)

        return data

