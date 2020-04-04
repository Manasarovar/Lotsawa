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

textFile=list()
dict=list()
pageSize=100
#pageStyle='practice.html'
pageStyle='page.html'
#pageStyle='practice_read.html'
readMode=1
printKey=0   #print debug messages


#enum
READ=1 #режим чтения с переводом слогов по памяти
ALL=1
AUTO=0
EMPTY=-1
EDIT=1
LINK=0
CHINK_SIZE=1024*40
VALUE_SIZE=1024*20
MB=1024*1000
START_MARK='@_dict_/'
END_MARK='@_end_/'
EMPTY_MARK='_*_'
MARK=':|:'
JS=0
USER=1
TRANSLATE=1
DICT_REPORT_TEXT=2
DICT_REPORT_USER=3
FULL_REPORT=4
PAGE_SIZE=2048			#размер страницы текста в байтах		

INDEX_RESIZE=4 			#во сколько раз будет увеличиваться размер индекса
FILE_RESIZE=2 			#во сколько раз будет увеличиваться размер файла
FILE_RESIZE_DELTA=100 	#количество записей на которое увеличивается размер файла в дополнении к увеличению в FILE_RESIZE раз.(нужен при записи больших записей в небольшой файл)
POOL_SIZE=16384  

MEMORY_LOCATION=0
MMAP_LOCATION=1

global Pref
Pref=list()		 #preferences

