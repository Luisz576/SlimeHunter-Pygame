import pygame.time

from game.settings import *
from game.level import level_builder, Levels
from game.ui import PauseScreen


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

        # pause
        self.paused = False
        self.load_pause_screen()

        # level
        self.load_level()

    def load_pause_screen(self):
        self.pause_screen = PauseScreen(self)

    def load_level(self):
        self.level = level_builder(Levels.WORLD_1)

    def _input(self):
        # TODO: FIX PRESS (IF YOU PRESS SO MUCH IT PAUSE AND UNPAUSE)
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_ESCAPE]:
            self.paused = not self.paused

    def run(self):
        if self.pause_screen is None:
            raise Exception("Pause screen not loaded!")
        if self.level is None:
            raise Exception("No level loaded!")

        # Game Loop
        while True:
            self._input()

            delta = self.clock.tick() / 1000

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Game Logic
            if self.paused:
                self.pause_screen.run(delta)
            else:
                self.level.run(delta)
            pygame.display.update()
            # print(f"FPS: {self.clock.get_fps()}")
