import pygame

import game.importer as importer

from game.components import Sprite
from game.settings import join


class Projectile(Sprite):
    def __init__(self, game, render_group, pos, direction, duration, speed, path):
        super().__init__(pos,
                         pygame.transform.flip(importer.import_image(path), direction[0] < 0, False),
                         render_group)
        self.game = game
        self.direction = direction
        self.duration = duration
        self.duration_delta = duration
        self.speed = speed
        self.is_destroyed = False

    def update(self, delta):
        if self.is_destroyed:
            return
        #####

        ##### MOVE ARROW
        # TODO: TA ZUADO
        self.rect.x += self.direction[0] * self.speed * delta
        self.rect.y += self.direction[1] * self.speed * delta

        #####
        self.duration_delta -= delta
        if self.duration_delta <= 0:
            self.is_destroyed = True


ArrowSpeed = 300

class ArrowProjectile(Projectile):
    def __init__(self, game, render_group, pos, direction, duration):
        super().__init__(game, render_group, pos, direction, duration, ArrowSpeed, join("assets", "characters", "Soldier", "Arrow", "Arrow.png"))
