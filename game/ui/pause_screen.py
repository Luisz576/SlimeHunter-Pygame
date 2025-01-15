import pygame

from game.components.ui import Label, ButtonLabel
from game.ui.controls_screen import ControlsScreen

class PauseScreen:
    def __init__(self, game):
        self.game = game
        self.paused_label = Label(
            text="Paused",
            pos=(330, 220),
            color=(255, 255, 255),
            size=48
        )
        self.button_controls = ButtonLabel(
            text="Controls List",
            pos=(320, 290),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
            selected=True # button_index = 0
        )
        self.button_selected = 0
        self.delay_to_change = 0
        self.page_index = 0
        self.controls_screen = ControlsScreen(game)

    def _input(self):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_SPACE]:
            if self.button_selected == 0:
                self.page_index = 1

    def update(self, delta):
        self._input()
        self.render(delta)

    def render(self, delta):
        if self.page_index == 0:
            self.paused_label.render(self.game.screen)
            self.button_controls.render(self.game.screen)
        elif self.page_index == 1:
            self.controls_screen.render(delta)