class GVector:
	def __init__(self):
		self.dataPath=''
	  #MemoryFile
		self.dataMFile=''
	  #GVector *parent
		self.index=[]						#массив индексов записей в GVector
		self.innerData=array('Q')			#массив размещенный в начале файла, в который записываются внутренние переменные
	  #внутренние переменные
		self.recordCount=0  	  			  	#количество записей в векторе
		self.recordArraySize=0				#размер файла учета записей
		self.dataSize=0  	 	  			#размер занимаемый актуальными данными
		self.poolSize=0  	 	  			#общий размер файла вектора
		self.lockFlag=0						#флаг блокировки чтения-записи
		self.indexOffset=0	 	  			#адрес размещения массива индекса записей. отсчитывается от начала файла
		self.vectorID=0
		self.dataLocation=0
		
	def __del__(self):
		self.dataMFile.close()
	
	def openData(self,dataPath):
		self.dataPath=dataPath
		f = None
		try:
			f=open(dataPath, 'r')
		except:
			f=open(dataPath, 'w')
		f.close()
		
		c=os.stat(dataPath)
		self.dataMFile=open(dataPath, 'rb+')
		self.poolSize=c.st_size
		print ('poolSize={:,}'.format(self.poolSize))
		self.init()
		
			
	def init(self):
		self.dataLocation=MMAP_LOCATION 	 		 	#флаг размещения данных в оперативной  или  отображаемой памяти
		#cout<<" dataMFile->size()={}".format(dataMFile->size()
		#проверяем является ли файл файлом GVector
		if(self.poolSize<POOL_SIZE):					#новый файл GVector 	 	
			print ('new vector')
			for i in range(16): self.innerData.append(0)
			self.innerData[0]=0xfffffffa		  		#маркер наличия GVector
			self.recordArraySize=1024
			self.recordCount=0
			self.dataSize=(self.recordArraySize)*8+128
			self.indexOffset=128
			self.vectorID=0xffffffff
			self.lockFlag=0
			indexName="name:|:data"
			#index=(uint*)(data+*indexOffset)  			#инициализация индекса
			self.push_back(indexName) 	 	 	 	 	#инициализация индекса именных записей
			self.recordCount=1
			self.setSpace(POOL_SIZE)
			self.saveData()			
		else:
			#проверяем является ли файл файлом GVector
			self.readData()
			if(self.innerData[0]!=0xfffffffa):
				print ("no valid GVector file "+ self.dataPath)
				return
	def loadData(self,dataPath):
		print ('load lext files in text database')
		print ("load data " + dataPath)
		self.dataPath=dataPath
		if(os.path.isdir(self.dataPath)):
			listD=os.listdir(self.dataPath)
		else: 
			print (self.dataPath+" is not valid path")
		for line in listD:
			if(line[0]=='.'):
				continue
			print (line)		
			self.loadTXT(self.dataPath+line)
	
	def loadTXT(self,fileName):
		print ('load'.format(fileName))
		
		with open(fileName, newline="\n", encoding='utf-8') as f:
			str=f.read()
			f.close()
			self.push_back(str)
	
	
			
	def saveData(self):			
			self.innerData[1]=self.poolSize				#размер файла вектора
			self.innerData[2]=self.recordCount  		#количество записей в векторе
			self.innerData[3]=self.recordArraySize		#размер файла учета записей
			self.innerData[4]=self.dataSize 	 		#размер занимаемый актуальными данными
			self.innerData[5]=self.lockFlag				#флаг блокировки чтения-записи
			self.innerData[6]=self.indexOffset	 	 	#адрес размещения массива индекса записей. отсчитывается от начала файла
			self.innerData[7]=self.vectorID 	 		#индекс записи, в которой GVector размещен в родительском векторе
			
			str=array.tobytes(self.innerData)
			#os.lseek(self.dataMFile,0,os.SEEK_SET)
			#os.write(self.dataMFile,str)	
			self.dataMFile.seek(0, 0)
			self.dataMFile.write(str)
		
	def readData(self):
		#os.lseek(self.dataMFile,0,os.SEEK_SET)
		#str=os.read(self.dataMFile,128)
		self.dataMFile.seek(0, 0)
		str=self.dataMFile.read(128)
		self.innerData=array('Q')
		self.innerData.frombytes(str)
		#print (self.innerData)
		self.poolSize=self.innerData[1]					#размер файла вектора
		self.recordCount=self.innerData[2]  			#количество записей в векторе
		self.recordArraySize=self.innerData[3]			#размер файла учета записей
		self.dataSize=self.innerData[4] 	 			#размер занимаемый актуальными данными
		self.lockFlag=self.innerData[5]					#флаг блокировки чтения-записи
		self.indexOffset=self.innerData[6]	 	 		#адрес размещения массива индекса записей. отсчитывается от начала файла
		self.vectorID=self.innerData[7] 	 			#индекс записи, в которой GVector размещен в родительском векторе
		
	def mPut(self,offset,line):
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		self.dataMFile.seek(offset, 0)
		str_b = str.encode(line)
		#os.write(self.dataMFile,str_b)
		self.dataMFile.write(str_b)

		
	def mPutBin(self,offset,line):
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		#os.write(self.dataMFile,line)	
		self.dataMFile.seek(offset, 0)
		self.dataMFile.write(line)
			
		
	def mPutInt(self,offset,value):
		str=value.to_bytes(8, byteorder='little')		
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		#os.write(self.dataMFile,str)	
		self.dataMFile.seek(offset, 0)
		self.dataMFile.write(str)
		#print ("valueIn:{} str:{} value:{} offset:{}".format(value,str.hex(),value,offset))

		#self.dataMFile.seek(offset, 0)
		#strBin=self.dataMFile.read(8)
		#value=int.from_bytes(strBin,'little')
		#print ("strOut:{} read int:{}".format(strBin.hex(),value))
			

	def mGetBin(self,offset,size):
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		#return os.read(self.dataMFile,size)
		self.dataMFile.seek(offset, 0)
		return self.dataMFile.read(size)


	def mGet(self,offset,size):
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		#line=os.read(self.dataMFile,size)
		self.dataMFile.seek(offset, 0)
		line=self.dataMFile.read(size)
		
		return line.decode('utf-8')
	
	def mGetInt(self,offset):
		#print ('of {}'.format(offset))
		#os.lseek(self.dataMFile,offset,os.SEEK_SET)
		#strBin=os.read(self.dataMFile,8)
		self.dataMFile.seek(offset, 0)
		strBin=self.dataMFile.read(8)
		return int.from_bytes(strBin,'little')
			
	def setSpace(self,space):
		if(self.vectorID==0xffffffff):
			if(self.dataLocation==MEMORY_LOCATION):
				print ("MEMORY_LOCATION")
				pass
			else:
				self.dataMFile.truncate(space)
				self.poolSize=space
		else:
			print ("no valid GVector")							
			
	def close(self):
		self.saveData()
		os.close(self.dataMFile)		
		
			
	#добавление новой записи в GVector
	def push_back(self,strData):
		strBin=str.encode(strData)
		size=len(strBin)	
		
		#проверяем достаточно ли места в массиве индекса
		if(self.recordArraySize<self.recordCount+1):
			self.recordArraySize=self.recordCount+1
			print ("resize GVector index recordArraySize={:,} recordCount={} self.poolSize={:,}".format(self.recordArraySize,self.recordCount,self.poolSize))
			#увеличиваем массив индекса и записываем его как новую запись
			#проверяем достаточно ли места в пуле
			if(self.recordArraySize*INDEX_RESIZE+self.dataSize>self.poolSize):
				newSize=self.poolSize+(self.recordArraySize+1)*INDEX_RESIZE
				print ('start resize pool for index. New size={:,}'.format(newSize))
				#print ("vectorID_={}".format(self.vectorID)
				self.setSpace(newSize)	
			#копируем индекс
			s=self.mGetBin(self.indexOffset,(self.recordArraySize-1)*8)
			self.mPutBin(self.dataSize,s)
			self.recordArraySize=self.recordArraySize*INDEX_RESIZE
			self.indexOffset=self.dataSize
			self.dataSize+=self.recordArraySize*8
		#cout<<" poolSize1={}".format(self.poolSize<<" dataSize={}".format(self.dataSize
		#проверяем достаточно ли места в пуле для новой записи
		if(self.dataSize+size+256>self.poolSize):
			newSize=(self.poolSize)*FILE_RESIZE+size
			if(newSize<self.dataSize+size+256):
				newSize=int((self.dataSize+size+256)*1.5)
			print ("@resize GVector file new poolSize={:,} bytes c3".format(newSize))
			self.setSpace(newSize)
			
 		#записываем адрес записи в индекс
		self.mPutInt(self.indexOffset+self.recordCount*8,self.dataSize)	
		
		#if self.recordCount>300:
		#	print (self.recordCount)
		#	offset=self.mGetInt(self.indexOffset+self.recordCount*8)
		#	print ("offset:{} address:{} self.dataSize:{} pool:{}".format(offset,self.indexOffset+self.recordCount*8, self.dataSize,self.poolSize))

		
 		#записываем данные
		self.mPutInt(self.dataSize,size)					#записываем длину записи
		self.mPutBin(self.dataSize+8,strBin)				#записываем данные записи
	
		self.recordCount=self.recordCount+1
		self.dataSize=self.dataSize+size+8
		
		self.saveData()	
		
		#print ("new data")
		#print ("innerData={}".format(self.innerData))
		#print ("poolSize={}".format(self.poolSize))
		#print ("recordCount={}".format(self.recordCount))
		#print ("recordArraySize={}".format(self.recordArraySize))
		#print ("dataSize={}".format(self.dataSize))
		#print ("indexOffset={}".format(self.indexOffset))	
		
		indexRecord=self.recordCount-1  #пропускаем индекс именных записей
		offset=self.mGetInt(self.indexOffset+indexRecord*8)
		size=self.mGetInt(offset)
		#print ('index={} offset={} size={} recordCount={}'.format(indexRecord,offset,size,self.recordCount))
		if(size+offset+8>self.dataSize):
			print ('index={} offset={} size={} recordCount={}'.format(indexRecord,offset,size,self.recordCount))
			print ("size out of range index:{}".format(indexRecord))
			sys.exit()



		
	def resize(self,size,recordSize):
		size+=1  #плюс именная запись
		if(size>self.recordCount):
			if(size>self.recordArraySize):
				self.recordArraySize=size
				if(self.recordArraySize+self.dataSize>self.poolSize):
					newSize=self.poolSize+(self.recordArraySize+1)*INDEX_RESIZE
					self.setSpace(newSize)
				#копируем индекс
				str=self.mGet(self.indexOffset,(self.recordArraySize-1)*8)
				self.mPut(self.dataSize,str)
				self.recordArraySize=self.recordArraySize*INDEX_RESIZE
				self.indexOffset=self.dataSize
				self.dataSize+=self.recordArraySize*8
			newSize=size*(recordSize+8)+self.recordArraySize*8+128	
			if(newSize>self.poolSize):
				self.setSpace(newSize)
			#инициализируем индекс записи
			for i in range(self.recordCount,size):
				self.mPutInt(self.indexOffset+i*8,0)
		self.recordCount=size
		
	def putStr(self,indexRecord,strData):
		strBin=str.encode(strData)
		sizeBin=len(strBin)
		indexRecord+=1  #пропускаем индекс именных записей
		offset=self.mGetInt(self.indexOffset+indexRecord*8)
		if(offset==0): #запись еще не инициализирована
			size=0
		else:
			size=self.mGetInt(offset)
			
		if(sizeBin>size):
			size	=sizeBin
			#указаваем что место записи свободно,записываем запись на новое место и обновляем индекс
			if(offset>0): 
				#print ("offset:{} indexRecord:{}".format(offset,indexRecord))
				self.mPutInt(offset,0)
			#проверяем достаточно ли места в пуле для новой записи
			if(self.dataSize+size+256>self.poolSize):
				newSize=(self.poolSize)*FILE_RESIZE+size*FILE_RESIZE_DELTA
				print ("@resize GVector file new poolSize={:,} bytes c1".format(newSize))
				self.setSpace(newSize)	
   		#записываем данныe
			self.mPutInt(self.dataSize,size) 	 	 	#записываем длину записи
			self.mPutBin(self.dataSize+8,strBin)		#копируем запись
			#записываем адрес записи в индекс
			self.mPutInt(self.indexOffset+indexRecord*8,self.dataSize)				
			self.dataSize=self.dataSize+size+8			
		else:
			#записываем данныe
			size=sizeBin
			self.mPutInt(offset,size) 	 				#записываем длину записи
			self.mPutBin(offset+8,strBin)				#копируем запись
		self.saveData()	
		
	def getStr(self,indexRecord):
		indexRecord+=1  #пропускаем индекс именных записей
		if(indexRecord>=self.recordCount):
			return EMPTY
		offset=self.mGetInt(self.indexOffset+indexRecord*8)
		size=self.mGetInt(offset)
		#print ('index={} offset={} size={} recordCount={}'.format(indexRecord,offset,size,self.recordCount))
		if(size+offset+8>self.dataSize):
			print ('index={} offset={} size={} recordCount={}'.format(indexRecord,offset,size,self.recordCount))
			print ("size out of range index:{}".format(indexRecord))
			sys.exit()
			return EMPTY
		return self.mGet(offset+8,size)		

	def checkIndex(self,limit):
		print ('check index')
		for i in range(limit):
			t=self.mGetInt(self.indexOffset+i*8)
			print (t)
			d=self.mGetInt(t)
			print ('    d={}'.format(d))
			
	def printStr(self,str):
		t=memoryview(str)
		g=t.tolist()
		g=g[:25]
		print (g)

