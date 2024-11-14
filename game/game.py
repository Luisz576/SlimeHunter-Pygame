import pygame.time

from game.settings import *
from game.level import Levels, level_builder


class Game:
    def __init__(self):
        # init vars
        self.level = None
        self.pause_screen = None

        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()

        # level
        self.load_level()

    def load_level(self):
        self.level = level_builder(Levels.MENU)

    def run(self):
        if self.level is None:
            raise Exception("No level loaded!")

        # Game Loop
        while True:
            delta = self.clock.tick() / 1000

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Game Logic
            self.level.run(delta)
            pygame.display.update()
            # print(f"FPS: {self.clock.get_fps()}")
