import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from intro import Intro
from option import Option
from ui import UI

class Game:
	def __init__(self):

		# Atributos del juego
		self.max_level = 0
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.max_option = 0

		# Audio 
		self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')

		#Atributos overworld
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)

		#Atributos Into
		self.intro = Intro(0,self.max_option,screen,self.create_option)
		self.status = 'intro'

		# Interfaz de usuario 
		self.ui = UI(screen)

	def create_option(self, current_option):
		self.option = Option(current_option, screen, self.create_intro)
		self.status = 'option'

	def create_intro(self, current_option, new_max_option):
		if new_max_option > self.max_option:
			self.max_option = new_max_option
		self.intro = Intro(current_option, self.max_option, screen, self.create_option)
		self.status = 'intro'

	# Funcion para crear el nivel
	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.level_bg_music.play(loops = -1)

	# Funcion para crear el menu de niveles
	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()

	# Funcion para acumular las monedas obtenidas
	def change_coins(self,amount):
		self.coins += amount

	# Funcion para verificar la salud del jugador
	def change_health(self,amount):
		self.cur_health += amount

	# Funcion para chequear si el juego terminó y restablecer todos los valores
	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			self.level_bg_music.stop()
			self.overworld_bg_music.play(loops = -1)

	# Funcion para ejecutar el juego
	def run(self):
		# Si el estado es "overworld" se muestran los niveles
		if self.status == 'intro':
			self.intro.run()		
		elif self.status == 'option':
			self.overworld.run()
		elif self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

# Configuracion de PyGame
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	game.run()

	pygame.display.update()
	clock.tick(60)