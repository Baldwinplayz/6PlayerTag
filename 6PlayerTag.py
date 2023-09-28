# Credits to Baldwin Huang the creator

import pygame
from pygame.locals import *
import sys
import random
import threading
import time
import json
from tkinter import *
from PIL import Image, ImageTk

with open('Sprites/settings.json', 'r') as file:
	settings = json.loads(file.read())

# Tkinter Functions

def openMenu():
	global homeButton

	canvas.itemconfigure(settingsButtonID, state='hidden')
	canvas.itemconfigure(playButtonID, state='hidden')
	canvas.itemconfigure(homeButtonID, state='normal')
	canvas.itemconfigure(optionsPlatformID, state='normal')
	canvas.itemconfigure(playersMenuID, state='normal')
	canvas.itemconfigure(doubleJumpMenuID, state='normal')
	canvas.itemconfigure(movingPlatformMenuID, state='normal')
	canvas.itemconfigure(setSettingsButtonID, state='normal')

def openHome():
	global settingsButton, playButton

	canvas.itemconfigure(doubleJumpMenuID, state='hidden')
	canvas.itemconfigure(playersMenuID, state='hidden')
	canvas.itemconfigure(homeButtonID, state='hidden')
	canvas.itemconfigure(optionsPlatformID, state='hidden')
	canvas.itemconfigure(movingPlatformMenuID, state='hidden')
	canvas.itemconfigure(setSettingsButtonID, state='hidden')
	canvas.itemconfigure(settingsButtonID, state='normal')
	canvas.itemconfigure(playButtonID, state='normal')

def updateSettings():
	settings['Players'] = intListVar.get()
	if optionListVar.get() == 'Yes':
		settings['doubleJump'] = True
	elif optionListVar.get() == 'No':
		settings['doubleJump'] = False
	if optionListVar2.get() == 'Yes':
		settings['movingPlatforms'] = True
	elif optionListVar2.get() == 'No':
		settings['movingPlatforms'] = False
	with open('Sprites/settings.json', 'w') as file:
		file.write(json.dumps(settings, indent=4))
	openHome()

root = Tk()
root.geometry('500x400')
root.title('Tag But Cheap')
root.protocol('WM_DELETE_WINDOW', quit)
root.resizable(False, False)

bgImage = PhotoImage(file='Sprites/backgroundHomeScreen.png')
settingsButtonImage = Image.open('Sprites/settingsButton.png')
settingsButtonImage = settingsButtonImage.resize((int(91*2.5), int(29*2.5)), resample=Image.BILINEAR)
settingsButtonImage = ImageTk.PhotoImage(settingsButtonImage)

playButtonImage = Image.open('Sprites/playImage.png')
playButtonImage = playButtonImage.resize((int(91*2.5), int(29*2.5)), resample=Image.BILINEAR)
playButtonImage = ImageTk.PhotoImage(playButtonImage)

homeButtonImage = Image.open('Sprites/homeButton.png')
homeButtonImage = homeButtonImage.resize((int(91), int(29)), resample=Image.BILINEAR)
homeButtonImage = ImageTk.PhotoImage(homeButtonImage)

optionsPlatformImage = Image.open('Sprites/optionsPlatform.png')
optionsPlatformImage = optionsPlatformImage.resize((300, 300), resample=Image.BILINEAR)
optionsPlatformImage = ImageTk.PhotoImage(optionsPlatformImage)

saveButtonImage= Image.open('Sprites/saveButton.png')
saveButtonImage = saveButtonImage.resize((int(91*1.5), int(29*1.5)), resample=Image.BILINEAR)
saveButtonImage = ImageTk.PhotoImage(saveButtonImage)

canvas = Canvas(root, width = 500, height=400)
canvas.pack()

bg_label = Label(canvas, image=bgImage)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire Canvas

# The option list for the playerMenu
intList = (1, 2, 3, 4, 5, 6)
intListVar = IntVar()
intListVar.set(int(settings['Players']))

# Options for Double Jump
optionList = ('Yes', 'No')
optionListVar = StringVar()
optionListVar.set(settings['doubleJump'])
if settings['doubleJump'] == 1:
	optionListVar.set('Yes')
elif settings['doubleJump'] == 0:
	optionListVar.set('No')

# Options for Moving Platforms
optionList2 = ('Yes', 'No')
optionListVar2 = StringVar()
if settings['movingPlatforms'] == 1:
	optionListVar2.set('Yes')
elif settings['movingPlatforms'] == 0:
	optionListVar2.set('No')

