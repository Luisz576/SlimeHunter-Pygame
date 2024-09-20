import pygame.time

from .settings import *
from game.level import Level


class Game:
    def __init__(self):
        # init vars
        self.level = None

        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()

    def load_level(self):
        self.level = Level()

    def run(self):
        if self.level is None:
            raise Exception("No level loaded!")

        # Game Loop
        while True:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Game Logic
            delta = self.clock.tick() / 1000
            self.level.run(delta)
            pygame.display.update()
