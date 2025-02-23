from game.level.entity.projectile import ArrowProjectile
from game.settings import calc_points_vector_look, WINDOW_WIDTH, WINDOW_HEIGHT

PROJECTILE_ARROW = "arrow"

DEFAULT_DURATION = 3

class Shootable:
    def __init__(self, game, entity, projectile_type, projectile_render_group, enemy_group):
        self.game = game
        self.entity = entity
        self.__projectile = None
        self.projectile_render_group = projectile_render_group
        self.enemy_group = enemy_group

        if projectile_type == PROJECTILE_ARROW:
            self.__projectile = ArrowProjectile

    def shoot(self, target_pos):
        pos = (self.entity.rect.centerx, self.entity.rect.centery)
        offset_x = (pos[0] - WINDOW_WIDTH / 2)
        offset_y = (pos[1] - WINDOW_HEIGHT / 2)
        target_pos = (target_pos[0] + offset_x, target_pos[1] + offset_y)
        direction = calc_points_vector_look(pos, target_pos)
        projectile = self.__projectile(self.entity.game, self.projectile_render_group, self.enemy_group, pos, direction, DEFAULT_DURATION)
        self.entity.game.level.add_projectile(projectile)
        # play sound
        self.game.sound_manager.play_sound(projectile.shoot_sound)
