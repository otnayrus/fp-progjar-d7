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

list_of_clients = []  # Berisi IP dan Port Klien mulai dari index 1
roles = []  # Berisi Role dari Klien mulai dari index 1
client_names = []  # Berisi Nama Klien mulai dari index 1
tally = [0, 0, 0, 0, 0, 0, 0, 0, 0] # Index ke-0 tidak dipakai 
start_game = False

list_of_sides = ["villager", "werewolf", "villager", "seer", "villager", "werewolf", "villager", "villager"] 

# Game mechanism here
def werewolfGame():
    print "game start"
    roleRandomizer()
    broadcast("daftar pemain",client_names,'')
    broadcast("daftar role",roles,'')
    while True:
        # Afternoon Phase
        broadcast("afternoon", "Village at a Day, you are headed to the assembly.", '')
        count = 60
        while count != 0:
            broadcast("countdown",count,'')
            count-=1
            time.sleep(1)
        # Voting Phase
        broadcast("voting", "Vote a player to execute!", '')
        count = 30
        while count != 0:
            broadcast("countdown",count,'')
            count-=1
            time.sleep(1)
        hasil = revise("villager vote")
        if hasil == 1:
            return 0
        # Night Phase
        broadcast("night", "The darkness comes, you are in your home with candle lights.", '')
        count = 20
        while count != 0:
            broadcast("countdown",count,'')
            count-=1
            time.sleep(1)
        hasil = revise("werewolf vote")
        if hasil == 1:
            return 0
    return
        

def revise(arg):
    if arg.startswith('v'):
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            # Execute and reveal
            roles[chosen] = "Ded"
            broadcast("execute", "REVEAL message", '') # To do <<<
    elif arg.startswith('w'):
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            # Execute and reveal
            roles[chosen] = "Ded"
            broadcast("kill", "Werewolf KILLS message", '') # To do <<<
    werewolf_left = [i for i, x in enumerate(tally) if x == "werewolf"]
    if len(roles) <= len(werewolf_left) + 1 :
        # Werewolf win <<
        broadcast("werewolfwin", "Werewolf won", '')
        return 1
    elif len(werewolf_left) == 0:
        # Villager win <<
            broadcast("villagerwin", "Villager won", '')
            return 1

    tallyReset()


def roleRandomizer():
    num_participant = len(list_of_clients) - 1
    roles = list_of_sides[:num_participant]
    random.shuffle(roles)
    roles[1:], roles[0] = roles[0:], ''
    # >>> Broadcast role <<<


def tallyReset():
    for i in range(len(tally)):
        tally[i] = 0


def clientthread(conn, addr):
    while True:
        try:
            # deklarasi start_game sebagai global
            global start_game
            message_from_client = conn.recv(2048)
            message = marshal.loads(message_from_client)
            print(message)
            # pisah pesan
            pesan = []
            pesan = message.split(" ")  
            # Jika mengirim nama
            if pesan[0] == "name":
                client_names.append(pesan[1])
                print client_names
                print conn
            # Jika mengirim chat pada siang hari
            elif pesan[0] == "chat":
                mess = addr[0]
                for i in len(pesan):
                    if i == 0:
                        continue
                    mess += pesan[i] + " "
                broadcast("chat", mess, conn)
            # Voting siang
            elif pesan[0] == "vote":
                target = int(pesan[1])
                tally[target] += 1
                broadcast("vote", client_names[list_of_clients.index(conn)] + ' (' + str(list_of_clients.index(conn)) + 
                    ') agreed to execute ' + client_names[target] + ' (' + str(target) + ')\n', conn)
            # Seer Ability
            elif pesan[0] == "seer":
                target = int(pesan[1])
                message_to_seer = ["seer", str(target) + ' is ' + str(roles[target - 1])]
                to_client("seer", message_to_seer, conn)
            else:
                remove(conn)
        except:
            continue


def to_client(msg_type, message,connection):
    message_to_send = [msg_type, message]
    connection.send(marshal.dumps(message_to_send))

def broadcast(msg_type, message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                message_to_send = [msg_type, message]
                clients.send(marshal.dumps(message_to_send))
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


# Loading players
num = 0
while not start_game:
    # print start_game
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(str(addr) + " connected")
    start_new_thread(clientthread, (conn, addr))
    num += 1
    if num == 8:
        while len(client_names) < 8:
            time.sleep(1)
        start_game = True

werewolfGame()
conn.close()
server.close()