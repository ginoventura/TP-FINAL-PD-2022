import pygame
from settings import screen_width, screen_height
from game_data import options

class Instru:
    def __init__(self,surface):

        #setup opciones
        self.display_surface = surface

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)