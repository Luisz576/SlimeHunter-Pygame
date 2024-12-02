from game.level.entity.slime import Slime, Slimes

class NormalSlime(Slime):
    def __init__(self, game, pos, group, collision_group, player_group):
        super().__init__(game, pos, group, collision_group, player_group, Slimes.NORMAL_SLIME)