settingsButton = Button(root, padx=0, pady=0, borderwidth=0, image=settingsButtonImage, command=openMenu)
playButton = Button(root, padx=0, pady=0, borderwidth=0, image=playButtonImage, command=root.destroy)
optionsPlatform = Label(root, image=optionsPlatformImage)
homeButton = Button(root, padx=0, pady=0, borderwidth=0, image=homeButtonImage, command=openHome)
playersMenu = OptionMenu(root, intListVar, *intList)
playersMenu.configure(background='#858585')
doubleJumpMenu = OptionMenu(root, optionListVar, *optionList)
doubleJumpMenu.configure(background='#858585')
movingPlatformMenu = OptionMenu(root, optionListVar2, *optionList2)
movingPlatformMenu.configure(background='#858585')
setSettingsButton = Button(root, padx=0, pady=0, borderwidth=0, image=saveButtonImage, command=updateSettings)

# Configuring playersMenu
playersMenu.config(width=5)

# Configuring doubleJumpMenu
doubleJumpMenu.config(width=5)

# Configuring movingPlatformMenu
movingPlatformMenu.config(width=5)

settingsButtonID = canvas.create_window(250, 200, window=settingsButton)
playButtonID = canvas.create_window(250, 300, window=playButton)
optionsPlatformID = canvas.create_window(250, 200, window=optionsPlatform)
homeButtonID = canvas.create_window(55, 25, window=homeButton)
playersMenuID = canvas.create_window(300, 166, window=playersMenu)
doubleJumpMenuID = canvas.create_window(300, 199, window=doubleJumpMenu)
movingPlatformMenuID = canvas.create_window(300, 232, window=movingPlatformMenu)
setSettingsButtonID = canvas.create_window(250, 285, window=setSettingsButton)

canvas.itemconfigure(optionsPlatformID, state='hidden')
canvas.itemconfigure(homeButtonID, state='hidden')
canvas.itemconfigure(playersMenuID, state='hidden')
canvas.itemconfigure(doubleJumpMenuID, state='hidden')
canvas.itemconfigure(movingPlatformMenuID, state='hidden')
canvas.itemconfigure(setSettingsButtonID, state='hidden')

root.mainloop()

pygame.init()

icon_image = pygame.image.load('Sprites/Tag.png')
pygame.display.set_icon(icon_image)

vec = pygame.math.Vector2  # 2 for two-dimensional

# These can be modified
Players = settings['Players']
ACC = settings['ACC']
FRIC = settings['FRIC']
doubleJump = settings['doubleJump']
movingPlatforms = settings['movingPlatforms']

FPS = 60
HEIGHT = 600
WIDTH = 1000

font = pygame.font.Font('Sprites/ARCADECLASSIC.TTF', 72)

second3 = pygame.font.Font('Sprites/ARCADECLASSIC.TTF', 12)

FramePerSec = pygame.time.Clock()

backgroundImage = pygame.image.load('Sprites/background.png')
backgroundImage = pygame.transform.scale(backgroundImage, (1000, 650))

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tag But Cheap")

