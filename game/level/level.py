from game.settings import *
from game.level.hud import Hud
from .map import Map
from game.components import RenderSpritesGroup, CollisionSpritesGroup
from game.level.entity import Player, Players, Slime, Slimes


class Levels(Enum):
    WORLD_1 = 0


class Level:
    def __init__(self, map_path, map_layers, map_collision_layers, tile_scale):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.render_sprites = RenderSpritesGroup()
        self.collision_sprites = CollisionSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, map_collision_layers, self.render_sprites,
                       collision_group=self.collision_sprites, tile_scale=tile_scale)
        self.enemies = []
        # player
        self.player = Player(
            (400, 400),
            self.render_sprites,
            self.collision_sprites,
            Players.SOLDIER
        )
        # hud
        self.hud = Hud(self)

    def run(self, delta):
        self.display_surface.fill(COLORS['black'])
        self.spawner()
        self.hud.update(delta)
        # sprites
        self.render_sprites.draw(self.player.rect.center)
        self.render_sprites.update(delta)
        self.hud.draw()

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


def level_builder(level):
    if level == Levels.WORLD_1:
        return Level(join('map', 'world_1.tmx'), ['floor', 'walls'], ['collisions'], 3)
