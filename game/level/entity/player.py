import pygame

from game.settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        # sprite
        self.image = pygame.Surface((32, 32))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=position)

        # attributes
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.velocity = pygame.math.Vector2(0, 0)

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
        self._input()
        self._move(delta)