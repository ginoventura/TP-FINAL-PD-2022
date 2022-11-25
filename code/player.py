import pygame 
from support import import_folder
from math import sin

# Clase jugador
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles,change_health):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		
		# Particulas de tierra 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# Movimientos del jugador
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 5
		self.gravity = 0.8
		self.jump_speed = -16
		self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))

		# Estado del jugador
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# Manejo de la barra de salud
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

		# Audio de los saltos y cuando golpea un enemigo
		self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

	# Funcion para importar la visual y el comportamiento del personaje
	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	# Funcion para importar la "tierra"
	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.collision_rect.bottomleft
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image
			self.rect.bottomright = self.collision_rect.bottomright

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)		

	# Funcion para controlar la animacion de la tierra cuando el personaje esta corriendo
	def run_dust_animation(self):

		# Si el presonaje esta en estado corriendo y sobre el terreno(tierra)
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	# Funcion para establecer los movimientos del jugador, dependendiendo 
	# de la tecla que se presione
	def get_input(self):
		keys = pygame.key.get_pressed()

	# Si se presiona la flecha derecha: 
	# El jugador suma uno al valor de X, por lo que avanza hacia la izquierda
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True

	# Si se presiona la flecha izquierda: 
	# El jugador resta uno al valor de X, por lo que retrocede hacia la derecha
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		
	# Si no se presiona ninguna tecla, el jugador no se mueve
		else:
			self.direction.x = 0

	# Si se presiona espacio y el jugador esta en tierra, 
	# Se llama a la funcion "saltar" y creando las particulas de salto
		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.midbottom)

	# Funcion para obtener el estado del jugador
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	# Funcion para establecer la gravedad
	def apply_gravity(self):
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	# Funcion para controlar el salto
	def jump(self):
		self.direction.y = self.jump_speed
		self.jump_sound.play()

	# Funcion para establecer el daño y la barra de salud
	def get_damage(self):
		if not self.invincible:
			self.hit_sound.play()
			self.change_health(-10)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	# Funcion para establecer el temporizador de invencibilidad luego de recibir daño
	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	# Funcion para que las olas en la parte inferior tengan movimiento
	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	# Funcion para luego actualizar los sprites
	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
		self.invincibility_timer()
		self.wave_value()
		