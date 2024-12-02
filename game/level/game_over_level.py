from game.components.ui import Label
from game.level import Level
import pygame

class GameOverLevel(Level):
    def __init__(self, game):
        super().__init__(game)
        # delay to exit
        self.delay_to_exit = 1.5
        # components
        self.components = [
            Label(
                text="Game Over",
                pos=(230, 100),
                color=(255, 255, 255),
                size=64,
            ),
            Label(
                text=f"Score: {self.game.game_score}",
                pos=(290, 190),
                color=(255, 255, 255),
                size=48,
            ),
            Label(
                text=f"<Space to close>",
                pos=(260, 480),
                color=(255, 255, 255),
                size=32,
            )
        ]

    def _input(self, delta):
        keys = pygame.key.get_pressed()
        if self.delay_to_exit <= 0 and keys[pygame.K_SPACE]:
            self.game.quit()

    def run(self, delta):
        self._input(delta)
        if self.delay_to_exit > 0:
            self.delay_to_exit -= delta
        self.render()

    def render(self):
        self.game.screen.fill((0, 0, 0))
        for component in self.components:
            component.render(self.game.screen)
