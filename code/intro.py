import pygame 
from game_data import options
from support import import_folder
from decoration import Bgintro

class Node(pygame.sprite.Sprite):
	def __init__(self,pos, status, icon_speed,path):
		super().__init__()
		self.frames = import_folder(path)
		self.frames_index = 0
		self.image = self.frames[self.frames_index]
		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed, icon_speed)

class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('../graphics/intro/hat.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos

class Intro:
	def __init__(self,start_option,max_option,surface, create_option):

		# Inicializacion
		self.display_surface = surface 
		self.max_option = max_option
		self.current_option = start_option
		self.create_option = create_option

		# Logica de movimiento
		self.moving = False
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 8
		
		#Spritess
		self.setup_nodes()
		self.setup_icon()
		self.bgintro = Bgintro()

	def setup_nodes(self):
		self.nodes = pygame.sprite.Group()
		for index, node_data in enumerate(options.values()):
			if index <= self.max_option:
				node_sprite = Node(node_data['node_pos'], 'available', self.speed,node_data['node_graphics'])
			else:
				node_sprite = Node(node_data['node_pos'], 'locked', self.speed,node_data['node_graphics'])
			self.nodes.add(node_sprite)

	def draw_path(self):
		points = [node['node_pos']for node in options.values()]
		pygame.draw.lines(self.display_surface, '#AE7764', False, points, 3) #A34C4F

	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_option].rect.center)
		self.icon.add(icon_sprite)

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.moving: #and self.allow_input:
			if keys[pygame.K_RIGHT] and self.current_option < self.max_option:
				self.move_direction = self.get_movement_data('next')
				self.current_option += 1
				self.moving = True
			elif keys[pygame.K_LEFT] and self.current_option > 0:
				self.move_direction = self.get_movement_data('previous')
				self.current_option -= 1
				self.moving = True
			elif keys[pygame.K_SPACE]:
				self.create_option(self.current_option)

	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodes.sprites()[self.current_option].rect.center)
		
		if target == 'next': 
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_option + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_option - 1].rect.center)

		return (end - start).normalize()

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_option]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)



	# Funcion para "ejecutar" un nivel
	def run(self):
		self.input()
		self.update_icon_pos()
		self.icon.update()

		self.bgintro.draw(self.display_surface)
		self.draw_path()
		self.nodes.draw(self.display_surface)
		self.icon.draw(self.display_surface)