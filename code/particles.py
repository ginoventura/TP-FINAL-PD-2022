import pygame
from support import import_folder

# Clase para mostrar las animaciones del personaje y de los enemigos (Salto, aterrizaje y explosion al matar enemigo)
class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump':
			self.frames = import_folder('../graphics/character/dust_particles/jump')
		if type == 'land':
			self.frames = import_folder('../graphics/character/dust_particles/land')
		if type == 'explosion':
			self.frames = import_folder('../graphics/enemy/explosion')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	# Funcion para animar la accion 
	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	# Actualizacion de la animacion
	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
