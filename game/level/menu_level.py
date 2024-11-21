import pygame

from game.settings import *
from game.level import Level, Levels
from game.components.ui import Label, ButtonLabel


class MenuLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        self.delay_to_change = 0
        # components
        self.button_play = ButtonLabel(
            text="Play",
            pos=(360, 280),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
        )
        self.quit_button = ButtonLabel(
            text="Quit",
            pos=(350, 340),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
        )
        self.button_selected = 0
        self.components = [
            Label(
                text="Slime Hunter",
                pos=(230, 180),
                color=(255, 255, 255),
                size=52
            ),
            self.button_play,
            self.quit_button
        ]

    def _input(self, delta):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_SPACE]:
            if self.button_selected == 0:
                self.game.load_level(Levels.WORLD_1)
            else:
                self.game.quit()

        if self.delay_to_change > 0:
            self.delay_to_change = self.delay_to_change - delta
        else:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
                self.delay_to_change = 0.3
                if self.button_selected == 0:
                    self.button_selected = 1
                else:
                    self.button_selected = 0

    def run(self, delta):
        self._input(delta)
        self.update(delta)
        self.render()

    def update(self, delta):
        # play
        self.button_play.selected = (self.button_selected == 0)
        self.button_play.update(delta)
        # quit
        self.quit_button.selected = (self.button_selected == 1)
        self.quit_button.update(delta)

    def render(self):
        for component in self.components:
            component.render(self.game.screen)
