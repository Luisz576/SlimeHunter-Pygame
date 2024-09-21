from game.settings import *
from .map import Map
from game.components import AllSpritesGroup
from game.level.entity import Player, get_player_data, Players


class Levels(Enum):
    WORLD_1 = 0


class Level:
    def __init__(self, map_path, map_layers):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = AllSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, self.all_sprites)
        # player
        self.player = Player(
            (random.randint(10, 600), random.randint(10, 600)),
            self.all_sprites,
            get_player_data(Players.SOLDIER)
        )

    def run(self, delta):
        self.display_surface.fill(COLORS['black'])
        # sprites
        self.all_sprites.draw(self.player.rect.center)
        self.all_sprites.update(delta)


def level_builder(level):
    if level == Levels.WORLD_1:
        return Level(join('map', 'world_1.tmx'), ['floor', 'walls'])
