import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)
dark_blue = (0,0,100)
bright_green = (0,255,0)
bright_blue = (0,0,210)


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Werewolf")
clock = pygame.time.Clock()

def logo(x,y):
	logo = pygame.image.load('img/ww_logo.png')
	gameDisplay.blit(logo,(x,y))

def text_objects(text,font,color):
	textSurface = font.render(text,True,color)
	return textSurface, textSurface.get_rect()

def createText(text,font,size,color,x,y):
	largeText = pygame.font.Font(font, size)
	TextSurf, TextRect = text_objects(text,largeText,color)
	# print "anjaaay : "+repr(TextRect.center)
	TextRect.center=x,y
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()

def draw_button(text,text_size,font,font_color,x,y,width,height,color1,color2,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	# print click
	if x+width > mouse[0] > x and y+height > mouse[1] > y:
		pygame.draw.rect(gameDisplay, color2, (x,y,width,height))
		if click[0] == 1 and action != None:
			action()
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
	logo(display_width*0.35,display_height*0.20)
	createText("Werewolf with chat and socket","freesansbold.ttf",50,black,display_width/2,display_height*0.1)
	while intro :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				intro = False 
			print(event)
		mouse = pygame.mouse.get_pos()
		# print mouse
		draw_button("Create Room",20,"freesansbold.ttf",white,100,450,150,100,green,bright_green,create_room)
		draw_button("Join Room",20,"freesansbold.ttf",white,550,450,150,100,dark_blue,bright_blue,join_room)
		pygame.display.update()
		clock.tick(60)
	pygame.display.update()

def form(index,a,b,c,d,color1,color2,font,font_size,font_color,events):
	global text
	global active
	global create_room
	global color
	fonts = pygame.font.Font(font, font_size)
	input_box = pygame.Rect(a,b,c,d)
	# pygame.Rect.Rect(left, top, width, height)

	for event in events:
		print event
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
					text[index] = ''
				elif event.unicode == '\x08':
					text[index] = text[index][:-1]
				else:
					text[index] += event.unicode

	txt_surface = fonts.render(text[index], True, font_color)
	# Resize the box if the text[index] is too long.
	a = max(a, txt_surface.get_width()+10)
	input_box.w = a
	# Blit the text[index].
	gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))
	# Blit the input_box rect.
	pygame.draw.rect(gameDisplay, color[index], input_box,2)
	pygame.display.update()


def create_room():
	global intro
	global create_room
	global text
	global active
	global color
	active = [False,False,False]
	text = ['','','']
	color =[0,0,0]
	intro = False
	create_room = True
	gameDisplay.fill(black)

	while create_room :
		gameDisplay.fill((30,30,30))
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		create_room = False
		createText("Name.CreateRoomCode","freesansbold.ttf",50,white,display_width/2,display_height*0.4)
		form(0,(display_width/2)-150,(display_height*0.5),150,50,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,white,pygame.event.get())
		# createText("Insert Room Code","freesansbold.ttf",50,white,display_width*0.5,display_height*0.5)
		# form(1,(display_width*0.5)-150,200,150,32,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,pygame.event.get())
		# print(event)
		pygame.display.update()
		clock.tick(30)

def join_room():
	global intro
	global create_room
	global text
	global active
	global color
	active = [False,False,False]
	text = ['','','']
	color =[0,0,0]
	intro = False
	join_room = True
	gameDisplay.fill(black)

	while join_room :
		gameDisplay.fill((30,30,30))
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		join_room = False
		createText("Name.JoinRoomCode","freesansbold.ttf",50,white,display_width/2,display_height*0.4)
		form(0,(display_width/2)-150,(display_height*0.5),150,50,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,white,pygame.event.get())
		# createText("Insert Room Code","freesansbold.ttf",50,white,display_width*0.5,display_height*0.5)
		# form(1,(display_width*0.5)-150,200,150,32,pygame.Color('lightskyblue3'),pygame.Color('dodgerblue2'),None,32,pygame.event.get())
		# print(event)
		pygame.display.update()
		clock.tick(30)

def try_room():
	font = pygame.font.Font(None, 32)
	clock = pygame.time.Clock()
	input_box = pygame.Rect(200, 100, 140, 32)
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
	active = False
	text = ''
	create_room = False

	while not create_room:
		for event in pygame.event.get():
			print event
			if event.type == pygame.QUIT:
				create_room = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				# If the user clicked on the input_box rect.
				if input_box.collidepoint(event.pos):
					# Toggle the active variable.
					active = not active
				else:
					active = False
				# Change the current color of the input box.
				color = color_active if active else color_inactive
			if event.type == pygame.KEYDOWN:
				if active:
					if event.key == pygame.K_RETURN:
						print(text)
						text = ''
					elif event.key == pygame.K_BACKSPACE:
						text = text[:-1]
					else:
						text += event.unicode

		gameDisplay.fill(black)
		createText("Insert Room Code","freesansbold.ttf",50,white,display_width/2,display_height*0.1)

		# Render the current text.
		txt_surface = font.render(text, True, color)
		# Resize the box if the text is too long.
		width = max(200, txt_surface.get_width()+10)
		input_box.w = width
		# Blit the text.
		gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))
		# Blit the input_box rect.
		pygame.draw.rect(gameDisplay, color, input_box, 2)
		pygame.display.update()
		# pygame.display.flip()
		clock.tick(30)


# try_room()
# create_room()
game_intro()
pygame.quit()			