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

#declare global database variables
global dt								#основной словарь	
global dk								#словарь памяти переводов
global dBook							#база данных текстов

#_________________________________________________________________________________________

def init(inputData_):
	global inputData
	global dt								#основной словарь	
	global dk								#словарь памяти переводов
	global dBook							#база данных текстов
	inputData = inputData_
	dt=inputData['dt']
	dk=inputData['dk']
	dBook=inputData['dBook']
#_________________________________________________________________________________________

def addWord():
	db=''
	key=''
	value=''
	if('db' in inputData):
		db=inputData['db']
	if('key' in inputData):
		key=inputData['key']
	if('value' in inputData):
		value=inputData['value']	
	if(key=='' or value=='' or db==''):
		print ('no data in request')
		return	
	dataBase=inputData[db]
	dataBase.add(key,value)
#_________________________________________________________________________________________

def getWord():
	db=''
	key=''
	value=''
	if('db' in inputData):
		db=inputData['db']
	if('key' in inputData):
		key=inputData['key']
	if('value' in inputData):
		value=inputData['value']	
	if(key=='' or value=='' or db==''):
		print ('no data in request')
		return	
	dataBase=inputData[db]
	return dataBase.get(key)
#_________________________________________________________________________________________

def remWord():
	db=''
	key=''
	value=''
	if('db' in inputData):
		db=inputData['db']
	if('key' in inputData):
		key=inputData['key']
	if(key=='' or db==''):
		print ('no data in request')
		return	
	dataBase=inputData[db]
	dataBase.rem(key)
#_________________________________________________________________________________________

# 3 handler functions
def start_element(name, attrs):
	if(name=='key'):
		if(attrs['ln']=='tb'):
			dt.keyTib='{}'.format(attrs['key'])
		else:
			n=Pref[4]
			#str=attrs['key']+':|:'+attrs['ln']+':|:TD'
			dt.value+=attrs['key']+MARK+n+END_MARK		
	
	if(name=='rec'):	
		dt.value=''
		#print ('Start element:', name, attrs)
#_________________________________________________________________________________________

def end_element(name):
	if(name=='rec'):
		n=Pref[4]
		if(len(dt.keyTib)>1 and len(dt.value)>3):
			#dt.rep(dt.keyTib,dt.value,':|:'+n)
			#print (dt.keyTib)
			dt.add(dt.keyTib,dt.value)
#_________________________________________________________________________________________	

def test():
	return 'HelloWorld'

#_________________________________________________________________________________________	

def loadXML(name):
			if(len(Pref)<5):
				for i in range(5):
					Pref.append('')
			Pref[4]=name
			p = xml.parsers.expat.ParserCreate()
			p.StartElementHandler = start_element
			p.EndElementHandler = end_element
			p.CharacterDataHandler = char_data
			with open(pathDB+'XML_DICT/'+name+'.xml') as f:
				p.ParseFile(f)

#_________________________________________________________________________________________

def fullRep(sender):
	str=searchText.text
	if(len(str)>0):
		str+='་'
		str=str.replace('་་','་')
		searchText.text=str	
		translate()
		printHtml(dt.data[0])
			
	inputData['mainMode']=FULL_REPORT	
	js='readText()'
	textAll=textIn.eval_js(js)
	#textIn.text is unicode, it is need convert it in utf-8
	textAll='{}'.format(textAll)
	textAll=htmlToText(textAll)
	dt.data[0]=textAll
	translate()
	printHtml(dt.data[0])
	#searchBtn.title='Word From Text'
	inputData['mainMode']=DICT_REPORT_TEXT
	#t2=time.time()
	#printHtml(report+'\n done in {} sec'.format(t2-t1))
#_________________________________________________________________________________________    
    
def TibetanUTFToRus():
	report=""
	
	if('user_text' in inputData):
		report_=inputData['user_text']
		text=bytearray()
	
		#это место нужно переделать. 
		#bottle возвращает кодированную в utf-8 строку которая уже была закодирована в utf-8 
		#в момент формирования адреса URL в Java Script
		for c in report_:
			text.append(ord(c))
		inputData['user_text']=text.decode()

	else:
		index=""
		field=""
		if "index" in inputData:
			index=inputData['index']
		if "field" in inputData:
			field=inputData['field']
		inputData['user_text']=read()	
		
	inputData['mainMode']=TRANSLATE
	
	report=translate()
	
	return report
