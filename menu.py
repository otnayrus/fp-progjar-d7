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
	logo = pygame.image.load('ww_logo.png')
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
	pygame.quit()
	quit()

def game_intro():
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
		draw_button("Create Room",20,"freesansbold.ttf",white,100,450,150,100,green,bright_green,None)
		draw_button("Join Room",20,"freesansbold.ttf",white,550,450,150,100,dark_blue,bright_blue,None)
		pygame.display.update()
		clock.tick(60)




game_intro()
pygame.quit()			