from game.components.ui import Label, InlineComponents, Image
from game.settings import join


MAX_HEALTH = 5
MAX_ARROWS_INV = 16


class GameHud:
    def __init__(self, game):
        self.game = game

        # self.player_life = Label(
        #     "Life: 0",
        #     pos=(20, 20),
        #     color=(255, 255, 255),
        #     size=32,
        # )
        heart_icons = []
        for i in range(MAX_HEALTH):
            heart_icons.append(
                Image(
                    pos=(0, 0),
                    path=join('assets', 'hud', 'Heart.png'),
                )
            )
        self.player_life = InlineComponents(
            pos_x=30,
            pos_y=30,
            offset_x=45,
            offset_y=0,
            icons=heart_icons
        )
        self.difficulty = Label(
            "Difficulty: 0",
            pos=(580, 60),
            color=(255, 255, 255),
            size=32,
        )
        self.enemies = Label(
            "Enemies: 0",
            pos=(580, 100),
            color=(255, 255, 255),
            size=32,
        )
        self.score = Label(
            "Score: 0",
            pos=(580, 20),
            color=(255, 255, 255),
            size=32,
        )
        # inventory
        arrows_icons = []
        for i in range(MAX_ARROWS_INV):
            arrows_icons.append(
                Image(
                    pos=(0, 0),
                    path=join('assets', 'hud', 'arrow.png'),
                )
            )
        self.inventory_arrows = InlineComponents(
            pos_x=20,
            pos_y=560,
            offset_x=48,
            offset_y=0,
            icons=arrows_icons
        )

        # components
        self.components = [
            self.player_life,
            self.score,
            self.difficulty,
            self.inventory_arrows,
            self.enemies
        ]

    def update(self, delta):
        self.score.change_text(f"Score: {self.game.game_score}")
        self.difficulty.change_text(f"Difficulty: {self.game.level.current_difficult}")
        self.enemies.change_text(f"Enemies: {len(self.game.level.enemies)}")
        self.player_life.set_render_amount(self.game.level.player.health.health)
        self.player_life.update(delta)
        self.inventory_arrows.set_render_amount(self.game.level.player.inventory.arrows())
        self.inventory_arrows.update(delta)

    def render(self, delta):
        for component in self.components:
            component.render(self.game.screen)