#_________________________________________________________________________________________		
			
def dictionaryReport():
	"""report from all dictionaries in database"""
	textAll=inputData['user_text']
	textAll+='་'
	textAll=textAll.replace('་་','་')
	dt=inputData['dt']
	dk=inputData['dk']
	dt.history.append(textAll)
	dk.get(textAll)
	res=''
	res+='['+linkDict(textAll)+linkEdit('='+dk.res)+']་<hr>'
	dt.get(textAll)
	str_=formatReport(dt.res)
	res+=str_
	return res
#_________________________________________________________________________________________	

def translateLine(text):
	inputData['user_text']=text
	inputData['mainMode']=TRANSLATE
	return translate()
	
def translate():
	report=''
	textAll=inputData['user_text']+"\n"
	inputData['user_text']=""
	dt=inputData['dt']
	dk=inputData['dk']
	mainMode=inputData['mainMode']
	
	#textAll='བ་དག་གི་འབྲས་བུའི་མཆོག་མཐར་ཐུག་པ་ནི་རང་བཞིན་རྫོགས་པ་ཆེན་པོའི་ཆོས་ཀྱི་རྣམ་གྲངས་ལས་འོད་གསལ་རྡོ་རྗེ་སྙིང་པོའི་ཐེག་པ་བླ་ན་མེད་པ་འདི་ཡིན་ཏེ་།་\n'
	textAll=textAll.replace(' ','\n')
	text=textAll.split('\n')
	d=dk.dictKey
	reportT=''
	n=0
	
		
	for n in range(0,len(text)-1):
		src=text[n]
		s=src
		
		reportN=text[n+1]
		rd={} #dictionary of words result
		lng=len(s)
		if(lng<2):
			continue
		if(re.search('་', reportN) == None and re.search('།', reportN) == None):
			reportT=reportN
		if(re.search('་', s) == None and re.search('།', s) == None):
			if(re.search('[\d\[<]',src)!=None):
				report+='<br><d>'+src+'</d>'
			continue
		s=re.sub(u'[ _\d\ "	\'\*\(\)\{\}\[\]@•#\%\&༄༅༔༴༡༢༣༤༥༦༧༨༩༠༎།༑༈༌༐༏༼༽ऀ-ॿ]',u"་",s)
		s=re.sub(u'ཿ',u'ཿ་',s)
		s=s+u'་།'
		s=re.sub(u'་[་]+',u"་",s)
		s=re.sub(u'([^་])འོ་',r"\1་(точка)་",s)
		#s=re.sub(u'([^་])འམ་',r"\1་[འམ=или]་",s)
		s=re.sub(u'ག་གོ་།',u"ག་(точка)་",s)
		s=re.sub(u'ང་ངོ་།',u"ང་(точка)་",s)
		s=re.sub(u'ད་དོ་།',u"ད་(точка)་",s)
		s=re.sub(u'ན་ནོ་།',u"ན་(точка)་",s)
		s=re.sub(u'བ་བོ་།',u"བ་(точка)་",s)
		s=re.sub(u'མ་མོ་།',u"མ་(точка)་",s)
		s=re.sub(u'ར་རོ་།',u"ར་(точка)་",s)
		s=re.sub(u'ལ་ལོ་།',u"ལ་(точка)་",s)
		s=re.sub(u'ས་སོ་།',u"ས་(точка)་",s)
		s=re.sub(u'་ཏོ་།',u"་(точка)་",s)
		s=re.sub(u'་པའང་',u"་པ་[འང=уступ.]་",s)
		s=re.sub(u'་བའང་',u"་བ་[འང=очень]་",s)
		s='{}'.format(s)

		l=s.split('་')
		res=''
		resD=''
				
		lng=len(l)
		start=0
		end=lng-1
		
		i=lng
		count=0
		#t1=time.time()
		
		while start<lng :
			#make query string decrease end
			end=lng
			while end>-1 :
				j=start
				line=''
				while j < end:
					line+=l[j]+'་'
					j+=1
				count+=1
				#print (line)
				if (count >1000):
					#print (line+' {} {}'.format(start,end))
					break
				ld=line+'\n'
				if(ld in d):
					dk.get(line)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					if('__' in c):
						res+='['+linkDict(line)+linkEdit('='+c)+']་<br></c><c>'
						end-=1
						continue
					res+='['+linkDict(line)+linkEdit('='+c)+']་'
					if(mainMode==FULL_REPORT and start==0 and end==lng-1):
						end-=1
						continue
					start=end-1
					break
				#next check big dictionary report
				if(len(line)>3 and ld in dt.dictKey):
					resD+='['+linkDict(line)+linkEdit('=')+'] '
				ln=line+'@'
				l1=ln.replace('འི་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-འི་')+linkEdit('=g.p')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('ས་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-ས་')+linkEdit('=i.p.')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('ར་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-ར་')+linkEdit('=d.l.')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):	
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('འོ་@','འ་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+'](точка)་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('འམ་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-འམ་')+linkEdit('=или')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				end-=1
				if(end==start):
					res+=line
					break
			start+=1
			res=res.replace(':|:YP','')	
		
		if(re.search('lt',src)!=None):
			src='<d>'+src+'</d>'
		else:
			src='<p class="tib">'+src+'</p>'
		report+=src+'\n@'
		if(len(reportT)):
			report+='<d>'+reportT+'</d>\n'
		report+='<w>'+res+'\n'
			
		if(len(resD)>10):
			report+='<td>'+resD+'</td>'	
		report+='</w>\n'
		report=report.replace('@་','@')
		reportT=''
		if(inputData['mainMode']==FULL_REPORT):
			res=''
			for line in l:
				ld=line+'་\n'
				key=line+'་'
				if(ld in d):
					dk.get(key)
					c=dk.res
					res+='['+linkDict(key)+linkEdit('='+c)+']་'	
			res=res.replace(':|:YP','')		
			report+='<br><c>'+res+'</c>\n<br>'	
			
		#print (report)
		#sys.exit()
	return report
