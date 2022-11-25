import pygame 
from support import import_folder

#Creamos clase tile (Cuadrado del editor de juego)
class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__() #Para obtener la herencia
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	#Actualizamos
	def update(self,shift):
		self.rect.x += shift

#Sobreescribo para no cambiar lo de arriba
class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface 

#Clase caja (porque no es capaz de llenar todo el mosaico y quedaria flotando)
class Crate(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('../graphics/terrain/crate.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

#clase Animacion
class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	#Velocidad de la animacion
	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames): #Para volver a la primera imagen
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	#Actializamos (tambien actualiza el Tile)
	def update(self,shift):
		self.animate()
		self.rect.x += shift

#Clase moneda (para centrarlo)
class Coin(AnimatedTile):
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value

#Clase Palmera (para subir la posicion unos pixeles)
class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,offset):
		super().__init__(size,x,y,path)
		offset_y = y - offset
		self.rect.topleft = (x,offset_y)