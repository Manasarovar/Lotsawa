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

from src.GVector import *

global inputData

# declare global database variables
global dt  # основной словарь
global dk  # словарь памяти переводов
global dBook  # база данных текстов
global dLotsawa  # рабочая База


# _________________________________________________________________________________________

def init(inputData_):
    print('init')
    global inputData
    global dt  # основной словарь
    global dk  # словарь памяти переводов
    global dBook  # база данных текстов
    global dLotsawa  # рабочая База
    inputData = inputData_
    #dt = inputData['dt']
    dLotsawa = inputData['dLotsawa']
    dBook = inputData['dBook']
    dk = inputData['dk']
    dt = inputData['dt']

# _________________________________________________________________________________________


def printCatalog():
    print('printCatalog')
    global dBook
    lines = dBook.keyList
    report = "<h3>Каталог Текстов</h3>"

    for line in lines:
        report += '<a href="/?ocrData=TibetanUTFToRus&index=' + \
            str(dBook.dictKey[line]) + '&field=0" class="books_list" target="">' + \
            line + '</a><br/>\n'
    #print('report ', report)
    return [report]
# _________________________________________________________________________________________


def read():
    print("read")
    '''
    Текстовые файлы из DHARMABOOK размещаются в БД db их можно запрашивать из Питона постранично.
    Фомат вызова из Питона в функции def read():

    Формат вызова из JavaScript
    http://localhost:4443/?index=(номер текста)&field=(номер страницы)&ocrData=read
    '''
    global dBook
    index = int(inputData['index'])
    field = int(inputData['field'])
    #text = dBook.vData.getStr(index)

    print(inputData['bostr'])
    if('bostr' in inputData and inputData['bostr'] != ''):
        text = inputData['bostr']
        #print(text)
        inputData['bostr'] = ''
    else:
        text = dBook.vData.getStr(index)

    if ':|:' in text:
        #text = re.sub(r'.*:\|:', '', text, 0, re.MULTILINE)
        text = text[text.index(':|:')+3:]
    #print('index ',index)
    l = len(text)
    start = field*PAGE_SIZE
    if(start >= l):
        start = 0
    end = start + PAGE_SIZE
    if(end >= l):
        end = l-1

    #print("FIELD:"+str(field) + " start:"+ str(start) + " end:"+ str(end)+ " l:"+ str(l))
    # передвигаем начало страницы в начало предложения
    limit = 0
    if(start != 0):
        limit = 0
        while (text[start+limit] != " "):
            limit += 1
            if (limit == 256 or limit == l-1):
                limit = 0
                break
    start += limit

    # передвигаем конец страницы в начало предложения
    limit = 0
    while (text[end+limit] != " "):
        limit += 1
        if (limit == 256 or limit == l-1):
            limit = 0
            break
    end += limit

    page = text[start:end]

    #print("page: "+page)

    return page
# _________________________________________________________________________________________

def read_():
    print("read_")

    '''
    Текстовые файлы из DHARMABOOK размещаются в БД db их можно запрашивать из Питона постранично. 
    Фомат вызова из Питона в функции def read():
    Формат вызова из JavaScript 
    http://localhost:4443/?index=(номер текста)&field=(номер страницы)&ocrData=read
    '''
    global dBook
    PAGE_SIZE=1024
    
    index = inputData['index']
    #print(index)
    field = int(inputData['field'])

    path = inputData['pathDB']+'DHARMABOOK/TAB_DATA/!_User_String.txt'
    #with open(path, 'w', encoding='utf-8') as wf:
    #    wf.write(f'{str(inputData["key"])} ')

    #print(inputData['bostr'])
    if(index == 'usrBo'):
        text = inputData['usrTb']
        #print(text)
    #    #inputData['bostr'] = ''
    else:
        text = dBook.vData.getStr(int(index))

    if ':|:' in text:
        #text = re.sub(r'.*:\|:', '', text, 0, re.MULTILINE)
        text = text[text.index(':|:')+3:]
    #print('index ', index)
    len_txt = len(text)
    #print('len_txt', len_txt)
    start = field*PAGE_SIZE
    # Если весь текст влезает на 1 страницу
    start_idx = 0
    end_idx = len_txt

    if len_txt > PAGE_SIZE:
        if field == 0:
            end_idx = text.rfind(' ', 0, PAGE_SIZE)
        else:
            start_idx = text.rfind(' ', start - PAGE_SIZE, start)
            end_idx = text.rfind(' ', start_idx, start + PAGE_SIZE)

    #if start_idx == end_idx:  # >= len_txt:  # Текст закончен раньше
    #    return 'Text Finished'

    #print("FIELD:"+str(field) + " start:"+ str(start) + " end:"+ str(end)+ " l:"+ str(l))
    #print('start_idx ', start_idx, '\n', 'end_idx ', end_idx,)
    page = text[start_idx:end_idx]
    #print('page', page)


    return page
