from game.settings import *
from game.level import MenuLevel, MonsterLevel


class Levels(Enum):
    MENU = 0,
    WORLD_1 = 5


def level_builder(level):
    if level == Levels.MENU:
        return MenuLevel()
    if level == Levels.WORLD_1:
        return MonsterLevel(join('map', 'world_1.tmx'), ['floor', 'walls'], ['collisions'], 3)
