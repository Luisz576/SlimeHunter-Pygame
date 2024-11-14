from game.settings import *
from game.level import MapLevel
from game.level.entity import Slime, Slimes


class MonsterLevel(MapLevel):
    def __init__(self, map_path, map_layers, map_collision_layers, tile_scale):
        super().__init__(map_path, map_layers, map_collision_layers, tile_scale)

    def _update(self, delta):
        self.spawner()
        super()._update(delta)

    def spawner(self):
        # TODO: Slime aleatório
        if random.random() < 0.001:
            enemy = Slime(
                (random.randint(200, 2000), random.randint(200, 1800)),
                self.render_sprites,
                self.collision_sprites,
                Slimes.NORMAL_SLIME
            )
            enemy.target = self.player
            self.enemies.append(enemy)