# _________________________________________________________________________________________


def input_strn(data):
    print("input_strn run")
    if '.txt' in data:
        with open(data, 'r', encoding='utf-8') as f:
            strn = f.read()
    elif '་' in data:
        strn = data
    else:
        print('введите тибетский текст')
        # strn=input()
    return strn

# _________________________________________________________________________________________

def format_txt(strn):
    print("format_txt run")
    strn += ' '

    strn = re.sub(f'༌', '་', strn, 0)
    strn = re.sub(r'[‘’]', "'", strn, 0)

    # подменяем '[' ']' '_' исходного форматирования
    strn = re.sub(r'\[(.+?)\]', r'-{\1}-', strn, 0)
    strn = re.sub(r'_', '-=-', strn, 0)

    strn = re.sub(r'([<\s\t]*)([\u0021-\u0171\t\u1E00-\u1EA1\s–—]+)([\u0021-\u0040\u005B-\u0060\u007B-\u00BF“”А-я–—\d\s\tА-я]+)',
                  r'\1\n<p lang="en">\2</p>\n<p lang="ru">\3</p>', strn, 0)

    # 0.Предложение ч1
    strn = re.sub(
        r'([༄༅\s\n\t༈།\u0021-\u0171\u1E00-\u1EA1“”А-я–—]*)(\S*[༔།/s]*)', r'\1@\2&', strn, 0)
    strn = re.sub(f'@&', '', strn, 0)

    # 0.1. Название
    strn = re.sub(r'([༄༅།\s@]+\S+?ལས[།༔]&)\s+(\S+?་བཞུགས\S*[།༔]*&)',
                  r'<h1 class="Toc">\1 \2</h1> <br>\n', strn, 0)

    # 0.2. Тема - подзаголовок
    strn = re.sub(
        r'(\S+?ནི[།༔]&)', r'\n<br><h4 class="Topic">\1</h4> <br>\n', strn, 0)

    # 0.3. Новая глава
    strn = re.sub(r'(༈)', r'\n\n<br><br>\1', strn, 0)

    # 0.4. Цитата до первого окончания
    strn = re.sub(r'([།])(\S+?ལས[༔།]+&)\s+(.+?[༔།་]*)\s([།]([@]ཞེས|ཅེས).+?[༔།&]+)',
                  r'\n<br><snt class="citeSrc">\1\2</snt> <div class="cite">\3</div> <br>\n\4<br>\n', strn, 0)

    # 0.4. Цитата продолжение
    strn = re.sub(r'([།]@(ཞེས|ཅེས).+?དང[༔།་]*&)(<br>\n)*\s*(.+?[༔།་&]*)\s([།]@(ཞེས|ཅེས).+?[༔།&]+)',
                  r'</div>\1 <div class="cite">\4</div> <br>\n\5<br>\n', strn, 0)

    # 0.5 Конец абзаца (заключающий помощник གོ ངོ དོ ནོ བོ མོ རོ ལོ སོ ཏོ после второго суффикса ད་; འོ་ - после слога без суффикса)
    strn = re.sub(
        f'((ག་གོ|ང་ངོ[་]*|ད་དོ|ན་ནོ|བ་བོ|མ་མོ|ར་རོ|ལ་ལོ|ས་སོ|ད་ཏོ|འོ)([༔།{1,2}&\s\t])+)[།\s]', r'\1<br><br>\n\n ', strn)
    strn = re.sub(
        f'(ག་གོ|ང་ངོ[་]*|ད་དོ|ན་ནོ|བ་བོ|མ་མོ|ར་རོ|ལ་ལོ|ས་སོ|ད་ཏོ)([༔།&\s\t])', r'\1#\2', strn)
    strn = re.sub(f'(འོ)([༔།&\s\t])', r'་\1#\2', strn)

    #  \\1-приставка    \\2-корневая         \\3-1й суффикс      \\4-2й суфф
    # ([ག|བ|ད|མ|འ]?)([\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ]+?)([ག|ང|ད|ན|བ|མ|འ|ར|ལ|ས]?)([ས|ད]?)

    # 0.6 Разделительные частицы - не выполняем
    # strn=re.sub(f'(་)(གི|ཀྱི|གྱི|ཡི|གིས|ཀྱིས|གྱིས|ཡིས|སུ|རུ|ཏུ|ན|ལ|དུ|ཏེ|དེ|སྟེ|དང|ཞིང|ཅིང|ཤིང|ཀྱང|ཡང)([་།༔&])', r'\1<a class="cc">\2</a>\3',strn)
    # strn=re.sub(f'(འི|འིས|འང|འམ)|འང([་།༔&])', r'<a class="cc">\1\2</a>',strn)

    # 0.7 Предложение ч2
    lst = strn.split('@')

    strng = lst[0]
    i = 1
    while i in range(len(lst)):
        strng += f'<snt class="sent" id="s{i}">{lst[i]}'
        i += 1

    strn = strng.replace('&', '</snt>')
    #strn = re.sub(r'@(.+?)&', f'<snt class="sent" id="{i}">\\1</snt>', strn, 0)

    # print(strn)
    return strn

