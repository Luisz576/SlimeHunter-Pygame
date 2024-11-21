from game.settings import *
from game.level import MapLevel
from game.level.entity import Slime, Slimes


class MonsterLevel(MapLevel):
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale):
        super().__init__(game, map_path, map_layers, map_collision_layers, tile_scale)
        self.TEMP = True

    def _update(self, delta):
        self.spawner()
        super()._update(delta)

    def spawner(self):
        # TODO: Slime aleatório
        # TODO: if random.random() < 0.001:
        if self.TEMP:
            self.TEMP = False
            enemy = Slime(
                # (random.randint(200, 2000), random.randint(200, 1800)),
                (600, 600),
                self.render_sprites,
                self.collision_sprites,
                Slimes.NORMAL_SLIME
            )
            enemy.target = self.player
            self.enemies.append(enemy)
