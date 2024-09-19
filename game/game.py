from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW.WIDTH, WINDOW.HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.import_assets()

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('..', 'maps', 'world.tmx'))}

    def run(self):
        while True:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # LOGIC
            pygame.display.update()
