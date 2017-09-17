import pygame
from pygame import *
import os
import random
from random import randint
from tileset import *
from player import *
from bullet import Bullet
from enemy import *
from item import *

def loadControls(p1,p2):
	tempFile = open("keyconfig.txt")
	tcontrols = tempFile.readlines()
	for i in xrange(3):
		tcontrols[i] = tcontrols[i].split("=")
		p1.keys[tcontrols[i][0]] = tcontrols[i][1].rstrip()
	for i in range(3):
		tcontrols[i+3] = tcontrols[i+3].split("=")
		p2.keys[tcontrols[i+3][0]] = tcontrols[i+3][1].rstrip()

def main():
	pygame.init()
	pygame.font.init()
	debugFont = font.Font(None, 12)
	debugFont2 = font.Font(None,16)
	screenRes = [800, 600]
	sPassed = 0
	gameFrame = 0
	gameScreen = display.set_mode(screenRes)
	#--------sound
	pygame.mixer.init()
	bgm = pygame.mixer.Sound("Shit Soundtrack 1.ogg")
	fart = pygame.mixer.Sound("gfart.wav")
	pygame.mixer.Sound.play(bgm)
	bgcolor = (85, 180, 255)
	isloop = 1
	terrain = Tileset(gameScreen)
	fpstick = time.Clock()
	p1 = Player(terrain,"p", gameScreen)#new arg, imgid
	pn = Player(terrain,"cj", gameScreen)
   	loadControls(p1,pn)
   	bullets = []
	bdelay = 2
	btime = 0
	enemies = []
	shoot = 0
	#font
	msgdur = 600
	msgcurr = 0
	message = ""
	messageq = []
	messageqt = []
	messageqpos = []
	killreq = 5
	items = []
	while isloop:
		for act in pygame.event.get():
			if act.type == pygame.QUIT:
				isloop = 0
			if act.type == KEYDOWN:
				print(str(act.key))
				if str(act.key) == p1.keys["left"]:
					p1.l = 1
				if str(act.key) == p1.keys["right"]:
					p1.r = 1
				if str(act.key) == p1.keys["shoot"]:
					p1.shooting = 1

				if act.key == K_q:
					isloop = 0
				if act.key == K_p:
					pass
			if act.type == KEYUP:
				if str(act.key) == p1.keys["left"]:
					p1.l = 0
				if str(act.key) == p1.keys["right"]:
					p1.r = 0
				if act.key == p1.keys["shoot"]:
					p1.shooting = 0

		#HEALTHPACK DROPS
		if p1.killCount >= killreq:
			items.append(Item(terrain))
			killreq += 20
		#ENEMY SPAWNS
		foechanche = randint(1,201) + (sPassed / 10)
		if (sPassed % 15 == 0)  and sPassed and (gameFrame < 1):
			message = "Enemy chance increased by " + str(sPassed / 10)
		if foechanche >= 200:
			iselite = randint(1,100)
			if (iselite == 2) and (sPassed > 10): #2 n 10s lol
				enemyType = 6
			else:
				enemyType = randint(1,3)
			enemies.append(Enemy(random.choice(["l","r"]), terrain, enemyType, gameScreen))
		#UPDATING TILES AND BG
		gameScreen.fill(bgcolor)
		terrain.update_tiles(gameScreen)
		#UPDATING AND DISPLAYING ENEMIES
		for i in xrange(len(enemies)):
			enemies[i].moveEnemy(gameScreen, terrain, debugFont, p1, fart )
			if enemies[i].rect.colliderect(p1.rect):
				if enemies[i].active:
					p1.hp -= 10
		#SAME BUT BULLETS
		for i in xrange(len(p1.bullets)):
			print(len(p1.bullets))
			for x in xrange(len(enemies)):
				if p1.bullets[i].rect.colliderect(enemies[x]):
					if (p1.bullets[i].active and enemies[x].active):
						#PIERCE MEKANIKS
						if not p1.bullets[i].pierce:
							p1.bullets[i].active = 0
							pygame.mixer.Sound.play(fart)
						else:
							p1.bullets[i].rect.move_ip((p1.bullets[i].speed * 8, 0))
						enemies[x].hp -= p1.bullets[i].dmg
						#ADDING DMG NUMBER TO BE DISPLAYED
						messageq.append(p1.bullets[i].dmg)
						messageqt.append(33)
						messageqpos.append((enemies[x].rect.left + randint(-4,4)*3, enemies[x].rect.top - randint(-4,4)* 3))
		p1.showPlayer(gameScreen, terrain, debugFont)
		p1.updatebullets(gameScreen, terrain)
		#CALCULATING FPS AND TIME
		gameFrame +=  1
		if gameFrame >= 60:
			gameFrame = 0
			sPassed += 1
			print sPassed

		#printing log
		if message <> "":
			msgrnd = debugFont.render(message,True,(255,255,255))
			message = ""
			msgcurr = msgdur
		if (message == "") and (msgcurr > 0):
			gameScreen.blit(msgrnd,(5,5))
			msgcurr -= 1
		#printing onhit dmg
		for i in xrange(len(messageq)):
			if messageqt[i] > 0:
				if messageq[i] > 30:
					noimg = debugFont2.render(str(messageq[i]),True,(200,0,0))
				else:
					noimg = debugFont.render(str(messageq[i]),True,(255,200,255))
				gameScreen.blit(noimg,messageqpos[i])
				messageqt[i] -= 1
		#CLEANING UP DEAD OBJECTS
		tempfoes = []
		tempq = []
		tempqt = []
		tempqpos = []
		p1.cleanupbullets()
		for i in xrange(len(enemies)):
			if enemies[i].active:
				tempfoes.append(enemies[i])
		enemies = tempfoes
		for i in xrange(len(messageq)):
			if messageqt[i] > 0:
				tempq.append(messageq[i])
				tempqt.append(messageqt[i])
				tempqpos.append(messageqpos[i])
		messageq = tempq
		messageqt = tempqt
		messageqpos = tempqpos
		titems = []
		for i in xrange(len(items)):
			items[i].updateItem(gameScreen,terrain,p1)
			if items[i].active:
				titems.append(items[i])
		items = titems
		fpstick.tick(60)
		display.flip()





#TODO





if __name__ == "__main__":
	main()


