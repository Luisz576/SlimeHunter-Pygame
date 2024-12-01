from game.components.ui import Label

class PauseScreen:
    def __init__(self, game):
        self.game = game
        self.paused_label = Label(
            text="Paused",
            pos=(330, 220),
            color=(255, 255, 255),
            size=48
        )

    def _input(self):
        pass

    def update(self, delta):
        self._input()
        self.render(delta)

    def render(self, delta):
        self.paused_label.render(self.game.screen)
