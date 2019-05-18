import socket
import select
import sys
import time
from thread import *
import marshal
import random

# -- Main

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
number_of_player = 4 # by default
start_game = False
ingame = True

list_of_sides = ["villager", "werewolf", "villager", "seer", "villager", "werewolf", "villager", "villager"] 

# -- End of main ----------------------------------------------


# --- Functions and Utilities ---
# Game mechanism here
def werewolfGame():
    global roles, ingame
    roleRandomizer()
    while ingame:
        # Afternoon Phase
        broadcast("afternoon", "Village at a Day, you are headed to the assembly.", '')
        time.sleep(1)
        # Voting Phase
        broadcast("voting", "Vote a player to execute!", '')
        print roles
        time.sleep(30)
        revise("villager vote")
        if ingame == False:
            endgame()
        # Night Phase
        broadcast("night", "The darkness comes, you are in your home with candle lights.", '')
        time.sleep(20)
        revise("werewolf vote")
        if ingame == False:
            endgame()
    endgame()
        

def revise(arg):
    global ingame,roles
    if arg.startswith('v'):
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            # Execute and reveal
            
            broadcast("execute", "The Village executed " + str(client_names[chosen[0]]) + "Turns out " + str(chosen[0]) + " is a " + str(roles[chosen[0]]), '')
            to_client("killed", "You have been slain. Thanks for playing.",list_of_clients[chosen[0]])
            roles[chosen[0]] = "Ded"
            
    elif arg.startswith('w'):
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            # Execute and reveal
            broadcast("execute", "The Werewolves kills " + str(client_names[chosen[0]]) + "Turns out " + str(chosen[0]) + " is a " + str(roles[chosen[0]]), '')
            to_client("killed", "You have been slain. Thanks for playing.",list_of_clients[chosen[0]])            
            roles[chosen[0]] = "Ded"

    # Check number of werewolves left
    werewolf_left = [i for i, x in enumerate(tally) if x == "werewolf"]

    if len(roles) - 1 <= len(werewolf_left) :
        # Werewolf win <<
        broadcast("status", "Werewolf won", '')
        time.sleep(1)
        ingame = False
    elif len(werewolf_left) == 0:
        # Villager win <<
        broadcast("status", "Villager won", '')
        time.sleep(1)
        ingame = False
    tallyReset()


def roleRandomizer():
    global roles
    num_participant = len(list_of_clients) - 1
    roles = list_of_sides[:num_participant]
    random.shuffle(roles)
    roles[1:], roles[0] = roles[0:], ''
    # Broadcast role
    for i in range(1,len(list_of_clients)):
        to_client("role", roles[i], list_of_clients[i])


def tallyReset():
    for i in range(len(tally)):
        tally[i] = 0


def clientthread(conn, addr):
    while True:
        try:
            message_from_client = conn.recv(2048)
            message = marshal.loads(message_from_client)
            print message
            print message[0]
            # Player Count
            if message[0] == "numberofplayer":
                number_of_player = int(message[1])
            # Jika mengirim nama
            elif message[0] == "name":
                client_names.append(message[1])
                print client_names
            # Jika memulai game
            elif message[0] == "start":
                start_game = True
            # Jika mengirim chat pada siang hari
            elif message[0] == "chat":
                broadcast("chat", client_names[list_of_clients.index(conn)] + " : " + message[1], conn)
            # Voting siang
            elif message[0] == "vote":
                target = int(message[1])
                tally[target] += 1
                broadcast("vote", client_names[list_of_clients.index(conn)] + ' (' + str(list_of_clients.index(conn)) + 
                    ') agreed to execute ' + client_names[target] + ' (' + str(target) + ')\n', conn)
            # Seer Ability
            elif message[0] == "seer":
                target = int(message[1])
                message_to_seer = ["seer", str(target) + ' is ' + str(roles[target])]
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
        if clients != connection and clients != '':
            try:
                message_to_send = [msg_type, message]
                clients.send(marshal.dumps(message_to_send))
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def endgame():
    for clients in list_of_clients:
        if clients != '':
            clients.close()


# Loading players
while number_of_player > 0:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(str(addr) + " connected")
    start_new_thread(clientthread, (conn, addr))
    number_of_player -= 1
    if number_of_player == 0:
        while len(client_names)<5 :
            time.sleep(1)

werewolfGame()
server.close()
