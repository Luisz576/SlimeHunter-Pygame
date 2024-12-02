import sys

import pygame.time

from game.settings import *
from game.level import Levels, level_builder
from game.sound import SlimeHunterSoundManager


class Game:
    def __init__(self):
        # init vars
        self.level = None
        self.pause_screen = None

        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.sound_manager = SlimeHunterSoundManager()

        self.clock = pygame.time.Clock()

        # global
        self.game_score = 0

        # level
        self.load_level()

    def load_level(self, level=Levels.MENU):
        if self.level is not None:
            self.level.unload_level()
        self.level = level_builder(level, self)

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

    def quit(self):
        sys.exit()
