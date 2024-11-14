from game.settings import *
from game.level import Level, Levels


class MenuLevel(Level):
    def __init__(self, game):
        super().__init__(game)

    def _input(self):
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_SPACE]:
            self.game.load_level(Levels.WORLD_1)

    def run(self, delta):
        self._input()
        self.render()

    def render(self):
        # TODO: titulo game e botões
        pass
