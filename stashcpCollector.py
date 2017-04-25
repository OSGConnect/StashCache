#!/usr/bin/env python
import Queue, os, sys, time
import threading
from threading import Thread
import socket, requests
import json

import json
from datetime import datetime

import tools


#hostIP="192.170.227.128"

SUMMARY_PORT = 9951

hostIP=socket.gethostbyname(socket.gethostname())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((hostIP, SUMMARY_PORT))
sock.listen(5)

AllState={}

def eventCreator():
    aLotOfData=[]
    es_conn = tools.get_es_connection()
    while(True):
        [dat,addr]=q.get()
        #print(dat)

        d = datetime.now()
        ind="stashcp-"+str(d.year)+"."+str(d.month)
        dat['_index']=ind
        dat['_type']= 'rec'
        dat['IP']=addr
        print(dat)

        q.task_done()
               
        aLotOfData.append(dat)
        
        if len(aLotOfData) > 50:
            succ = tools.bulk_index(aLotOfData, es_conn=es_conn, thread_name=threading.current_thread().name)
            if succ is True:
                aLotOfData = []


q=Queue.Queue()
#start eventCreator threads
for i in range(1):
     t = Thread(target=eventCreator)
     t.daemon = True
     t.start()
     
nMessages=0
while (True):
    try:
        client_sock, addr = sock.accept()
        data = client_sock.recv(4096)
        data1=''
        if len(data)<200:
    	    data1= client_sock.recv(4096)
    
        #print (len(data), data, data1)
        data += data1

        response_body_raw="jebi se urllib2!"
        response_headers = {
           'Content-Type': 'text/html; encoding=utf8',
           'Content-Length': len(response_body_raw),
           'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'
        client_sock.send('%s %s %s' % (response_proto, response_status, response_status_text))
        client_sock.send(response_headers_raw)
        client_sock.send('\n') # to separate headers from body
        client_sock.send(response_body_raw)

        # and closing connection, as we stated before
        client_sock.close()
    except Exception as e:
        print e

    try:
	data=data.split('\r\n\r\n')	
	jdata=json.loads(data[1])
        #print(jdata)
	q.put([jdata,addr[0]])
    	nMessages+=1
    except IndexError:
	print("No data in the message?", data)
    except Exception as e:
        print e

    if (nMessages%100==0):
        print("messages received:",nMessages, "   qsize:", q.qsize())

print(" ERROR - unexpected exit.")