#_________________________________________________________________________________________	
	
def linkDict(line):
	dt=inputData['dt']
	s=''
	id='s{}'.format(dt.id)
	s='<tb id="'+id+'" onClick="set(\''+id+'\')">'+line+'</tb>'
	dt.id+=1
	return s
#_________________________________________________________________________________________
	
def linkText(line):
	dt=inputData['dt']
	s=''
	id='s{}'.format(dt.id)
	s='<t id="'+id+'" onClick="edit(\''+id+'\')">'+line+'</t>'
	dt.id+=1
	return s
#_________________________________________________________________________________________

def linkEdit(line):
	dt=inputData['dt']
	#line=re.sub('^[^:]*:\|:','=',line)
	s=''
	id='s{}'.format(dt.id)
	l=line
	line=line.replace('@','')
	line=line.replace('*','')
	line=line.replace('%','')
	
	s='<t id="'+id+'" onClick="edit(\''+id+'\')" onBlur="v(\''+id+'\')">'+line+'</t>'
	
	dt.id+=1
	return s	
#_________________________________________________________________________________________

def formatReport(str_):

	lines=str_.split(END_MARK)
	str_=''
	for line in lines:
		line=line.replace(MARK,'<br>')
		line=re.sub(r'\[c:[^\]]*\]',r'',line)
		line=re.sub(r'^([^\<]*)<br>\1',r'\1',line)
		#print (line)
		#print ('_____________')
		if('<br>TT' in line or '<br>DK' in line):
			#print (line)
			line=line.replace('༡','@1')
			line=line.replace('༢','@2')
			line=line.replace('༣','@3')
			line=line.replace('༤','@4')
			line=line.replace('༥','@5')
			line=line.replace('༦','@6')
			line=line.replace('༧','@7')
			line=line.replace('༨','@8')
			line=line.replace('༩','@9')
			line=line.replace('༠','@0')
			line=re.sub(r'@([\d])@([\d])',r'@\1\2',line)
			line=re.sub(r'@([\d])@([\d])',r'@\1\2',line)
			line=line.replace('@','\n')
			line=line.replace(' ','་྾་')
			line=line.replace('།་','།')
			line=line.replace('།','།\n')
			line=line.replace('༼','\n༽')
			line=line.replace('༽','༽\n')
			line=line.replace('<br>TT','')
			line=line.replace('<br>DK','')
			line=translateLine(line)
			line=line.replace('྾་',' ')
			line=line.replace('྾','<br>')
			line=line.replace('<c><br>','<c>')
			line=line.replace('<br>།</c>','།</c>')
			line+='TT'
		else:
			#id='{}'.format(dt.id) #?
			id=""
			line='<t id="l'+id+'" onClick="edit(\'l'+id+'\')">'+line+'</t>'
			#dt.id+=1
		str_+=line+'<hr>'
	return str_
