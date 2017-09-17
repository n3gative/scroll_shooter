from pygame import *
from random import randint
from bullet import Bullet
class Player:
	def __init__(self,tileset,imgid,screen, playertype = "pistolGuy"):
		#loading some stats from txtfile
		statsFile = open(playertype + ".cha","r")
		self.basestats = {}
		self.keys = {"left":"", "right":"", "shoot":""}
		statscont = statsFile.readlines()
		for i in xrange( len( statscont)):
			tempLine = statscont[i].split("=")
			self.basestats[tempLine[0]] = tempLine[1]
		statsFile.close()
		print self.basestats
		self.basedmg = [1,12]
		self.direction = "right"
		self.frame = 1#anim
		self.frametime = 15
		self.currtime = 0

		self.imgid = imgid
		self.rect = (tileset.images["pright1"]).get_rect()
		self.rect.bottomright = (screen.get_width() / 2, screen.get_height() - 168)
		self.arect = tileset.images["arrow"].get_rect()
		self.arect.topleft = self.rect.topleft
		self.arect.move_ip(14,-250)
		self.l, self.r = 0,0
		self.speed = 2
		self.hp = 15000
		self.maxhp = 15000
		self.gbars = 20
		self.killCount = 0
		#inname stats = load from taxt files
		#add textfile to args and calls

		self.critChance = 20
		self.shooting = 0
		self.prchance = 20
		self.atkspd = 10 # per s
		self.bfps = 0
		self.bullets = []
	def showPlayer(self,surface,tileset,hpfont):
		if self.l:
			self.rect.move_ip(-self.speed, 0)
			self.arect.move_ip(-self.speed, 0)
			self.direction = "left"
		if self.r:
			self.rect.move_ip(self.speed, 0)
			self.arect.move_ip(self.speed, 0)
			self.direction = "right"
		if not(self.r or self.l):
			self.currtime -= 1
		surface.blit(tileset.images[self.imgid +self.direction +str(self.frame)],self.rect)
		self.currtime += 1
		if self.currtime > self.frametime:
			self.currtime = 0
			if self.frame == 1:
				self.frame = 2
			else:
				self.frame = 1
		hpimg = hpfont.render(str(self.hp),True,(0,0,200))
		self.gbars = self.hp * 20
		self.gbars = int(self.gbars / self.maxhp)
		for i in xrange(20):
			if i <= self.gbars:
				surface.blit(tileset.images["green"], (50 + i*2 , 50))
			else:
				surface.blit(tileset.images["red"], (50 + i*2 , 50))
		surface.blit(hpimg,(100, 25))
		surface.blit(tileset.images["arrow"], self.arect)
		if self.shooting:
			abullet = self.shoot(tileset)
			try:
				int(abullet)
			except AttributeError:
					print("Real")
					self.bullets.append(abullet)
	def enemy_col(self,enemielist):
		for i in xrange(len(enemielist)):
			for x in xrange(len(self.bullets)):
				if enemielist[i].rect.colliderect(self.bullets[x].rect):
					enemielist[i].hp -= self.bullets[x].dmg
					if not self.bullets[x].pierce:
						self.bullets[x].active = 0
	def cleanupbullets(self):
		tempb = []
		for i in xrange(len(self.bullets)):
			if self.bullets[i].active:
				tempb.append(self.bullets[i])
		self.bullets = tempb
	def updatebullets(self,screen,tileset):
		for i in xrange(len(self.bullets)):
			print(str(i) + "w" )
			self.bullets[i].moveBullet(screen,tileset)

		#####
	def shoot(self, tileset): # sfr frames
		fpshot = int( 60 / self.atkspd)
		self.bfps +=  1
		if self.bfps >= fpshot:
			bullet = Bullet(tileset,self)
			critrng = randint(self.critChance,100)
			if critrng == 2:
				bullet.dmg = (bullet.dmg + randint(self.basedmg[0], self.basedmg[1]))
				bullet.crit = 1
			else:
				bullet.dmg += randint(self.basedmg[0], self.basedmg[1])
			piercechance = randint(1,self.prchance)
			if piercechance == 2:
				bullet.pierce = 1
			self.bfps = 0
			##print "a"
			return bullet
		##print "b"
		return 2
