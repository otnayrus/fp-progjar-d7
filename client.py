import pygame
import threading
import socket
import marshal
from thread import *
import time

pygame.init()
players = []
namamu = ''
display_width = 800
display_height = 600

black = (0,0,0)
dark_gray = (50,50,50)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)
dark_blue = (0,0,100)
bright_green = (0,255,0)
bright_blue = (0,0,210)
role = ''
chats =[]
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Werewolf")
clock = pygame.time.Clock()

# --------------------------------------------SOCKs-
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port = 8081
server.connect((IP_address,Port))

def send_name(name):
	global namamu
	namamu = name
	server.send(marshal.dumps(["name",name]))
	wait_room_f()

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Port2 = 8082
server2.connect((IP_address,Port2))
start = "NOPE"
eventnow = ['','']
    

# ----------------------------------------------

def load_image(x,y,name):
	logo = pygame.image.load(name)
	gameDisplay.blit(logo,(x,y))

def text_objects(text,font,color):
	textSurface = font.render(text,True,color)
	return textSurface, textSurface.get_rect()

def createText(text,font,size,color,x,y):
	largeText = pygame.font.Font(font, size)
	TextSurf, TextRect = text_objects(text,largeText,color)
	TextRect.center=x,y
	gameDisplay.blit(TextSurf,TextRect)
	# pygame.display.update()

def chatText(text,font,size,color,x,y):
	largeText = pygame.font.Font(font, size)
	TextSurf, TextRect = text_objects(text,largeText,color)
	TextRect.left=x
	TextRect.top=y
	gameDisplay.blit(TextSurf,TextRect)


def draw_button(text,text_size,font,font_color,x,y,width,height,color1,color2,action=None,arg=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	# print click
	if x+width > mouse[0] > x and y+height > mouse[1] > y:
		pygame.draw.rect(gameDisplay, color2, (x,y,width,height))
		if click[0] == 1 and action != None and arg == None:
			action()
		elif click[0] == 1 and action != None and arg != None:
			action(arg)
	else:
		pygame.draw.rect(gameDisplay, color1, (x,y,width,height))
	createText(text,font,text_size,font_color,(x+(width/2)),(y+(height/2)))

def quitgame():
	global create_room
	global intro
	global join_room
	join_room = False
	intro = False
	create_room=False
	pygame.quit()
	quit()


def game_intro():
	global intro
	intro = True
	gameDisplay.fill(white)
	load_image(display_width*0.35,display_height*0.20,"img/ww_logo.png")
	createText("Werewolf with chat and socket","freesansbold.ttf",50,black,display_width/2,display_height*0.1)
	while intro :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro = False
			# print(event)
		mouse = pygame.mouse.get_pos()
		draw_button("PLAY",20,"freesansbold.ttf",white,(display_width*0.5)-75,(display_height*0.75),150,100,black,dark_gray,your_name)
		pygame.display.update()
		clock.tick(60)
	pygame.display.update()

def form(index,a,b,c,d,color1,color2,font,font_size,font_color,events,action=None):
	global text
	global active
	global create_room
	global color
	fonts = pygame.font.Font(font, font_size)
	input_box = pygame.Rect(a,b,c,d)
	# pygame.Rect.Rect(left, top, width, height)

	for event in events:
		# print event
		if event.type == pygame.QUIT:
			quitgame()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if input_box.collidepoint(event.pos):
				active[index] = not active[index]
			else :
				active[index] = False
			color[index] = color1 if active[index] else color2

		if event.type == pygame.KEYDOWN:
			# print "benar"
			if active[index]:
				if event.unicode == '\r':
					print text[index]
					if action is not None:
						action(str(text[index]))
					text[index] = ''
				elif event.unicode == '\x08':
					text[index] = text[index][:-1]
				else:
					text[index] += event.unicode

	txt_surface = fonts.render(text[index], True, font_color)
	a = max(a, txt_surface.get_width()+10)
	input_box.w = a
	gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))
	pygame.draw.rect(gameDisplay, color[index], input_box,2)
	# pygame.display.update()

def your_name():
	global intro
	global your_name
	global text
	global active
	global color
	active = [False,False,False]
	text = ['','','']
	color =[0,0,0]
	intro = False
	your_name = True
	gameDisplay.fill(black)

	while your_name :
		gameDisplay.fill((30,30,30))
		createText("Your Name","freesansbold.ttf",50,white,display_width/2,display_height*0.4)
		events=pygame.event.get()
		form(0,(display_width*0.338),(display_height*0.5),150,50,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,white,events,send_name)
		# form(1,(display_width/2)-150,(display_height*0.8),150,50,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,white,events)
		pygame.display.update()
		clock.tick(50)

def wait_room_f():
	global wait_room
	global players
	global your_name
	global start
	your_name = False
	# players = ["player a","player b","player c"]
	wait_room = True
	while wait_room:
		# print start
		gameDisplay.fill((30, 30, 30))
		height_p = 120

		createText("Waiting Room","freesansbold.ttf",50,white,display_width/2,display_height*0.1)
		for player in reversed(players):
			if player!= ' ':
				chatText(player,"freesansbold.ttf",50,white,120,height_p)
				height_p = height_p +50

		# draw_button("Start",20,"freesansbold.ttf",white,(display_width*0.5)-75,(display_height*0.75),150,100,black,dark_gray,your_role)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
		if start == "START":
			wait_room = False
			your_role_f()
		pygame.display.update()
		clock.tick(30)