#_________________________________________________________________________________________	

def printCatalog():
	global dBook
	lines=dBook.keyList
	report=""
	
	for line in lines:
		report+="<a href=\"/?ocrData=read&index="+str(dBook.dictKey[line])+"&field=0\" target=\"_blank\">"+line+"</a><br/>\n"
	return report
	
#_________________________________________________________________________________________

def read():
	'''
	Текстовые файлы из DHARMABOOK размещаются в БД db их можно запрашивать из Питона постранично. 
	Фомат вызова из Питона в функции def read():

	Формат вызова из JavaScript 
	http://localhost:4443/?index=(номер текста)&field=(номер страницы)&ocrData=read
	'''
	global dBook
	index = int(inputData['index'])
	field = int(inputData['field'])
	text = dBook.vData.getStr(index)
	print('index ',index)
	l = len(text)
	start = field*PAGE_SIZE
	if(start >= l):
		start = 0
	end = start + PAGE_SIZE
	if(end >= l):
		end = l-1
	
	#print("FIELD:"+str(field) + " start:"+ str(start) + " end:"+ str(end)+ " l:"+ str(l))		
	# передвигаем начало страницы в начало предложения
	limit=0
	if(start!=0):
		limit=0;
		while (text[start+limit]!=" "):
			limit+=1;
			if (limit==256 or limit==l-1):
				limit=0
				break
	start+=limit;

	# передвигаем конец страницы в начало предложения
	limit=0;
	while (text[end+limit]!=" "):
		limit+=1;
		if (limit==256 or limit==l-1):
			limit=0
			break
	end+=limit;

	page = text[start:end]
	
	
	#print("page:"+page)
	
	return page
#_________________________________________________________________________________________


def previousPage(sender):
	global Pref
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r", newline="\n") as f:
		textFile=f.readlines()
	c=pageIndex.text
	i=0
	if('#' in c):
		for line in textFile:
			if(c in line):
				break
			i+=1
		i=i/pageSize
	else:
		i=eval(c)-1
	if(i<0):
		i=len(textFile)/pageSize
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	Pref[2]=pageIndex.text
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	searchBtn.title='Translate'
	inputData['mainMode']=TRANSLATE
	searchText.text=''
	savePref()
	printHtml(text)
#_________________________________________________________________________________________

def nextPage(sender):
	global Pref
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
	c=pageIndex.text
	i=0
	if('#' in c):
		for line in textFile:
			if(c in line):
				break
			i+=1
		i=i/pageSize
	else:
		i=eval(c)+1
	if(i>len(textFile)/pageSize):
		i=0
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	Pref[2]=pageIndex.text
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	searchBtn.title='Translate'
	inputData['mainMode']=TRANSLATE
	searchText.text=''
	savePref()
	printHtml(text)
#_________________________________________________________________________________________	
	
