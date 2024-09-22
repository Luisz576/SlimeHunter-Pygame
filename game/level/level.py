from game.settings import *
from .map import Map
from game.components import RenderSpritesGroup, CollisionSpritesGroup
from game.level.entity import Player, Players, Slime, Slimes


class Levels(Enum):
    WORLD_1 = 0


class Level:
    def __init__(self, map_path, map_layers, map_collision_layers):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.render_sprites = RenderSpritesGroup()
        self.collision_sprites = CollisionSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, map_collision_layers, self.render_sprites,
                       collision_group=self.collision_sprites)
        # player
        self.player = Player(
            (random.randint(10, 600), random.randint(10, 600)),
            self.render_sprites,
            self.collision_sprites,
            Players.SOLDIER
        )

        # TODO: temp
        Slime(
            (random.randint(10, 600), random.randint(10, 600)),
            self.render_sprites,
            self.collision_sprites,
            Slimes.NORMAL_SLIME
        )

    def run(self, delta):
        self.display_surface.fill(COLORS['black'])
        # sprites
        self.render_sprites.draw(self.player.rect.center)
        self.render_sprites.update(delta)


def level_builder(level):
    if level == Levels.WORLD_1:
        return Level(join('map', 'world_1.tmx'), ['floor', 'walls'], ['collisions'])
