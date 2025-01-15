from game.components.ui import Label, InlineComponents, Image
from game.settings import join

class GameHud:
    def __init__(self, game):
        self.game = game

        # self.player_life = Label(
        #     "Life: 0",
        #     pos=(20, 20),
        #     color=(255, 255, 255),
        #     size=32,
        # )
        self.player_life = InlineComponents(
            pos_x=30,
            pos_y=30,
            offset_x=45,
            offset_y=0,
            icons=[
                Image(
                    pos=(0, 0),
                    path=join('assets', 'hud', 'Heart.png'),
                ),
                Image(
                    pos=(0, 0),
                    path=join('assets', 'hud', 'Heart.png'),
                ),
                Image(
                    pos=(0, 0),
                    path=join('assets', 'hud', 'Heart.png'),
                ),
            ]
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
        self.player_life.update(delta)
        self.player_life.set_render_amount(self.game.level.player.health.health)

    def render(self, delta):
        for component in self.components:
            component.render(self.game.screen)