def openText():
	pathField=fileView['textfield1']
	path=pathField.text	
	path=pathMain+'{}'.format(path)
	if(os.path.isfile(path)):
		
		with open(pathDB+pageStyle,"r") as f:
			htmlPage=f.read()
			Pref[0]=htmlPage
		with open(path,"r",newline="\n") as f:
			textFile=f.readlines()
			if(len(textFile)<1):
				str='no text'
			else:
				if(len(textFile[0])>1024):
					str='too long line'
				else:
					c=pageIndex.text
					i=eval(c)
					page=textFile[i*pageSize:i*pageSize+pageSize]
					#pageIndex.text='{}'.format(i)
					str='<br>'.join(page)
					if(len(str)>90000):
						str='too long line'
				
			text='<t id="t1" onClick="edit(\'t1\')">'+str+'</t>'
			str=htmlPage.replace('@@@TEXT@@@',text)
			str=str.replace( chr(0),' ')
			textIn.load_html(str)	
			#print (str)
	else:
		print ('not open '+ path)
		menu(1)
#_________________________________________________________________________________________
		
def copyText(sender):
	pathField=fileView['textfield1']
	path=pathField.text	
	path=pathMain+'{}'.format(path)
	if(os.path.isfile(path)):
		with open(path,"r") as f:
			textFile=f.read()
		dialogs.share_text(textFile)
#_________________________________________________________________________________________
	
def menu(sender):
	path=fileView['textfield1'].text
	path=re.sub('/[/]+','/',path)
	fileView['textfield1'].text=path
	tbl=fileView['tableview1']
	tblD=fileView['tableview2']
	path=os.path.dirname(path)
	if(os.path.isdir(pathMain+path)):
		listD=os.listdir(pathMain+path)
	else:
		path='/'
		listD=os.listdir(pathMain)
		fileView['textfield1'].text='/'
	l=[]
	ld=['...']
	for line in listD:
		if(os.path.isdir(pathMain+path+'/'+line)):
			ld.append(line)
		else:
			l.append(line)
	tbl.data_source.items=l
	tblD.data_source.items=ld
	fileView.x=0
#_________________________________________________________________________________________
	
def openDir(sender):
	path=fileView['textfield1'].text
	path=path.replace('#','/')
	path=os.path.dirname(path)
	tbl=fileView['tableview1']
	tblD=fileView['tableview2']
	dir=tblD.data_source.items[tblD.selected_row[1]]
	if(dir=='...'):
		path=os.path.dirname(path)
		dir=''
	listD=os.listdir(pathMain+path+'/'+dir)
	c=path+'/'+dir+'/'
	c=c.replace('#','/')
	c=re.sub('//+','/',c)
	fileView['textfield1'].text=c
	l=[]
	ld=['...']
	for line in listD:
		if(os.path.isdir(pathMain+path+'/'+dir+'/'+line)):
			ld.append(line)
		else:
			l.append(line)
	tbl.data_source.items=l
	tblD.data_source.items=ld
#_________________________________________________________________________________________

def openFile(sender):
	global Pref
	tbl=fileView['tableview1']
	line=tbl.data_source.items[tbl.selected_row[1]]
	fileView.x=1024
	path=fileView['textfield1'].text
	path=os.path.dirname(path)
	fileView['textfield1'].text=path+'/'+line
	Pref[1]=path+'/'+line
	Pref[2]='0'
	pageIndex.text='0'
	savePref()
	openText()
#_________________________________________________________________________________________		