'''	
#test
pathData=pathDB+"XML_DICT/_GVectorTest.bin"	
#os.unlink(pathData)	

v=GVector()
v.openData(pathData)		
print ('start')
st=v.getStr(996)
print (st)

#v.checkIndex(10)
sys.exit()
	
for i in range(1000):
	#print (i)
	#s='1234567890 wwwwwwwwwwwwwwwwwwwwwwwwwwwww 1234567890 www {}'.format(i)
	#v.push_back(s)
	s='1234567890 www {}'.format(i)
	v.putStr(i,s)
	
	st=v.getStr(i)
	if(st!=s):
		print ('no data')
		print (i)
		print ('retutn str=')
		v.printStr(st)
		print (st)
		break

print ('done')	
sys.exit()
'''	

	
class dictBase:
	def __init__(self,pathDB):
		#init inner variables
		self.path=pathDB
		self.keyTib=''
		self.keyList=list()
		self.data=list()
		self.history=list()
		self.vData=GVector()
		self.pathIndex=''  #path to index file
		self.dictKey={}
		self.dictSize=0
		self.fileSize=0
		self.step=0
		self.flagSave=0
		self.emptyStr=''
		self.emptyRec=EMPTY #dict of empty record index
		self.res=''
		self.insert=0
		self.value=''
		self.editMode=LINK
		self.mainMode=TRANSLATE
		self.id=1
		
		#инициализируем переменные путей к файлам словаря
		self.pathData=pathDB+"/_GVector.bin"			#путь к файлу базы данных словаря
		self.pathIndex=pathDB+"/_GVectorIndex.txt"		#путь к файлу  индекса словаря
		self.pathDictData=pathDB+"/TAB_DATA/"			#путь к текстовым файлам словаря

		#открываем файлы базы данных словаря
		print ("init dictionary "+ pathDB)
		self.openData()									#инициализируем экземпляр класса базы данных основного словаря

		#если словарь пустой, импортируем текстовые файлы словаря в базу данных

		if(self.dictSize==0):
			print ("import data in dictionary "+ pathDB)
			self.loadDB()
	
	def __del__(self):
		pass
		
	def openData(self):
		self.vData.openData(self.pathData)	
		
		f = None
		try:
			f=open(self.pathIndex, 'r')
		except:	
			f=open(self.pathIndex, 'w')
		f.close()
		
		f=open(self.pathIndex, 'r',newline="\n",encoding="utf-8")
		self.keyList=f.readlines()
		f.close()
		i=0
		for line in self.keyList:
			self.dictKey[line]=i
			i+=1
		#t2=time.time()
		#print 'time={}'.format(t2-t1)

		self.emptyStr=''.zfill(CHINK_SIZE)
		self.data.append('')
		self.data.append('')
		self.data.append('')
		self.dictSize=len(self.keyList)

	def loadDB(self):
		print ('load lext files in dictionary')
		if(os.path.isdir(self.pathDictData)):
			listD=os.listdir(self.pathDictData)
		else: 
			print (self.pathDictData+" is not valid path")
		for line in listD:
			if(line[0]=='.'):
				continue
			print (line)		
			self.loadDataFile(self.pathDictData+line,'')
			self.saveInd()		
		
	def close(self):
		self.vData.close()
		if(self.flagSave==1):
			f=open(pathIndex, 'w',newline="\n",encoding="utf-8")
			f.writelines(self.keyList,)
			f.close()	
	
	def has_key(self,key):
		if(key in self.dictKey):
			str=self.dictKey[key]
			c=int(str)
			return c
		else:
			return -1
			
	def get(self,key):
		self.res=''
		if(len(self.keyList)==0):
			print ('no data')
			return self.res
		i=self.has_key(key+'\n')	
		#print ("index:{}".format(i))
		if(i>EMPTY):
			self.res=self.vData.getStr(i)
			return self.res 
		return self.res
			
	
	def put(self,key,value):
		if(self.step>10000):  #progress
			self.step=0
			#print ('{} {}'.format(self.insert,len(self.keyList)))
		self.step+=1
		self.insert+=1
		
		i=self.has_key(key+'\n')
		#print ('has key={}'.format(i))
		if(i==EMPTY):
			self.flagSave=1
			self.dictKey[key+'\n']=len(self.keyList)
			self.keyList.append(key+'\n')
			self.vData.push_back(value)
		else:
			self.vData.putStr(i,value)
						
			
	def add(self,key,value):
		self.get(key)
		str=self.res
		if(len(str)):
			str=str+END_MARK+value
		else:
			str=key+':|:'+value
		self.put(key,str)
				
	def push(self,key,value):
		self.get(key)
		str=self.res
		if(len(str)):
			str=value+END_MARK+str
		else:
			str=key+':|:'+value
		self.put(key,str)
		
	def rep(self,key,value,dName):
		'''
		self.get(key)
		str=self.res
		if(len(str)):
			c=str.split(END_MARK)
			str=''
			for line in c:
				if(dName in line):
					continue
				str+=line+END_MARK
			str+=value
		else:
			str=key+':|:'+value
		self.put(key,str)
		'''
		
	def saveInd(self):
		with open(self.pathIndex, 'w', newline="\n", encoding='utf-8') as f:
			f.writelines(self.keyList)
			#print 'done save'
		self.insert=0
		self.step=0
		f.close()
	
	def rem(self,key):
		key_n=key+'\n'
		if(key_n in self.dictKey):
			self.put(key,EMPTY_MARK)
			
	def clear(self):
		f=open(pathIndex, 'w', newline="\n", encoding='utf-8')
		f.close()
		self.vData.resize(0,128)
		self.vData.saveData()
		self.keyList=list()
		self.dictKey={}
		
	def normalisation(self):
		step=0
		for i in range(1,len(self.keyList)):
			if(step>=1000):
				print (i)
				step=0
			step+=1
			str=self.vData.getStr(i)
			lines=str.split(MARK)
			if(len(lines)<4):
				continue
			if(len(str)):
				str=re.sub(r'^[^:]*:\|:', '',str)
				if(len(str)<10):
					print ('no data in str')
					print (i)
					#print str
				else:
					self.vData.putStr(i,str)
			else:
				print ('no data')
				print (i)
		
	def loadDataFile(self,fileName,mode):
		fLines=fileName.split('.')
		ext=fLines[len(fLines)-1]
		if(ext=="txt"):
			self.loadTXT(fileName,mode)
		if(ext=="tab"):
			self.loadTAB(fileName,'put')
		if(ext=="xml"):
			self.loadTAB(fileName,'add')
	
	def loadTXT(self,fileName,mode):	
		print ('load TXT {} mode {}'.format(fileName,mode))
		fLines=fileName.split('/')
		fName=fLines[len(fLines)-1]
		
		with open(fileName, newline="\n", encoding='utf-8') as f:
			str=f.read()
			f.close()
			self.add(fName,str)
			
	
		
	def loadTAB(self,fileName,mode):
		print ('load TAB {} mode {}'.format(fileName,mode))

		with open(fileName, newline="\n", encoding='utf-8') as f:
			str=f.read()
			f.close()
			str=str.replace('\r','\n')
			d=str.split('\n')
			print (len(d))
			name= re.sub('.*_', '', fileName)
			name= re.sub('\..*', '', name)
			if(len(name)>5):
				name='YP'
			i=0
			m=0
			if(mode=='put'):
				m=1
			if(mode=='roots'):
				m=3
			for line in d:
				#print (len(line))
				#print (line)
				line=line.replace(':|:YP','')
				line=line.replace(' @ ','\t')
				c=line.split('\t')
				if (m == 3):
					cd=c[0].split('་')
					if len(cd) ==2:
					 self.get(c[0])
					 if self.res!='':
					 	 continue
					else:
						continue;
				i+=1
				global printKey
				if i>333360:
					printKey=1;	
				
				if(len(c)>1 and len(c[0])<1048):
					str=c[1]+MARK+name
					if m==1 or m==3:
						self.put(c[0],str)
					else:
						self.add(c[0],str)
					#self.rep(c[0],str,':|:'+name)
				else:
					if(len(line)>0):
						print ('no valid record '+line[0:128])
						print (i)
						
		print ("doneImport")		

	def export(self,path):
		searchText='{}'.format(len(self.keyList))
		with open(path,'w',  newline="\n", encoding='utf-8') as f:
			res=list()
			step=0
			i=0
			for line in self.keyList:
				if(step==1000):
					step=0
					searchText='{}'.format(i)
				i+=1
				step+=1
				key=line[0:len(line)-1]
				#print (key) 
				s=self.get(key)
				#print (str)
				res.append(key+'\t'+str(s)+'\n')
			f.writelines(res)
		print('done export')
		