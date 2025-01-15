from game.level import Levels

class Level:
    def __init__(self, game):
        self.game = game

    def is_paused(self):
        return False

    def kill_entity(self, entity):
        pass

    def game_over(self):
        self.game.load_level(Levels.GAME_OVER)

    def run(self, delta):
        pass

    def unload_level(self):
        pass
