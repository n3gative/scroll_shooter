from pygame import *
from random import randint
class Enemy:
	def __init__(self,dr,tileset,npcid, gsurface):
		self.active = 1
		self.npcid = npcid
		self.dr = dr
		self.rect = tileset.images["npc1l1"].get_rect()
		self.frame = 1
		self.frameTime = 30
		self.cTime = 0
		self.gbars = 10
		if npcid == 1:
			self.hp = 300
			self.maxhp = 300
			self.speed = 1
		elif npcid == 2:
			self.hp = 600
			self.maxhp = 600
			self.speed = 1
		elif npcid ==  3:
			self.hp = 200
			self.maxhp = 200
			self.speed = 2
		elif npcid == 6:
			self.hp = 5000
			self.maxhp = 5000
			self.speed = 1
		if self.dr == "l":
			self.rect.topright = (gsurface.get_width() + 5, gsurface.get_height() - 200 )
			self.speed *= -1
		else:
			self.rect.topleft  = (0, gsurface.get_height() - 200)
	def moveEnemy(self,surface,tileset,dFont, player, dsound):
		if self.hp < 1:
			self.active = 0
			player.killCount += 1
			print(str(player.killCount) + "   ded")
			#pygame.mixer.Sound.play(dsound)
		if self.active:
			self.rect.move_ip((self.speed,0))
			self.cTime += 1
			if self.cTime >self.frameTime:
				self.cTime = 0
				if self.frame > 1:
					self.frame = 1
				else:
					self.frame = 2
			self.gbars = self.hp * 20
			self.gbars = int(self.gbars / self.maxhp)
			for i in xrange(20):
				if i <= self.gbars:
					surface.blit(tileset.images["green"], (self.rect.left + 2 + i , self.rect.top -8))
				else:
					surface.blit(tileset.images["red"], (self.rect.left + 2 + i , self.rect.top -8))

			#surface.blit(hpbar, (self.rect.left + 2, self.rect.top - 16))
			surface.blit(tileset.images["npc"+str(self.npcid)+self.dr+str (self.frame)],self.rect)
