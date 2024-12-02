from game.settings import *
from game.level import Levels, MenuLevel, MonsterLevel, GameOverLevel
from game.level.entity.slime import NormalSlime


def level_builder(level, game):
    if level == Levels.MENU:
        return MenuLevel(game)
    elif level == Levels.GAME_OVER:
        return GameOverLevel(game)
    elif level == Levels.WORLD_1:
        return MonsterLevel(
            game=game,
            map_path=join('map', 'world_1.tmx'),
            map_layers=['floor', 'walls'],
            map_collision_layers=['collisions'],
            tile_scale=3,
            slime_chances=[
                (1, NormalSlime)
            ]
        )
