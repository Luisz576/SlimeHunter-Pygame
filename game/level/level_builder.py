from game.settings import *
from game.level import Levels, MenuLevel, MonsterLevel


def level_builder(level, game):
    if level == Levels.MENU:
        return MenuLevel(game)
    if level == Levels.WORLD_1:
        return MonsterLevel(game, join('map', 'world_1.tmx'), ['floor', 'walls'], ['collisions'], 3)
