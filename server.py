import socket
import select
import sys
import time
from thread import *
import marshal
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '127.0.0.1'
Port = 8081
server.bind((IP_address, Port))
server.listen(10)

list_of_clients = ['']  # Berisi IP dan Port Klien mulai dari index 1
roles = ['']  # Berisi Role dari Klien mulai dari index 1
client_names = ['']  # Berisi Nama Klien mulai dari index 1
tally = [0, 0, 0, 0, 0, 0, 0, 0, 0] # Index ke-0 tidak dipakai
queue_act = []
start_game = False

list_of_sides = ["villager", "werewolf", "villager", "seer", "villager", "werewolf", "villager", "villager"] 

# Loading players
while not start_game:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(str(addr[1]) + " connected")
    start_new_thread(clientthread, (conn, addr))

werewolfGame()
conn.close()
server.close()


# Game mechanism starts
def werewolfGame():
    roleRandomizer()
    while True:
        # To do game
        return
        

def roleRandomizer():
    num_participant = len(list_of_clients) - 1
    roles = list_of_sides[:num_participant]
    random.shuffle(roles)
    roles[1:], roles[0] = roles[0:], ''

def tallyReset():
    for i in range(len(tally)):
        tally[i] = 0


def clientthread(conn, addr):
    while True:
        try:
            message_from_client = conn.recv(2048)
            message = marshal.loads(message_from_client)
            # Jika mengirim nama
            if message[0] == "name":
                client_names.append(message[1])
            # Jika memulai game
            elif message[0] == "start":
                start_game = True
            # Jika mengirim chat pada siang hari
            elif message[0] == "chat":
                broadcast(message[1], conn)
            # Voting siang
            elif message[0] == "vote":
                target = int(message[1])
                tally[target] += 1
                broadcast(client_names[list_of_clients.index(conn)] + ' (' + str(list_of_clients.index(conn)) + 
                    ') agreed to execute ' + client_names[target] + ' (' + str(target) + ')\n', conn)
            # Seer Ability
            elif message[0] == "seerability":
                target = int(message[1])
                message_to_seer = ["seer", str(target) + ' is ' + str(roles[target - 1])]
                conn.send(marshal.dumps(message_to_seer))
            else:
                remove(conn)
        except:
            continue


def to_client(message,connection):
    message_to_send = ["chat", message]
    connection.send(marshal.dumps(message_to_send))

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                message_to_send = ["chat", message]
                clients.send(marshal.dumps(message_to_send))
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)