# _________________________________________________________________________________________

def cut_particle(strn):
    print("cut_particle run")
    # 1. отлепляем ->འི от слога
    for syl in ['འིས', 'འང', 'འམ', 'འུ', 'འི']:  # исключил доп.строк - 'འུ'
        strn = re.sub(f'([་\S])({syl})([་།༔])', r"\1་\2\3", strn)

    # ПРАВИЛО: в слоге, состоящем из двух букв, при отсутствие надписных, подписных и огласовок
    # 1я буква считается корневой, а 2я суффиксом.
    # Чтобы 2я буква превратилась в корневую, её необходимо завершить суффиксом འ་, который не читается
    # и замещается འི
    # отлепляем འི заменяя его на འ
    for word in ['གཉ', 'གཏ', 'གད', 'གན', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'དཀ', 'དག', 'དགེ', 'དཔ', 'དབ', 'དམ', 'བཀ',
                 'བཅ', 'བད', 'བཙ', 'བཟ', 'བརྡ', 'བཤ', 'མཀ', 'མཁ', 'མག', 'མང', 'མཐ', 'མད', 'མན', 'མཛ', 'མཟ',
                 'འག', 'འཆ', 'འཇ', 'འད', 'འབ', 'འཛ']:
        strn = re.sub(f'({word})(་འི)', r"\1འ\2", strn)

    strn = re.sub(f'([་\S])(མོ|པ|པོ|བོ|དེ|འདི)(ར)', r"\1\2་\3", strn)
    strn = re.sub(f'([>་?])(པ|པོ|བ|བོ|ཏེ|དེ|འདི)(ས་)', r"\1\2་\3", strn)

    # print(strn)
    return strn

# _________________________________________________________________________________________

def Dict_DB_load():
    print('Dict_DB_load')
    pathSave = "C:/LOTSAWA/"  # путь к локальным файлам основной программы словаря
    # C:\LOTSAWA\DB_DATA\LOTSAWA_DICT
    # pathSave="/MainYagpoOCR/RETREAT/DICT_SCRIPT/"   #путь к локальным файлам основной программы словаря

    pathDB = pathSave+"DB_DATA/LOTSAWA_DICT/"
    pUnionData = pathSave+"DB_DATA/LOTSAWA_DICT/_GVector.bin"
    pUnionIndex = pathSave+"DB_DATA/LOTSAWA_DICT/_GVectorIndex.txt"

    # путь к подключаемым словарям (техт)
    pDictData = pathSave+"DB_DATA/LOTSAWA_DICT/MAIN_DICT_TAB"

    pDictTranslMemoData = pathSave + \
        "DB_DATA/LOTSAWA_DICT/MEMO_TRANSL/Lotsava_MemoTranslate.txt"  # словарь памяти переводов

    # открываем файлы базы данных основного словаря
    print("init Union dictionary")
    v = GVector()
    # объединенный словарь _LotsavaUnion.txt пишем в бинарн файл строк переменной длины
    v.openData(pUnionData)

    dbU = dictBase(pathDB)  # добавился путь в ГВектор
    # noSQL база,  ключи объединенного словаря _LotsavaUnionIndex.txt
    dbU.openData(v, pUnionIndex)

    # если словарь пустой, импортируем текстовые файлы словаря в базу данных
    if(dbU.dictSize == 0):
        print("From MAIN_DICT_TAB import All dictionary in Union dictionary")
        print(dbU.dictSize)
        loadDB(dbU, pDictData)
    return dbU