class Player(pygame.sprite.Sprite):

	def __init__(self, initial_position, images: dict):
		super().__init__() 
		self.it = False
		self.surf = pygame.Surface((16, 16), pygame.SRCALPHA)
		self.rect = self.surf.get_rect(center=initial_position)
		self.images = images
		self.direction = ''
		self.pos = vec(initial_position)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.addedACC = 0
		if doubleJump:
			self.jumpsLeft = 2
		else:
			self.jumpsLeft = 1

	def move(self, kleft, kright):
		self.acc = vec(0, 0.5)

		pressed_keys = pygame.key.get_pressed()
			
		if pressed_keys[kleft]:
			self.acc.x = -(ACC + self.addedACC) 
			if self.it:
				self.setImage(self.images['LEFT-ITIS-MOVE'], 'LEFT')
			else:
				self.setImage(self.images['LEFT-NOTIT-MOVE'], 'LEFT')
		if pressed_keys[kright]:
			self.acc.x = (ACC + self.addedACC) 
			if self.it:
				self.setImage(self.images['RIGHT-ITIS-MOVE'], 'RIGHT')
			else:
				self.setImage(self.images['RIGHT-NOTIT-MOVE'], 'RIGHT')        

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if round(self.vel[0]) == 0:
			if self.direction == 'LEFT':
				if self.it:
					self.setImage(self.images['LEFT-ITIS-STILL'], 'LEFT')
				else:
					self.setImage(self.images['LEFT-NOTIT-STILL'], 'LEFT')
			if self.direction == 'RIGHT':
				if self.it:
					self.setImage(self.images['RIGHT-ITIS-STILL'], 'RIGHT')
				else:
					self.setImage(self.images['RIGHT-NOTIT-STILL'], 'RIGHT')

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
			
		self.rect.midbottom = self.pos
	
	def update(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		if self.vel.y > 0:        
			if hits:
				self.vel.y = 0
				self.pos.y = hits[0].rect.top + 1
				if doubleJump:
					self.jumpsLeft = 2
	
	def jump(self):
		if not doubleJump:
			hits = pygame.sprite.spritecollide(self, platforms, False)
			if hits:
				self.vel.y = -12
		else:
			if self.jumpsLeft > 0:
				self.vel.y = -12
				self.jumpsLeft -= 1
			
	def tag(self, person_tagged):
		person_tagged.it = True
		self.it = False

	def setImage(self, image, imageDirection):
		self.image = pygame.transform.scale(image, (64, 64))
		self.direction = imageDirection

class platform(pygame.sprite.Sprite):
	def __init__(self, fill, rect, size):
		super().__init__()
		self.surf = pygame.Surface(size)
		self.surf.fill(fill)
		self.rect = self.surf.get_rect(center=rect)
		self.vel = 0
		self.canMove = True
		if movingPlatforms:
			self.vel = random.uniform(-2, 2)

	def update(self):
		if self.canMove:
			self.rect.x -= self.vel

			if self.rect[0] + 200 > WIDTH:
				self.vel = self.vel * -1
			if self.rect[0] < 0:
				self.vel = self.vel * -1

def wait3():
	global canTag
	global timeUntilTag

	timeUntilTag = 3
	time.sleep(1)
	timeUntilTag = 2
	time.sleep(1)
	timeUntilTag = 1
	time.sleep(1)
	canTag = True

# All the images for teh sprites
	
LEFT_P1_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P1-NOTIT-MOVE.png')
LEFT_P1_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P1-NOTIT-STILL.png')
LEFT_P1_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P1-ITIS-MOVE.png')
LEFT_P1_ITIS_STILL = pygame.image.load('Sprites/LEFT-P1-ITIS-STILL.png')
LEFT_P2_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P2-NOTIT-MOVE.png')
LEFT_P2_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P2-NOTIT-STILL.png')
LEFT_P2_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P2-ITIS-MOVE.png')
LEFT_P2_ITIS_STILL = pygame.image.load('Sprites/LEFT-P2-ITIS-STILL.png')
LEFT_P3_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P3-NOTIT-MOVE.png')
LEFT_P3_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P3-NOTIT-STILL.png')
LEFT_P3_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P3-ITIS-MOVE.png')
LEFT_P3_ITIS_STILL = pygame.image.load('Sprites/LEFT-P3-ITIS-STILL.png')
LEFT_P4_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P4-NOTIT-MOVE.png')
LEFT_P4_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P4-NOTIT-STILL.png')
LEFT_P4_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P4-ITIS-MOVE.png')
LEFT_P4_ITIS_STILL = pygame.image.load('Sprites/LEFT-P4-ITIS-STILL.png')
LEFT_P5_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P5-NOTIT-MOVE.png')
LEFT_P5_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P5-NOTIT-STILL.png')
LEFT_P5_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P5-ITIS-MOVE.png')
LEFT_P5_ITIS_STILL = pygame.image.load('Sprites/LEFT-P5-ITIS-STILL.png')
LEFT_P6_NOTIT_MOVE = pygame.image.load('Sprites/LEFT-P6-NOTIT-MOVE.png')
LEFT_P6_NOTIT_STILL = pygame.image.load('Sprites/LEFT-P6-NOTIT-STILL.png')
LEFT_P6_ITIS_MOVE = pygame.image.load('Sprites/LEFT-P6-ITIS-MOVE.png')
LEFT_P6_ITIS_STILL = pygame.image.load('Sprites/LEFT-P6-ITIS-STILL.png')
RIGHT_P1_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P1-NOTIT-MOVE.png')
RIGHT_P1_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P1-NOTIT-STILL.png')
RIGHT_P1_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P1-ITIS-MOVE.png')
RIGHT_P1_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P1-ITIS-STILL.png')
RIGHT_P2_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P2-NOTIT-MOVE.png')
RIGHT_P2_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P2-NOTIT-STILL.png')
RIGHT_P2_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P2-ITIS-MOVE.png')
RIGHT_P2_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P2-ITIS-STILL.png')
RIGHT_P3_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P3-NOTIT-MOVE.png')
RIGHT_P3_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P3-NOTIT-STILL.png')
RIGHT_P3_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P3-ITIS-MOVE.png')
RIGHT_P3_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P3-ITIS-STILL.png')
RIGHT_P4_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P4-NOTIT-MOVE.png')
RIGHT_P4_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P4-NOTIT-STILL.png')
RIGHT_P4_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P4-ITIS-MOVE.png')
RIGHT_P4_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P4-ITIS-STILL.png')
RIGHT_P5_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P5-NOTIT-MOVE.png')
RIGHT_P5_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P5-NOTIT-STILL.png')
RIGHT_P5_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P5-ITIS-MOVE.png')
RIGHT_P5_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P5-ITIS-STILL.png')
RIGHT_P6_NOTIT_MOVE = pygame.image.load('Sprites/RIGHT-P6-NOTIT-MOVE.png')
RIGHT_P6_NOTIT_STILL = pygame.image.load('Sprites/RIGHT-P6-NOTIT-STILL.png')
RIGHT_P6_ITIS_MOVE = pygame.image.load('Sprites/RIGHT-P6-ITIS-MOVE.png')
RIGHT_P6_ITIS_STILL = pygame.image.load('Sprites/RIGHT-P6-ITIS-STILL.png')

# The sprites of the game

PT1 = platform((53, 37, 23), (WIDTH/2, HEIGHT - 10), (WIDTH, 20))
PT1.canMove = False
PT2 = platform((53, 37, 23), (175, 500), (200, 20))
PT3 = platform((53, 37, 23), (825, 500), (200, 20))
PT4 = platform((53, 37, 23), (450, 400), (200, 20))
PT5 = platform((53, 37, 23), (600, 300), (200, 20))
PT6 = platform((53, 37, 23), (400, 200), (200, 20))
PT7 = platform((53, 37, 23), (125, 325), (200, 20))
PT8 = platform((53, 37, 23), (800, 175), (200, 20))

P1 = Player((20, 385), {'LEFT-NOTIT-STILL': LEFT_P1_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P1_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P1_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P1_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P1_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P1_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P1_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P1_ITIS_MOVE, 
						})
P2 = Player((980, 385), {'LEFT-NOTIT-STILL': LEFT_P2_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P2_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P2_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P2_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P2_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P2_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P2_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P2_ITIS_MOVE, 
						})
P3 = Player((60, 385), {'LEFT-NOTIT-STILL': LEFT_P3_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P3_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P3_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P3_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P3_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P3_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P3_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P3_ITIS_MOVE, 
						})
P4 = Player((940, 385), {'LEFT-NOTIT-STILL': LEFT_P4_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P4_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P4_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P4_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P4_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P4_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P4_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P4_ITIS_MOVE, 
						})
P5 = Player((100, 385), {'LEFT-NOTIT-STILL': LEFT_P5_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P5_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P5_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P5_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P5_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P5_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P5_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P5_ITIS_MOVE, 
						})
P6 = Player((900, 385), {'LEFT-NOTIT-STILL': LEFT_P6_NOTIT_STILL, 
						'RIGHT-NOTIT-STILL': RIGHT_P6_NOTIT_STILL, 
						'LEFT-ITIS-STILL': LEFT_P6_ITIS_STILL, 
						'RIGHT-ITIS-STILL': RIGHT_P6_ITIS_STILL, 
						'LEFT-NOTIT-MOVE': LEFT_P6_NOTIT_MOVE, 
						'RIGHT-NOTIT-MOVE': RIGHT_P6_NOTIT_MOVE, 
						'LEFT-ITIS-MOVE': LEFT_P6_ITIS_MOVE, 
						'RIGHT-ITIS-MOVE': RIGHT_P6_ITIS_MOVE, 
						})  # Adjust the initial position for the second player
platforms = pygame.sprite.Group()
platforms.add(PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8)
  # Add both players to the group

entities = list()

if Players >= 1:
	entities.append(P1)
	all_sprites.add(P1)
	P1.setImage(RIGHT_P1_NOTIT_STILL, 'RIGHT')

if Players >= 2:
	entities.append(P2)
	all_sprites.add(P2)
	P2.setImage(LEFT_P2_NOTIT_STILL, 'LEFT')

if Players >= 3:
	entities.append(P3)
	all_sprites.add(P3)
	P3.setImage(RIGHT_P3_NOTIT_STILL, 'RIGHT')

if Players >= 4:
	entities.append(P4)
	all_sprites.add(P4)
	P4.setImage(LEFT_P4_NOTIT_STILL, 'LEFT')

if Players >= 5:
	entities.append(P5)
	all_sprites.add(P5)
	P5.setImage(RIGHT_P5_NOTIT_STILL, 'RIGHT')

if Players >= 6:
	entities.append(P6)
	all_sprites.add(P6)
	P6.setImage(LEFT_P6_NOTIT_STILL, 'LEFT')

canTag = False

timeUntilTag = 0

threading.Thread(target=wait3).start()

isit = random.randint(1, Players)
isit = entities[isit - 1]
isit.it = True
isit.addedACC = 0.05

if P1.it:
			P1.setImage(RIGHT_P1_ITIS_STILL, 'RIGHT')
if P2.it:
			P2.setImage(LEFT_P2_ITIS_STILL, 'LEFT')
if P3.it:
			P3.setImage(RIGHT_P3_ITIS_STILL, 'RIGHT')
if P4.it:
			P4.setImage(LEFT_P4_ITIS_STILL, 'LEFT')
if P5.it:
			P5.setImage(RIGHT_P5_ITIS_STILL, 'RIGHT')
if P6.it:
			P6.setImage(LEFT_P6_ITIS_STILL, 'LEFT')

timer = 200 * 60

gameEnd = False

while True:

	displaysurface.fill((0, 0, 0))
	displaysurface.blit(backgroundImage, (0, 0))

	for entity in all_sprites:
			entity.update()
			displaysurface.blit(entity.surf, entity.rect)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:    
			if event.key == pygame.K_w and Players >= 1:
				P1.jump()
			if event.key == pygame.K_y and Players >= 2:
				P2.jump()
			if event.key == pygame.K_p and Players >= 3:
				P3.jump()
			if event.key == pygame.K_x and Players >= 4:
				P4.jump()
			if event.key == pygame.K_b and Players >= 5:
				P5.jump()
			if event.key == pygame.K_PERIOD and Players >= 6:
				P6.jump()

	if canTag:
		for char in entities:
			if char.it == False:
				if pygame.sprite.collide_rect(isit, char):
					canTag = False
					threading.Thread(target=wait3).start()
					char.it = True
					char.addedACC = 0.05
					isit.it = False
					isit.addedACC = 0
					isit = char
					break
	else:
		second3Text = font.render(str(timeUntilTag), True, (255, 255, 255))
		displaysurface.blit(second3Text, (isit.rect[0] - 10, isit.rect[1] - 90))

	if not gameEnd:
		if Players >= 1:
			P1.move(K_q, K_e)
			displaysurface.blit(P1.image, (P1.rect[0] - 4, P1.rect[1] - 50))

		if Players >= 2:
			P2.move(K_t, K_u)
			displaysurface.blit(P2.image, (P2.rect[0] - 4, P2.rect[1] - 50))

		if Players >= 3:
			P3.move(K_o, K_LEFTBRACKET)
			displaysurface.blit(P3.image, (P3.rect[0] - 4, P3.rect[1] - 50))

		if Players >= 4:
			P4.move(K_z, K_c)
			displaysurface.blit(P4.image, (P4.rect[0] - 4, P4.rect[1] - 50))

		if Players >= 5:
			P5.move(K_v, K_n)
			displaysurface.blit(P5.image, (P5.rect[0] - 4, P5.rect[1] - 50))

		if Players >= 6:
			P6.move(K_COMMA, K_SLASH)
			displaysurface.blit(P6.image, (P6.rect[0] - 4, P6.rect[1] - 50))
	else:
		loserFont = pygame.font.Font('Sprites/half_bold_pixel-7.ttf', 96)
		loserText = loserFont.render('GAME OVER', True, (255, 0, 0))
		displaysurface.blit(loserText, (WIDTH/2 - loserText.get_width()/2, HEIGHT/2 - loserText.get_height()/2))

	if timer > 0:
		timer -= 1
		counter_text = font.render(str(int(timer/60) * 1), True, (64, 64, 64))  # Text, anti-aliasing, color

    # Blit the text onto the screen
	displaysurface.blit(counter_text, (WIDTH/2 - counter_text.get_width()/2, 10))

	pygame.display.update()

	if timer <= 0:
		gameEnd = True

	FramePerSec.tick(FPS)
