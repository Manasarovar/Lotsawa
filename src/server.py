# -*- coding: utf-8 -*-

import sys
from array import *
import os
import copy
import pickle
import re
import io
import time
import xml.parsers.expat
import importlib
from src.bottle import *


global inputData
global GVectorDict
global Lotsawa

# init GUI
# _________________________________________________________________________________________

def serveFile(request, fileName):
    print('serveFile')
    res = ""
    report = ""
    for line in request.query:
        inputData[line] = request.query[line]

    ocrData = ""

    if 'ocrData' in inputData:
        ocrData = inputData['ocrData']

    with open(fileName, newline="\n", encoding='utf-8') as f:
        res = f.read()
        f.close()

    if(inputData['user'] == 'Lotsawa'):
        if (ocrData == ""):
            report = Lotsawa.printCatalog()
        else:
            report = getattr(Lotsawa, ocrData)()
        i = 1
        for line in report:
            # @@@PAGE_DATA{i}@@@ --> %Report_n()
            res = res.replace(f'%Report_{i}()', line)
            i += 1

    else:  # inputData['user']!='Lotsawa'
        index = ""
        field = ""
        if "index" in inputData:
            index = inputData['index']
        if "field" in inputData:
            field = inputData['field']
            
        if (ocrData == ""):
            report = GVectorDict.printCatalog()
        else:
            # выполняем функцию из модуля GVectorDict по имени функции в переменной ocrData
            report = getattr(GVectorDict, ocrData)()
        res = res.replace("@@@PAGE_DATA@@@", report)
        # формируем URL для кнопок интерфейса
        link = "/?ocrData=read&mode=read&index="+index+"&field="+field
        res = res.replace("@@@readPageLink@@@", link)
        link = "/?ocrData=TibetanUTFToEng&mode=read&index="+index+"&field="+field
        res = res.replace("@@@translatePageEngLink@@@", link)
        link = "/?ocrData=TibetanUTFToRus&mode=read&index="+index+"&field="+field
        res = res.replace("@@@translatePageRusLink@@@", link)

    inputData['ocrData'] = ""

    return res

# _________________________________________________________________________________________

def servePost(request):
    print('servePost')
    report = ""
    for line in request.json:
        inputData[line] = request.json[line]
        # Если меняем Юзера, то подгружаем соответствующую Базу
        if line == 'user':  # serveUser
            if request.json[line] == 'Lotsawa':
                inputData['dLotsawa'] = GVector.dictBase(inputData['pathDB']+"LOTSAWA_DICT")
            elif request.json[line] == 'OSBL':
                inputData['dk'] = GVector.dictBase(inputData['pathDB']+"MEMO_TRANSL")

    ocrData = inputData['ocrData']
    if (ocrData == None):
        report = "no ocrData"
    else:  # serveFunction
        # выполняем функцию из модуля GVectorDict | Lotsawa по имени функции в переменной ocrData
        if (inputData['user'] == 'Lotsawa'):
            report = getattr(Lotsawa, ocrData)()
        else:
            report = getattr(GVectorDict, ocrData)()
    ocrData = ""
    return report 
# _________________________________________________________________________________________

def startServer(inputData_, GVectorDict_, Lotsawa_):
    #print('startServer')
    global inputData
    inputData = inputData_
    global GVectorDict
    GVectorDict = GVectorDict_
    global Lotsawa
    Lotsawa = Lotsawa_

    pathGUI = inputData['pathGUI']
    pathApp = inputData['pathApp']

    # define socket server route
    @route('/', method=['GET', 'POST'])
    @route('/<user>')
    def index(user='Lotsawa'):  # user='Lotsawa' # 'OSBL'
        #print('index', user)
        inputData['user'] = user
        print('request', request)
        res_file = pathGUI+"lotsawa.html"
        if (user != 'Lotsawa'):
            res_file = pathGUI+"index.html"
        
        return serveFile(request, res_file)

    @route('/create/post.esp', method=['GET', 'POST'])
    def postRoute():
        print('postRoute')
        inputData['ocrData'] = None
        return servePost(request)

    @route('/_img/<fileName>')
    def server_static(fileName):
        return static_file(fileName, root=pathGUI+"_img")

    @route('/_js/<fileName>')
    def server_static(fileName):
        return static_file(fileName, root=pathGUI+"_js")

    @route('/_css/<fileName>')
    def server_static(fileName):
        return static_file(fileName, root=pathGUI + "_css")

    @route('/_font/<fileName>')
    def server_static(fileName):
        return static_file(fileName, root=pathGUI+"_font")

    print("Стартуйте интерфейс программы, открыв в браузере  URL http://localhost:4445")

    # start socket server
    run(host='localhost', port=4445, debug=True)
