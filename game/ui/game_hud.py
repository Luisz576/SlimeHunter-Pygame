from game.components.ui import Label

class GameHud:
    def __init__(self, game):
        self.game = game

        self.player_life = Label(
            "Life: 0",
            pos=(20, 20),
            color=(255, 255, 255),
            size=32,
        )
        self.score = Label(
            "Score: 0",
            pos=(600, 20),
            color=(255, 255, 255),
            size=32,
        )

        # components
        self.components = [
            self.player_life,
            self.score
        ]

    def update(self, delta):
        self.score.change_text(f"Score: {self.game.game_score}")
        self.player_life.change_text(f"Life: {self.game.level.player.health.health}/{self.game.level.player.health.max_health}")

    def render(self, delta):
        for component in self.components:
            component.render(self.game.screen)
