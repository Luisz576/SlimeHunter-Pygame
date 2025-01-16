import math

import pygame

import game.importer as importer

from game.components import Sprite
from game.level.attack import AttackArea
from game.settings import join, calc_point_angle
from game.sound import Sounds


def rotate_sprite(surf, direction):
    return pygame.transform.rotate(surf, calc_point_angle(direction))


class Projectile(Sprite):
    def __init__(self, game, render_group, enemy_group, shoot_sound, pos, direction, duration, speed, path):
        super().__init__(pos,
                         rotate_sprite(importer.import_image(path), direction),
                         render_group)
        self.game = game
        self.direction = direction
        self.duration = duration
        self.duration_delta = duration
        self.speed = speed
        self.is_destroyed = False
        self.__dis_moved = 0
        self.shoot_sound = shoot_sound
        self.render_group = render_group
        self.enemy_group = enemy_group

    def amount_of_damage(self) -> int: ...

    def destroy(self):
        self.remove(self.render_group)
        self.is_destroyed = True

    def update(self, delta):
        if self.is_destroyed:
            return
        #####

        ##### MOVE ARROW
        disToMoveX = self.direction[0] * self.speed * delta
        disToMoveY = self.direction[1] * self.speed * delta
        disToMove = math.sqrt(disToMoveX**2 + disToMoveY**2)

        self.rect.x += disToMoveX
        self.rect.y += disToMoveY

        self.__dis_moved += disToMove

        self.__verify_collision()

        #####
        self.duration_delta -= delta
        if self.duration_delta <= 0:
            self.destroy()

    def __verify_collision(self):
        AttackArea(
            self.amount_of_damage(),
           (self.rect.x, self.rect.y),
           (self.rect.width, self.rect.height),
           self.enemy_group
       )


ArrowSpeed = 350

class ArrowProjectile(Projectile):
    def __init__(self, game, render_group, enemy_group, pos, direction, duration):
        super().__init__(game, render_group, enemy_group, Sounds.ARROW_SHOOT, pos, direction, duration, ArrowSpeed, join("assets", "characters", "Soldier", "Arrow", "Arrow.png"))
        self.arrow_power = 5

    def amount_of_damage(self):
        d_r = self.duration_delta / self.duration
        return math.ceil(self.arrow_power * d_r)