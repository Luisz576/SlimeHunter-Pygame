from game.settings import *
from game.level import Level, Levels
from game.components.ui import Label, ButtonLabel


class MenuLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        # components
        self.button_play = ButtonLabel(
            text="Space to Play",
            pos=(280, 180),
            selected_color=(255, 255, 255),
            size=36,
            time_selected=0.2,
            not_selected_color=(100, 100, 100),
        )
        self.components = [
            Label(
                text="Slime Hunter",
                pos=(230, 80),
                color=(255, 255, 255),
                size=52
            ),
            self.button_play
        ]

    def _input(self):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_SPACE]:
            self.game.load_level(Levels.WORLD_1)

    def run(self, delta):
        self._input()
        self.update(delta)
        self.render()

    def update(self, delta):
        # logic
        self.button_play.selected = True
        self.button_play.update(delta)

    def render(self):
        for component in self.components:
            component.render(self.game.screen)
