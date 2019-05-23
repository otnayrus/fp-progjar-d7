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

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address2 = '127.0.0.1'
Port2 = 8082
server2.bind((IP_address, Port2))
server2.listen(10)

list_of_clients = ['']  # Berisi IP dan Port Klien mulai dari index 1
list_of_clients2 = ['']
roles = ['']  # Berisi Role dari Klien mulai dari index 1
client_names = ['']  # Berisi Nama Klien mulai dari index 1
tally = [0, 0, 0, 0, 0, 0, 0, 0, 0] # Index ke-0 tidak dipakai 
number_of_player = 4 # by default
number_of_name = 4
start_game = False

list_of_sides = ["villager", "werewolf", "villager", "seer", "villager", "werewolf", "villager", "villager"] 

# -- End of main ----------------------------------------------


# --- Functions and Utilities ---
# Game mechanism here
def werewolfGame():
    roleRandomizer()
    time.sleep(1)
    broadcast("state","START",'')
    time.sleep(3)

    while ingame:
        time.sleep(3)
        # Afternoon Phase
        broadcast("afternoon", "Village at a Day, you are headed to the assembly.", '')
        time.sleep(3)
        waktu = 5
        while waktu > -1:
            broadcast("chat_time",waktu,'')
            time.sleep(1) 
            waktu = waktu - 1
        time.sleep(3)
        # Voting Phase
        broadcast("voting", "Vote a player to execute!", '')
        time.sleep(3)
        waktu = 5
        while waktu > -1:
            broadcast("vote_time",waktu,'')
            time.sleep(1) 
            waktu = waktu - 1
        revise("villager vote")
        # Night Phase
        for i in roles:
            if i == "werewolf":
                to_client("eat", "You werewolf wanted to kill!", list_of_clients2[roles.index(i)])
            elif i == "seer":
                to_client("seer", "Use your seer ability.", list_of_clients2[roles.index(i)])
            elif i == "villager":
                to_client("night", "The darkness comes, you are in your home with candle lights.", list_of_clients2[roles.index(i)])
        waktu = 10
        while waktu > -1:
            broadcast("vote_time",waktu,'')
            time.sleep(1) 
            waktu = waktu - 1
        revise("werewolf vote")
        time.sleep(3)
    endgame()
        

def revise(arg):
    global ingame,roles
    if arg.startswith('villager'): # villager vote
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            broadcast("execute", "The Village executed " + str(client_names[chosen[0]]) + " Turns out " + str(chosen[0]) + " is a " + str(roles[chosen[0]]), '')
            to_client("role", "Ded", list_of_clients2[chosen[0]])
            roles[chosen[0]] = "Ded"
            
    elif arg.startswith('werewolf'): # werewolf vote
        chosen = [i for i, x in enumerate(tally) if x == max(tally)]
        if len(chosen) == 1:
            broadcast("execute", "The Werewolves kills " + str(client_names[chosen[0]]) + " Turns out " + str(chosen[0]) + " is a " + str(roles[chosen[0]]), '')
            to_client("role", "Ded", list_of_clients2[chosen[0]])            
            roles[chosen[0]] = "Ded"

    # Check number of werewolves left
    werewolf_left = roles.count("werewolf")
    slain_peeps = roles.count("Ded")
    print "roles = " + str(roles)
    print "ww left = " + str(werewolf_left)
    if len(roles) - slain_peeps - 1 < werewolf_left :
        # Werewolf win <<
        broadcast("status", "Werewolf won", '')
        time.sleep(1)
        ingame = False
    elif werewolf_left == 0:
        # Villager win <<
        broadcast("status", "Villager won", '')
        time.sleep(1)
        ingame = False
    tallyReset()


def roleRandomizer():
    global roles
    num_participant = len(list_of_clients2) - 1
    roles = list_of_sides[:num_participant]
    random.shuffle(roles)
    roles[1:], roles[0] = roles[0:], ''
    # Broadcast role
    for i in range(1,len(list_of_clients2)):
        to_client("role", roles[i], list_of_clients2[i])

def tallyReset():
    for i in range(len(tally)):
        tally[i] = 0


def clientthread(conn, addr):
    global number_of_name

    while True:
        try:
            message_from_client = conn.recv(2048)
            message = marshal.loads(message_from_client)
            print str(conn) + " >> " + str(message)
            # Player Count
            if message[0] == "numberofplayer":
                number_of_player = int(message[1])
            # Jika mengirim nama
            elif message[0] == "name":
                client_names[list_of_clients.index(conn)] = message[1]
                print message[1]
                broadcast("name", client_names, '')
                number_of_name -= 1
            # Jika memulai game
            elif message[0] == "start":
                start_game = True
            # Jika mengirim chat pada siang hari
            elif message[0] == "chat":
                broadcast("chat", message[1], conn)
            # Voting siang
            elif message[0] == "vote":
                target = int(message[1])
                tally[target] += 1
                #broadcast("vote", client_names[list_of_clients.index(conn)] + ' (' + str(list_of_clients.index(conn)) + ') agreed to execute ' + client_names[target] + ' (' + str(target) + ')\n', conn)
            # Seer Ability
            elif message[0] == "seer":
                target = int(message[1])
                message_to_seer = ["seer_result", str(target) + ' is ' + str(roles[target])]
                to_client("seer_result", message_to_seer, list_of_clients2[list_of_clients.index(conn)])
            else:
                remove(conn)
        except:
            continue


def to_client(msg_type, message,connection):
    message_to_send = [msg_type, message]
    connection.send(marshal.dumps(message_to_send))

def broadcast(msg_type, message, connection):
    for clients in list_of_clients2:
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


def statethread():
    while True:
        conn, addr = server2.accept()
        list_of_clients2.append(conn)

start_new_thread(statethread,())

# Loading players
for i in range(0,number_of_player):
    client_names.append('')

while number_of_player > 0:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(str(addr) + " connected")
    start_new_thread(clientthread, (conn, addr))
    number_of_player -= 1

while number_of_name > 0:
    continue

# print "kluar"

ingame = True
werewolfGame()
server.close()
werewolfGame()
server.close()