import random
from game.level import MapLevel
from game.settings import SLIME_CHANCES_TO_SPAWN_BASED_ON_TIME, MAX_DIFFICULT, SPANW_NEAR_PLAYER_RANGE


class MonsterLevel(MapLevel):
    # slime_chances => [ (Chance, SlimeClass), ... ]
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale, slime_chances, background_music_path):
        super().__init__(game, map_path, map_layers, map_collision_layers, tile_scale, background_music_path)
        self.slime_chances = slime_chances
        self.time_elapsed = 0
        self.current_difficult = 0
        self.amount_spawned = 0

    def run(self, delta):
        self.spawner()
        self.time_elapsed += delta
        super().run(delta)

    def spawner(self):
        if random.random() < SLIME_CHANCES_TO_SPAWN_BASED_ON_TIME[self.current_difficult]:
            self.spawn_slime()
            if self.amount_spawned % 10 == 0:
                if self.current_difficult >= MAX_DIFFICULT:
                    return
                self.current_difficult = min(self.current_difficult+1, MAX_DIFFICULT)

    def hardcore(self):
        self.current_difficult = 100

    def spawn_slime(self):
        r = random.random()
        c = 0
        self.amount_spawned += 1
        for chance, slime in self.slime_chances:
            c += chance
            if r <= c:
                new_slime = slime(
                    self.game,
                    self.spawn_near_to_player(),
                    [self.render_sprites, self.enemy_group],
                    self.collision_sprites,
                    self.player_group
                )
                new_slime.target = self.player
                self.enemies.append(new_slime)
                break

    def spawn_near_to_player(self):
        x = self.player.rect.x
        y = self.player.rect.y
        minSpawnX = max(100, x - SPANW_NEAR_PLAYER_RANGE)
        maxSpawnX = min(2700, x + SPANW_NEAR_PLAYER_RANGE)
        minSpawnY = max(100, y - SPANW_NEAR_PLAYER_RANGE)
        maxSpawnY = min(1700, y + SPANW_NEAR_PLAYER_RANGE)
        return random.randint(minSpawnX, maxSpawnX), random.randint(minSpawnY, maxSpawnY)