def transisi(action=None):
	global eventnow
	# players = ["player a","player b","player c"]
	gameDisplay.fill((30, 30, 30))
	createText(eventnow[1],"freesansbold.ttf",20,white,display_width/2,display_height*0.1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quitgame()
	pygame.display.update()
	time.sleep(3)
	eventnow[0]=" "
	eventnow[1]=" "
	action()
	

def your_role_f():
	global your_role
	global role
	global eventnow

	your_role = True
	while your_role:
		gameDisplay.fill((30, 30, 30))
		createText("You are a","freesansbold.ttf",50,white,display_width/2,display_height*0.1)
		# print role
		if role != '':
			img = "img/role-"+role+".jpg"
			load_image(display_width*0.3,display_height*0.15,img)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
		if eventnow[0]=="afternoon":
			your_role = False
			transisi(chat_room_f)
		if eventnow[0]=="voting":
			your_role = False
			transisi(event_vote_f)
		pygame.display.update()
		clock.tick(30)

def send_vote_f(index):
	global server
	global waktu_vote
	print "voted"
	server.send(marshal.dumps(["vote",index]))
	while waktu_vote!=0:
		gameDisplay.fill((30, 30, 30))
		createText("Thank you for your vote!","freesansbold.ttf",50,white,display_width/2,display_height*0.1)
		createText("Waiting for other player...","freesansbold.ttf",50,white,display_width/2,display_height*0.3)
		pygame.display.update()
		clock.tick(30)
	your_role_f()


def event_vote_f():
	global event_vote
	global players
	global waktu_vote
	event_vote = True
	while event_vote:
		height_p = 120
		gameDisplay.fill((30, 30, 30))
		createText("VOTE","freesansbold.ttf",50,white,display_width/2,display_height*0.1)
		createText(str(waktu_vote),"freesansbold.ttf",30,white,display_width/2,display_height*0.2)
		for player in players:
			if player!='':
				draw_button(player,20,"freesansbold.ttf",white,50,height_p,100,50,dark_blue,bright_blue,send_vote_f,players.index(player))
				height_p = height_p + 60
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
		pygame.display.update()
		clock.tick(30)
		if waktu_vote==0:
			event_vote = False
			your_role_f()


def chatRender(color, text):
	global chats
	font = pygame.font.Font(None, 32)
	input_box = pygame.Rect(50, 550, 240, 32)
	height_chat = 500
	createText("Discussion Time","freesansbold.ttf",50,white,display_width/2,display_height*0.1)
	for chat in reversed(chats):
		chatText(chat,"freesansbold.ttf",20,white,50,height_chat)
		height_chat = height_chat - 20
	txt_surface = font.render(text, True, color)
	width = max(200, txt_surface.get_width()+10)
	input_box.w = width
	gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))
	pygame.draw.rect(gameDisplay, color, input_box, 2)
	pygame.display.update()


def chat_room_f():
	global chat_room
	global waktu
	global chats
	global namamu
	chats = []
	input_box = pygame.Rect(50, 550, 240, 32)
	clock = pygame.time.Clock()
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
	active = False
	text = ''
	chat_room = True
	# waktu = 30	
	chatRender(color, text)
	while chat_room:
		gameDisplay.fill((30, 30, 30))
		createText(str(waktu),"freesansbold.ttf",30,white,display_width/2,display_height*0.2)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if input_box.collidepoint(event.pos):
					active = not active
				else:
					active = False
				color = color_active if active else color_inactive
				chatRender(color, text)
			if event.type == pygame.KEYDOWN:
				if active:
					if event.key == pygame.K_RETURN:
						print(text)
						# print chats
						text2 = str(namamu)+" : "+str(text)
						server.send(marshal.dumps(["chat",text2]))
						text = ''
					elif event.key == pygame.K_BACKSPACE:
						text = text[:-1]
					else:
						text += event.unicode
		chatRender(color, text)
		if waktu==0:
			chat_room = False
			your_role_f()

def clientthread():
	global players
	global role
	global start
	global eventnow
	global waktu
	global chats
	global waktu_vote
	while True:
		msg = server2.recv(2048)
		message = marshal.loads(msg)
		print message
		if message[0] == "name":
			players = message[1]
		elif message[0] == 'role':
			role = message[1]
		elif message[0] == 'state':
			start = message[1]
		elif message[0] == 'afternoon':
			eventnow[0] = message[0]
			eventnow[1] = message[1]
		elif message[0] == 'voting':
			eventnow[0] = message[0]
			eventnow[1] = message[1]
		elif message[0] == 'chat_time':
			waktu = message[1]
		elif message[0] == 'vote_time':
			waktu_vote = message[1]
		elif message[0] == 'chat':
			chats.append(message[1])

start_new_thread(clientthread,())
game_intro()
#chat_room()
pygame.quit()

# ---------------------------------------------------------------------------------------------------

