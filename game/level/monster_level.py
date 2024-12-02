import random
from game.level import MapLevel


class MonsterLevel(MapLevel):
    # slime_chances => [ (Chance, SlimeClass), ... ]
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale, slime_chances, background_music_path):
        super().__init__(game, map_path, map_layers, map_collision_layers, tile_scale, background_music_path)
        self.slime_chances = slime_chances
        self.time_elapsed = 0

    def run(self, delta):
        self.spawner()
        self.time_elapsed += delta
        super().run(delta)

    def spawner(self):
        # TODO: better spawn system
        if random.random() < 0.002:
            self.spawn_slime()

    def spawn_slime(self):
        r = random.random()
        c = 0
        for chance, slime in self.slime_chances:
            c += chance
            if r <= c:
                new_slime = slime(
                    self.game,
                    (random.randint(200, 2000), random.randint(200, 1800)),
                    [self.render_sprites, self.enemy_group],
                    self.collision_sprites,
                    self.player_group
                )
                new_slime.target = self.player
                self.enemies.append(new_slime)
                break
