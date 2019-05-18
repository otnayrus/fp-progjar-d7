import socket
import select
import sys
import marshal

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port = 8081
server.connect((IP_address,Port))

while True:
	socket_list = [sys.stdin, server]
	read_socket,write_socket,error_socket = select.select(socket_list,[],[])

	for socks in read_socket:
		if socks == server:
			message = socks.recv(2024)
			mess = marshal.loads(message)
			print mess
		else :
			# message = sys.stdin.readline()
			message = raw_input()
			if message == "name":
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
			else server.send(marshal.dumps(message))
			sys.stdout.flush()
server.close()