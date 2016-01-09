#!/usr/bin/env python

import socket
import binascii
import threading
import time
import json

reconnect_flag = 0

class Live:
    #public variable
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    key = 0
    cid = 0
    
    #Initialize receiving data
    def __init__(self, cid, key):
        self.key = key
        self.cid = cid
        self.conn_ctrl(key)
        print("Initializing...")
        
    #Starting & Keeping socket connection
    def conn_ctrl(self, key):
        global reconnect_flag
        if key == 0:
            #When disconnected
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.s.connect(("livecmt.bilibili.com",88))
                handshake = "0101000c0000%04x00000000" % int(self.cid)
                self.s.send(binascii.a2b_hex(handshake))
            except:
                pass
            print("Connected")
        else:
            #When needing reconnect
            print("Disonnected")
            self.s.close()
            time.sleep(0.5)
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.s.connect(("livecmt.bilibili.com",88))
                handshake = "0101000c0000%04x00000000" % int(self.cid)
                self.s.send(binascii.a2b_hex(handshake))
            except:
                pass
            reconnect_flag = 0
            print("Connected")
    
    #Connection heart beat
    def heart_beat(self):
        while(not reconnect_flag):
            time.sleep(29)
            try:
                self.s.send(binascii.a2b_hex("01020004"))
            except:
                pass
            print("Heart beat done !")
    
            
    #core function
    def recv(self):
        global reconnect_flag
        #for i in range(0,5):
        while(1):
            #check if connection is broken
            if reconnect_flag == 1:
                break
            else:
                pass
            #receive data
            try:
                data = self.s.recv(1024)
                
            except:
                pass
            #check if data id null
            if not data: 
                reconnect_flag = 1
                continue
            #modify data
            else:
                data = data.decode('utf-8','ignore')
                data = data[3:]
                #print(data)
                self.s.setblocking(0)
                self.s.setblocking(1024)
            #try to covert to json format
            try:
                info = json.loads(data)
                try:
                    #receive danmuku info
                    output = info['info'][2][1]+':'+info['info'][1]
                    #cancel comment this in python2
                    #output = output.encode('gbk')
                    print(output)
                except:
                    pass
            except Exception as e:
                #print(e)
                pass
#create 'Live' class
now = Live(51112, 0)
#create first heart beat thread
timer = threading.Thread(target=now.heart_beat)
#create first receive thread
receiver = threading.Thread(target=now.recv)
#start first thread
timer.start()
receiver.start()
#using loop to check connection status
while(1):
    #using 'reconnect_flag' to confirm connection status
    if reconnect_flag == 1:
        #if connection broken, reconnect socket
        now.conn_ctrl(1)
        #re-create two threads
        timer.start()
        receiver.start()
        continue
    else:
        pass