# _________________________________________________________________________________________

def find_phrase(strn):
    global dLotsawa
    print("find_phrase run")
    # phrase=strn_lst[0]
    res_strn = ""
    res_dct = {}
    not_in_dict = []

    # взяли в список все предложения
    strn_lst = re.findall(f'\d+\">(\S+?)་?[<#༔།\s]', strn)
    # print(strn_lst)

    dbU = dLotsawa  # inputData['dk']  # Dict_DB_load()
    dbU_Key = dbU.dictKey
    # print(dbU_Key)
    for sentence in strn_lst:
        sent_syl_lst = sentence.split('་')
        # print(sentence)
        phrs_syl_lst = list(sent_syl_lst)
        while len(phrs_syl_lst) > 0:  # '་' in phrase:
            phrase = '་'.join(phrs_syl_lst)
            #print("prh ", phrase)
            # НАШЛИ. (отрезаем найденную фразу с начала предлож)
            if phrase+'\n' in dbU_Key:
                value = dbU.get(phrase)
                # print("prh ",phrase)
                # print("val - ", value)  # REPORT
                # 'སྐྱེས་བུ:|:nnn, личность:|:YP'

                if phrase not in res_dct:  # если нет в словаре, записываем фраза : значение
                    try:
                        val = str(value).split(':|:')[1].split('_|_')
                    except:
                        val = str(value).split('_|_')
                        # print(value)

                    # Добавляем в словарь
                    res_dct[phrase] = val

                # форматируем цепляем найденное
                #res_strn += parse_strn(phrase, val)

                # отрезаем найденную фразу с начала предлож
                ln = len(phrs_syl_lst)
                #print("sent_syl_lst", sent_syl_lst, '\n', "phrs_syl_lst", phrs_syl_lst)
                # уменьшенное на найденную фразу предложение
                sent_syl_lst = sent_syl_lst[ln:]
                phrs_syl_lst = list(sent_syl_lst)

            else:   # НЕ НАШЛИ фразу
                # '་' not in phrase:  # если последний слог во фразе отрезаем ненайденный слог с начала
                if len(phrs_syl_lst) == 1:
                    del sent_syl_lst[0]
                    # print(sent_syl_lst)
                    # not_in_dict.append(phrase+'\txxx, \n') # пополняем словарь ненайденных !слогов!
                    phrs_syl_lst = list(sent_syl_lst)
                else:   # DONE уменьшаем фразу, отрезая слог с конца
                    # print("prh ",phrase)
                    del phrs_syl_lst[-1]

    # print(f'strn = {strn}')# \n res_dct = {res_dct}')
    # print(not_in_dict)
    return strn, res_dct

# _________________________________________________________________________________________

def bracket_res_strn(strn, res_dct):
    print("bracket_res_strn run")

    res_strn = strn
    # lst=list(dict.fromkeys(re.findall(r'_\d+_(\S+?)\]', res_strn)))
    # В.Поиск по strn каждого уник из sent_lst в строке
    for key in sorted(res_dct, key=len, reverse=True):
        # из исход строки убираем найденное sent
        # print(key)
        # strn = re.sub(
        #    f'([་།༽༼ ༿\s>]+)({str(key)})([་༽༈།༔༾\s<]+)', r'\1|\3', strn)

        k = str(key).replace('་', '_')
        # в дубль_строке заменяем sent
        res_strn = re.sub(
            f'([་།༽༼\s༿>]+)({str(key)})([་༽༈།༔༾\s<]+)', f'\\1[{k}]\\3', res_strn, 0, re.MULTILINE)
        # res_strn=re.sub(f'([་།༽༼\s༿>]+)({str(key)})', '\\1[\\2]', res_strn, 0, re.MULTILINE) #в дубль_строке заменяем sent
        # print ("res_strn1:   ", res_strn)

    res_strn = res_strn.replace('_', '་')
    # print ("strn:   ", strn)
    # print ("res_strn2:   ", res_strn)
    return res_strn

