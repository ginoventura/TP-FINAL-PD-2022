import pygame 
from tiles import AnimatedTile
from random import randint

#Clase enemigo
class Enemy(AnimatedTile):

	#Posicion donde se encuentra
	def __init__(self,size,x,y):
		super().__init__(size,x,y,'../graphics/enemy/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(3,5) #Cada enemigo va a tener una velocidad distinta

	#Movimento
	def move(self):
		self.rect.x += self.speed

	#Imagen segun el sentido del movimiento
	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	#Invertir la velocidad
	def reverse(self):
		self.speed *= -1

	#Actualizamos (tambien actualiza el Tile y la animacion)
	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()