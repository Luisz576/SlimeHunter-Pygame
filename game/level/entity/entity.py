from game.settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        # render // TODO:
        self.image = pygame.Surface((32, 32))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=position)

        # attributes
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.velocity = pygame.math.Vector2(0, 0)

    def _move(self, delta):
        # normalizationws
        if self.velocity.magnitude() > 0:
            self.velocity = self.velocity.normalize()
        # moviment
        self.position.x += self.velocity.x * self.speed * delta
        self.rect.centerx = self.position.x
        self.position.y += self.velocity.y * self.speed * delta
        self.rect.centery = self.position.y

    def update(self, delta):
        self._move(delta)
