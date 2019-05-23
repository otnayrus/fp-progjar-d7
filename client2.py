import socket
import select
import sys
import marshal
import threading
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port = 8081
server.connect((IP_address,Port))

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port2 = 8082
server2.connect((IP_address,Port2))

list_names = ['']
def serverthread():
	global list_names
	while True:
	    message = server2.recv(2024)
	    mess = marshal.loads(message)
	    if mess[0] == "name":
	    	list_names = mess[1]
	    print mess

start_new_thread(serverthread,())

while True:
    message = raw_input()
    if message == "name":
    	print list_names
        name = raw_input()
        kirim = ["name",name]
        server.send(marshal.dumps(kirim))
    elif message == "chat":
        chat = raw_input()
        kirim = ["chat",chat]
        server.send(marshal.dumps(kirim))
    elif message == "vote":
        vote = raw_input()
        kirim = ["vote",vote]
        server.send(marshal.dumps(kirim))
    elif message == "seer":
        seer = raw_input()
        kirim = ["seer",seer]
        server.send(marshal.dumps(kirim))  	    
    else:
        server.send(marshal.dumps(message))
    sys.stdout.flush()
    
server.close()