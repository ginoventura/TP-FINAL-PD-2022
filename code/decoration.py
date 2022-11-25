from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

#Clase Background de la intro para decorar el fondo.
class Bgintro:
	def __init__(self):
		self.background = pygame.image.load('../graphics/intro/blackground/background_principal.png').convert()

	#Dibujamos.
	def draw(self,surface):
		surface.blit(self.background,(0,0))

#Clase Cielo para decorar el fondo tanto del overworld como de cada nivel.
class Sky:
	def __init__(self,horizon,style = 'level'):
		self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
		self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
		self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
		self.horizon = horizon

		#Tramo 
		self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
		self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
		self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))

		self.style = style
		if self.style == 'overworld':
			palm_surfaces = import_folder('../graphics/overworld/palms')
			self.palms = []

			for surface in [choice(palm_surfaces) for image in range(10)]:
				x = randint(0,screen_width)
				y = (self.horizon * tile_size) + randint(50,100)
				rect = surface.get_rect(midbottom = (x,y))
				self.palms.append((surface,rect))

			cloud_surfaces = import_folder('../graphics/overworld/clouds')
			self.clouds = []

			for surface in [choice(cloud_surfaces) for image in range(10)]:
				x = randint(0,screen_width)
				y = randint(0,(self.horizon * tile_size) - 100)
				rect = surface.get_rect(midbottom = (x,y))
				self.clouds.append((surface,rect))

	#Definimos la superficie que queremos dibujar.
	def draw(self,surface):
		for row in range(vertical_tile_number):
			y = row * tile_size
			#Parte de arriba del cielo.
			if row < self.horizon: 
				surface.blit(self.top,(0,y)) 
			#Horizonte del cielo.
			elif row == self.horizon:	
				surface.blit(self.middle,(0,y))
			#Parte de abajo del cielo (todo lo demas).
			else:						
				surface.blit(self.bottom,(0,y))	

		if self.style == 'overworld':
			for palm in self.palms:
				surface.blit(palm[0],palm[1])
			for cloud in self.clouds:
				surface.blit(cloud[0],cloud[1])

#Clase agua para decorar cada nivel.
class Water:
	#Obtenemos datos el agua (porque tiene que extenderse mas que la superficie del mapa).
	def __init__(self,top,level_width):
		water_start = -screen_width
		water_tile_width = 192
		tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
		self.water_sprites = pygame.sprite.Group()

		#Colocamos el agua en la posicion.
		for tile in range(tile_x_amount):
			x = tile * water_tile_width + water_start
			y = top
			sprite = AnimatedTile(192,x,y,'../graphics/decoration/water')
			self.water_sprites.add(sprite)

	#Dibujamos.
	def draw(self,surface,shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

#Clase nubes para poder decorar los niveles y el "overworld".
class Clouds:
	#Obtenemos datos de la nube (igual que el agua).
	def __init__(self,horizon,level_width,cloud_number):
		cloud_surf_list = import_folder('../graphics/decoration/clouds')
		min_x = -screen_width
		max_x = level_width + screen_width
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		#Colocamos las nubes en la posicion
		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list) #Elige una nube de manera aleatoria.
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	#Dibujamos.
	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)