# _________________________________________________________________________________________

def join_particles(res_strn):
    print("join_particles")
    # Присоединяем оторванные частицы обратно
    res_strn = re.sub(f'((མོ|པ|པོ|བ|བོ|དེ|འདི)\])་(\[ར\])', r'\1\3', res_strn)
    res_strn = re.sub(f'((པ|པོ|བ|བོ|ཏེ|དེ|འདི)\])་(\[ས\])', r'\1\3', res_strn)

    for syl in ['འིས', 'འང', 'འམ', 'འི', 'འུ']:
        res_strn = re.sub(f'་(\[?{syl}\]?)', r"\1", res_strn)

    res_strn = re.sub(f'(གོ|ངོ[་]*|དོ|ནོ|བོ|མོ|རོ|ལོ|སོ|ཏོ)#',
                      '<a def="¶" class="cc">\\1</a>', res_strn)
    res_strn = re.sub(f'་(འོ)#', '<a def="¶" class="cc">\\1</a>', res_strn)
    res_strn = res_strn.replace('#', '')

    # print ('strn:  ',strn)
    #print ('res_strn2:  ', res_strn)

    # print(*res_dct.items(), sep="\n")
    # print('res_dct', res_dct)

    return res_strn

# _________________________________________________________________________________________

def count_word_dict(res_strn):
    print("count_word_dict")
    # замена/уборка вложенных скобок
    res_strn = re.sub(
        f'(\[)([\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ་]+)(\[)', '[\\2', res_strn, 0)

    res_strn = re.sub(
        f'(\])([་\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ]+)(\])', '\\2]', res_strn, 0)

    cont_ = 1

    # исходная строка
    # res_strn

    # старая подстрока - заменяемая часть строки
    subStrOld = '['

    # длина старой подстроки
    lenStrOld = len(subStrOld)

    # Функция find() возвращает индекс первого символа
    # подстроки. Если подстроки нет, то возвращает -1.
    # Цикл используется на случай, если в строке
    # несколько одинаковых подстрок.
    while cont_ < res_strn.find(subStrOld):
        # новая подстрока
        subStrNew = '_'+str(cont_)+'_'
        # сохранить в переменную индекс первого элемента
        # старой подстроки
        i = res_strn.find(subStrOld)
        # Перезаписать строку: взять срез от начала до индекса,
        # добавить новую подстроки и соединить со срезом от конца
        # старой подстроки.
        res_strn = res_strn[:i] + subStrNew + res_strn[i+lenStrOld:]
        cont_ += 1

    # res_strn=re.sub(f'(\d+)({k})\]',
    # print(res_strn)
    return res_strn

# _________________________________________________________________________________________

def parse_strn(strn, phrase, val):
    dgt = 0
    val_lst = val.split(":|:").split("_|_")
    try:
        strn = f'<a id="{dgt}_{phrase}" def="{val_lst[1]}" class="{val_lst[0]}" href="#h_{phrase}">{phrase}</a>'
    except:
        print(phrase)
        strn = f'<a id="{dgt}_{phrase}" def="{val_lst[1]}" class="{val_lst[0]}" href="#h_{phrase}">{phrase}</a>'
    dgt += 1
    return strn
# _________________________________________________________________________________________

