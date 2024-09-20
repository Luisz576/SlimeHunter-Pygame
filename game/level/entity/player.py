from game.settings import *
from game.level.entity import Entity


class Player(Entity):
    def __init__(self, position, group):
        super().__init__(position, group)

    def _input(self):
        keys = pygame.key.get_pressed()

        # moviment
        if keys[pygame.K_w]:
            self.velocity.y = -1
        elif keys[pygame.K_s]:
            self.velocity.y = 1
        else:
            self.velocity.y = 0

        if keys[pygame.K_a]:
            self.velocity.x = -1
        elif keys[pygame.K_d]:
            self.velocity.x = 1
        else:
            self.velocity.x = 0

    def update(self, delta):
        self._input()

        super().update(delta)
