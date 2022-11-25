import pygame
from settings import screen_width, screen_height
from game_data import options

class Option:
    def __init__(self, current_option, surface, create_intro):

        #setup opciones
        self.display_surface = surface

        #Conexion a intro
        self.create_intro = create_intro
        self.current_option = current_option
        option_data = options[self.current_option]
        self.new_max_option = option_data['unlock']
        options_content = option_data['content']


        #Visualizacion de opcion
        self.font = pygame.font.Font(None,40)
        self.text_surf = self.font.render(options_content, True, 'White')
        self.text_rect = self.text_surf.get_rect(center = (screen_width/2, screen_height/2))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_intro(self.current_option, self.new_max_option)
        if keys[pygame.K_ESCAPE]:
            self.create_intro(self.current_option, 0)

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)