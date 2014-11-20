#!/usr/bin/python2
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#import socks
#import socket
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 2311)
#socket.socket = socks.socksocket
import urllib2

f=open('words.txt')
words=f.read()
f.close()
resultfile=open('result.csv','w')
resultfile.write('Original\tWord\tPart of Speech\tEng Meaning\tChn Meaning\tSentence\n')
words=words.split('\n')
for i in words:
	jsondata=json.loads(urllib2.urlopen('http://api.pearson.com/v2/dictionaries/entries?headword=%s'%i).read())
	f.close()
	log=open('log','w')
	log.write(words.index(i))
	log.close()
	print 'json loaded successfully for',i
	eng={}
	chn={}
	for j in jsondata['results']:
		if 'laad3' in j['datasets']:
			eng=j
			break
	for j in jsondata['results']:
		if 'ldec' in j['datasets']:
			chn=j
			break
	print 'meanings found successfully for',i
	if chn=={}:chn['senses']=[{'translation':''}]
	if eng=={}:eng={'headword':'','part_of_speech':'',}
	if 'senses' not in eng:eng['senses']=[{'definition':''}]
	if 'examples' not in eng['senses'][0]:eng['senses'][0]['examples']=[{'text':''}]
	if eng!=chn!={}:resultfile.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(i,eng['headword'],eng['part_of_speech'],eng['senses'][0]['definition'],chn['senses'][0]['translation'],eng['senses'][0]['examples'][0]['text']))
resultfile.close()
