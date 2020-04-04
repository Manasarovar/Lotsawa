#  Open Source Buddhism Library  2020 www.buddism.ru.
#****************************************************************************
#  NAMO TASSA BHAGAVATO ARAHATO SAMMA SAMBUDDHASSA
#  May Buddha Dharma bring benefit and peace in all the world.
#****************************************************************************
#
# C- This software is subject to, and may be distributed under, the
# C- GNU General Public License, either Version 2 of the license,
# C- or (at your option) any later version. The license should have
# C- accompanied the software or you may obtain a copy of the license
# C- from the Free Software Foundation at http://www.fsf.org .

# -*- coding: utf-8 -*-

import os
import sys
import importlib

GVector=importlib.import_module("src.GVector")
server=importlib.import_module("src.server")
GVectorDict=importlib.import_module("src.GVectorDict")
Lotsawa=importlib.import_module("src.Lotsawa")


#объявляем inputData типа dict в котором инициализируются все глобальные переменные
inputData={}

#объявляем пользователя 
#inputData['user']='Lotsawa'
#inputData['user']='OSBL'


#создаем объект класса commandData в котором инициализируются все глобальные переменные
pathApp=os.path.dirname(__file__).replace('\\','/') +"/"	#путь к локальным файлам программы
print(pathApp)
inputData['pathApp']=pathApp						#путь к локальным файлам программы
inputData['pathDB']=pathApp+"DB_DATA/"				#путь к локальным файлам базы данных
inputData['pathGUI']=pathApp+"GUI/"					#путь к файлам главного интерфейса пользователя - GUI

#declare global database variables
inputData['dt']=None								#основной словарь	
inputData['dLotsawa']=None							#словарь Lotsawa	
inputData['dk']=None								#словарь памяти переводов
inputData['dBook']=None								#база данных текстов


#init dictionaries data base
inputData['dt']= GVector.dictBase(inputData['pathDB']+"MAIN_DICT")
inputData['dLotsawa']= GVector.dictBase(inputData['pathDB']+"LOTSAWA_DICT")
inputData['dk']= GVector.dictBase(inputData['pathDB']+"MEMO_TRANSL")

#init texts data base
inputData['dBook']= GVector.dictBase(inputData['pathDB']+"DHARMABOOK")

#init GVectorDict
GVectorDict.init(inputData)
#init Lotsawa
Lotsawa.init(inputData)

#start socket-server
server.startServer(inputData, GVectorDict, Lotsawa)

#пример словарного разбора без сокет сервера
#inputData['user_text']="བ་དག་གི་འབྲས་བུའི་མཆོག་མཐར་"
#inputData['mainMode']=GVector.TRANSLATE
#GVectorDict.dictReport()

#пример записи ключа в базу
#inputData['key']='རི་བོ་'
#inputData['db']='dk'
#inputData['value']='гора,холм4'
#GVectorDict.addWord()
#inputData['value']=''
#print (GVectorDict.getWord())

