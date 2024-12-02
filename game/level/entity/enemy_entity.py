from game.level.entity import Entity


class EnemyEntity(Entity):
    def __init__(self, game, pos, speed, group, collision_group, animations, start_animation_name, enemy_die_score):
        super().__init__(game, pos, speed, group, collision_group, animations, start_animation_name)
        self.enemy_die_score = enemy_die_score
