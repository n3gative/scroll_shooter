from pygame import *
from random import randint
class Item:
	def __init__(self,tileset):
		self.name = ""
		self.value = 5000
		self.action = "heal"
		self.active = 1
		self.rect = tileset.images["medkit"].get_rect()
		self.rect.topleft = (randint(0,610), 100)
	def updateItem(self,surface,tileset,player):
		if self.rect.colliderect(player):
			player.hp += self.value
			self.active = 0
		if self.active:
			if self.rect.bottom < 415:
				self.rect.move_ip(0,1)
			surface.blit(tileset.images["medkit"],self.rect)
