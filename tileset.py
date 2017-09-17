from pygame import *
from random import randint
class Tile:
	def __init__(self, imgname, imgobj, posx, posy, anim, dirx, diry):
				#name for image id, example img for hitbox, to be fixed sometime
				#posx, posy , anim = 0 for static, 1 for moving tile
				#dirx, diry - moving for animated tiles
		self.sprname = imgname
		self.solid = True
		self.rect = imgobj.get_rect()
		self.rect.topleft = (posx, posy)
		self.anim = anim
		self.dr = [dirx, diry]

class Tileset:
	def __init__(self,surface):
		self.images = {}
		self.sres = [surface.get_width(), surface.get_height()]
		imgfile = open("imgfile.txt","r")
		templines = imgfile.readlines()
		imgfile.close()
		for i in xrange(len(templines)):
			if (templines[i][0] <> "#") and (templines[i][0] <> "@"):
				disline = templines[i].strip("\n").split(",")
				self.images[disline[0]] = image.load(disline[1]).convert()
			if (templines[i][0] == "@"):
				print templines[i][1:].strip()
		self.tiles = []
		self.getTiles(surface)
	def update_tiles(self, surface):
		for i in xrange(len(self.tiles)):
			surface.blit(self.images[self.tiles[i].sprname],self.tiles[i].rect)
			if self.tiles[i].anim:
				self.tiles[i].rect.move_ip(self.tiles[i].dr)
				if self.tiles[i].rect.left >1000:
					self.tiles[i].rect.left = -100 -1 * (randint(100,200))
	def getTiles(self, surface):
		txtfile = open("tilepos.txt","r")
		alllines = txtfile.readlines()
		txtfile.close()
		for i in xrange(len(alllines)):
			fc = alllines[i][0]
			if fc == "#":
				pass
			elif fc == "@":
				linerez = alllines[i].split(",")
				linerez[0] = linerez[0][1:]
				tsurf = self.images[linerez[0]]
				tcount = surface.get_width() / tsurf.get_width()
				for x in xrange(tcount):
					self.tiles.append(Tile(linerez[0], self.images[linerez[0]], x * tsurf.get_width(), surface.get_height() - int(linerez[2]), int(linerez[3]), int(linerez[4]), int(linerez[5]) ))
			else:
				linerez = alllines[i].split(",")
				self.tiles.append(Tile(linerez[0], self.images[linerez[0]], int(linerez[1]), int(linerez[2]), int(linerez[3]), int(linerez[4]), int(linerez[5]) ))
