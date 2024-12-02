from time import sleep

import pygame

class AttackArea:
    def __init__(self, damage, pos, attack_range, attack_group):
        self.damage = damage
        self.pos = pos
        self.attack_group = attack_group
        self.attack_range = attack_range

        # attack
        self.attack()

    def is_achievable(self, target_pos):
        tx = target_pos[0]
        ty = target_pos[1]

        attack_pos_x_a = self.pos[0]
        attack_pos_x_b = self.pos[0] + self.attack_range[0]
        if attack_pos_x_b < attack_pos_x_a:
            aux_x = attack_pos_x_b
            attack_pos_x_b = attack_pos_x_a
            attack_pos_x_a = aux_x

        attack_pos_y_a = self.pos[1] - self.attack_range[1]
        attack_pos_y_b = self.pos[1] + self.attack_range[1]
        if attack_pos_y_b < attack_pos_y_a:
            aux_y = attack_pos_y_b
            attack_pos_y_b = attack_pos_y_a
            attack_pos_y_a = aux_y

        return (attack_pos_x_a <= tx <= attack_pos_x_b) and (attack_pos_y_a <= ty <= attack_pos_y_b)

    def attack(self):
        for sprite in self.attack_group:
            if self.is_achievable((sprite.rect.centerx, sprite.rect.centery)):
                if sprite.give_damage is not None:
                    sprite.give_damage(self.damage)