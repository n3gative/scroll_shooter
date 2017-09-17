from pygame import *
from random import randint
class Bullet:
	def __init__(self,tileset,player,baseDmg = 25,basemSpeed = 4):
		self.active = 1
		self.imgname = "bullet"
		self.rect = tileset.images[self.imgname].get_rect()
		self.speed = 3
		self.crit = 0
		self.dmg = baseDmg
		self.pierce = 0
		self.speed = basemSpeed
		if player.direction == "left":
			self.rect.topright = (player.rect.left - 2, player.rect.top + 16 + randint(-8,8))
			self.speed *= -1
		else:
			self.rect.topleft = (player.rect.right + 2, player.rect.top + 16 + randint(-8,8))
		
	def moveBullet(self, surface, tileset):
		if self.active:
			self.rect.move_ip((self.speed, 0))
			surface.blit(tileset.images["bullet"], self.rect)
			if (self.rect.left < 0) or (self.rect.right > surface.get_width()):
				self.active = 0
				print("Bam")
