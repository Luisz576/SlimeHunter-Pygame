import pygame

from game.components.ui import Label

class ControlsScreen:
    def __init__(self, game):
        self.game = game
        self.controller_title = Label(
            text="Controls",
            pos=(330, 220),
            color=(255, 255, 255),
            size=48
        )

        controls = [
            {
                "text": "Move up",
                "key": "W"
            },
            {
                "text": "Move down",
                "key": "S"
            },
            {
                "text": "Move left",
                "key": "A"
            },
            {
                "text": "Move right",
                "key": "D"
            },
            {
                "text": "Attack",
                "key": "Space"
            },
            {
                "text": "Pause",
                "key": "Esc"
            },
            {
                "text": "Shoot",
                "key": "Left Click"
            }
        ]
        self.controls_labels = []
        i = 0
        for control in controls:
            self.controls_labels.append(
                Label(
                    text=f"{control["text"]}: {control["key"]}",
                    pos=(80, 100 + i*52),
                    color=(255, 255, 255),
                    size=42
                )
            )
            i += 1

    def _input(self):
        pass

    def update(self, delta):
        self._input()
        self.render(delta)

    def render(self, delta):
        for control in self.controls_labels:
            control.render(self.game.screen)
