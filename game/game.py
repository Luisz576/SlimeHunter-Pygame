import pygame.time

from game.settings import *
from game.level import level_builder, Levels


class Game:
    def __init__(self):
        # init vars
        self.level = None

        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()

        self.load_level()

    def load_level(self):
        self.level = level_builder(Levels.WORLD_1)

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
            print(f"FPS: {self.clock.get_fps()}")