def res_strn_dct_html(res_strn, res_dct):
    print("res_strn_dct_html")
    res_dct_html = ""
    # lst=list(dict.fromkeys(re.findall(r'_\d+_(\S+?)\]', res_strn)))
    lst = re.findall(r'_\d+_(\S+?)\]', res_strn)
    # print(lst)
    cnt = 1
    for ind, k in enumerate(lst):  # идем по строке
        # print(lst[ind])
        # создаем тэги для строки
        # res_strn=res_strn.replace(f'[{k}]', f'<a id="{cnt}" def="{res_dct[k]}" class="{part_speech}" href="#h{cnt}">{k}</a>')
        # print(res_strn)
        try:
            res_strn = re.sub(
                f'_(\d+)_({k})\]', f'<a id="\\1_{k}" def="{res_dct[k][1]}" class="{res_dct[k][0]}" href="#h_{k}">{k}</a>', res_strn, 0)
        except:
            print(res_dct[k])
            res_strn = re.sub(
                f'_(\d+)_({k})\]', f'<a id="\\1_{k}" def="{res_dct[k][1]}" class="{res_dct[k][0]}" href="#h_{k}">{k}</a>', res_strn, 0)
            # собираем опции для списка значений
        add = ""
        num = 1
        for itm in res_dct[k]:
            add += f'<div class="option" id="o{num}"><div class="vote_line" style="width: 57%;"></div>{itm}</div>'
            num += 1

        # создаем тэги для словарика
        # завернуть в тиб тег
        res_dct_html += f'<a href="#" id="h_{k}">{add}</a>\n'
        cnt += 1

    # восстанавливаем [ и ] исходного форматирования
    res_strn = re.sub(r'-{(.+?)}-', r'[\1]', res_strn, 0)
    res_strn = re.sub(r'-=-', '_', res_strn, 0)
    # print(res_strn)
    # print(dct_str)
    #  འ заменяя его на འི
    for word in ['གཉ', 'གཏ', 'གད', 'གན', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'དཀ', 'དག', 'དགེ', 'དཔ', 'དབ', 'དམ', 'བཀ',
                 'བཅ', 'བད', 'བཙ', 'བཟ', 'བརྡ', 'བཤ', 'མཀ', 'མཁ', 'མག', 'མང', 'མཐ', 'མད', 'མན', 'མཛ', 'མཟ',
                 'འག', 'འཆ', 'འཇ', 'འད', 'འབ', 'འཛ']:
        res_strn_html = re.sub(f'({word})འ(<.*>འི)', r"\1\2", res_strn)

    # print(res_strn_html)
    return res_strn_html, res_dct_html

# _________________________________________________________________________________________

def save_html_result(res_strn_html, res_dct_html):
    print("save_html_result")
    # пишем тэги для строки и словарика в template Result.html
    res_html = f'% def Result(): \n{res_strn_html}\n % end\n\n\
        % def Slovar(): \n{res_dct_html}\n % end\n\n\
        %rebase Lotsawa %Report_1()=Result, %Report_2()=Slovar'

    with open(inputData['pathGUI']+'\Result.html', 'w', encoding='utf-8') as wf:
        wf.write(res_html)

# _________________________________________________________________________________________

def current_milli_time():
    return int(round(time.time() * 1000))

# _________________________________________________________________________________________

def TibetanUTFToRus(data=''):
    ''' Формат вызова из JavaScript
     http://localhost:4443/?index=(номер текста)&field=(номер страницы)&ocrData=TibetanUTFToRus
     читаем одну страницу из базы данных текстов'''
    global dLotsawa

    #print('data',data)

    # strn = input_strn(data) #эта функция нужна будет только при вызове перевода произвольного текстового файла через GUI
    start_time = current_milli_time()
    start_time_main = start_time

    data = str(read_())
    
    print(current_milli_time() - start_time)

    # print(data)
    start_time = current_milli_time()
    strn = format_txt(data)
    print(current_milli_time() - start_time)
    #print(strn)
    start_time = current_milli_time()
    strn = cut_particle(strn)
    print(current_milli_time() - start_time)
    #print(strn)
    start_time = current_milli_time()
    strn, res_dct = find_phrase(strn)
    print(current_milli_time() - start_time)
    #print(strn)
    start_time = current_milli_time()
    res_strn = bracket_res_strn(strn, res_dct)
    print(current_milli_time() - start_time)
    #print(res_strn)
    start_time = current_milli_time()
    res_strn = join_particles(res_strn)
    print(current_milli_time() - start_time)

    start_time = current_milli_time()
    res_strn = count_word_dict(res_strn)
    print(current_milli_time() - start_time)

    start_time = current_milli_time()
    res_strn_html, res_dct_html = res_strn_dct_html(res_strn, res_dct)
    print(current_milli_time() - start_time)

    # save_html_result(res_strn_html, res_dct_html)
    print("Lotsawa finished. Time:" + str(current_milli_time() - start_time_main))
    #print(res_strn_html)
    return [res_strn_html, res_dct_html]
    #f'{res_strn_html}<div style="display:none">{res_dct_html}</div>'
    #
# _________________________________________________________________________________________

def getWord():  # DONE
    global dLotsawa
    key = ''
    if('key' in inputData):
        key = inputData['key']
        inputData['key'] = ''
    if(key == ''):
        print('no data in request')

    # print(key)
    res=dLotsawa.get(key)
    if res!='':
        res = res.replace(f'{key}:|:', '')
        res = res.replace(f'@_end_/', '\n')
        return res
    else:
        res_lst = TibetanUTFToRus(key)
        return f'{res_lst[0]}<div style="display:none">{res_lst[1]}</div>'