def replaceRegExpFile(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	pathRep=fileView['textfield3'].text
	pathRep=pathMain+'{}'.format(pathRep)
	with open(pathRep,"r") as f:
		str=f.read()
		dataRegExp=str.split('\n:|:\n')
		
	path=os.path.dirname(path)
	listD=os.listdir(path)
	for line in listD:
		print (line)
		if(os.path.isdir(path+'/'+line)):
			pass
		else:
			print ('start '+line)
			with open(path+'/'+line,"r") as f:
				text=f.read()
				for l in dataRegExp:
					c=l.split(' --> ')
					if(len(c)<2):
						print ('not valid re '+l)
					else:
						text=re.sub(c[0],c[1],text)
			with open(path+'/'+line,"w") as f:	
				f.write(text)	
			print ('done '+line	)
#_________________________________________________________________________________________
	
def replaceRegExpText(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	textSrc=fileView['textfield4'].text
	textSrc='{}'.format(textSrc)
	textRep=fileView['textfield5'].text
	textRep='{}'.format(textRep)
	a=re.compile(textSrc,re.M)
	with open(path,"r") as f:
		textFile=f.read()
		textFile=unicode(textFile)
		c=chr(0xA0)
		textFile=re.sub(c,' ',textFile)
		textFile='{}'.format(textFile)
		#s=textFile[0:32]
		#s=unicode(s)
		#i=0
		#while i<len(s):
		#	print ('{0:x}'.format(ord(s[i])))
		#	i+=1
		
		textFile=re.sub(a,textRep,textFile)
		#textFile=textFile.replace(textSrc,textRep)
		#textFile=textFile.replace(' ','\n')
		#textFile=re.sub('།','།\n',textFile)
		#textFile=re.sub(r'\n[\n]+','\n',textFile)
		#textFile=re.sub(r'།\n[ ]*།\n','།\n།',textFile)
		#textFile=re.sub(r' ','\n',textFile)
		
	with open(path,"w") as f:	
		f.write(textFile)		
	openText()
	fileView.x=1024
#_________________________________________________________________________________________	
	
def searchInDharmabook(sender):
	path=pathDB+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	res=''
	i=0

	with open(path,"r") as f:
		for line in f:
			str=line[0:1024]
			if(text in str):
				l=len(str)
				str=str[0:str.rfind(' ')]
				if(len(str)==l):
					str=str[0:str.rfind('¶')]
				res+=str+'\n'
				i+=1
			if(i>300):
				break		
	with open(pathDB+'res_dharmabook.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
#_________________________________________________________________________________________
		
def searchInDharmabookFullText(sender):
	path=pathDB+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	res=''
	searchCount=0

	with open(path,"r") as f:
		for line in f:
			index=line.find(text)
			if(index!=-1):
				str=line[0:256]
				if(str.rfind(' ')!=-1):
					str=str[0:str.rfind(' ')]
				else:
					if(str.rfind('¶')!=-1):
						str=str[0:str.rfind('¶')]
					else:
						if(str.rfind('་')!=-1):
								str=str[0:str.rfind('་')]
				#print ('{0:d}'.format(len(resList))+' found '+str)
				res+='\n================================\n'+str+'\n____________________________________\n'
	
			while(index!=-1):	
					str=line[index-512:index]
					l=len(str)
					if(str.find(' ')!=-1):
						str=str[str.find(' '):l]
					else:
						if(str.find('¶')!=-1):
							str=str[str.find('¶'):l]
						else:
							if(str.find('་')!=-1):
								str=str[str.find('་'):l]
					res+=str
					
					str=line[index:index+512]
					if(str.rfind(' ')!=-1):
						str=str[0:str.rfind(' ')]
					else:
						if(str.rfind('¶')!=-1):
							str=str[0:str.rfind('¶')]
						else:
							if(str.rfind('་')!=-1):
								str=str[0:str.rfind('་')]
					res+=str+'\n\n'
					searchCount+=1
					if(searchCount>300):
						break		
					index=line.find(text,index+len(text))
			if(searchCount>300):
					break 
	res=unicode(res)
	c=chr(0xA0)
	res=re.sub(c,' ',res)
	res='{}'.format(res)		
	res=res.replace('¶','\n')
	res=res.replace('། ','།\n')
	res=res.replace('༔ ','༔ \n')
	with open(pathDB+'res_dharmabookFullText.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
#_________________________________________________________________________________________
				
def exportTextByID(sender):
	path=pathDB+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	with open(path,"r") as f:
		for line in f:
			str=line[0:128]
			if(text in str):
				with open(pathDB+'res_dharmabookText.txt',"w") as f:
					f.write(line)  
				break	
		fileView.x=1024
#_________________________________________________________________________________________

def searchInFolder(sender):
	print ('search')
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	print (path)
	str=fileView['textfield6'].text
	str='{}'.format(str)
	res=''	
	path=os.path.dirname(path)
	listD=os.listdir(path)
	i=0
	for line in listD:
		if(os.path.isdir(path+'/'+line)):
			pass
		else:
			with open(path+'/'+line,"r") as f:
				for l in f:
					if (str in l):
						res+=line+'\n'+l+'\n'
						i+=1
						if(i>100):
							res=res.replace('\n\n','\n')
							with open(pathDB+'res.txt',"w") as f:
								f.write(res)
							return
	res=res.replace('\n\n','\n')
	with open(pathDB+'res_1.txt',"w") as f:
		f.write(res)
#_________________________________________________________________________________________

def searchInFileText(sender):
	path=fileView['textfield1'].text
	text=fileView['textfield6'].text
	text='{}'.format(text)
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
	i=0
	for line in textFile:
		if(text in line):
			break
		i+=1
	i=i/pageSize
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	printHtml(text)
	fileView.x=1024
#_________________________________________________________________________________________
	
def searchInFile(sender):	
	path=fileView['textfield1'].text
	text=fileView['textfield6'].text
	text='{}'.format(text)
	path=pathMain+'{}'.format(path)
	res='test'
	searchCount=0

	with open(path,"r",newline="\n") as f:
		textLines=f.readlines()
		i=1
		l=len(textLines)-1
		while(i<l):
			index=textLines[i].find(text)
			if(index!=-1):
				res+=textLines[i-1]+textLines[i]+textLines[i+1]+'\n༄།།\n'
				searchCount+=1
			i+=1
	print (searchCount)
	with open(pathDB+'res_dharmabookTextSearch.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
#_________________________________________________________________________________________		


def close(sender):
	dt.close()	
	view.close()
	savePref()
#_________________________________________________________________________________________	

def cmpLines(a,b):
	a_=len(a.split(' @ ')[0])
	b_=len(b.split(' @ ')[0])
	if(a_>b_):
		return -1
	elif(a_<b_):
		return 1
	else:
		return 0
	
#_________________________________________________________________________________________

def saveDict():
	dictNew=list()
	text=re.sub(r'<[^>]*>','',text)
	text=text.replace('«','༼')
	text=text.replace('{','༼')
	text=text.replace('»','༽')
	text=text.replace('}','༽')
	lines=text.split('[')
	for l in lines:
		if ('=' in l):
			continue
		if ('/' in l):
			#print (l)
			c=l.split(']')
			d=c[0].split('/')
			if(len(d)>1):
				key=d[0]+'་'
				key=key.replace('་་','་')
				if (d[1]=='-'):
					dk.rem(key)
					continue
				if(len(d[0])<3 or len(d[1])<3):
					continue
				value=d[1]+'%'
				value=value.replace('@%','%')
				value=value.replace('*%','%')
				value=value.replace('%%','%')
				dk.put(key,value)
	dk.saveInd()
#_________________________________________________________________________________________
		
def htmlToText(textAll):
	textAll=textAll.replace('\n','')
	textAll=textAll.replace('<br>','\n')
	textAll=textAll.replace('<div>','\n')
	textAll=textAll.replace('&nbsp','')
	textAll=textAll.replace('<c>','@')
	textAll=textAll.replace('<td>','@')
	#textAll=textAll.replace('[','@')
	textAll=re.sub(r'@.*','@',textAll)
	textAll=textAll.replace('@\n','')
	textAll=re.sub(r'<[^>]*>','',textAll)
	return textAll
#_________________________________________________________________________________________

def save(sender):
	f = open(pathDB+'_pref.txt',"w")
	pickle.dump(Pref, f)
	f.close()	
		
	#textIn.text is unicode, it is need convert it in utf-8
	#need rewrite with codecs 
	js='readText()'
	if(mainDictView.x==0):
		textAll=dictView.eval_js(js)
		textAll='{}'.format(textAll)
		saveDict(textAll)
		return
	
	textAll=textIn.eval_js(js)
	#textIn.text is unicode, it is need convert it in utf-8
	textAll='{}'.format(textAll)
	saveDict(textAll)
#_________________________________________________________________________________________
		
def closeDictView(sender):
	if(len(dt.history)>0):
		dt.history.pop()
		if(len(dt.history)>0):
			searchText.text=dt.history[len(dt.history)-1]
			dt.history.pop()
			dictEntry()
		else:
			mainDictView.x=1024
	else:
		mainDictView.x=1024
#_________________________________________________________________________________________
	
def setCommentaryTag(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
												  
	for key in dk.keyList:
		key=key.rstrip('\n')
		dk.get(key)
		c=dk.res
		if('__' in c):
			i=0
			key=key.rstrip('་')
			for line in textFile:
				s=unicode(line)
				s=re.sub(u'[ _\d\ "	\'\*\(\)\{\}\[\]@•#\%\&༄༅༔༴༡༢༣༤༥༦༧༨༩༠༎།༑༈༌༐༏༼༽ऀ-ॿ]',u"་",s)
				s=re.sub(u'་[་]+',u"་",s)
				s='{}'.format(s)
				if(key in s):
					textFile[i]='#_'+textFile[i]
					break
				i+=1
	with open(path,"w") as f:
		f.writelines(textFile)
#_________________________________________________________________________________________
			
def buildSummary(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	res=''
	with open(path,"r") as f:
		for line in f:
			if('#' in line):
				res+=line	
	fileView['textfield1'].text='Dictionary/_res.txt'
	path=pathMain+'Dictionary/_res.txt'
	with open(path,"w") as f:
		f.write(res)
	openText()
#_________________________________________________________________________________________	

def fileCopy(path1,path2):
	print (copy)
	f=open(path1, 'r',newline="\n")
	t=f.readlines()
	#print (len(t))
	f.close()
	f=open(path2, 'w',newline="\n")
	f.writelines(t)
	f.close()
#_________________________________________________________________________________________
	
def sortDict(name):
	print ('load {}'.format(name))
	with open(pathDB+'XML_DICT/'+name+'.txt') as f:
		str=f.read()
		f.close()
		str=str.replace('\r','\n')
		d=str.split('\n')
		print (len(d))
		d.sort()
		i=0
		s=list()
		l=''
		for line in d:
			i+=1
			line=line.replace('*','@')
			line=re.sub('[\n\r\t ]*$','',line)
			if(l==line):
				continue
			
			#print (line+'/')
			#print (len(line))
			#if(i==10):
				#break	
				
			l=line
			s.append(line+'\n')
		f=open(pathDB+'XML_DICT/'+name+'_new.txt', 'w')
		f.writelines(s)	
		f.close()
		print (len(s))
		print ('done')
#_________________________________________________________________________________________
		
def loadPref():
	global Pref
	p=pathDB+'_pref_dict.txt'
	try:
		io.open(p,'r')
	except IOError:
		savePref()
	with open(p,'r') as f:
		Pref=pickle.load(f)
	while len(Pref) < 5:
		Pref.append('')
	fileView['textfield1'].text=Pref[1]
	if(Pref[2]==''):
		Pref[2]='0'
	pageIndex.text=Pref[2]
#_________________________________________________________________________________________	
		
def savePref():
	global Pref
	p=pathDB+'_pref_dict.txt'
	with open(p,'w') as f:
		pickle.dump(Pref,f)
#_________________________________________________________________________________________

def getWord():
	db = ''
	key = ''
	value = ''
	if('db' in inputData):
		db = inputData['db']
	if('key' in inputData):
		key = inputData['key']
	if(key == '' or db == ''):
		print('no data in request')
	dataBase = inputData[db]
	return dataBase.get(key)
#_________________________________________________________________________________________

def putWord():
	db = ''
	key = ''
	value = ''
	if('db' in inputData):
		db = inputData['db']
	if('key' in inputData):
		key = inputData['key']
	if('value' in inputData):
		value = inputData['value']
	if(key == '' or value == '' or db == ''):
		print('no data in request')
	dataBase = inputData[db]
	dataBase.put(key, value)
	return
#_________________________________________________________________________________________

def remWord():
	db = ''
	key = ''
	value = ''
	if('db' in inputData):
		db = inputData['db']
	if('key' in inputData):
		key = inputData['key']
	if(key == '' or db == ''):
		print('no data in request')
	dataBase = inputData[db]
	dataBase.rem(key)
	return
#_________________________________________________________________________________________