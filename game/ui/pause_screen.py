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
            pos=(300, 290),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
            selected=True # button_index = 0
        )
        self.hardcore_button = ButtonLabel(
            text="HARDCORE",
            pos=(310, 340),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
            selected=False  # button_index = 1
        )
        self.button_selected = 0
        self.delay_to_change = 0
        self.page_index = 0
        self.controls_screen = ControlsScreen(game)

    def _input(self, delta):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_SPACE]:
            if self.button_selected == 0:
                self.page_index = 1
            elif self.button_selected == 1:
                self.game.level.hardcore()

        if self.delay_to_change > 0:
            self.delay_to_change = self.delay_to_change - delta
        else:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
                self.delay_to_change = 0.3
                if self.button_selected == 0:
                    self.button_selected = 1
                else:
                    self.button_selected = 0

    def update(self, delta):
        self._input(delta)
        self.button_controls.selected = (self.button_selected == 0)
        self.button_controls.update(delta)
        self.hardcore_button.selected = (self.button_selected == 1)
        self.hardcore_button.update(delta)
        self.render(delta)

    def render(self, delta):
        if self.page_index == 0:
            self.paused_label.render(self.game.screen)
            self.button_controls.render(self.game.screen)
            self.hardcore_button.render(self.game.screen)
        elif self.page_index == 1:
            self.controls_screen.render(delta)