# _________________________________________________________________________________________

def prs2txt():  # DONE
    global dLotsawa
    key = ''
    value = ''
    rw = ''  # rewrite checkbox
    rewrite = False
    if('rw' in inputData):
        if inputData['rw'] == 'true':
            rewrite = True
    if('key' in inputData):
        key = inputData['key']
        inputData['key'] = ''
    if('value' in inputData):
        value = inputData['value']
    if(key == '' or value == ''):
        print('no data in request')

    # rewrite checkbox=False & key in dLotsawa
    if not rewrite and dLotsawa.get(key) != '':
        '''Добавляет/присоединяет новое значение к пулу значений ключа по аналогии 
        с dct['key'].append('val'), поскольку строки текстовые то concatenation	'''
        old_val = dLotsawa.get(key)
        new_val = f'{old_val}, {str(value)}'
        dLotsawa.put(key, new_val)
        # print('appendValue2Key')
    else:
        # если не указана часть речи, то добавляем 'xxx, '
        if value[:3] not in list(['adj', 'avd', 'avi', 'avm', 'avp', 'avt', 'clc', 'cag', 'cld', 'css', 'ccp', 'clc',
                                  'cgn', 'clc', 'cnr', 'cld', 'clc', 'cfs', 'cqt', 'clc', 'cag', 'cld', 'cnr', 'css', 'clc', 'cfn', 'cgn',
                                  'cim', 'clc', 'qst', 'csf', 'cld', 'det', 'dmf', 'dpl', 'uhh', 'nnn', 'nnn', 'nnn', 'nnn', 'nnn', 'nvf',
                                  'nvi', 'nvn', 'nvd', 'nvc', 'num', 'num', 'num', 'num', 'prn', 'itr', 'prn', 'prn', 'vft', 'vim', 'vrb',
                                  'vng', 'vps', 'vpr']):
            value = f'xxx_|_{value}'

        dLotsawa.put(key, value)

    dLotsawa.saveInd()
    # проверка записи
    # print(dLotsawa.get(key))

    path = inputData['pathDB']+'LOTSAWA_DICT/TAB_DATA/00_NW.xml'
    with open(path, 'a+', encoding='utf-8') as wf:
        wf.write(f'{key}\t{value}\n')

    return
# _________________________________________________________________________________________


def snt2txt():  # DONE
    '''
    выгружает переведенное предложение в файл 03_TR.xml в формате
    номер предложения (id)	тибетское предложение	русский перевод
    '''
    global dLotsawa
    sent_id = ''
    tib_snt = ''
    rus_trs = ''

    if('sent_id' in inputData):
        sent_id = inputData['sent_id']
    if('tib_snt' in inputData):
        tib_snt = inputData['tib_snt']
    if('rus_trs' in inputData):
        rus_trs = inputData['rus_trs']
    if(tib_snt == '' or rus_trs == ''):
        print('no data in request')

    # очищаем тиб предложение от [༔།] и помещаем в Базу Переводов
    tib_snt = re.sub(r'་*[༔།]*$', '', tib_snt, 0, re.MULTILINE)
    dLotsawa.put(tib_snt, f'snt_|_{rus_trs}')
    dLotsawa.saveInd()

    # 'MEMO_TRANSL/Transl_Bo_Ru.xml'
    path = inputData['pathDB'] + 'LOTSAWA_DICT/TAB_DATA/03_ST.xml'
    # print(path)
    # print(sent_id, tib_snt, rus_trs)
    # Затем, способ заблуждения существ показывается, и;
    with open(path, 'a+', encoding='utf-8') as wf:
        wf.write(f'{tib_snt}\tsnt_|_{rus_trs} \n')
        # wf.write(sent_id + '\t' + tib_snt + '\t' + rus_trs + '\n')

    return  [f'Sent exported']# sent_id, tib_snt, rus_trs jsonify(result=sent_str)
# _________________________________________________________________________________________

def backUpDB():  # DONE
    '''
    выгружает словарь .txt
    '''
    path = inputData['pathDB'] + 'BackUpDB/BackUpDB.xml'
    dLotsawa.export(path)

    return [f'DB exported to <a href="{path}">BackUpDB.xml</a>']
